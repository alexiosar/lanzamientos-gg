#!/usr/bin/env python3
"""Genera una página HTML estática por juego en juegos/{id}.html a partir de datos/juegos.js.

Ventajas sobre juego.html?id= (que se arma con JavaScript):
- Open Graph por juego: al compartir en WhatsApp/X se ve la carátula del juego.
- Google indexa el contenido completo sin ejecutar JS.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-fichas.py

Correr después de cada cambio en datos/juegos.js (junto con generar-sitemap.py).
"""
import datetime
import html as html_mod
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comun import plat, titulo as titulo_normal, leer_noticias_propias
import plantilla

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


# Fecha de subida y título de cada trailer, cacheados por scripts/cargar-meta-trailers.py.
# Sin `uploadDate` el VideoObject queda incompleto y Google lo ignora, y ese dato no
# está en oEmbed: hay que leerlo de la página del video, que pesa casi un mega.
def leer_meta_trailers():
    archivo = RAIZ / "datos" / "trailers-meta.json"
    return json.loads(archivo.read_text(encoding="utf-8")) if archivo.exists() else {}


META_TRAILERS = leer_meta_trailers()

# Mínimo de votos para mostrar el puntaje de usuarios en la ficha. Con menos, el
# número dice más sobre quién pasó por ahí que sobre el juego.
MIN_VOTOS = 20


# Las noticias de datos/noticias.js que citan a un juego se muestran también en su
# ficha, no sólo en /noticias. El que busca "marvel tokon" en Google cae en la ficha,
# y ahí es donde tiene que encontrar lo último que se dijo del juego.
#
# Van marcadas con su categoría —y los rumores, con el borde punteado— porque no son
# lo mismo que las novedades propias del juego: siguen sin tocar ningún dato.
def indice_noticias_propias():
    indice = {}
    for n in leer_noticias_propias():
        for gid in n.get("juegos") or []:
            indice.setdefault(gid, []).append(n)
    return indice


NOTICIAS_PROPIAS = indice_noticias_propias()


# Título de la pestaña, que es lo que Google muestra como enlace del resultado.
#
# Los clics del sitio (agosto 2026) vienen todos de búsquedas de un juego puntual,
# y casi siempre con la consola y la intención adentro: "grounded 2 ps5 cuando sale",
# "he-man ps5", "yet another zombie survivors ps5". El título decía sólo
# "GROUNDED 2 — LANZAMIENTOS.LAT": ni la consola ni la intención aparecían.
#
# Va en minúsculas porque en una lista de resultados un título todo en mayúsculas
# se lee como si gritara. El H1 de la página sigue en mayúsculas, que es el diseño.
# Google corta el título cerca de los 60 caracteres, así que cada palabra pesa.
# Medido sobre los 331 juegos: "fecha de salida" con dos consolas y el nombre del
# sitio sólo cuando entra deja la mediana en 56 y baja de 316 a 71 los que se pasan.
# Lo que nunca se recorta es el nombre del juego: es el término de la consulta.
SUFIJO = " — LANZAMIENTOS.LAT"


def titulo_pestania(j):
    plats = [plat(p) for p in j["plataformas"]][:2]
    en = f"{plats[0]} y {plats[1]}" if len(plats) > 1 else plats[0]
    base = f"{titulo_normal(j)} en {en}: fecha de salida"
    return base + SUFIJO if len(base + SUFIJO) <= 60 else base


def plat_slug(p):
    return {"PS5": "/ps5", "PS4": "/ps4", "XBOX": "/xbox",
            "SWITCH2": "/switch-2", "SWITCH": "/switch"}.get(p, "/")


def meta_clase(n):
    return "meta-alto" if n >= 75 else ("meta-medio" if n >= 50 else "meta-bajo")


def _fecha(j):
    return datetime.date(*map(int, j["fecha"].split("-")))


def relacionados(j, juegos, n=6):
    """Juegos parecidos: comparten género y, ojalá, plataforma y fecha cercana.

    Existe para que la ficha no sea un callejón sin salida: hasta ahora la única
    salida era volver al calendario.
    """
    gen, plat, hoy = set(j["genero"]), set(j["plataformas"]), _fecha(j)
    puntuados = []
    for o in juegos:
        if o["id"] == j["id"]:
            continue
        coinc_gen = len(gen & set(o["genero"]))
        if not coinc_gen:
            continue
        dias = abs((_fecha(o) - hoy).days)
        score = coinc_gen * 10 + len(plat & set(o["plataformas"])) * 3 - min(dias, 400) / 120
        if o.get("imagen"):
            score += 1          # con carátula la fila se ve mejor
        puntuados.append((score, o["fecha"], o))
    puntuados.sort(key=lambda t: (-t[0], t[1]))
    elegidos = [o for _, _, o in puntuados[:n]]

    # Si comparte género con muy pocos, completar con juegos de la misma plataforma
    if len(elegidos) < n:
        ya = {o["id"] for o in elegidos} | {j["id"]}
        resto = [o for o in juegos if o["id"] not in ya and plat & set(o["plataformas"])]
        resto.sort(key=lambda o: abs((_fecha(o) - hoy).days))
        elegidos += resto[:n - len(elegidos)]
    return elegidos


def mismo_mes(j, juegos, excluir, n=6):
    """Otros lanzamientos del mismo mes, para saltar de una fecha a la de al lado."""
    mes = j["fecha"][:7]
    otros = [o for o in juegos
             if o["id"] != j["id"] and o["id"] not in excluir and o["fecha"][:7] == mes]
    otros.sort(key=lambda o: (o["fecha"], o["titulo"]))
    return otros[:n]


def tarjeta_rel(o):
    y, m, d = map(int, o["fecha"].split("-"))
    fecha = (o.get("fechaEstimada") or MESES_ES[m - 1]) if o.get("estimado") \
        else f"{d:02d} {MESES_ES[m - 1][:3]}"
    portada = (f'<img class="rel-portada" src="{e(o["imagen"])}" alt="" loading="lazy" '
               f'onerror="this.remove()">') if o.get("imagen") else '<span class="rel-portada"></span>'
    plats = "".join(f'<span class="plat {plat_class(p)}">{plat_label(p)}</span>'
                    for p in o["plataformas"][:3])
    return f'''
          <a class="rel-item" href="/juegos/{o["id"]}">
            {portada}
            <span class="rel-info">
              <span class="rel-titulo">{e(o["titulo"])}</span>
              <span class="rel-fecha">{fecha}</span>
              <span class="plataformas">{plats}</span>
            </span>
          </a>'''


def bloque_rel(titulo, items):
    if not items:
        return ""
    return f'''
      <div class="seccion">
        <div class="seccion-titulo">{titulo}</div>
        <div class="rel-grid">{"".join(tarjeta_rel(o) for o in items)}
        </div>
      </div>'''


def generar(j, juegos):
    gid = j["id"]
    y, m, d = map(int, j["fecha"].split("-"))
    estimado = bool(j.get("estimado"))
    fecha_str = (j.get("fechaEstimada") or f"{MESES_ES[m-1]} {y}") if estimado else f"{d:02d} {MESES_ES[m-1]} {y}"
    url = f"{DOMINIO}/juegos/{gid}"
    desc_corta = j["descripcion"][:150].rsplit(" ", 1)[0] + "…"
    og_imagen = j.get("imagen") or f"{DOMINIO}/og-image.png"
    # El tipo de tarjeta depende de la forma de la carátula, no puede ser fijo. La tarjeta
    # grande espera una imagen apaisada de ~2:1: con una carátula vertical de 600x900, X la
    # recorta por arriba y por abajo y se come el título del juego. Al 20/08/2026 eso le
    # pasaba a 189 de 349 fichas, y es justo lo que se ve cuando posteamos el link.
    # La imagen del sitio (og-image.png) sí es apaisada.
    apaisada = "header" in og_imagen or og_imagen.endswith("/og-image.png")
    tarjeta = "summary_large_image" if apaisada else "summary"

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
        # El puntaje de usuarios va al lado del de crítica porque lo que importa es
        # la diferencia entre los dos: un 87 de prensa con un 4 de jugadores cuenta
        # una historia que ninguno de los dos números cuenta solo.
        # Con pocos votos el puntaje de usuarios no se muestra: un 6.8 sacado de nueve
        # votos al lado de un 73 de la prensa parece una controversia y es ruido, y
        # además cualquiera lo mueve. Metacritic publica el número sin decir sobre
        # cuántos votos se calculó, así que la advertencia la ponemos nosotros.
        usuarios = ""
        votos = j.get("metacriticVotos")
        if j.get("metacriticUsuarios") is not None and (votos or 0) >= MIN_VOTOS:
            usuarios = (f'<span class="badge-metacritic {meta_clase(j["metacriticUsuarios"] * 10)}" '
                        f'title="Puntaje de los usuarios de Metacritic, de 0 a 10, sobre {votos} votos">'
                        f'{j["metacriticUsuarios"]:.1f} <span class="badge-quien">USUARIOS</span></span>')
        metacritic_html = f'''
            <div>
              <span class="ficha-campo-label">METACRITIC</span>
              <span class="badge-metacritic {meta_clase(j["metacritic"])}" title="Puntaje de la crítica en Metacritic, de 0 a 100">{j["metacritic"]} <span class="badge-quien">CRÍTICA</span></span>
              {usuarios}
            </div>'''

    # Sin imagen va un marcador con la marca del sitio, no un hueco: el `this.remove()`
    # del onerror dejaba la ficha descuadrada cuando la URL fallaba.
    portada_html = f'<span class="portada-page portada-vacia" role="img" aria-label="Sin carátula disponible"></span>'
    if j.get("imagen"):
        forma = " forma-tapa" if "images.igdb.com" in j["imagen"] else ""
        portada_html = f'<img class="portada-page{forma}" src="{e(j["imagen"])}" alt="Portada de {e(j["titulo"])}" loading="lazy" onerror="this.outerHTML=\'<span class=&quot;portada-page portada-vacia&quot;></span>\'">'

    # Resumen propio de lo que dijo la prensa, escrito leyendo las reseñas. No se
    # copian ni se traducen: un extracto de otro sitio no aporta nada que Google no
    # tenga ya, y en español no existe en ningún lado.
    critica_html = css_critica = ""
    if j.get("critica"):
        css_critica = ("    .critica-texto     { color: var(--gris-7); font-size: 0.8125rem; "
                       "line-height: 1.9; border-left: 2px solid var(--gris-3); padding-left: 1rem; }\n")
        critica_html = f'''
      <div class="seccion">
        <div class="seccion-titulo">QUÉ DICE LA CRÍTICA</div>
        <p class="critica-texto">{e(j["critica"])}</p>
      </div>'''

    # Las propias del juego y las de datos/noticias.js que lo citan, todas juntas
    # y ordenadas por fecha: al lector le da igual de qué archivo salió cada una.
    novedades = [dict(n, categoria=None) for n in (j.get("noticias") or [])]
    novedades += [dict(n) for n in NOTICIAS_PROPIAS.get(j["id"], [])]
    novedades.sort(key=lambda n: n["fecha"], reverse=True)

    # Sólo las fichas que traen una noticia de datos/noticias.js necesitan estos
    # estilos. Emitirlos siempre cambiaría el contenido de las 337 fichas y el
    # sitemap les movería el lastmod a todas por un estilo que casi ninguna usa.
    css_noticias = ""
    if any(n.get("categoria") for n in novedades):
        css_noticias = """    .noticia-cat       { font-size: 0.5625rem; letter-spacing: 2px; border: 1px solid; padding: 1px 6px; margin-left: 0.5rem; color: var(--gris-6); border-color: var(--gris-4); white-space: nowrap; }
    .cat-suscripciones { color: var(--xbox); border-color: var(--xbox); }
    .cat-retrasos      { color: var(--switch); border-color: var(--switch); }
    .cat-anuncios      { color: var(--ps5); border-color: var(--ps5); }
    .cat-eventos       { color: var(--amarillo); border-color: var(--amarillo); }
    /* El borde punteado dice "esto no está confirmado" sin tener que leer nada. */
    .cat-rumores       { color: var(--gris-6); border-color: var(--gris-5); border-style: dashed; }
    .noticia-fuente    { display: inline-block; margin-top: 0.4rem; font-size: 0.6875rem; letter-spacing: 1px; color: var(--gris-5); }
    .noticia-fuente:hover { color: var(--acento); }
"""

    noticias_html = ""
    if novedades:
        items = ""
        for n in novedades:
            cat = ""
            if n.get("categoria"):
                cat = (f'<span class="noticia-cat cat-{n["categoria"].lower()}">'
                       f'{e(n["categoria"])}</span>')
            fuente = ""
            if n.get("fuente"):
                fuente = (f'<a class="noticia-fuente" href="{e(n["fuente"])}" '
                          f'target="_blank" rel="noopener nofollow">FUENTE ↗</a>')
            items += f'''
        <div class="noticia">
          <div class="noticia-linea">
            <span class="noticia-fecha">{e(n["fecha"])}</span>
            <span class="noticia-titulo">▸ {e(n["titulo"])}</span>{cat}
          </div>
          <p class="noticia-texto">{e(n["texto"])}</p>{fuente}
        </div>'''
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

    rel = relacionados(j, juegos)
    mes_titulo = f"MÁS LANZAMIENTOS DE {MESES_ES[m-1]} {y}"
    rel_html = bloque_rel("JUEGOS RELACIONADOS", rel) + \
        bloque_rel(mes_titulo, mismo_mes(j, juegos, {o["id"] for o in rel}))

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

    # El trailer, declarado como video para que Google sepa que la ficha tiene uno.
    # Se omite si no está en la caché: un VideoObject sin uploadDate no sirve de nada
    # y es preferible no emitir marcado incompleto.
    vid = (re.search(r"embed/([\w-]{11})", j["trailer"]) if j.get("trailer") else None)
    meta = META_TRAILERS.get(vid.group(1)) if vid else None
    if meta:
        datos_ld["trailer"] = {
            "@type": "VideoObject",
            "name": meta.get("titulo") or f'Trailer de {j["titulo"]}',
            "description": j["descripcion"][:200],
            "thumbnailUrl": f"https://i.ytimg.com/vi/{vid.group(1)}/hqdefault.jpg",
            "uploadDate": meta["uploadDate"],
            "embedUrl": j["trailer"],
        }

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(titulo_normal(j))}: fecha de salida, plataformas, puntaje y trailer. {e(desc_corta)}">
  <title>{e(titulo_pestania(j))}</title>
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#000000">
  <link rel="apple-touch-icon" href="/icon-192.png">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LANZAMIENTOS.LAT">
  <meta property="og:title" content="{e(titulo_normal(j))} — {fecha_str}">
  <meta property="og:description" content="{e(desc_corta)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{e(og_imagen)}">
  <meta property="og:locale" content="es_LA">
  <meta name="twitter:card" content="{tarjeta}">

  <script type="application/ld+json">{json.dumps(datos_ld, ensure_ascii=False)}</script>

  <link rel="alternate" type="application/rss+xml" title="Novedades de LANZAMIENTOS.LAT" href="/rss.xml">
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
    /* CRÍTICA / USUARIOS adentro de cada badge: sin la aclaración, un 86 y un 8.0
       uno al lado del otro no se entienden (uno va sobre 100 y el otro sobre 10). */
    .badge-quien       {{ font-size: 0.5625rem; letter-spacing: 1px; opacity: 0.7; }}
{css_critica}{css_noticias}    .juego-hero        {{ display: flex; gap: 2rem; align-items: flex-start; flex-wrap: wrap; }}
    .juego-hero-info   {{ flex: 1; min-width: 260px; }}
    /* Caja de tamaño fijo: el alto tiene que estar reservado ANTES de que la imagen
       cargue, o la ficha entera salta hacia abajo cuando llega (eso es CLS). Antes
       la clase .apaisada cambiaba el ancho recién en el onload, con lo cual el salto
       estaba garantizado por diseño. Ahora el hueco no cambia nunca y la carátula se
       acomoda adentro con object-fit: contain, sea vertical u horizontal.
       El 26/08/2026 la caja pasó de 200x220 a 200x300: 220 era el promedio de cuando
       convivían tres formas, y con el 98% del calendario ya vertical le sobraba ancho y le
       faltaba alto, así que la tapa salía chica y flotando en el medio del hueco. */
    .portada-page      {{ width: 200px; height: 300px; flex-shrink: 0; border: 1px solid var(--gris-3);
                         background: var(--gris-1); object-fit: contain; display: block; }}
    /* Las de IGDB son 3:4 y no 2:3: en la caja de 300 quedaban con un hueco abajo. La forma
       se sabe por la URL, así que el alto se puede reservar sin haber cargado la imagen. */
    .portada-page.forma-tapa {{ height: 267px; }}
    .video-wrapper     {{ position: relative; padding-bottom: 56.25%; height: 0; border: 1px solid var(--gris-3); background: var(--negro); }}
    .video-wrapper iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: none; }}
    .badge-gamepass    {{ color: var(--xbox); }}
    .badge-psplus      {{ color: var(--ps5); }}
    /* Juegos relacionados: la ficha ya no es un callejón sin salida */
    .rel-grid          {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 0.75rem; }}
    .rel-item          {{ display: flex; gap: 0.6rem; align-items: center; padding: 5px; border: 1px solid transparent; color: inherit; min-width: 0; }}
    .rel-item:hover    {{ border-color: var(--acento); background: rgba(160,160,255,0.05); }}
    .rel-item:hover .rel-titulo {{ color: var(--acento); }}
    /* Vertical como las de las listas: recortada a un cuadrado no se reconoce el juego. */
    .rel-portada       {{ width: 44px; height: 66px; object-fit: cover; border: 1px solid var(--gris-3); background: var(--gris-1); flex-shrink: 0; display: block; }}
    .rel-info          {{ display: flex; flex-direction: column; gap: 2px; min-width: 0; }}
    .rel-titulo        {{ color: var(--blanco); font-size: 0.75rem; letter-spacing: 0.5px; font-weight: 700; line-height: 1.3; overflow-wrap: anywhere; }}
    .rel-fecha         {{ color: var(--gris-5); font-size: 0.6875rem; letter-spacing: 1px; }}
    .rel-info .plataformas {{ gap: 0.25rem; }}
    .rel-info .plat    {{ font-size: 0.625rem; padding: 0 4px; }}
  </style>
</head>
<body>

{plantilla.cabecera(None)}

  <main class="contenedor">
    <div class="ficha-page">
      <a href="/" class="volver" id="volver">◀ VOLVER AL CALENDARIO</a>

      <div class="breadcrumb">
        <a href="/">INICIO</a> &gt;
        <a href="{plat_slug(j["plataformas"][0])}">{plat_label(j["plataformas"][0])}</a> &gt;
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
                <span class="ficha-campo-label">{"FECHA ESTIMADA" if estimado else "FECHA DE LANZAMIENTO"}</span>
                <span class="ficha-campo-valor">{fecha_str}</span>
                {'<span class="relanzamiento">◔ FECHA EXACTA SIN CONFIRMAR</span>' if estimado else f'<span class="cuenta-regresiva" id="regresiva" data-fecha="{j["fecha"]}"></span>'}{f'''
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
            <div style="margin-top:1rem; display:flex; gap:1rem; flex-wrap:wrap;">
              {'' if estimado else f'''<button class="btn-trailer" id="btn-agendar" onclick="agendarJuego('{gid}')" style="display:none">◷ AGENDAR LANZAMIENTO</button>'''}
              <button class="btn-trailer" id="btn-compartir" onclick="compartirJuego('{gid}')">⇗ COMPARTIR</button>
              <!-- La ficha es un archivo estático y cacheable, así que sale siempre en
                   "sin guardar": favPintar() lo corrige al cargar según lo que haya en
                   este navegador. Nunca al revés, o una página cacheada mentiría. -->
              <button class="btn-fav" data-fav="{gid}" data-fav-texto=""
                      onclick="favAlternar('{gid}', event)" aria-pressed="false"
                      title="Guardar en MIS JUEGOS" aria-label="Guardar en mis juegos">☆ GUARDAR EN MIS JUEGOS</button>
            </div>
          </div>
        </div>
      </div>
{critica_html}{noticias_html}
      <div class="seccion">
        <div class="seccion-titulo">DESCRIPCIÓN</div>
        <p class="descripcion-page">{e(j["descripcion"])}</p>
      </div>

      <div class="seccion">
        <div class="seccion-titulo">TAGS</div>
        <div class="ficha-tags">{tags_html}</div>
      </div>
{trailer_html}{rel_html}
    </div>
  </main>

{plantilla.pie("../rss.xml")}

  <script src="../datos/juegos.js"></script>
  <script src="../js/favoritos.js"></script>
  <script>
{plantilla.script_tema()}

    // El enlace de volver apunta al calendario, pero si llegaste desde el propio
    // sitio te devuelve a la vista donde estabas (la grilla, un filtro, una consola)
    // en lugar de tirarte siempre al calendario sin filtros.
    (function () {{
      const link = document.getElementById("volver");
      if (!link || !document.referrer) return;
      let ref;
      try {{ ref = new URL(document.referrer); }} catch (e) {{ return; }}
      if (ref.origin !== location.origin) return;
      if (ref.pathname === location.pathname) return;  // volviste a la misma ficha

      link.href = ref.href;
      const vista = ref.searchParams.get("vista");
      const nombre = ref.pathname.replace(/^\\/|\\.html$/g, "");
      if (vista === "grilla")            link.textContent = "◀ VOLVER A LA GRILLA";
      else if (vista === "ranking")      link.textContent = "◀ VOLVER AL RANKING";
      else if (nombre === "archivo")     link.textContent = "◀ VOLVER AL ARCHIVO";
      else if (nombre.startsWith("ps") || nombre.startsWith("xbox") || nombre.startsWith("switch"))
        link.textContent = "◀ VOLVER A " + nombre.toUpperCase().replace("-", " ");

      // history.back() conserva la posición de scroll; el href queda igual como
      // respaldo para clic del medio, "abrir en pestaña nueva" y sin JS.
      link.addEventListener("click", function (ev) {{
        if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button !== 0) return;
        ev.preventDefault();
        history.back();
      }});
    }})();

    // cuenta regresiva y botón agendar, calculados al cargar (no se congelan al generar)
    (function () {{
      const el = document.getElementById("regresiva");
      if (!el) return;  // fichas con fecha estimada no tienen cuenta regresiva
      const [y, m, d] = el.dataset.fecha.split("-").map(Number);
      const hoy = new Date(); hoy.setHours(0, 0, 0, 0);
      const dias = Math.round((new Date(y, m - 1, d) - hoy) / 864e5);
      if (dias === 0) {{ el.textContent = "▸ ¡SALE HOY!"; el.classList.add("regresiva-hoy"); }}
      else if (dias === 1) el.textContent = "▸ FALTA 1 DÍA";
      else if (dias > 1) el.textContent = "▸ FALTAN " + dias + " DÍAS";
      else el.remove();
      if (dias > 0) document.getElementById("btn-agendar").style.display = "";
    }})();

    function compartirJuego(id) {{
      const j = JUEGOS.find(x => x.id === id);
      if (!j) return;
      const url = location.origin + "/juegos/" + id;
      if (navigator.share) {{
        navigator.share({{ title: `${{j.titulo}} — LANZAMIENTOS.LAT`, url }}).catch(() => {{}});
      }} else {{
        navigator.clipboard.writeText(url).then(() => {{
          const b = document.getElementById("btn-compartir");
          const original = b.textContent;
          b.textContent = "✓ LINK COPIADO";
          setTimeout(() => {{ b.textContent = original; }}, 1600);
        }});
      }}
    }}

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
        `DESCRIPTION:${{esc("Lanzamiento en " + j.plataformas.map(etiqueta).join(" / ") + ". Ficha: " + location.origin + "/juegos/" + j.id)}}`,
        `URL:${{location.origin}}/juegos/${{j.id}}`,
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
        (destino / f'{j["id"]}.html').write_text(generar(j, juegos), encoding="utf-8")
        generadas += 1
    # limpiar fichas de juegos que ya no existen
    #
    # Y avisar si se van sin redirect. Borrar la ficha en silencio es como se perdieron
    # cinco URLs el 23/06/2026 —gta-vi, mario-kart-world, metroid-prime-4, split-fiction y
    # elden-ring-nightreign—: Google ya las tenía indexadas y siguió pidiéndolas durante dos
    # meses. Las tres validaciones de "No se ha encontrado (404)" que se pidieron en agosto
    # fallaron por esas cinco, y no había forma de darse cuenta mirando el sitio.
    #
    # El script no puede no borrarlas: el juego ya no está. Lo que sí puede es no callarse.
    redirects = (RAIZ / "_redirects")
    cubiertas = set(re.findall(r"^\s*(\S+)", redirects.read_text(encoding="utf-8"), re.M)) \
        if redirects.exists() else set()
    ids = {j["id"] for j in juegos}
    borradas, sin_redirect = 0, []
    for f in destino.glob("*.html"):
        if f.stem != "juego" and f.stem not in ids:
            f.unlink()
            borradas += 1
            if f"/juegos/{f.stem}" not in cubiertas:
                sin_redirect.append(f.stem)
    print(f"{generadas} fichas generadas en juegos/ ({borradas} obsoletas borradas)")
    for gid in sin_redirect:
        print(f"  ⚠ /juegos/{gid} se borró y NO tiene redirect en _redirects: va a dar 404.")
    if sin_redirect:
        print("    Si el juego se renombró, apuntar a la ficha nueva; si se fue del")
        print("    calendario, a la portada. Ver 'Si se borra o se renombra un juego' en el README.")


if __name__ == "__main__":
    main()
