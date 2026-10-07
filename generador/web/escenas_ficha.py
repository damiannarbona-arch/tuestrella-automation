"""Fotos 1, 2 y 4 del carrusel: el diseño real dentro del hueco gris de las 3 escenas de ChatGPT.

Escenas en assets/ia/ficha/: escena-a-frente, escena-b-apoyado, escena-c-detalle (hueco gris 2:3).
Por cada escena: máscara del gris → esquinas subpíxel → perspectiva → luz del gris aplicada al retrato →
corrección de color común (pared hacia el #F6F2EC de la web) → 2000×2000.

Uso: python3 generador/web/escenas_ficha.py [estilo ...]
→ assets/web/ficha/<estilo>-1-frente.jpg, -2-apoyado.jpg, -4-detalle.jpg
"""
import os, sys
import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'video'))
sys.path.insert(0, os.path.dirname(__file__))
from componer_marco import mascara_gris, esquinas, afinar  # noqa: E402
from ficha_producto import ARTICULOS, A  # noqa: E402

ESCENAS = [('a-frente', '1-frente'), ('b-apoyado', '2-apoyado'), ('c-detalle', '4-detalle')]
PARED_WEB = np.array([246, 242, 236], np.float32)   # #F6F2EC
LADO = 2000


def encajar(escena, retrato):
    a = np.asarray(Image.open(escena).convert('RGB')).astype(np.float32)
    H, W = a.shape[:2]
    m = mascara_gris(a.astype(np.uint8))
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
    return a * (1 - al) + np.clip(warp, 0, 255) * al, m


def color_web(a, m):
    """Lleva la pared (zona clara fuera del cuadro) a medio camino del crema de la web: todas las escenas iguales."""
    v = a.mean(2)
    pared = (v > np.percentile(v[~m], 80)) & ~ndimage.binary_dilation(m, iterations=40)
    actual = a[pared].mean(0)
    k = 1 + .6 * (PARED_WEB / actual - 1)
    return np.clip(a * k, 0, 255)


if __name__ == '__main__':
    out = A('web', 'ficha')
    os.makedirs(out, exist_ok=True)
    for e in (sys.argv[1:] or ARTICULOS):
        retrato = ARTICULOS[e][1]
        for esc, nombre in ESCENAS:
            img, m = encajar(A('ia', 'ficha', f'escena-{esc}.webp'), retrato)
            img = color_web(img, m)
            Image.fromarray(img.astype(np.uint8)).resize((LADO, LADO), Image.LANCZOS).save(
                os.path.join(out, f'{e}-{nombre}.jpg'), quality=92)
        print(e, 'ok')
