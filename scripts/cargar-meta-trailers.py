#!/usr/bin/env python3
"""Guarda la fecha de subida y el título de cada trailer en datos/trailers-meta.json.

Para que Google entienda que una ficha tiene video hace falta declararlo con
schema.org VideoObject, y ese esquema pide `uploadDate`. YouTube no lo expone en
oEmbed: hay que leerlo de la página del video, que pesa casi un mega.

Por eso se cachea. La fecha de subida de un video **no cambia nunca**, así que
esto se paga una sola vez por trailer: las corridas siguientes sólo bajan los
que todavía no están en el archivo. Si a un juego se le cambia el trailer, el id
nuevo se descarga solo y el viejo queda en la caché sin molestar.

Uso (desde la raíz del proyecto):
    python3 scripts/cargar-meta-trailers.py [--limite N]
"""
import argparse
import json
import re
import ssl
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / "datos" / "trailers-meta.json"
CTX = ssl._create_unverified_context()
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
# la marca aparece pasados los 400 KB de la página; con 900 KB entra siempre
TROZO = 900_000


def ids_en_uso():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    # el www. es opcional: una entrada vieja lo tenía y se quedaba sin fecha
    return sorted(set(re.findall(r'trailer: "https://(?:www\.)?youtube\.com/embed/([\w-]{11})"', src)))


def bajar(vid):
    req = urllib.request.Request(f"https://www.youtube.com/watch?v={vid}",
                                 headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=30, context=CTX).read(TROZO).decode("utf-8", "replace")
    fecha = re.search(r'"uploadDate":"(\d{4}-\d{2}-\d{2})', html)
    titulo = re.search(r'<meta name="title" content="([^"]+)"', html)
    if not fecha:
        return None
    return {"uploadDate": fecha.group(1),
            "titulo": (titulo.group(1) if titulo else "").strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0, help="cuántos bajar en esta corrida (0 = todos)")
    args = ap.parse_args()

    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    faltan = [v for v in ids_en_uso() if v not in cache]
    if args.limite:
        faltan = faltan[:args.limite]

    print(f"trailers en uso: {len(ids_en_uso())} | en caché: {len(cache)} | a bajar: {len(faltan)}")
    nuevos, fallidos = 0, []
    for i, vid in enumerate(faltan, 1):
        try:
            meta = bajar(vid)
            if meta:
                cache[vid] = meta
                nuevos += 1
            else:
                fallidos.append(vid)
        except Exception:
            fallidos.append(vid)
        if i % 25 == 0:
            CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True), encoding="utf-8")
            print(f"  {i}/{len(faltan)}…")
        time.sleep(0.2)

    CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True), encoding="utf-8")
    print(f"\n✓ {nuevos} nuevos | caché: {len(cache)} | sin fecha: {len(fallidos)}")
    if fallidos:
        print("  " + ", ".join(fallidos[:12]))


if __name__ == "__main__":
    main()
