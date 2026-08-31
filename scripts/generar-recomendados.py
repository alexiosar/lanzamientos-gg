#!/usr/bin/env python3
"""Genera recomendados.html: la selección del mes, elegida a mano.

Por qué existe y por qué no es el ranking: el ranking ordena por puntaje de Metacritic y
sólo muestra juegos ya lanzados, así que del mes que arranca no puede decir nada. Y es
justo del mes que arranca de lo que la gente quiere que le digan algo. Con 106 juegos en
septiembre de 2026, una lista por fecha no ayuda a decidir qué mirar.

Los datos salen de datos/recomendados.js, que trae el mes y una línea propia por juego.
Todo lo demás —carátula, fecha, plataformas— se lee de datos/juegos.js, así que no hay
nada duplicado: si un juego se retrasa, esta página se entera sola.

Se genera estática, igual que /noticias, porque el objetivo es que Google la indexe.

Si el mes de recomendados.js no es el mes en curso, la página lo dice en vez de hacer
pasar por actual una selección vieja.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-recomendados.py

Se regenera con la rutina diaria (scripts/actualizar.py lo invoca). La lista nueva se
arma en la rutina mensual.
"""
import datetime
import html as html_mod
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://lanzamientos.lat"
MESES_ES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
PLATS = {"PS5": "PS5", "PS4": "PS4", "XBOX": "Xbox", "SWITCH2": "Switch 2", "SWITCH": "Switch"}


def e(t):
    return html_mod.escape(str(t), quote=True)


def _leer(archivo, marca):
    """Los datos son JS, no JSON: se recorta el objeto y se le ponen comillas a las claves."""
    src = (RAIZ / "datos" / archivo).read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1]
    cuerpo = cuerpo[:cuerpo.rindex(marca) + 1].strip()
    return json.loads(re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M))


def fecha_larga(f):
    a, m, d = f.split("-")
    return f"{int(d)} DE {MESES_ES[int(m) - 1]}"


def tarjeta(rec, j):
    plats = " ".join(f'<span class="plat plat-{p.lower()}">{e(PLATS.get(p, p))}</span>'
                     for p in j["plataformas"])
    if j.get("imagen"):
        portada = (f'<img class="rec-portada" src="{e(j["imagen"])}" '
                   f'alt="Carátula de {e(j["titulo"])}" loading="lazy" decoding="async">')
    else:
        portada = '<span class="rec-portada portada-vacia"></span>'
    return f'''      <a class="rec" href="/juegos/{e(j["id"])}">
        {portada}
        <div class="rec-cuerpo">
          <div class="rec-fecha">{e(fecha_larga(j["fecha"]))}</div>
          <h2 class="rec-titulo">{e(j["titulo"])}</h2>
          <div class="plataformas">{plats}</div>
          <p class="rec-texto">{e(rec["texto"])}</p>
        </div>
      </a>'''


def main():
    juegos = {x["id"]: x for x in _leer("juegos.js", "]")}
    datos = _leer("recomendados.js", "}")
    mes = datos["mes"]
    anio_mes = MESES_ES[int(mes[5:7]) - 1] + " " + mes[:4]
    hoy = datetime.date.today()
    # Publicar la selección antes de que empiece el mes es lo normal y no se avisa: a fin
    # de agosto la de septiembre ya tiene que estar. Lo que sí se avisa es que quedó vieja,
    # porque una lista de "recomendados del mes" del mes pasado engaña al que llega.
    vigente = mes >= hoy.strftime("%Y-%m")

    faltan = [r["id"] for r in datos["juegos"] if r["id"] not in juegos]
    if faltan:
        print(f"  ⚠ {len(faltan)} recomendado(s) que no están en juegos.js: {', '.join(faltan)}")
    elegidos = [(r, juegos[r["id"]]) for r in datos["juegos"] if r["id"] in juegos]
    # Por fecha de salida: la página se lee de arriba abajo como el mes que viene.
    elegidos.sort(key=lambda p: p[1]["fecha"])

    # Un recomendado que se retrasó a otro mes deja de tener sentido acá, y no se detecta
    # mirando la página: la tarjeta sigue igual de prolija con la fecha nueva.
    fuera = [j["id"] for _, j in elegidos if j["fecha"][:7] != mes]
    if fuera:
        print(f"  ⚠ {len(fuera)} recomendado(s) que ya no salen en {mes}: {', '.join(fuera)}")

    cuerpo = "\n".join(tarjeta(r, j) for r, j in elegidos)
    descripcion = (f"Los {len(elegidos)} juegos de {anio_mes.lower()} que vale la pena mirar, "
                   "elegidos uno por uno: fechas, plataformas y por qué cada uno está en la lista.")
    aviso = "" if vigente else (
        f'      <p class="rec-aviso">Esta selección es de {e(anio_mes.lower())} y quedó vieja. '
        'La del mes en curso todavía no se publicó.</p>\n')

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(descripcion)}">
  <title>Los Mejores Juegos de {anio_mes.title()} — Recomendados | LANZAMIENTOS.LAT</title>
  <link rel="canonical" href="{DOMINIO}/recomendados">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#000000">
  <link rel="apple-touch-icon" href="/icon-192.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LANZAMIENTOS.LAT">
  <meta property="og:title" content="Los mejores juegos de {anio_mes.title()} — LANZAMIENTOS.LAT">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{DOMINIO}/recomendados">
  <meta property="og:image" content="{DOMINIO}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .pagina-titulo   {{ font-size: 1.25rem; color: var(--blanco); letter-spacing: 3px; margin-bottom: 0.25rem; }}
    .pagina-sub      {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 1.5rem; }}
    .rec-intro       {{ font-size: 0.8125rem; color: var(--gris-7); line-height: 1.9; max-width: 720px; margin-bottom: 2rem; }}
    .rec-aviso       {{ font-size: 0.75rem; color: var(--amarillo); letter-spacing: 1px; margin-bottom: 1.5rem; }}
    .recomendados    {{ max-width: 720px; }}
    /* Mismo esqueleto que una tarjeta de noticia: borde a la izquierda, carátula vertical
       y el texto al lado. La carátula es más grande que en /noticias porque acá la imagen
       es media razón para entrar. */
    .rec             {{ display: flex; gap: 1.25rem; align-items: flex-start; color: inherit;
                       border-left: 2px solid var(--gris-3); padding: 0 0 1.75rem 1.25rem;
                       margin-bottom: 1.75rem; transition: border-color 0.1s; }}
    .rec:hover       {{ border-left-color: var(--acento); }}
    .rec:hover .rec-titulo {{ color: var(--acento); }}
    .rec-portada     {{ width: 120px; height: 180px; object-fit: cover; flex-shrink: 0;
                       border: 1px solid var(--gris-3); background: var(--gris-1); display: block; }}
    .rec-cuerpo      {{ min-width: 0; flex: 1; }}
    .rec-fecha       {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 0.35rem; }}
    .rec-titulo      {{ font-size: 0.9375rem; color: var(--blanco); letter-spacing: 1px;
                       font-weight: 700; line-height: 1.5; margin-bottom: 0.5rem; }}
    .rec-texto       {{ font-size: 0.8125rem; color: var(--gris-7); line-height: 1.9; margin-top: 0.6rem; }}
    /* Lo define cada página en su bloque inline, no css/style.css. Sin esto el enlace sale
       con el estilo por omisión y se nota al lado del resto del sitio. */
    .volver          {{ display: inline-block; font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 1.5rem; }}
    .volver:hover    {{ color: var(--acento); }}
    @media (max-width: 600px) {{
      .rec           {{ gap: 0.9rem; padding-left: 0.9rem; }}
      .rec-portada   {{ width: 84px; height: 126px; }}
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="contenedor">
      <button class="btn-tema" onclick="toggleTema()" id="btn-tema" title="Cambiar tema" aria-label="Cambiar tema">☾</button>
      <a href="/" class="site-logo">LANZAMIENTOS.LAT</a>
      <span class="site-tagline">▸ CALENDARIO DE VIDEOJUEGOS EN ESPAÑOL ◂</span>
      <nav class="nav">
        <a href="/">INICIO</a>
        <a href="/recomendados" class="activo">RECOMENDADOS</a>
        <a href="/noticias">NOTICIAS</a>
        <a href="/ps5">PS5</a>
        <a href="/xbox">XBOX</a>
        <a href="/switch-2">SWITCH 2</a>
        <a href="/switch">SWITCH</a>
        <a href="/ps4">PS4</a>
      </nav>
    </div>
  </header>

  <main class="contenedor">
    <a href="/" class="volver">◀ VOLVER AL CALENDARIO</a>
    <h1 class="pagina-titulo">RECOMENDADOS DE {e(anio_mes)}</h1>
    <p class="pagina-sub">{len(elegidos)} JUEGOS ELEGIDOS A MANO</p>
{aviso}    <p class="rec-intro">El ranking del sitio ordena por puntaje, y por eso sólo habla de
      juegos que ya salieron. Esta lista es lo contrario: son los que todavía no salieron y
      vale la pena tener en el radar. No hay nota que los ordene, así que están elegidos uno
      por uno y en cada caso decimos por qué.</p>

    <div class="recomendados">
{cuerpo}
    </div>
  </main>

  <footer class="site-footer">
    <div class="contenedor" style="display:flex; justify-content:space-between; width:100%; flex-wrap:wrap; gap:0.5rem;">
      <span>LANZAMIENTOS.LAT &copy; {hoy.year}</span>
      <span class="footer-links"><a href="/acerca">ACERCA DE</a> · <a href="/api">API</a> · <a href="/widget">WIDGET</a> · <a href="/privacidad">PRIVACIDAD</a> · <a href="/terminos">TÉRMINOS</a> · <a href="/rss.xml">RSS</a></span>
      <span>DATOS: STEAM · NINTENDO · METACRITIC · HLTB <span class="cursor"></span></span>
    </div>
  </footer>

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
    sistemaClaro.addEventListener("change", ev => {{
      if (!localStorage.getItem("tema")) aplicarTema(ev.matches);
    }});
    if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
  </script>
</body>
</html>
'''
    (RAIZ / "recomendados.html").write_text(html, encoding="utf-8")
    print(f"recomendados.html generada: {len(elegidos)} juegos de {anio_mes}"
          + ("" if vigente else "  ⚠ SELECCIÓN VIEJA: armar la del mes en curso"))


if __name__ == "__main__":
    main()
