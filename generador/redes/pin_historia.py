"""Pin de Pinterest (1000×1500), historia de Instagram (1080×1920) y portada de destacada a partir de una foto real.

Uso: python3 generador/redes/pin_historia.py FOTO NOMBRE [--cx .42 --cy .6]
Salida: assets/redes/pinterest/<nombre>.jpg · assets/redes/historias/<nombre>.jpg · assets/redes/historias/destacada-real.jpg
"""
import argparse, os, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from publicaciones import (A, abrir, recorte, sombra, PAPEL, TINTA, SALVIA, GRIS, ROSA, TIT, TIT_I, MARCA, TXT, TXT_B)  # noqa: E402


def pin(foto, nombre, cx, cy):
    W, H = 1000, 1500
    im = Image.new('RGBA', (W, H), PAPEL + (255,))
    im.paste(recorte(foto, W, 1160, cx, cy), (0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, 372, 96), 28, fill=PAPEL + (235,))
    d.text((206, 70), 'FOTO REAL · SIN FILTROS', font=TXT_B(22), fill=SALVIA, anchor='mm')
    d.text((W / 2, 1238), 'Retrato personalizado de tu mascota', font=TIT(46), fill=TINTA, anchor='mm')
    d.text((W / 2, 1300), 'a partir de una foto de tu móvil', font=TIT_I(40), fill=GRIS, anchor='mm')
    d.line((W / 2 - 50, 1350, W / 2 + 50, 1350), fill=ROSA, width=3)
    d.text((W / 2, 1420), 'Kivoa', font=MARCA(52), fill=SALVIA, anchor='mm')
    os.makedirs(A('redes', 'pinterest'), exist_ok=True)
    ruta = A('redes', 'pinterest', f'{nombre}.jpg')
    im.convert('RGB').save(ruta, quality=92)
    return ruta


def historia(foto, nombre, cx, cy):
    """Foto a pantalla completa con un sello arriba; abajo queda libre para la pegatina de enlace de Instagram."""
    W, H = 1080, 1920
    im = Image.new('RGBA', (W, H), PAPEL + (255,))
    im.paste(recorte(foto, W, H, cx, cy), (0, 0))
    d = ImageDraw.Draw(im)
    f = TXT_B(30)
    t = 'ASÍ LLEGA A CASA · FOTO REAL'
    w = d.textlength(t, font=f) + 80
    d.rounded_rectangle(((W - w) / 2, 250, (W + w) / 2, 322), 36, fill=PAPEL + (235,))
    d.text((W / 2, 287), t, font=f, fill=SALVIA, anchor='mm')
    os.makedirs(A('redes', 'historias'), exist_ok=True)
    ruta = A('redes', 'historias', f'{nombre}.jpg')
    im.convert('RGB').save(ruta, quality=92)
    return ruta


def destacada():
    """Portada de la destacada "Reales": círculo salvia con un marquito dibujado (se ve recortada en círculo)."""
    W, H = 1080, 1920
    im = Image.new('RGB', (W, H), SALVIA)
    d = ImageDraw.Draw(im)
    cx, cy = W / 2, H / 2
    d.rounded_rectangle((cx - 110, cy - 150, cx + 110, cy + 120), 10, outline=PAPEL, width=14)
    d.rounded_rectangle((cx - 70, cy - 110, cx + 70, cy + 80), 6, outline=PAPEL, width=6)
    d.line((cx - 40, cy + 120, cx - 80, cy + 190), fill=PAPEL, width=14)
    d.line((cx + 40, cy + 120, cx + 80, cy + 190), fill=PAPEL, width=14)
    d.ellipse((cx - 22, cy - 40, cx + 22, cy + 4), fill=ROSA)
    ruta = A('redes', 'historias', 'destacada-real.jpg')
    im.save(ruta, quality=95)
    return ruta


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('foto'); p.add_argument('nombre')
    p.add_argument('--cx', type=float, default=.42); p.add_argument('--cy', type=float, default=.6)
    a = p.parse_args()
    f = abrir(a.foto)
    for r in (pin(f, a.nombre, a.cx, a.cy), historia(f, a.nombre, a.cx, .5), destacada()):
        print(r)
