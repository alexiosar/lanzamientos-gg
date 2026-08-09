#!/usr/bin/env python3
"""Servidor de vista previa que resuelve las URLs limpias del sitio.

Los enlaces internos apuntan a /ps5 y /juegos/<id>, sin extensión, que es como
los sirve Cloudflare en producción. `python3 -m http.server` devolvería 404 en
todas, así que la vista previa local necesita este puente: prueba <ruta>.html
antes de darse por vencido, y sirve 404.html con estado 404 igual que el sitio.

Uso (desde la raíz del proyecto):
    python3 scripts/servidor-local.py [puerto]
"""
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        destino = Path(super().translate_path(path))
        if destino.is_file() or destino.is_dir() and (destino / "index.html").is_file():
            return str(destino)
        con_html = destino.with_name(destino.name + ".html")
        if con_html.is_file():
            return str(con_html)
        return str(destino)

    def send_error(self, code, message=None, explain=None):
        pagina = RAIZ / "404.html"
        if code == 404 and pagina.is_file():
            cuerpo = pagina.read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(cuerpo)
            return
        super().send_error(code, message, explain)


if __name__ == "__main__":
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    ThreadingHTTPServer(("", puerto), partial(Handler, directory=str(RAIZ))).serve_forever()
