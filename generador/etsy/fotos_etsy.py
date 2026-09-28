"""Fotos de anuncio para Etsy (2400×1800, 4:3) con la estética de assets/etsy.

Uso:
  python3 generador/etsy/fotos_etsy.py                      # fotos comunes a los 5 estilos
  python3 generador/etsy/fotos_etsy.py antes-despues FOTO RETRATO SALIDA [etiqueta_estilo]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = lambda *p: os.path.join(RAIZ, 'assets', *p)
W, H = 2400, 1800
FONDO = (245, 242, 236)
TINTA = (44, 50, 47)
GRIS = (110, 110, 105)
VERDE = (63, 81, 72)
ROJO = (178, 74, 62)
LINEA = (200, 192, 176)
FD = '/usr/share/fonts/truetype/liberation/'
F = lambda n, s: ImageFont.truetype(FD + n, s)
SERIF, ITAL = 'LiberationSerif-Regular.ttf', 'LiberationSerif-Italic.ttf'


def lienzo():
    im = Image.new('RGB', (W, H), FONDO)
    return im, ImageDraw.Draw(im)


def centrado(d, x, y, txt, fuente, color):
    d.text((x, y), txt, font=fuente, fill=color, anchor='mm')


def titulo(d, es, en):
    centrado(d, W / 2, 150, es, F(SERIF, 112), TINTA)
    centrado(d, W / 2, 262, en, F(ITAL, 58), GRIS)


def sombra(im, caja, r=28, off=(8, 14), alfa=70):
    x0, y0, x1, y1 = caja
    capa = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle((x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1]), r, fill=(40, 30, 20, alfa))
    capa = capa.filter(ImageFilter.GaussianBlur(18))
    im.paste(capa, (0, 0), capa)


def redondear(foto, r):
    m = Image.new('L', foto.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, foto.width - 1, foto.height - 1), r, fill=255)
    return m


def check(d, cx, cy, ok, r=46):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=VERDE if ok else ROJO)
    w = 9
    if ok:
        d.line([(cx - r * .42, cy + r * .02), (cx - r * .1, cy + r * .34), (cx + r * .45, cy - r * .3)], fill='white', width=w, joint='curve')
    else:
        k = r * .36
        d.line([(cx - k, cy - k), (cx + k, cy + k)], fill='white', width=w)
        d.line([(cx - k, cy + k), (cx + k, cy - k)], fill='white', width=w)


# ---------------------------------------------------------------- guía de fotos
def guia_fotos():
    im, d = lienzo()
    titulo(d, 'Qué foto enviarnos', 'Which photo to send')
    base = Image.open(A('antes-foto-luna.jpg')).convert('RGB')
    cara = base.crop((380, 520, 1060, 1260))  # cabeza y pecho de Luna, nítida y con luz
    casos = [
        (cara, True, 'Nítida y con luz', 'Sharp, good light', 'La cara bien visible'),
        (cara.filter(ImageFilter.GaussianBlur(9)), False, 'Movida o borrosa', 'Blurry', 'Perdemos el detalle'),
        (ImageEnhance.Contrast(ImageEnhance.Brightness(cara).enhance(.28)).enhance(.8), False, 'Oscura', 'Too dark', 'Sin luz no hay color'),
        (ImageOps.fit(base, cara.size, Image.LANCZOS, centering=(.5, .5)).resize((cara.width // 3, cara.height // 3)).resize(cara.size, Image.BICUBIC), False, 'Lejos o pixelada', 'Too far / low-res', 'Captura, zoom, recorte'),
    ]
    fw, fh = 490, 640
    gap = (W - 4 * fw) / 5
    y0 = 400
    for i, (foto, ok, es, en, nota) in enumerate(casos):
        x0 = round(gap + i * (fw + gap))
        f = ImageOps.fit(foto, (fw, fh), Image.LANCZOS)
        caja = (x0, y0, x0 + fw, y0 + fh)
        sombra(im, caja)
        im.paste(f, (x0, y0), redondear(f, 24))
        if ok:
            d.rounded_rectangle((x0 - 10, y0 - 10, x0 + fw + 10, y0 + fh + 10), 32, outline=VERDE, width=8)
        check(d, x0 + fw - 10, y0 + 10, ok)
        cx = x0 + fw / 2
        centrado(d, cx, y0 + fh + 90, es, F(SERIF, 56), TINTA)
        centrado(d, cx, y0 + fh + 158, en, F(ITAL, 42), GRIS)
        centrado(d, cx, y0 + fh + 228, nota, F(ITAL, 38), VERDE if ok else ROJO)
    d.line((300, 1450, W - 300, 1450), fill=LINEA, width=3)
    centrado(d, W / 2, 1545, 'Mejor la foto original del móvil que una captura de WhatsApp', F(ITAL, 54), TINTA)
    centrado(d, W / 2, 1625, 'The original phone photo beats a screenshot · up to 3 extra photos', F(ITAL, 40), GRIS)
    im.save(A('etsy', 'foto-que-foto-enviar.jpg'), quality=92)


# ------------------------------------------------------- vista previa en el móvil
def burbuja(d, caja, color, r=34):
    d.rounded_rectangle(caja, r, fill=color)


def vista_previa():
    im, d = lienzo()
    # texto a la izquierda
    x = 170
    d.text((x, 360), 'Tu vista previa', font=F(SERIF, 112), fill=TINTA)
    d.text((x, 490), 'en 48 h', font=F(SERIF, 112), fill=TINTA)
    d.text((x, 640), 'Your digital proof in 48 h', font=F(ITAL, 54), fill=GRIS)
    puntos = [('Te la enviamos por mensaje de Etsy', 'Sent via Etsy messages'),
              ('2 rondas de cambios incluidas', '2 rounds of changes included'),
              ('Nada se imprime sin tu OK', 'Nothing is printed without your OK')]
    y = 830
    for es, en in puntos:
        check(d, x + 40, y + 34, True, r=38)
        d.text((x + 110, y), es, font=F(SERIF, 56), fill=TINTA)
        d.text((x + 110, y + 70), en, font=F(ITAL, 40), fill=GRIS)
        y += 200
    # teléfono a la derecha
    pw, ph = 780, 1560
    px, py = 1440, (H - ph) // 2 + 10
    sombra(im, (px, py, px + pw, py + ph), r=110, off=(14, 24), alfa=90)
    d.rounded_rectangle((px, py, px + pw, py + ph), 110, fill=(30, 32, 34))
    m = 26
    sx0, sy0, sx1, sy1 = px + m, py + m, px + pw - m, py + ph - m
    d.rounded_rectangle((sx0, sy0, sx1, sy1), 88, fill=(250, 249, 246))
    d.rounded_rectangle((px + pw / 2 - 110, sy0 + 22, px + pw / 2 + 110, sy0 + 70), 24, fill=(30, 32, 34))
    # cabecera del chat
    d.line((sx0, sy0 + 190, sx1, sy0 + 190), fill=(225, 220, 212), width=3)
    d.ellipse((sx0 + 40, sy0 + 105, sx0 + 115, sy0 + 180), fill=VERDE)
    centrado(d, sx0 + 77, sy0 + 142, 'K', F(SERIF, 44), 'white')
    d.text((sx0 + 140, sy0 + 124), 'Kivoa', font=F(SERIF, 46), fill=TINTA, anchor='lm')
    d.text((sx0 + 140, sy0 + 166), 'Mensaje de Etsy', font=F(ITAL, 26), fill=GRIS, anchor='lm')
    # mensaje con la vista previa
    bx0, by0 = sx0 + 36, sy0 + 240
    bx1 = sx1 - 110
    ret = Image.open(A('despues-retrato-luna-v2.webp')).convert('RGB')
    rw = bx1 - bx0 - 60
    rh = round(rw * ret.height / ret.width)
    ret = ret.resize((rw, rh), Image.LANCZOS)
    burbuja(d, (bx0, by0, bx1, by0 + rh + 190), (236, 232, 224))
    d.text((bx0 + 30, by0 + 26), '¡Aquí tienes su vista previa!', font=F(SERIF, 36), fill=TINTA)
    im.paste(ret, (bx0 + 30, by0 + 90), redondear(ret, 16))
    d.text((bx0 + 30, by0 + 90 + rh + 26), '¿Quieres cambiar algo?', font=F(ITAL, 34), fill=GRIS)
    # respuesta del cliente
    ry0 = by0 + rh + 230
    txt = '¡Me encanta! Adelante'
    f = F(SERIF, 38)
    tw = d.textlength(txt, font=f)
    burbuja(d, (sx1 - 36 - tw - 70, ry0, sx1 - 36, ry0 + 90), VERDE, r=45)
    d.text((sx1 - 36 - tw - 35, ry0 + 45), txt, font=f, fill='white', anchor='lm')
    im.save(A('etsy', 'foto-vista-previa.jpg'), quality=92)


# ------------------------------------------------------------- antes / después
def antes_despues(foto, retrato, salida, estilo=None):
    im, d = lienzo()
    fw, fh = 860, 1200
    y0 = 170
    xs = (230, W - 230 - fw)
    for x, p in zip(xs, (foto, retrato)):
        f = ImageOps.fit(Image.open(p).convert('RGB'), (fw, fh), Image.LANCZOS, centering=(.5, .45))
        sombra(im, (x, y0, x + fw, y0 + fh), r=6)
        im.paste(f, (x, y0))
    # flecha
    ax0, ax1, ay = 230 + fw + 40, W - 230 - fw - 40, y0 + fh / 2
    d.line((ax0, ay, ax1 - 30, ay), fill=TINTA, width=10)
    d.polygon([(ax1, ay), (ax1 - 50, ay - 34), (ax1 - 50, ay + 34)], fill=TINTA)
    for x, es, en in ((xs[0], 'Tu foto', 'Your photo'), (xs[1], 'Su retrato', 'Their portrait')):
        centrado(d, x + fw / 2, y0 + fh + 120, es, F(SERIF, 88), TINTA)
        centrado(d, x + fw / 2, y0 + fh + 210, en, F(ITAL, 50), GRIS)
    if estilo:
        centrado(d, W / 2, H - 70, estilo, F(ITAL, 40), GRIS)
    im.save(salida, quality=92)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'antes-despues':
        antes_despues(*sys.argv[2:])
    else:
        os.makedirs(A('etsy'), exist_ok=True)
        guia_fotos()
        vista_previa()
        antes_despues(A('antes-foto-luna.jpg'), A('despues-retrato-luna-v2.webp'),
                      A('etsy', 'foto-antes-despues-rosa.jpg'), 'Ejemplo real · estilo Rosa')
        print('ok')
