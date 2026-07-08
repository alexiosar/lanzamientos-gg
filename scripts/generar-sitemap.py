#!/usr/bin/env python3
"""Genera sitemap.xml a partir de los juegos cargados en datos/juegos.js.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-sitemap.py
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://lanzamientos.lat"

src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
ids = re.findall(r'id: "([^"]+)"', src)

if not ids:
    raise SystemExit("ERROR: no se encontró ningún id en datos/juegos.js — no se tocó el sitemap.")

urls = [f"""  <url>
    <loc>{DOMINIO}/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""]

for i in ids:
    urls.append(f"""  <url>
    <loc>{DOMINIO}/juegos/juego.html?id={i}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
    + "\n\n".join(urls)
    + "\n\n</urlset>\n"
)

(RAIZ / "sitemap.xml").write_text(xml, encoding="utf-8")
print(f"sitemap.xml actualizado: {len(ids)} juegos + portada = {len(urls)} URLs")
