// ── VOTOS: "¿LO VAS A JUGAR?" ──
//
// El sitio sigue siendo archivos estáticos: Cloudflare sirve primero cualquier archivo que
// exista, y este Worker sólo recibe lo que no coincide con ninguno. De eso atiende una sola
// ruta, /votos, y todo lo demás lo devuelve a los assets para que el 404 siga siendo el de
// siempre.
//
//   GET  /votos/<id>   → { si, talvez, no, total }
//   POST /votos/<id>   body { votante, voto }  → los conteos actualizados
//                      voto: "si" | "talvez" | "no" | null (null borra el voto)
//
// Los votos viven en un Durable Object con SQLite. Se eligió así y no D1 ni KV porque no
// hay que crear nada a mano en el panel: la clase y su base se crean solas en el deploy,
// con la migración declarada en wrangler.jsonc.
//
// Qué se guarda y qué no (lo mismo que dice /privacidad):
//   - Un identificador al azar que genera el navegador. No es un dato de nadie: identifica
//     a un navegador, no a una persona, y sirve para que un voto se pueda cambiar sin
//     sumarse dos veces.
//   - La IP NO se guarda. Para frenar abusos se cuenta cuántos votos llegan de una misma IP
//     por hora, pero lo que se anota es un hash con una sal al azar que cambia todos los
//     días, y esas filas se borran a la hora. Con la sal descartada no hay forma de volver
//     a la IP. No se limita a un voto por IP porque en Argentina y el resto de la región
//     muchas conexiones móviles comparten la misma IP pública entre miles de personas.

import { DurableObject } from "cloudflare:workers";

const OPCIONES = ["si", "talvez", "no"];
const POR_HORA = 60;                       // votos por IP en una hora
const ORIGENES = ["https://lanzamientos.lat", "https://www.lanzamientos.lat"];

function json(datos, estado = 200) {
  return new Response(JSON.stringify(datos), {
    status: estado,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}

export class Votos extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.env = env;
    this.ids = null;
    ctx.blockConcurrencyWhile(async () => {
      this.ctx.storage.sql.exec(`
        CREATE TABLE IF NOT EXISTS votos (
          juego   TEXT NOT NULL,
          votante TEXT NOT NULL,
          voto    TEXT NOT NULL,
          fecha   INTEGER NOT NULL,
          PRIMARY KEY (juego, votante)
        );
        CREATE TABLE IF NOT EXISTS limites (
          clave TEXT NOT NULL,
          hora  INTEGER NOT NULL,
          n     INTEGER NOT NULL,
          PRIMARY KEY (clave, hora)
        );
        CREATE TABLE IF NOT EXISTS sal (dia TEXT PRIMARY KEY, valor TEXT NOT NULL);
      `);
    });
  }

  // Sólo se aceptan ids que existen en el calendario, para que nadie llene la base de
  // basura. La lista sale de la API pública del propio sitio y se relee cada hora.
  async idValido(id, origen) {
    const ahora = Date.now();
    if (!this.ids || ahora - this.idsFecha > 3600_000) {
      try {
        const r = await this.env.ASSETS.fetch(new Request(origen + "/api/juegos.json"));
        const datos = await r.json();
        const lista = Array.isArray(datos) ? datos : (datos.juegos || []);
        this.ids = new Set(lista.map(j => j.id));
        this.idsFecha = ahora;
      } catch (e) {
        if (!this.ids) return true;   // si la API falla, no se rompe el voto
      }
    }
    return this.ids.has(id);
  }

  conteos(juego) {
    const res = { si: 0, talvez: 0, no: 0, total: 0 };
    for (const fila of this.ctx.storage.sql.exec(
      "SELECT voto, COUNT(*) AS n FROM votos WHERE juego = ? GROUP BY voto", juego)) {
      if (OPCIONES.includes(fila.voto)) { res[fila.voto] = fila.n; res.total += fila.n; }
    }
    return res;
  }

  async salDelDia() {
    const dia = new Date().toISOString().slice(0, 10);
    const fila = [...this.ctx.storage.sql.exec("SELECT valor FROM sal WHERE dia = ?", dia)][0];
    if (fila) return fila.valor;
    const valor = crypto.randomUUID();
    this.ctx.storage.sql.exec("DELETE FROM sal");
    this.ctx.storage.sql.exec("INSERT INTO sal (dia, valor) VALUES (?, ?)", dia, valor);
    return valor;
  }

  async permitido(ip) {
    const sal = await this.salDelDia();
    const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(sal + ip));
    const clave = [...new Uint8Array(bytes)].slice(0, 12).map(b => b.toString(16).padStart(2, "0")).join("");
    const hora = Math.floor(Date.now() / 3600_000);
    this.ctx.storage.sql.exec("DELETE FROM limites WHERE hora < ?", hora);
    const fila = [...this.ctx.storage.sql.exec(
      "SELECT n FROM limites WHERE clave = ? AND hora = ?", clave, hora)][0];
    if (fila && fila.n >= POR_HORA) return false;
    this.ctx.storage.sql.exec(
      `INSERT INTO limites (clave, hora, n) VALUES (?, ?, 1)
       ON CONFLICT (clave, hora) DO UPDATE SET n = n + 1`, clave, hora);
    return true;
  }

  async leer(juego, origen) {
    if (!(await this.idValido(juego, origen))) return { error: "juego", estado: 404 };
    return this.conteos(juego);
  }

  async votar(juego, votante, voto, ip, origen) {
    if (!(await this.idValido(juego, origen))) return { error: "juego", estado: 404 };
    if (!(await this.permitido(ip))) return { error: "limite", estado: 429 };
    if (voto === null) {
      this.ctx.storage.sql.exec("DELETE FROM votos WHERE juego = ? AND votante = ?", juego, votante);
    } else {
      this.ctx.storage.sql.exec(
        `INSERT INTO votos (juego, votante, voto, fecha) VALUES (?, ?, ?, ?)
         ON CONFLICT (juego, votante) DO UPDATE SET voto = excluded.voto, fecha = excluded.fecha`,
        juego, votante, voto, Date.now());
    }
    return this.conteos(juego);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const m = url.pathname.match(/^\/votos\/([a-z0-9-]{1,120})\/?$/);
    if (!m) return env.ASSETS.fetch(request);

    const juego = m[1];
    const origen = url.origin;
    // Una sola instancia para todo el sitio: el volumen de un calendario no necesita más.
    const votos = env.VOTOS.get(env.VOTOS.idFromName("sitio"));

    if (request.method === "GET") {
      const res = await votos.leer(juego, origen);
      return res.error ? json({ error: res.error }, res.estado) : json(res);
    }

    if (request.method === "POST") {
      // Sólo desde el propio sitio. En desarrollo local (wrangler dev) el origen es localhost.
      const cabecera = request.headers.get("Origin") || "";
      const local = /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(cabecera);
      if (!ORIGENES.includes(cabecera) && cabecera !== origen && !local) return json({ error: "origen" }, 403);

      let cuerpo;
      try { cuerpo = await request.json(); } catch (e) { return json({ error: "cuerpo" }, 400); }
      const votante = typeof cuerpo.votante === "string" && /^[a-f0-9-]{20,40}$/.test(cuerpo.votante) ? cuerpo.votante : null;
      const voto = cuerpo.voto === null ? null : (OPCIONES.includes(cuerpo.voto) ? cuerpo.voto : undefined);
      if (!votante || voto === undefined) return json({ error: "cuerpo" }, 400);

      const ip = request.headers.get("CF-Connecting-IP") || "local";
      const res = await votos.votar(juego, votante, voto, ip, origen);
      return res.error ? json({ error: res.error }, res.estado) : json(res);
    }

    return json({ error: "metodo" }, 405);
  },
};
