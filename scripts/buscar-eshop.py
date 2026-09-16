#!/usr/bin/env python3
"""Consulta la eShop europea: si un juego existe, en qué consola de Nintendo y con qué fecha.

Es el primer paso de "Descubrir no es verificar" (README): Nintendo tiene una API de búsqueda
pública que responde sin navegador y devuelve **una fila por plataforma**, así que en una sola
consulta se sabe si un juego sale en Switch, en Switch 2 o en las dos, y para qué día.

Tres cosas a tener en cuenta al leer el resultado:
  - `2026-12-31`, `2027-12-31` o `2050-12-31` no son fechas: son el "próximamente" de la eShop.
    Si un juego que teníamos con día pasa a una de esas, se retrasó (así se vio 007 First Light).
  - Sin `nsuid` no hay producto a la venta todavía; es una ficha informativa.
  - Que no aparezca no prueba que no salga en Nintendo: a veces la eShop de EE.UU. lo tiene
    antes. Para eso, buscar en nintendo.com/us/search con el navegador.

Uso (desde la raíz del proyecto):
    python3 scripts/buscar-eshop.py "Moros Protocol" "Ratatan"
    python3 scripts/buscar-eshop.py --rango 2026-10-01 2026-10-31   # todo lo que sale en ese rango

Sin red para nada más que searching.nintendo-europe.com, y sin claves.
"""
import argparse
import json
import ssl
import urllib.parse
import urllib.request

API = "https://searching.nintendo-europe.com/en/select"
CAMPOS = "title,dates_released_dts,system_names_txt,nsuid_txt,publisher"
# Igual que actualizar.py: el Python de python.org en macOS no trae certificados raíz.
CTX = ssl._create_unverified_context()


def consultar(params):
    base = {"fq": "type:GAME", "wt": "json", "fl": CAMPOS}
    base.update(params)
    url = API + "?" + urllib.parse.urlencode(base)
    with urllib.request.urlopen(url, timeout=30, context=CTX) as r:
        return json.load(r)["response"]["docs"]


def fila(d):
    fecha = (d.get("dates_released_dts") or ["?"])[0][:10]
    plats = ", ".join(d.get("system_names_txt") or [])
    nsuid = (d.get("nsuid_txt") or ["—"])[0]
    return f"  {fecha}  {d.get('title', '?')[:60]:60}  {plats:22}  nsuid {nsuid}  {d.get('publisher') or ''}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("nombres", nargs="*", help="uno o más títulos a buscar")
    ap.add_argument("--rango", nargs=2, metavar=("DESDE", "HASTA"), help="fechas AAAA-MM-DD")
    ap.add_argument("--filas", type=int, default=5, help="resultados por búsqueda (por nombre)")
    args = ap.parse_args()

    if args.rango:
        desde, hasta = args.rango
        docs = consultar({
            "q": "*",
            "fq": f"type:GAME AND dates_released_dts:[{desde}T00:00:00Z TO {hasta}T23:59:59Z]",
            "rows": 500,
            "sort": "dates_released_dts asc",
        })
        print(f"═══ eShop: {len(docs)} filas entre {desde} y {hasta} ═══")
        for d in docs:
            print(fila(d))
        return

    if not args.nombres:
        ap.error("pasá al menos un nombre, o --rango DESDE HASTA")
    for nombre in args.nombres:
        docs = consultar({"q": nombre, "rows": args.filas, "sort": "score desc"})
        print(f"═══ {nombre}")
        if not docs:
            print("  (sin resultados)")
        for d in docs:
            print(fila(d))


if __name__ == "__main__":
    main()
