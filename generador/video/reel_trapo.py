"""Reel "trapo" (1080×1920, ~11,5 s): foto original ("no sabe lo que he hecho con sus fotos…") → cuadro tapado
con un trapo → ráfaga rápida de sus fotos → pausa de intriga → cae el trapo → resultado → llamada a la acción.

Uso: python3 generador/video/reel_trapo.py CASO ESTILO [idiomas]      p. ej. … sonic aventurero en,es
Necesita en assets/casos/<caso>/: foto-principal.jpg, extra-1..3.jpg y mockup-pared-<idioma>.jpg
(retrato en el marco grande de assets/mockups/pared-dos-marcos). El trapo se dibuja aquí.
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
from videos import kenburns, ease  # noqa: E402
from tiktok_revelacion import render  # noqa: E402
from reel_polaroids import abrir, ARR, ABA  # noqa: E402
from reel_zoom import recorte_log  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)
S = (1080, 1920)
TRAPO = (1395, 210, 2305, 1545)          # zona del trapo en mockup-pared (3072×2048), marco grande
VISTA = (1850, 1024, 1956)               # encuadre 9:16 de la pared (centro x, centro y, alto)
MARCO = (1858, 840, 1300)                # acercamiento al marco

CASOS = {
    'sonic': {
        'foco': [(.5, .38), (.55, .6), (.78, .72), (.6, .5)],   # principal, extra-1..3
        'txt': {
            'en': {'a': [('He has no idea', 'b'), ('what I did with his photos…', 'b')],
                   'b': [("(don't tell him)", 'i')],
                   'c': [('4 photos from my phone…', 'b')],
                   'd': [('Ready to see it?', 'b')],
                   'f': [('Want one of yours?', 'b'), ('Link in bio', 'i')]},
            'es': {'a': [('No sabe lo que he hecho', 'b'), ('con sus fotos…', 'b')],
                   'b': [('(que no se entere)', 'i')],
                   'c': [('4 fotos de mi móvil…', 'b')],
                   'd': [('¿Quieres verlo?', 'b')],
                   'f': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
        },
    },
}


def trapo(caja=TRAPO):
    """Tela de lino (imagen y máscara) con pliegues que se abren hacia abajo."""
    x0, y0, x1, y1 = caja
    w, h = x1 - x0, y1 - y0
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    u, v = xx / w, yy / h
    rng = np.random.default_rng(5)
    pl = np.zeros_like(u)
    for f, a, ph in [(2.3, .09, .4), (4.1, .06, 1.3), (6.7, .035, 2.2), (10.5, .018, .9)]:
        pl += a * np.sin(2 * np.pi * (f * u + ph) + (v ** 1.4) * 2.4 * np.sin(2.5 * u + ph)) * (.15 + .85 * v ** 1.3)
    luz = 1.03 - .09 * v + pl - .07 * u
    img = np.array([237, 230, 216], float)[None, None, :] * luz[..., None]
    img += (rng.normal(0, 1, (h, w)) * 2.2 + rng.normal(0, 1, (h, 1)) * 1.6)[..., None]
    tela = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))
    m = Image.new('L', (w, h), 0)
    n = 60
    bajo = [(w - 14 - (w - 28) * i / n, h - 38 + 16 * math.sin(i * .33 + .5) + 9 * math.sin(i * .9)) for i in range(n + 1)]
    ImageDraw.Draw(m).polygon([(26, 58), (70, 10), (w - 70, 10), (w - 26, 58), (w - 8, h * .5)] + bajo + [(8, h * .5)], fill=255)
    return tela, m.filter(ImageFilter.GaussianBlur(2.5))


def con_trapo(pared, tela, m, caida=0.0, caja=TRAPO):
    """Pared con el trapo; caida 0–1: el trapo resbala hacia abajo y desaparece."""
    W, H = pared.size
    x0, y0 = caja[0], caja[1]
    dy = int((caida ** 2) * (H - y0 + 200))
    out = pared.copy()
    sh = Image.new('L', (W, H), 0)
    sh.paste(m.point(lambda a: int(a * .5 * (1 - caida))), (x0 + 26, y0 + 34 + dy))
    out.paste(Image.new('RGB', (W, H), (70, 60, 50)), (0, 0), sh.filter(ImageFilter.GaussianBlur(30)))
    t = tela if caida == 0 else tela.filter(ImageFilter.GaussianBlur(6 * caida))  # desenfoque de movimiento
    out.paste(t, (x0, y0 + dy), m)
    return out


def montar(caso, estilo, idiomas='en,es'):
    cfg = CASOS[caso]
    fotos = [abrir(C(caso, 'foto-principal.jpg'))] + [abrir(C(caso, f'extra-{i}.jpg')) for i in (1, 2, 3)]
    tela, m = trapo()
    for lang in idiomas.split(','):
        T = cfg['txt'][lang]
        rot = lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]
        pared = abrir(C(caso, f'mockup-pared-{lang}.jpg'))
        tapada = con_trapo(pared, tela, m)
        vista = lambda img, x, c0, c1: recorte_log(img, x, c0, c1)
        orden = [1, 2, 3, 0]  # ráfaga: playa, cascada, baño, principal

        def rafaga(tl, x):
            i = min(int(x * len(orden)), len(orden) - 1)
            k = orden[i]
            return kenburns(fotos[k], S, (x * len(orden)) % 1, 1.1, 1.2, cfg['foco'][k], cfg['foco'][k])

        def caer(tl, x):
            return vista(con_trapo(pared, tela, m, min(1, ease(x) * 1.05)), 0, MARCO, MARCO)

        render(f'reel-{caso}-trapo-{lang}.mp4', [
            (2.0, lambda tl, x: kenburns(fotos[0], S, x, 1.05, 1.25, (.5, .45), cfg['foco'][0]), rot('a', ARR)),
            (1.4, lambda tl, x: vista(tapada, x, VISTA, (VISTA[0], VISTA[1], VISTA[2] * .93)), rot('b', ABA, .1)),
            (1.4, rafaga, rot('c', ABA)),
            (1.5, lambda tl, x: vista(tapada, x, VISTA, MARCO), rot('d', ABA, .15)),
            (0.7, caer, []),
            (2.2, lambda tl, x: vista(pared, x, MARCO, (MARCO[0], MARCO[1] - 60, MARCO[2] * .8)), []),
            (2.3, lambda tl, x: vista(pared, x, VISTA, (VISTA[0], VISTA[1], VISTA[2] * .95)), rot('f', ABA, .1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:4])
