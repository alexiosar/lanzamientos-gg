#!/usr/bin/env python3
"""Genera el avatar y la portada para los perfiles de X y Bluesky.

Reusa la identidad del sitio: fondo negro, monoespaciada, acento #a0a0ff y el cursor
en bloque. El avatar repite la marca "L▸" del favicon para que se reconozca igual en
la pestaña del navegador y en la red social.

Uso (desde la raíz del proyecto):
    python3 scripts/generar-imagenes-redes.py

Salida en redes/: avatar.png (400x400) y portada.png (1500x500).
El mismo par sirve para X y para Bluesky: las dos usan avatar cuadrado y portada 3:1.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "redes"
MENLO = "/System/Library/Fonts/Menlo.ttc"

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ACENTO = (160, 160, 255)
GRIS = (51, 51, 51)
GRIS_TEXTO = (136, 136, 136)


def fuente(tam, negrita=True):
    return ImageFont.truetype(MENLO, tam, index=1 if negrita else 0)


def centrar(draw, texto, font, cx, y, fill):
    """Dibuja `texto` centrado horizontalmente en cx, con la parte superior en y."""
    x0, y0, x1, y1 = draw.textbbox((0, 0), texto, font=font)
    draw.text((cx - (x1 - x0) / 2 - x0, y - y0), texto, font=font, fill=fill)


def avatar(lado=400):
    """Marca 'L▸': legible incluso en el círculo de 40px de la línea de tiempo.

    Dos decisiones que vienen de cómo se ve en la red y no de cómo se ve el archivo:
    - X y Bluesky recortan el avatar en círculo, así que el marco es un aro, no un
      cuadrado: un rectángulo perdería las cuatro esquinas.
    - El aro va en el color de acento y no en gris: sobre el fondo casi negro del modo
      oscuro de X, un avatar negro con borde gris se funde con la línea de tiempo.
    """
    escala = 4                                   # se dibuja en grande y se reduce: bordes suaves
    L = lado * escala
    img = Image.new("RGB", (L, L), NEGRO)
    d = ImageDraw.Draw(img)

    aro = int(L * 0.030)
    d.ellipse([aro // 2, aro // 2, L - aro // 2 - 1, L - aro // 2 - 1],
              outline=ACENTO, width=aro)

    f = fuente(int(L * 0.40))
    x0, y0, x1, y1 = d.textbbox((0, 0), "L", font=f)
    ancho_l, alto_l = x1 - x0, y1 - y0
    sep = int(L * 0.055)
    lado_tri = int(alto_l * 0.58)
    ancho_tri = lado_tri * 0.85

    # Se centra el grupo completo (L + triángulo) por su tinta real, no por la caja
    # de la fuente, que trae espacio muerto arriba y abajo.
    izq = (L - (ancho_l + sep + ancho_tri)) / 2
    cima = (L - alto_l) / 2

    d.text((izq - x0, cima - y0), "L", font=f, fill=BLANCO)

    # El triángulo se dibuja a mano y no como carácter: así queda nítido en cualquier tamaño
    tx = izq + ancho_l + sep
    ty = cima + (alto_l - lado_tri) / 2
    d.polygon([(tx, ty), (tx + ancho_tri, ty + lado_tri / 2), (tx, ty + lado_tri)],
              fill=ACENTO)
    return img.resize((lado, lado), Image.LANCZOS)


def portada(ancho=1500, alto=500):
    """Portada 3:1. En X el avatar tapa la esquina inferior izquierda: el texto va arriba."""
    img = Image.new("RGB", (ancho, alto), NEGRO)
    d = ImageDraw.Draw(img)
    d.rectangle([24, 24, ancho - 25, alto - 25], outline=GRIS, width=2)

    cx = ancho / 2
    f_titulo = fuente(96)
    f_bajada = fuente(30, negrita=False)
    f_plats = fuente(28, negrita=False)

    titulo = "LANZAMIENTOS.LAT"
    x0, y0, x1, y1 = d.textbbox((0, 0), titulo, font=f_titulo)
    ancho_t = x1 - x0
    bloque = int(f_titulo.size * 0.62)          # el cursor en bloque, como en el sitio
    total = ancho_t + 14 + bloque * 0.55
    izq = cx - total / 2
    y_titulo = 132
    d.text((izq - x0, y_titulo - y0), titulo, font=f_titulo, fill=BLANCO)
    d.rectangle([izq + ancho_t + 14, y_titulo,
                 izq + ancho_t + 14 + bloque * 0.55, y_titulo + bloque], fill=ACENTO)

    centrar(d, "▸ CALENDARIO DE VIDEOJUEGOS EN ESPAÑOL ◂", f_bajada, cx, 268, ACENTO)
    centrar(d, "PS5 · PS4 · XBOX · SWITCH 2 · SWITCH", f_plats, cx, 330, GRIS_TEXTO)
    centrar(d, "ACTUALIZADO TODOS LOS DÍAS", f_plats, cx, 386, GRIS_TEXTO)
    return img


def main():
    DESTINO.mkdir(exist_ok=True)
    avatar().save(DESTINO / "avatar.png")
    portada().save(DESTINO / "portada.png")
    for f in sorted(DESTINO.glob("*.png")):
        with Image.open(f) as im:
            print(f"  redes/{f.name}: {im.size[0]}x{im.size[1]} — {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
