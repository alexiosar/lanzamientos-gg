#!/usr/bin/env python3
"""Busca juegos cargados dos veces con id distinto.

El 26/08/2026 apareció SESAME STREET: AMIGOS Y RISAS por duplicado: mismo título, misma
fecha, mismas plataformas y el mismo appid de Steam, pero con dos ids —uno armado con el
nombre en castellano y otro con el nombre en inglés—. El barrido semanal lo cargó de nuevo
dieciséis días después del primero y no se dio cuenta porque compara por id, y el id era
distinto. En el sitio se veía como dos juegos, con dos fichas y dos URLs en el sitemap.

Es un error que no se nota mirando: las dos fichas están bien hechas, el error es que existan
las dos. Y no se arregla mirando el id, que es justo lo que falla.

LO QUE NO ES UN DUPLICADO, y es la mitad del problema: el mismo juego llegando a otra
plataforma en otra fecha se carga aparte a propósito, con el mismo título y hasta el mismo
trailer. Hoy hay cinco casos así —The Relic: First Guardian sale tres veces, en PS5, Xbox y
Switch 2 con dos meses de diferencia— y son correctos. Por eso el título repetido solo no
alcanza para acusar a nadie.

Un duplicado necesita las dos cosas: que sea EL MISMO PRODUCTO y que ocupe EL MISMO LUGAR.

  Mismo producto: el título normalizado, o el appid de Steam de la carátula.
  Mismo lugar:    la misma fecha, o plataformas que se pisan.

Con esas dos condiciones juntas, al 26/08/2026 el único grupo que sale es el que había que
encontrar; con cualquiera de las dos suelta salen los cinco ports legítimos.

Tampoco alcanza el trailer repetido. Toy Story 3: Complete Edition y Disney/Pixar Toy Story:
Retro Roundup salen el mismo día y comparten video, y son dos juegos distintos: el trailer es
el anuncio conjunto de Atari, que presenta los dos a la vez.

Uso (desde la raíz del proyecto):
    python3 scripts/verificar-duplicados.py

Lo corre `actualizar.py` todos los días, así un duplicado no sobrevive más de una jornada.
"""
import collections
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comun import cargar_juegos

RAIZ = Path(__file__).resolve().parent.parent


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]", "", t)


def appid(j):
    m = re.search(r"/apps/(\d+)/", j.get("imagen") or "")
    return m.group(1) if m else None


def mismo_producto(j):
    """Las señales de que dos entradas son el mismo juego, no dos juegos parecidos."""
    claves = [("título", norm(j["titulo"]))]
    a = appid(j)
    if a:
        claves.append(("appid de Steam", a))
    return claves


def mismo_lugar(a, b):
    """Y las de que ocupan el mismo lugar del calendario. Sin esto, un port legítimo
    —el mismo juego en otra plataforma dos meses después— se denuncia como duplicado."""
    if a["fecha"] == b["fecha"]:
        return "misma fecha"
    pisan = set(a["plataformas"]) & set(b["plataformas"])
    if pisan:
        return "se pisan en " + "/".join(sorted(pisan))
    return None


def main():
    juegos = cargar_juegos()
    print(f"═══ JUEGOS DUPLICADOS ═══  ({len(juegos)} en el calendario)\n")

    grupos = collections.defaultdict(list)
    for j in juegos:
        for etiqueta, valor in mismo_producto(j):
            grupos[(etiqueta, valor)].append(j)

    # Un mismo par puede aparecer por título y por appid: se reporta una sola vez.
    vistos, hallazgos = set(), 0
    for (etiqueta, _), miembros in grupos.items():
        if len(miembros) < 2:
            continue
        for i, a in enumerate(miembros):
            for b in miembros[i + 1:]:
                par = tuple(sorted((a["id"], b["id"])))
                if par in vistos:
                    continue
                razon = mismo_lugar(a, b)
                if not razon:
                    continue
                vistos.add(par)
                hallazgos += 1
                print(f"  ⚠ mismo {etiqueta} y {razon}")
                for x in (a, b):
                    print(f"      {x['id']:46} {x['fecha']} · "
                          f"{'/'.join(x['plataformas']):24} alta {x.get('alta', '—')}")
                print()

    if not hallazgos:
        print("  (ninguno)")
        return 0

    print("  Verificar en la tienda que sean el mismo producto y no dos ediciones.")
    print("  Si lo son: se queda el de alta más vieja, que es el que Google pudo indexar,")
    print("  se borra la ficha del otro en juegos/ y se le agrega un 301 en _redirects.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
