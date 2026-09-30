"""Reel "¿foto o cuadro?" (1080×1920, ~12,5 s): primerísimo plano de los ojos del retrato (parece una foto real)
→ la cámara se aleja → es un cuadro colgado en la pared → el perro de verdad → sus fotos vuelan a las polaroids
→ cara real frente a cara del retrato → llamada a la acción.

Uso: python3 generador/video/reel_zoom.py CASO ESTILO [idiomas]      p. ej. … sonic aventurero en,es
Necesita en assets/casos/<caso>/: retrato-<estilo>-<idioma>.jpg, diseno-<estilo>-<idioma>.png|webp,
foto-principal.jpg y mockup-pared-<idioma>.jpg (el retrato en el marco grande de assets/mockups/pared-dos-marcos).
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from videos import kenburns, ease  # noqa: E402
from tiktok_revelacion import render  # noqa: E402
from reel_polaroids import en_pantalla, tarjetas, vuelo, abrir, ARR, ABA  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)
S = (1080, 1920)

CASOS = {
    'sonic': {
        'ojos': (.628, .215),          # entre los ojos, en el retrato
        'cara_foto': (.5, .36),        # cara en foto-principal
        'hueco': (1534, 347, 2182, 1331),   # lámina del marco grande en mockup-pared (3072×2048)
        'final': (1300, 46, 2400, 2002),    # encuadre final 9:16 de la pared (sin el marco pequeño)
        'txt': {
            'en': {'a': [('He has no idea', 'b'), ('what I did with his photos…', 'b')],
                   'c': [("…and he's still", 'b'), ('wondering', 'b')],
                   'e': [('Every curl,', 'b'), ('just as he is', 'b')],
                   'f': [('Want one of yours?', 'b'), ('Link in bio', 'i')]},
            'es': {'a': [('No sabe lo que he hecho', 'b'), ('con sus fotos…', 'b')],
                   'c': [('…y sigue', 'b'), ('preguntándoselo', 'b')],
                   'e': [('Cada rizo,', 'b'), ('tal cual es', 'b')],
                   'f': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
        },
    },
}


def recorte_log(img, t, caja0, caja1):
    """Interpola el recorte (cx, cy, alto) en escala logarítmica: el alejamiento se siente constante."""
    e = ease(t)
    (cx0, cy0, h0), (cx1, cy1, h1) = caja0, caja1
    h = math.exp(math.log(h0) + (math.log(h1) - math.log(h0)) * e)
    k = (h - h0) / (h1 - h0) if h1 != h0 else e  # el centro sigue al tamaño
    cx, cy = cx0 + (cx1 - cx0) * k, cy0 + (cy1 - cy0) * k
    w = h * S[0] / S[1]
    x = min(max(cx - w / 2, 0), img.width - w)
    y = min(max(cy - h / 2, 0), img.height - h)
    return img.resize(S, Image.LANCZOS, box=(x, y, x + w, y + h))


def montar(caso, estilo, idiomas='en,es'):
    cfg = CASOS[caso]
    foto = abrir(C(caso, 'foto-principal.jpg'))
    for lang in idiomas.split(','):
        T = cfg['txt'][lang]
        rot = lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]
        ret = abrir(C(caso, f'retrato-{estilo}-{lang}.jpg'))
        dis = [f for f in (C(caso, f'diseno-{estilo}-{lang}.png'), C(caso, f'diseno-{estilo}-{lang}.webp')) if os.path.exists(f)][0]
        diseno = Image.open(dis).convert('RGB')
        pared = abrir(C(caso, f'mockup-pared-{lang}.jpg'))
        base = en_pantalla(diseno.resize((diseno.width * 3, diseno.height * 3), Image.LANCZOS))
        fin = en_pantalla(ret)
        piezas = tarjetas(diseno, ret)

        # A · de los ojos al retrato entero (alto de pantalla = alto del retrato)
        ox, oy = cfg['ojos']
        a0 = (ox * ret.width, oy * ret.height, ret.height / 3.2)
        a1 = (ret.width / 2, ret.height / 2, ret.height)
        def escena_a(tl, x):
            return recorte_log(ret, x, a0, a1).filter(ImageFilter.UnsharpMask(2, 80, 2))

        # B · la lámina dentro del marco → la pared entera
        hx0, hy0, hx1, hy1 = cfg['hueco']
        fx0, fy0, fx1, fy1 = cfg['final']
        b0 = ((hx0 + hx1) / 2, (hy0 + hy1) / 2, hy1 - hy0)
        b1 = ((fx0 + fx1) / 2, (fy0 + fy1) / 2, fy1 - fy0)

        # E · cara real arriba, cara del retrato abajo
        mitad = (S[0], S[1] // 2)
        def escena_e(tl, x):
            im = Image.new('RGB', S)
            z = 1 + .08 * ease(x)
            im.paste(kenburns(foto, mitad, 0, 1.25 * z, 1.25 * z, (.5, .4), (.5, .4)), (0, 0))
            im.paste(kenburns(ret, mitad, 0, 1.9 * z, 1.9 * z, (ox - .06, oy + .07), (ox - .06, oy + .07)), (0, S[1] // 2))
            ImageDraw.Draw(im).line((0, S[1] // 2, S[0], S[1] // 2), fill=(246, 242, 236), width=8)
            return im

        def escena_d(tl, x):
            if x < .06:
                return base
            return fin if x > .94 else vuelo(base, piezas, x, inicios=(.08, .3, .52))

        render(f'reel-{caso}-zoom-{lang}.mp4', [
            (2.4, escena_a, rot('a', ARR)),
            (1.6, lambda tl, x: recorte_log(pared, x, b0, b1), rot('a', ARR, 0, .5)),
            (1.6, lambda tl, x: kenburns(foto, S, x, 1.05, 1.3, (.5, .45), cfg['cara_foto']), rot('c', ABA, .1)),
            (2.8, escena_d, []),
            (1.8, escena_e, rot('e', 850, .1)),
            (2.2, lambda tl, x: recorte_log(pared, x, b1, (b1[0], b1[1], b1[2] * .92)), rot('f', ABA, .1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:4])
