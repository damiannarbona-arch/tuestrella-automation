"""Reel «Competición de alegría» (1080×1920, ~9 s, sin audio): Curro contra Noah celebrando su cuadro.

Gancho: los dos marcos tapados con tela («les enseñamos lo que hay debajo…») → pantalla partida, Curro arriba
(apenas se mueve: «3/10») y Noah abajo, cuyo nivel de alegría va en un rótulo con fondo que la sigue y tapa la zona
íntima (la IA de vídeo le dibujó genitales de macho) → caen las telas: los dos cuadros y pregunta para comentarios.

Uso: python3 generador/video/reel_competicion_alegria.py
Clips: assets/ia/baile/curro-dola.mp4 y assets/ia/noah-video/dola-baile.mp4 (Dola, 720×1280, 24 fps).
"""
import os, sys
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from tiktok_revelacion import render, S  # noqa: E402
from videos import ease, fuente_tiktok  # noqa: E402
from reel_duelo import lienzo  # noqa: E402
from reel_trapo import trapo, con_trapo  # noqa: E402
from reel_zoom import recorte_log  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = lambda *p: os.path.join(RAIZ, 'assets', *p)
ARR, ABA = 250, 1300

# zona a tapar en el clip de Noah: (segundo, x, y) en px del clip original, revisado cada 0,5 s
CENSURA = [(0.35, 358, 775), (0.5, 358, 792), (1.0, 350, 825), (1.5, 358, 833), (2.0, 358, 842), (2.5, 358, 858),
           (3.0, 342, 858), (3.5, 358, 858), (4.0, 342, 850), (4.5, 333, 833), (5.0, 367, 850), (5.5, 367, 850),
           (6.0, 290, 858), (6.5, 333, 883), (7.0, 333, 900), (7.5, 392, 925), (7.9, 392, 925)]
# rótulo con fondo que tapa la zona y sigue a Noah
CARTEL = {'?': [('Nivel de alegría:', 'i'), ('???', 'b')],
          'sube': [('Nivel de alegría:', 'i'), ('subiendo…', 'b')],
          'fuera': [('Nivel de alegría:', 'i'), ('FUERA DE', 'b'), ('ESCALA', 'b')]}

TXT = {
    'gancho': [('Les enseñamos lo que', 'b'), ('hay debajo de las telas…', 'b')],
    'curro': [('Nivel de alegría', 'i'), ('Curro: 3/10', 'b')],
    'final': [('¿Quién ganó?', 'b'), ('Comenta Curro o Noah', 'b')],
}


def leer(ruta):
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24')
    meta = next(gen)
    w, h = meta['size']
    return [Image.frombytes('RGB', (w, h), f) for f in gen], meta.get('fps') or 24


def zona(t):
    """Centro de la zona a tapar en el clip original, o None fuera del tramo en que se ve."""
    if not CENSURA[0][0] <= t <= CENSURA[-1][0]:
        return None
    ts = [k[0] for k in CENSURA]
    return np.interp(t, ts, [k[1] for k in CENSURA]), np.interp(t, ts, [k[2] for k in CENSURA])


def cartel(im, centro, k, lineas):
    """Rótulo con fondo blanco (estilo texto de TikTok) que tapa la zona; k = escala respecto a pantalla completa."""
    d = ImageDraw.Draw(im)
    w, h = 540 * k, 340 * k
    cx, cy = centro
    cy += 15 * k
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 34 * k, fill=(255, 255, 255))
    fs = [fuente_tiktok(int((58 if e == 'i' else 84) * k), 600 if e == 'i' else 760) for _, e in lineas]
    alto = sum(f.size * 1.18 for f in fs)
    y = cy - alto / 2
    for (t, e), f in zip(lineas, fs):
        d.text((cx, y + f.size * .59), t, font=f, fill=(20, 20, 20), anchor='mm')
        y += f.size * 1.18
    return im


def recorte(im, z, cx, cy, size, caja=False):
    w, h = im.size
    tw, th = size
    s = max(tw / w, th / h) * z
    cw, ch = tw / s, th / s
    x0 = min(max(cx * w - cw / 2, 0), w - cw)
    y0 = min(max(cy * h - ch / 2, 0), h - ch)
    out = im.resize(size, Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return (out, (x0, y0, s)) if caja else out


def montar():
    curro, fc = leer(A('ia', 'baile', 'curro-dola.mp4'))
    noah, fn = leer(A('ia', 'noah-video', 'dola-baile.mp4'))
    beat = .5

    def f_curro(t, size=S, z0=1.2):
        f = curro[min(int((0.6 + t * 1.35) * fc), len(curro) - 1)]
        fase = (t % beat) / beat
        z = z0 + .09 * (1 - ease(min(fase / .35, 1)))
        return recorte(f, z, .47, .44, size)

    VN = 1.2   # Noah algo acelerada: el baile gana ritmo

    def f_noah(t, size=S, z=1.1, cy=.47, lineas=None, ks=1.0):
        tc = min(0.2 + t * VN, (len(noah) - 1) / fn)
        im, (x0, y0, s) = recorte(noah[int(tc * fn)], z, .47, cy, size, caja=True)
        p = zona(tc)
        if p and lineas:
            im = cartel(im, ((p[0] - x0) * s, (p[1] - y0) * s), s / 1.65 * ks, lineas)
        return im

    mitad = (S[0], S[1] // 2)

    def partida(t, x):
        im = Image.new('RGB', S)
        im.paste(f_curro(t, mitad, 1.25), (0, 0))
        im.paste(f_noah(t + 1.0, mitad, 1.0, .5, CARTEL['sube' if t < 1.1 else 'fuera'], .72), (0, S[1] // 2))
        ImageDraw.Draw(im).rectangle((0, S[1] // 2 - 4, S[0], S[1] // 2 + 4), fill=(255, 255, 255))
        return im

    # pared con los dos cuadros tapados con tela: se destapan al final
    ret_c = Image.open(A('casos', 'curro', 'retrato-clasico-es.jpg')).convert('RGB')
    ret_n = Image.open(A('casos', 'noah', 'retrato-botanico-es.jpg')).convert('RGB')
    pared, marcos = lienzo([ret_c, ret_n], ['Curro', 'Noah'])
    (a0, b0, a1, b1), (c0, d0, c1, d1) = marcos
    cajas = [(a0 - 30, b0 - 30, a1 + 12, b1 + 70), (c0 - 12, d0 - 30, c1 + 30, d1 + 70)]
    telas = [trapo(cajas[0])]
    tt, mm = trapo(cajas[1])
    telas.append((tt.transpose(Image.FLIP_LEFT_RIGHT), mm.transpose(Image.FLIP_LEFT_RIGHT)))

    def tapada(caida=0.0):
        return con_trapo(con_trapo(pared, *telas[1], caida, cajas[1]), *telas[0], caida, cajas[0])

    quieta = tapada()
    H = pared.height
    todo = (pared.width / 2, H / 2, H)
    cerca = (pared.width / 2, (b0 + b1) / 2 + 120, H * .8)

    render('reel-competicion-alegria-es.mp4', [
        (1.6, lambda t, x: recorte_log(quieta, x, todo, cerca), [(TXT['gancho'], ARR, 0, 1)]),
        (4.2, partida, [(TXT['curro'], ARR, 0, 1)]),
        (0.7, lambda t, x: recorte_log(tapada(min(1, x * 1.1)), 0, cerca, cerca), []),
        (2.6, lambda t, x: recorte_log(pared, x, cerca, todo), [(TXT['final'], ARR, .05, 1)]),
    ])


if __name__ == '__main__':
    montar()
