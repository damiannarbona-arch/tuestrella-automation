"""Reel "duelo" (1080×1920, ~13 s): dos mascotas peleándose (vídeo real) → "¿quieres saber por qué se pelean?"
→ dos marcos iguales tapados con trapo, con su nombre debajo → cae un trapo → cae el otro → los dos retratos
→ "¿tú cuál eliges? Team A o Team B" (pregunta para comentarios).

Uso: python3 generador/video/reel_duelo.py DUELO [idiomas]      p. ej. … avelino-lichi en,es
Necesita: assets/mockups/pared-dos-marcos-iguales.webp (2 huecos grises, prompt en generador/prompts/pared-dos-marcos-iguales.md),
assets/casos/<caso>/retrato-<estilo>-<idioma>.jpg de cada mascota y el clip de la pelea.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tiktok_revelacion import render, leer_clip, de_clip  # noqa: E402
from reel_polaroids import abrir, ARR  # noqa: E402
from reel_zoom import recorte_log  # noqa: E402
from reel_trapo import trapo, con_trapo  # noqa: E402
from banner_youtube import huecos  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)
ESCENA = os.path.join(RAIZ, 'assets', 'mockups', 'pared-dos-marcos-iguales.webp')
LETRA = os.path.join(RAIZ, 'generador', 'fuentes', 'Satisfy-Regular.ttf')
CW, ARRIBA = 2160, 600          # lienzo: la escena a 2160 de ancho y 600 px de pared añadida arriba (9:16 = 2160×3840)
PASPARTU = 54                   # del hueco gris al borde exterior del marco, en px de la escena original

DUELOS = {
    'avelino-lichi': {
        'mascotas': [('avelino', 'Avelino', 'clasico'), ('lichi', 'Lichi', 'lavanda')],   # izquierda, derecha
        'clip': (C('lichi', 'video-pelea.mp4'), .5, 0.8, 2.2),   # ruta, centro x, desde (s), duración
        'txt': {
            'en': {'a': [('Want to know', 'b'), ("why they're fighting?", 'b')],
                   'b': [('They each got', 'b'), ('their own portrait…', 'b')],
                   'c': [('…and each one says', 'b'), ('theirs is the best', 'b')],
                   'd': [('Which one wins?', 'b'), ('Team Avelino or Team Lichi', 'i')]},
            'es': {'a': [('¿Quieres saber', 'b'), ('por qué se pelean?', 'b')],
                   'b': [('Cada uno tiene', 'b'), ('su propio retrato…', 'b')],
                   'c': [('…y cada uno dice que', 'b'), ('el suyo es el mejor', 'b')],
                   'd': [('¿Tú cuál eliges?', 'b'), ('Team Avelino o Team Lichi', 'i')]},
        },
    },
}


def lienzo(retratos, nombres):
    """Escena 9:16 con los retratos en los huecos, de izquierda a derecha, y el nombre bajo cada marco.
    Devuelve la imagen y la caja exterior de cada marco (en px del lienzo)."""
    esc = Image.open(ESCENA).convert('RGB')
    cajas = sorted(huecos(esc), key=lambda c: c[0])
    for (x0, y0, x1, y1), ret in zip(cajas, retratos):
        x0, y0, x1, y1 = x0 - 1, y0 - 1, x1 + 1, y1 + 1
        esc.paste(ImageOps.fit(ret, (x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))
    k = CW / esc.width
    esc = esc.resize((CW, round(esc.height * k)), Image.LANCZOS)
    im = Image.new('RGB', (CW, ARRIBA + esc.height))
    im.paste(esc.crop((0, 0, CW, 4)).resize((CW, ARRIBA + 4)), (0, 0))   # se prolonga la pared hacia arriba
    im.paste(esc, (0, ARRIBA))
    d, f = ImageDraw.Draw(im), ImageFont.truetype(LETRA, 150)
    marcos = []
    for (x0, y0, x1, y1), nombre in zip(cajas, nombres):
        m = [round((x0 - PASPARTU) * k), round((y0 - PASPARTU) * k) + ARRIBA,
             round((x1 + PASPARTU) * k), round((y1 + PASPARTU) * k) + ARRIBA]
        marcos.append(m)
        d.text(((m[0] + m[2]) / 2, m[3] + 140), nombre, font=f, fill=(58, 48, 40), anchor='mm')
    return im, marcos


def montar(duelo, idiomas='en,es'):
    cfg = DUELOS[duelo]
    ruta, fx, desde, dur_clip = cfg['clip']
    frames, fps = leer_clip(ruta, fx)
    pelea = de_clip(frames, fps, desde)
    for lang in idiomas.split(','):
        T = cfg['txt'][lang]
        rot = lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]
        retratos = [abrir(C(caso, f'retrato-{estilo}-{lang}.jpg')) for caso, _, estilo in cfg['mascotas']]
        pared, marcos = lienzo(retratos, [n for _, n, _ in cfg['mascotas']])
        # el trapo cubre el marco y cuelga un poco por debajo, sin invadir el hueco entre marcos; el de la derecha, en espejo
        (a0, b0, a1, b1), (c0, d0, c1, d1) = marcos
        cajas = [(a0 - 30, b0 - 30, a1 + 12, b1 + 70), (c0 - 12, d0 - 30, c1 + 30, d1 + 70)]
        telas = [trapo(cajas[0])]
        t, m = trapo(cajas[1])
        telas.append((t.transpose(Image.FLIP_LEFT_RIGHT), m.transpose(Image.FLIP_LEFT_RIGHT)))
        solo_dcha = con_trapo(pared, *telas[1], caja=cajas[1])
        tapada = con_trapo(solo_dcha, *telas[0], caja=cajas[0])

        H = pared.height
        todo = (CW / 2, H / 2, H)
        cerca = (CW / 2, (marcos[0][1] + marcos[0][3]) / 2 + 120, H * .86)
        foco = [((x0 + x1) / 2, (y0 + y1) / 2 + 60, (x1 - x0) * 16 / 9 * 1.22) for x0, y0, x1, y1 in marcos]
        v = lambda img, x, c0, c1: recorte_log(img, x, c0, c1)

        render(f'reel-{duelo}-{lang}.mp4', [
            (dur_clip, lambda tl, x: pelea(tl), rot('a', ARR)),
            (1.6, lambda tl, x: v(tapada, x, todo, cerca), rot('b', ARR, .1)),
            (0.9, lambda tl, x: v(tapada, x, cerca, foco[0]), []),
            (0.6, lambda tl, x: v(con_trapo(solo_dcha, *telas[0], min(1, x * 1.05), cajas[0]), 0, foco[0], foco[0]), []),
            (1.1, lambda tl, x: v(solo_dcha, x, foco[0], (*foco[0][:2], foco[0][2] * .94)), []),
            (0.4, lambda tl, x: v(solo_dcha, 0, foco[1], foco[1]), []),
            (0.6, lambda tl, x: v(con_trapo(pared, *telas[1], min(1, x * 1.05), cajas[1]), 0, foco[1], foco[1]), []),
            (1.1, lambda tl, x: v(pared, x, foco[1], (*foco[1][:2], foco[1][2] * .94)), []),
            (2.3, lambda tl, x: v(pared, x, cerca, todo), rot('c', ARR, .05)),
            (2.6, lambda tl, x: v(pared, x, todo, (todo[0], todo[1], H * .97)), rot('d', ARR, .05)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:3])
