"""Publicaciones de Instagram/Facebook (carrusel 4:5, 1080×1350) con la guía visual de Kivoa.

Guía: redes/guia-visual.md. Mismas fuentes y colores que kivoa.es (tema Horizon).

Uso:
  python3 generador/redes/publicaciones.py 1|2        # publicación #1 o #2, en EN (Instagram) y ES (Facebook)
Salida: assets/redes/publicaciones/01-antes-despues/{en,es}/01.jpg …
"""
import os, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

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
    cw, ch = min(w / s, img.width), min(h / s, img.height)  # el redondeo no puede salirse de la foto
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


def polaroid(im, foto, centro, ancho, angulo, texto=None, foco=(.6, .55)):
    borde, pie_p = 22, 78 if texto else 22
    w = ancho - 2 * borde
    h = int(w * 1.18)
    p = Image.new('RGBA', (ancho, h + borde + pie_p), (255, 255, 255, 255))
    p.paste(recorte(foto, w, h, *foco), (borde, borde))
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




# ---------- Publicación #2 · Caso real Bizcocho (4 fotos del móvil → 1 retrato) ----------

T2 = {
    'en': {
        'serie': 'Real case · 02',
        'p': ('They sent us\n4 phone photos…', 'Swipe to see what we made  »'),
        's2': ('No studio.\nNo photographer.', 1),
        's3': ('Every feature,\njust as he is', 1), 'foto': 'His photo', 'retrato': 'His portrait',
        's4': ('The digital proof,\nin 48 hours', 1),
        's5': ('Framed and\nready to hang', 1),
        's6': ('Ready to gift,\nstraight to the door', 1),
        'cta_t': 'What about\nyours?',
        'cta': ['1 main photo + up to 3 more', 'Digital proof in 48 hours', 'Nothing prints without your OK'],
        'boton': 'Create yours · link in bio',
    },
    'es': {
        'serie': 'Caso real · 02',
        'p': ('Nos enviaron\n4 fotos del móvil…', 'Desliza y mira qué hicimos  »'),
        's2': ('Sin estudio.\nSin fotógrafo.', 1),
        's3': ('Cada rasgo,\ntal cual es', 1), 'foto': 'Su foto', 'retrato': 'Su retrato',
        's4': ('La vista previa,\nen 48 horas', 1),
        's5': ('Enmarcado y\nlisto para colgar', 1),
        's6': ('Listo para regalar,\nen la puerta de casa', 1),
        'cta_t': '¿Y el de\ntu mascota?',
        'cta': ['1 foto principal + hasta 3 más', 'Vista previa en 48 horas', 'Nada se imprime sin tu OK'],
        'boton': 'Crea el tuyo · enlace en la bio',
    },
}


def publicacion_2():
    C = lambda *p: A('casos', 'bizcocho', *p)
    fotos = [abrir(C('foto-principal.jpg'))] + [abrir(C(f'extra-{i}.jpg')) for i in (1, 2, 3)]
    total = 7
    for lang, T in T2.items():
        ret = abrir(C(f'retrato-clasico-{lang}.jpg'))
        pared, caja = abrir(C(f'mockup-pared-{lang}.jpg')), abrir(C(f'mockup-clasico-{lang}-caja.jpg'))
        out = A('redes', 'publicaciones', '02-caso-bizcocho', lang)
        os.makedirs(out, exist_ok=True)
        diapos = []

        # 1 · Portada con intriga: las 4 fotos sobre el cuadro desenfocado
        im = lienzo()
        cabecera(im, T['serie'], T['p'][0], None)
        x0, y0, x1, y1 = FOTO
        sombra(im, FOTO, radio=22, off=(0, 12), alfa=55)
        fondo = recorte(pared, x1 - x0, y1 - y0, .43, .42, 1.9).filter(ImageFilter.GaussianBlur(26))
        im.paste(fondo, (x0, y0))
        for foto, c, ang, foco in zip(fotos, [(330, 590), (760, 615), (340, 960), (750, 975)], [-6, 5, 4, -5],
                                      [(.36, .45), (.45, .4), (.45, .4), (.5, .45)]):
            polaroid(im, foto, c, 330, ang, foco=foco)
        d = ImageDraw.Draw(im)  # etiqueta "desliza" sobre la foto, abajo a la derecha
        f = TXT_B(30)
        tw = d.textlength(T['p'][1], font=f)
        d.rounded_rectangle((W / 2 - tw / 2 - 30, y1 - 96, W / 2 + tw / 2 + 30, y1 - 30), 33, fill=SALVIA)
        d.text((W / 2, y1 - 62), T['p'][1], font=f, fill='white', anchor='mm')
        diapos.append(im)

        # 2 · Las 4 fotos originales en cuadrícula
        im = lienzo()
        cabecera(im, T['serie'], *T['s2'])
        g = 16
        cw, ch = (x1 - x0 - g) // 2, (y1 - y0 - g) // 2
        sombra(im, FOTO, radio=22, off=(0, 12), alfa=45)
        for i, (foto, (cx, cy)) in enumerate(zip(fotos, [(.36, .4), (.45, .35), (.45, .3), (.5, .4)])):
            im.paste(recorte(foto, cw, ch, cx, cy, 1.1), (x0 + (i % 2) * (cw + g), y0 + (i // 2) * (ch + g)))
        diapos.append(im)

        # 3 · Detalle: su foto ↔ su retrato
        im = lienzo()
        cabecera(im, T['serie'], *T['s3'])
        lado, alto = (x1 - x0 - 24) // 2, y1 - y0 - 96
        yy = y0
        for i, (img, (cx, cy, z), et) in enumerate([(fotos[0], (.355, .36, 2.0), T['foto']),
                                                   (ret, (.575, .32, 1.8), T['retrato'])]):
            xx = x0 + i * (lado + 24)
            sombra(im, (xx, yy, xx + lado, yy + alto), radio=18, off=(0, 10), alfa=60)
            im.paste(recorte(img, lado, alto, cx, cy, z), (xx, yy))
            ImageDraw.Draw(im).text((xx + lado / 2, yy + alto + 66), et, font=TIT_I(44), fill=TINTA, anchor='ms')
        diapos.append(im)

        # 4 · El retrato sobre papel (vista previa)
        im = lienzo()
        cabecera(im, T['serie'], *T['s4'])
        ImageDraw.Draw(im).rectangle(FOTO, fill=ARENA)
        h = y1 - y0 - 90
        w = int(ret.width * h / ret.height)
        cx = (x0 + x1) // 2
        caja_r = (cx - w // 2, y0 + 45, cx + w // 2, y0 + 45 + h)
        sombra(im, caja_r, radio=18, off=(0, 10), alfa=80)
        im.paste(ret.resize((w, h), Image.LANCZOS), caja_r[:2])
        diapos.append(im)

        # 5 · En la pared (marcos reales)
        im = lienzo()
        cabecera(im, T['serie'], *T['s5'])
        foto_en_zona(im, pared, cx=.52, cy=.5, zoom=1.35)
        diapos.append(im)

        # 6 · En su caja de regalo
        im = lienzo()
        cabecera(im, T['serie'], *T['s6'])
        foto_en_zona(im, caja, cx=.55, cy=.5, zoom=1.0)
        diapos.append(im)

        # 7 · Llamada a la acción
        im = lienzo()
        d = ImageDraw.Draw(im)
        d.text((W / 2, 118), T['serie'].upper(), font=TXT_B(26), fill=SALVIA, anchor='ms')
        y = 250
        for l in T['cta_t'].split('\n'):
            d.text((W / 2, y), l, font=TIT(92), fill=TINTA, anchor='ms')
            y += 108
        d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
        y += 70
        for b in T['cta']:
            check(d, 230, y - 12)
            d.text((276, y), b, font=TXT(42), fill=TINTA, anchor='ls')
            y += 88
        polaroid(im, ret, (W / 2, 950), 230, -4)
        d = ImageDraw.Draw(im)
        boton(d, W / 2, 1180, T['boton'])
        diapos.append(im)

        for i, im in enumerate(diapos, 1):
            pie(im, i, total)
            im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
        print(out)



# ---------- Publicación #3 · Informativa: 5 claves para la foto perfecta ----------

ROJO = (178, 74, 62)

T3 = {
    'en': {
        'serie': 'Photo guide',
        'p': ('The portrait starts\nwith your photo', 1), 'p_sub': '5 keys to the perfect one  »',
        'k': [('01 · Light', 'Natural light,\nnear a window', 1, 'Daylight', 'Too dark'),
              ('02 · Angle', 'At their\neye level', 1, 'Eye level', 'From above'),
              ('03 · Sharpness', 'The original,\nnot a screenshot', 1, 'Original photo', 'Screenshot / zoom'),
              ('04 · Distance', 'Fill the frame\nwith their face', 1, 'Close up', 'Too far')],
        'k5': ('05 · Personality', 'Up to 3 extra photos\nwith their story', 1),
        'k5_txt': 'The beach, their favourite spot, that look… they go in the polaroids.',
        'cta_t': 'Not sure\nabout yours?',
        'cta': ['Send it: we check it for free', 'Digital proof in 48 hours', 'Nothing prints without your OK'],
        'boton': 'Save this guide · link in bio',
    },
    'es': {
        'serie': 'Guía de fotos',
        'p': ('El retrato empieza\npor tu foto', 1), 'p_sub': '5 claves para la foto perfecta  »',
        'k': [('01 · Luz', 'Luz natural,\ncerca de una ventana', 1, 'Luz de día', 'Demasiado oscura'),
              ('02 · Ángulo', 'A la altura\nde sus ojos', 1, 'A su altura', 'Desde arriba'),
              ('03 · Nitidez', 'La original,\nno una captura', 1, 'Foto original', 'Captura o zoom'),
              ('04 · Distancia', 'Que su cara\nllene la foto', 1, 'De cerca', 'Demasiado lejos')],
        'k5': ('05 · Personalidad', 'Hasta 3 fotos más\ncon su historia', 1),
        'k5_txt': 'La playa, su rincón favorito, esa mirada… van en las polaroids.',
        'cta_t': '¿Dudas con\nla tuya?',
        'cta': ['Mándala: la revisamos gratis', 'Vista previa en 48 horas', 'Nada se imprime sin tu OK'],
        'boton': 'Guarda esta guía · enlace en la bio',
    },
}


def insignia(d, cx, cy, ok, r=30):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SALVIA if ok else ROJO, outline='white', width=4)
    if ok:
        d.line([(cx - r * .42, cy + r * .02), (cx - r * .1, cy + r * .34), (cx + r * .45, cy - r * .3)], fill='white', width=6, joint='curve')
    else:
        k = r * .36
        d.line((cx - k, cy - k, cx + k, cy + k), fill='white', width=6)
        d.line((cx - k, cy + k, cx + k, cy - k), fill='white', width=6)


def pareja(im, bien, mal, et_bien, et_mal):
    """Dos fotos en la zona de imagen: ✔ a la izquierda, ✘ a la derecha, con su rótulo."""
    x0, y0, x1, y1 = FOTO
    w, h = (x1 - x0 - 24) // 2, y1 - y0 - 96
    for i, (img, et, ok) in enumerate([(bien, et_bien, True), (mal, et_mal, False)]):
        xx = x0 + i * (w + 24)
        sombra(im, (xx, y0, xx + w, y0 + h), radio=18, off=(0, 10), alfa=60)
        im.paste(img.resize((w, h), Image.LANCZOS) if img.size != (w, h) else img, (xx, y0))
        d = ImageDraw.Draw(im)
        insignia(d, xx + 50, y0 + 50, ok)
        d.text((xx + w / 2, y0 + h + 66), et, font=TIT_I(44), fill=TINTA if ok else ROJO, anchor='ms')


def publicacion_3():
    C = lambda caso, f: abrir(A('casos', caso, f))
    x0, y0, x1, y1 = FOTO
    w, h = (x1 - x0 - 24) // 2, y1 - y0 - 96
    R = lambda img, cx, cy, z=1.0: recorte(img, w, h, cx, cy, z)
    # un solo perro en toda la guía (Sonic)
    son = lambda f: C('sonic', f)
    ppal, playa, cascada, bano, captura = son('foto-principal.jpg'), son('extra-1.jpg'), son('extra-2.jpg'), son('extra-3.jpg'), son('captura.jpg')
    oscura = ImageEnhance.Contrast(ImageEnhance.Brightness(R(ppal, .5, .4, 1.1)).enhance(.3)).enhance(.8)
    pix = R(bano, .62, .45, 1.3)
    pix = pix.resize((w // 12, h // 12), Image.BILINEAR).resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(1.5))
    pares = [(R(ppal, .5, .4, 1.1), oscura), (R(playa, .55, .62, 1.7), R(captura, .5, .55, 1.0)),
             (R(bano, .62, .45, 1.3), pix), (R(ppal, .5, .33, 1.45), R(cascada, .5, .5, 1.0))]
    total = 7
    for lang, T in T3.items():
        out = A('redes', 'publicaciones', '03-guia-fotos', lang)
        os.makedirs(out, exist_ok=True)
        diapos = []
        # 1 · Portada: su foto, grande
        im = lienzo()
        cabecera(im, T['serie'], *T['p'])
        foto_en_zona(im, ppal, cx=.5, cy=.4, zoom=1.15)
        d = ImageDraw.Draw(im)
        f = TXT_B(30)
        tw = d.textlength(T['p_sub'], font=f)
        d.rounded_rectangle((W / 2 - tw / 2 - 30, y1 - 96, W / 2 + tw / 2 + 30, y1 - 30), 33, fill=SALVIA)
        d.text((W / 2, y1 - 62), T['p_sub'], font=f, fill='white', anchor='mm')
        diapos.append(im)
        # 2–5 · Claves con ✔ / ✘
        for (et, tit, ac, eb, em), (b, m) in zip(T['k'], pares):
            im = lienzo()
            cabecera(im, et, tit, ac)
            pareja(im, b, m, eb, em)
            diapos.append(im)
        # 6 · Personalidad: 3 polaroids
        im = lienzo()
        cabecera(im, *T['k5'])
        extras = [playa, cascada, bano]
        for foto, c, a, foco in zip(extras, [(300, 650), (770, 610), (540, 930)], [-6, 5, -3],
                                    [(.52, .6), (.78, .72), (.62, .45)]):
            polaroid(im, foto, c, 350, a, foco=foco)
        d = ImageDraw.Draw(im)
        d.text((W / 2, 1232), T['k5_txt'], font=TIT_I(32), fill=GRIS, anchor='ms')
        diapos.append(im)
        # 7 · Llamada a la acción
        im = lienzo()
        d = ImageDraw.Draw(im)
        d.text((W / 2, 118), T['serie'].upper(), font=TXT_B(26), fill=SALVIA, anchor='ms')
        y = 250
        for l in T['cta_t'].split('\n'):
            d.text((W / 2, y), l, font=TIT(92), fill=TINTA, anchor='ms')
            y += 108
        d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
        y += 70
        for b in T['cta']:
            check(d, 230, y - 12)
            d.text((276, y), b, font=TXT(42), fill=TINTA, anchor='ls')
            y += 88
        polaroid(im, ppal, (W / 2, 950), 230, -4, foco=(.5, .35))
        d = ImageDraw.Draw(im)
        boton(d, W / 2, 1180, T['boton'])
        diapos.append(im)
        for i, im in enumerate(diapos, 1):
            pie(im, i, total)
            im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
        print(out)



# ---------- Publicación #4 · Paso a paso (texto + fotos), solo EN ----------

def texto_centrado(d, lineas, y, fuente, color, sep):
    for l in lineas:
        d.text((W / 2, y), l, font=fuente, fill=color, anchor='ms')
        y += sep
    return y


def publicacion_4():
    C = lambda f: abrir(A('casos', 'sonic', f))
    ppal, playa, cascada, bano = C('foto-principal.jpg'), C('extra-1.jpg'), C('extra-2.jpg'), C('extra-3.jpg')
    ret = C('retrato-aventurero-en.jpg')
    out = A('redes', 'publicaciones', '04-paso-a-paso', 'en')
    os.makedirs(out, exist_ok=True)
    total, diapos = 6, []
    x0, y0, x1, y1 = FOTO

    # 1 · Solo texto: la pregunta gancho
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 300), 'STEP BY STEP', font=TXT_B(28), fill=SALVIA, anchor='ms')
    y = texto_centrado(d, ['Do you know', 'how to start'], 520, TIT(104), TINTA, 124)
    y = texto_centrado(d, ["your pet's portrait?"], y, TIT_I(104), TINTA, 124)
    d.line((W / 2 - 60, y + 10, W / 2 + 60, y + 10), fill=ROSA, width=4)
    f = TXT_B(32)
    tw = d.textlength('Swipe  »', font=f)
    d.rounded_rectangle((W / 2 - tw / 2 - 40, 1060, W / 2 + tw / 2 + 40, 1132), 36, fill=SALVIA)
    d.text((W / 2, 1097), 'Swipe  »', font=f, fill='white', anchor='mm')
    diapos.append(im)

    # 2 · Solo texto: elegir las fotos
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 300), '01', font=TIT(120), fill=SALVIA, anchor='ms')
    y = texto_centrado(d, ['Just pick the photos', 'you love the most'], 520, TIT(84), TINTA, 104)
    y = texto_centrado(d, ['straight from your phone'], y + 10, TIT_I(64), GRIS, 80)
    for b in ['1 main photo: their face, their look', 'Up to 3 more with their story']:
        y += 30
        check(d, 190, y + 40 - 12)
        d.text((236, y + 40), b, font=TXT(40), fill=TINTA, anchor='ls')
        y += 60
    diapos.append(im)

    # 3 · La foto principal
    im = lienzo()
    cabecera(im, '02 · The main photo', 'Looking straight\nat the camera', 1)
    foto_en_zona(im, ppal, cx=.5, cy=.42, zoom=1.1)
    diapos.append(im)

    # 4 · El resto de fotos
    im = lienzo()
    cabecera(im, '03 · A few more, if you like', 'They go in\nthe polaroids', 1)
    for foto, c, a, foco in zip([playa, cascada, bano], [(300, 650), (770, 610), (540, 960)], [-6, 5, -3],
                                [(.55, .6), (.78, .72), (.6, .5)]):
        polaroid(im, foto, c, 360, a, foco=foco)
    diapos.append(im)

    # 5 · El resultado
    im = lienzo()
    cabecera(im, '04 · The result', 'This could be\nyour pet', 1)
    ImageDraw.Draw(im).rectangle(FOTO, fill=ARENA)
    h = y1 - y0 - 70
    w = int(ret.width * h / ret.height)
    cx = (x0 + x1) // 2
    caja = (cx - w // 2, y0 + 35, cx + w // 2, y0 + 35 + h)
    sombra(im, caja, radio=18, off=(0, 10), alfa=80)
    im.paste(ret.resize((w, h), Image.LANCZOS), caja[:2])
    diapos.append(im)

    # 6 · Dónde conseguirlo
    im = lienzo()
    d = ImageDraw.Draw(im)
    y = texto_centrado(d, ['Want one', 'of your pet?'], 250, TIT(92), TINTA, 108)
    d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
    y += 60
    for b in ['Follow us for more real cases', 'Like & save this post', 'Digital proof in 48 hours']:
        check(d, 230, y - 12)
        d.text((276, y), b, font=TXT(42), fill=TINTA, anchor='ls')
        y += 88
    polaroid(im, ret, (W / 2, 960), 230, -4, foco=(.5, .4))
    d = ImageDraw.Draw(im)
    boton(d, W / 2, 1180, 'Get yours · link in bio')
    diapos.append(im)

    for i, im in enumerate(diapos, 1):
        pie(im, i, total)
        im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
    print(out)


# ---------- Publicación #5 · Avelino vs Lichi: presentación del combate (antes del reel) ----------

def ficha(im, foto, foco, esquina, color, nombre, apodo, datos, zoom=1.0):
    """Ficha de luchador: esquina, nombre + apodo, foto y 4 datos de combate."""
    d = ImageDraw.Draw(im)
    f = TXT_B(26)
    tw = d.textlength(esquina.upper(), font=f)
    d.rounded_rectangle((M, 92, M + tw + 44, 140), 24, fill=color)
    d.text((M + 22, 117), esquina.upper(), font=f, fill='white', anchor='lm')
    d.text((M - 3, 238), nombre, font=TIT(92), fill=TINTA, anchor='ls')
    d.text((M, 306), apodo, font=TIT_I(54), fill=GRIS, anchor='ls')
    caja = (M, 350, W - M, 900)
    sombra(im, caja, radio=22, off=(0, 12), alfa=55)
    im.paste(recorte(foto, caja[2] - caja[0], caja[3] - caja[1], *foco, zoom=zoom), caja[:2])
    d = ImageDraw.Draw(im)
    y = 975
    for etiqueta, valor in datos:
        d.text((M, y), etiqueta.upper(), font=TXT_B(26), fill=SALVIA, anchor='ls')
        d.text((M + 330, y), valor, font=TXT(40), fill=TINTA, anchor='ls')
        d.line((M, y + 26, W - M, y + 26), fill=ARENA, width=2)
        y += 74


def publicacion_5():
    import imageio_ffmpeg
    sys.path.insert(0, os.path.join(RAIZ, 'generador', 'video'))
    sys.path.insert(0, os.path.join(RAIZ, 'generador'))
    from reel_duelo import lienzo as pared_duelo  # noqa: E402
    from reel_trapo import trapo, con_trapo  # noqa: E402
    ave = abrir(A('casos', 'avelino', 'foto-principal.jpg'))
    lic = abrir(A('casos', 'lichi', 'foto-principal.jpg'))
    g = imageio_ffmpeg.read_frames(A('casos', 'lichi', 'video-pelea.mp4'))
    meta = next(g)
    fot = {i: Image.frombytes('RGB', meta['size'], f) for i, f in enumerate(g) if i in (36, 52, 84)}
    out = A('redes', 'publicaciones', '05-avelino-vs-lichi', 'en')
    os.makedirs(out, exist_ok=True)
    total, diapos = 6, []

    # 1 · Portada: cartel de combate
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 150), 'FIGHT NIGHT', font=TXT_B(30), fill=SALVIA, anchor='ms')
    texto_centrado(d, ['Avelino vs Lichi'], 270, TIT(96), TINTA, 0)
    texto_centrado(d, ['the fight nobody asked for'], 350, TIT_I(56), GRIS, 0)
    polaroid(im, ave, (300, 760), 430, -7, 'Avelino', foco=(.55, .3))
    polaroid(im, lic, (780, 760), 430, 7, 'Lichi', foco=(.5, .45))
    d = ImageDraw.Draw(im)
    d.ellipse((W / 2 - 72, 690, W / 2 + 72, 834), fill=ROSA)
    d.text((W / 2, 764), 'VS', font=TIT(70), fill='white', anchor='mm')
    f = TXT_B(32)
    tw = d.textlength('Meet the fighters  »', font=f)
    d.rounded_rectangle((W / 2 - tw / 2 - 40, 1130, W / 2 + tw / 2 + 40, 1202), 36, fill=SALVIA)
    d.text((W / 2, 1167), 'Meet the fighters  »', font=f, fill='white', anchor='mm')
    diapos.append(im)

    # 2 y 3 · Fichas de los luchadores
    im = lienzo()
    ficha(im, ave, (.5, .3), 'In the green corner', SALVIA, 'Avelino', 'King of the house',
          [('Rank', 'The veteran'), ('Weight class', '"Big boned"'), ('Special move', 'The 3-hour nap'),
           ('Weakness', 'The treat bag')], zoom=1.15)
    diapos.append(im)
    im = lienzo()
    ficha(im, lic, (.5, .52), 'In the pink corner', ROSA, 'Lichi', "Small, but she's the boss",
          [('Rank', 'The rookie'), ('Weight class', 'Featherweight'), ('Special move', '3 a.m. sneak attack'),
           ('Weakness', 'Anything that moves')], zoom=1.0)
    diapos.append(im)

    # 4 · Round 1 (fotograma real de la pelea)
    im = lienzo()
    cabecera(im, 'Round 1', 'The Crocs\nincident', 1)
    # fotogramas del vídeo en polaroids pequeñas: a ese tamaño no se nota que es vídeo de móvil
    for k, c, a, foco in [(36, (290, 640), -6, (.55, .62)), (52, (790, 640), 5, (.55, .55)), (84, (540, 1000), -2, (.45, .55))]:
        polaroid(im, fot[k], c, 380, a, foco=foco)
    diapos.append(im)

    # 5 · El motivo: dos cuadros tapados
    im = lienzo()
    cabecera(im, 'The reason', 'They each got a portrait…\n…and both say theirs wins', 1)
    rets = [abrir(A('casos', c, f'retrato-{e}-en.jpg')) for c, e in (('avelino', 'clasico'), ('lichi', 'lavanda'))]
    pared, marcos = pared_duelo(rets, ['Avelino', 'Lichi'])
    (a0, b0, a1, b1), (c0, d0, c1, d1) = marcos
    cajas = [(a0 - 30, b0 - 30, a1 + 12, b1 + 70), (c0 - 12, d0 - 30, c1 + 30, d1 + 70)]
    t0, t1 = trapo(cajas[0]), trapo(cajas[1])
    tapada = con_trapo(con_trapo(pared, t1[0].transpose(Image.FLIP_LEFT_RIGHT), t1[1].transpose(Image.FLIP_LEFT_RIGHT),
                                 caja=cajas[1]), *t0, caja=cajas[0])
    x0, y0, x1, y1 = FOTO
    cy = ((b0 + b1) / 2 + 300) / tapada.height
    foto_en_zona(im, tapada, cx=.5, cy=cy, zoom=1.0)
    diapos.append(im)

    # 6 · Llamada: el reel de esta noche
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 250), 'THE REVEAL', font=TXT_B(28), fill=SALVIA, anchor='ms')
    y = texto_centrado(d, ['Tonight we', 'unveil them'], 400, TIT(104), TINTA, 124)
    d.line((W / 2 - 60, y - 40, W / 2 + 60, y - 40), fill=ROSA, width=4)
    y += 50
    for b in ['Pick your side now', 'Comment: Team Avelino or Team Lichi', 'Follow so you don\'t miss the reel']:
        check(d, 160, y - 12)
        d.text((206, y), b, font=TXT(42), fill=TINTA, anchor='ls')
        y += 92
    d = ImageDraw.Draw(im)
    boton(d, W / 2, 1150, 'Team Avelino  or  Team Lichi?')
    diapos.append(im)

    for i, im in enumerate(diapos, 1):
        pie(im, i, total)
        im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
    print(out)


# ---------- Publicación #6 · Ricky, el guardián de la ventana (historia del caso) ----------

def publicacion_6():
    C = lambda f: abrir(A('casos', 'ricky', f))
    ventana, ret = C('extra-1.jpg'), C('retrato-clasico-en.jpg')
    out = A('redes', 'publicaciones', '06-ricky-ventana', 'en')
    os.makedirs(out, exist_ok=True)
    total, diapos = 6, []
    x0, y0, x1, y1 = FOTO

    # 1 · Portada: en su ventana
    im = lienzo()
    cabecera(im, 'Meet Ricky', 'The window\nwatcher', 1)
    foto_en_zona(im, ventana, cx=.48, cy=.45, zoom=1.15)
    diapos.append(im)

    # 2 · Solo texto: su costumbre
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 330), 'HIS STORY', font=TXT_B(28), fill=SALVIA, anchor='ms')
    y = texto_centrado(d, ['Every evening,', 'Ricky waits', 'at the window…'], 520, TIT(92), TINTA, 112)
    y = texto_centrado(d, ['…so his family wanted', 'a portrait that tells', 'his story'], y + 60, TIT_I(70), GRIS, 88)
    d.line((W / 2 - 60, y + 10, W / 2 + 60, y + 10), fill=ROSA, width=4)
    diapos.append(im)

    # 3 · Sus fotos
    im = lienzo()
    cabecera(im, 'The photos', 'Straight from\ntheir phone', 1)
    fotos = [ventana, C('foto-principal.jpg'), C('extra-4.jpg'), C('extra-2.jpg')]
    for foto, c, a, foco in zip(fotos, [(300, 640), (780, 620), (310, 1030), (780, 1010)], [-5, 4, 3, -4],
                                [(.48, .42), (.45, .38), (.4, .33), (.5, .45)]):
        polaroid(im, foto, c, 380, a, foco=foco)
    diapos.append(im)

    # 4 · El resultado
    im = lienzo()
    cabecera(im, 'The result', 'His story,\nin one portrait', 1)
    ImageDraw.Draw(im).rectangle(FOTO, fill=ARENA)
    h = y1 - y0 - 70
    w = int(ret.width * h / ret.height)
    cx = (x0 + x1) // 2
    caja = (cx - w // 2, y0 + 35, cx + w // 2, y0 + 35 + h)
    sombra(im, caja, radio=18, off=(0, 10), alfa=80)
    im.paste(ret.resize((w, h), Image.LANCZOS), caja[:2])
    diapos.append(im)

    # 5 · Detalle: su carácter
    im = lienzo()
    cabecera(im, 'The details', 'His personality,\nin six words', 1)
    foto_en_zona(im, ret, cx=.5, cy=.73, zoom=1.0)
    diapos.append(im)

    # 6 · Llamada
    im = lienzo()
    d = ImageDraw.Draw(im)
    y = texto_centrado(d, ['Every pet has', 'a story to tell'], 250, TIT(92), TINTA, 108)
    d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
    y += 50
    for b in ['Send us 4 photos from your phone', 'Digital proof in 48 hours', "We don't charge you until you approve it"]:
        check(d, 150, y - 12)
        d.text((196, y), b, font=TXT(40), fill=TINTA, anchor='ls')
        y += 84
    polaroid(im, ret, (W / 2, 950), 240, -4, foco=(.5, .4))
    boton(ImageDraw.Draw(im), W / 2, 1185, 'Get yours · link in bio')
    diapos.append(im)

    for i, im in enumerate(diapos, 1):
        pie(im, i, total)
        im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
    print(out)

# ---------- Publicación #7 · Producto real (Penny): así llega a casa ----------

T7 = {
    'es': {
        'p': ('Foto real · sin filtros', 'Así llega\na casa', 1),
        's2': ('Los detalles · 20 × 25 cm', 'Su cara, su nombre\ny su frase', 1),
        's3': ('Y al caer la tarde', 'Con luz cálida,\nigual de bonito', 1),
        's4': ('Listo para poner', 'Con soporte\npara la mesa', 1),
        'pol': ('delante', 'detrás'),
        'h': 'PENNY',
        'h1': ['Ahora sigue', 'cada día', 'en el salón'],
        'h2': ['entre una vela', 'y un poco de lavanda'],
        'cta_t': ['¿Y el de', 'tu mascota?'],
        'cta': ['Mándanos 4 fotos de tu móvil', 'Vista previa en 48 horas', 'No te cobramos hasta que lo apruebes'],
        'boton': 'Pide el tuyo · enlace en la bio',
    },
    'en': {
        'p': ('Real photo · no filters', 'This is how\nit arrives', 1),
        's2': ('The details · 8 × 10 in', 'Her face, her name\nand her words', 1),
        's3': ('And in the evening', 'In warm light,\njust as lovely', 1),
        's4': ('Ready to display', 'With a stand\nfor your shelf', 1),
        'pol': ('front', 'back'),
        'h': 'PENNY',
        'h1': ['Now she stays', 'every day', 'in the living room'],
        'h2': ['between a candle', 'and some lavender'],
        'cta_t': ['What about', 'your pet?'],
        'cta': ['Send us 4 photos from your phone', 'Digital proof in 48 hours', "We don't charge you until you approve it"],
        'boton': 'Get yours · link in bio',
    },
}


def publicacion_7():
    P = lambda f: abrir(A('casos', 'penny', 'producto-real', f))
    casa, noche, mano2, trasera, frente = P('web-principal.jpg'), P('lampara-83.jpg'), P('foto-2.jpg'), P('trasera.jpg'), P('estudio-80.jpg')
    for lang, T in T7.items():
        out = A('redes', 'publicaciones', '07-penny-real', lang)
        os.makedirs(out, exist_ok=True)
        total, diapos = 6, []

        # 1 · Portada: en casa, con la vela y la lavanda
        im = lienzo()
        cabecera(im, *T['p'])
        foto_en_zona(im, casa, cx=.42, cy=.6)
        diapos.append(im)

        # 2 · Detalle: cara, nombre y frase
        im = lienzo()
        cabecera(im, *T['s2'])
        foto_en_zona(im, mano2, cx=.5, cy=.56, zoom=1.2)
        diapos.append(im)

        # 3 · De tarde, con la lámpara encendida (otro ambiente, no otra foto del marco en la mano)
        im = lienzo()
        cabecera(im, *T['s3'])
        foto_en_zona(im, noche, cx=.5, cy=.62)
        diapos.append(im)

        # 4 · Delante y detrás (soporte y colgador)
        im = lienzo()
        cabecera(im, *T['s4'])
        polaroid(im, frente, (300, 760), 460, -4, T['pol'][0], foco=(.5, .55))
        polaroid(im, trasera, (780, 790), 460, 4, T['pol'][1], foco=(.5, .55))
        diapos.append(im)

        # 5 · Solo texto: dónde está ahora
        im = lienzo()
        d = ImageDraw.Draw(im)
        d.text((W / 2, 330), T['h'], font=TXT_B(28), fill=SALVIA, anchor='ms')
        y = texto_centrado(d, T['h1'], 520, TIT(92), TINTA, 112)
        y = texto_centrado(d, T['h2'], y + 60, TIT_I(70), GRIS, 88)
        d.line((W / 2 - 60, y + 10, W / 2 + 60, y + 10), fill=ROSA, width=4)
        diapos.append(im)

        # 6 · Llamada
        im = lienzo()
        d = ImageDraw.Draw(im)
        y = texto_centrado(d, T['cta_t'], 250, TIT(92), TINTA, 108)
        d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
        y += 50
        for b in T['cta']:
            check(d, 150, y - 12)
            d.text((196, y), b, font=TXT(40), fill=TINTA, anchor='ls')
            y += 84
        polaroid(im, casa, (W / 2, 950), 240, -4, foco=(.32, .6))
        boton(ImageDraw.Draw(im), W / 2, 1185, T['boton'])
        diapos.append(im)

        for i, im in enumerate(diapos, 1):
            pie(im, i, total)
            im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
        print(out)


# ---------- Publicación #8 · Curro (sencilla: nuevo caso → sus fotos → su resultado → Kivoa) ----------

def publicacion_8():
    C = lambda f: abrir(A('casos', 'curro', f))
    frente, dormido, perfil, hermano = C('foto-1-limpia.jpg'), C('foto-2-limpia.jpg'), C('foto-4-limpia.jpg'), C('foto-3-limpia.jpg')
    ret = C('retrato-clasico-es.jpg')
    out = A('redes', 'publicaciones', '08-curro', 'es')
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    total, diapos = 4, []
    x0, y0, x1, y1 = FOTO

    # 1 · Nuevo caso
    im = lienzo()
    cabecera(im, 'Nuevo caso', 'Curro se une a\nla familia Kivoa', 1)
    foto_en_zona(im, frente, cx=.53, cy=.42, zoom=1.25)
    diapos.append(im)

    # 2 · Sus fotos
    im = lienzo()
    cabecera(im, 'Sus fotos', 'Estas son las\nfotos de Curro', 1)
    for foto, c, a, foco in zip([frente, perfil, hermano, dormido], [(300, 610), (780, 590), (310, 985), (780, 965)],
                                [-5, 4, 3, -4], [(.53, .4, 1.7), (.42, .45, 1.45), (.62, .45, 1.15), (.56, .38, 1.9)]):
        polaroid(im, foto, c, 380, a, foco=foco)
    diapos.append(im)

    # 3 · Su resultado
    im = lienzo()
    cabecera(im, 'Su resultado', 'Su retrato\npersonalizado', 1)
    ImageDraw.Draw(im).rectangle(FOTO, fill=ARENA)
    h = y1 - y0 - 70
    w = int(ret.width * h / ret.height)
    cx = (x0 + x1) // 2
    caja = (cx - w // 2, y0 + 35, cx + w // 2, y0 + 35 + h)
    sombra(im, caja, radio=18, off=(0, 10), alfa=80)
    im.paste(ret.resize((w, h), Image.LANCZOS), caja[:2])
    diapos.append(im)

    # 4 · Kivoa
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 420), 'Kivoa', font=MARCA(110), fill=SALVIA, anchor='ms')
    y = texto_centrado(d, ['Un cuadro personalizado,', 'no uno cualquiera'], 560, TIT(72), TINTA, 92)
    d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
    y += 60
    for b in ['Mándanos sus fotos del móvil', 'Vista previa en 48 horas', 'No te cobramos hasta que la apruebes',
              'Enmarcado y listo para tu casa']:
        check(d, 150, y - 12)
        d.text((196, y), b, font=TXT(40), fill=TINTA, anchor='ls')
        y += 84
    boton(d, W / 2, y + 90, '¿El siguiente es el tuyo? · enlace en la bio')
    diapos.append(im)

    for i, im in enumerate(diapos, 1):
        pie(im, i, total)
        im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
    print(out)


# ---------- Publicación #9 · Ejemplo por raza (mascota creada con IA, siempre marcada) ----------

def sello_ia(im, texto='EJEMPLO CREADO CON IA'):
    d = ImageDraw.Draw(im)
    f = TXT_B(22)
    w = d.textlength(texto, font=f) + 40
    d.rounded_rectangle((W - M - w, 70, W - M, 112), 21, fill=ARENA)
    d.text((W - M - w / 2, 91), texto, font=f, fill=TINTA, anchor='mm')


def publicacion_9(raza='caniche', nombre='Canela'):
    """Ejemplo por raza: sus fotos → su retrato → en casa → Kivoa. Mascota creada con IA: el aviso va en la
    etiqueta de IA de la red social y en el texto de la publicación ("ejemplo de estilo creado con IA")."""
    E = lambda f: abrir(A('ejemplos-ia', nombre.lower(), f))
    ret, escena = E('retrato-lavanda-es.jpg'), abrir(A('ia', 'salon-oscuro', f'inicial-{nombre.lower()}.jpg'))
    fotos = [E('foto-principal.webp'), E('extra-parque.webp'), E('extra-juguete.webp'), E('extra-dormida.webp')]
    out = A('redes', 'publicaciones', f'09-ejemplo-{raza}', 'es')
    os.makedirs(out, exist_ok=True)
    total, diapos = 4, []
    x0, y0, x1, y1 = FOTO

    # 1 · Sus fotos (portada)
    im = lienzo()
    cabecera(im, f'¿Tienes un {raza}?', 'Mándanos unas fotos\nde tu móvil…', 1)
    for foto, c, a in zip(fotos, [(300, 610), (780, 590), (310, 985), (780, 965)], [-5, 4, 3, -4]):
        polaroid(im, foto, c, 380, a, foco=(.5, .4, 1.1))
    diapos.append(im)

    # 2 · Su retrato
    im = lienzo()
    cabecera(im, 'Su retrato', '…y creamos el suyo,\ncon su carácter', 1)
    ImageDraw.Draw(im).rectangle(FOTO, fill=ARENA)
    h = y1 - y0 - 70
    w = int(ret.width * h / ret.height)
    cx = (x0 + x1) // 2
    caja = (cx - w // 2, y0 + 35, cx + w // 2, y0 + 35 + h)
    sombra(im, caja, radio=18, off=(0, 10), alfa=80)
    im.paste(ret.resize((w, h), Image.LANCZOS), caja[:2])
    diapos.append(im)

    # 3 · En casa
    im = lienzo()
    cabecera(im, 'En casa', 'Enmarcado y listo\npara su rincón', 1)
    foto_en_zona(im, escena, cx=.55, cy=.62, zoom=1.15)
    diapos.append(im)

    # 4 · Kivoa
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 420), 'Kivoa', font=MARCA(110), fill=SALVIA, anchor='ms')
    y = texto_centrado(d, ['Un cuadro personalizado,', 'no uno cualquiera'], 560, TIT(72), TINTA, 92)
    d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
    y += 60
    for b in [f'Mándanos las fotos de tu {raza}', 'Vista previa en 48 horas', 'No te cobramos hasta que la apruebes',
              'Navidad: pide antes del 1/12']:
        check(d, 150, y - 12)
        d.text((196, y), b, font=TXT(40), fill=TINTA, anchor='ls')
        y += 84
    boton(d, W / 2, y + 90, 'Pide el suyo · enlace en la bio')
    diapos.append(im)

    for i, im in enumerate(diapos, 1):
        pie(im, i, total)
        im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
    print(out)


# ---------- Publicación #10 · Cómo pedir tu cuadro (paso a paso, aporta valor) ----------

def paso(im, n, etiqueta, titular, acento=1):
    """Cabecera de paso: número grande salvia + titular."""
    cabecera(im, f'Paso {n} · {etiqueta}', titular, acento)


def publicacion_10():
    F = lambda *p: A('web', 'ficha', *p)
    out = A('redes', 'publicaciones', '10-como-pedir', 'es')
    os.makedirs(out, exist_ok=True)
    total = 7
    diapos = []

    # 1 · Portada: la duda que tiene la gente
    im = lienzo()
    cabecera(im, 'Guía rápida', '¿Quieres el cuadro\nde tu mascota y no\nsabes cómo pedirlo?', 2)
    x0, y0, x1, y1 = FOTO
    zona = (x0, y0 + 70, x1, y1)
    sombra(im, zona, radio=22, off=(0, 12), alfa=55)
    im.paste(recorte(abrir(F('clasico-1-frente.jpg')), x1 - x0, y1 - y0 - 70, .5, .42, 1.15), zona[:2])
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((W / 2 - 250, y1 - 110, W / 2 + 250, y1 - 30), 40, fill=PAPEL + (235,))
    d.text((W / 2, y1 - 68), 'Te lo explico en 5 pasos  »', font=TXT_B(34), fill=SALVIA, anchor='mm')
    diapos.append(im)

    # 2 · Elige el estilo
    im = lienzo()
    paso(im, 1, 'El estilo', 'Elige el estilo\nque cuente su historia')
    estilos = [('rosa', 'Recuerdo', 'para recordar'), ('lavanda', 'Botánico', 'para regalar'),
               ('clasico', 'Clásico', 'para decorar'), ('aventurero', 'Aventurero', 'para aventureros'),
               ('caballos', 'Ecuestre', 'para caballos')]
    d = ImageDraw.Draw(im)
    posiciones = [(250, 560), (540, 560), (830, 560), (395, 930), (685, 930)]
    for (k, nom, para), (cx, cy) in zip(estilos, posiciones):
        foto = recorte(abrir(F(f'{k}-1-frente.jpg')), 250, 250, .5, .4, 1.6)
        caja = (cx - 125, cy - 150, cx + 125, cy + 100)
        sombra(im, caja, radio=14, off=(0, 8), alfa=50)
        im.paste(foto, caja[:2])
        d = ImageDraw.Draw(im)
        d.text((cx, cy + 142), nom, font=TIT(40), fill=TINTA, anchor='ms')
        d.text((cx, cy + 180), para, font=TXT(26), fill=GRIS, anchor='ms')
    diapos.append(im)

    # 3 · Tamaño y marco
    im = lienzo()
    paso(im, 2, 'Tamaño y marco', 'Elige tamaño\ny color del marco')
    foto_en_zona(im, abrir(F('lavanda-2-tres-marcos.jpg')), cy=.578, zoom=1.15)   # sin el título de la imagen
    diapos.append(im)

    # 4 · Sus fotos y sus datos
    im = lienzo()
    paso(im, 3, 'Sus fotos', 'Sube sus fotos y\ncuéntanos cómo es')
    C = lambda n: A('casos', 'sonic', n)
    polaroid(im, abrir(C('foto-principal.jpg')), (300, 640), 360, -5, 'la principal', foco=(.5, .4))
    polaroid(im, abrir(C('extra-1.jpg')), (640, 560), 250, 6, foco=(.5, .5))
    polaroid(im, abrir(C('extra-2.jpg')), (820, 760), 230, -4, foco=(.5, .5))
    d = ImageDraw.Draw(im)
    y = 1000
    for b in ['1 foto principal + hasta 3 más', 'Su nombre y una frase', 'Hasta 6 rasgos de su forma de ser']:
        check(d, 150, y - 12)
        d.text((196, y), b, font=TXT(40), fill=TINTA, anchor='ls')
        y += 76
    diapos.append(im)

    # 5 · Vista previa (Penny: la diapositiva siguiente es su cuadro real ya en casa)
    im = lienzo()
    paso(im, 4, 'La vista previa', 'En 48 h te enviamos\nsu vista previa')
    foto_en_zona(im, abrir(F('rosa-5-vista-previa.jpg')), cx=.5, cy=.578, zoom=1.15)
    diapos.append(im)

    # 6 · En casa
    im = lienzo()
    paso(im, 5, 'En casa', 'Lo apruebas y\nte llega enmarcado')
    foto_en_zona(im, abrir(A('casos', 'penny', 'producto-real', 'web-principal.jpg')), cx=.5, cy=.55, zoom=1.0)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = FOTO
    d.rounded_rectangle((x0 + 24, y1 - 86, x0 + 430, y1 - 24), 31, fill=PAPEL + (235,))
    d.text((x0 + 227, y1 - 55), 'Foto real · en casa en 5–9 días', font=TXT_B(26), fill=SALVIA, anchor='mm')
    diapos.append(im)

    # 7 · Llamada a la acción
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 330), 'Kivoa', font=MARCA(110), fill=SALVIA, anchor='ms')
    y = texto_centrado(d, ['Un cuadro personalizado,', 'no un cuadro cualquiera'], 470, TIT(68), TINTA, 88)
    d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
    y += 60
    for b in ['Vista previa en 48 horas', '2 rondas de cambios incluidas', 'No te cobramos hasta que la apruebes',
              'Navidad: pide antes del 1/12']:
        check(d, 170, y - 12)
        d.text((216, y), b, font=TXT(40), fill=TINTA, anchor='ls')
        y += 82
    d.rounded_rectangle((W / 2 - 330, y + 10, W / 2 + 330, y + 96), 18, outline=SALVIA, width=3)
    d.text((W / 2, y + 54), '-10 % en tu primer pedido: BIENVENIDA10', font=TXT_B(32), fill=SALVIA, anchor='mm')
    boton(d, W / 2, y + 200, 'kivoa.es · enlace en la bio')
    diapos.append(im)

    for i, im in enumerate(diapos, 1):
        pie(im, i, total)
        im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
    print(out)


# ---------- Publicación #11 · «¿Sabéis quién se ha puesto celosa?» (caso real Noah, compañera de Curro) ----------

def publicacion_11():
    N = lambda f: abrir(A('casos', 'noah', f))
    cocina, perfil, cachorra, durmiendo, playa = (N('sentada-cocina.jpg'), N('calle-perfil.jpg'), N('cachorra.jpg'),
                                                  N('con-curro-durmiendo.jpg'), N('con-curro-playa.jpg'))
    ret_n = N('retrato-botanico-es.jpg')
    ret_c = abrir(A('casos', 'curro', 'retrato-clasico-es.jpg'))
    pared_c = abrir(A('web', 'ficha', 'clasico-1-frente.jpg'))
    out = A('redes', 'publicaciones', '11-noah-celosa', 'es')
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    total, diapos = 7, []
    x0, y0, x1, y1 = FOTO

    def retrato_en_zona(im, rets):
        ImageDraw.Draw(im).rectangle(FOTO, fill=ARENA)
        h = y1 - y0 - 70 if len(rets) == 1 else int((x1 - x0 - 90) / 2 * 1.5)
        ws = [int(r.width * h / r.height) for r in rets]
        g = 30
        x = (x0 + x1 - sum(ws) - g * (len(rets) - 1)) // 2
        y = (y0 + y1 - h) // 2
        for r, w in zip(rets, ws):
            sombra(im, (x, y, x + w, y + h), radio=18, off=(0, 10), alfa=80)
            im.paste(r.resize((w, h), Image.LANCZOS), (x, y))
            x += w + g

    # 1 · Gancho
    im = lienzo()
    cabecera(im, 'Caso real', '¿Sabéis quién se\nha puesto celosa?', 1)
    foto_en_zona(im, cocina, cx=.5, cy=.36, zoom=1.15)
    diapos.append(im)

    # 2 · Curro ya tenía el suyo
    im = lienzo()
    cabecera(im, 'Hace unas semanas', 'Curro estrenó\nsu cuadro…', 1)
    foto_en_zona(im, pared_c, cx=.445, cy=.45, zoom=1.0)
    diapos.append(im)

    # 3 · Noah, ofendida
    im = lienzo()
    cabecera(im, 'Desde entonces', '…y Noah no nos\nmira igual', 1)
    foto_en_zona(im, perfil, cx=.55, cy=.45, zoom=1.35)
    diapos.append(im)

    # 4 · Sus fotos
    im = lienzo()
    cabecera(im, 'Así que', 'le pedimos\nsus fotos', 1)
    for foto, c, a, foco in zip([cachorra, cocina, durmiendo, playa], [(300, 610), (780, 590), (310, 985), (780, 965)],
                                [-5, 4, 3, -4], [(.45, .35, 1.3), (.5, .38, 1.5), (.5, .5, 1.2), (.5, .55, 1.0)]):
        polaroid(im, foto, c, 380, a, foco=foco)
    diapos.append(im)

    # 5 · Su retrato
    im = lienzo()
    cabecera(im, 'Su resultado', 'Noah, en estilo\nBotánico', 1)
    retrato_en_zona(im, [ret_n])
    diapos.append(im)

    # 6 · Los dos
    im = lienzo()
    cabecera(im, 'Paz en casa', 'Ahora sí: cada uno\ncon el suyo', 1)
    retrato_en_zona(im, [ret_c, ret_n])
    diapos.append(im)

    # 7 · Kivoa
    im = lienzo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 330), 'Kivoa', font=MARCA(110), fill=SALVIA, anchor='ms')
    y = texto_centrado(d, ['Un cuadro personalizado,', 'no un cuadro cualquiera'], 470, TIT(68), TINTA, 88)
    d.line((W / 2 - 60, y - 30, W / 2 + 60, y - 30), fill=ROSA, width=4)
    y += 60
    for b in ['¿Tienes dos? Hacemos uno para cada uno', 'Vista previa en 48 horas',
              'No te cobramos hasta que la apruebes', 'Enmarcado y listo para colgar']:
        check(d, 150, y - 12)
        d.text((196, y), b, font=TXT(38), fill=TINTA, anchor='ls')
        y += 82
    d.rounded_rectangle((W / 2 - 330, y + 10, W / 2 + 330, y + 96), 18, outline=SALVIA, width=3)
    d.text((W / 2, y + 54), '-10 % en tu primer pedido: BIENVENIDA10', font=TXT_B(32), fill=SALVIA, anchor='mm')
    boton(d, W / 2, y + 200, 'kivoa.es · enlace en la bio')
    diapos.append(im)

    for i, im in enumerate(diapos, 1):
        pie(im, i, total)
        im.convert('RGB').save(os.path.join(out, f'{i:02d}.jpg'), quality=92)
    print(out)


if __name__ == '__main__':
    import sys
    {"1": publicacion_1, "2": publicacion_2, "3": publicacion_3, "4": publicacion_4, "5": publicacion_5, "6": publicacion_6, "7": publicacion_7, "8": publicacion_8, "9": publicacion_9, "10": publicacion_10, "11": publicacion_11}[sys.argv[1] if len(sys.argv) > 1 else "2"]()
