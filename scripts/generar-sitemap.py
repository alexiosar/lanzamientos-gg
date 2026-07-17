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

# páginas de plataforma (SEO: "lanzamientos ps5", etc.)
for pagina in ["ps5.html", "ps4.html", "xbox.html", "switch-2.html", "switch.html"]:
    urls.append(f"""  <url>
    <loc>{DOMINIO}/{pagina}</loc>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>""")

# páginas estáticas
for pagina in ["acerca.html", "privacidad.html", "terminos.html", "archivo.html"]:
    urls.append(f"""  <url>
    <loc>{DOMINIO}/{pagina}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>""")

for i in ids:
    urls.append(f"""  <url>
    <loc>{DOMINIO}/juegos/{i}.html</loc>
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
