#!/usr/bin/env python3
"""Busca videos en YouTube y verifica un id, para tráilers y gameplays en español.

El navegador de la app tiene YouTube bloqueado, pero `curl` con un user-agent de navegador
entra bien. Este script junta las tres cosas que se usan al cargar un video:

  buscar      La página de resultados trae los datos en `ytInitialData`; de ahí salen id,
              título, canal y hace cuánto se publicó.
  --verificar oEmbed: confirma que el id existe y devuelve título y autor. **Todo video se
              verifica antes de cargarlo**: un id de YouTube tiene 11 caracteres y las
              búsquedas mezclan otros productos (el corto de Pixar por "Lifted").
  --canal     El RSS de un canal por su id (UC…): los últimos videos con fecha. Es la forma
              de ver qué subió L0k0hGaming sin buscar juego por juego (README, "El gameplay
              en español").

Si YouTube devuelve 429 es por exceso de pedidos seguidos: esperar un rato.

Uso (desde la raíz del proyecto):
    python3 scripts/buscar-youtube.py "Moros Protocol trailer"
    python3 scripts/buscar-youtube.py --verificar vHFTZnZa4-c 6e6lN24jpA0
    python3 scripts/buscar-youtube.py --canal UCHybEMsTlz5LLR7MxOOfGjw
"""
import argparse
import html
import json
import re
import ssl
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
# Igual que actualizar.py: el Python de python.org en macOS no trae certificados raíz.
CTX = ssl._create_unverified_context()


def pedir(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-419,es;q=0.9"})
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        return r.read().decode("utf-8", errors="replace")


def buscar(consulta, maximo):
    pagina = pedir("https://www.youtube.com/results?search_query=" + urllib.parse.quote(consulta))
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", pagina, re.S)
    if not m:
        print("  (YouTube no devolvió resultados legibles)")
        return
    encontrados = []

    def recorrer(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                titulo = "".join(r.get("text", "") for r in v.get("title", {}).get("runs", []))
                canal = "".join(r.get("text", "") for r in v.get("ownerText", {}).get("runs", []))
                cuando = v.get("publishedTimeText", {}).get("simpleText", "")
                encontrados.append((v.get("videoId"), titulo, canal, cuando))
            for x in o.values():
                recorrer(x)
        elif isinstance(o, list):
            for x in o:
                recorrer(x)

    recorrer(json.loads(m.group(1)))
    for vid, titulo, canal, cuando in encontrados[:maximo]:
        print(f"  {vid}  {titulo[:80]:80}  {canal[:28]:28}  {cuando}")


def verificar(vid):
    url = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}")
    try:
        d = json.loads(pedir(url))
        print(f"  ✓ {vid}  {d.get('title')}  ·  {d.get('author_name')}")
    except Exception as e:
        print(f"  ✗ {vid}  no existe o no es público ({e})")


def canal(cid, maximo):
    xml = pedir(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
    for entrada in re.findall(r"<entry>(.*?)</entry>", xml, re.S)[:maximo]:
        fecha = re.search(r"<published>(.{10})", entrada).group(1)
        vid = re.search(r"<yt:videoId>(.*?)<", entrada).group(1)
        titulo = html.unescape(re.search(r"<title>(.*?)</title>", entrada).group(1))
        print(f"  {fecha}  {vid}  {titulo}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("consulta", nargs="*", help="texto a buscar")
    ap.add_argument("--verificar", nargs="+", metavar="ID", help="ids a confirmar con oEmbed")
    ap.add_argument("--canal", metavar="UC…", help="últimos videos de un canal")
    ap.add_argument("--max", type=int, default=10, help="cuántos resultados mostrar")
    args = ap.parse_args()

    if args.verificar:
        for vid in args.verificar:
            verificar(vid)
    elif args.canal:
        canal(args.canal, args.max)
    elif args.consulta:
        buscar(" ".join(args.consulta), args.max)
    else:
        ap.error("pasá una búsqueda, --verificar ID o --canal UC…")


if __name__ == "__main__":
    main()
