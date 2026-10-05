#!/usr/bin/env python3
"""Compara la fecha de los próximos lanzamientos con la que dicen las tiendas de Xbox y Nintendo.

Por qué existe (05/10/2026): la revisión de los juegos "dados por lanzados" encontró que el
error más común del calendario no es cargar mal un juego, sino que **se retrase y nadie lo
cargue**. Don't Fret siguió anunciado para el 1/10 dos meses después de retrasarse, y la
tienda de Xbox ya decía "sin día". Steins;Gate Re:Boot figuraba en Xbox el 20/08 cuando esa
versión se había pasado al 29/10. Ninguno tenía noticias, así que ningún chequeo los miraba.

Este script mira hacia adelante: toma los juegos con día confirmado en los próximos N días y
pregunta a las tiendas. Avisa cuando:
  - la tienda tiene **otra fecha** (más de un día de diferencia: un día es zona horaria),
  - la tienda dice **"sin día"** (el "próximamente" de cada una), que casi siempre es un retraso,
  - la ficha de Microsoft es **sólo de PC** (`Windows.Desktop`), que no es la versión de Xbox.
Un falso positivo conocido: para juegos en preventa, Microsoft a veces da como fecha el día en
que abrió la reserva (Dragon's Dogma 2: Dark Arisen figuraba "25/06" saliendo el 9/10). Si
la alerta es de Xbox y la fecha es anterior a hoy en un juego que no salió, mirar la PS Store.

Lo que no encuentra lo lista aparte: no prueba nada, porque los buscadores fallan con
nombres traducidos o con signos raros, pero conviene mirarlo.

PlayStation queda afuera: la PS Store no tiene una API que responda sin navegador. Los
juegos que sólo salen en PlayStation se cuentan, para que se sepa que no se miraron.

Uso (desde la raíz del proyecto):
    python3 scripts/verificar-proximos.py           # próximos 14 días
    python3 scripts/verificar-proximos.py --dias 7

No modifica nada. Sale con 0 siempre: es un aviso, no un bloqueo del deploy.
"""
import argparse
import datetime
import difflib
import importlib.util
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

from comun import cargar_juegos


def cargar_modulo(nombre):
    """Los buscadores tienen guion en el nombre y no se importan con `import`."""
    spec = importlib.util.spec_from_file_location(nombre.replace("-", "_"), RAIZ / "scripts" / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


xbox = cargar_modulo("buscar-xbox")
eshop = cargar_modulo("buscar-eshop")

UMBRAL = 0.85


def clave(t):
    """Título comparable: sin acentos, sin ™/®, sin el sufijo de edición de Switch 2."""
    t = re.sub(r"\s*[—–-]\s*NINTENDO SWITCH(?:™)? 2 EDITION.*$", "", t, flags=re.I)
    t = re.sub(r"for Nintendo Switch(?:™)? 2", "", t, flags=re.I)
    t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t.lower().replace("™", "").replace("®", "")).strip()


def parecido(a, b):
    """0 a 1. Sin atajo por prefijo: "Dragon's Dogma 2" no es "Dragon's Dogma 2: Dark Arisen",
    ni "Gear.Club Unlimited 3" es su Deluxe Edition. Y si los números no coinciden, no es el
    mismo juego aunque el resto sea igual: "Party Pack 12" no es "Party Pack 4"."""
    a, b = clave(a), clave(b)
    if not a or not b:
        return 0
    if re.findall(r"\d+", a) != re.findall(r"\d+", b):
        return 0
    return 1 if a == b else difflib.SequenceMatcher(None, a, b).ratio()


def dias_entre(a, b):
    return abs((datetime.date.fromisoformat(a) - datetime.date.fromisoformat(b)).days)


def consultar_xbox(titulo):
    """(fecha, solo_pc, titulo_tienda) del mejor resultado, o None si no lo encuentra."""
    ids = []
    for grupo in xbox.pedir(xbox.SUGERENCIAS + xbox.urllib.parse.quote(titulo)).get("ResultSets", []):
        for s in grupo.get("Suggests", []):
            meta = {m.get("Key"): m.get("Value") for m in (s.get("Metas") or [])}
            if meta.get("ProductType") == "Game" and meta.get("BigCatalogId"):
                ids.append(meta["BigCatalogId"])
    if not ids:
        return None
    mejor = None
    for p in xbox.pedir(xbox.CATALOGO + ",".join(ids[:4])).get("Products", []):
        nombre = p["LocalizedProperties"][0]["ProductTitle"]
        if re.search(r"\b(demo|soundtrack|bundle|pack)\b", nombre, re.I):
            continue
        r = parecido(titulo, nombre)
        if r < UMBRAL or (mejor and (r, -len(nombre)) <= (mejor[0], -len(mejor[3]))):
            continue
        fecha = (p.get("MarketProperties", [{}])[0].get("OriginalReleaseDate") or "?")[:10]
        plats = set()
        for sku in p.get("DisplaySkuAvailabilities", []):
            for a in sku.get("Availabilities", []):
                for pl in (a.get("Conditions", {}).get("ClientConditions", {}).get("AllowedPlatforms") or []):
                    plats.add(pl.get("PlatformName"))
        solo_pc = bool(plats) and not any("Xbox" in (x or "") for x in plats)
        mejor = (r, fecha, solo_pc, nombre)
    return mejor[1:] if mejor else None


def consultar_eshop(titulo, switch2):
    """(fecha, titulo_tienda) de la fila de esa consola, o None si no la encuentra."""
    try:
        docs = eshop.consultar({"q": clave(titulo), "rows": 8, "sort": "score desc"})
    except Exception:
        return None
    mejor = None
    for d in docs:
        # nsuid 7005… son paquetes ("Nintendo Switch 2 Edition" que se compra aparte, bundles):
        # su fecha no es la del juego. Harvest Moon: Echoes of Teradea daba 14/09 por eso.
        if (d.get("nsuid_txt") or [""])[0].startswith("7005"):
            continue
        sistemas = " ".join(d.get("system_names_txt") or [])
        es_s2 = "Switch 2" in sistemas
        if es_s2 != switch2:
            continue
        r = parecido(titulo, d.get("title", ""))
        if r >= UMBRAL and (not mejor or r > mejor[0]):
            mejor = (r, (d.get("dates_released_dts") or ["?"])[0][:10], d.get("title", ""))
    return mejor[1:] if mejor else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dias", type=int, default=14)
    args = ap.parse_args()

    hoy = datetime.date.today()
    hasta = (hoy + datetime.timedelta(days=args.dias)).isoformat()
    proximos = [j for j in cargar_juegos()
                if not j.get("estimado") and hoy.isoformat() <= j["fecha"] <= hasta]

    otra_fecha, sin_dia, solo_pc, no_esta, ok = [], [], [], [], 0
    sin_revisar = 0
    for j in sorted(proximos, key=lambda x: x["fecha"]):
        plats = j["plataformas"]
        revisadas = 0
        consultas = []
        if "XBOX" in plats:
            consultas.append(("Xbox", consultar_xbox(j["titulo"])))
        if "SWITCH2" in plats:
            consultas.append(("Switch 2", consultar_eshop(j["titulo"], True)))
        if "SWITCH" in plats:
            consultas.append(("Switch", consultar_eshop(j["titulo"], False)))
        if not consultas:
            sin_revisar += 1
            continue
        for tienda, res in consultas:
            revisadas += 1
            fila = (j["id"], j["fecha"], tienda)
            if res is None:
                no_esta.append(fila)
                continue
            fecha = res[0]
            # Un 31 de diciembre de la eShop es su "próximamente", salvo que el juego de verdad
            # salga ese día.
            marcador = (fecha.startswith("9998") if tienda == "Xbox"
                        else fecha.endswith("-12-31") and not j["fecha"].endswith("-12-31"))
            if tienda == "Xbox" and res[1]:
                solo_pc.append(fila + (fecha,))
            elif marcador:
                sin_dia.append(fila + (fecha,))
            elif fecha[:4].isdigit() and dias_entre(fecha, j["fecha"]) > 1:
                otra_fecha.append(fila + (fecha,))
            else:
                ok += 1

    print(f"═══ PRÓXIMOS {args.dias} DÍAS CONTRA LAS TIENDAS ═══  ({len(proximos)} juegos con día, "
          f"hasta el {hasta})\n")

    def bloque(titulo, filas, explica):
        if not filas:
            return
        print(f"── {titulo} ──")
        for f in filas:
            extra = f"  tienda: {f[3]}" if len(f) > 3 else ""
            print(f"  ⚠ {f[0]:44} nosotros {f[1]} · {f[2]:8}{extra}")
        print(f"  {explica}\n")

    bloque("La tienda tiene otra fecha", otra_fecha,
           "Verificar y corregir. Si la tienda la cambió hace poco, suele ser un retraso con noticia.")
    bloque("La tienda dice «sin día»", sin_dia,
           "Casi siempre es un retraso que todavía no cargamos (Don't Fret, octubre de 2026).")
    bloque("La ficha de Microsoft es sólo de PC", solo_pc,
           "Esa no es la versión de Xbox: buscar la de consola antes de confiar en la fecha.")
    if no_esta:
        print("── No los encontró (revisar a mano si suena raro) ──")
        for f in no_esta:
            print(f"  · {f[0]:44} nosotros {f[1]} · {f[2]}")
        print("  Los buscadores fallan con nombres traducidos o signos raros: esto no prueba nada.\n")

    total_alertas = len(otra_fecha) + len(sin_dia) + len(solo_pc)
    print(f"  ✓ {ok} coinciden · {total_alertas} para revisar · {len(no_esta)} sin encontrar · "
          f"{sin_revisar} sólo en PlayStation (no se pueden revisar sin navegador)")


if __name__ == "__main__":
    main()
