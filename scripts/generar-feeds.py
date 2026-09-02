#!/usr/bin/env python3
"""Genera el feed RSS y la API pública JSON a partir de datos/juegos.js.

Salidas:
  rss.xml          — últimas novedades (campo `noticias`), para lectores y agregadores.
  api/juegos.json  — calendario completo en JSON, para que terceros lo usen.
  api/proximos.json— solo los lanzamientos de los próximos 30 días (payload liviano).

Uso (desde la raíz del proyecto):
    python3 scripts/generar-feeds.py

La rutina diaria (scripts/actualizar.py) lo invoca automáticamente.
"""
import datetime
import json
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

from comun import cargar_juegos, leer_noticias_propias

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://lanzamientos.lat"
MAX_ITEMS = 40


def plat_label(p):
    return "SWITCH 2" if p == "SWITCH2" else p


def generar_rss(juegos):
    # cada noticia es un item del feed, ordenadas de más nueva a más vieja
    items = []
    for j in juegos:
        for n in j.get("noticias") or []:
            items.append((n["fecha"], j, n))
    for n in leer_noticias_propias():
        items.append((n["fecha"], None, n))  # None = no es de un juego puntual
    items.sort(key=lambda x: x[0], reverse=True)
    items = items[:MAX_ITEMS]

    ahora = datetime.datetime.now(datetime.timezone.utc)
    partes = []
    for fecha, j, n in items:
        y, m, d = map(int, fecha.split("-"))
        pub = datetime.datetime(y, m, d, 12, 0, tzinfo=datetime.timezone.utc)
        if j is None:
            # noticia propia: no tiene ficha adonde apuntar, va a la página de novedades
            enlace = f"{DOMINIO}/noticias"
            titulo = escape(n["titulo"])
            desc = n["texto"]
            guid = n["id"]
        else:
            enlace = f"{DOMINIO}/juegos/{j['id']}"
            plats = " / ".join(plat_label(p) for p in j["plataformas"])
            titulo = f"{escape(j['titulo'])}: {escape(n['titulo'])}"
            desc = f"{n['texto']} — {j['titulo']} para {plats}."
            guid = f"{j['id']}-{fecha}"
        partes.append(f"""    <item>
      <title>{titulo}</title>
      <link>{enlace}</link>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{format_datetime(pub)}</pubDate>
      <description>{escape(desc)}</description>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>LANZAMIENTOS.LAT — Novedades de videojuegos</title>
    <link>{DOMINIO}/</link>
    <atom:link href="{DOMINIO}/rss.xml" rel="self" type="application/rss+xml"/>
    <description>Novedades del calendario de lanzamientos de videojuegos en español: debuts, puntajes, retrasos y anuncios para PS5, PS4, Xbox, Switch y Switch 2.</description>
    <language>es</language>
    <lastBuildDate>{format_datetime(ahora)}</lastBuildDate>
{chr(10).join(partes)}
  </channel>
</rss>
"""


def limpiar(j):
    """Deja el juego con los campos públicos y la URL de su ficha."""
    salida = {k: v for k, v in j.items() if k != "noticias"}
    salida["url"] = f"{DOMINIO}/juegos/{j['id']}"
    if j.get("noticias"):
        salida["noticias"] = j["noticias"]
    return salida


def main():
    juegos = cargar_juegos()
    hoy = datetime.date.today()
    hoy_str = hoy.isoformat()
    en30 = (hoy + datetime.timedelta(days=30)).isoformat()

    (RAIZ / "rss.xml").write_text(generar_rss(juegos), encoding="utf-8")

    api = RAIZ / "api"
    api.mkdir(exist_ok=True)

    meta = {
        "sitio": "LANZAMIENTOS.LAT",
        "descripcion": "Calendario de lanzamientos de videojuegos en español para PS5, PS4, Xbox, Switch y Switch 2.",
        "url": DOMINIO,
        "generado": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "licencia": "Uso libre citando la fuente con un enlace a lanzamientos.lat",
        "contacto": "contacto@lanzamientos.lat",
    }

    completo = dict(meta, total=len(juegos), juegos=[limpiar(j) for j in juegos])
    (api / "juegos.json").write_text(json.dumps(completo, ensure_ascii=False, indent=1), encoding="utf-8")

    proximos = [limpiar(j) for j in juegos
                if not j.get("estimado") and hoy_str <= j["fecha"] <= en30]
    proximos.sort(key=lambda j: j["fecha"])
    corto = dict(meta, desde=hoy_str, hasta=en30, total=len(proximos), juegos=proximos)
    (api / "proximos.json").write_text(json.dumps(corto, ensure_ascii=False, indent=1), encoding="utf-8")

    noticias = sum(len(j.get("noticias") or []) for j in juegos)
    print(f"rss.xml: {min(noticias, MAX_ITEMS)} items | api/juegos.json: {len(juegos)} juegos | api/proximos.json: {len(proximos)}")


if __name__ == "__main__":
    main()
