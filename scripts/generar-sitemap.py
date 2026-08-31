#!/usr/bin/env python3
"""Genera sitemap.xml a partir de los juegos cargados en datos/juegos.js.

Incluye `lastmod` por URL, que es la señal con la que Google decide a qué páginas
vale la pena volver. Sin ese dato trata todas las URLs como igual de estáticas y no
se entera de que la ficha de un juego se actualizó ayer con una noticia nueva.

Para que `lastmod` sea honesto no alcanza con poner la fecha de hoy en todo: eso le
diría a Google que las 292 fichas cambian a diario, que es falso y le hace perder la
confianza en el dato. En cambio se guarda una huella del contenido de cada URL en
`datos/lastmod.json` y la fecha sólo se mueve cuando esa huella cambia de verdad.

Ese archivo hay que commitearlo: si se pierde, todas las fechas se resetean al día
que se regenere y el sitemap miente durante un tiempo.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-sitemap.py
"""
import datetime
import hashlib
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://lanzamientos.lat"
CACHE = RAIZ / "datos" / "lastmod.json"

src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
ids = re.findall(r'id: "([^"]+)"', src)

if not ids:
    raise SystemExit("ERROR: no se encontró ningún id en datos/juegos.js — no se tocó el sitemap.")

hoy = datetime.date.today().isoformat()
previo = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
actual = {}
cambiadas = 0


def lastmod(clave, contenido):
    """Devuelve la fecha de la última vez que ESTE contenido cambió de verdad."""
    global cambiadas
    huella = hashlib.sha1(contenido.encode("utf-8")).hexdigest()[:16]
    anterior = previo.get(clave)
    if anterior and anterior.get("hash") == huella:
        fecha = anterior["lastmod"]
    else:
        fecha = hoy
        if anterior:
            cambiadas += 1
    actual[clave] = {"hash": huella, "lastmod": fecha}
    return fecha


# El campo alta (fecha en que el juego entró al calendario) no cambia nada de lo
# que se ve en la página, así que no debe mover el lastmod: si entrara en la huella,
# el día que se agregó ese campo Google leería que las 304 URLs cambiaron a la vez.
def sin_ruido(texto):
    # El campo alta no cambia nada de lo que se ve en la página.
    texto = re.sub(r'\n\s*alta: "[^"]*",?', "", texto)
    # La sangría tampoco: el 11/08/2026 se corrigió la de 30 bloques que tenían
    # `noticias:` pegado al margen y, sin esto, el sitemap le habría dicho a Google
    # que esas 30 fichas cambiaron cuando su HTML quedó byte a byte idéntico.
    return re.sub(r"\n[ \t]*", "\n", texto)


def url(ruta, contenido, changefreq, priority):
    return f"""  <url>
    <loc>{DOMINIO}{ruta}</loc>
    <lastmod>{lastmod(ruta, sin_ruido(contenido))}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""


# Bloque de cada juego dentro de juegos.js: si cambia algo del juego, cambia la huella
bloques = dict(re.findall(r'\n  \{\n    id: "([^"]+)",(.*?)\n  \},?', src, re.S))

urls = []

# La portada y las páginas de plataforma dependen de TODO el calendario: cualquier
# juego nuevo o corregido las cambia, así que su huella es la del archivo entero.
urls.append(url("/", src, "daily", "1.0"))
for pagina in ["ps5", "ps4", "xbox", "switch-2", "switch"]:
    urls.append(url(f"/{pagina}", src, "daily", "0.7"))

# Páginas estáticas: la huella es su propio HTML
# noticias cambia varias veces por semana, a diferencia del resto de las estáticas
noticias = RAIZ / "noticias.html"
urls.append(url("/noticias", noticias.read_text(encoding="utf-8") if noticias.exists() else "noticias",
                "daily", "0.8"))

# recomendados cambia una vez por mes, pero es contenido editorial y no una página fija
# como /acerca: se le da prioridad de página de contenido.
recomendados = RAIZ / "recomendados.html"
urls.append(url("/recomendados",
                recomendados.read_text(encoding="utf-8") if recomendados.exists() else "recomendados",
                "monthly", "0.8"))

for pagina in ["acerca", "api", "widget", "privacidad", "terminos", "archivo"]:
    archivo = RAIZ / f"{pagina}.html"
    contenido = archivo.read_text(encoding="utf-8") if archivo.exists() else pagina
    urls.append(url(f"/{pagina}", contenido, "monthly", "0.3"))

# La huella de una ficha es su HTML generado, no su bloque en juegos.js. Desde que
# las fichas muestran también las noticias de datos/noticias.js que las citan, el
# bloque dejó de contar toda la historia: un rumor nuevo cambia la página y el
# bloque del juego queda igual. Con el HTML no hay forma de que se escape un cambio.
for i in ids:
    ficha = RAIZ / "juegos" / f"{i}.html"
    contenido = ficha.read_text(encoding="utf-8") if ficha.exists() else bloques.get(i, i)
    urls.append(url(f"/juegos/{i}", contenido, "weekly", "0.8"))

xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
    + "\n\n".join(urls)
    + "\n\n</urlset>\n"
)

(RAIZ / "sitemap.xml").write_text(xml, encoding="utf-8")
CACHE.write_text(json.dumps(actual, indent=1, sort_keys=True), encoding="utf-8")

nuevas = len(actual) - len([k for k in actual if k in previo])
print(f"sitemap.xml actualizado: {len(ids)} juegos + portada = {len(urls)} URLs")
print(f"  lastmod: {cambiadas} URLs cambiaron hoy, {nuevas} nuevas, "
      f"{len(actual) - cambiadas - nuevas} sin cambios")
