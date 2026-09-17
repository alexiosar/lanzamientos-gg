#!/usr/bin/env python3
"""Consulta la tienda de Xbox sin navegador: si un juego existe y con qué fecha sale.

La página de búsqueda de xbox.com se arma con JavaScript y hay que navegarla de a una. Pero
Microsoft tiene dos APIs públicas que responden a `curl` y resuelven lo mismo en segundos:

  1. autosuggest   devuelve los productos que coinciden con el nombre y su id de catálogo.
  2. displaycatalog con ese id devuelve la ficha, y en ella `OriginalReleaseDate`.

Cómo leer la fecha:
  - `9998-12-30` es el "próximamente" de Microsoft: el producto existe pero no tiene día.
  - Una fecha pasada con el juego en venta es un lanzamiento real.
  - Que no aparezca no prueba que no salga en Xbox: el buscador a veces no encuentra títulos
    con punto y coma o nombres traducidos (ENCHUFAO es HYPERWIRED en español). Ante la duda,
    buscar en xbox.com con el navegador.

Hay que usar `curl` y no `urllib`: con el cliente de Python la conexión se cuelga.

Uso (desde la raíz del proyecto):
    python3 scripts/buscar-xbox.py "Boltgun 2" "Fable"
"""
import json
import subprocess
import sys
import urllib.parse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
SUGERENCIAS = ("https://www.microsoft.com/msstoreapiprod/api/autosuggest?market=es-ar"
               "&clientId=7F27B536-CF6B-4C65-8638-A0F8CBDFCA65"
               "&sources=Microsoft-Terms,Iris-Products,xSearch-Products"
               "&filter=+ClientType:StoreWeb&counts=5,1,5&query=")
CATALOGO = "https://displaycatalog.mp.microsoft.com/v7.0/products?market=AR&languages=es-AR&bigIds="


def pedir(url):
    salida = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url],
                            capture_output=True, text=True).stdout
    try:
        return json.loads(salida or "{}")
    except json.JSONDecodeError:
        return {}


def buscar(nombre):
    ids = []
    for grupo in pedir(SUGERENCIAS + urllib.parse.quote(nombre)).get("ResultSets", []):
        for s in grupo.get("Suggests", []):
            meta = {m.get("Key"): m.get("Value") for m in (s.get("Metas") or [])}
            if meta.get("ProductType") == "Game" and meta.get("BigCatalogId"):
                ids.append(meta["BigCatalogId"])
    print(f"═══ {nombre}")
    if not ids:
        print("  (sin resultados en Xbox)")
        return
    for p in pedir(CATALOGO + ",".join(ids[:4])).get("Products", []):
        titulo = p["LocalizedProperties"][0]["ProductTitle"]
        fecha = (p.get("MarketProperties", [{}])[0].get("OriginalReleaseDate") or "?")[:10]
        aviso = "  (sin día)" if fecha.startswith("9998") else ""
        print(f"  {fecha}  {titulo[:60]:60}  {p['ProductId']}{aviso}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for nombre in sys.argv[1:]:
        buscar(nombre)


if __name__ == "__main__":
    main()
