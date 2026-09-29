"""Reel/Short/TikTok (1080×1920, ~13 s): gancho con sus fotos → retrato tapado → las fotos VUELAN a las
polaroids del retrato → zoom a la cara → pared → caja → llamada a la acción. Cortes secos.

Uso:
  python3 generador/video/reel_polaroids.py CASO ESTILO [idiomas]
  p. ej. python3 generador/video/reel_polaroids.py lula rosa en,es

Necesita en assets/casos/<caso>/: diseno-<estilo>-<idioma>.webp (polaroids grises), retrato-<estilo>-<idioma>.jpg,
foto-principal.jpg, extra-1..3.jpg, mockup-pared-<idioma>.jpg y mockup-<estilo>-<idioma>-caja.jpg.
El retrato no pasa por la IA de vídeo: se anima aquí, idéntico al impreso. Salida sin audio (música en la app).
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from videos import kenburns, ease  # noqa: E402
from tiktok_revelacion import render  # noqa: E402
from polaroids import cuadros_grises  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)
S = (1080, 1920)
PAPEL = (246, 242, 236)
ARR, ABA = 250, 1330
RW, RX, RY = 1000, 40, 250  # retrato en pantalla: ancho y posición

CASOS = {
    'lula': {
        'gancho': ('extra-2.jpg', (.34, .27)),                     # foto del gancho y su cara
        'rafaga': [('extra-1.jpg', (.5, .35)), ('extra-3.jpg', (.63, .45)), ('foto-principal.jpg', (.5, .3))],
        'cara': (.53, .27),                                         # cara en el retrato
        'txt': {
            'en': {'gancho': [('She stared at my popcorn', 'b'), ('for 3 hours…', 'b')],
                   'rafaga': [('…so I sent 4 photos of her', 'b')], 'espera': [('48 hours later…', 'b')],
                   'rasgos': [('Every feature,', 'b'), ('just as she is', 'b')],
                   'pared': [('Now she lives on my wall', 'b')],
                   'cta': [('Want one of yours?', 'b'), ('Link in bio', 'i')]},
            'es': {'gancho': [('3 horas mirando', 'b'), ('mis palomitas…', 'b')],
                   'rafaga': [('…así que mandé 4 fotos suyas', 'b')], 'espera': [('48 horas después…', 'b')],
                   'rasgos': [('Cada rasgo,', 'b'), ('tal cual es', 'b')],
                   'pared': [('Ahora vive en mi pared', 'b')],
                   'cta': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
        },
    },
}


def abrir(p):
    return ImageOps.exif_transpose(Image.open(p)).convert('RGB')


def en_pantalla(img):
    """El retrato entero sobre papel, en la posición fija del reel."""
    f = Image.new('RGB', S, PAPEL)
    rh = int(img.height * RW / img.width)
    f.paste(img.resize((RW, rh), Image.LANCZOS), (RX, RY))
    return f


def tarjetas(diseno, final):
    """Cada polaroid como recorte del retrato final (con su perspectiva), en coordenadas de pantalla."""
    k = RW / diseno.width
    fin = en_pantalla(final)
    out = []
    for q in cuadros_grises(np.asarray(diseno)):
        q = q * k + (RX, RY)
        x0, y0 = np.floor(q.min(0)).astype(int) - 3
        x1, y1 = np.ceil(q.max(0)).astype(int) + 3
        m = Image.new('L', (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(m).polygon([tuple(p - (x0, y0)) for p in q], fill=255)
        pieza = fin.crop((x0, y0, x1, y1)).convert('RGBA')
        pieza.putalpha(m.filter(ImageFilter.MaxFilter(3)))
        out.append((pieza, ((x0 + x1) / 2, (y0 + y1) / 2)))
    return out


def vuelo(base, piezas, x, inicios, dur=.22):
    """Las fotos entran desde abajo girando y se posan en su polaroid. x = avance 0–1 de la escena."""
    im = base.copy().convert('RGBA')
    salidas = [(-250, 2300, -28), (1330, 2250, 24), (540, 2450, -16)]
    for (pieza, (tx, ty)), t0, (sx, sy, rot) in zip(piezas, inicios, salidas):
        if x < t0:
            continue
        k = ease(min(1, (x - t0) / dur))
        esc = 2.3 + (1 - 2.3) * k
        ang = rot * (1 - k)
        p = pieza.resize((max(1, int(pieza.width * esc)), max(1, int(pieza.height * esc))), Image.LANCZOS)
        p = p.rotate(ang, resample=Image.BICUBIC, expand=True)
        cx, cy = sx + (tx - sx) * k, sy + (ty - sy) * k
        if k < 1:  # sombra mientras vuela
            s = Image.new('RGBA', p.size, (40, 30, 20, 0))
            s.putalpha(p.getchannel('A').point(lambda v: int(v * .35)))
            s = s.filter(ImageFilter.GaussianBlur(18))
            im.alpha_composite(s, (int(cx - p.width / 2 + 14), int(cy - p.height / 2 + 30)))
        im.alpha_composite(p, (int(cx - p.width / 2), int(cy - p.height / 2)))
    return im.convert('RGB')


def montar(caso, estilo, idiomas='en,es'):
    cfg = CASOS[caso]
    g_img, g_foco = abrir(C(caso, cfg['gancho'][0])), cfg['gancho'][1]
    rafaga = [(abrir(C(caso, f)), foco) for f, foco in cfg['rafaga']]
    for lang in idiomas.split(','):
        T = cfg['txt'][lang]
        rot = lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]
        diseno = Image.open(C(caso, f'diseno-{estilo}-{lang}.webp')).convert('RGB')
        final = abrir(C(caso, f'retrato-{estilo}-{lang}.jpg'))
        base = en_pantalla(diseno.resize((diseno.width * 3, diseno.height * 3), Image.LANCZOS))
        fin = en_pantalla(final)
        piezas = tarjetas(diseno, final)
        tapado = fin.filter(ImageFilter.GaussianBlur(38))
        pared = abrir(C(caso, f'mockup-pared-{lang}.jpg'))
        caja = abrir(C(caso, f'mockup-{estilo}-{lang}-caja.jpg'))
        cx, cy = cfg['cara']
        cara = ((RX + cx * RW) / S[0], (RY + cy * RW * 1.5) / S[1])

        def rafaga_fn(tl, x):
            img, foco = rafaga[min(int(x * len(rafaga)), len(rafaga) - 1)]
            return kenburns(img, S, (x * len(rafaga)) % 1, 1.15, 1.25, foco, foco)

        def revelar(tl, x):
            if x < .08:  # se va el desenfoque del retrato (todavía con las polaroids vacías)
                return base.filter(ImageFilter.GaussianBlur(38 * (1 - x / .08)))
            if x > .92:
                return fin
            return vuelo(base, piezas, x, inicios=(.12, .34, .56))

        render(f'reel-{caso}-{estilo}-{lang}.mp4', [
            (1.8, lambda tl, x: kenburns(g_img, S, x, 1.0, 1.9, (.5, .55), g_foco), rot('gancho', ABA)),  # de las palomitas a su cara
            (1.3, rafaga_fn, rot('rafaga', ARR)),
            (1.0, lambda tl, x: tapado, rot('espera', ARR)),
            (3.0, revelar, []),
            (1.6, lambda tl, x: kenburns(fin, S, x, 1.0, 2.2, (.5, .5), cara), rot('rasgos', ABA, .15)),
            (1.8, lambda tl, x: kenburns(pared, S, x, 1.0, 1.35, (.52, .5), (.5, .42)), rot('pared', ABA, .1)),
            (1.1, lambda tl, x: kenburns(caja, S, x, 1.0, 1.08, (.55, .45), (.55, .45)), []),
            (1.9, lambda tl, x: kenburns(fin, S, x, 1.0, 1.04), rot('cta', ABA, .1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:4])
