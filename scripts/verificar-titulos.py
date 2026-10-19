#!/usr/bin/env python3
"""Compara cómo escribimos cada título en redes y en la pestaña con el nombre de Steam.

Los títulos están en MAYÚSCULAS en la base y `titulo()` de comun.py los pasa a formato
título. Hay grafías que ninguna regla deduce desde las mayúsculas —BeamNG.drive, DuneCrawl,
CloverPit— y van a mano en `CASO_PROPIO` o `TITULO_EXACTO`. Hasta el 19/10/2026 se
descubrían recién al ver el posteo ("Beamng.Drive"); este script las encuentra antes.

Sólo mira juegos con carátula de Steam (el appid sale de la URL) y sólo títulos que son
el mismo texto salvo mayúsculas. Marca diferencias que hay que mirar, no errores seguros:
un nombre oficial todo en mayúsculas (SOMA, ELDEN RING) se deja en formato título a
propósito, para que el posteo no grite.

Uso (desde la raíz del proyecto):
    python3 scripts/verificar-titulos.py                  # todo el calendario (~7 min)
    python3 scripts/verificar-titulos.py --desde 2026-10-15   # sólo lo cargado desde esa fecha
"""
import argparse
import json
import re
import ssl
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import _sin_diacriticos, cargar_juegos, titulo  # noqa: E402

CTX = ssl._create_unverified_context()


def nombre_steam(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&filters=basic"
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20, context=CTX) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            return d[appid]["data"]["name"] if d.get(appid, {}).get("success") else None
        except Exception:
            time.sleep(5)
    return None


def palabras(t):
    return re.findall(r"[\w'’.\-:!?&+]+", re.sub(r"[™®©]", "", t))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--desde", help="sólo juegos con `alta` desde esta fecha (AAAA-MM-DD)")
    args = ap.parse_args()

    juegos = [j for j in cargar_juegos() if not args.desde or (j.get("alta") or "") >= args.desde]
    revisados = 0
    for j in juegos:
        m = re.search(r"/apps/(\d+)/", j.get("imagen") or "")
        if not m:
            continue
        nombre = nombre_steam(m.group(1))
        time.sleep(1.6)   # Steam corta si se le pide más rápido
        if not nombre:
            continue
        revisados += 1
        a, b = palabras(titulo(j)), palabras(nombre)
        if len(a) != len(b) or [_sin_diacriticos(x).lower() for x in a] != [_sin_diacriticos(x).lower() for x in b]:
            continue
        distintas = [(x, y) for x, y in zip(a, b) if x != y]
        if distintas:
            print(f"  {j['id']:45} nosotros «{titulo(j)}» · Steam «{nombre}»")
    print(f"\n{revisados} títulos comparados. Las mayúsculas en el medio de una palabra van a "
          "CASO_PROPIO; las de un título puntual, a TITULO_EXACTO (scripts/comun.py).")


if __name__ == "__main__":
    main()
