"""Publicaciones de Instagram/Facebook (carrusel 4:5, 1080×1350) con la guía visual de Kivoa.

Guía: redes/guia-visual.md. Mismas fuentes y colores que kivoa.es (tema Horizon).

Uso:
  python3 generador/redes/publicaciones.py            # publicación #1 en EN (Instagram) y ES (Facebook)
Salida: assets/redes/publicaciones/01-antes-despues/{en,es}/01.jpg …
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = lambda *p: os.path.join(RAIZ, 'assets', *p)
FU = lambda n: os.path.join(RAIZ, 'generador', 'fuentes', n)

# ---- Paleta (60 % papel · 30 % foto · 10 % salvia; rosa solo como acento puntual) ----
PAPEL = (246, 242, 236)   # #F6F2EC  fondo de la web
ARENA = (220, 213, 202)   # #DCD5CA  líneas, fondos secundarios
TINTA = (44, 51, 47)      # #2C332F  texto
SALVIA = (63, 81, 71)     # #3F5147  marca: botones, números, checks
GRIS = (80, 86, 85)       # #505655  texto secundario
ROSA = (216, 167, 160)    # #D8A7A0  acento (la rosa de los retratos): 1 detalle por pieza como máximo

# ---- Tipografía (la de kivoa.es) ----
TIT = lambda s: ImageFont.truetype(FU('Trirong-Light.ttf'), s)          # titulares
TIT_I = lambda s: ImageFont.truetype(FU('Trirong-LightItalic.ttf'), s)  # acento en titulares
MARCA = lambda s: ImageFont.truetype(FU('Trirong-Regular.ttf'), s)      # logotipo
TXT = lambda s: ImageFont.truetype(FU('QuattrocentoSans-Regular.ttf'), s)
TXT_B = lambda s: ImageFont.truetype(FU('QuattrocentoSans-Bold.ttf'), s)

W, H = 1080, 1350
M = 64                      # margen = "paspartú": toda foto va enmarcada en papel
FOTO = (M, 372, W - M, 1238)  # zona de imagen común a todas las diapositivas


def abrir(p):
    return ImageOps.exif_transpose(Image.open(p)).convert('RGB')


def recorte(img, w, h, cx=.5, cy=.5, zoom=1.0):
    s = max(w / img.width, h / img.height) * zoom
    cw, ch = w / s, h / s
    x = min(max(cx * img.width - cw / 2, 0), img.width - cw)
    y = min(max(cy * img.height - ch / 2, 0), img.height - ch)
    return img.resize((w, h), Image.LANCZOS, box=(x, y, x + cw, y + ch))


def sombra(base, caja, radio=26, off=(0, 14), alfa=70, r=0):
    capa = Image.new('RGBA', base.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = caja
    ImageDraw.Draw(capa).rounded_rectangle((x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1]), r, fill=(40, 30, 20, alfa))
    capa = capa.filter(ImageFilter.GaussianBlur(radio))
    base.alpha_composite(capa)


def lienzo():
    return Image.new('RGBA', (W, H), PAPEL + (255,))


def pie(im, n, total):
    """Pie común: logotipo a la izquierda, contador a la derecha."""
    d = ImageDraw.Draw(im)
    d.text((M, H - 58), 'Kivoa', font=MARCA(40), fill=SALVIA, anchor='ls')
    d.text((W - M, H - 62), f'{n:02d} / {total:02d}', font=TXT(26), fill=GRIS, anchor='rs')


def cabecera(im, etiqueta, titular, acento=None):
    """Etiqueta (versalitas salvia) + titular Trirong. 'acento' = parte del titular en cursiva."""
    d = ImageDraw.Draw(im)
    y = 118
    if etiqueta:
        d.text((M, y), etiqueta.upper(), font=TXT_B(26), fill=SALVIA, anchor='ls')
        y += 30
    lineas = titular.split('\n')
    for i, l in enumerate(lineas):
        f = TIT_I(70) if acento is not None and i == acento else TIT(70)
        y += 84
        d.text((M - 3, y), l, font=f, fill=TINTA, anchor='ls')


def foto_en_zona(im, foto, cx=.5, cy=.5, zoom=1.0):
    x0, y0, x1, y1 = FOTO
    sombra(im, FOTO, radio=22, off=(0, 12), alfa=55)
    im.paste(recorte(foto, x1 - x0, y1 - y0, cx, cy, zoom), (x0, y0))


def polaroid(im, foto, centro, ancho, angulo, texto=None):
    borde, pie_p = 22, 78 if texto else 22
    w = ancho - 2 * borde
    h = int(w * 1.18)
    p = Image.new('RGBA', (ancho, h + borde + pie_p), (255, 255, 255, 255))
    p.paste(recorte(foto, w, h, .6, .55), (borde, borde))
    if texto:
        ImageDraw.Draw(p).text((ancho / 2, h + borde + pie_p / 2 + 2), texto, font=TIT_I(40), fill=TINTA, anchor='mm')
    p = p.rotate(angulo, resample=Image.BICUBIC, expand=True)
    x, y = int(centro[0] - p.width / 2), int(centro[1] - p.height / 2)
    s = Image.new('RGBA', im.size, (0, 0, 0, 0))
    s.paste(Image.new('RGBA', p.size, (40, 30, 20, 90)), (x + 6, y + 16), p)
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
    im.alpha_composite(p, (x, y))


def check(d, cx, cy, r=24):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SALVIA)
    d.line([(cx - r * .42, cy + r * .02), (cx - r * .1, cy + r * .34), (cx + r * .45, cy - r * .3)], fill='white', width=5, joint='curve')


def boton(d, cx, cy, texto):
    f = TXT_B(34)
    w = d.textlength(texto, font=f) + 110
    d.rounded_rectangle((cx - w / 2, cy - 44, cx + w / 2, cy + 44), 44, fill=SALVIA)
    d.text((cx, cy + 2), texto, font=f, fill='white', anchor='mm')


# ---------- Publicación #1 · Antes / después ----------

T1 = {
    'en': {
        'p': ('', 'From a phone photo…\n…to a portrait forever', 1),
        'antes': 'before',
        's2': ('01 · The photo', 'One photo from\nyour phone', None),
        's3': ('02 · The digital proof', 'Designed for her,\nready in 48 hours', 1),
        's4': ('03 · On their wall', 'Framed and\nready to hang', 1),
        'cta_t': 'Your pet\ncould be next',
        'cta': ['Digital proof in 48 hours', '2 rounds of changes included', 'Nothing prints without your OK'],
        'boton': 'Order yours · link in bio',
    },
    'es': {
        'p': ('', 'De una foto del móvil…\n…a un recuerdo para siempre', 1),
        'antes': 'antes',
        's2': ('01 · La foto', 'Una foto\nde tu móvil', None),
        's3': ('02 · La vista previa', 'Diseñado para ella,\nlisto en 48 horas', 1),
        's4': ('03 · En su pared', 'Enmarcado y\nlisto para colgar', 1),
        'cta_t': 'El siguiente\npuede ser el tuyo',
        'cta': ['Vista previa en 48 horas', '2 rondas de cambios incluidas', 'Nada se imprime sin tu OK'],
        'boton': 'Pide el tuyo · enlace en la bio',
    },
}


def publicacion_1():
    foto, ret, salon = abrir(A('antes-foto-luna.jpg')), abrir(A('despues-retrato-luna-v2.webp')), abrir(A('banner-salon-luna.webp'))
    total = 5
    for lang, T in T1.items():
        out = A('redes', 'publicaciones', '01-antes-despues', lang)
        os.makedirs(out, exist_ok=True)
        diapos = []

        # 1 · Portada: el resultado en la pared + la foto original en polaroid (gancho = contraste)
        im = lienzo()
        cabecera(im, *T['p'])
        foto_en_zona(im, salon, cx=.47, cy=.42, zoom=1.55)
        polaroid(im, foto, (250, 1010), 300, 7, T['antes'])
        diapos.append(im)

        # 2 · La foto original
        im = lienzo()
        cabecera(im, *T['s2'])
        foto_en_zona(im, foto, cy=.6)
        diapos.append(im)

        # 3 · El retrato sobre papel (como la vista previa que recibe el cliente)
        im = lienzo()
        cabecera(im, *T['s3'])
        x0, y0, x1, y1 = FOTO
        ImageDraw.Draw(im).rectangle(FOTO, fill=ARENA)
        h = y1 - y0 - 90
        w = int(ret.width * h / ret.height)
        cx = (x0 + x1) // 2
        caja = (cx - w // 2, y0 + 45, cx + w // 2, y0 + 45 + h)
        sombra(im, caja, radio=18, off=(0, 10), alfa=80)
        im.paste(ret.resize((w, h), Image.LANCZOS), caja[:2])
        diapos.append(im)

        # 4 · En la pared
        im = lienzo()
        cabecera(im, *T['s4'])
        foto_en_zona(im, salon, cx=.5, cy=.45, zoom=1.0)
        diapos.append(im)

        # 5 · Llamada a la acción
        im = lienzo()
        d = ImageDraw.Draw(im)
        y = 230
        for l in T['cta_t'].split('\n'):
            d.text((W / 2, y), l, font=TIT(92), fill=TINTA, anchor='ms')
            y += 108
        d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
        y += 70
        for b in T['cta']:
            check(d, 250, y - 12)
            d.text((296, y), b, font=TXT(42), fill=TINTA, anchor='ls')
            y += 88
        polaroid(im, ret, (W / 2, 935), 240, -4)
        d = ImageDraw.Draw(im)
        boton(d, W / 2, 1170, T['boton'])
        diapos.append(im)

        for i, im in enumerate(diapos, 1):
            pie(im, i, total)
            im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
        print(out)


if __name__ == '__main__':
    publicacion_1()
