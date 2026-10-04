"""Reel de humor de Curro (1080×1920, ~17 s): "¿estás preparado para verte?" (ojos cerrados) → "Allá voy…"
(vídeo real andando hacia la cámara) → cuadro tapado → cae el trapo → "Ya sabía yo que era guapo" (ojos abiertos)
→ detalle de rasgos y frase ("un cuadro personalizado, no uno cualquiera") → llamada.

Uso: python3 generador/video/reel_curro.py [idiomas]      (es por defecto)
Sin audio: la música se pone en la app.
"""
import os, sys
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from videos import kenburns, ease  # noqa: E402
from tiktok_revelacion import render, S, ARR  # noqa: E402
from reel_polaroids import ABA  # noqa: E402
from reel_zoom import recorte_log  # noqa: E402
from reel_trapo import trapo, con_trapo, VISTA, MARCO  # noqa: E402
from reel_historia import pared  # noqa: E402
from reel_producto import tramo  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda *p: os.path.join(RAIZ, 'assets', 'casos', 'curro', *p)
CFG = {'pequeno': ('avelino', 'retrato-clasico-{}.jpg')}

TXT = {
    'es': {'a': [('Curro, ¿estás', 'b'), ('preparado para verte?', 'b')],
           'b': [('Allá voy…', 'b')],
           'c': [('Redoble de tambores…', 'b')],
           'd': [('Ya sabía yo', 'b'), ('que era guapo', 'b')],
           'e': [('Un cuadro personalizado,', 'b'), ('no uno cualquiera', 'i')],
           'f': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
}


def montar(idiomas='es'):
    abrir = lambda f: ImageOps.exif_transpose(Image.open(C(f))).convert('RGB')
    dormido, guapo = abrir('foto-2-limpia.jpg'), abrir('foto-1-limpia.jpg')
    anda = tramo(C('video-1.mp4'), 8.4, 2.2)          # se acerca de frente a la cámara
    tela, m = trapo()
    for lang in idiomas.split(','):
        T = TXT[lang]
        rot = lambda k, y=ARR, a=.0, b=1.0: [(T[k], y, a, b)]
        muro, (gx0, gy0, gx1, gy1) = pared('curro', 'clasico', lang, CFG)
        tapada = con_trapo(muro, tela, m)
        cerca = (MARCO[0], MARCO[1] - 40, MARCO[2] * .92)
        detalle = (gx0 + .5 * (gx1 - gx0), gy0 + .8 * (gy1 - gy0), (gx1 - gx0) * .97 * 16 / 9)
        caer = lambda tl, x: recorte_log(con_trapo(muro, tela, m, min(1, ease(x) * 1.05)), 0, MARCO, MARCO)
        render(f'reel-curro-{lang}.mp4', [
            (2.4, lambda tl, x: kenburns(dormido, S, x, 1.15, 1.45, (.52, .45), (.56, .42)), rot('a')),
            (2.0, lambda tl, x: anda(tl), rot('b')),
            (1.5, lambda tl, x: recorte_log(tapada, x, VISTA, MARCO), rot('c', ABA, .1)),
            (0.7, caer, []),
            (1.4, lambda tl, x: recorte_log(muro, x, MARCO, cerca), []),
            (2.0, lambda tl, x: kenburns(guapo, S, x, 1.2, 1.45, (.53, .45), (.56, .42)), rot('d')),
            (2.6, lambda tl, x: recorte_log(muro, x, cerca, detalle), rot('e', ARR, .1)),
            (2.4, lambda tl, x: recorte_log(muro, x, VISTA, (VISTA[0], VISTA[1], VISTA[2] * .95)), rot('f', ABA, .1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:2])
