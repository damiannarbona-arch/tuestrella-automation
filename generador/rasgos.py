"""Iconos, rasgos y frase del retrato en ES y EN, sin depender de ChatGPT.

ChatGPT falla mucho con los iconos (no casan con la palabra) y cada idioma exige otra generación.
Aquí se borran los iconos y textos de la fila de rasgos (o se rellenan los círculos vacíos) y se
dibujan iconos de línea (Tabler, MIT) con su palabra, y la frase, en los dos idiomas.
De 1 imagen de ChatGPT salen 2 retratos idénticos: retrato-<estilo>-en.jpg y -es.jpg.

Uso:
  python3 generador/rasgos.py RETRATO SALIDA_BASE GENERO RASGO1,…,RASGO6 "FRASE EN" "FRASE ES" [--frase x0,y0,x1,y1]
  p. ej. … retrato-rosa.jpg assets/casos/lula/retrato-rosa f loyal,loving,foodie,playful,curious,special \
         "Tiny paws, the biggest heart" "Pequeña, pero con un corazón enorme"
- RETRATO: el retrato ya con las polaroids puestas (generador/polaroids.py).
- GENERO: m / f (para el español: Juguetón / Juguetona).
- --frase: caja de la frase en fracciones del retrato si hay que borrar una frase existente
  (si ChatGPT dejó el hueco vacío, se omite y se escribe centrada bajo los rasgos).
Rasgos disponibles: ver RASGOS.
"""
import argparse, io, os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ICONOS = os.path.join(RAIZ, 'generador', 'iconos')
LETRA = os.path.join(RAIZ, 'generador', 'fuentes', 'Satisfy-Regular.ttf')
TINTA = (34, 32, 32)

# clave: (icono Tabler, inglés, español masc., español fem.)
RASGOS = {
    'loyal': ('paw', 'Loyal', 'Leal', 'Leal'),
    'loving': ('heart', 'Loving', 'Cariñoso', 'Cariñosa'),
    'cuddly': ('hearts', 'Cuddly', 'Mimoso', 'Mimosa'),
    'playful': ('ball-tennis', 'Playful', 'Juguetón', 'Juguetona'),
    'funny': ('mood-smile', 'Funny', 'Gracioso', 'Graciosa'),
    'foodie': ('bowl', 'Foodie', 'Comilón', 'Comilona'),
    'curious': ('search', 'Curious', 'Curioso', 'Curiosa'),
    'brave': ('shield', 'Brave', 'Valiente', 'Valiente'),
    'sassy': ('crown', 'Sassy', 'Pícaro', 'Pícara'),
    'sleepy': ('moon', 'Sleepy', 'Dormilón', 'Dormilona'),
    'cheerful': ('sun', 'Cheerful', 'Alegre', 'Alegre'),
    'adventurous': ('compass', 'Adventurous', 'Aventurero', 'Aventurera'),
    'calm': ('leaf', 'Calm', 'Tranquilo', 'Tranquila'),
    'clever': ('bulb', 'Clever', 'Listo', 'Lista'),
    'protective': ('home', 'Protective', 'Protector', 'Protectora'),
    'energetic': ('bolt', 'Energetic', 'Enérgico', 'Enérgica'),
    'gentle': ('feather', 'Gentle', 'Dulce', 'Dulce'),
    'special': ('star', 'Special', 'Especial', 'Especial'),
    'unique': ('sparkles', 'Unique', 'Único', 'Única'),
    'greedy': ('cookie', 'Treat lover', 'Goloso', 'Golosa'),
    'charming': ('sparkles', 'Charming', 'Coqueto', 'Coqueta'),
    'faithful': ('paw', 'Faithful', 'Fiel', 'Fiel'),
}


def circulos(img):
    """Los 6 círculos de acuarela de la fila de rasgos: (cx, cy, r) de izquierda a derecha."""
    a = np.asarray(img).astype(int)
    H, W = a.shape[:2]
    y0, y1 = int(H * .62), int(H * .88)
    claros = a.reshape(-1, 3)[::97]
    papel = np.median(claros[claros.mean(1) > 225], 0)  # color del papel: la mayoría de píxeles claros
    m = np.abs(a[y0:y1] - papel).sum(2) > 18
    m = ndimage.binary_closing(m, iterations=max(2, W // 400))
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    cand = []
    for i, s in enumerate(ndimage.find_objects(lab), 1):
        h, w = s[0].stop - s[0].start, s[1].stop - s[1].start
        if W * .06 < w < W * .16 and .75 < h / w < 1.6:  # >1: la palabra de debajo se ha pegado al círculo
            lado = min(w, h)
            cand.append(((s[1].start + s[1].stop) / 2, y0 + s[0].start + lado / 2, lado / 2))
    # la fila: 6 candidatos con la misma altura
    cand.sort(key=lambda c: c[1])
    mejor = []
    for c in cand:
        fila = [d for d in cand if abs(d[1] - c[1]) < W * .03]
        if len(fila) > len(mejor):
            mejor = fila
    mejor = sorted(mejor, key=lambda c: c[0])
    if len(mejor) != 6:
        raise SystemExit(f'Encontrados {len(mejor)} círculos en la fila de rasgos (se esperaban 6)')
    return mejor


def borrar_oscuro(a, cajas, umbral=120):
    lum = a.mean(2)
    mask = np.zeros(lum.shape, np.uint8)
    for x0, y0, x1, y1 in cajas:
        x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
        mask[y0:y1, x0:x1] = (lum[y0:y1, x0:x1] < umbral) * 255
    k = max(3, a.shape[1] // 400) | 1
    mask = cv2.dilate(mask, np.ones((k, k), np.uint8), iterations=2)
    return cv2.inpaint(a, mask, 9, cv2.INPAINT_TELEA)


def icono(nombre, lado, grosor=1.7):
    import cairosvg
    svg = open(os.path.join(ICONOS, nombre + '.svg')).read()
    svg = svg.replace('currentColor', '#%02x%02x%02x' % TINTA).replace('stroke-width="2"', f'stroke-width="{grosor}"')
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=lado, output_height=lado)
    return Image.open(io.BytesIO(png)).convert('RGBA')


def encajar(textos, tam, ancho_max):
    """Mismo cuerpo para todos los textos: el mayor que deja caber al más largo."""
    d = ImageDraw.Draw(Image.new('L', (1, 1)))
    while tam > 10 and max(d.textlength(t, font=ImageFont.truetype(LETRA, tam)) for t in textos) > ancho_max:
        tam -= 2
    return tam


def texto(im, t, centro, tam):
    f = ImageFont.truetype(LETRA, tam)
    capa = Image.new('L', im.size, 0)
    ImageDraw.Draw(capa).text(centro, t, font=f, fill=255, anchor='mm')
    capa = capa.filter(ImageFilter.MaxFilter(3 if im.width > 2000 else 1)) if im.width > 2000 else capa
    im.paste(Image.new('RGB', im.size, TINTA), (0, 0), capa)


def componer(ruta, salida, genero, claves, frase_en, frase_es, caja_frase=None, extra=(), subrayar=False):
    img = Image.open(ruta).convert('RGB')
    W, H = img.size
    cs = circulos(img)
    r = np.median([c[2] for c in cs])
    paso = np.median(np.diff([c[0] for c in cs]))
    y_pal = np.median([c[1] for c in cs]) + r * 1.55          # línea de las palabras
    cajas = [(cx - r * .8, cy - r * .8, cx + r * .8, cy + r * .8) for cx, cy, _ in cs]
    cajas += [(cx - paso * .5, cy + r * .9, cx + paso * .5, y_pal + r * .75) for cx, cy, _ in cs]
    if caja_frase:
        fx0, fy0, fx1, fy1 = caja_frase
        cajas.append((fx0 * W, fy0 * H, fx1 * W, fy1 * H))
    cajas += [(x0 * W, y0 * H, x1 * W, y1 * H) for x0, y0, x1, y1 in extra]
    base = Image.fromarray(borrar_oscuro(np.asarray(img).copy(), cajas))

    for lang, frase in (('en', frase_en), ('es', frase_es)):
        im = base.copy()
        palabras = [RASGOS[k][1] if lang == 'en' else RASGOS[k][3 if genero == 'f' else 2] for k in claves]
        tam_p = encajar(palabras, int(r * .62), paso * .86)
        for (cx, cy, _), k, palabra in zip(cs, claves, palabras):
            lado = int(r * 1.0)
            ic_img = icono(RASGOS[k][0], lado)
            im.paste(ic_img, (int(cx - lado / 2), int(cy - lado / 2)), ic_img)
            texto(im, palabra, (cx, y_pal), tam_p)
        if caja_frase:
            fx0, fy0, fx1, fy1 = caja_frase
            cx, cy, ancho = (fx0 + fx1) / 2 * W, (fy0 + fy1) / 2 * H, (fx1 - fx0) * W * .86
        else:
            cx, cy, ancho = W / 2, y_pal + r * 1.9, W * .6
        lineas = frase.split('|')
        tam = encajar(lineas, int(r * .95), ancho)
        for i, l in enumerate(lineas):
            dy = (i - (len(lineas) - 1) / 2) * tam * 1.15
            texto(im, l, (cx, cy + dy), tam)
        if subrayar:  # trazo curvo bajo la frase, como el de la plantilla
            y = cy + (len(lineas) / 2) * tam * 1.15 + tam * .45
            d, n = ImageDraw.Draw(im), 60
            pts = [(cx - W * .1 + W * .2 * i / n, y + tam * .12 * (1 - (2 * i / n - 1) ** 2) * -1) for i in range(n + 1)]
            d.line(pts, fill=TINTA, width=max(3, int(W * .0045)), joint='curve')
        im.save(f'{salida}-{lang}.jpg', quality=95)
        print(f'{salida}-{lang}.jpg')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('retrato'); p.add_argument('salida'); p.add_argument('genero', choices='mf')
    p.add_argument('rasgos'); p.add_argument('frase_en'); p.add_argument('frase_es')
    p.add_argument('--frase', help='x0,y0,x1,y1 en fracciones: caja de la frase existente a borrar (y donde se escribe la nueva); '
                                   'más cajas a borrar separadas por ";"')
    p.add_argument('--subrayar', action='store_true', help='dibuja el trazo curvo bajo la frase')
    a = p.parse_args()
    claves = a.rasgos.split(',')
    assert len(claves) == 6 and all(k in RASGOS for k in claves), f'6 rasgos de: {", ".join(RASGOS)}'
    cajas = [tuple(map(float, c.split(','))) for c in a.frase.split(';')] if a.frase else [None]
    componer(a.retrato, a.salida, a.genero, claves, a.frase_en, a.frase_es, cajas[0], cajas[1:], a.subrayar)
