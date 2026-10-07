"""Reel «Del refugio a su sitio» con Rufo (ejemplo IA): clip de Dola/Seedance con el retrato ya compuesto
(marco_en_video.py) + textos de la historia + cierre con el retrato y el eslogan. ~12,5 s, 1080×1920, sin audio.

Uso: python3 generador/video/reel_rufo.py assets/ia/rufo-video/compuesto.mp4
"""
import os, sys
import imageio_ffmpeg
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from tiktok_revelacion import render, S  # noqa: E402
from videos import texto  # noqa: E402

ARR, ABA = 250, 1560
TXT = [  # (desde, hasta, líneas, y)
    (0.2, 2.0, [('Llevaba 2 años', 'b'), ('esperando a alguien', 'b')], ARR),
    (2.1, 4.0, [('Un día, alguien', 'b'), ('volvió a por él', 'b')], ARR),
    (4.1, 6.0, [('Ahora la playa es suya', 'b')], ARR),
    (6.1, 7.6, [('Y la calle. Y el sofá.', 'b'), ('Y nosotros.', 'b')], ARR),
    (7.8, 10.0, [('Ahora tiene su sitio', 'b')], ABA),
]
FIN = [('Un cuadro personalizado,', 'b'), ('no un cuadro cualquiera', 'b')]
NOTA = [('Historia recreada con IA · Adopta', 'i')]


def leer(ruta):
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24')
    meta = next(gen)
    w, h = meta['size']
    return [Image.frombytes('RGB', (w, h), f) for f in gen], meta.get('fps') or 24


def montar(clip):
    frames, fps = leer(clip)
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
        im = ultimo
        im = texto(im, FIN, ABA - 80, min(1, tl / .2), tam=78)
        return texto(im, NOTA, ABA + 140, min(1, tl / .3), tam=46)

    render('reel-rufo-adopcion-es.mp4', [(dur, historia, []), (2.6, cierre, [])])


if __name__ == '__main__':
    montar(sys.argv[1])
