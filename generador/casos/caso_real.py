"""Fotos de anuncio (Etsy/Shopify, 2400×1800) a partir de un caso real, con la estética de assets/etsy.

Carpeta del caso (assets/casos/<mascota>/):
  foto-principal.jpg          la foto con la que se hizo la ilustración
  extra-1.jpg … extra-3.jpg   las fotos secundarias (polaroids)
  retrato-<estilo>.jpg        el retrato terminado (uno o varios estilos)

Uso:
  python3 generador/casos/caso_real.py miau Miau lavanda "ojos de distinto color"
  → assets/casos/miau/anuncio/<estilo>-1-antes-despues.jpg … -4-marcos.jpg

Recortes: FOCO[caso] = (fx, fy) de la cara en la foto principal y en el retrato (0–1).
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'etsy'))
from fotos_etsy import (W, H, FONDO, TINTA, GRIS, VERDE, LINEA, F, SERIF, ITAL,  # noqa: E402
                        lienzo, centrado, sombra, titulo, antes_despues, check)

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)

# cara en la foto principal / en el retrato (fracciones), y tamaño del recorte de detalle (fracción del ancho)
FOCO = {'miau': {'foto': (.52, .44, .62), 'retrato': (.53, .30, .48)}}


def abrir(p):
    return ImageOps.exif_transpose(Image.open(p)).convert('RGB')


def recorte(img, w, h, fx, fy, ancho_rel=None):
    """Recorte de proporción w:h centrado en (fx, fy); ancho_rel = fracción del ancho de la imagen."""
    cw = img.width * ancho_rel if ancho_rel else min(img.width, img.height * w / h)
    ch = cw * h / w
    if ch > img.height:
        ch, cw = img.height, img.height * w / h
    x = min(max(fx * img.width - cw / 2, 0), img.width - cw)
    y = min(max(fy * img.height - ch / 2, 0), img.height - ch)
    return img.resize((w, h), Image.LANCZOS, box=(x, y, x + cw, y + ch))


def polaroid(im, foto, centro, ancho, angulo):
    b = int(ancho * .06)
    w = ancho - 2 * b
    p = Image.new('RGBA', (ancho, w + b + int(b * 2.6)), (252, 250, 246, 255))
    p.paste(ImageOps.fit(foto, (w, w), Image.LANCZOS, centering=(.5, .42)), (b, b))
    p = p.rotate(angulo, resample=Image.BICUBIC, expand=True)
    x, y = int(centro[0] - p.width / 2), int(centro[1] - p.height / 2)
    s = Image.new('RGBA', im.size, (0, 0, 0, 0))
    s.paste(Image.new('RGBA', p.size, (40, 30, 20, 80)), (x + 8, y + 18), p)
    base = im.convert('RGBA')
    base.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
    base.alpha_composite(p, (x, y))
    im.paste(base.convert('RGB'))


def flecha(d, x0, x1, y):
    d.line((x0, y, x1 - 30, y), fill=TINTA, width=10)
    d.polygon([(x1, y), (x1 - 50, y - 34), (x1 - 50, y + 34)], fill=TINTA)


# 2 · De sus fotos a su retrato: demuestra que usamos TODAS las fotos del cliente
def fotos_a_retrato(caso, nombre, estilo, salida):
    im, d = lienzo()
    titulo(d, f'De sus fotos al retrato de {nombre}', f'From {nombre}\'s photos to the portrait')
    fotos = [abrir(C(caso, 'foto-principal.jpg'))] + [abrir(C(caso, f'extra-{i}.jpg')) for i in (1, 2, 3)]
    for foto, c, a in zip(fotos, [(430, 690), (830, 740), (440, 1210), (840, 1250)], [-5, 4, 3, -4]):
        polaroid(im, foto, c, 390, a)
    d = ImageDraw.Draw(im)
    flecha(d, 1110, 1330, 980)
    ret = abrir(C(caso, f'retrato-{estilo}.jpg'))
    rh = 1300
    rw = int(ret.width * rh / ret.height)
    x0, y0 = 1420 + (820 - rw) // 2, 380
    sombra(im, (x0, y0, x0 + rw, y0 + rh), r=6)
    im.paste(ret.resize((rw, rh), Image.LANCZOS), (x0, y0))
    d = ImageDraw.Draw(im)
    centrado(d, 650, 1580, 'La principal + hasta 3 más', F(SERIF, 58), TINTA)
    centrado(d, 650, 1650, 'Main photo + up to 3 extra', F(ITAL, 42), GRIS)
    centrado(d, x0 + rw / 2, 1735, f'Caso real · estilo {estilo.capitalize()}', F(ITAL, 40), GRIS)
    im.save(salida, quality=92)


# 3 · Detalle: la misma zona de la foto y del retrato (fidelidad)
def detalle(caso, nombre, estilo, rasgo, salida):
    im, d = lienzo()
    titulo(d, f'Hasta el último detalle: {rasgo}', 'True to every detail')
    foto, ret = abrir(C(caso, 'foto-principal.jpg')), abrir(C(caso, f'retrato-{estilo}.jpg'))
    ff, fr = FOCO[caso]['foto'], FOCO[caso]['retrato']
    s = 1000
    for x, img, (fx, fy, ar), es, en in ((200, foto, ff, 'Su foto', 'Their photo'),
                                        (W - 200 - s, ret, fr, 'Su retrato', 'Their portrait')):
        c = recorte(img, s, s, fx, fy, ar)
        sombra(im, (x, 400, x + s, 400 + s), r=6)
        im.paste(c, (x, 400))
        centrado(d, x + s / 2, 1500, es, F(SERIF, 64), TINTA)
        centrado(d, x + s / 2, 1570, en, F(ITAL, 42), GRIS)
    d = ImageDraw.Draw(im)
    flecha(d, 1230, 1370, 900)
    centrado(d, W / 2, 1715, f'Caso real · {nombre}', F(ITAL, 40), GRIS)
    im.save(salida, quality=92)


# 4 · Los 3 marcos con su retrato (maqueta plana, sin IA)
def marco(im, ret, caja, color, veta=False):
    x0, y0, x1, y1 = caja
    m = int((x1 - x0) * .07)       # grosor del marco
    pp = int((x1 - x0) * .09)      # paspartú
    sombra(im, caja, r=4, off=(10, 22), alfa=90)
    d = ImageDraw.Draw(im)
    d.rectangle(caja, fill=color)
    if veta:  # madera: vetas suaves
        for i in range(0, y1 - y0, 7):
            t = (math.sin(i * .09) + math.sin(i * .023)) * 6
            c = tuple(int(v + t) for v in color)
            d.line((x0, y0 + i, x1, y0 + i), fill=c, width=3)
    # bisel: luz arriba/izquierda, sombra abajo/derecha
    luz, osc = tuple(min(255, v + 28) for v in color), tuple(max(0, v - 30) for v in color)
    d.polygon([(x0, y0), (x1, y0), (x1 - m, y0 + m), (x0 + m, y0 + m)], fill=luz)
    d.polygon([(x1, y1), (x0, y1), (x0 + m, y1 - m), (x1 - m, y1 - m)], fill=osc)
    d.rectangle((x0 + m, y0 + m, x1 - m, y1 - m), fill=(250, 249, 245))
    ix0, iy0, ix1, iy1 = x0 + m + pp, y0 + m + pp, x1 - m - pp, y1 - m - pp
    im.paste(ImageOps.fit(ret, (ix1 - ix0, iy1 - iy0), Image.LANCZOS, centering=(.5, .45)), (ix0, iy0))
    d.line((ix0, iy0, ix1, iy0), fill=(215, 210, 200), width=3)  # sombra interior del paspartú


def marcos(caso, nombre, estilo, salida):
    im = Image.new('RGB', (W, H), (238, 232, 222))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1560, W, H), fill=(206, 186, 160))           # balda
    d.rectangle((0, 1560, W, 1580), fill=(226, 210, 188))
    ret = abrir(C(caso, f'retrato-{estilo}.jpg'))
    fw, fh = 620, 800
    for i, (col, veta, es, en) in enumerate([((250, 250, 248), False, 'Blanco', 'White'),
                                             ((196, 150, 102), True, 'Madera', 'Natural wood'),
                                             ((34, 34, 34), False, 'Negro', 'Black')]):
        x = 150 + i * (fw + 185)
        marco(im, ret, (x, 520, x + fw, 520 + fh), col, veta)
        d = ImageDraw.Draw(im)
        centrado(d, x + fw / 2, 1650, es, F(SERIF, 60), TINTA)
        centrado(d, x + fw / 2, 1720, en, F(ITAL, 40), GRIS)
    centrado(d, W / 2, 170, f'{nombre}, en el marco que elijas', F(SERIF, 104), TINTA)
    centrado(d, W / 2, 280, f'{nombre}, in the frame of your choice', F(ITAL, 56), GRIS)
    im.save(salida, quality=92)


def kit(caso, nombre, estilo, rasgo):
    out = C(caso, 'anuncio')
    os.makedirs(out, exist_ok=True)
    p = lambda n: os.path.join(out, f'{estilo}-{n}.jpg')
    antes_despues(C(caso, 'foto-principal.jpg'), C(caso, f'retrato-{estilo}.jpg'), p('1-antes-despues'),
                  f'Caso real · {nombre} · estilo {estilo.capitalize()}')
    fotos_a_retrato(caso, nombre, estilo, p('2-sus-fotos'))
    detalle(caso, nombre, estilo, rasgo, p('3-detalle'))
    marcos(caso, nombre, estilo, p('4-marcos'))
    print(out)


if __name__ == '__main__':
    kit(*sys.argv[1:5])
