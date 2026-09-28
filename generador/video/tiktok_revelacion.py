"""TikTok "revelación" (10 s, 1080×1920): gancho con la mascota → retrato tapado → revelación → reacción → comparación.

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
           'ojos': [('Even his two', 'b'), ('different eyes', 'b')], 'reaccion': [('His reaction:', 'b')],
           'cta': [('Want one of yours?', 'b'), ('Link in bio', 'i')]},
    'es': {'gancho': [('Mi gato no sabe', 'b'), ('lo que le he hecho…', 'b')], 'tapado': [('(no se lo digáis)', 'i')],
           'ojos': [('Hasta sus ojos', 'b'), ('de distinto color', 'b')], 'reaccion': [('Su reacción:', 'b')],
           'cta': [('¿Hacemos el de tu mascota?', 'b'), ('Enlace en el perfil', 'i')]},
}

# cara/ojos en el retrato (fracciones) para el zoom de la revelación
OJOS = {'miau': (.55, .33)}


def leer_clip(ruta):
    """Fotogramas del clip reescalados y recortados a 1080×1920."""
    gen = imageio_ffmpeg.read_frames(ruta, pix_fmt='rgb24')
    meta = next(gen)
    w, h = meta['size']
    fps = meta.get('fps') or 24
    frames = [ImageOps.fit(Image.frombytes('RGB', (w, h), f), S, Image.LANCZOS) for f in gen]
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


def montar(clip_gancho, clip_reaccion, caso, estilo):
    os.makedirs(SALIDA, exist_ok=True)
    g, gfps = leer_clip(clip_gancho)
    r, rfps = leer_clip(clip_reaccion)
    ret = Image.open(C(caso, f'retrato-{estilo}.jpg')).convert('RGB')
    foto = ImageOps.exif_transpose(Image.open(C(caso, 'foto-principal.jpg'))).convert('RGB')
    ox, oy = OJOS.get(caso, (.5, .35))
    gancho, reaccion = de_clip(g, gfps, .3), de_clip(r, rfps, .5)
    # retrato tapado: muy desenfocado (precalculado)
    tapado_base = kenburns(ret, S, 0, 1.15, 1.15, (.5, .4), (.5, .4)).filter(ImageFilter.GaussianBlur(38))

    def revelar(tl, x):
        nitido = kenburns(ret, S, x, 1.15, 2.4, (.5, .4), (ox, oy))
        k = ease(x / .22)  # el desenfoque se quita en el primer ~0,5 s
        return nitido if k >= 1 else nitido.filter(ImageFilter.GaussianBlur(38 * (1 - k)))

    def comparar(tl, x):
        im = Image.new('RGB', S, (246, 242, 236))
        mitad = (S[0], S[1] // 2)
        z = 1 + .05 * ease(x)
        im.paste(kenburns(foto, mitad, x, 1.0, z, (.52, .42), (.52, .42)), (0, 0))
        im.paste(kenburns(ret, mitad, x, 1.35, 1.35 * z, (.5, .33), (.5, .33)), (0, S[1] // 2))
        return im

    for lang in ('en', 'es', 'sin-texto'):
        T = TXT.get(lang)
        rot = (lambda k, y, a=.0, b=1.0: [(T[k], y, a, b)]) if T else (lambda *a, **k: [])
        render(f'tiktok-{caso}-{lang}.mp4', [
            (2.2, lambda tl, x: gancho(tl), rot('gancho', ARR, 0, 1)),
            (1.3, lambda tl, x: tapado_base, rot('tapado', ABA, .1, 1)),
            (2.5, revelar, rot('ojos', ARR, .3, 1)),
            (2.0, lambda tl, x: reaccion(tl), rot('reaccion', ARR, 0, 1)),
            (2.0, comparar, rot('cta', 880, .15, 1)),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:5])
