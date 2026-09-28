"""TikTok "revelación" (~12 s, 1080×1920): gancho → caja tapada → revelación en la caja → detalle → reacción → pared.

Uso:
  python3 generador/video/tiktok_revelacion.py CLIP_GANCHO CLIP_REACCION CASO ESTILO
  p. ej.: … clip1.mp4 clip4.mp4 miau lavanda

- Los clips de la mascota vienen de la IA de vídeo; el retrato NUNCA pasa por la IA (se anima aquí, idéntico al impreso).
- Salida en assets/videos/: tiktok-<caso>-{en,es,sin-texto}.mp4, sin audio (la música se pone en TikTok).
"""
import os, subprocess, sys
import imageio_ffmpeg
from PIL import Image, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
from videos import kenburns, texto, ease, FPS, SALIDA  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)
S = (1080, 1920)
ARR, ABA = 250, 1300

TXT = {
    'en': {'gancho': [('My cat has no idea', 'b'), ('what I did…', 'b')], 'tapado': [('(don\'t tell him)', 'i')],
           'rasgos': [('Every feature,', 'b'), ('just as he is', 'b')], 'reaccion': [('His reaction:', 'b')],
           'cta': [('Want one of yours?', 'b'), ('Link in bio', 'i')]},
    'es': {'gancho': [('Mi gato no sabe', 'b'), ('lo que le he hecho…', 'b')], 'tapado': [('(no se lo digáis)', 'i')],
           'rasgos': [('Con cada rasgo,', 'b'), ('tal cual es', 'b')], 'reaccion': [('Su reacción:', 'b')],
           'cta': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
}

# cara/ojos en el retrato (fracciones) para el zoom de la revelación
OJOS = {'miau': (.67, .37)}


def leer_clip(ruta, fx=.5):
    """Fotogramas del clip recortados a 9:16 centrados en fx (0–1) y escalados a 1080×1920.
    Hailuo entrega 2944×1248 aunque se pida vertical: el recorte central deja fuera su marca de agua."""
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24')
    meta = next(gen)
    w, h = meta['size']
    fps = meta.get('fps') or 24
    frames = [ImageOps.fit(Image.frombytes('RGB', (w, h), f), S, Image.LANCZOS, centering=(fx, .5)) for f in gen]
    return frames, fps


def de_clip(frames, fps, desde=0.0):
    def f(t_abs):
        i = min(int((desde + t_abs) * fps), len(frames) - 1)
        return frames[i]
    return f


def render(nombre, escenas):
    ruta = os.path.join(SALIDA, nombre)
    total = sum(e[0] for e in escenas)
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{S[0]}x{S[1]}', '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'slow',
           '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', ruta]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = 0.0
    for dur, fn, rot in escenas:  # cortes secos, sin fundidos: en TikTok el ritmo retiene
        for k in range(int(round(dur * FPS))):
            tl = k / FPS
            im = fn(tl, tl / dur)
            for lineas, y, a0, a1 in rot:
                x = tl / dur
                if a0 <= x <= a1:
                    im = texto(im, lineas, y, min(1, ease((x - a0) / .08)), tam=84)
            p.stdin.write(im.convert('RGB').tobytes())
        t0 += dur
    p.stdin.close()
    p.wait()
    print(ruta, f'{total:.1f} s', f'{os.path.getsize(ruta) / 1e6:.1f} MB')


# centro horizontal del gato en cada clip y segundo desde el que se usa
CLIPS = {'miau': {'gancho': (.49, .3), 'reaccion': (.53, .5)}}


def montar(clip_gancho, clip_reaccion, caso, estilo, idiomas='en,es,sin-texto'):
    """Gancho → caja tapada → revelación en la caja → detalle → reacción → cuadro en la pared.
    Las maquetas (caja, salón) salen de generador/mockups.py con el retrato real."""
    os.makedirs(SALIDA, exist_ok=True)
    cg, cr = CLIPS.get(caso, {}).get('gancho', (.5, .3)), CLIPS.get(caso, {}).get('reaccion', (.5, .5))
    g, gfps = leer_clip(clip_gancho, cg[0])
    r, rfps = leer_clip(clip_reaccion, cr[0])
    ret = Image.open(C(caso, f'retrato-{estilo}.jpg')).convert('RGB')
    caja = Image.open(C(caso, f'mockup-{estilo}-caja.jpg')).convert('RGB')
    salon = Image.open(C(caso, f'mockup-{estilo}-salon.jpg')).convert('RGB')
    ox, oy = OJOS.get(caso, (.5, .35))
    gancho, reaccion = de_clip(g, gfps, cg[1]), de_clip(r, rfps, cr[1])
    CX = (.504, .5)  # centro de la lámina en la maqueta de la caja
    tapada = kenburns(caja, S, 0, 1.0, 1.0, CX, CX).filter(ImageFilter.GaussianBlur(30))

    def revelar(tl, x):  # el desenfoque se va en ~0,5 s y la cámara se acerca despacio
        nitido = kenburns(caja, S, x, 1.0, 1.1, CX, (.52, .42))
        k = ease(x / .2)
        return nitido if k >= 1 else nitido.filter(ImageFilter.GaussianBlur(30 * (1 - k)))

    for lang in idiomas.split(','):
        T = TXT.get(lang)
        rot = (lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]) if T else (lambda *a, **k: [])
        render(f'tiktok-{caso}-{lang}.mp4', [
            (2.2, lambda tl, x: gancho(tl), rot('gancho', ARR, 0, 1)),
            (1.2, lambda tl, x: tapada, rot('tapado', ABA, .1, 1)),
            (2.4, revelar, []),  # sin texto: el producto se ve entero
            (1.8, lambda tl, x: kenburns(ret, S, x, 1.35, 1.75, (.6, .36), (ox - .05, oy)), rot('rasgos', ARR, .1, 1)),
            (1.8, lambda tl, x: reaccion(tl), rot('reaccion', ARR, 0, 1)),
            (2.4, lambda tl, x: kenburns(salon, S, x, 1.35, 1.02, (.51, .36), (.51, .42)), rot('cta', ABA, .25, 1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:6])  # 5.º argumento opcional: idiomas, p. ej. 'en,sin-texto' con el retrato en inglés
