#!/usr/bin/env python3
"""Chequea que la estrella de favoritos siga enchufada en todas las páginas.

Por qué existe. `js/main.js` llama a `favBotonHtml()` en medio de `renderCalendario()`,
y esa función vive en otro archivo. Si alguna vez se renombra, se borra o se deja de
cargar `js/favoritos.js`, la llamada tira una excepción **en medio del render** y la
portada queda con el calendario vacío. No es que se vea fea: no se ve nada. Y no lo
avisa nadie, porque el HTML se sirve igual y en la consola del navegador —que uno no
mira todos los días— queda un error solo.

Es el mismo modo de falla que ya se cobró un commit entero el 31/08/2026, cuando
generar-plataformas.py estuvo roto y las cinco páginas de plataforma se quedaron
viejas: se veían bien, así que nadie lo notó. La diferencia es que acá el resultado es
peor —la portada en blanco— y el chequeo es gratis, porque no toca la red.

Qué mira:

  1. Que toda función favXxx() que alguien llama esté definida en js/favoritos.js.
  2. Que las páginas que la usan carguen el script.
  3. Que las 369 fichas tengan el script y el botón con SU id.
  4. Que /mis-juegos siga con noindex y fuera del sitemap: el contenido lo pone cada
     visitante, así que para Google está siempre vacía.
  5. Que el CSS de .btn-fav siga estando (si no, la estrella funciona pero se ve como
     un botón del navegador en medio de la fila).

Uso (desde la raíz del proyecto):
    python3 scripts/verificar-favoritos.py

Lo corre `actualizar.py` todos los días.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FAVJS = RAIZ / "js" / "favoritos.js"

# Páginas que usan la estrella y por lo tanto tienen que cargar el script.
PAGINAS = ["index.html", "archivo.html", "mis-juegos.html"]


def definidas(texto):
    return set(re.findall(r"function\s+(fav[A-Za-z0-9_]*)\s*\(", texto))


def llamadas(texto):
    # `favAlternar(` cuenta; `function favAlternar(` no, que es la definición.
    return {m.group(1) for m in re.finditer(r"(?<!function )\b(fav[A-Za-z0-9_]*)\s*\(", texto)}


def main():
    print("═══ FAVORITOS ═══\n")
    problemas = []

    if not FAVJS.exists():
        print("  ⚠ falta js/favoritos.js — la portada se rompe entera")
        return 1

    fav_src = FAVJS.read_text(encoding="utf-8")
    api = definidas(fav_src)

    # 1) Nadie llama a una función que no existe.
    #    Cada archivo puede definir las suyas (mis-juegos.html define favAlCambiar), así
    #    que se descuentan antes de comparar.
    usuarios = [RAIZ / "js" / "main.js"] + [RAIZ / p for p in PAGINAS]
    for archivo in usuarios:
        if not archivo.exists():
            problemas.append(f"falta {archivo.name}")
            continue
        texto = archivo.read_text(encoding="utf-8")
        faltantes = llamadas(texto) - definidas(texto) - api
        for nombre in sorted(faltantes):
            problemas.append(f"{archivo.name} llama a {nombre}(), que no está en js/favoritos.js")

    # 2) Y las páginas que la usan cargan el script.
    for pagina in PAGINAS:
        p = RAIZ / pagina
        if p.exists() and "js/favoritos.js" not in p.read_text(encoding="utf-8"):
            problemas.append(f"{pagina} no carga js/favoritos.js")

    # 3) Las fichas: el script y el botón con SU id. Si generar-fichas.py pierde el
    #    botón, las 369 salen sin él de una y no se nota mirando una sola.
    fichas = sorted((RAIZ / "juegos").glob("*.html"))
    fichas = [f for f in fichas if f.name != "juego.html"]  # el fallback viejo no lo lleva
    sin_script, sin_boton = [], []
    for f in fichas:
        texto = f.read_text(encoding="utf-8")
        if "js/favoritos.js" not in texto:
            sin_script.append(f.stem)
        if f'data-fav="{f.stem}"' not in texto:
            sin_boton.append(f.stem)
    if sin_script:
        problemas.append(f"{len(sin_script)} ficha(s) sin el script: {', '.join(sin_script[:5])}"
                         + (" …" if len(sin_script) > 5 else ""))
    if sin_boton:
        problemas.append(f"{len(sin_boton)} ficha(s) sin el botón: {', '.join(sin_boton[:5])}"
                         + (" …" if len(sin_boton) > 5 else ""))

    # 4) /mis-juegos es de cada visitante: no se indexa.
    # Se busca la etiqueta, no la palabra: el archivo explica el noindex en un comentario
    # y buscar "noindex" suelto daba por bueno un <meta> que decía justo lo contrario.
    mis = RAIZ / "mis-juegos.html"
    if mis.exists() and not re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex',
                                      mis.read_text(encoding="utf-8")):
        problemas.append("mis-juegos.html perdió el noindex")
    sitemap = RAIZ / "sitemap.xml"
    if sitemap.exists() and "/mis-juegos" in sitemap.read_text(encoding="utf-8"):
        problemas.append("/mis-juegos entró al sitemap y no debería")

    # 5) El estilo de la estrella.
    css = RAIZ / "css" / "style.css"
    if css.exists() and ".btn-fav" not in css.read_text(encoding="utf-8"):
        problemas.append("css/style.css perdió las reglas de .btn-fav")

    if problemas:
        for p in problemas:
            print(f"  ⚠ {p}")
        print("\n  NO subir así: si falla la primera, la portada queda en blanco.")
        return 1

    print(f"  {len(api)} funciones en js/favoritos.js · {len(fichas)} fichas con el botón · "
          "/mis-juegos con noindex y fuera del sitemap")
    print("  ✓ todo enchufado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
