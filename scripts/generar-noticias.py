#!/usr/bin/env python3
"""Genera noticias.html: todas las novedades del sitio en una sola página.

Mezcla dos fuentes y las ordena por fecha, de la más nueva a la más vieja:

  1. El campo `noticias` de cada juego en datos/juegos.js — puntajes de debut,
     retrasos de un título concreto, ediciones especiales.
  2. datos/noticias.js — las que no cuelgan de un lanzamiento: juegos mensuales
     de PS Plus y Game Pass, Directs, cierres de estudios.

Se genera estática (no con JavaScript en el navegador) porque el objetivo es
que Google la indexe: es la única parte del sitio que da una razón para volver
más de una vez por mes, y sólo sirve si se encuentra desde el buscador.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-noticias.py

Se regenera con la rutina diaria (scripts/actualizar.py lo invoca).
"""
import datetime
import html as html_mod
import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import plantilla

from comun import leer_noticias_propias

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://lanzamientos.lat"
MESES_ES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

# Cuántas mostrar. Con 97 y subiendo, volcarlas todas haría una página larguísima
# que además tarda en cargar. Las viejas siguen accesibles desde la ficha de su
# juego, que es donde tienen sentido.
TOPE = 60


def e(t):
    return html_mod.escape(str(t), quote=True)


def leer_juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    inicio, fin = src.index("["), src.rindex("]") + 1
    # datos/juegos.js es JavaScript, no JSON: las claves van sin comillas
    cuerpo = re.sub(r'(\n\s*)([a-zA-Z_][a-zA-Z0-9_]*):', r'\1"\2":', src[inicio:fin])
    return json.loads(cuerpo)


def recolectar():
    """Devuelve todas las noticias, de la más nueva a la más vieja."""
    juegos = {j["id"]: j for j in leer_juegos()}
    items = []

    for j in juegos.values():
        for n in j.get("noticias") or []:
            items.append({
                "fecha": n["fecha"],
                "titulo": n["titulo"],
                "texto": n["texto"],
                "categoria": "JUEGOS",
                "juegos": [j["id"]],
                "fuente": None,
                "imagen": None,
            })

    for n in leer_noticias_propias():
        items.append({
            "fecha": n["fecha"],
            "titulo": n["titulo"],
            "texto": n["texto"],
            "categoria": n.get("categoria", "ANUNCIOS"),
            "juegos": n.get("juegos") or [],
            "fuente": n.get("fuente"),
            "imagen": n.get("imagen"),
        })

    # Un id mal escrito en el campo `juegos` de datos/noticias.js no rompe nada:
    # simplemente no se dibuja el enlace. Como eso es imposible de notar mirando la
    # página, se avisa por consola.
    huerfanos = sorted({g for n in items for g in n["juegos"] if g not in juegos})
    if huerfanos:
        print("  ⚠ ids que no existen en datos/juegos.js: " + ", ".join(huerfanos))

    # a igual fecha, primero las propias: son las que ordenan el día
    items.sort(key=lambda x: (x["fecha"], x["categoria"] == "JUEGOS"), reverse=True)
    return items, juegos


def fecha_larga(iso):
    y, m, d = map(int, iso.split("-"))
    return f"{d:02d} {MESES_ES[m - 1][:3]} {y}"


def tarjeta(n, juegos):
    enlaces = "".join(
        f'<a class="noticia-juego" href="/juegos/{g}">{e(juegos[g]["titulo"])}</a>'
        for g in n["juegos"] if g in juegos)
    fuente = (f'<a class="noticia-fuente" href="{e(n["fuente"])}" rel="nofollow noopener" '
              f'target="_blank">FUENTE ↗</a>') if n.get("fuente") else ""

    # La carátula del juego del que habla la noticia. Ya la tenemos cargada, así que
    # la página pasa de ser una lista de texto a algo que se mira, sin buscar nada
    # nuevo ni pedir una imagen más al servidor de la que ya se pediría.
    # Las noticias propias que no citan ningún juego (un Direct, un cierre de
    # estudio) van sin imagen: no hay una que las represente de verdad.
    # Primero la imagen propia de la noticia, si la tiene: es para las que no citan
    # ningún juego del calendario y se eligió a mano. Si no, la carátula del juego
    # del que habla, que ya está cargada.
    portada = ""
    if n.get("imagen"):
        portada = (f'<span class="noticia-portada">'
                   f'<img src="{e(n["imagen"])}" alt="" loading="lazy" decoding="async"></span>')
    else:
        con_imagen = [juegos[g] for g in n["juegos"] if g in juegos and juegos[g].get("imagen")]
        if con_imagen:
            j = con_imagen[0]
            portada = (f'<a class="noticia-portada" href="/juegos/{j["id"]}" tabindex="-1" aria-hidden="true">'
                       f'<img src="{e(j["imagen"])}" alt="" loading="lazy" decoding="async"></a>')

    return f'''      <article class="noticia{" noticia-con-portada" if portada else ""}">
        {portada}
        <div class="noticia-cuerpo">
          <div class="noticia-meta">
            <time datetime="{n["fecha"]}">{fecha_larga(n["fecha"])}</time>
            <span class="noticia-cat cat-{n["categoria"].lower()}">{e(n["categoria"])}</span>
          </div>
          <h2 class="noticia-titulo">{e(n["titulo"])}</h2>
          <p class="noticia-texto">{e(n["texto"])}</p>
          <div class="noticia-pie">{enlaces}{fuente}</div>
        </div>
      </article>'''


def generar(items, juegos):
    visibles = items[:TOPE]
    anio = datetime.date.today().year
    descripcion = ("Novedades de los lanzamientos de videojuegos en español: puntajes de estreno, "
                   "retrasos, y qué entra cada mes a PlayStation Plus y Xbox Game Pass.")

    cuerpo = "\n".join(tarjeta(n, juegos) for n in visibles)

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(descripcion)}">
  <title>Noticias de Videojuegos {anio} — Novedades y Lanzamientos | LANZAMIENTOS.LAT</title>
  <link rel="canonical" href="{DOMINIO}/noticias">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#000000">
  <link rel="apple-touch-icon" href="/icon-192.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LANZAMIENTOS.LAT">
  <meta property="og:title" content="Noticias de Videojuegos {anio} — LANZAMIENTOS.LAT">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{DOMINIO}/noticias">
  <meta property="og:image" content="{DOMINIO}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="alternate" type="application/rss+xml" title="Novedades de LANZAMIENTOS.LAT" href="/rss.xml">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .pagina-titulo   {{ font-size: 1.25rem; color: var(--blanco); letter-spacing: 3px; margin-bottom: 0.25rem; }}
    .pagina-sub      {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 2rem; }}
    .noticias        {{ max-width: 720px; }}
    .noticia         {{ border-left: 2px solid var(--gris-3); padding: 0 0 1.5rem 1.25rem; margin-bottom: 1.5rem; }}
    .noticia:hover   {{ border-left-color: var(--acento); }}
    .noticia-meta    {{ display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 0.4rem; }}
    .noticia-meta time {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; }}
    .noticia-cat     {{ font-size: 0.625rem; letter-spacing: 2px; border: 1px solid; padding: 1px 7px; color: var(--gris-6); border-color: var(--gris-4); }}
    .cat-suscripciones {{ color: var(--xbox); border-color: var(--xbox); }}
    .cat-retrasos    {{ color: var(--switch); border-color: var(--switch); }}
    .cat-anuncios    {{ color: var(--ps5); border-color: var(--ps5); }}
    .cat-eventos     {{ color: var(--amarillo); border-color: var(--amarillo); }}
    /* El borde punteado dice "esto no está confirmado" sin tener que leer nada. */
    .cat-rumores     {{ color: var(--gris-6); border-color: var(--gris-5); border-style: dashed; }}
    .noticia-con-portada {{ display: flex; gap: 1rem; align-items: flex-start; }}
    .noticia-cuerpo  {{ min-width: 0; flex: 1; }}
    /* 2:3 y no cuadrada, por lo mismo que las miniaturas del calendario: recortar un arte
       de tapa a un cuadrado le come los costados y deja el centro, que es donde no está el
       logo. Con la forma de la caja se reconoce el juego sin leer el título. */
    .noticia-portada {{ flex-shrink: 0; display: block; width: 96px; height: 144px; border: 1px solid var(--gris-3); background: var(--gris-1); }}
    .noticia-portada img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    @media (max-width: 600px) {{ .noticia-portada {{ width: 72px; height: 108px; }} }}
    .noticia-titulo  {{ font-size: 0.875rem; color: var(--blanco); letter-spacing: 1px; font-weight: 700; margin-bottom: 0.5rem; line-height: 1.5; }}
    .noticia-texto   {{ font-size: 0.8125rem; color: var(--gris-7); line-height: 1.9; margin-bottom: 0.6rem; }}
    .noticia-pie     {{ display: flex; gap: 0.5rem; flex-wrap: wrap; }}
    .noticia-juego   {{ font-size: 0.6875rem; letter-spacing: 1px; border: 1px solid var(--gris-4); color: var(--gris-6); padding: 2px 8px; }}
    .noticia-juego:hover {{ border-color: var(--acento); color: var(--acento); }}
    .noticia-fuente  {{ font-size: 0.6875rem; letter-spacing: 1px; color: var(--gris-5); padding: 2px 8px; }}
    .noticia-fuente:hover {{ color: var(--acento); }}
    .noticias-pie    {{ font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 1px; line-height: 1.9; border-top: 1px solid var(--gris-2); padding-top: 1rem; margin-top: 1rem; }}
  </style>
</head>
<body>

{plantilla.cabecera("/noticias")}

  <main class="contenedor">
    <a href="/" class="volver">◀ VOLVER AL CALENDARIO</a>
    <h1 class="pagina-titulo">NOTICIAS</h1>
    <p class="pagina-sub">PUNTAJES DE ESTRENO · RETRASOS · PS PLUS Y GAME PASS</p>

    <div class="noticias">
{cuerpo}
      <p class="noticias-pie">Se muestran las {len(visibles)} novedades más recientes de {len(items)}.
        Las anteriores siguen en la ficha de cada juego.<br>
        También salen por <a href="/rss.xml">RSS</a>.</p>
    </div>
  </main>

{plantilla.pie()}

  <script src="/js/favoritos.js"></script>
  <script>
{plantilla.script_tema()}
  </script>
</body>
</html>
'''


if __name__ == "__main__":
    items, juegos = recolectar()
    (RAIZ / "noticias.html").write_text(generar(items, juegos), encoding="utf-8")
    print(f"noticias.html generada: {min(len(items), TOPE)} de {len(items)} novedades")
