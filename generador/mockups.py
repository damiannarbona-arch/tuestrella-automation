"""Coloca el retrato REAL (sin IA) dentro de una escena (caja de regalo, pared…), en perspectiva.

Uso:
  python3 generador/mockups.py RETRATO SALIDA_PREFIJO
  → <prefijo>-caja.jpg, <prefijo>-salon.jpg

Cada escena define las 4 esquinas de la lámina (TL, TR, BR, BL, en píxeles de la escena original)
y, si hace falta, qué píxeles de delante hay que respetar (p. ej. hojas que tapan el cuadro).
Para añadir escenas: pedir a ChatGPT la escena con la lámina en blanco o con cualquier retrato,
medir las esquinas y añadirla a ESCENAS.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageOps

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
A = lambda *p: os.path.join(RAIZ, 'assets', *p)
S = 2  # se trabaja al doble para que el retrato quede nítido

ESCENAS = {
    'caja': {'archivo': A('mockups', 'caja-regalo-lavanda.jpg'),
             'quad': [(423, 142), (810, 140), (813, 706), (335, 660)], 'delante': None},
    'salon': {'archivo': A('banner-salon-luna.webp'),
              'quad': [(602, 116), (966, 110), (966, 621), (602, 619)],
              'delante': ('verde', (930, 560, 1000, 640))},  # hojas de la planta, solo en la esquina inferior derecha
}


def perspectiva(dst, src):
    A_, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A_ += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        b += [u, v]
    return np.linalg.solve(np.array(A_, float), np.array(b, float))


def encajar(ret, aspecto):
    """Retrato entero (sin recortar) ampliado con su propio papel hasta la proporción de la lámina."""
    papel = tuple(int(v) for v in np.median(np.asarray(ret)[:12].reshape(-1, 3), axis=0))
    if ret.width / ret.height < aspecto:
        lienzo = Image.new('RGB', (round(ret.height * aspecto), ret.height), papel)
    else:
        lienzo = Image.new('RGB', (ret.width, round(ret.width / aspecto)), papel)
    lienzo.paste(ret, ((lienzo.width - ret.width) // 2, (lienzo.height - ret.height) // 2))
    return lienzo


def colocar(escena, retrato):
    e = ESCENAS[escena]
    base = Image.open(e['archivo']).convert('RGB')
    grande = base.resize((base.width * S, base.height * S), Image.LANCZOS)
    q = np.array(e['quad'], float)
    c = q.mean(0)
    q = c + (q - c) * (1 + 1.5 / np.linalg.norm(q - c, axis=1, keepdims=True))  # tapar el borde de la lámina anterior
    Q = q * S
    w = (np.linalg.norm(Q[1] - Q[0]) + np.linalg.norm(Q[2] - Q[3])) / 2
    h = (np.linalg.norm(Q[3] - Q[0]) + np.linalg.norm(Q[2] - Q[1])) / 2
    ret = encajar(Image.open(retrato).convert('RGB'), w / h)
    m = .01 * ret.width
    src = [(m, m), (ret.width - m, m), (ret.width - m, ret.height - m), (m, ret.height - m)]
    capa = ret.transform(grande.size, Image.PERSPECTIVE, perspectiva(Q, src), Image.BICUBIC)
    mascara = Image.new('L', (grande.width * 4, grande.height * 4), 0)
    ImageDraw.Draw(mascara).polygon([tuple(p * 4) for p in Q], fill=255)
    mascara = mascara.resize(grande.size, Image.LANCZOS)
    if e['delante']:  # hojas por delante del cuadro: no se tapan (solo dentro de su zona)
        _, (x0, y0, x1, y1) = e['delante']
        a = np.asarray(grande).astype(int)
        hoja = (a[..., 1] > a[..., 0] + 12) & (a[..., 1] > a[..., 2] + 12)
        zona = np.zeros(hoja.shape, bool)
        zona[y0 * S:y1 * S, x0 * S:x1 * S] = True
        mascara = Image.fromarray(np.where(hoja & zona, 0, np.asarray(mascara)).astype(np.uint8))
    grande.paste(capa, (0, 0), mascara)
    return grande


if __name__ == '__main__':
    retrato, prefijo = sys.argv[1:3]
    for n in ESCENAS:
        im = colocar(n, retrato)
        im.save(f'{prefijo}-{n}.jpg', quality=93)
        print(f'{prefijo}-{n}.jpg', im.size)
