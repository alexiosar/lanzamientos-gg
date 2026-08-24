#!/usr/bin/env python3
"""Busca juegos que el sitio muestra como lanzados y capaz nunca salieron.

Es el error más caro que puede cometer un calendario y no se ve mirando el sitio: la ficha
queda igual de prolija con la fecha equivocada. En agosto de 2026 se encontraron tres por
casualidad, cada uno por un camino distinto: Rivage figuraba salido el 13/08 y la PlayStation
Store decía 22/09; Ratatan figuraba salido el 16/07 y no estaba en ninguna tienda; BloodRayne
figuraba salido el 29/07 y su editor decía octubre.

Dos pasadas, de más a menos confiable:

  1. **Steam dice que todavía no salió.** Si `appdetails` devuelve `coming_soon: true` para un
     juego que nosotros damos por lanzado, es casi seguro que la fecha está mal. No da falsos
     positivos con los ports: si un juego ya salió en PC, Steam dice `coming_soon: false`.

  2. **Nadie lo jugó.** Un juego que salió hace semanas y no tiene puntaje de crítica, ni de
     usuarios, ni noticias, puede ser un indie que nadie miró —eso es normal— o puede no haber
     salido. Acá el script no decide: lista para revisar a mano. Es la única forma de agarrar
     los que no están en Steam, que es justo el caso de Ratatan y BloodRayne.

Uso (desde la raíz del proyecto):
    python3 scripts/verificar-lanzados.py
    python3 scripts/verificar-lanzados.py --dias 30   # cuánto hace que salió, para la pasada 2

Va en la rutina semanal. La pasada 1 hace una consulta por juego lanzado; la 2 no usa red.
"""
import argparse
import datetime
import json
import re
import ssl
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

# Cuántos días tienen que haber pasado para sospechar de un juego sin rastro. Menos que esto
# y el silencio es normal: los puntajes y las reseñas tardan.
DIAS_SILENCIO = 21


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")


def cargar_juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1].strip().rstrip(";")
    cuerpo = re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M)
    return json.loads(cuerpo)


def appid(j):
    m = re.search(r"/apps/(\d+)/", j.get("imagen") or "")
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=DIAS_SILENCIO,
                    help="días desde el lanzamiento para la segunda pasada")
    args = ap.parse_args()

    hoy = datetime.date.today()
    juegos = cargar_juegos()
    lanzados = []
    for j in juegos:
        if j.get("estimado"):
            continue          # sin día confirmado no se le puede reclamar nada
        try:
            f = datetime.date(*map(int, j["fecha"].split("-")))
        except ValueError:
            continue
        if f <= hoy:
            lanzados.append((j, (hoy - f).days))

    print(f"═══ JUEGOS DADOS POR LANZADOS ═══  ({len(lanzados)} con fecha pasada)\n")

    print("── 1. Steam dice que todavía no salió ──")
    sospechosos = 0
    for j, dias in lanzados:
        a = appid(j)
        if not a:
            continue
        try:
            d = json.loads(get("https://store.steampowered.com/api/appdetails"
                               f"?appids={a}&filters=release_date"))[a]
            r = d["data"]["release_date"]
        except Exception:
            continue
        finally:
            time.sleep(0.25)
        # Si ya tiene puntaje, salió: lo jugaron y lo puntuaron. Ahí `coming_soon` es de la
        # versión de PC, que sale después que la de consola. Culdcept Begins es el ejemplo:
        # 76 en Metacritic desde julio y en Steam figura para el cuarto trimestre.
        if r.get("coming_soon") and not j.get("metacritic") and j.get("metacriticUsuarios") is None:
            sospechosos += 1
            print(f"  ⚠ {j['id']:44} nosotros {j['fecha']} · Steam «{r.get('date')}» sin salir")
    if not sospechosos:
        print("  (ninguno)")

    print(f"\n── 2. Sin rastro después de {args.dias} días: revisar a mano ──")
    mudos = []
    for j, dias in lanzados:
        if dias < args.dias:
            continue
        if j.get("metacritic") or j.get("metacriticUsuarios") is not None or j.get("noticias"):
            continue
        if j.get("duracion"):
            continue          # HowLongToBeat lo tiene cronometrado: alguien lo jugó
        mudos.append((j, dias))
    for j, dias in sorted(mudos, key=lambda x: -x[1]):
        tienda = "steam" if appid(j) else "sin appid"
        print(f"  · {j['id']:44} salió hace {dias:>3} días · {'/'.join(j['plataformas'])[:20]:20} {tienda}")
    if not mudos:
        print("  (ninguno)")
    else:
        print("\n  Sin puntaje de crítica, sin puntaje de usuarios y sin noticias. Puede ser un")
        print("  indie que no miró nadie, que es lo normal, o un juego que nunca salió. Se")
        print("  verifica en la tienda de su plataforma; si no aparece en ninguna, es lo segundo.")


if __name__ == "__main__":
    main()
