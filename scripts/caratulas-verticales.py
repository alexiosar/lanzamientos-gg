#!/usr/bin/env python3
"""Busca carátulas verticales de 2:3 en SteamGridDB para los juegos que no la tienen.

El problema: al 26/08/2026 el calendario tenía 163 carátulas verticales de Steam, 161
apaisadas de 460x215 y 27 cuadradas de Nintendo. Con tres formas distintas, las tarjetas
quedan disparejas por más que el CSS las acomode. Y no hay nada más que rascar por el lado
de Steam: se revisaron las 161 apaisadas una por una y ninguna tiene `library_600x900`.

SteamGridDB es un banco de arte de portada subido por la comunidad, pensado justamente para
esto: sus "grids" de 600x900 son la misma proporción que usa Steam y que usa releases.com,
que normaliza todo a 200x300.

LA CLAVE NO VA EN EL REPO. Es público. Va en una variable de entorno:

    export SGDB_API_KEY='...'     # se saca en steamgriddb.com/profile/preferences/api
    python3 scripts/caratulas-verticales.py            # sólo mira y reporta
    python3 scripts/caratulas-verticales.py --aplicar  # escribe datos/juegos.js

Cómo busca cada juego, en este orden:
  1. Por el appid de Steam, que ya está en la URL de la carátula que tenemos. Es exacto.
  2. Por nombre, y sólo acepta el resultado si el título coincide de verdad. Un banco de
     comunidad tiene mucho fan art y muchos juegos con nombres parecidos: si la coincidencia
     es floja, no se carga nada. Vale más un hueco que la portada de otro juego.

Sólo toma imágenes con `nsfw: false` y `humor: false`, y prefiere las más votadas.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comun import cargar_juegos

RAIZ = Path(__file__).resolve().parent.parent
API = "https://www.steamgriddb.com/api/v2"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

CLAVE = os.environ.get("SGDB_API_KEY", "").strip()


def get(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {CLAVE}",
        "User-Agent": "lanzamientos.lat/1.0 (calendario de lanzamientos)",
    })
    return json.loads(urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8"))


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]", "", t)


def es_vertical(url):
    """Las que ya están bien: Steam, PlayStation, IGDB, o las que trajo este mismo script.

    Ojo con la última: faltaba `steamgriddb` y el script no reconocía su propio resultado,
    así que volvía a consultar los 74 juegos que ya había resuelto en cada corrida. No
    rompía nada —encontraba la misma imagen y no escribía— pero eran 150 pedidos al pedo.

    `store-images.s-microsoft.com` es la de Xbox (ImagePurpose "Poster", 2:3 exacto) y se
    agregó el 02/09/2026, el mismo día que se empezó a usar esa fuente.
    """
    if not url:
        return False
    return ("library_600x900" in url or "image.api.playstation.com" in url
            or "store-images.s-microsoft.com" in url
            or "images.igdb.com" in url or "steamgriddb" in url)


def appid(j):
    m = re.search(r"/apps/(\d+)/", j.get("imagen") or "")
    return m.group(1) if m else None


def mejor_grid(sgdb_id):
    """La grilla 600x900 más votada, sin porno ni chistes."""
    datos = get(f"{API}/grids/game/{sgdb_id}?dimensions=600x900&types=static"
                "&nsfw=false&humor=false")
    if not datos.get("success") or not datos.get("data"):
        return None
    mejor = max(datos["data"], key=lambda g: (g.get("upvotes", 0) - g.get("downvotes", 0)))
    return mejor.get("url")


def anios_esperados(j):
    """El año de nuestra fecha más los que mencione `relanzamiento`."""
    a = {j["fecha"][:4]}
    a |= set(re.findall(r"\b((?:19|20)\d{2})\b", j.get("relanzamiento") or ""))
    return a


def buscar(j):
    """Devuelve (url, cómo se encontró) o (None, motivo).

    Dos reglas que salieron de revisar las primeras 118 a ojo, el 26/08/2026:

    - **El nombre tiene que parecerse de verdad.** La primera versión aceptaba que uno
      estuviera contenido en el otro y "The Caribou Trail" se llevó la portada de un juego
      llamado «'the», porque "the" está adentro de "thecariboutrail".
    - **Y el año tiene que cuadrar.** Hay dos Star Fox en el banco, el de 1993 y el de 2026;
      sin mirar el año se cargaba la caja original de Super Nintendo en el remake de Switch 2.
    """
    a = appid(j)
    if a:
        try:
            d = get(f"{API}/games/steam/{a}")
            if d.get("success") and d.get("data"):
                url = mejor_grid(d["data"]["id"])
                if url:
                    return url, "por appid"
        except Exception:
            pass
    try:
        d = get(f"{API}/search/autocomplete/{urllib.parse.quote(j['titulo'])}")
    except Exception as e:
        return None, f"error de búsqueda ({type(e).__name__})"
    if not d.get("success") or not d.get("data"):
        return None, "sin resultados"

    objetivo = norm(j["titulo"])
    esperados = anios_esperados(j)
    candidatos = []
    for cand in d["data"][:8]:
        n = norm(cand.get("name", ""))
        if len(n) < 4:
            continue
        parecido = difflib.SequenceMatcher(None, n, objetivo).ratio()
        if n != objetivo and parecido < 0.90:
            continue
        rd = cand.get("release_date")
        anio = str(datetime.datetime.fromtimestamp(rd).year) if rd else None
        candidatos.append((anio in esperados, cand.get("verified", False), parecido, anio, cand))
    if not candidatos:
        return None, f"ninguno coincide (el primero era «{d['data'][0].get('name','')[:30]}»)"

    # primero los del año que esperamos, después los verificados, después el más parecido
    candidatos.sort(key=lambda c: (c[0], c[1], c[2]), reverse=True)
    coincide_anio, _, _, anio, cand = candidatos[0]
    if len(candidatos) > 1 and not coincide_anio:
        return None, (f"«{cand.get('name','')[:24]}» es de {anio} y esperábamos "
                      f"{'/'.join(sorted(esperados))}")
    url = mejor_grid(cand["id"])
    if url:
        marca = f", {anio}" if anio else ""
        return url, f"por nombre «{cand.get('name','')[:30]}»{marca}"
    return None, f"«{cand.get('name','')[:30]}» no tiene 600x900"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true", help="escribe datos/juegos.js")
    ap.add_argument("--limite", type=int, default=0, help="cortar después de N juegos")
    ap.add_argument("--json", metavar="ARCHIVO", help="guarda lo encontrado para revisarlo antes")
    args = ap.parse_args()

    if not CLAVE:
        sys.exit("Falta SGDB_API_KEY. Sacala en steamgriddb.com/profile/preferences/api y:\n"
                 "    export SGDB_API_KEY='...'\n"
                 "No la pongas en un archivo del repo: es público.")

    juegos = cargar_juegos()
    faltan = [j for j in juegos if not es_vertical(j.get("imagen"))]
    if args.limite:
        faltan = faltan[:args.limite]
    print(f"═══ CARÁTULAS VERTICALES ═══  ({len(faltan)} juegos sin 2:3)\n")

    encontradas, sin_suerte = {}, []
    for j in faltan:
        try:
            url, como = buscar(j)
        except Exception as e:
            url, como = None, f"error ({type(e).__name__})"
        if url:
            encontradas[j["id"]] = url
            print(f"  ✓ {j['id'][:42]:42} {como}")
        else:
            sin_suerte.append((j["id"], como))
        time.sleep(0.3)

    print(f"\n── {len(encontradas)} encontradas · {len(sin_suerte)} sin resultado ──")
    for gid, motivo in sin_suerte[:20]:
        print(f"  · {gid[:42]:42} {motivo}")
    if len(sin_suerte) > 20:
        print(f"  … y {len(sin_suerte) - 20} más")

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
