"""Reel «Del refugio a su sitio» con Rufo (ejemplo IA): clip de Dola/Seedance con el retrato ya compuesto
(marco_en_video.py) + textos de la historia + cierre con el retrato y el eslogan. ~12,5 s, 1080×1920, sin audio.

Uso: python3 generador/video/reel_rufo.py assets/ia/rufo-video/compuesto.mp4
"""
import os, sys
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from tiktok_revelacion import render, S  # noqa: E402
from videos import texto, kenburns  # noqa: E402

ARR, ABA = 250, 1560
TXT = [  # (desde, hasta, líneas, y)
    (0.2, 2.0, [('Llevaba 2 años', 'b'), ('esperando a alguien', 'b')], ARR),
    (2.1, 4.0, [('Un día, alguien', 'b'), ('volvió a por él', 'b')], ARR),
    (4.1, 6.0, [('Ahora la playa es suya', 'b')], ARR),
    (6.1, 7.6, [('Y la calle. Y el sofá.', 'b'), ('Y nosotros.', 'b')], ARR),
    (7.8, 10.0, [('Ahora tiene su sitio', 'b')], ABA),
]
LUZ = (7.3, 8.1)   # el plano del marco sale con la lámpara cálida: de aquí en adelante se aclara y neutraliza
FIN = [('Un cuadro personalizado,', 'b'), ('no un cuadro cualquiera', 'b')]


def leer(ruta):
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24')
    meta = next(gen)
    w, h = meta['size']
    return [Image.frombytes('RGB', (w, h), f) for f in gen], meta.get('fps') or 24


def aclarar(frames, fps):
    """Quita la viñeta y el naranja de la lámpara: aplana la luz (desenfoque grande de la luminancia) y lleva
    los claros (percentil 92) a un crema luminoso. Ganancias suavizadas en el tiempo (sin parpadeo) y entrada
    progresiva entre LUZ[0] y LUZ[1]."""
    i0, i1 = int(LUZ[0] * fps), int(LUZ[1] * fps)
    planos, refs = {}, {}
    for k in range(i0, len(frames)):
        a = np.asarray(frames[k]).astype(np.float32)
        base = cv2.GaussianBlur(a.mean(2), (0, 0), a.shape[1] * .2)
        planos[k] = np.clip((np.percentile(base, 70) / np.maximum(base, 1)) ** .35, .8, 1.5)
        refs[k] = np.percentile((a * planos[k][..., None]).reshape(-1, 3), 92, axis=0)
    ks = sorted(refs)
    R = np.array([refs[k] for k in ks])
    R = np.array([R[max(0, j - 6):j + 7].mean(0) for j in range(len(R))])
    for j, k in enumerate(ks):
        a = np.asarray(frames[k]).astype(np.float32)
        b = a * planos[k][..., None] * (np.array([238, 230, 218]) / R[j])
        t = min(1, (k - i0) / max(1, i1 - i0))
        t = t * t * (3 - 2 * t)
        frames[k] = Image.fromarray(np.clip(a + (b - a) * t, 0, 255).astype(np.uint8))
    return frames


def montar(clip):
    frames, fps = leer(clip)
    frames = aclarar(frames, fps)
    w, h = frames[0].size
    z = 1.09                                   # recorte: fuera la marca de agua de la esquina inferior derecha
    cw, ch = w / z, h / z
    caja = (w * .47 - cw / 2, h * .47 - ch / 2, w * .47 + cw / 2, h * .47 + ch / 2)
    dur = len(frames) / fps
    marco = lambda i: frames[min(i, len(frames) - 1)].resize(S, Image.LANCZOS, box=caja)

    def historia(tl, x):
        im = marco(int(tl * fps))
        for a, b, lineas, y in TXT:
            if a <= tl <= b:
                im = texto(im, lineas, y, min(1, (tl - a) / .12), tam=84)
        return im

    ultimo = marco(len(frames) - 1)

    def cierre(tl, x):
        im = kenburns(ultimo, S, x, 1.0, 1.035, (.5, .45), (.5, .45))   # acercamiento lento al retrato
        return texto(im, FIN, ABA, min(1, tl / .2), tam=78)

    render('reel-rufo-adopcion-es.mp4', [(dur, historia, []), (2.6, cierre, [])])


if __name__ == '__main__':
    montar(sys.argv[1])
