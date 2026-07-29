#!/usr/bin/env python3
"""Arma el texto del posteo diario para X y Bluesky a partir de datos/juegos.js.

No publica nada: imprime los textos listos para copiar y pegar, con el conteo de
caracteres de cada red (X: 280, Bluesky: 300). La idea es engancharlo a la rutina
diaria y no tener que redactar nada a mano.

Uso (desde la raíz del proyecto):
    python3 scripts/post-diario.py                 # el día de hoy
    python3 scripts/post-diario.py --fecha 2026-08-01
    python3 scripts/post-diario.py --regresiva grand-theft-auto-vi

Salen tres opciones y se elige la que mejor quede ese día:
  A) los lanzamientos del día
  B) lo que viene en los próximos 7 días
  C) cuenta regresiva a un juego grande
"""
import argparse
import datetime
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITIO = "https://lanzamientos.lat"
LIMITES = {"X": 280, "Bluesky": 300}
MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
# Etiquetas: pocas y en español, que es donde está el público del sitio.
TAGS = "#Videojuegos #Lanzamientos #Gaming"


def cargar_juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1].strip().rstrip(";")
    cuerpo = re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M)
    return json.loads(cuerpo)


PLATS = {"PS5": "PS5", "PS4": "PS4", "XBOX": "Xbox", "SWITCH2": "Switch 2", "SWITCH": "Switch"}
# Palabras que no se capitalizan en medio de un título
MINUSCULAS = {"of", "the", "and", "in", "on", "a", "an", "to", "for", "from", "at", "by",
              "de", "del", "la", "el", "los", "las", "y", "en", "un", "una", "por", "con",
              "vs"}
ROMANOS = re.compile(r"^(?:[IVXLC]+)$", re.I)
ORDINAL = re.compile(r"^\d+(ST|ND|RD|TH)$", re.I)
# Siglas y marcas con vocales que igual van en mayúscula (las que no tienen vocales
# —FC, HD, MXGP, VS— se detectan solas). Ampliar si aparece alguna nueva.
SIGLAS = {"EA", "NBA", "LEGO", "TOEM", "DLC", "MLB", "NFL", "NHL", "UFC", "WWE", "AEW"}


def plat(p):
    return PLATS.get(p, p)


def plats(j, maximo=4):
    ps = [plat(p) for p in j["plataformas"]]
    return "/".join(ps[:maximo]) + ("+" if len(ps) > maximo else "")


def titulo(j):
    """Los títulos están en MAYÚSCULAS en la base; en redes gritan demasiado."""
    palabras = j["titulo"].split()
    salida = []
    for i, p in enumerate(palabras):
        nucleo = p.strip(":()!?¡¿,.-'’")
        limpio = re.sub(r"[^A-Za-z0-9]", "", nucleo)
        if not limpio:
            salida.append(p)
        elif ROMANOS.match(limpio) and limpio.upper() in {"II", "III", "IV", "VI", "VII",
                                                          "VIII", "IX", "XI", "XII", "XIII"}:
            salida.append(p.upper())          # DOOM II, no Doom Ii
        elif ORDINAL.match(limpio):
            salida.append(p[:-2] + p[-2:].lower())   # 2ND -> 2nd
        elif i > 0 and limpio.lower() in MINUSCULAS and not palabras[i - 1].endswith(":"):
            salida.append(p.lower())          # City of Wolves, no City Of Wolves
        elif limpio.upper() in SIGLAS or not re.search(r"[AEIOUY]", limpio, re.I) \
                or (re.search(r"\d", limpio) and len(limpio) <= 5):
            salida.append(p.upper())          # EA SPORTS FC 27, NBA 2K27, X/X-2 HD
        else:
            # capitaliza cada tramo: RE:BUILD -> Re:Build, no Re:build
            salida.append(re.sub(r"[A-Za-z0-9]+", lambda m: m.group(0).capitalize(), p))
    return " ".join(salida)


def armar_lista(cabecera, lineas, pie, resumen):
    """Mete todas las líneas que entren en el límite más chico (X, 280) y resume el resto.

    Se calcula sobre el texto COMPLETO —no sólo sobre las líneas— porque si no, el
    encabezado, el link y las etiquetas hacen que el posteo se pase sin avisar.
    """
    limite = min(LIMITES.values())
    for usar in range(len(lineas), 0, -1):
        sobran = len(lineas) - usar
        texto = cabecera + "\n".join(lineas[:usar]) + (resumen(sobran) if sobran else "") + pie
        if len(texto) <= limite:
            return texto
    return cabecera + resumen(len(lineas)) + pie


def url(j):
    return f"{SITIO}/juegos/{j['id']}"


def fecha_larga(f):
    y, m, d = map(int, f.split("-"))
    return f"{d} de {MESES_ES[m-1]}"


def mostrar(nombre, texto):
    print(f"\n▸ OPCIÓN {nombre}")
    print("─" * 62)
    print(texto)
    print("─" * 62)
    marcas = []
    for red, limite in LIMITES.items():
        n = len(texto)
        marcas.append(f"{red}: {n}/{limite} {'✓' if n <= limite else '✗ SE PASA'}")
    print("  " + "  |  ".join(marcas))


def opcion_hoy(hoy, juegos):
    dia = [j for j in juegos if j["fecha"] == hoy and not j.get("estimado")]
    if not dia:
        return None
    if len(dia) == 1:
        j = dia[0]
        mc = f"\nPuntaje: {j['metacritic']} en Metacritic" if j.get("metacritic") else ""
        return (f"🎮 Hoy sale {titulo(j)}\n\n"
                f"Plataformas: {plats(j)}{mc}\n\n"
                f"Ficha completa 👉 {url(j)}\n\n{TAGS}")

    # Con varios, entran los que quepan y el resto se resume
    return armar_lista(
        cabecera=f"🎮 Lanzamientos de HOY ({fecha_larga(hoy)})\n\n",
        lineas=[f"▸ {titulo(j)} — {plats(j, 3)}" for j in dia],
        pie=f"\n\nCalendario completo 👉 {SITIO}\n\n{TAGS}",
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
    return armar_lista(
        cabecera="📅 Lo que sale esta semana\n\n",
        lineas=lineas,
        pie=f"\n\nTodo el calendario 👉 {SITIO}\n\n{TAGS}",
        resumen=lambda n: f"\n…y {n} más esta semana")


def opcion_regresiva(hoy, juegos, gid=None):
    d0 = datetime.date(*map(int, hoy.split("-")))
    if gid:
        j = next((x for x in juegos if x["id"] == gid), None)
        if not j:
            return f"(no existe ningún juego con id '{gid}')"
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
    return (f"⏳ {cuanto} para {titulo(j)}\n\n"
            f"Sale el {fecha_larga(j['fecha'])} en {plats(j)}\n\n"
            f"Ficha y cuenta regresiva 👉 {url(j)}\n\n{TAGS}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=datetime.date.today().isoformat())
    ap.add_argument("--regresiva", metavar="ID",
                    help="id del juego para la cuenta regresiva (por defecto, el próximo destacado)")
    args = ap.parse_args()

    juegos = cargar_juegos()
    hoy = args.fecha

    print(f"═══ POSTEO DEL DÍA — {hoy} ═══")
    print("Copiar y pegar en X y en Bluesky (el mismo texto sirve para las dos).")

    opciones = [
        ("A · LANZAMIENTOS DE HOY", opcion_hoy(hoy, juegos)),
        ("B · LO QUE VIENE ESTA SEMANA", opcion_semana(hoy, juegos)),
        ("C · CUENTA REGRESIVA", opcion_regresiva(hoy, juegos, args.regresiva)),
    ]
    vacias = 0
    for nombre, texto in opciones:
        if texto:
            mostrar(nombre, texto)
        else:
            vacias += 1
            print(f"\n▸ OPCIÓN {nombre}: (nada para hoy)")

    if vacias == len(opciones):
        print("\nNo hay nada para postear hoy. Pasa si no lanza nada en 7 días.")
    print("\n═══ Elegir una, copiar y publicar ═══")


if __name__ == "__main__":
    main()
