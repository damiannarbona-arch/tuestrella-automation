"""Encaja un retrato real en el marco gris (#BDBDBD) de una IMAGEN (la imagen inicial de una escena de IA),
con su perspectiva y su luz, para animarla después con movimiento mínimo (cinemagraph).

Uso: python3 generador/marco_en_imagen.py IMAGEN RETRATO SALIDA
"""
import sys, os
import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'video'))
from componer_marco import mascara_gris, esquinas, afinar, retrato_con_papel  # noqa: E402
from scipy import ndimage  # noqa: E402


def encajar(imagen, retrato, salida):
    a = np.asarray(Image.open(imagen).convert('RGB')).copy()
    H, W = a.shape[:2]
    m = mascara_gris(a)
    q = afinar(m, esquinas(m, None))
    q = q.mean(0) + (q - q.mean(0)) * 1.012
    ret = Image.open(retrato).convert('RGB')
    ret = ret.resize((1400, int(1400 * ret.height / ret.width)), Image.LANCZOS)
    src = retrato_con_papel(ret, ret.getpixel((10, ret.height - 10)))
    sh, sw = src.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]]), np.float32(q))
    warp = cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_LANCZOS4).astype(np.float32)
    g = cv2.GaussianBlur(a.mean(2).astype(np.float32), (0, 0), 25)
    warp *= np.clip(g / 189, .5, 1.12)[..., None]
    zona = np.zeros((H, W), np.uint8)
    cv2.fillConvexPoly(zona, np.int32(np.round(q)), 1)
    zona &= ndimage.binary_dilation(m, iterations=6).astype(np.uint8)
    al = cv2.GaussianBlur(zona.astype(np.float32), (0, 0), 1)[..., None]
    out = (a * (1 - al) + np.clip(warp, 0, 255) * al).astype(np.uint8)
    Image.fromarray(out).save(salida, quality=95)
    np.save(os.path.splitext(salida)[0] + '-esquinas.npy', q)   # para volver a poner el retrato tras animar
    print(salida)


if __name__ == '__main__':
    encajar(*sys.argv[1:4])
