#!/usr/bin/env python3
"""Verifica que las carátulas y los trailers cargados sigan existiendo.

Ningún otro script mira esto y las URLs se rompen solas: Steam reorganiza sus
CDN, un estudio borra su video de YouTube, o directamente se cargó mal la URL.
El 11/08/2026, la primera vez que se corrió esto, aparecieron tres carátulas
que devolvían 404 en producción (skatesterre, pro-jank-footy y
aliens-fireteam-elite-2, las tres con una URL de library_600x900 inexistente) y
un trailer con el id de YouTube truncado a 10 caracteres.

Nada de esto se nota mirando el sitio: una carátula rota muestra el marcador de
"sin carátula", que es exactamente igual al de un juego que todavía no tiene, y
un trailer roto solo se ve si alguien entra a esa ficha y le da play.

Uso (desde la raíz del proyecto):
    python3 scripts/verificar-enlaces.py
"""
import json
import re
import ssl
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CTX = ssl._create_unverified_context()
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def juegos():
    src = (RAIZ / "datos" / "juegos.js").read_text(encoding="utf-8")
    cuerpo = re.sub(r'(\n\s*)([a-zA-Z_][a-zA-Z0-9_]*):', r'\1"\2":',
                    src[src.index("["):src.rindex("]") + 1])
    return json.loads(cuerpo)


def responde(url, metodo="HEAD", intentos=3):
    """True si responde 200. Reintenta antes de dar algo por roto.

    Sin esto el chequeo da falsos positivos: en la primera corrida marcó dos
    carátulas como caídas y las dos respondían 200 al reintentarlas. Un chequeo
    que grita en falso se termina ignorando, que es peor que no tenerlo.
    Un 404 no se reintenta: es una respuesta clara, no un fallo de red.
    """
    ultimo = "error"
    for intento in range(intentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA}, method=metodo)
            if urllib.request.urlopen(req, timeout=20, context=CTX).status == 200:
                return True
        except Exception as ex:
            ultimo = getattr(ex, "code", "error")
            if isinstance(ultimo, int) and 400 <= ultimo < 500:
                return ultimo
        time.sleep(0.5 * (intento + 1))
    return ultimo


def main():
    datos = juegos()
    print(f"═══ VERIFICACIÓN DE ENLACES ═══  ({len(datos)} juegos)\n")

    imgs = [(j["id"], j["imagen"]) for j in datos if j.get("imagen")]
    print(f"── Carátulas ({len(imgs)}) ──")
    rotas = []
    for gid, u in imgs:
        r = responde(u)
        if r is not True:
            rotas.append((gid, r, u))
        time.sleep(0.05)
    print(f"  rotas: {len(rotas)}")
    for gid, code, u in rotas:
        print(f"    {code}  {gid}\n         {u}")

    trailers = [(j["id"], j["trailer"]) for j in datos if j.get("trailer")]
    print(f"\n── Trailers ({len(trailers)}) ──")
    malos = []
    for gid, u in trailers:
        m = re.search(r"embed/([\w-]+)", u)
        # los ids de YouTube son siempre de 11 caracteres: uno más corto es un
        # id truncado al cargarlo, y el embed queda roto sin avisar
        if not m or len(m.group(1)) != 11:
            malos.append((gid, "id inválido", u))
            continue
        r = responde(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={m.group(1)}"
                     f"&format=json", "GET")
        if r is not True:
            malos.append((gid, r, u))
        time.sleep(0.04)
    print(f"  rotos: {len(malos)}")
    for gid, code, u in malos:
        print(f"    {code}  {gid}\n         {u}")

    total = len(rotas) + len(malos)
    print(f"\n═══ {'todo en orden' if not total else str(total) + ' enlace(s) para arreglar'} ═══")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
