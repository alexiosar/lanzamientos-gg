#!/usr/bin/env python3
"""Carga el campo `duracion` desde HowLongToBeat en los juegos que no lo tengan.

El buscador de HLTB bloquea peticiones ingenuas, pero su propia web usa un protocolo
público en dos pasos que se puede replicar:

  1. GET  /api/bleed/init  ->  {token, hpKey, hpVal}
  2. POST /api/bleed       con las cabeceras x-auth-token, x-hp-key, x-hp-val
                           y el par hpKey/hpVal repetido dentro del cuerpo

El endpoint y los nombres de las cabeceras rotan cada tanto: si un día devuelve 403 en
todas las consultas, hay que volver a mirar el JavaScript de howlongtobeat.com y
actualizar `init()` y `buscar()`. Se busca en los chunks de /_next/static/ la llamada
a fetch que hace la búsqueda.

Sólo carga un resultado cuando el título coincide en un 82% o más, así no mete la
duración de otro juego. Lo que queda por debajo lo lista como dudoso y no lo toca.

Uso (desde la raíz del proyecto):
    python3 scripts/cargar-duraciones.py            # muestra qué haría, no escribe
    python3 scripts/cargar-duraciones.py --aplicar  # escribe datos/juegos.js
    python3 scripts/cargar-duraciones.py --aplicar --limite 15
"""
import argparse
import difflib
import json
import re
import ssl
import time
import unicodedata
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO = RAIZ / "datos" / "juegos.js"
BASE = "https://howlongtobeat.com"
CTX = ssl._create_unverified_context()
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
UMBRAL = 0.82

# Juegos donde el dato de HLTB existe pero es engañoso y no se carga nunca.
# Los MMO dan una "historia principal" de pocas horas que no representa nada.
EXCLUIDOS = {"final-fantasy-xiv-online"}


def cargar_juegos():
    src = ARCHIVO.read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1].strip().rstrip(";")
    return json.loads(re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M))


def init():
    r = urllib.request.Request(f"{BASE}/api/bleed/init?t={int(time.time() * 1000)}",
                               headers={"User-Agent": UA, "Referer": BASE + "/"})
    return json.loads(urllib.request.urlopen(r, timeout=20, context=CTX).read())


def buscar(termino, sec):
    body = {
        "searchType": "games", "searchTerms": termino.split(), "searchPage": 1, "size": 20,
        "searchOptions": {
            "games": {"userId": 0, "platform": "", "sortCategory": "popular",
                      "rangeCategory": "main", "rangeTime": {"min": None, "max": None},
                      "gameplay": {"perspective": "", "flow": "", "genre": "", "difficulty": ""},
                      "rangeYear": {"min": "", "max": ""}, "modifier": ""},
            "users": {"sortCategory": "postcount"}, "lists": {"sortCategory": "follows"},
            "filter": "", "sort": 0, "randomizer": 0},
        "useCache": True}
    body[sec["hpKey"]] = sec["hpVal"]
    r = urllib.request.Request(
        f"{BASE}/api/bleed", data=json.dumps(body).encode(), method="POST",
        headers={"User-Agent": UA, "Referer": BASE + "/", "Content-Type": "application/json",
                 "x-auth-token": sec["token"], "x-hp-key": sec["hpKey"],
                 "x-hp-val": str(sec["hpVal"])})
    return json.loads(urllib.request.urlopen(r, timeout=20, context=CTX).read())


def norm(t):
    t = "".join(c for c in unicodedata.normalize("NFD", t)
                if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def horas(segundos):
    h = segundos / 3600
    return f"{h:.1f}".replace(".", ",").replace(",0", "") if h < 10 else f"{h:.0f}"


def texto_duracion(comp_main, comp_100):
    t = f"≈ {horas(comp_main)} h (historia)"
    if comp_100 and comp_100 > comp_main:
        t += f" · {horas(comp_100)} h (completo)"
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true", help="escribir datos/juegos.js")
    ap.add_argument("--limite", type=int, default=0, help="cuántos juegos procesar (0 = todos)")
    args = ap.parse_args()

    juegos = cargar_juegos()
    pendientes = [j for j in juegos
                  if j.get("relanzamiento") and not j.get("duracion")
                  and j["id"] not in EXCLUIDOS]
    if args.limite:
        pendientes = pendientes[:args.limite]
    print(f"{len(pendientes)} juegos sin duración a consultar\n")

    sec = init()
    encontrados, dudosos, sin_datos = {}, [], []
    for j in pendientes:
        # el sufijo de las ediciones de Switch 2 no existe en HLTB
        termino = re.sub(r"\s*[—-]\s*NINTENDO SWITCH 2 EDITION", "", j["titulo"])
        datos = None
        for intento in (1, 2):
            try:
                datos = buscar(termino, sec)
                break
            except Exception as e:
                if getattr(e, "code", 0) == 403 and intento == 1:
                    try:
                        sec = init()      # el token dura poco: se renueva y se reintenta
                    except Exception:
                        pass
                    time.sleep(1)
                else:
                    break
        if not datos or not datos.get("data"):
            sin_datos.append(j["id"])
            time.sleep(0.35)
            continue
        mejor = max(datos["data"],
                    key=lambda g: difflib.SequenceMatcher(None, norm(termino), norm(g["game_name"])).ratio())
        ratio = difflib.SequenceMatcher(None, norm(termino), norm(mejor["game_name"])).ratio()
        if ratio >= UMBRAL and mejor.get("comp_main", 0) > 0:
            encontrados[j["id"]] = texto_duracion(mejor["comp_main"], mejor.get("comp_100", 0))
            print(f"  ✓ {j['id'][:44]:46} {encontrados[j['id']]}")
        else:
            motivo = "sin datos de tiempo" if ratio >= UMBRAL else f"coincidencia {ratio:.2f}"
            dudosos.append((j["id"], mejor["game_name"], motivo))
        time.sleep(0.35)

    print(f"\n── Resumen ──\n  encontrados: {len(encontrados)}"
          f"  |  dudosos: {len(dudosos)}  |  sin resultado: {len(sin_datos)}")
    if dudosos:
        print("\n  Dudosos (no se cargan, revisar a mano):")
        for gid, nombre, motivo in dudosos:
            print(f"    {gid[:40]:42} → «{nombre[:34]}» ({motivo})")
    if sin_datos:
        print(f"\n  Sin resultado en HLTB: {', '.join(sin_datos)}")

    if not args.aplicar:
        print("\n(prueba en seco: no se escribió nada. Agregar --aplicar para guardar)")
        return

    src = ARCHIVO.read_text(encoding="utf-8")
    for gid, txt in encontrados.items():
        b = re.search(r'(\n  \{\n    id: "' + re.escape(gid) + r'",.*?\n  \},?)', src, re.S).group(1)
        if "duracion:" in b:
            continue
        m = re.search(r'\n    relanzamiento: "[^"]*",', b)
        if not m:
            continue
        src = src.replace(b, b[:m.end()] + f'\n    duracion: "{txt}",' + b[m.end():], 1)
    ARCHIVO.write_text(src, encoding="utf-8")
    print(f"\n✓ datos/juegos.js actualizado con {len(encontrados)} duraciones.")
    print("  Siguiente paso: regenerar fichas, plataformas, feeds y sitemap.")


if __name__ == "__main__":
    main()
