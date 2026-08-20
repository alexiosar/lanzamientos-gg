#!/usr/bin/env python3
"""Novedades que publican los propios estudios en Steam, para los juegos del calendario.

Por qué existe: los juegos chicos son los que mejor nos rinden en Google —el 20/08/2026,
"sombras: negative frames" tenía 20% de CTR contra 0,6% del sitio entero— y son justo los
que las webs grandes no cubren. Pero el estudio sí los cuenta, en la pestaña de novedades
de su propia página de Steam. Es fuente primaria: no hay que verificar nada, ES el anuncio.

De paso corrige el calendario. El 18/08/2026 el estudio de RetroSpace anunció su fecha en
Steam y releases.com la reflejó recién al día siguiente; para los juegos chicos, Steam se
entera antes que el agregador.

Lo que NO hay que hacer con esto: publicar todo lo que devuelve. La mayoría son notas de
parche, concursos y descuentos, y una entrada floja vale menos que ninguna. El script filtra
por lo que le importa a un calendario —fecha, retraso, plataforma nueva, demo, lanzamiento—
y lo demás lo esconde salvo que se pida.

Uso (desde la raíz del proyecto):
    python3 scripts/novedades-steam.py              # lo nuevo de los últimos 14 días
    python3 scripts/novedades-steam.py --dias 30
    python3 scripts/novedades-steam.py --todos      # sin filtrar por tema
    python3 scripts/novedades-steam.py --repetir    # incluye lo ya visto en corridas previas

Va en la rutina diaria. Guarda en datos/novedades-steam.json lo que ya se mostró, así cada
día aparece sólo lo que no vimos.
"""
import argparse
import datetime
import html as html_mod
import json
import re
import ssl
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / "datos" / "novedades-steam.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

# Cuántos días después del lanzamiento se sigue mirando un juego. Después de eso lo que
# publica el estudio son parches y no le sirve a un calendario.
DIAS_DESPUES = 30

# El filtro mira SÓLO EL TÍTULO. Probado contra 301 juegos el 20/08/2026: buscando también
# en el cuerpo pasaba de todo, porque cualquier nota de parche dice "released" o "available"
# en algún lado. Los estudios titulan estos anuncios de forma bastante parecida.
INTERESA = re.compile(
    r"release date|launch(es|ing|ed)?\b|out now|available now|now available|coming (to|soon)|"
    r"delay|postpon|demo|playtest|open beta|early access|full release|1\.0 |version 1\.0|"
    r"nintendo switch|switch 2|playstation|ps5|ps4|xbox|console|physical edition|award",
    re.I)
# Lo que casi nunca es noticia para un calendario, aunque el título diga "update".
RUIDO = re.compile(
    r"patch|hotfix|bug ?fix|update \d|title update|content.?update|contest|giveaway|"
    r"sale\b|discount|wishlist|soundtrack|vinyl|merch|devlog|roadmap|meme|"
    r"celebrat|festival|screenshot saturday|dev ?diary|behind the scenes", re.I)
# Estos ganan siempre: si están en el título, no importa qué más diga.
MANDA = re.compile(r"release date|out now|delay|postpon|coming to|launches?\b|"
                   r"now available on|physical edition", re.I)
# Fechas que aparecen en el texto, para avisar si no coinciden con la nuestra.
MESES = ("january february march april may june july august september october "
         "november december").split()
FECHA = re.compile(r"\b(" + "|".join(MESES) + r")\s+(\d{1,2})(?:st|nd|rd|th)?\b|"
                   r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(" + "|".join(MESES) + r")\b", re.I)


def get(url, intentos=2):
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")
        except Exception:
            if i == intentos - 1:
                raise
            time.sleep(1)


def cargar_juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    cuerpo = src.split("=", 1)[1].strip().rstrip(";")
    cuerpo = re.sub(r"^(\s*)([a-zA-Z_]\w*):", r'\1"\2":', cuerpo, flags=re.M)
    return json.loads(cuerpo)


def appid(j):
    """El appid de Steam sale de la URL de la carátula, que ya la tenemos cargada."""
    m = re.search(r"/apps/(\d+)/", j.get("imagen") or "")
    return m.group(1) if m else None


def limpiar(texto):
    """El cuerpo viene con BBCode de Steam o con HTML, según el tipo de novedad."""
    texto = re.sub(r"\[/?[^\]]{0,40}\]", " ", texto)      # [b], [url=...], [img]
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = html_mod.unescape(texto)
    return re.sub(r"\s+", " ", texto).strip()


def fechas_mencionadas(texto):
    """Fechas en inglés que aparecen en el anuncio, normalizadas a MM-DD."""
    salida = set()
    for m in FECHA.finditer(texto):
        mes, dia = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(3))
        salida.add(f"{MESES.index(mes.lower()) + 1:02d}-{int(dia):02d}")
    return salida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=14, help="antigüedad máxima de la novedad")
    ap.add_argument("--todos", action="store_true", help="no filtrar por tema")
    ap.add_argument("--repetir", action="store_true", help="incluir lo ya visto")
    args = ap.parse_args()

    hoy = datetime.date.today()
    limite = time.time() - args.dias * 86400
    visto = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}

    juegos = cargar_juegos()
    # Sólo los que están por salir o salieron hace poco: en los viejos, lo que publica el
    # estudio son parches.
    candidatos = []
    for j in juegos:
        a = appid(j)
        if not a:
            continue
        try:
            fecha = datetime.date(*map(int, j["fecha"].split("-")))
        except ValueError:
            continue
        if (hoy - fecha).days <= DIAS_DESPUES:
            candidatos.append((j, a))

    print(f"═══ NOVEDADES EN STEAM ═══  ({len(candidatos)} juegos por salir o recién salidos, "
          f"últimos {args.dias} días)\n")

    hallazgos = 0
    revisar_fecha = []
    for j, a in candidatos:
        url = (f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
               f"?appid={a}&count=5&maxlength=700&format=json")
        try:
            items = json.loads(get(url))["appnews"]["newsitems"]
        except Exception:
            continue
        finally:
            time.sleep(0.25)

        for it in items:
            if it["date"] < limite:
                continue
            clave = f"{j['id']}:{it['gid']}"
            if not args.repetir and clave in visto:
                continue
            texto = limpiar(it.get("contents", ""))
            titulo = it.get("title", "")
            if not args.todos:
                if not MANDA.search(titulo):
                    if RUIDO.search(titulo) or not INTERESA.search(titulo):
                        continue

            visto[clave] = hoy.isoformat()
            hallazgos += 1
            cuando = datetime.datetime.fromtimestamp(it["date"]).strftime("%d/%m")
            fuente = it.get("feedlabel") or ""
            marca = ""
            # Sólo se avisa de fechas cuando el anuncio ES de fecha: si no, cualquier
            # mención suelta ("la oferta termina el 13 de agosto") levantaba la bandera.
            dichas = fechas_mencionadas(titulo + " " + texto[:300]) if MANDA.search(titulo) else set()
            if dichas and j["fecha"][5:] not in dichas:
                marca = "  ⚠ NOMBRA OTRA FECHA"
                revisar_fecha.append((j["id"], j["fecha"], sorted(dichas)))
            print(f"── {j['id']}  ({j['fecha']}, {'/'.join(j['plataformas'])}){marca}")
            print(f"   {cuando} · {fuente[:22]} · {titulo[:80]}")
            print(f"   {texto[:230]}")
            print(f"   {it.get('url','')}\n")

    if not hallazgos:
        print("(nada nuevo)")
    if revisar_fecha:
        print("── Anuncios que nombran una fecha distinta a la nuestra ──")
        for gid, nuestra, dichas in revisar_fecha:
            print(f"   {gid:44} tenemos {nuestra}  ·  el anuncio dice {', '.join(dichas)}")
        print("   Verificar en la tienda antes de tocar nada: puede ser la fecha de una demo,")
        print("   de otra plataforma o de un evento.")

    CACHE.write_text(json.dumps(visto, indent=1, sort_keys=True), encoding="utf-8")
    print(f"\n{hallazgos} novedad(es) · {len(visto)} ya vistas en total")


if __name__ == "__main__":
    main()
