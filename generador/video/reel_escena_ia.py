"""Reel híbrido de intriga (1080×1920, ≤15 s), para contenido diario sin casos nuevos:
escena de IA con el marco quieto (etiquetar como IA) y el retrato REAL encajado → detalle del retrato → vídeo real
de la mascota (si lo hay) → cierre de Kivoa.

Uso: python3 generador/video/reel_escena_ia.py ESCENA CASO RETRATO [VIDEO_MASCOTA DESDE] [--gancho N]
  p. ej. … salon-oscuro ricky retrato-clasico-es.jpg assets/casos/ricky/video-ventana.mp4 0
- ESCENA: carpeta de assets/ia/ con hailuo-1.mp4. Se compone (generador/video/componer_marco.py) en
  assets/ia/<escena>/<caso>-compuesto.mp4 si no existe.
"""
import argparse, os, sys
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'redes'))
from tiktok_revelacion import render, S, ARR  # noqa: E402
from videos import kenburns  # noqa: E402
from reel_producto import tramo  # noqa: E402
from componer_marco import componer  # noqa: E402
from publicaciones import check, texto_centrado, PAPEL, TINTA, SALVIA, ROSA, TIT, MARCA, TXT, TXT_B  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
W, H = S

GANCHOS = [
    [('Espera a ver quién', 'b'), ('está en el cuadro…', 'b')],
    [('¿Adivinas la raza antes', 'b'), ('de verle la cara?', 'b')],
    [('Lo que hay en este marco', 'b'), ('no es una foto…', 'b')],
    [('POV: el regalo que va a', 'b'), ('abrir tu madre en Navidad', 'b')],
]


def escena(ruta):
    """Clip horizontal de Hailuo (2944×1248) → 9:16 a pantalla completa centrado en el marco (el gris)."""
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24')
    meta = next(gen)
    w, h = meta['size']
    fps = meta.get('fps') or 24
    crudos = [f for f in gen]
    import numpy as np
    from componer_marco import mascara_gris
    ult = np.frombuffer(crudos[-1], np.uint8).reshape(h, w, 3)
    m = mascara_gris(ult)
    cx = int(np.nonzero(m)[1].mean()) if m is not None else w // 2
    cw = round(h * 9 / 16)
    x0 = min(max(cx - cw // 2, 0), w - cw)
    frames = [Image.frombytes('RGB', (w, h), f).crop((x0, 0, x0 + cw, h)).resize(S, Image.LANCZOS) for f in crudos]
    return lambda tl: frames[min(int(tl * fps), len(frames) - 1)], len(frames) / fps


def cinemagraph(ruta, dur=5.0, fps=30, zoom=(1.0, 1.1), centro=(.55, .6)):
    """Foto fija hecha vídeo sin IA: empieza desenfocada y enfoca (intriga), acercamiento lento de cámara y las
    luces (puntos brillantes cálidos) parpadeando cada una a su ritmo. Nada se deforma: el retrato es el de la foto."""
    import numpy as np
    from scipy import ndimage
    im = Image.open(ruta).convert('RGB')
    k = max(S[0] / im.width, S[1] / im.height) * 1.12
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    lum = a.mean(2)
    calido = (a[..., 0] > a[..., 2] + 25)
    luces = np.clip((lum - 170) / 60, 0, 1) * calido
    lab, n = ndimage.label(luces > .15)
    rng = np.random.default_rng(3)
    fase, vel = rng.uniform(0, 6.28, n + 1), rng.uniform(1.5, 4.0, n + 1)
    halo = ndimage.gaussian_filter(luces, 6)
    color = np.array([255, 196, 120], np.float32)
    def frame(tl):
        x = tl / dur
        f = .5 + .5 * np.sin(fase * 1.0 + vel * tl * 2)
        mod = f[lab] * (lab > 0)
        mod = ndimage.gaussian_filter(mod.astype(np.float32), 4)
        b = a + (halo * (mod - .5) * 70)[..., None] * (color / 255)
        img = Image.fromarray(np.clip(b, 0, 255).astype(np.uint8))
        out = kenburns(img, S, x, zoom[0], zoom[1], centro, centro)
        sigma = 14 * max(0.0, 1 - x / .5) ** 1.6     # empieza desenfocado y enfoca a mitad de plano (intriga)
        return out.filter(ImageFilter.GaussianBlur(sigma)) if sigma > .3 else out
    return frame


def cierre():
    im = Image.new('RGB', S, PAPEL)
    d = ImageDraw.Draw(im)
    d.text((W / 2, 480), 'Kivoa', font=MARCA(170), fill=SALVIA, anchor='ms')
    d.line((W / 2 - 80, 550, W / 2 + 80, 550), fill=ROSA, width=5)
    y = texto_centrado(d, ['Un cuadro personalizado,', 'no uno cualquiera'], 720, TIT(84), TINTA, 104)
    y += 110
    for p in ['A partir de sus fotos del móvil', 'Vista previa en 48 h', 'Navidad: pide antes del 1/12']:
        check(d, 170, y - 18, r=34)
        d.text((234, y), p, font=TXT(58), fill=TINTA, anchor='ls')
        y += 112
    f = TXT_B(52)
    cta = 'Enlace en el perfil'
    w = d.textlength(cta, font=f) + 150
    d.rounded_rectangle((W / 2 - w / 2, y + 40, W / 2 + w / 2, y + 160), 60, fill=SALVIA)
    d.text((W / 2, y + 102), cta, font=f, fill='white', anchor='mm')
    return im


def montar(esc, caso, retrato, video=None, desde=0.0, gancho=0, imagen=None, ejemplo=False, fotos=None):
    carpeta = os.path.join(RAIZ, 'assets', 'ia', esc)
    ruta_ret = retrato if os.path.exists(retrato) else os.path.join(RAIZ, 'assets', 'casos', caso, retrato)
    comp = os.path.join(carpeta, f'{caso}-compuesto.mp4')
    if not imagen and not os.path.exists(comp):
        componer(os.path.join(carpeta, 'hailuo-1.mp4'), ruta_ret, comp)
    if imagen:
        dur = 5.0
        ia = cinemagraph(imagen, dur)
    else:
        ia, dur = escena(comp)
    ret = Image.open(ruta_ret).convert('RGB')
    alto = round(ret.width * 16 / 9)
    papel = Image.new('RGB', (ret.width, alto), ret.getpixel((20, ret.height - 20)))
    papel.paste(ret, (0, (alto - ret.height) // 2))
    nombre = caso.capitalize()
    escenas = [(dur, lambda tl, x: ia(tl), [(GANCHOS[gancho], ARR, 0, .45)])]
    if fotos:   # sus fotos, rápidas, una detrás de otra
        imgs = [ImageOps.exif_transpose(Image.open(f)).convert('RGB') for f in fotos]
        paso = .5
        escenas.append((paso * len(imgs), lambda tl, x: kenburns(imgs[min(int(tl / paso), len(imgs) - 1)], S,
                                                                   (tl / paso) % 1, 1.05, 1.15, (.5, .42), (.5, .4)),
                        [([('A partir de unas fotos', 'b'), ('de su móvil', 'b')], ARR, 0, 1)]))
    escenas += [
        (2.8, lambda tl, x: kenburns(papel, S, x, 1.9, 1.0, (.6, .38), (.5, .5)),
         [([(f'Es {nombre}', 'b'), ('con su carácter y su frase', 'i')], ARR, 0, 1)]
         + ([([('Ejemplo de estilo · creado con IA', 'i')], 1700, 0, 1)] if ejemplo else [])),
    ]
    if video:
        clip = tramo(video, float(desde), 2.2)
        escenas.append((2.2, lambda tl, x: clip(tl), [([('Hecho a partir de', 'b'), ('sus fotos del móvil', 'b')], ARR, 0, 1)]))
    fin = cierre()
    escenas.append((3.0, lambda tl, x: fin, []))
    render(f'reel-{esc}-{caso}' + ('-foto' if imagen else '') + '-es.mp4', escenas)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('escena'); ap.add_argument('caso'); ap.add_argument('retrato')
    ap.add_argument('video', nargs='?'); ap.add_argument('desde', nargs='?', default=0)
    ap.add_argument('--gancho', type=int, default=0)
    ap.add_argument('--fotos', nargs='+', help='sus fotos, que pasan rápidas tras la escena')
    ap.add_argument('--ejemplo', action='store_true', help='mascota creada con IA: rótulo "Ejemplo de estilo · creado con IA"')
    ap.add_argument('--imagen', help='foto fija con el retrato ya encajado (marco_en_imagen.py): vídeo sin IA')
    a = ap.parse_args()
    montar(a.escena, a.caso, a.retrato, a.video, a.desde, a.gancho, a.imagen, a.ejemplo, a.fotos)
