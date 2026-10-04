"""Reel de humor de Curro (1080×1920, ≤15 s), con vídeo real hasta el resultado: "¿estás preparado para ver tu
retrato personalizado?" (Curro mirando) → "Se lo está pensando…" (se da la vuelta) → "Allá voy…" (anda hacia la
cámara) → cuadro tapado → cae el trapo → "Ya sabía yo que era guapo" (llega de frente, a cámara lenta)
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
    'es': {'a': [('Curro, ¿estás preparado', 'b'), ('para ver tu retrato', 'b'), ('personalizado?', 'b')],
           'p': [('Se lo está pensando…', 'b')],
           'b': [('Allá voy…', 'b')],
           'd': [('Ya sabía yo', 'b'), ('que era guapo', 'b')],
           'e': [('Un cuadro personalizado,', 'b'), ('no uno cualquiera', 'i')],
           'f': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
}


def montar(idiomas='es'):
    abrir = lambda f: ImageOps.exif_transpose(Image.open(C(f))).convert('RGB')
    video = C('video-1.mp4')
    mira = tramo(video, 0.0, 3.0)                      # quieto, mirando alrededor
    piensa = tramo(video, 6.0, 2.0)                    # se da la vuelta
    anda = tramo(video, 8.3, 2.0)                      # anda hacia la cámara
    llega = tramo(video, 10.3, 1.2)                    # llega de frente (se pone a cámara lenta)
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
            (2.6, lambda tl, x: mira(tl), rot('a')),
            (1.6, lambda tl, x: piensa(tl), rot('p')),
            (1.8, lambda tl, x: anda(tl), rot('b')),
            (1.0, lambda tl, x: recorte_log(tapada, x, VISTA, MARCO), []),
            (0.7, caer, []),
            (1.2, lambda tl, x: recorte_log(muro, x, MARCO, cerca), []),
            (1.8, lambda tl, x: llega(tl * .66), rot('d')),
            (2.2, lambda tl, x: recorte_log(muro, x, cerca, detalle), rot('e', ARR, .1)),
            (2.0, lambda tl, x: recorte_log(muro, x, VISTA, (VISTA[0], VISTA[1], VISTA[2] * .95)), rot('f', ABA, .1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:2])
