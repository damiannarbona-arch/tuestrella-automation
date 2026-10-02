"""Tarjetas iguales para la sección "Casos reales" de kivoa.es: sus 4 fotos del móvil → su retrato.

Uso: python3 generador/web/galeria_casos.py  → assets/web/casos/<caso>.jpg (1200×1500, 4:5)
Para añadir un caso: una línea en CASOS (carpeta, retrato, rótulo, centro de cada foto).
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = lambda *p: os.path.join(RAIZ, 'assets', *p)
FU = lambda n, s: ImageFont.truetype(os.path.join(RAIZ, 'generador', 'fuentes', n), s)
W, H = 1200, 1500
PAPEL, TINTA, GRIS, SALVIA = (246, 242, 236), (44, 51, 47), (80, 86, 85), (63, 81, 71)

# carpeta, retrato, nombre, estilo, centro (fx, fy) de foto-principal y extra-1..3
CASOS = [
    ('bizcocho', 'retrato-clasico-es.jpg', 'Bizcocho', 'Clásico', [(.36, .36), (.45, .35), (.45, .3), (.5, .4)]),
    ('lula', 'retrato-rosa-es.jpg', 'Lula', 'Rosa', [(.5, .3), (.5, .35), (.34, .3), (.63, .45)]),
    ('miau', 'retrato-lavanda.jpg', 'Miau', 'Lavanda', [(.5, .4), (.5, .4), (.5, .4), (.5, .4)]),
    ('sonic', 'retrato-aventurero-es.jpg', 'Sonic', 'Aventurero', [(.5, .38), (.55, .6), (.78, .72), (.6, .5)]),
    ('ricky', 'retrato-clasico-es.jpg', 'Ricky', 'Clásico', [(.45, .4), (.48, .45), (.5, .45), (.55, .5)]),
]


def abrir(p):
    return ImageOps.exif_transpose(Image.open(p)).convert('RGB')


def sombra(im, caja, r=16, alfa=70, off=(0, 10)):
    capa = Image.new('RGBA', im.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = caja
    ImageDraw.Draw(capa).rectangle((x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1]), fill=(40, 30, 20, alfa))
    im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(r)))


def tarjeta(caso, retrato, nombre, estilo, focos):
    im = Image.new('RGBA', (W, H), PAPEL + (255,))
    d = ImageDraw.Draw(im)
    d.text((W / 2, 92), 'SUS 4 FOTOS DEL MÓVIL', font=FU('QuattrocentoSans-Bold.ttf', 26), fill=SALVIA, anchor='ms')
    fotos = [abrir(A('casos', caso, 'foto-principal.jpg'))] + [abrir(A('casos', caso, f'extra-{i}.jpg')) for i in (1, 2, 3)]
    lado, g = 245, 20
    x0 = (W - 4 * lado - 3 * g) / 2
    for i, (f, foco) in enumerate(zip(fotos, focos)):
        x = int(x0 + i * (lado + g))
        sombra(im, (x, 125, x + lado, 125 + lado), r=10, alfa=55, off=(0, 6))
        im.paste(ImageOps.fit(f, (lado, lado), Image.LANCZOS, centering=foco), (x, 125))
    d = ImageDraw.Draw(im)
    ya = 125 + lado + 30  # flecha hacia abajo
    d.line((W / 2, ya, W / 2, ya + 44), fill=TINTA, width=5)
    d.polygon([(W / 2 - 16, ya + 36), (W / 2 + 16, ya + 36), (W / 2, ya + 60)], fill=TINTA)
    ret = abrir(A('casos', caso, retrato))
    rh = 930
    rw = int(ret.width * rh / ret.height)
    rx, ry = (W - rw) // 2, ya + 84
    sombra(im, (rx, ry, rx + rw, ry + rh), r=20, alfa=85, off=(0, 14))
    im.paste(ret.resize((rw, rh), Image.LANCZOS), (rx, ry))
    # rótulo centrado: "Bizcocho · estilo Clásico"
    txt_n, txt_e = nombre, f'  ·  estilo {estilo}'
    fn, fe = FU('Trirong-Regular.ttf', 44), FU('Trirong-LightItalic.ttf', 40)
    wn, we = d.textlength(txt_n, font=fn), d.textlength(txt_e, font=fe)
    im2 = Image.new('RGBA', (W, H), PAPEL + (255,))
    im2.alpha_composite(im.crop((0, 0, W, H - 110)), (0, 0))
    d = ImageDraw.Draw(im2)
    xs = (W - wn - we) / 2
    d.text((xs, H - 52), txt_n, font=fn, fill=TINTA, anchor='ls')
    d.text((xs + wn, H - 52), txt_e, font=fe, fill=GRIS, anchor='ls')
    out = A('web', 'casos', f'{caso}.jpg')
    im2.convert('RGB').save(out, quality=88, optimize=True)
    print(out)


if __name__ == '__main__':
    for c in CASOS:
        tarjeta(*c)
