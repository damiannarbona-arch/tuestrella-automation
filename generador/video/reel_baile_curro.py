"""Curro en la pista de baile (Seedance/Dola) → flash → su cuadro real en la pared (~9 s, 1080×1920, sin audio).

El clip de IA casi no se mueve: le damos ritmo con golpes de zoom cada medio tiempo y lo aceleramos.
El recorte quita la marca de agua de Dola (esquina inferior derecha). El cuadro nunca pasa por la IA.

Uso: python3 generador/video/reel_baile_curro.py CLIP.mp4
"""
import os, sys
import imageio_ffmpeg
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from tiktok_revelacion import render, S  # noqa: E402
from videos import kenburns, ease  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BPM = 120          # ritmo de los golpes de zoom (se cuadra con un sonido de ~120 bpm en TikTok)
VEL = 1.35         # aceleración del clip

TXT = {
    'es': {'gancho': [('Curro cuando se entera', 'b'), ('de que tiene su propio cuadro', 'b')],
           'final': [('Posando desde que nació', 'b')],
           'cta': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
    'en': {'gancho': [('Curro when he finds out', 'b'), ('he has his own portrait', 'b')],
           'final': [('Posing since day one', 'b')],
           'cta': [('Want one of yours?', 'b'), ('Link in bio', 'i')]},
}


def leer(ruta):
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24')
    meta = next(gen)
    w, h = meta['size']
    return [Image.frombytes('RGB', (w, h), f) for f in gen], meta.get('fps') or 24


def montar(clip, idiomas='es,en,sin-texto'):
    frames, fps = leer(clip)
    w, h = frames[0].size
    beat = 60 / BPM

    def baile(tl, x):
        f = frames[min(int((0.6 + tl * VEL) * fps), len(frames) - 1)]
        fase = (tl % beat) / beat
        z = 1.2 + .09 * (1 - ease(min(fase / .35, 1)))       # golpe al inicio de cada tiempo y vuelta
        cw, ch = w / z, h / z
        cx, cy = w * .47, h * .44                               # algo arriba/izquierda: fuera la marca de agua
        caja = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        return f.resize(S, Image.LANCZOS, box=caja)

    blanco = Image.new('RGB', S, (255, 255, 255))
    pared = Image.open(os.path.join(RAIZ, 'assets', 'web', 'ficha', 'clasico-1-frente.jpg')).convert('RGB')

    def flash(tl, x):
        return Image.blend(blanco, kenburns(pared, S, 0, 1.0, 1.0, (.445, .45), (.445, .45)), ease(x))

    for lang in idiomas.split(','):
        T = TXT.get(lang)
        rot = (lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]) if T else (lambda *a, **k: [])
        render(f'tiktok-curro-baile-{lang}.mp4', [
            (4.6, baile, rot('gancho', 250, 0, 1)),
            (.25, flash, []),
            (2.3, lambda tl, x: kenburns(pared, S, x, 1.0, 1.06, (.445, .45), (.445, .43)), rot('final', 1640, .15, 1)),
            (1.8, lambda tl, x: kenburns(pared, S, x, 1.06, 1.08, (.445, .43), (.445, .43)), rot('cta', 1640, 0, 1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:3])
