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
            "sin_noticias": "noticias:" not in cuerpo,
            "relanzamiento": "relanzamiento:" in cuerpo,
            "alta": (re.search(r'alta: "([^"]+)"', cuerpo) or [None, ""])[1],
            "rel_texto": (re.search(r'relanzamiento: "([^"]*)"', cuerpo) or [None, ""])[1],
        })

    print(f"═══ MANTENIMIENTO {hoy} ═══  ({len(juegos)} juegos en el calendario)\n")

    # 1) Puntajes de Metacritic
    pendientes = [j["id"] for j in juegos if j["metacritic"] == "null" and j["fecha"] <= hoy]
    print(f"── Metacritic: {len(pendientes)} lanzados sin puntaje ──")
    aplicados = {}
    por_id = {j["id"]: j for j in juegos}
    sospechosos = []
    for gid in pendientes:
        try:
            html = get(f"https://www.metacritic.com/game/{gid}/")
            rv = re.search(r'"ratingValue":(\d+)', html)
            if not rv:
                continue
            # El slug puede coincidir con OTRO juego de la misma saga: el 04/08/2026
            # "final-fantasy-xiv-online" devolvió 49, que es el lanzamiento fallido de
            # 2010, no A Realm Reborn (86), que es lo que llega a Switch 2. Se compara
            # el año de Metacritic contra el que conocemos para detectarlo.
            fecha_mc = re.search(r'"datePublished":"(\d{4})', html)
            anio_mc = fecha_mc.group(1) if fecha_mc else "?"
            j = por_id[gid]
            # años válidos: el del lanzamiento + los que mencione el campo relanzamiento
            anios_esperados = {j["fecha"][:4]} | set(
                re.findall(r"\b((?:19|20)\d{2})\b", j["rel_texto"]))
            ok = anio_mc in anios_esperados or anio_mc == "?"
            aplicados[gid] = int(rv.group(1))
            marca = "" if ok else f"   ⚠ REVISAR: Metacritic dice {anio_mc}, esperábamos {sorted(anios_esperados)}"
            if not ok:
                sospechosos.append(gid)
            print(f"  ★ NUEVO PUNTAJE {gid}: {rv.group(1)}  (Metacritic {anio_mc}){marca}")
        except Exception:
            pass  # 404 = la página no existe con ese slug; queda para revisión manual
        time.sleep(0.4)
    if sospechosos:
        print(f"\n  ⚠ {len(sospechosos)} puntaje(s) con año que no cuadra: {', '.join(sospechosos)}")
        print("    Verificar a mano antes del commit — puede ser otro juego de la misma saga.")
    if not aplicados:
        print("  (sin puntajes nuevos)")

    # 1 bis) Fecha de alta de los juegos cargados a mano desde la última corrida.
    # El badge ★ NUEVO sale de este campo, así que si nadie lo sella el juego
    # entra al calendario sin marcar. Se pone hoy, que es cuando se cargó.
    selladas = 0
    sin_alta = [j["id"] for j in juegos if not j["alta"]]
    if sin_alta:
        print(f"\n── Sellando fecha de alta: {len(sin_alta)} juego(s) nuevo(s) ──")
        for gid in sin_alta:
            patron = re.compile(r'(id: "' + re.escape(gid) + r'",.*?)(\n  \})', re.S)
            src, n = patron.subn(lambda m: m.group(1).rstrip() + f',\n    alta: "{hoy}"' + m.group(2), src, count=1)
            if n:
                print(f"  + {gid} → {hoy}")
                selladas += 1

    for gid, score in aplicados.items():
        patron = re.compile(r'(id: "' + re.escape(gid) + r'",.*?)metacritic: null,', re.S)
        src = patron.sub(lambda m: m.group(1) + f"metacritic: {score},", src, count=1)
    if aplicados or selladas:
        ARCHIVO.write_text(src, encoding="utf-8")

    # 2) Regenerar
    print("\n── Regenerando fichas y sitemap ──")
    # cargar-meta-trailers.py va PRIMERO: generar-fichas.py lee su caché para
    # declarar el trailer en los datos estructurados. Si no falta ninguno no hace
    # una sola petición, así que en un día normal no cuesta nada.
    for script in ["cargar-meta-trailers.py", "generar-fichas.py", "generar-plataformas.py",
                   "generar-noticias.py", "generar-feeds.py", "generar-sitemap.py"]:
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

    # Faltantes que se resuelven en la rutina SEMANAL (paso 6)
    print("\n── Backlog semanal: carátulas y trailers ──")
    print(f"  Sin trailer: {', '.join(j['id'] for j in juegos if j['sin_trailer']) or '(ninguno)'}")
    print(f"  Sin carátula: {', '.join(j['id'] for j in juegos if j['sin_imagen']) or '(ninguna)'}")

    # Faltantes que se resuelven en la rutina MENSUAL (pasos 10 y 11)
    print("\n── Backlog mensual: duraciones (cargar ~15 por mes) ──")
    ports_sin_duracion = [j["id"] for j in juegos if j["relanzamiento"] and j["sin_duracion"]]
    print(f"  Ports sin duración: {len(ports_sin_duracion)}")
    for gid in ports_sin_duracion[:15]:
        print(f"    · {gid}")
    if len(ports_sin_duracion) > 15:
        print(f"    … y {len(ports_sin_duracion) - 15} más")

    print("\n── Backlog mensual: noticias (los mejor puntuados sin noticias) ──")
    sin_noticias = sorted(
        (j for j in juegos if j["sin_noticias"] and j["metacritic"] != "null"),
        key=lambda j: int(j["metacritic"]), reverse=True)
    print(f"  Juegos con noticias: {sum(1 for j in juegos if not j['sin_noticias'])} de {len(juegos)}")
    for j in sin_noticias[:10]:
        print(f"    · {j['metacritic']}  {j['id']}")
    if not sin_noticias:
        print("    (ninguno)")

    # Las noticias propias (retrasos, Directs, PS Plus/Game Pass) no las puede
    # detectar el script: no salen de datos/juegos.js. Se recuerdan acá para que
    # la rutina diaria no se limite a lo que ya está cargado.
    propias = RAIZ / "datos" / "noticias.js"
    cuantas = len(re.findall(r'\n    id: "', propias.read_text(encoding="utf-8"))) if propias.exists() else 0
    ultima = "—"
    if cuantas:
        fechas = re.findall(r'fecha: "(\d{4}-\d{2}-\d{2})"', propias.read_text(encoding="utf-8"))
        if fechas:
            ultima = max(fechas)
            dias = (datetime.date.fromisoformat(hoy) - datetime.date.fromisoformat(ultima)).days
            ultima = f"{ultima} (hace {dias} día{'s' if dias != 1 else ''})"
    print("\n── Noticias propias (datos/noticias.js) ──")
    print(f"  Cargadas: {cuantas}  |  última: {ultima}")
    print("  ¿Pasó algo que no cuelgue de un lanzamiento? Retrasos, un Direct o State of")
    print("  Play, PS Plus o Game Pass del mes. Si no pasó nada, no se fuerza.")
    print("  Fuentes:  blog.latam.playstation.com · news.xbox.com · gematsu.com")
    print("            nintendo.com/us/nintendo-direct · vandal.elespanol.com · 3djuegos.com")
    print("  Vandal y 3DJuegos son radar: verificar en la tienda antes de tocar una fecha.")
    print("  De ahí no sale solo la noticia: también juegos que faltan y fechas a corregir.")

    print("\n═══ Siguiente paso: noticias (si hay), commit y deploy ═══")


if __name__ == "__main__":
    main()
