#!/usr/bin/env python3
"""Una página por mes: /septiembre-2026, /octubre-2026, etc.

Por qué existen. Al 01/09/2026 el sitio tenía 361 páginas indexadas y 4.870 impresiones,
pero 32 clics: posición media 28, o sea que aparece en la página 3 de resultados. Ese
problema no se arregla con funciones nuevas, se arregla teniendo páginas que apunten a
búsquedas donde la competencia sea flaca. "Juegos que salen en septiembre de 2026" es una
de esas: existe, se repite doce veces por año y tenemos el dato verificado para
contestarla. Hasta ahora el sitio no tenía dónde recibir esa consulta.

No suman mantenimiento: salen enteras de datos/juegos.js y se regeneran con la rutina
diaria. No hay ningún campo nuevo que alguien tenga que llenar.

Los meses ya pasados también se generan, y ahí está el otro motivo: los juegos lanzados
salen de la portada y quedan en /archivo, con sus puntajes y sus resúmenes de crítica sin
que nadie los mire. "Juegos que salieron en agosto de 2026" es una página útil que hasta
hoy no existía.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-meses.py

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


def cargar_juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1]
    cuerpo = cuerpo[:cuerpo.rindex("]") + 1].strip()
    return json.loads(re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M))


def e(t):
    return html_mod.escape(str(t), quote=True)


def plat_class(p):
    return {"PS5": "plat-PS5", "PS4": "plat-PS4", "XBOX": "plat-XBOX",
            "SWITCH2": "plat-SWITCH2", "SWITCH": "plat-SWITCH"}.get(p, "plat-MULTI")


def plat_label(p):
    return "SWITCH 2" if p == "SWITCH2" else p


def meta_clase(n):
    return "meta-alto" if n >= 75 else ("meta-medio" if n >= 50 else "meta-bajo")


def slug(mes_key):
    y, m = mes_key.split("-")
    return f"{MESES_ES[int(m) - 1].lower()}-{y}"


def fila(j):
    plats = "".join(f'<span class="plat {plat_class(p)}">{plat_label(p)}</span>'
                    for p in j["plataformas"])
    mc = (f'<span class="badge-metacritic {meta_clase(j["metacritic"])}" '
          f'style="font-size:0.6875rem;">{j["metacritic"]}</span>') if j.get("metacritic") else ""
    dur = (f'<span class="mes-duracion">{e(j["duracion"])}</span>') if j.get("duracion") else ""
    mini = (f'<img class="mini-portada" src="{e(j["imagen"])}" alt="" loading="lazy" decoding="async">'
            if j.get("imagen") else '<span class="mini-portada"></span>')
    return f'''      <a class="fila-plat" href="/juegos/{e(j["id"])}">
        {mini}
        <span class="juego-nombre">{e(j["titulo"])}</span>
        {mc}{dur}
        <div class="plataformas">{plats}</div>
      </a>'''


def generar(mes_key, juegos_mes, anterior, siguiente, pasado):
    y, m = map(int, mes_key.split("-"))
    nombre = MESES_ES[m - 1]
    verbo = "salieron" if pasado else "salen"
    total = len(juegos_mes)

    cuerpo, dia_previo = [], None
    for j in sorted(juegos_mes, key=lambda x: (x.get("estimado", False), x["fecha"], x["titulo"])):
        clave = "estimado" if j.get("estimado") else j["fecha"]
        if clave != dia_previo:
            if j.get("estimado"):
                etiqueta = "SIN FECHA CONFIRMADA"
            else:
                yy, mm, dd = map(int, j["fecha"].split("-"))
                f = datetime.date(yy, mm, dd)
                etiqueta = f'{DIAS_ES[(f.weekday() + 1) % 7]} <span>{dd:02d} {nombre[:3]}</span>'
            cuerpo.append(f'      <div class="dia-label" style="margin-top:0.75rem;">{etiqueta}</div>')
            dia_previo = clave
        cuerpo.append(fila(j))

    # Sólo entre los YA LANZADOS. Un port trae el puntaje del original, así que sin este
    # filtro un mes futuro anunciaba un "mejor puntuado" de un juego que todavía no salió:
    # septiembre de 2026 decía "Maestro con 93" el día que se generó la página. Es el mismo
    # cuidado que tienen el ranking y el destacado.
    hoy_iso = datetime.date.today().isoformat()
    con_puntaje = [j for j in juegos_mes if j.get("metacritic") and j["fecha"] <= hoy_iso]
    resumen = f"{total} juego{'s' if total != 1 else ''}"
    if con_puntaje:
        mejor = max(con_puntaje, key=lambda j: j["metacritic"])
        resumen += f" · el mejor puntuado es {mejor['titulo'].title()} con {mejor['metacritic']}"

    descripcion = (f"Todos los juegos que {verbo} en {nombre.lower()} de {y} para PS5, PS4, Xbox, "
                   f"Switch 2 y Switch: {total} lanzamientos con fecha, plataformas y puntajes.")

    def enlace_mes(mk, texto):
        return f'<a href="/{slug(mk)}">{texto}</a>' if mk else '<span class="mes-nav-vacio"></span>'

    navegacion = (f'    <div class="mes-nav">{enlace_mes(anterior, "◀ " + MESES_ES[int(anterior[5:7]) - 1].title() if anterior else "")}'
                  f'{enlace_mes(siguiente, MESES_ES[int(siguiente[5:7]) - 1].title() + " ▶" if siguiente else "")}</div>')

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(descripcion)}">
  <title>Juegos que {verbo} en {nombre.title()} de {y} — LANZAMIENTOS.LAT</title>
  <link rel="canonical" href="{DOMINIO}/{slug(mes_key)}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#000000">
  <link rel="apple-touch-icon" href="/icon-192.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LANZAMIENTOS.LAT">
  <meta property="og:title" content="Juegos que {verbo} en {nombre.title()} de {y}">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{DOMINIO}/{slug(mes_key)}">
  <meta property="og:image" content="{DOMINIO}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .pagina-titulo  {{ font-size: 1.25rem; color: var(--blanco); letter-spacing: 3px; margin-bottom: 0.25rem; }}
    .pagina-sub     {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 1.5rem; }}
    .mes-lista      {{ max-width: 760px; }}
    .mes-duracion   {{ font-size: 0.625rem; color: var(--gris-5); letter-spacing: 1px; }}
    .mes-nav        {{ display: flex; justify-content: space-between; gap: 1rem; margin: 2rem 0 0;
                      max-width: 760px; font-size: 0.6875rem; letter-spacing: 2px; }}
    .mes-nav a      {{ color: var(--gris-5); }}
    .mes-nav a:hover {{ color: var(--acento); }}
    .mes-nav-vacio  {{ flex: 1; }}
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
        <a href="/recomendados">RECOMENDADOS</a>
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
    <h1 class="pagina-titulo">JUEGOS QUE {verbo.upper()} EN {nombre} DE {y}</h1>
    <p class="pagina-sub">{e(resumen.upper())}</p>

    <div class="mes-lista">
{chr(10).join(cuerpo)}
    </div>

{navegacion}
  </main>

  <footer class="site-footer">
    <div class="contenedor" style="display:flex; justify-content:space-between; width:100%; flex-wrap:wrap; gap:0.5rem;">
      <span>LANZAMIENTOS.LAT &copy; {datetime.date.today().year}</span>
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


def main():
    juegos = cargar_juegos()
    hoy = datetime.date.today().strftime("%Y-%m")
    por_mes = {}
    for j in juegos:
        por_mes.setdefault(j["fecha"][:7], []).append(j)
    claves = sorted(por_mes)

    for i, mk in enumerate(claves):
        anterior = claves[i - 1] if i > 0 else None
        siguiente = claves[i + 1] if i < len(claves) - 1 else None
        html = generar(mk, por_mes[mk], anterior, siguiente, pasado=mk < hoy)
        (RAIZ / f"{slug(mk)}.html").write_text(html, encoding="utf-8")
    print(f"{len(claves)} páginas de mes generadas: {', '.join(slug(k) for k in claves)}")


if __name__ == "__main__":
    main()
