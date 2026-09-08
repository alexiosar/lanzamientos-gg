#!/usr/bin/env python3
"""Genera las páginas de recomendados: la selección del mes, elegida a mano.

Son dos cosas distintas y salen del mismo archivo de datos:

  /recomendados                    el mes en curso (el campo `mes` de recomendados.js)
  /mejores-juegos-agosto-2026      cada mes ya pasado (la lista `anteriores`)

Por qué existen y por qué no es el ranking: el ranking ordena por puntaje de Metacritic y
sólo muestra juegos ya lanzados, así que del mes que arranca no puede decir nada. Y es
justo del mes que arranca de lo que la gente quiere que le digan algo. Con 106 juegos en
septiembre de 2026, una lista por fecha no ayuda a decidir qué mirar.

Por qué los meses pasados también tienen página (desde el 08/09/2026): la lista de agosto
era trabajo ya hecho que no leía nadie, porque vivía comentada dentro del archivo de datos.
Y una selección vieja no es peor que una nueva, es distinta: cuando el mes terminó los
puntajes están, así que la misma lista dice MÁS que el día que se escribió. Además apunta a
una búsqueda que existe todos los meses —"mejores juegos de agosto de 2026"— y que el sitio
no tenía dónde recibir.

Los datos duros —carátula, fecha, plataformas, puntaje— se leen de datos/juegos.js, así que
no hay nada duplicado: si un juego se retrasa, esta página se entera sola.

Se generan estáticas, igual que /noticias, porque el objetivo es que Google las indexe.

Si el mes de recomendados.js no es el mes en curso, /recomendados lo dice en vez de hacer
pasar por actual una selección vieja.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-recomendados.py

Se regenera con la rutina diaria (scripts/actualizar.py lo invoca). La lista nueva se
arma en la rutina mensual, y ahí el mes que termina se mueve a `anteriores`.
"""
import datetime
import html as html_mod
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comun import MESES_ES, PLATS, cargar_juegos, leer_recomendados, ruta_recomendados

import plantilla

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://lanzamientos.lat"


def e(t):
    return html_mod.escape(str(t), quote=True)


def fecha_larga(f):
    a, m, d = f.split("-")
    return f"{int(d)} DE {MESES_ES[int(m) - 1]}"


def nombre_mes(mes):
    """"2026-08" → "AGOSTO 2026". Para títulos y botones, que van en mayúsculas."""
    return MESES_ES[int(mes[5:7]) - 1] + " " + mes[:4]


def mes_prosa(mes):
    """"2026-08" → "agosto de 2026". Para las frases, donde falta el "de" del medio."""
    return MESES_ES[int(mes[5:7]) - 1].lower() + " de " + mes[:4]


def ruta(mes, datos):
    """La URL de la selección de ese mes. La arma comun.py, que es quien la sabe."""
    return ruta_recomendados(mes, datos)


def tarjeta(rec, j, hoy):
    plats = " ".join(f'<span class="plat plat-{p.lower()}">{e(PLATS.get(p, p))}</span>'
                     for p in j["plataformas"])
    if j.get("imagen"):
        portada = (f'<img class="rec-portada" src="{e(j["imagen"])}" '
                   f'alt="Carátula de {e(j["titulo"])}" loading="lazy" decoding="async">')
    else:
        portada = '<span class="rec-portada portada-vacia"></span>'
    # El puntaje sólo si el juego YA salió, que es el mismo cuidado que tienen el ranking,
    # el destacado y las páginas de mes: un port arrastra la nota del original, así que sin
    # este filtro una lista de lanzamientos futuros mostraría notas de juegos que no salieron
    # —The Witcher 3 en Switch 2 con su 92 de 2015— y eso no es un puntaje, es un espejismo.
    # En las páginas de meses cerrados salen todos, y ahí es medio motivo de la página: la
    # lista se escribió sin notas y ahora se puede leer con las notas al lado.
    nota = ""
    if j.get("metacritic") and j["fecha"] <= hoy:
        clase = ("alto" if j["metacritic"] >= 75 else
                 "medio" if j["metacritic"] >= 50 else "bajo")
        nota = f'<span class="rec-meta meta-{clase}">{j["metacritic"]}</span>'
    return f'''      <a class="rec" href="/juegos/{e(j["id"])}">
        {portada}
        <div class="rec-cuerpo">
          <div class="rec-fecha">{e(fecha_larga(j["fecha"]))}{nota}</div>
          <h2 class="rec-titulo">{e(j["titulo"])}</h2>
          <div class="plataformas">{plats}</div>
          <p class="rec-texto">{e(rec["texto"])}</p>
        </div>
      </a>'''


def botones(meses, mes, datos):
    """Los botones de mes, con el mismo cuadrado que los filtros de la portada.

    Sin esto las páginas de meses pasados no las encuentra nadie: quedarían colgando del
    sitemap, que es la forma más débil de que Google descubra una página, y un lector que
    llegó a la de agosto no tendría cómo ir a la de septiembre.
    """
    if len(meses) < 2:
        return ""
    items = "\n".join(
        f'        <a class="filtro-btn{" activo" if m == mes else ""}" '
        f'href="{ruta(m, datos)}">{e(nombre_mes(m))}</a>'
        for m in meses)
    return f'''    <nav class="rec-meses" aria-label="Recomendados por mes">
{items}
    </nav>
'''


def estilos():
    return '''    .pagina-titulo   { font-size: 1.25rem; color: var(--blanco); letter-spacing: 3px; margin-bottom: 0.25rem; }
    .pagina-sub      { font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 1.5rem; }
    .rec-meses       { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.9rem 0 1.5rem; }
    /* Es un <a>, así que hay que apagarle el subrayado que trae de la regla global. */
    .rec-meses .filtro-btn { text-decoration: none; display: inline-block; }
    .rec-intro       { font-size: 0.8125rem; color: var(--gris-7); line-height: 1.9; max-width: 720px; margin-bottom: 2rem; }
    .rec-aviso       { font-size: 0.75rem; color: var(--amarillo); letter-spacing: 1px; margin-bottom: 1.5rem; }
    .recomendados    { max-width: 720px; }
    /* Mismo esqueleto que una tarjeta de noticia: borde a la izquierda, carátula vertical
       y el texto al lado. La carátula es más grande que en /noticias porque acá la imagen
       es media razón para entrar. */
    .rec             { display: flex; gap: 1.25rem; align-items: flex-start; color: inherit;
                       border-left: 2px solid var(--gris-3); padding: 0 0 1.75rem 1.25rem;
                       margin-bottom: 1.75rem; transition: border-color 0.1s; }
    .rec:hover       { border-left-color: var(--acento); }
    .rec:hover .rec-titulo { color: var(--acento); }
    .rec-portada     { width: 120px; height: 180px; object-fit: cover; flex-shrink: 0;
                       border: 1px solid var(--gris-3); background: var(--gris-1); display: block; }
    .rec-cuerpo      { min-width: 0; flex: 1; }
    .rec-fecha       { font-size: 0.6875rem; color: var(--gris-5); letter-spacing: 2px; margin-bottom: 0.35rem; }
    .rec-meta        { border: 1px solid currentColor; padding: 0 5px; margin-left: 0.6rem; letter-spacing: 0; }
    .rec-titulo      { font-size: 0.9375rem; color: var(--blanco); letter-spacing: 1px;
                       font-weight: 700; line-height: 1.5; margin-bottom: 0.5rem; }
    .rec-texto       { font-size: 0.8125rem; color: var(--gris-7); line-height: 1.9; margin-top: 0.6rem; }
    @media (max-width: 600px) {
      .rec           { gap: 0.9rem; padding-left: 0.9rem; }
      .rec-portada   { width: 84px; height: 126px; }
    }'''


def pagina(datos_mes, juegos, meses, datos):
    """Arma una página de un mes.

    `datos_mes` es su entrada de recomendados.js —`mes`, `juegos` y opcionalmente `intro`—
    y `datos` el objeto entero, que es quien sabe qué URL le toca a cada mes.
    """
    mes = datos_mes["mes"]
    lista = datos_mes["juegos"]
    camino = ruta(mes, datos)
    pasado = camino != "/recomendados"
    anio_mes = nombre_mes(mes)
    hoy = datetime.date.today()
    canonica = DOMINIO + camino

    faltan = [r["id"] for r in lista if r["id"] not in juegos]
    if faltan:
        print(f"  ⚠ {len(faltan)} recomendado(s) de {mes} que no están en juegos.js: "
              f"{', '.join(faltan)}")
    elegidos = [(r, juegos[r["id"]]) for r in lista if r["id"] in juegos]
    # Por fecha de salida: la página se lee de arriba abajo como el mes que viene.
    elegidos.sort(key=lambda p: p[1]["fecha"])

    # Un recomendado que se retrasó a otro mes deja de tener sentido acá, y no se detecta
    # mirando la página: la tarjeta sigue igual de prolija con la fecha nueva.
    fuera = [j["id"] for _, j in elegidos if j["fecha"][:7] != mes]
    if fuera:
        print(f"  ⚠ {len(fuera)} recomendado(s) que ya no salen en {mes}: {', '.join(fuera)}")

    # Publicar la selección antes de que empiece el mes es lo normal y no se avisa: a fin
    # de agosto la de septiembre ya tiene que estar. Lo que sí se avisa es que /recomendados
    # quedó vieja, porque una lista de "recomendados del mes" del mes pasado engaña al que
    # llega. En las páginas de meses pasados no hay nada que avisar: dicen el mes en el
    # título y el lector sabe perfectamente dónde está parado.
    vigente = pasado or mes >= hoy.strftime("%Y-%m")
    aviso = "" if vigente else (
        f'      <p class="rec-aviso">Esta selección es de {e(mes_prosa(mes))} y quedó vieja. '
        'La del mes en curso todavía no se publicó.</p>\n')

    if pasado:
        titulo_h1 = f"MEJORES JUEGOS DE {anio_mes}"
        descripcion = (f"Los {len(elegidos)} mejores juegos de {mes_prosa(mes)} para PS5, "
                       "Xbox y Switch: puntajes, plataformas, gameplay en español y qué tiene "
                       "cada uno.")
        title = f"Los Mejores Juegos de {anio_mes.title()} — LANZAMIENTOS.LAT"
        respaldo = (f"Los {len(elegidos)} juegos de {mes_prosa(mes)} que valieron la pena, "
                    "con el puntaje de la crítica al lado.")
    else:
        titulo_h1 = f"RECOMENDADOS DE {anio_mes}"
        descripcion = (f"Los {len(elegidos)} juegos de {mes_prosa(mes)} que vale la pena "
                       "mirar: fechas, plataformas y qué tiene cada uno.")
        title = f"Los Mejores Juegos de {anio_mes.title()} — Recomendados | LANZAMIENTOS.LAT"
        respaldo = (f"Los {len(elegidos)} juegos de {mes_prosa(mes)} que vale la pena tener "
                    "en el radar.")
    # La entrada del mes puede traer su propia `intro`, escrita a mano, y es lo que conviene:
    # la genérica no puede nombrar un juego y el que llega quiere leer de juegos. La de
    # respaldo existe para que un mes cargado a las apuradas no quede sin nada arriba.
    intro = (datos_mes.get("intro") or "").strip() or respaldo

    cuerpo = "\n".join(tarjeta(r, j, hoy.isoformat()) for r, j in elegidos)
    sub = (f"{len(elegidos)} JUEGOS ELEGIDOS A MANO" if not pasado
           else f"{len(elegidos)} JUEGOS ELEGIDOS A MANO — EL MES YA PASÓ")

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(descripcion)}">
  <title>{e(title)}</title>
  <link rel="canonical" href="{canonica}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#000000">
  <link rel="apple-touch-icon" href="/icon-192.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LANZAMIENTOS.LAT">
  <meta property="og:title" content="Los mejores juegos de {anio_mes.title()} — LANZAMIENTOS.LAT">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{canonica}">
  <meta property="og:image" content="{DOMINIO}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="css/style.css">
  <style>
{estilos()}
  </style>
</head>
<body>

{plantilla.cabecera("/recomendados")}

  <main class="contenedor">
    <a href="/" class="volver">◀ VOLVER AL CALENDARIO</a>
{botones(meses, mes, datos)}    <h1 class="pagina-titulo">{e(titulo_h1)}</h1>
    <p class="pagina-sub">{sub}</p>
{aviso}    <p class="rec-intro">{e(intro)}</p>

    <div class="recomendados">
{cuerpo}
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
    destino = RAIZ / f"{camino.lstrip('/')}.html"
    destino.write_text(html, encoding="utf-8")
    return destino.name, len(elegidos), anio_mes, vigente


def main():
    juegos = {x["id"]: x for x in cargar_juegos()}
    datos = leer_recomendados()
    actual = datos["mes"]
    anteriores = datos.get("anteriores") or []

    # Un mes en las dos listas serían dos URLs con el mismo contenido, que es justo lo que
    # estamos peleando con la indexación. Se avisa fuerte y se ignora la copia vieja.
    if any(a["mes"] == actual for a in anteriores):
        print(f"  ⚠ {actual} está en `mes` Y en `anteriores`: se ignora la copia de "
              "`anteriores` para no publicar dos URLs iguales")
        anteriores = [a for a in anteriores if a["mes"] != actual]
        datos["anteriores"] = anteriores

    # Del más nuevo al más viejo: el que entra a una página vieja suele querer la actual.
    meses = sorted([actual] + [a["mes"] for a in anteriores], reverse=True)

    nombre, n, anio_mes, vigente = pagina(datos, juegos, meses, datos)
    print(f"{nombre} generada: {n} juegos de {anio_mes}"
          + ("" if vigente else "  ⚠ SELECCIÓN VIEJA: armar la del mes en curso"))

    for a in sorted(anteriores, key=lambda x: x["mes"], reverse=True):
        nombre, n, anio_mes, _ = pagina(a, juegos, meses, datos)
        print(f"{nombre} generada: {n} juegos de {anio_mes}")


if __name__ == "__main__":
    main()
