#!/usr/bin/env python3
"""Genera las páginas de PS Plus y Game Pass de cada mes desde datos/suscripciones.js.

  /ps-plus-octubre-2026      los juegos del mes de PlayStation Plus
  /game-pass-octubre-2026    lo que entra a Game Pass ese mes

Por qué existen (29/09/2026): son búsquedas que vuelven todos los meses y que el sitio no
tenía dónde recibir. Las noticias cuentan cada anuncio el día que sale; la página junta el
mes entero, tanda por tanda, y enlaza a las fichas de los que están en el calendario.

Un mes sin tandas no genera página, y las páginas de meses que ya no están en el archivo
de datos se borran, para que no queden colgadas en el sitemap.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-suscripciones.py

Se regenera con la rutina diaria (scripts/actualizar.py lo invoca).
"""
import datetime
import html as html_mod
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comun import MESES_ES, PLATS, cargar_juegos

import plantilla

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://lanzamientos.lat"
ARCHIVO = RAIZ / "datos" / "suscripciones.js"
SERVICIOS = {
    "psplus": {"slug": "ps-plus", "nombre": "PS Plus", "largo": "PlayStation Plus"},
    "gamepass": {"slug": "game-pass", "nombre": "Game Pass", "largo": "Xbox Game Pass"},
}


def e(t):
    return html_mod.escape(str(t), quote=True)


def leer():
    """La lista SUSCRIPCIONES del archivo de datos, con el mismo truco que cargar_juegos():
    se ancla en la declaración y se le ponen comillas a las claves para leerlo como JSON."""
    if not ARCHIVO.exists():
        return []
    src = ARCHIVO.read_text(encoding="utf-8")
    inicio = src.index("[", src.index("const SUSCRIPCIONES"))
    fin = src.index("];", inicio) + 1
    cuerpo = src[inicio:fin]
    return json.loads(re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M))


def ruta(servicio, mes):
    return f"/{SERVICIOS[servicio]['slug']}-{MESES_ES[int(mes[5:7]) - 1].lower()}-{mes[:4]}"


def nombre_mes(mes):
    return f"{MESES_ES[int(mes[5:7]) - 1].title()} de {mes[:4]}"


def fecha_corta(f):
    y, m, d = map(int, f.split("-"))
    return f"{d} de {MESES_ES[m - 1].lower()}"


def tarjeta(item, fichas):
    j = fichas.get(item.get("id")) if item.get("id") else None
    # Casi ningún juego de suscripción está en el calendario (son de años anteriores), así
    # que el archivo de datos puede traer su propia carátula; la de la ficha manda si existe.
    imagen = (j or {}).get("imagen") or item.get("imagen")
    portada = (f'<img class="rec-portada" src="{e(imagen)}" alt="Carátula de {e(item["titulo"])}" '
               f'loading="lazy" decoding="async">') if imagen else '<span class="rec-portada portada-vacia"></span>'
    plats = " ".join(f'<span class="plat plat-{p.lower()}">{e(PLATS.get(p, p))}</span>'
                     for p in item.get("plataformas", []))
    entra = f'ENTRA EL {fecha_corta(item["entra"]).upper()}' if item.get("entra") else ""
    interior = f'''        {portada}
        <div class="rec-cuerpo">
          <div class="rec-fecha">{e(entra)}</div>
          <h3 class="rec-titulo">{e(item["titulo"])}</h3>
          <div class="plataformas">{plats}</div>
          <p class="rec-texto">{e(item.get("texto", ""))}</p>
        </div>'''
    # Sólo es enlace si hay ficha: un <a> que no lleva a ningún lado confunde.
    if j:
        return f'      <a class="rec" href="/juegos/{e(j["id"])}">\n{interior}\n      </a>'
    return f'      <div class="rec">\n{interior}\n      </div>'


def pagina(entrada, fichas, meses_servicio):
    serv = SERVICIOS[entrada["servicio"]]
    mes = entrada["mes"]
    url = ruta(entrada["servicio"], mes)
    titulo = f"{serv['nombre']} {nombre_mes(mes).replace(' de ', ' ')}"
    total = sum(len(t["juegos"]) for t in entrada["tandas"])
    descripcion = (f"Todos los juegos de {serv['largo']} de {nombre_mes(mes).lower()}: "
                   f"{total} juegos, cuándo entran y qué plan hace falta para cada uno.")
    intro = entrada.get("intro") or descripcion

    bloques = []
    for t in entrada["tandas"]:
        fuente = (f' · <a href="{e(t["fuente"])}" rel="noopener" target="_blank">FUENTE OFICIAL</a>'
                  if t.get("fuente") else "")
        tarjetas = "\n".join(tarjeta(i, fichas) for i in t["juegos"])
        bloques.append(f'''    <h2 class="sus-tanda">{e(t["nombre"])}</h2>
    <p class="sus-detalle">{e(t.get("detalle", ""))}{fuente}</p>
    <div class="recomendados">
{tarjetas}
    </div>''')

    meses_btn = "\n".join(
        f'        <a class="filtro-btn{" activo" if m == mes else ""}" href="{ruta(entrada["servicio"], m)}">'
        f'{e(nombre_mes(m).upper())}</a>' for m in sorted(meses_servicio, reverse=True))
    nav = (f'    <nav class="rec-meses" aria-label="Meses">\n{meses_btn}\n    </nav>\n'
           if len(meses_servicio) > 1 else "")

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(descripcion)}">
  <title>{e(titulo)}: todos los juegos del mes — LANZAMIENTOS.LAT</title>
  <link rel="canonical" href="{DOMINIO}{url}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#000000">
  <link rel="apple-touch-icon" href="/icon-192.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LANZAMIENTOS.LAT">
  <meta property="og:title" content="{e(titulo)}: todos los juegos del mes">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{DOMINIO}{url}">
  <meta property="og:image" content="{DOMINIO}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .pagina-titulo  {{ font-size: 1.25rem; color: var(--blanco); letter-spacing: 3px; margin-bottom: 0.25rem; }}
    .pagina-sub     {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 1.5rem; }}
    .rec-meses      {{ display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.9rem 0 1.5rem; }}
    .rec-meses .filtro-btn {{ text-decoration: none; display: inline-block; }}
    .rec-intro      {{ font-size: 0.8125rem; color: var(--gris-7); line-height: 1.9; max-width: 720px; margin-bottom: 2rem; }}
    .sus-tanda      {{ font-size: 0.875rem; color: var(--acento); letter-spacing: 3px; font-weight: normal;
                      border-bottom: 1px solid var(--gris-2); padding-bottom: 0.5rem; margin: 2rem 0 0.4rem; max-width: 720px; }}
    .sus-detalle    {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 1px; line-height: 1.8; margin-bottom: 1.5rem; max-width: 720px; }}
    .sus-otro       {{ margin-top: 2rem; }}
    .sus-otro a     {{ text-decoration: none; display: inline-block; }}
    .recomendados   {{ max-width: 720px; }}
    .rec            {{ display: flex; gap: 1.25rem; align-items: flex-start; color: inherit;
                      border-left: 2px solid var(--gris-3); padding: 0 0 1.5rem 1.25rem; margin-bottom: 1.5rem; }}
    a.rec:hover     {{ border-left-color: var(--acento); }}
    a.rec:hover .rec-titulo {{ color: var(--acento); }}
    .rec-portada    {{ width: 96px; height: 144px; object-fit: cover; flex-shrink: 0;
                      border: 1px solid var(--gris-3); background: var(--gris-1); display: block; }}
    .rec-cuerpo     {{ min-width: 0; flex: 1; }}
    .rec-fecha      {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 0.35rem; }}
    .rec-titulo     {{ font-size: 0.9375rem; color: var(--blanco); letter-spacing: 1px; font-weight: 700; line-height: 1.5; margin-bottom: 0.5rem; }}
    .rec-texto      {{ font-size: 0.8125rem; color: var(--gris-7); line-height: 1.9; margin-top: 0.6rem; }}
    @media (max-width: 600px) {{
      .rec          {{ gap: 0.9rem; padding-left: 0.9rem; }}
      .rec-portada  {{ width: 72px; height: 108px; }}
    }}
  </style>
</head>
<body>

{plantilla.cabecera(None)}

  <main class="contenedor">
    <a href="/" class="volver">◀ VOLVER AL CALENDARIO</a>
{nav}    <h1 class="pagina-titulo">{e(titulo.upper())}</h1>
    <p class="pagina-sub">{total} JUEGO{"S" if total != 1 else ""} · {e(serv["largo"].upper())}</p>
    <p class="rec-intro">{e(intro)}</p>
{chr(10).join(bloques)}
    <p class="sus-otro"><a class="filtro-btn" href="/{MESES_ES[int(mes[5:7]) - 1].lower()}-{mes[:4]}">TODOS LOS LANZAMIENTOS DE {e(nombre_mes(mes).upper())}</a></p>
  </main>

{plantilla.pie()}

  <script src="/js/favoritos.js"></script>
  <script>
{plantilla.script_tema()}
  </script>
</body>
</html>
'''


INICIO_PORTADA = "<!-- SUSCRIPCIONES:INICIO — lo escribe scripts/generar-suscripciones.py, no editar a mano -->"
FIN_PORTADA = "<!-- SUSCRIPCIONES:FIN -->"


def portada(datos):
    """Escribe en index.html los botones a las páginas del mes en curso y del siguiente.

    El siguiente también, porque Sony y Xbox anuncian antes de que empiece el mes: el
    30/09 ya existe la de octubre y es la que se busca. Va en HTML estático entre dos
    marcadores, y no armado con JavaScript, para que Google siga el enlace desde la
    portada, que es la página que más rastrea. Sin páginas vigentes, el bloque queda vacío."""
    hoy = datetime.date.today()
    sig = (hoy.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
    vigentes = {f"{hoy:%Y-%m}", f"{sig:%Y-%m}"}
    orden = list(SERVICIOS)
    elegidos = sorted((d for d in datos if d["mes"] in vigentes),
                      key=lambda d: (d["mes"], orden.index(d["servicio"])))
    if elegidos:
        botones = "\n".join(
            f'            <a class="filtro-btn" href="{ruta(d["servicio"], d["mes"])}">'
            f'{SERVICIOS[d["servicio"]]["nombre"].upper()} DE {MESES_ES[int(d["mes"][5:7]) - 1].upper()}</a>'
            for d in elegidos)
        bloque = (f'{INICIO_PORTADA}\n        <div class="filtros">\n'
                  f'          <div class="filtros-label">PS PLUS Y GAME PASS:</div>\n'
                  f'          <div class="filtros-botones">\n{botones}\n          </div>\n        </div>\n'
                  f'        {FIN_PORTADA}')
    else:
        bloque = f"{INICIO_PORTADA}\n        {FIN_PORTADA}"
    index = RAIZ / "index.html"
    src = index.read_text(encoding="utf-8")
    if INICIO_PORTADA not in src or FIN_PORTADA not in src:
        print("  ⚠ index.html no tiene los marcadores de SUSCRIPCIONES: la portada no enlaza las páginas")
        return
    a = src.index(INICIO_PORTADA)
    b = src.index(FIN_PORTADA) + len(FIN_PORTADA)
    nuevo = src[:a] + bloque + src[b:]
    if nuevo != src:
        index.write_text(nuevo, encoding="utf-8")
    print(f"  portada: {', '.join(ruta(d['servicio'], d['mes']) for d in elegidos) or 'sin páginas vigentes'}")


def main():
    datos = [d for d in leer() if d.get("tandas")]
    fichas = {j["id"]: j for j in cargar_juegos()}
    generadas = set()
    for d in datos:
        faltan = [i["id"] for t in d["tandas"] for i in t["juegos"] if i.get("id") and i["id"] not in fichas]
        if faltan:
            print(f"  ⚠ {ruta(d['servicio'], d['mes'])}: ids que no están en juegos.js: {', '.join(faltan)}")
        meses_servicio = [x["mes"] for x in datos if x["servicio"] == d["servicio"]]
        archivo = ruta(d["servicio"], d["mes"]).lstrip("/") + ".html"
        (RAIZ / archivo).write_text(pagina(d, fichas, meses_servicio), encoding="utf-8")
        generadas.add(archivo)
    viejas = [f for f in list(RAIZ.glob("ps-plus-*-20??.html")) + list(RAIZ.glob("game-pass-*-20??.html"))
              if f.name not in generadas]
    for f in viejas:
        f.unlink()
    print(f"  {len(generadas)} página(s) de PS Plus y Game Pass"
          + (f": {', '.join(sorted(g[:-5] for g in generadas))}" if generadas else "")
          + (f" ({len(viejas)} viejas borradas)" if viejas else ""))
    portada(datos)


if __name__ == "__main__":
    main()
