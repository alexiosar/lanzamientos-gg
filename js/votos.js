// ── ¿LO VAS A JUGAR? ──
//
// Tres botones en la ficha (SÍ / TAL VEZ / NO) contra el Worker de /votos. Sin cuentas: el
// navegador genera un identificador al azar la primera vez y lo manda con cada voto, para
// que cambiar de opinión reemplace el voto en lugar de sumar otro.
//
// El bloque sale oculto en el HTML y sólo aparece si el Worker responde. Así, si /votos
// falla o se abre la ficha con el servidor local de Python (que no corre el Worker), la
// ficha se ve igual que antes y no queda un recuadro roto.
//
// Los porcentajes se muestran recién con VOTOS_MINIMO votos. Con dos o tres, un "100% SÍ"
// no dice nada y un "0 votos" hace que la ficha parezca abandonada.

const VOTOS_MINIMO = 5;
const VOTOS_CLAVE = "votos";
const VOTOS_ETIQUETAS = { si: "SÍ", talvez: "TAL VEZ", no: "NO" };

function votosLeerLocal() {
  try {
    const crudo = JSON.parse(localStorage.getItem(VOTOS_CLAVE) || "{}");
    return crudo && typeof crudo === "object" ? crudo : {};
  } catch (e) {
    return {};
  }
}

function votosGuardarLocal(datos) {
  try { localStorage.setItem(VOTOS_CLAVE, JSON.stringify(datos)); } catch (e) {}
}

function votosVotante() {
  const datos = votosLeerLocal();
  if (typeof datos._votante !== "string") {
    datos._votante = (crypto.randomUUID ? crypto.randomUUID()
      : "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, c => {
          const r = Math.random() * 16 | 0;
          return (c === "x" ? r : (r & 0x3 | 0x8)).toString(16);
        }));
    votosGuardarLocal(datos);
  }
  return datos._votante;
}

function votosPintar(caja, conteos, propio) {
  caja.querySelectorAll("[data-voto]").forEach(btn => {
    const activo = btn.dataset.voto === propio;
    btn.classList.toggle("activo", activo);
    btn.setAttribute("aria-pressed", activo ? "true" : "false");
  });

  const resultado = caja.querySelector(".votos-resultado");
  if (conteos && conteos.total >= VOTOS_MINIMO) {
    const pct = k => Math.round(conteos[k] * 100 / conteos.total);
    resultado.innerHTML =
      ["si", "talvez", "no"].map(k =>
        `<div class="votos-fila"><span class="votos-etq">${VOTOS_ETIQUETAS[k]}</span>` +
        `<span class="votos-barra"><span style="width:${pct(k)}%"></span></span>` +
        `<span class="votos-pct">${pct(k)}%</span></div>`).join("") +
      `<div class="votos-total">${conteos.total} ${conteos.total === 1 ? "VOTO" : "VOTOS"}</div>`;
    resultado.hidden = false;
  } else {
    resultado.innerHTML = "";
    resultado.hidden = true;
  }
}

async function votosIniciar() {
  const caja = document.getElementById("votos");
  if (!caja || !window.fetch) return;
  const juego = caja.dataset.juego;
  const propio = votosLeerLocal()[juego] || null;

  let conteos;
  try {
    const r = await fetch(`/votos/${juego}`, { headers: { Accept: "application/json" } });
    if (!r.ok) return;
    conteos = await r.json();
  } catch (e) {
    return;
  }

  caja.hidden = false;
  votosPintar(caja, conteos, propio);

  caja.querySelectorAll("[data-voto]").forEach(btn => {
    btn.addEventListener("click", async () => {
      // Un voto por vez: si el anterior todavía no volvió, el segundo clic leería un estado
      // viejo y podría deshacer lo que el primero acaba de guardar.
      if (caja.classList.contains("enviando")) return;
      const locales = votosLeerLocal();
      const anterior = locales[juego] || null;
      // Tocar la opción ya elegida la desmarca.
      const nuevo = btn.dataset.voto === anterior ? null : btn.dataset.voto;

      caja.classList.add("enviando");
      caja.querySelector(".votos-aviso").hidden = true;
      // Se marca antes de que responda el servidor; si falla, se vuelve a lo que había.
      votosPintar(caja, conteos, nuevo);
      try {
        const r = await fetch(`/votos/${juego}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ votante: votosVotante(), voto: nuevo }),
        });
        if (!r.ok) throw new Error(r.status);
        const actual = votosLeerLocal();
        if (nuevo) actual[juego] = nuevo; else delete actual[juego];
        votosGuardarLocal(actual);
        conteos = await r.json();
        votosPintar(caja, conteos, nuevo);
      } catch (e) {
        votosPintar(caja, conteos, anterior);
        caja.querySelector(".votos-aviso").hidden = false;
      } finally {
        caja.classList.remove("enviando");
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", votosIniciar);
