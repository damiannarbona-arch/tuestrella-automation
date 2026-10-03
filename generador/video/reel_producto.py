"""Reel/TikTok "producto real" (1080×1920, ~12 s) con el vídeo de llegada y las fotos del marco en casa.

Gancho de la duda que más frena la compra ("¿se ve igual que en la pantalla?") → el marco llegando (vídeo real)
→ la trasera con soporte y colgador → detalle de cerca → en casa → llamada.

Uso: python3 generador/video/reel_producto.py [CASO] [idiomas]      p. ej. … penny es,en
Necesita assets/casos/<caso>/producto-real/: video-llegada.mp4, foto-2.jpg, web-principal.jpg.
Sin audio: la música se pone en la app.
"""
import os, sys
import imageio_ffmpeg
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
from tiktok_revelacion import render, S, ARR  # noqa: E402
from videos import kenburns, FPS  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
R = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, 'producto-real', *p)

TXT = {
    'es': {'a': [('¿Se ve igual que', 'b'), ('en la pantalla?', 'b')],
           'b': [('Así llega:', 'b'), ('foto real, sin filtros', 'i')],
           'c': [('Con soporte y colgador', 'b')],
           'd': [('Cada detalle,', 'b'), ('tal cual lo apruebas', 'i')],
           'e': [('Y así queda en casa', 'b')],
           'f': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
    'en': {'a': [('Does it look the same', 'b'), ('as on screen?', 'b')],
           'b': [('This is how it arrives:', 'b'), ('real footage, no filters', 'i')],
           'c': [('With a stand and a hanger', 'b')],
           'd': [('Every detail,', 'b'), ('just as you approved it', 'i')],
           'e': [('And this is it at home', 'b')],
           'f': [('Want one of your pet?', 'b'), ('Link in bio', 'i')]},
}


def tramo(ruta, desde, dur):
    """Fotogramas de un tramo del vídeo, a FPS y a 1080×1920 (solo ese tramo: el vídeo entero no cabe en memoria)."""
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24', input_params=['-ss', str(desde)],
                                     output_params=['-t', str(dur), '-vf', f'fps={FPS}'])
    w, h = next(gen)['size']
    frames = [ImageOps.fit(Image.frombytes('RGB', (w, h), f), S, Image.LANCZOS) for f in gen]
    return lambda tl: frames[min(int(tl * FPS), len(frames) - 1)]


def montar(caso='penny', idiomas='es,en'):
    video = R(caso, 'video-llegada.mp4')
    llega, cerca, detras = tramo(video, 0, 2.6), tramo(video, 2.6, 2.0), tramo(video, 10.8, 1.6)
    abrir = lambda f: ImageOps.exif_transpose(Image.open(R(caso, f))).convert('RGB')
    mano, casa = abrir('foto-2.jpg'), abrir('web-principal.jpg')
    for lang in idiomas.split(','):
        T = TXT[lang]
        rot = lambda k, a=.0, b=1.0: [(T[k], ARR, a, b)]
        render(f'reel-producto-{caso}-{lang}.mp4', [
            (2.6, lambda tl, x: llega(tl), rot('a')),
            (2.0, lambda tl, x: cerca(tl), rot('b')),
            (1.6, lambda tl, x: detras(tl), rot('c')),
            (2.2, lambda tl, x: kenburns(mano, S, x, 1.0, 1.35, (.5, .5), (.52, .4)), rot('d')),
            (3.6, lambda tl, x: kenburns(casa, S, x, 1.18, 1.0, (.42, .62), (.45, .55)), rot('e', 0, .55) + rot('f', .55)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:3])
