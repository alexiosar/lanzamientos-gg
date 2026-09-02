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


def cargar_juegos():
    """El array JUEGOS de datos/juegos.js, ya como lista de diccionarios.

    Lo necesitan doce scripts y hasta el 02/09/2026 cada uno tenía su copia, en TRES
    variantes distintas. Daban lo mismo con el archivo de hoy, pero no son equivalentes:
    nueve cortaban con `.rstrip(";")` —o sea que se rompen si algún día se agrega algo
    después del array, como el `module.exports` que sí tiene datos/recomendados.js— y dos
    cortaban en el último `]`. Doce copias que sólo coinciden por casualidad son doce
    formas de que un cambio de formato rompa la mitad de los scripts y la otra no, en
    silencio.

    Esta versión es más firme que las tres: se ancla en la declaración `const JUEGOS`, así
    que no la confunde un `=` que aparezca antes en un comentario, y corta en el último `]`,
    así que no la molesta lo que venga después.

    El archivo es JavaScript, no JSON: las claves van sin comillas y hay que agregárselas.
    Van siempre al principio de una línea, que es lo que hace seguro al reemplazo.
    """
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    inicio = src.index("[", src.index("const JUEGOS"))
    cuerpo = src[inicio:src.rindex("]") + 1]
    return json.loads(re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M))


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
               "MOTOGP": "MotoGP", "MXGP": "MXGP", "MYSTBOUND": "Mystbound",
               "RETROSPACE": "RetroSpace"}
# Cuando la palabra suelta es ambigua, la excepción va por título completo. "SIN" acá es
# el nombre del juego de 1998, pero en español es una preposición: si estuviera en
# CASO_PROPIO, cualquier título con "sin" saldría "SiN".
TITULO_EXACTO = {
    "SIN: RELOADED": "SiN: Reloaded",
    "1000XRESIST": "1000xRESIST",
    # "kun" es un honorífico japonés y va en minúscula; después de un guion no se
    # puede deducir, porque Yog-Sothoth sí lleva mayúscula.
    "TRUCK-KUN IS SUPPORTING ME FROM ANOTHER WORLD?!":
        "Truck-kun Is Supporting Me from Another World?!",
}


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
    # La clave se compara en mayúsculas porque algunos títulos ya están guardados con su
    # grafía propia (1000xRESIST) y otros en MAYÚSCULAS como el resto.
    if j["titulo"].upper() in TITULO_EXACTO:
        return TITULO_EXACTO[j["titulo"].upper()]
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
            # Se baja todo y se suben sólo los arranques de palabra. La letra que sigue
            # a un apóstrofo no arranca palabra: sin esa excepción DON'T FRET salía
            # "Don'T Fret" y DANTE'S, "Dante'S". Y no alcanza con no capitalizarla,
            # porque lo que la regex no toca queda como estaba, o sea en mayúscula.
            salida.append(re.sub(r"(?<![\w'’])(\w)", lambda m: m.group(1).upper(), p.lower()))
    return " ".join(salida)
