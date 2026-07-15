#!/usr/bin/env python3
"""Genera una página HTML estática por juego en juegos/{id}.html a partir de datos/juegos.js.

Ventajas sobre juego.html?id= (que se arma con JavaScript):
- Open Graph por juego: al compartir en WhatsApp/X se ve la carátula del juego.
- Google indexa el contenido completo sin ejecutar JS.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-fichas.py

Correr después de cada cambio en datos/juegos.js (junto con generar-sitemap.py).
"""
import html as html_mod
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://lanzamientos.lat"
MESES_ES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]


def cargar_juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1].strip().rstrip(";")
    # claves sin comillas -> JSON (las claves siempre abren línea)
    cuerpo = re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M)
    return json.loads(cuerpo)


def e(t):
    return html_mod.escape(str(t), quote=True)


def plat_class(p):
    return {"PS5": "plat-PS5", "PS4": "plat-PS4", "XBOX": "plat-XBOX",
            "SWITCH2": "plat-SWITCH2", "SWITCH": "plat-SWITCH"}.get(p, "plat-MULTI")


def plat_label(p):
    return "SWITCH 2" if p == "SWITCH2" else p


def meta_clase(n):
    return "meta-alto" if n >= 75 else ("meta-medio" if n >= 50 else "meta-bajo")


def generar(j):
    gid = j["id"]
    y, m, d = map(int, j["fecha"].split("-"))
    fecha_str = f"{d:02d} {MESES_ES[m-1]} {y}"
    url = f"{DOMINIO}/juegos/{gid}.html"
    desc_corta = j["descripcion"][:150].rsplit(" ", 1)[0] + "…"
    og_imagen = j.get("imagen") or f"{DOMINIO}/og-image.png"

    plats_html = "".join(f'<span class="plat {plat_class(p)}">{plat_label(p)}</span>' for p in j["plataformas"])
    tags_html = "".join(f'<span class="tag">{e(g)}</span>' for g in j["genero"]) + \
        "".join(f'<span class="plat {plat_class(p)}" style="font-size:0.6875rem;padding:2px 7px;">{plat_label(p)}</span>' for p in j["plataformas"]) + \
        ('<span class="tag tag-gamepass">GAME PASS</span>' if j.get("gamepass") else "") + \
        ('<span class="tag tag-psplus">PS PLUS</span>' if j.get("psplus") else "")

    incluido = " &nbsp; ".join(filter(None, [
        '<span class="ficha-campo-valor badge-gamepass">GAME PASS ✓</span>' if j.get("gamepass") else "",
        '<span class="ficha-campo-valor badge-psplus">PS PLUS ✓</span>' if j.get("psplus") else "",
    ])) or '<span class="ficha-campo-valor">—</span>'

    metacritic_html = ""
    if j.get("metacritic"):
        metacritic_html = f'''
            <div>
              <span class="ficha-campo-label">METACRITIC</span>
              <span class="badge-metacritic {meta_clase(j["metacritic"])}">{j["metacritic"]}</span>
            </div>'''

    portada_html = ""
    if j.get("imagen"):
        portada_html = f'<img class="portada-page" src="{e(j["imagen"])}" alt="Portada de {e(j["titulo"])}" loading="lazy" onerror="this.remove()" onload="if(this.naturalWidth>this.naturalHeight)this.classList.add(\'apaisada\')">'

    noticias_html = ""
    if j.get("noticias"):
        items = "".join(f'''
        <div class="noticia">
          <div class="noticia-linea">
            <span class="noticia-fecha">{e(n["fecha"])}</span>
            <span class="noticia-titulo">▸ {e(n["titulo"])}</span>
          </div>
          <p class="noticia-texto">{e(n["texto"])}</p>
        </div>''' for n in j["noticias"])
        noticias_html = f'''
      <div class="seccion">
        <div class="seccion-titulo">ÚLTIMAS NOVEDADES</div>{items}
      </div>'''

    trailer_html = ""
    if j.get("trailer"):
        trailer_html = f'''
      <div class="seccion">
        <div class="seccion-titulo">TRAILER OFICIAL</div>
        <div class="video-wrapper">
          <iframe src="{e(j["trailer"])}" title="Trailer de {e(j["titulo"])}" allowfullscreen allow="autoplay" loading="lazy"></iframe>
        </div>
      </div>'''

    datos_ld = {
        "@context": "https://schema.org",
        "@type": "VideoGame",
        "name": j["titulo"],
        "url": url,
        "description": j["descripcion"][:300],
        "datePublished": j["fecha"],
        "gamePlatform": [plat_label(p) for p in j["plataformas"]],
        "genre": j["genero"],
        "inLanguage": "es",
        "author": {"@type": "Organization", "name": j["desarrollador"]},
    }
    if j.get("imagen"):
        datos_ld["image"] = j["imagen"]

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(j["titulo"])} — fecha de lanzamiento, plataformas, puntaje y trailer. {e(desc_corta)}">
  <title>{e(j["titulo"])} — LANZAMIENTOS.LAT</title>
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#000000">
  <link rel="apple-touch-icon" href="/icon-192.png">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LANZAMIENTOS.LAT">
  <meta property="og:title" content="{e(j["titulo"])} — {fecha_str}">
  <meta property="og:description" content="{e(desc_corta)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{e(og_imagen)}">
  <meta property="og:locale" content="es_LA">
  <meta name="twitter:card" content="summary_large_image">

  <script type="application/ld+json">{json.dumps(datos_ld, ensure_ascii=False)}</script>

  <link rel="stylesheet" href="../css/style.css">
  <style>
    .ficha-page        {{ padding: 2rem 0; }}
    .breadcrumb        {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 1px; margin-bottom: 1.5rem; }}
    .breadcrumb a      {{ color: var(--gris-5); }}
    .breadcrumb a:hover{{ color: var(--acento); }}
    .juego-titulo-page {{ font-size: 1.375rem; color: var(--blanco); letter-spacing: 3px; margin-bottom: 0.25rem; }}
    .juego-dev-page    {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 1.5rem; }}
    .seccion           {{ margin-bottom: 2rem; border-top: 1px solid var(--gris-2); padding-top: 1rem; }}
    .seccion-titulo    {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 3px; margin-bottom: 0.75rem; }}
    .descripcion-page  {{ color: var(--gris-7); font-size: 0.8125rem; line-height: 2; border-left: 2px solid var(--gris-3); padding-left: 1rem; }}
    .meta-grid         {{ display: flex; gap: 2rem; flex-wrap: wrap; }}
    .noticia           {{ margin-bottom: 1rem; border-left: 2px solid var(--gris-3); padding-left: 1rem; }}
    .noticia-linea     {{ margin-bottom: 0.25rem; }}
    .noticia-fecha     {{ color: var(--acento); font-size: 0.6875rem; letter-spacing: 1px; margin-right: 0.5rem; }}
    .noticia-titulo    {{ color: var(--blanco); font-size: 0.75rem; letter-spacing: 1px; }}
    .noticia-texto     {{ color: var(--gris-7); font-size: 0.75rem; line-height: 1.8; }}
    .juego-hero        {{ display: flex; gap: 2rem; align-items: flex-start; flex-wrap: wrap; }}
    .juego-hero-info   {{ flex: 1; min-width: 260px; }}
    .portada-page      {{ width: 160px; flex-shrink: 0; border: 1px solid var(--gris-3); display: block; }}
    .portada-page.apaisada {{ width: 280px; max-width: 100%; }}
    .video-wrapper     {{ position: relative; padding-bottom: 56.25%; height: 0; border: 1px solid var(--gris-3); background: var(--negro); }}
    .video-wrapper iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: none; }}
    .volver            {{ display: inline-block; font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 1.5rem; }}
    .volver:hover      {{ color: var(--acento); }}
    .badge-gamepass    {{ color: var(--xbox); }}
    .badge-psplus      {{ color: var(--ps5); }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="contenedor">
      <button class="btn-tema" onclick="toggleTema()" id="btn-tema" title="Cambiar tema" aria-label="Cambiar tema">☾</button>
      <a href="../index.html" class="site-logo">LANZAMIENTOS.LAT</a>
      <span class="site-tagline">▸ CALENDARIO DE VIDEOJUEGOS EN ESPAÑOL ◂</span>
      <nav class="nav">
        <a href="../index.html">INICIO</a>
        <a href="../index.html?plat=PS5">PS5</a>
        <a href="../index.html?plat=XBOX">XBOX</a>
        <a href="../index.html?plat=SWITCH2">SWITCH 2</a>
        <a href="../index.html?plat=SWITCH">SWITCH</a>
        <a href="../index.html?plat=PS4">PS4</a>
      </nav>
    </div>
  </header>

  <main class="contenedor">
    <div class="ficha-page">
      <a href="../index.html" class="volver">◀ VOLVER AL CALENDARIO</a>

      <div class="breadcrumb">
        <a href="../index.html">INICIO</a> &gt;
        <a href="../index.html?plat={j["plataformas"][0]}">{plat_label(j["plataformas"][0])}</a> &gt;
        {e(j["titulo"])}
      </div>

      <div class="juego-hero">
        {portada_html}
        <div class="juego-hero-info">
          <h1 class="juego-titulo-page">{e(j["titulo"])}</h1>
          <p class="juego-dev-page">{e(j["desarrollador"])}</p>

          <div class="seccion">
            <div class="seccion-titulo">DATOS</div>
            <div class="meta-grid">
              <div>
                <span class="ficha-campo-label">FECHA DE LANZAMIENTO</span>
                <span class="ficha-campo-valor">{fecha_str}</span>
                <span class="cuenta-regresiva" id="regresiva" data-fecha="{j["fecha"]}"></span>{f'''
                <span class="relanzamiento">↺ {e(j["relanzamiento"])}</span>''' if j.get("relanzamiento") else ""}
              </div>
              <div>
                <span class="ficha-campo-label">PLATAFORMAS</span>
                <div class="plataformas" style="margin-top:3px;">{plats_html}</div>
              </div>
              <div>
                <span class="ficha-campo-label">GÉNERO</span>
                <span class="ficha-campo-valor">{e(" / ".join(j["genero"]))}</span>
              </div>{f'''
              <div>
                <span class="ficha-campo-label">DURACIÓN</span>
                <span class="ficha-campo-valor">{e(j["duracion"])}</span>
              </div>''' if j.get("duracion") else ""}
              <div>
                <span class="ficha-campo-label">INCLUIDO EN</span>
                {incluido}
              </div>{metacritic_html}
            </div>
            <div style="margin-top:1rem;">
              <button class="btn-trailer" id="btn-agendar" onclick="agendarJuego('{gid}')" style="display:none">◷ AGENDAR LANZAMIENTO</button>
            </div>
          </div>
        </div>
      </div>
{noticias_html}
      <div class="seccion">
        <div class="seccion-titulo">DESCRIPCIÓN</div>
        <p class="descripcion-page">{e(j["descripcion"])}</p>
      </div>

      <div class="seccion">
        <div class="seccion-titulo">TAGS</div>
        <div class="ficha-tags">{tags_html}</div>
      </div>
{trailer_html}
    </div>
  </main>

  <footer class="site-footer">
    <div class="contenedor" style="display:flex;justify-content:space-between;width:100%;flex-wrap:wrap;gap:.5rem;">
      <span>LANZAMIENTOS.LAT &copy; 2026</span>
      <span class="footer-links"><a href="../acerca.html">ACERCA DE</a> · <a href="../privacidad.html">PRIVACIDAD</a> · <a href="../terminos.html">TÉRMINOS</a></span>
      <span>DATOS: STEAM · NINTENDO · METACRITIC · HLTB <span class="cursor"></span></span>
    </div>
  </footer>

  <script src="../datos/juegos.js"></script>
  <script>
    function toggleTema() {{
      const claro = document.documentElement.classList.toggle("tema-claro");
      document.getElementById("btn-tema").textContent = claro ? "☀" : "☾";
      localStorage.setItem("tema", claro ? "claro" : "oscuro");
    }}
    function aplicarTema(claro) {{
      document.documentElement.classList.toggle("tema-claro", claro);
      document.getElementById("btn-tema").textContent = claro ? "☀" : "☾";
    }}
    const temaGuardado = localStorage.getItem("tema");
    const sistemaClaro = window.matchMedia("(prefers-color-scheme: light)");
    aplicarTema(temaGuardado ? temaGuardado === "claro" : sistemaClaro.matches);
    sistemaClaro.addEventListener("change", e => {{
      if (!localStorage.getItem("tema")) aplicarTema(e.matches);
    }});
    if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");

    // cuenta regresiva y botón agendar, calculados al cargar (no se congelan al generar)
    (function () {{
      const el = document.getElementById("regresiva");
      const [y, m, d] = el.dataset.fecha.split("-").map(Number);
      const hoy = new Date(); hoy.setHours(0, 0, 0, 0);
      const dias = Math.round((new Date(y, m - 1, d) - hoy) / 864e5);
      if (dias === 0) {{ el.textContent = "▸ ¡SALE HOY!"; el.classList.add("regresiva-hoy"); }}
      else if (dias === 1) el.textContent = "▸ FALTA 1 DÍA";
      else if (dias > 1) el.textContent = "▸ FALTAN " + dias + " DÍAS";
      else el.remove();
      if (dias > 0) document.getElementById("btn-agendar").style.display = "";
    }})();

    function agendarJuego(id) {{
      const j = JUEGOS.find(x => x.id === id);
      if (!j) return;
      const [y, m, d] = j.fecha.split("-").map(Number);
      const inicio = j.fecha.replace(/-/g, "");
      const fin = new Date(y, m - 1, d + 1);
      const finStr = `${{fin.getFullYear()}}${{String(fin.getMonth() + 1).padStart(2, "0")}}${{String(fin.getDate()).padStart(2, "0")}}`;
      const ahora = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      const esc = t => t.replace(/\\\\/g, "\\\\\\\\").replace(/[,;]/g, s => "\\\\" + s);
      const etiqueta = p => p === "SWITCH2" ? "SWITCH 2" : p;
      const ics = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//lanzamientos.lat//Calendario de Videojuegos//ES",
        "BEGIN:VEVENT",
        `UID:${{j.id}}@lanzamientos.lat`,
        `DTSTAMP:${{ahora}}`,
        `DTSTART;VALUE=DATE:${{inicio}}`,
        `DTEND;VALUE=DATE:${{finStr}}`,
        `SUMMARY:${{esc("🎮 Sale " + j.titulo)}}`,
        `DESCRIPTION:${{esc(`Lanzamiento en ${{j.plataformas.map(etiqueta).join(" / ")}}. Ficha: https://lanzamientos.lat/juegos/${{j.id}}.html`)}}`,
        `URL:https://lanzamientos.lat/juegos/${{j.id}}.html`,
        "END:VEVENT", "END:VCALENDAR"
      ].join("\\r\\n");
      const blob = new Blob([ics], {{ type: "text/calendar;charset=utf-8" }});
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `${{j.id}}.ics`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(a.href);
    }}
  </script>
</body>
</html>
'''


def main():
    juegos = cargar_juegos()
    destino = RAIZ / "juegos"
    generadas = 0
    for j in juegos:
        (destino / f'{j["id"]}.html').write_text(generar(j), encoding="utf-8")
        generadas += 1
    # limpiar fichas de juegos que ya no existen
    ids = {j["id"] for j in juegos}
    borradas = 0
    for f in destino.glob("*.html"):
        if f.stem != "juego" and f.stem not in ids:
            f.unlink()
            borradas += 1
    print(f"{generadas} fichas generadas en juegos/ ({borradas} obsoletas borradas)")


if __name__ == "__main__":
    main()
