"""Reel "regalo" híbrido (1080×1920, ≤15 s): escena con IA (manos sacando el marco de la caja, etiquetar como IA)
con el retrato REAL encajado (componer_marco.py) → detalle del retrato (nombre, rasgos, frase) → vídeo real de la
mascota → llamada con fecha límite de Navidad. Nunca se presenta como clienta real: es una demostración del regalo.

Uso: python3 generador/video/reel_regalo_ia.py CASO COMPUESTO.mp4 VIDEO_MASCOTA DESDE      (es)
p. ej. … curro assets/ia/regalo-caja/curro-compuesto.mp4 assets/casos/curro/video-1.mp4 8.3
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'redes'))
from tiktok_revelacion import render, S, ARR  # noqa: E402
from videos import kenburns  # noqa: E402
from reel_producto import tramo  # noqa: E402
from publicaciones import check, texto_centrado, PAPEL, TINTA, SALVIA, GRIS, ROSA, TIT, TIT_I, MARCA, TXT, TXT_B  # noqa: E402
import imageio_ffmpeg  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
W, H = S

TXT_ = {'a': [('POV: el regalo perfecto', 'b'), ('para quien adora a su perro', 'b')],
        'b': [('Con su nombre, su carácter', 'b'), ('y su frase', 'b')],
        'c': [('Hecho a partir de', 'b'), ('sus fotos del móvil', 'b')]}


def escena_ia(ruta, x0=972, ancho=1000):
    """Clip horizontal de la IA → ventana 4:5 a todo el ancho, con la misma escena difuminada arriba y abajo."""
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24')
    meta = next(gen)
    w, h = meta['size']
    fps = meta.get('fps') or 24
    frames = []
    for f in gen:
        im = Image.frombytes('RGB', (w, h), f).crop((x0, 0, x0 + ancho, h))
        fondo = ImageOps.fit(im, S, Image.BILINEAR).filter(ImageFilter.GaussianBlur(28))
        alto = round(W * im.height / im.width)
        fondo.paste(im.resize((W, alto), Image.LANCZOS), (0, (H - alto) // 2 + 60))
        frames.append(fondo)
    return lambda tl: frames[min(int(tl * fps), len(frames) - 1)], len(frames) / fps


def cierre():
    im = Image.new('RGB', S, PAPEL)
    d = ImageDraw.Draw(im)
    d.text((W / 2, 480), 'Kivoa', font=MARCA(170), fill=SALVIA, anchor='ms')
    d.line((W / 2 - 80, 550, W / 2 + 80, 550), fill=ROSA, width=5)
    y = texto_centrado(d, ['El regalo que', 'no esperan'], 730, TIT(118), TINTA, 138)
    y += 120
    for p in ['Vista previa en 48 h', 'No pagas hasta aprobarla', 'Navidad: pide antes del 1/12']:
        check(d, 170, y - 18, r=34)
        d.text((234, y), p, font=TXT(60), fill=TINTA, anchor='ls')
        y += 118
    f = TXT_B(52)
    cta = 'Enlace en el perfil'
    w = d.textlength(cta, font=f) + 150
    d.rounded_rectangle((W / 2 - w / 2, y + 40, W / 2 + w / 2, y + 160), 60, fill=SALVIA)
    d.text((W / 2, y + 102), cta, font=f, fill='white', anchor='mm')
    return im


def montar(caso, compuesto, video, desde):
    ia, dur = escena_ia(compuesto)
    ret = Image.open(os.path.join(RAIZ, 'assets', 'casos', caso, 'retrato-clasico-es.jpg')).convert('RGB')
    # el retrato entero en 9:16 (papel arriba y abajo) para que al alejar se lean todos los rasgos
    alto = round(ret.width * 16 / 9)
    papel = Image.new('RGB', (ret.width, alto), ret.getpixel((20, ret.height - 20)))
    papel.paste(ret, (0, (alto - ret.height) // 2))
    ret = papel
    anda = tramo(video, float(desde), 2.4)
    fin = cierre()
    rot = lambda k: [(TXT_[k], ARR, 0, 1)]
    render(f'reel-regalo-{caso}-es.mp4', [
        (dur, lambda tl, x: ia(tl), rot('a')),
        (3.0, lambda tl, x: kenburns(ret, S, x, 1.9, 1.0, (.6, .38), (.5, .5)), rot('b')),
        (2.4, lambda tl, x: anda(tl), rot('c')),
        (3.4, lambda tl, x: fin, []),
    ])


if __name__ == '__main__':
    montar(*sys.argv[1:5])
