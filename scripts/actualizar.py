#!/usr/bin/env python3
"""Mantenimiento diario de lanzamientos.lat en un solo comando.

Hace la parte mecánica de la rutina:
  1. Busca en Metacritic los puntajes de juegos lanzados que siguen sin puntaje
     y los aplica a datos/juegos.js.
  2. Regenera las fichas estáticas y el sitemap.
  3. Imprime un reporte: puntajes nuevos, lanzamientos de hoy/mañana (candidatos
     a noticias), y qué falta (trailers, carátulas, duraciones).

Uso (desde la raíz del proyecto):
    python3 scripts/actualizar.py

Después del script: cargar noticias si hay, commit y deploy.
"""
import datetime
import re
import ssl
import subprocess
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO = RAIZ / "datos" / "juegos.js"
CTX = ssl._create_unverified_context()
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")


def main():
    hoy = datetime.date.today().isoformat()
    maniana = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    src = ARCHIVO.read_text(encoding="utf-8")

    entradas = re.findall(
        r'id: "([^"]+)",\s*titulo: "([^"]+)",\s*(?:relanzamiento[^\n]*\n\s*)?(?:duracion[^\n]*\n\s*)?fecha: "([^"]+)",', src)
    # fallback robusto por bloque
    bloques = re.findall(r'\{\s*id: "([^"]+)",(.*?)\n  \}', src, re.S)
    juegos = []
    for gid, cuerpo in bloques:
        fecha = re.search(r'fecha: "([^"]+)"', cuerpo)
        mc = re.search(r'metacritic: (null|\d+)', cuerpo)
        juegos.append({
            "id": gid,
            "fecha": fecha.group(1) if fecha else "",
            "metacritic": mc.group(1) if mc else "null",
            "sin_trailer": "trailer: null" in cuerpo,
            "sin_imagen": "imagen: null" in cuerpo,
            "sin_duracion": "duracion:" not in cuerpo,
            "relanzamiento": "relanzamiento:" in cuerpo,
        })

    print(f"═══ MANTENIMIENTO {hoy} ═══  ({len(juegos)} juegos en el calendario)\n")

    # 1) Puntajes de Metacritic
    pendientes = [j["id"] for j in juegos if j["metacritic"] == "null" and j["fecha"] <= hoy]
    print(f"── Metacritic: {len(pendientes)} lanzados sin puntaje ──")
    aplicados = {}
    for gid in pendientes:
        try:
            html = get(f"https://www.metacritic.com/game/{gid}/")
            rv = re.search(r'"ratingValue":(\d+)', html)
            if rv:
                aplicados[gid] = int(rv.group(1))
                print(f"  ★ NUEVO PUNTAJE {gid}: {rv.group(1)}")
        except Exception:
            pass  # 404 = la página no existe con ese slug; queda para revisión manual
        time.sleep(0.4)
    if not aplicados:
        print("  (sin puntajes nuevos)")

    for gid, score in aplicados.items():
        patron = re.compile(r'(id: "' + re.escape(gid) + r'",.*?)metacritic: null,', re.S)
        src = patron.sub(lambda m: m.group(1) + f"metacritic: {score},", src, count=1)
    if aplicados:
        ARCHIVO.write_text(src, encoding="utf-8")

    # 2) Regenerar
    print("\n── Regenerando fichas y sitemap ──")
    for script in ["generar-fichas.py", "generar-plataformas.py", "generar-sitemap.py"]:
        r = subprocess.run(["python3", str(RAIZ / "scripts" / script)], capture_output=True, text=True)
        print(" ", r.stdout.strip() or r.stderr.strip())

    # 3) Reporte
    lanzan_hoy = [j["id"] for j in juegos if j["fecha"] == hoy]
    lanzan_maniana = [j["id"] for j in juegos if j["fecha"] == maniana]
    print("\n── Candidatos a noticias ──")
    print(f"  Lanzan HOY: {', '.join(lanzan_hoy) or '(nada)'}")
    print(f"  Lanzan MAÑANA: {', '.join(lanzan_maniana) or '(nada)'}")
    if aplicados:
        print(f"  Debuts en Metacritic para noticia: {', '.join(f'{g} ({s})' for g, s in aplicados.items())}")

    print("\n── Faltantes (para cuando haya tiempo) ──")
    print(f"  Sin trailer: {', '.join(j['id'] for j in juegos if j['sin_trailer']) or '(ninguno)'}")
    print(f"  Sin carátula: {', '.join(j['id'] for j in juegos if j['sin_imagen']) or '(ninguna)'}")
    ports_sin_duracion = [j["id"] for j in juegos if j["relanzamiento"] and j["sin_duracion"]]
    print(f"  Ports sin duración: {len(ports_sin_duracion)} ({', '.join(ports_sin_duracion[:6])}{'…' if len(ports_sin_duracion) > 6 else ''})")

    print("\n═══ Siguiente paso: noticias (si hay), commit y deploy ═══")


if __name__ == "__main__":
    main()
