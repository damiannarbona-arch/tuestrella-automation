"""Cambia los textos de un retrato ya terminado (p. ej. a inglés) sin regenerarlo con IA:
borra el texto original rellenando el papel (inpainting) y escribe el nuevo con una letra manuscrita similar.

Uso:
  python3 generador/traducir_textos.py miau lavanda en
  → assets/casos/<caso>/retrato-<estilo>-<idioma>.jpg

Cada caso define las cajas de texto (en píxeles del retrato terminado, 3×) y los textos nuevos.
"""
import os, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)
FUENTE = os.path.join(RAIZ, 'generador', 'fuentes', 'Satisfy-Regular.ttf')
TINTA = (30, 28, 28)

# caja = zona a borrar (x0, y0, x1, y1); pos = centro del texto nuevo; tam = cuerpo; ang = inclinación
TEXTOS = {
    ('miau', 'lavanda'): {
        'rasgos': {'cajas': [(x - 250, 3725, x + 250, 3865) for x in (350, 820, 1300, 1760, 2214, 2690)],
                   'y': 3800, 'tam': 96, 'ang': 0},
        'frase': {'cajas': [(1010, 3970, 2100, 4135), (1010, 4100, 1240, 4165), (1240, 4120, 1920, 4288)],
                  'lineas': [((1560, 4068), -5.5), ((1572, 4197), -4.7)], 'tam': 116},
    },
}
TRAD = {
    'en': {'rasgos': ['Loyal', 'Loving', 'Playful', 'Curious', 'Cheerful', 'Special'],
           'frase': ['Just say the word,', "and I'm all yours"]},
}


def borrar(img, cajas):
    a = np.asarray(img).copy()
    lum = a.mean(2)
    mask = np.zeros(lum.shape, np.uint8)
    for x0, y0, x1, y1 in cajas:
        mask[y0:y1, x0:x1] = (lum[y0:y1, x0:x1] < 150) * 255
    mask = cv2.dilate(mask, np.ones((11, 11), np.uint8))
    return Image.fromarray(cv2.inpaint(a, mask, 15, cv2.INPAINT_TELEA))


def escribir(img, texto, centro, tam, ang=0):
    f = ImageFont.truetype(FUENTE, tam)
    capa = Image.new('L', (int(tam * len(texto) * .8) + 200, tam * 3), 0)
    ImageDraw.Draw(capa).text((capa.width / 2, capa.height / 2), texto, font=f, fill=255, anchor='mm')
    capa = capa.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))  # trazo algo más grueso, como el original
    capa = capa.rotate(-ang, resample=Image.BICUBIC, expand=True)
    x, y = int(centro[0] - capa.width / 2), int(centro[1] - capa.height / 2)
    img.paste(Image.new('RGB', capa.size, TINTA), (x, y), capa)


def traducir(caso, estilo, idioma):
    cfg, tr = TEXTOS[(caso, estilo)], TRAD[idioma]
    img = Image.open(C(caso, f'retrato-{estilo}.jpg')).convert('RGB')
    r, fr = cfg['rasgos'], cfg['frase']
    img = borrar(img, r['cajas'] + fr['cajas'])
    for (x0, _, x1, _), t in zip(r['cajas'], tr['rasgos']):
        escribir(img, t, ((x0 + x1) / 2, r['y']), r['tam'], r['ang'])
    for (c, ang), t in zip(fr['lineas'], tr['frase']):
        escribir(img, t, c, fr['tam'], ang)
    salida = C(caso, f'retrato-{estilo}-{idioma}.jpg')
    img.save(salida, quality=95)
    print(salida)


if __name__ == '__main__':
    traducir(*sys.argv[1:4])
