#!/usr/bin/env python3
"""Cosas que usan varios scripts. Hoy: pasar los títulos de MAYÚSCULAS a normales.

Los títulos viven en MAYÚSCULAS en datos/juegos.js porque así los muestra el sitio.
Pero fuera del sitio gritan: en un posteo de Bluesky y en un resultado de Google,
un título todo en mayúsculas se lee peor y desentona con el resto.

Convertirlo no es trivial: hay números romanos (DOOM II, no Doom Ii), siglas
(EA SPORTS, NBA 2K27), preposiciones que van en minúscula en medio de un título
(City of Wolves, no City Of Wolves) y caracteres con diacríticos que rompen la
detección de vocales (TŌKON). Por eso está acá y no duplicado en cada script.
"""
import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def leer_noticias_propias():
    """Las de datos/noticias.js: PS Plus, Directs, cierres de estudios, rumores.

    Lo leen tres generadores (la página de noticias, los feeds y las fichas), así
    que vive acá: si el formato del archivo cambia, se toca en un solo lugar.
    """
    archivo = RAIZ / "datos" / "noticias.js"
    if not archivo.exists():
        return []
    src = archivo.read_text(encoding="utf-8")
    inicio = src.index("const NOTICIAS = [") + len("const NOTICIAS = ")
    fin = src.index("\n];", inicio) + 2
    # es JavaScript, no JSON: las claves van sin comillas
    cuerpo = re.sub(r'(\n\s*)([a-zA-Z_][a-zA-Z0-9_]*):', r'\1"\2":', src[inicio:fin])
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
# Marcas que se escriben con una mayúscula adentro y no al principio. No hay regla que
# las deduzca desde MAYÚSCULAS: van a mano. "IRACING" no es ni Iracing ni IRACING.
CASO_PROPIO = {"IRACING": "iRacing", "PLAYSTATION": "PlayStation", "XBOX": "Xbox",
               "MOTOGP": "MotoGP", "MXGP": "MXGP", "MYSTBOUND": "Mystbound"}


def plat(p):
    return PLATS.get(p, p)


def plats(j, maximo=4):
    ps = [plat(p) for p in j["plataformas"]]
    return "/".join(ps[:maximo]) + ("+" if len(ps) > maximo else "")


def _sin_diacriticos(t):
    """TŌKON -> TOKON. Sin esto, la Ō no cuenta como vocal y el título se toma por
    sigla: 'Marvel Tōkon' terminaba escrito 'Marvel TŌKon'."""
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def titulo(j):
    """Los títulos están en MAYÚSCULAS en la base; en redes gritan demasiado."""
    palabras = j["titulo"].split()
    salida = []
    for i, p in enumerate(palabras):
        nucleo = p.strip(":()!?¡¿,.-'’")
        limpio = re.sub(r"[^A-Za-z0-9]", "", _sin_diacriticos(nucleo))
        if limpio.upper() in CASO_PROPIO:
            salida.append(p.replace(nucleo, CASO_PROPIO[limpio.upper()]))
        elif not limpio:
            salida.append(p)
        elif ROMANOS.match(limpio) and limpio.upper() in {
                "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "XIII",
                "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"}:
            salida.append(p.upper())          # DOOM II, no Doom Ii
        elif ORDINAL.match(limpio):
            salida.append(p[:-2] + p[-2:].lower())   # 2ND -> 2nd
        elif i > 0 and limpio.lower() in MINUSCULAS and not palabras[i - 1].endswith(":"):
            salida.append(p.lower())          # City of Wolves, no City Of Wolves
        elif limpio.upper() in SIGLAS or not re.search(r"[AEIOUY]", limpio, re.I) \
                or (re.search(r"\d", limpio) and len(limpio) <= 5):
            salida.append(p.upper())          # EA SPORTS FC 27, NBA 2K27, X/X-2 HD
        else:
            # capitaliza cada tramo: RE:BUILD -> Re:Build, no Re:build. El patrón es \w
            # y no [A-Za-z] para que TŌKON quede "Tōkon" y no "TŌKon".
            salida.append(re.sub(r"\w+", lambda m: m.group(0).capitalize(), p))
    return " ".join(salida)
