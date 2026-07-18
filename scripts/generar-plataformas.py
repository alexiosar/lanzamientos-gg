#!/usr/bin/env python3
"""Genera páginas estáticas por plataforma (ps5.html, xbox.html, etc.) para SEO.

Cada página lista los lanzamientos de esa plataforma (mes actual en adelante)
pre-renderizados en HTML, indexables por Google para búsquedas tipo
"lanzamientos PS5" — cosa que el filtro por JavaScript de la portada no logra.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-plataformas.py

Se regenera con la rutina diaria (scripts/actualizar.py lo invoca).
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
DIAS_ES = ["DOM", "LUN", "MAR", "MIE", "JUE", "VIE", "SAB"]

PLATAFORMAS = [
    # (clave, archivo, nombre corto nav, nombre largo)
    ("PS5", "ps5.html", "PS5", "PlayStation 5"),
    ("PS4", "ps4.html", "PS4", "PlayStation 4"),
    ("XBOX", "xbox.html", "XBOX", "Xbox Series X|S"),
    ("SWITCH2", "switch-2.html", "SWITCH 2", "Nintendo Switch 2"),
    ("SWITCH", "switch.html", "SWITCH", "Nintendo Switch"),
]


def cargar_juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1].strip().rstrip(";")
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


def nav_html(activa):
    links = [f'<a href="index.html"{" " if activa else ""}>INICIO</a>']
    for clave, archivo, corto, _ in PLATAFORMAS:
        act = ' class="activo"' if clave == activa else ""
        links.append(f'<a href="{archivo}"{act}>{corto}</a>')
    return "\n        ".join(links)


def generar(clave, archivo, corto, largo, juegos, mes_actual):
    lista = sorted([j for j in juegos if clave in j["plataformas"] and j["fecha"][:7] >= mes_actual],
                   key=lambda j: j["fecha"])
    anio = datetime.date.today().year

    # agrupar por mes
    meses = {}
    for j in lista:
        meses.setdefault(j["fecha"][:7], []).append(j)

    cuerpo = []
    for mes_key in sorted(meses):
        y, m = map(int, mes_key.split("-"))
        cuerpo.append(f'<h2 class="mes-titulo">{MESES_ES[m-1]} {y} <span class="mes-contador">[ {len(meses[mes_key])} JUEGO{"S" if len(meses[mes_key]) != 1 else ""} ]</span></h2>')
        dia_previo = None
        for j in meses[mes_key]:
            yy, mm, dd = map(int, j["fecha"].split("-"))
            f = datetime.date(yy, mm, dd)
            if j["fecha"] != dia_previo:
                cuerpo.append(f'<div class="dia-label" style="margin-top:0.75rem;">{DIAS_ES[(f.weekday()+1) % 7]} <span>{dd:02d} {MESES_ES[mm-1][:3]}</span></div>')
                dia_previo = j["fecha"]
            plats = "".join(f'<span class="plat {plat_class(p)}">{plat_label(p)}</span>'
                            for p in j["plataformas"] if p != clave)
            mc = f'<span class="badge-metacritic {meta_clase(j["metacritic"])}" style="font-size:0.6875rem;">{j["metacritic"]}</span>' if j.get("metacritic") else ""
            mini = (f'<img class="mini-portada" src="{e(j["imagen"])}" alt="" loading="lazy" decoding="async">'
                    if j.get("imagen") else '<span class="mini-portada"></span>')
            cuerpo.append(f'''<a class="fila-plat" href="juegos/{j["id"]}.html">
        {mini}
        <span class="juego-nombre">{e(j["titulo"])}</span>
        {mc}
        <div class="plataformas">{plats}</div>
      </a>''')

    descripcion = (f"Calendario de lanzamientos de juegos para {largo} en español: "
                   f"todas las fechas de salida confirmadas, con fichas, trailers y puntajes. Actualizado a diario.")

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(descripcion)}">
  <title>Lanzamientos de {largo} {anio} — Calendario en Español | LANZAMIENTOS.LAT</title>
  <link rel="canonical" href="{DOMINIO}/{archivo.replace(".html", "")}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#000000">
  <link rel="apple-touch-icon" href="/icon-192.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LANZAMIENTOS.LAT">
  <meta property="og:title" content="Lanzamientos de {largo} {anio} — Calendario en Español">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{DOMINIO}/{archivo.replace(".html", "")}">
  <meta property="og:image" content="{DOMINIO}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .pagina-titulo {{ font-size: 1.25rem; color: var(--blanco); letter-spacing: 3px; margin-bottom: 0.25rem; }}
    .pagina-sub    {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 2rem; }}
    .mes-titulo    {{ display: flex; align-items: center; gap: 0.75rem; color: var(--acento); font-size: 0.875rem; letter-spacing: 3px; margin: 2rem 0 0.5rem; border-bottom: 1px solid var(--gris-2); padding-bottom: 0.5rem; font-weight: normal; }}
    .fila-plat     {{ display: flex; align-items: center; gap: 0.75rem; padding: 6px 0.75rem; border-left: 2px solid transparent; transition: all 0.1s; flex-wrap: wrap; color: inherit; }}
    .fila-plat:hover {{ border-left-color: var(--acento); background: rgba(160,160,255,0.05); color: inherit; }}
    .fila-plat:hover .juego-nombre {{ color: var(--acento); }}
    .link-filtros  {{ display: block; text-align: center; color: var(--gris-5); font-size: 0.6875rem; letter-spacing: 2px; padding: 0.6rem 1rem; border: 1px dashed var(--gris-3); margin: 2rem 0; }}
    .link-filtros:hover {{ color: var(--acento); border-color: var(--acento); }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="contenedor">
      <button class="btn-tema" onclick="toggleTema()" id="btn-tema" title="Cambiar tema" aria-label="Cambiar tema">☾</button>
      <a href="index.html" class="site-logo">LANZAMIENTOS.LAT</a>
      <span class="site-tagline">▸ CALENDARIO DE VIDEOJUEGOS EN ESPAÑOL ◂</span>
      <nav class="nav">
        {nav_html(clave)}
      </nav>
    </div>
  </header>

  <main class="contenedor">
    <h1 class="pagina-titulo">LANZAMIENTOS DE {largo.upper()}</h1>
    <p class="pagina-sub">FECHAS DE SALIDA CONFIRMADAS — {len(lista)} JUEGOS EN CALENDARIO</p>
    {"".join(cuerpo)}
    <a class="link-filtros" href="index.html?plat={clave}">⚙ VER EN EL CALENDARIO INTERACTIVO (FILTROS Y BÚSQUEDA) →</a>
  </main>

  <footer class="site-footer">
    <div class="contenedor" style="display:flex; justify-content:space-between; width:100%; flex-wrap:wrap; gap:0.5rem;">
      <span>LANZAMIENTOS.LAT &copy; {anio}</span>
      <span class="footer-links"><a href="acerca.html">ACERCA DE</a> · <a href="privacidad.html">PRIVACIDAD</a> · <a href="terminos.html">TÉRMINOS</a></span>
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
    sistemaClaro.addEventListener("change", e => {{
      if (!localStorage.getItem("tema")) aplicarTema(e.matches);
    }});
    if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
  </script>
</body>
</html>
'''


def main():
    juegos = cargar_juegos()
    mes_actual = datetime.date.today().strftime("%Y-%m")
    for clave, archivo, corto, largo in PLATAFORMAS:
        (RAIZ / archivo).write_text(generar(clave, archivo, corto, largo, juegos, mes_actual), encoding="utf-8")
        print(f"{archivo} generada")


if __name__ == "__main__":
    main()
