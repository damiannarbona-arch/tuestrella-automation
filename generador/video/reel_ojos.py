"""Reel "el reto de los ojos" (1080×1920, ~13 s): vídeo real ("tiene un ojo de cada color…") → zoom a sus ojos
("…¿lo clavará su retrato?") → ráfaga de fotos → cuadro tapado → cae el trapo → zoom a los ojos del retrato
→ pantalla partida ojos reales / ojos pintados → llamada a la acción.

Uso: python3 generador/video/reel_ojos.py CASO ESTILO [idiomas]      p. ej. … ricky aventurero en,es
Necesita en assets/casos/<caso>/: video-ventana.mp4, foto-principal.jpg, extra-*.jpg y retrato-<estilo>-<idioma>.jpg.
La pared (mockup-pared-<idioma>.jpg) se crea aquí si no existe, con el retrato en el marco grande de
assets/mockups/pared-dos-marcos.webp.
"""
import os, sys
from PIL import Image, ImageDraw, ImageOps

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
PAPEL = (246, 242, 236)

CASOS = {
    'ricky': {
        'clip': (.5, 0.0, 1.6),                    # centro x, desde (s), duración
        'ojos_foto': (.427, .375),                 # entre los ojos en foto-principal
        'ojos_retrato': (.51, .275),               # entre los ojos en el retrato
        'rafaga': [('extra-1.jpg', (.48, .42)), ('extra-4.jpg', (.4, .33)), ('extra-2.jpg', (.5, .45)),
                   ('foto-principal.jpg', (.45, .38))],
        'pequeno': ('lichi', 'retrato-lavanda-{}.jpg'),   # retrato del marco pequeño de la pared
        'txt': {
            'en': {'a': [('Ricky has one eye', 'b'), ('of each color…', 'b')],
                   'b': [('…would his portrait', 'b'), ('get it right?', 'b')],
                   'c': [('4 photos from his family', 'b')],
                   'd': [('Moment of truth…', 'b')],
                   'e': [('Both of them.', 'b'), ('Exactly.', 'b')],
                   'f': [('Want one of yours?', 'b'), ('Link in bio', 'i')]},
            'es': {'a': [('Ricky tiene un ojo', 'b'), ('de cada color…', 'b')],
                   'b': [('…¿lo clavará', 'b'), ('su retrato?', 'b')],
                   'c': [('4 fotos de su familia', 'b')],
                   'd': [('Momento de la verdad…', 'b')],
                   'e': [('Los dos.', 'b'), ('Tal cual.', 'b')],
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
    foto = abrir(C(caso, 'foto-principal.jpg'))
    rafaga = [(abrir(C(caso, f)), foco) for f, foco in cfg['rafaga']]
    tela, m = trapo()
    for lang in idiomas.split(','):
        T = cfg['txt'][lang]
        rot = lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]
        muro, (gx0, gy0, gx1, gy1) = pared(caso, estilo, lang, cfg)
        tapada = con_trapo(muro, tela, m)
        ret = abrir(C(caso, f'retrato-{estilo}-{lang}.jpg'))
        ox, oy = cfg['ojos_retrato']
        ojos_pared = (gx0 + ox * (gx1 - gx0), gy0 + oy * (gy1 - gy0), (gx1 - gx0) * .55 * 16 / 9)
        fo = cfg['ojos_foto']

        def rafaga_fn(tl, x):
            img, foco = rafaga[min(int(x * len(rafaga)), len(rafaga) - 1)]
            return kenburns(img, S, (x * len(rafaga)) % 1, 1.15, 1.25, foco, foco)

        def partida(tl, x):
            im = Image.new('RGB', S, PAPEL)
            mitad = (S[0], S[1] // 2)
            z = 1 + .06 * x
            im.paste(kenburns(foto, mitad, 0, 2.6 * z, 2.6 * z, fo, fo), (0, 0))
            im.paste(kenburns(ret, mitad, 0, 3.2 * z, 3.2 * z, (ox, oy), (ox, oy)), (0, S[1] // 2))
            ImageDraw.Draw(im).line((0, S[1] // 2, S[0], S[1] // 2), fill=PAPEL, width=10)
            return im

        render(f'reel-{caso}-ojos-{lang}.mp4', [
            (dur_clip, lambda tl, x: clip(tl), rot('a', ARR)),
            (1.4, lambda tl, x: kenburns(foto, S, x, 1.3, 2.4, (.5, .45), fo), rot('b', ARR)),
            (1.2, rafaga_fn, rot('c', ABA)),
            (1.5, lambda tl, x: recorte_log(tapada, x, VISTA, MARCO), rot('d', ABA, .1)),
            (0.7, lambda tl, x: recorte_log(con_trapo(muro, tela, m, min(1, x * 1.05)), 0, MARCO, MARCO), []),
            (1.0, lambda tl, x: recorte_log(muro, x, MARCO, (MARCO[0], MARCO[1] - 40, MARCO[2] * .92)), []),
            (1.3, lambda tl, x: recorte_log(muro, x, (MARCO[0], MARCO[1] - 40, MARCO[2] * .92), ojos_pared), []),
            (2.2, partida, rot('e', 820, .05)),
            (2.2, lambda tl, x: recorte_log(muro, x, VISTA, (VISTA[0], VISTA[1], VISTA[2] * .95)), rot('f', ABA, .1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:4])
