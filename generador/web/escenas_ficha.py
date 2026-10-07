"""Fotos 1, 2 y 3 del carrusel: el diseño real dentro del hueco gris de las 3 escenas de ChatGPT.

Escenas en assets/ia/ficha/: escena-a-frente, escena-d-tres-marcos, escena-b-apoyado, escena-c-detalle (huecos grises 2:3).
Por cada escena: máscara del gris → esquinas subpíxel → perspectiva → luz del gris aplicada al retrato →
corrección de color común (pared hacia el #F6F2EC de la web) → 2000×2000.

Uso: python3 generador/web/escenas_ficha.py [estilo ...]
→ assets/web/ficha/<estilo>-1-frente.jpg, -2-tres-marcos.jpg, -3-detalle.jpg
"""
import os, sys
import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'video'))
sys.path.insert(0, os.path.dirname(__file__))
from componer_marco import esquinas, afinar  # noqa: E402
from ficha_producto import ARTICULOS, A  # noqa: E402

ESCENAS = [('a-frente', '1-frente'), ('d-tres-marcos', '2-tres-marcos'), ('c-detalle', '3-detalle')]
PARED_WEB = np.array([246, 242, 236], np.float32)   # #F6F2EC
LADO = 2000


def huecos(a):
    """Todos los huecos grises de la escena (la de los 3 marcos tiene 3), de mayor a menor."""
    v = a.mean(2)
    g = (np.abs(a[..., 0] - a[..., 1]) < 11) & (np.abs(a[..., 1] - a[..., 2]) < 13) & (v > 120) & (v < 215)
    lab, n = ndimage.label(g)
    tam = ndimage.sum(g, lab, range(1, n + 1))
    res = []
    for i in np.argsort(-tam):
        if tam[i] < g.size * .01:
            break
        m = ndimage.binary_fill_holes(ndimage.binary_closing(lab == i + 1, np.ones((9, 9)), iterations=2))
        res.append(m)
    return res


def encajar(escena, retrato):
    a = np.asarray(Image.open(escena).convert('RGB')).astype(np.float32)
    todos = np.zeros(a.shape[:2], bool)
    for m in huecos(a):
        a = encajar_hueco(a, m, retrato)
        todos |= m
    return a, todos


def encajar_hueco(a, m, retrato):
    H, W = a.shape[:2]
    q = afinar(m, esquinas(m, None))
    q = q.mean(0) + (q - q.mean(0)) * 1.006             # cubre el borde antialias del gris
    ret = Image.open(retrato).convert('RGB')
    # recorte del diseño a la proporción exacta del hueco (alto/ancho medidos en la escena)
    prop = (np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / (np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3]))
    w = ret.width
    h = min(ret.height, int(w * prop))
    w = int(h / prop)
    ret = ret.crop(((ret.width - w) // 2, (ret.height - h) // 2, (ret.width + w) // 2, (ret.height + h) // 2))
    ret = ret.resize((1600, int(1600 * prop)), Image.LANCZOS)
    src = np.asarray(ret).astype(np.float32)
    sh, sw = src.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]]), np.float32(q))
    warp = cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
    # luz: el gris de la escena dividido por su mediana = sombras y degradados de la foto, aplicados al retrato
    gris = a.mean(2)
    med = np.median(gris[m])
    luz = cv2.GaussianBlur(np.where(m, gris, med).astype(np.float32), (0, 0), 6) / med
    warp *= np.clip(luz, .55, 1.15)[..., None]
    warp = cv2.GaussianBlur(warp, (0, 0), .45)          # misma nitidez que la foto
    # borde del hueco suavizado con supermuestreo (en estas escenas nada tapa el cuadro)
    zona = np.zeros((H * 4, W * 4), np.uint8)
    cv2.fillConvexPoly(zona, np.int32(np.round(q * 4)), 255, lineType=cv2.LINE_AA)
    al = cv2.resize(zona, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255
    dentro = al[..., 0] > .5
    # papel del impreso con el mismo brillo que el paspartú que lo rodea, no más
    anillo = ndimage.binary_dilation(dentro, iterations=14) & ~ndimage.binary_dilation(dentro, iterations=4)
    pasp = np.median(a[anillo], 0)
    papel = np.percentile(warp[dentro], 92, axis=0)
    warp *= float(np.clip(pasp.mean() * 1.01 / papel.mean(), .75, 1.05))   # solo brillo: se mantiene el tono crema
    # tras el cristal: un poco menos de contraste
    media = warp[dentro].mean(0)
    warp = media + (warp - media) * .95
    # sombra del paspartú sobre el impreso (luz desde la izquierda y arriba)
    desp = ndimage.shift(dentro.astype(np.float32), (5, 5), order=1)
    somb = cv2.GaussianBlur(np.clip(dentro - desp, 0, 1).astype(np.float32), (0, 0), 3)
    warp *= (1 - .22 * somb)[..., None]
    # grano de la foto
    warp += np.random.default_rng(1).normal(0, 1.6, warp.shape).astype(np.float32)
    return a * (1 - al) + np.clip(warp, 0, 255) * al


def color_web(a, m):
    """Lleva la pared (zona clara fuera del cuadro) a medio camino del crema de la web: todas las escenas iguales."""
    v = a.mean(2)
    pared = (v > np.percentile(v[~m], 80)) & ~ndimage.binary_dilation(m, iterations=40)
    actual = a[pared].mean(0)
    k = 1 + .6 * (PARED_WEB / actual - 1)
    return np.clip(a * k, 0, 255)


def rotular_marcos(im, escena):
    """Escena de los 3 marcos: título en la pared y la medida bajo cada marco, con la tipografía de la web."""
    from PIL import ImageDraw
    from ficha_producto import F, SERIF, ITAL, TINTA, GRIS, SALVIA
    a = np.asarray(Image.open(escena).convert('RGB')).astype(np.float32)
    k = LADO / a.shape[1]
    d = ImageDraw.Draw(im)
    d.text((LADO / 2, 150), '3 marcos · 3 tamaños', font=F(SERIF, 100), fill=TINTA, anchor='mm')
    d.text((LADO / 2, 250), 'Cualquier marco en cualquier tamaño', font=F(ITAL, 54), fill=GRIS, anchor='mm')
    # de izquierda a derecha: el marco pequeño, el mediano y el grande
    centros = sorted(ndimage.center_of_mass(m)[1] * k for m in huecos(a))
    fondo = max(np.nonzero(m)[0].max() for m in huecos(a)) * k
    for x, txt in zip(centros, ('20×25 cm', '30×40 cm', '50×70 cm')):
        f = F(SERIF, 46)
        w = d.textlength(txt, font=f) + 56
        y = fondo + 175
        d.rounded_rectangle((x - w / 2, y - 36, x + w / 2, y + 36), radius=36, fill=SALVIA)
        d.text((x, y), txt, font=f, fill=(255, 255, 255), anchor='mm')
    return im


if __name__ == '__main__':
    out = A('web', 'ficha')
    os.makedirs(out, exist_ok=True)
    for e in (sys.argv[1:] or ARTICULOS):
        retrato = ARTICULOS[e][1]
        for esc, nombre in ESCENAS:
            img, m = encajar(A('ia', 'ficha', f'escena-{esc}.webp'), retrato)
            img = color_web(img, m)
            im = Image.fromarray(img.astype(np.uint8)).resize((LADO, LADO), Image.LANCZOS)
            if esc == 'd-tres-marcos':
                im = rotular_marcos(im, A('ia', 'ficha', f'escena-{esc}.webp'))
            im.save(os.path.join(out, f'{e}-{nombre}.jpg'), quality=92)
        print(e, 'ok')
