#!/usr/bin/env python3
"""Segunda pasada de carátulas verticales, ahora contra IGDB.

`caratulas-verticales.py` dejó 110 juegos sin 2:3 porque SteamGridDB es un banco de arte de
comunidad: tiene el juego base y no las variantes. Los que quedaron son en buena medida
expansiones y ediciones —DOOM: The Dark Ages | Revelations, Disney Dreamlight Valley:
Honeyglow Woods, The Alters: Last Variable, Granblue Fantasy: Relink - Endless Ragnarok—
y ahí IGDB es mejor fuente: es una base de datos, cada expansión tiene su ficha y su tapa.

OJO CON LA PROPORCIÓN. Las tapas salen en 528x704 con `t_cover_big_2x`, que es lo más grande
que IGDB devuelve para tapas: eso es 3:4, no el 2:3 de Steam. Al meterla en el recuadro del
sitio se le recorta un 11% de ancho, que en un arte de tapa —donde el título va centrado— no
se nota. Contra una apaisada de 460x215 la mejora es enorme igual.

Y no todas son tapas. IGDB acepta cualquier imagen en ese campo y unas pocas son iconos
cuadrados; recortados a 2:3 pierden un tercio del alto y quedan peor que la apaisada que
venían a reemplazar. Por eso se descarta lo que no sea claramente vertical.

LAS CREDENCIALES NO VAN EN EL REPO. Es público. La API de IGDB se autentica con una
aplicación de Twitch (dev.twitch.tv/console/apps), y van en el entorno:

    export IGDB_CLIENT_ID='...'
    export IGDB_CLIENT_SECRET='...'
    python3 scripts/caratulas-igdb.py            # sólo mira y reporta
    python3 scripts/caratulas-igdb.py --aplicar  # escribe datos/juegos.js

Las reglas de coincidencia son las mismas que las de SteamGridDB, y por el mismo motivo:
el nombre tiene que coincidir de verdad y el año tiene que cuadrar. Ver el docstring de
`caratulas-verticales.py` para los dos casos que las hicieron necesarias.

La única diferencia es que acá el año se compara contra TODAS las fechas de lanzamiento que
tenga la ficha, no contra la primera. IGDB guarda una fecha por plataforma, y en un port la
primera es la de PC de hace años: es el mismo juego, no un homónimo.
"""
import argparse
import datetime
import difflib
import json
import os
import re
import ssl
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
API = "https://api.igdb.com/v4"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

CLIENT_ID = os.environ.get("IGDB_CLIENT_ID", "").strip()
CLIENT_SECRET = os.environ.get("IGDB_CLIENT_SECRET", "").strip()

# El tamaño más grande que IGDB devuelve para tapas. `t_1080p` existe pero en las tapas
# devuelve la misma imagen estirada, así que no gana nada.
TAMANIO = "t_cover_big_2x"

# Cuánto más alta que ancha tiene que ser para considerarla una tapa. Las de verdad son 3:4
# (1,33) o más; con 1,2 pasan todas y quedan afuera los iconos cuadrados.
MIN_ALTO = 1.2


def token():
    """La API de IGDB se autentica con un token de Twitch, que dura unos 60 días."""
    url = ("https://id.twitch.tv/oauth2/token?"
           + urllib.parse.urlencode({"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
                                     "grant_type": "client_credentials"}))
    req = urllib.request.Request(url, data=b"", method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=20, context=CTX).read())["access_token"]


def consultar(tok, cuerpo, endpoint="games"):
    req = urllib.request.Request(f"{API}/{endpoint}", data=cuerpo.encode("utf-8"), headers={
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {tok}",
        "Accept": "application/json",
    })
    return json.loads(urllib.request.urlopen(req, timeout=20, context=CTX).read())


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]", "", t)


def cargar_juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1].strip().rstrip(";")
    cuerpo = re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M)
    return json.loads(cuerpo)


def es_vertical(url):
    """Las que ya están bien: Steam 600x900, PlayStation, o las que trajo SteamGridDB."""
    if not url:
        return False
    return ("library_600x900" in url or "image.api.playstation.com" in url
            or "steamgriddb" in url or "images.igdb.com" in url)


def anios_esperados(j):
    """El año de nuestra fecha más los que mencione `relanzamiento`."""
    a = {j["fecha"][:4]}
    a |= set(re.findall(r"\b((?:19|20)\d{2})\b", j.get("relanzamiento") or ""))
    return a


def buscar(tok, j):
    """Devuelve (url, cómo se encontró) o (None, motivo)."""
    titulo = j["titulo"].replace('"', " ")
    cuerpo = (f'search "{titulo}"; '
              'fields name,cover.image_id,cover.width,cover.height,'
              'first_release_date,release_dates.y,category,parent_game.name; limit 10;')
    try:
        datos = consultar(tok, cuerpo)
    except Exception as e:
        return None, f"error de búsqueda ({type(e).__name__})"
    if not datos:
        return None, "sin resultados"

    objetivo = norm(j["titulo"])
    esperados = anios_esperados(j)
    candidatos = []
    for cand in datos:
        n = norm(cand.get("name", ""))
        if len(n) < 4:
            continue
        parecido = difflib.SequenceMatcher(None, n, objetivo).ratio()
        if n != objetivo and parecido < 0.90:
            continue
        tapa = cand.get("cover") or {}
        if not tapa.get("image_id"):
            continue
        # Tiene que ser vertical de verdad. Las tapas son 3:4 o más altas; lo que viene
        # cuadrado es un icono, y recortado al 2:3 del sitio pierde un tercio del alto.
        # El 26/08/2026 se colaban así Spooky Spirit Shooting Gallery y Marupoyo.
        if tapa.get("width") and tapa.get("height") / tapa["width"] < MIN_ALTO:
            continue
        # Todos los años de la ficha, no sólo el primero: en un port la primera fecha es la
        # de PC de hace años y sigue siendo el mismo juego.
        anios = {str(r["y"]) for r in cand.get("release_dates", []) if r.get("y")}
        if cand.get("first_release_date"):
            anios.add(str(datetime.datetime.fromtimestamp(cand["first_release_date"]).year))
        candidatos.append((bool(anios & esperados), parecido, sorted(anios), cand))
    if not candidatos:
        primero = datos[0].get("name", "")[:30]
        return None, f"ninguno coincide (el primero era «{primero}»)"

    candidatos.sort(key=lambda c: (c[0], c[1]), reverse=True)
    coincide_anio, _, anios, cand = candidatos[0]
    if not coincide_anio:
        vistos = "/".join(anios) or "sin fecha"
        return None, (f"«{cand.get('name','')[:24]}» es de {vistos} y esperábamos "
                      f"{'/'.join(sorted(esperados))}")

    url = (f"https://images.igdb.com/igdb/image/upload/{TAMANIO}/"
           f"{cand['cover']['image_id']}.jpg")
    de = (cand.get("parent_game") or {}).get("name")
    marca = f" (de «{de[:24]}»)" if de else ""
    return url, f"«{cand.get('name','')[:34]}»{marca}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true", help="escribe datos/juegos.js")
    ap.add_argument("--limite", type=int, default=0, help="cortar después de N juegos")
    ap.add_argument("--json", metavar="ARCHIVO", help="guarda lo encontrado para revisarlo antes")
    args = ap.parse_args()

    if not (CLIENT_ID and CLIENT_SECRET):
        sys.exit("Faltan IGDB_CLIENT_ID / IGDB_CLIENT_SECRET.\n"
                 "Se sacan creando una aplicación en dev.twitch.tv/console/apps y:\n"
                 "    export IGDB_CLIENT_ID='...'\n"
                 "    export IGDB_CLIENT_SECRET='...'\n"
                 "No las pongas en un archivo del repo: es público.")
    try:
        tok = token()
    except Exception as e:
        sys.exit(f"No se pudo autenticar contra Twitch: {type(e).__name__} {e}")

    juegos = cargar_juegos()
    faltan = [j for j in juegos if not es_vertical(j.get("imagen"))]
    if args.limite:
        faltan = faltan[:args.limite]
    print(f"═══ CARÁTULAS EN IGDB ═══  ({len(faltan)} juegos sin vertical)\n")

    encontradas, sin_suerte = {}, []
    for j in faltan:
        try:
            url, como = buscar(tok, j)
        except Exception as e:
            url, como = None, f"error ({type(e).__name__})"
        if url:
            encontradas[j["id"]] = url
            print(f"  ✓ {j['id'][:42]:42} {como}")
        else:
            sin_suerte.append((j["id"], como))
        time.sleep(0.3)          # IGDB permite 4 consultas por segundo

    print(f"\n── {len(encontradas)} encontradas · {len(sin_suerte)} sin resultado ──")
    for gid, motivo in sin_suerte[:25]:
        print(f"  · {gid[:42]:42} {motivo}")
    if len(sin_suerte) > 25:
        print(f"  … y {len(sin_suerte) - 25} más")

    if args.json:
        por_id = {j["id"]: j for j in juegos}
        Path(args.json).write_text(json.dumps(
            [{"id": gid, "titulo": por_id[gid]["titulo"], "url": url,
              "anterior": por_id[gid].get("imagen")} for gid, url in encontradas.items()],
            ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  (guardado en {args.json})")

    if not args.aplicar:
        print("\n(sólo mirando: correr con --aplicar para escribir)")
        return

    archivo = RAIZ / "datos" / "juegos.js"
    s = archivo.read_text(encoding="utf-8")
    escritas = 0
    for gid, url in encontradas.items():
        m = re.search(r'\n  \{\n    id: "' + re.escape(gid) + r'",.*?\n  \}', s, re.S)
        if not m:
            continue
        bloque = m.group(0)
        nuevo = re.sub(r'imagen: (?:null|"[^"]*")', f'imagen: "{url}"', bloque, count=1)
        if nuevo != bloque:
            s = s.replace(bloque, nuevo, 1)
            escritas += 1
    archivo.write_text(s, encoding="utf-8")
    print(f"\n{escritas} carátulas escritas en datos/juegos.js")
    print("Ahora: python3 scripts/actualizar.py && python3 scripts/verificar-enlaces.py")


if __name__ == "__main__":
    main()
