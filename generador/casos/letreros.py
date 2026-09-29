"""Escribe texto en los letreros de madera del Estilo Aventurero (ChatGPT los deja en blanco).
Tinta marrón en modo multiplicar para que se vea la veta de la madera, como pintado a mano.

Uso: python3 generador/casos/letreros.py RETRATO "TEXTO1" "TEXTO2" "TEXTO3"
Los letreros se definen en píxeles del retrato final (3072×4608): centro y giro de cada tabla.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FUENTE = os.path.join(RAIZ, 'generador', 'fuentes', 'QuattrocentoSans-Bold.ttf')
TABLAS = [((2650, 1398), 10.5, 470), ((2690, 1637), -5.5, 440), ((2712, 1862), -8.5, 450)]  # centro, giro, ancho útil
TINTA = np.array([62, 40, 26], float)


def letrero(img, texto, centro, giro, ancho, alto=66):
    tam = alto
    while True:
        f = ImageFont.truetype(FUENTE, tam)
        w = ImageDraw.Draw(Image.new('L', (1, 1))).textlength(texto, font=f) + (len(texto) - 1) * tam * .12
        if w <= ancho or tam < 30:
            break
        tam -= 2
    capa = Image.new('L', (int(w) + 80, tam * 3), 0)
    d, x = ImageDraw.Draw(capa), 40
    for ch in texto:  # espaciado entre letras
        d.text((x, capa.height / 2), ch, font=f, fill=235, anchor='lm')
        x += d.textlength(ch, font=f) + tam * .12
    capa = capa.filter(ImageFilter.GaussianBlur(1.1)).rotate(giro, resample=Image.BICUBIC, expand=True)
    x0, y0 = int(centro[0] - capa.width / 2), int(centro[1] - capa.height / 2)
    a = np.asarray(img).astype(float)
    m = np.asarray(capa).astype(float)[..., None] / 255
    zona = a[y0:y0 + capa.height, x0:x0 + capa.width]
    mult = zona * (TINTA / 255 + (1 - TINTA / 255) * .15)  # multiplicar: deja ver la veta
    a[y0:y0 + capa.height, x0:x0 + capa.width] = zona * (1 - m) + mult * m
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


if __name__ == '__main__':
    ruta, textos = sys.argv[1], sys.argv[2:5]
    img = Image.open(ruta).convert('RGB')
    for t, (c, g, w) in zip(textos, TABLAS):
        img = letrero(img, t.upper(), c, g, w)
    img.save(ruta, quality=95)
    img.crop((2300, 1150, 3050, 2050)).save(ruta.replace('.jpg', '-letreros.jpg'))
    print(ruta)
