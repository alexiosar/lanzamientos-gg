#!/usr/bin/env python3
"""Arma el texto del posteo diario para X y Bluesky a partir de datos/juegos.js.

No publica nada: imprime los textos listos para copiar y pegar, con el conteo de
caracteres de cada red (X: 280, Bluesky: 300). La idea es engancharlo a la rutina
diaria y no tener que redactar nada a mano.

Uso (desde la raíz del proyecto):
    python3 scripts/post-diario.py                 # el día de hoy
    python3 scripts/post-diario.py --fecha 2026-08-01
    python3 scripts/post-diario.py --regresiva grand-theft-auto-vi
    python3 scripts/post-diario.py --votar fable

Son dos posteos por día (desde el 18/09/2026):
  1. El informativo: se elige la que mejor quede entre
     A) los lanzamientos del día
     B) lo que viene en los próximos 7 días
     C) cuenta regresiva a un juego grande
  2. D) "¿Lo vas a jugar?": invita a votar en la ficha de un juego que sale pronto. Existe
     para mover los votos, que casi nadie usaba, y de paso da un segundo posteo que no repite
     el primero. Si el juego ya juntó 5 votos, el posteo cita el porcentaje de "sí".
"""
import json
import subprocess
import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RAIZ = Path(__file__).resolve().parent.parent
SITIO = "https://lanzamientos.lat"
LIMITES = {"X": 280, "Bluesky": 300}
MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
# Etiquetas: pocas y en español, que es donde está el público del sitio.
TAGS = "#Videojuegos #Lanzamientos #Gaming"


from comun import MINUSCULAS, ORDINAL, PLATS, ROMANOS, SIGLAS, _sin_diacriticos, cargar_juegos, plat, plats, titulo


def armar_lista(cabecera, lineas, link, resumen):
    """Mete todas las líneas que entren y resume el resto.

    Se mide sobre el texto COMPLETO de CADA red —no sólo sobre las líneas— porque si no,
    el encabezado, el link y las etiquetas hacen que el posteo se pase sin avisar.
    """
    def entra(cuerpo):
        return all(len(version(cuerpo, link, r)) <= LIMITES[r] for r in LIMITES)

    for usar in range(len(lineas), 0, -1):
        sobran = len(lineas) - usar
        cuerpo = cabecera + "\n".join(lineas[:usar]) + (resumen(sobran) if sobran else "")
        if entra(cuerpo):
            return {"cuerpo": cuerpo, "link": link}
    return {"cuerpo": cabecera + resumen(len(lineas)), "link": link}


def url(j):
    return f"{SITIO}/juegos/{j['id']}"


def fecha_larga(f):
    y, m, d = map(int, f.split("-"))
    return f"{d} de {MESES_ES[m-1]}"


def version(cuerpo, link, red):
    """X penaliza el alcance de los posteos con enlaces externos, sobre todo en cuentas
    nuevas. Ahí el link va aparte, en una respuesta al propio posteo. En Bluesky no hay
    penalización, así que va todo junto."""
    if red == "Bluesky":
        return f"{cuerpo}\n\n👉 {link}\n\n{TAGS}"
    return f"{cuerpo}\n\n{TAGS}"


def mostrar(nombre, opcion):
    cuerpo, link = opcion["cuerpo"], opcion["link"]
    print(f"\n▸ OPCIÓN {nombre}")
    for red in ("Bluesky", "X"):
        texto = version(cuerpo, link, red)
        n, limite = len(texto), LIMITES[red]
        print(f"\n  ── {red} ──  [{n}/{limite} {'✓' if n <= limite else '✗ SE PASA'}]")
        print("  " + "─" * 60)
        for linea in texto.split("\n"):
            print("  " + linea)
        if red == "X":
            print("  " + "─" * 60)
            print("  ↳ y como RESPUESTA a tu propio posteo:")
            print(f"     {link}")


def opcion_hoy(hoy, juegos):
    dia = [j for j in juegos if j["fecha"] == hoy and not j.get("estimado")]
    if not dia:
        return None
    if len(dia) == 1:
        j = dia[0]
        mc = f"\nPuntaje: {j['metacritic']} en Metacritic" if j.get("metacritic") else ""
        return {"cuerpo": f"🎮 Hoy sale {titulo(j)}\n\nPlataformas: {plats(j)}{mc}",
                "link": url(j)}

    # Con varios, entran los que quepan y el resto se resume
    return armar_lista(
        cabecera=f"🎮 Lanzamientos de HOY ({fecha_larga(hoy)})\n\n",
        lineas=[f"▸ {titulo(j)} — {plats(j, 3)}" for j in dia],
        link=SITIO,
        resumen=lambda n: f"\n…y {n} más")


def opcion_semana(hoy, juegos):
    d0 = datetime.date(*map(int, hoy.split("-")))
    fin = (d0 + datetime.timedelta(days=7)).isoformat()
    prox = sorted((j for j in juegos
                   if not j.get("estimado") and hoy < j["fecha"] <= fin),
                  key=lambda j: j["fecha"])
    if not prox:
        return None
    lineas = []
    for j in prox:
        y, m, d = map(int, j["fecha"].split("-"))
        lineas.append(f"▸ {d:02d}/{m:02d} {titulo(j)} — {plats(j, 3)}")
    # No decir "esta semana": la ventana son los próximos 7 días corridos, así que
    # un viernes la lista es casi toda de la semana que viene. Se pone el rango real.
    ini, fin_d = d0 + datetime.timedelta(days=1), d0 + datetime.timedelta(days=7)
    if ini.month == fin_d.month:
        rango = f"del {ini.day} al {fin_d.day} de {MESES_ES[fin_d.month - 1]}"
    else:
        rango = (f"del {ini.day} de {MESES_ES[ini.month - 1]} "
                 f"al {fin_d.day} de {MESES_ES[fin_d.month - 1]}")
    return armar_lista(
        cabecera=f"📅 Lo que sale {rango}\n\n",
        lineas=lineas,
        link=SITIO,
        resumen=lambda n: f"\n…y {n} más en esos días")


def opcion_regresiva(hoy, juegos, gid=None):
    d0 = datetime.date(*map(int, hoy.split("-")))
    if gid:
        j = next((x for x in juegos if x["id"] == gid), None)
        if not j:
            print(f"  (no existe ningún juego con id '{gid}')")
            return None
    else:
        # sin argumento: el próximo lanzamiento con noticias cargadas, que es
        # el mismo criterio de "destacado" que usa la portada
        cand = sorted((x for x in juegos
                       if not x.get("estimado") and x["fecha"] > hoy and x.get("noticias")),
                      key=lambda x: x["fecha"])
        if not cand:
            return None
        j = cand[0]
    dias = (datetime.date(*map(int, j["fecha"].split("-"))) - d0).days
    if dias <= 0:
        return None
    cuanto = "Falta 1 día" if dias == 1 else f"Faltan {dias} días"
    return {"cuerpo": f"⏳ {cuanto} para {titulo(j)}\n\n"
                      f"Sale el {fecha_larga(j['fecha'])} en {plats(j)}",
            "link": url(j)}


def votos_de(gid):
    """Los conteos reales del Worker de /votos. Si no responde, el posteo sale sin cifra."""
    try:
        salida = subprocess.run(["curl", "-s", "--max-time", "10", f"{SITIO}/votos/{gid}"],
                                capture_output=True, text=True).stdout
        datos = json.loads(salida)
        return datos if isinstance(datos.get("total"), int) else None
    except Exception:
        return None


def opcion_votar(hoy, juegos, gid=None, evitar=None):
    """Un juego que sale en los próximos 30 días y tiene noticias cargadas, que es la señal
    de que es de los que se esperan. Rota por día del año para no repetir, y evita el de la
    cuenta regresiva para que los dos posteos del día no hablen de lo mismo."""
    d0 = datetime.date(*map(int, hoy.split("-")))
    fin = (d0 + datetime.timedelta(days=30)).isoformat()
    if gid:
        j = next((x for x in juegos if x["id"] == gid), None)
        if not j:
            print(f"  (no existe ningún juego con id '{gid}')")
            return None
    else:
        cand = sorted((x for x in juegos
                       if not x.get("estimado") and hoy < x["fecha"] <= fin
                       and x.get("noticias") and x["id"] != evitar),
                      key=lambda x: (x["fecha"], x["id"]))
        if not cand:
            return None
        j = cand[d0.toordinal() % len(cand)]
    cuerpo = (f"🗳️ ¿Vas a jugar {titulo(j)}?\n\n"
              f"Sale el {fecha_larga(j['fecha'])} en {plats(j)}. "
              f"En su ficha podés votar sí, tal vez o no.")
    v = votos_de(j["id"])
    if v and v["total"] >= 5:
        cuerpo += f"\n\nPor ahora, el {round(v['si'] * 100 / v['total'])}% dice que sí."
    return {"cuerpo": cuerpo, "link": url(j)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=datetime.date.today().isoformat())
    ap.add_argument("--regresiva", metavar="ID",
                    help="id del juego para la cuenta regresiva (por defecto, el próximo destacado)")
    ap.add_argument("--votar", metavar="ID",
                    help="id del juego para el posteo de votos (por defecto, uno que rota)")
    args = ap.parse_args()

    juegos = cargar_juegos()
    hoy = args.fecha

    print(f"═══ POSTEO DEL DÍA — {hoy} ═══")
    print("Cada opción viene en dos versiones: Bluesky lleva el link adentro; en X va")
    print("aparte, en una respuesta, porque los enlaces le bajan el alcance al posteo.")

    regresiva = opcion_regresiva(hoy, juegos, args.regresiva)
    evitar = regresiva["link"].rsplit("/", 1)[-1] if regresiva else None
    opciones = [
        ("A · LANZAMIENTOS DE HOY", opcion_hoy(hoy, juegos)),
        ("B · LO QUE VIENE EN 7 DÍAS", opcion_semana(hoy, juegos)),
        ("C · CUENTA REGRESIVA", regresiva),
        ("D · ¿LO VAS A JUGAR? (segundo posteo)", opcion_votar(hoy, juegos, args.votar, evitar)),
    ]
    vacias = 0
    for nombre, opcion in opciones:
        if opcion:
            mostrar(nombre, opcion)
        else:
            vacias += 1
            print(f"\n▸ OPCIÓN {nombre}: (nada para hoy)")

    if vacias == len(opciones):
        print("\nNo hay nada para postear hoy. Pasa si no lanza nada en 7 días.")
    print("\n═══ Posteo 1: una entre A, B y C · Posteo 2: la D, más tarde en el día ═══")


if __name__ == "__main__":
    main()
