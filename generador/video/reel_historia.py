"""Reel "su historia" (1080×1920, ~12 s): vídeo real con su costumbre ("cada tarde espera en la ventana…")
→ ráfaga de sus fotos → cuadro tapado → cae el trapo → zoom a los letreros con sus sitios favoritos → llamada.
Sin primeros planos de los ojos: el retrato se enseña entero y se destaca la historia, no el detalle.

Uso: python3 generador/video/reel_historia.py CASO ESTILO [idiomas]      p. ej. … ricky aventurero en,es
Necesita en assets/casos/<caso>/: video-ventana.mp4, fotos y retrato-<estilo>-<idioma>.jpg. La pared
(mockup-pared-<idioma>.jpg) se crea aquí con el retrato en el marco grande de assets/mockups/pared-dos-marcos.webp.
"""
import os, sys
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from videos import kenburns  # noqa: E402
from tiktok_revelacion import render, leer_clip, de_clip  # noqa: E402
from reel_polaroids import abrir, ARR, ABA  # noqa: E402
from reel_zoom import recorte_log  # noqa: E402
from reel_trapo import trapo, con_trapo, VISTA, MARCO  # noqa: E402
from banner_youtube import huecos  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)
S = (1080, 1920)

CASOS = {
    'ricky': {
        'clip': (.5, 0.0, 1.6),                    # centro x, desde (s), duración
        'letreros': (.872, .36),                   # poste con sus sitios favoritos, en el retrato
        'rafaga': [('extra-1.jpg', (.48, .42)), ('extra-2.jpg', (.5, .45)), ('foto-principal.jpg', (.45, .38))],
        'pequeno': ('lichi', 'retrato-lavanda-{}.jpg'),   # retrato del marco pequeño de la pared
        'txt': {
            'en': {'a': [('Every evening, Ricky', 'b'), ('waits at the window…', 'b')],
                   'c': [('…so his family sent us', 'b'), ('his photos', 'b')],
                   'd': [('A surprise for him…', 'b')],
                   'e': [('His favorite spots,', 'b'), ('in his portrait', 'b')],
                   'f': [('Want one of yours?', 'b'), ('Link in bio', 'i')]},
            'es': {'a': [('Cada tarde, Ricky', 'b'), ('espera en la ventana…', 'b')],
                   'c': [('…así que su familia', 'b'), ('nos mandó sus fotos', 'b')],
                   'd': [('Una sorpresa para él…', 'b')],
                   'e': [('Sus sitios favoritos,', 'b'), ('en su retrato', 'b')],
                   'f': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
        },
    },
}


def pared(caso, estilo, lang, cfg):
    """mockup-pared-<lang>.jpg (3072×2048): retrato en el marco grande y otro caso en el pequeño.
    Devuelve la imagen y la caja del retrato en la pared."""
    esc = Image.open(os.path.join(RAIZ, 'assets', 'mockups', 'pared-dos-marcos.webp')).convert('RGB')
    esc = esc.resize((esc.width * 2, esc.height * 2), Image.LANCZOS)
    grande, pequeno = huecos(esc)[:2]
    otro = abrir(C(cfg['pequeno'][0], cfg['pequeno'][1].format(lang)))
    for (x0, y0, x1, y1), ret in ((grande, abrir(C(caso, f'retrato-{estilo}-{lang}.jpg'))), (pequeno, otro)):
        x0, y0, x1, y1 = x0 - 1, y0 - 1, x1 + 1, y1 + 1
        esc.paste(ImageOps.fit(ret, (x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))
    esc.save(C(caso, f'mockup-pared-{lang}.jpg'), quality=92)
    return esc, grande


def montar(caso, estilo, idiomas='en,es'):
    cfg = CASOS[caso]
    fx, desde, dur_clip = cfg['clip']
    frames, fps = leer_clip(C(caso, 'video-ventana.mp4'), fx)
    clip = de_clip(frames, fps, desde)
    rafaga = [(abrir(C(caso, f)), foco) for f, foco in cfg['rafaga']]
    tela, m = trapo()
    for lang in idiomas.split(','):
        T = cfg['txt'][lang]
        rot = lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]
        muro, (gx0, gy0, gx1, gy1) = pared(caso, estilo, lang, cfg)
        tapada = con_trapo(muro, tela, m)
        lx, ly = cfg['letreros']
        cerca = (MARCO[0], MARCO[1] - 40, MARCO[2] * .92)
        letreros = (gx0 + lx * (gx1 - gx0), gy0 + ly * (gy1 - gy0), (gx1 - gx0) * .42 * 16 / 9)

        def rafaga_fn(tl, x):
            img, foco = rafaga[min(int(x * len(rafaga)), len(rafaga) - 1)]
            return kenburns(img, S, (x * len(rafaga)) % 1, 1.15, 1.25, foco, foco)

        render(f'reel-{caso}-historia-{lang}.mp4', [
            (dur_clip, lambda tl, x: clip(tl), rot('a', ARR)),
            (1.5, rafaga_fn, rot('c', ABA)),
            (1.5, lambda tl, x: recorte_log(tapada, x, VISTA, MARCO), rot('d', ABA, .1)),
            (0.7, lambda tl, x: recorte_log(con_trapo(muro, tela, m, min(1, x * 1.05)), 0, MARCO, MARCO), []),
            (1.6, lambda tl, x: recorte_log(muro, x, MARCO, cerca), []),
            (2.2, lambda tl, x: recorte_log(muro, x, cerca, letreros), rot('e', ARR, .15)),
            (2.4, lambda tl, x: recorte_log(muro, x, VISTA, (VISTA[0], VISTA[1], VISTA[2] * .95)), rot('f', ABA, .1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:4])
