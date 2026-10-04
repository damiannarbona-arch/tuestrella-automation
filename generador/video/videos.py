"""Vídeos para anuncios de Etsy y redes (Reels / TikTok / Facebook) a partir de assets/.

Uso:
  python3 generador/video/videos.py            # genera todos en assets/videos/
  python3 generador/video/videos.py etsy       # solo el de Etsy
  python3 generador/video/videos.py reels      # solo los verticales

Etsy: 4:3, 1440×1080, 12 s, sin texto (vale para cualquier idioma) y sin audio (Etsy lo silencia).
Redes: 9:16, 1080×1920, 8–10 s, texto dentro de la zona segura (sin tapar la UI de TikTok/Reels).
Música: se añade en la propia app (audio en tendencia); por eso se exportan sin sonido.

Para un estilo distinto de Rosa, pasar sus imágenes en ESTILO (retrato, ambientación y foto original).
"""
import os, subprocess, sys
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = lambda *p: os.path.join(RAIZ, 'assets', *p)
SALIDA = A('videos')
FPS = 30

FONDO = (245, 242, 236)
TINTA = (44, 50, 47)
GRIS = (110, 110, 105)
VERDE = (63, 81, 72)
FD = '/usr/share/fonts/truetype/liberation/'
F = lambda n, s: ImageFont.truetype(FD + n, s)
SERIF, ITAL, BOLD = 'LiberationSerif-Regular.ttf', 'LiberationSerif-Italic.ttf', 'LiberationSerif-Bold.ttf'

ESTILO = {
    'foto': A('antes-foto-luna.jpg'),
    'retrato': A('despues-retrato-luna-v2.webp'),
    'salon': A('banner-salon-luna.webp'),
}


def abrir(p):
    return ImageOps.exif_transpose(Image.open(p)).convert('RGB')


def sin_titulo(img, arriba=.22, abajo=.9):
    """Quita la franja de título de las fotos de Etsy para poner encima el rótulo del vídeo."""
    return img.crop((0, int(img.height * arriba), img.width, int(img.height * abajo)))


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def kenburns(img, size, t, z0=1.0, z1=1.12, c0=(.5, .5), c1=(.5, .5)):
    """Recorte animado (zoom + desplazamiento) de img al tamaño size; t en [0,1]."""
    W, H = size
    e = ease(t)
    z = z0 + (z1 - z0) * e
    cx = c0[0] + (c1[0] - c0[0]) * e
    cy = c0[1] + (c1[1] - c0[1]) * e
    base = max(W / img.width, H / img.height)
    s = base * z
    cw, ch = W / s, H / s
    x = min(max(cx * img.width - cw / 2, 0), img.width - cw)
    y = min(max(cy * img.height - ch / 2, 0), img.height - ch)
    return img.resize(size, Image.LANCZOS, box=(x, y, x + cw, y + ch))


def sobre_papel(img, size, alto_rel=.78, t=0.0, z=(1.0, 1.04), sombra=True):
    """Coloca img entera (p. ej. el retrato) centrada sobre fondo papel, con leve zoom."""
    W, H = size
    k = z[0] + (z[1] - z[0]) * ease(t)
    h = int(H * alto_rel * k)
    w = int(img.width * h / img.height)
    if w > W * .9:
        w = int(W * .9 * k)
        h = int(img.height * w / img.width)
    lienzo = Image.new('RGB', size, FONDO)
    x, y = (W - w) // 2, (H - h) // 2
    if sombra:
        capa = Image.new('RGBA', size, (0, 0, 0, 0))
        ImageDraw.Draw(capa).rectangle((x + 10, y + 16, x + w + 10, y + h + 16), fill=(40, 30, 20, 80))
        capa = capa.filter(ImageFilter.GaussianBlur(22))
        lienzo.paste(capa, (0, 0), capa)
    lienzo.paste(img.resize((w, h), Image.LANCZOS), (x, y))
    return lienzo


# Estilo de los rótulos: 'tiktok' = letra nativa de TikTok (TikTok Sans seminegrita, blanca con contorno negro,
# sin caja), la que llevan los vídeos virales; 'pastilla' = el rótulo antiguo en pastilla clara.
ESTILO_TEXTO = 'tiktok'
TIKTOK_SANS = os.path.join(RAIZ, 'generador', 'fuentes', 'TikTokSans.ttf')   # Google Fonts, licencia OFL


def fuente_tiktok(tam, peso=600):
    f = ImageFont.truetype(TIKTOK_SANS, tam)
    f.set_variation_by_axes([36, 100, peso, 0])   # tamaño óptico, ancho, peso, inclinación
    return f


def texto_tiktok(frame, lineas, y, alfa=1.0, tam=78):
    """Rótulo al estilo TikTok centrado en x desde y: blanco, contorno negro fino y sombra suave; sin caja.
    Las líneas 'i' (secundarias) van algo más pequeñas."""
    W = frame.width
    t0 = int(tam * .88)
    fuentes = [fuente_tiktok(int(t0 * (.78 if e == 'i' else 1)), 560 if e == 'i' else 640) for _, e in lineas]
    capa = Image.new('RGBA', frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    a = int(255 * alfa)
    yy = y + 20
    for (t, e), f in zip(lineas, fuentes):
        h = int(f.size * 1.22)
        trazo = max(3, f.size // 14)
        d.text((W / 2 + 2, yy + h / 2 + 4), t, font=f, fill=(0, 0, 0, int(a * .35)), anchor='mm',
               stroke_width=trazo, stroke_fill=(0, 0, 0, int(a * .35)))
        d.text((W / 2, yy + h / 2), t, font=f, fill=(255, 255, 255, a), anchor='mm', stroke_width=trazo, stroke_fill=(0, 0, 0, a))
        yy += h
    out = frame.convert('RGBA')
    out.alpha_composite(capa)
    return out.convert('RGB')


def texto(frame, lineas, y, alfa=1.0, tam=78, estilo=None):
    """Rótulo centrado horizontalmente en y. lineas = [(txt, estilo), ...]."""
    if alfa <= 0:
        return frame
    if (estilo or ESTILO_TEXTO) == 'tiktok':
        return texto_tiktok(frame, lineas, y, alfa, tam)
    W = frame.width
    fuentes = [F(BOLD if e == 'b' else ITAL if e == 'i' else SERIF, int(tam * (.62 if e == 'i' else 1))) for _, e in lineas]
    d0 = ImageDraw.Draw(frame)
    cajas = [d0.textbbox((0, 0), t, font=f) for (t, _), f in zip(lineas, fuentes)]
    anchos = [c[2] - c[0] for c in cajas]
    altos = [int(f.size * 1.25) for f in fuentes]
    pw, ph = max(anchos) + 90, sum(altos) + 60
    capa = Image.new('RGBA', frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    a = int(255 * alfa)
    d.rounded_rectangle(((W - pw) / 2, y, (W + pw) / 2, y + ph), 34, fill=FONDO + (int(235 * alfa),))
    yy = y + 30
    for (t, e), f, h in zip(lineas, fuentes, altos):
        d.text((W / 2, yy + h / 2), t, font=f, fill=(GRIS if e == 'i' else TINTA) + (a,), anchor='mm')
        yy += h
    out = frame.convert('RGBA')
    out.alpha_composite(capa)
    return out.convert('RGB')


def render(nombre, size, escenas, fundido=.5):
    """escenas = [(duración_s, fn(t_local_0a1) -> Image, [rótulos])]; fundido cruzado entre escenas."""
    os.makedirs(SALIDA, exist_ok=True)
    ruta = os.path.join(SALIDA, nombre)
    total = sum(e[0] for e in escenas)
    n = int(total * FPS)
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'slow',
           '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', ruta]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    inicios = [sum(e[0] for e in escenas[:i]) for i in range(len(escenas))]

    def cuadro(i, s):
        dur, fn, rot = escenas[i]
        tl = (s - inicios[i]) / dur
        im = fn(min(max(tl, 0), 1))
        for txt, y, t0, t1 in rot:
            a = min(ease((tl - t0) / .12), ease((t1 - tl) / .12)) if t0 <= tl <= t1 else 0
            im = texto(im, txt, y, a)
        return im

    for f in range(n):
        s = f / FPS
        i = max(k for k in range(len(escenas)) if inicios[k] <= s + 1e-9)
        im = cuadro(i, s)
        fin = inicios[i] + escenas[i][0]
        if i + 1 < len(escenas) and s > fin - fundido:
            im = Image.blend(im, cuadro(i + 1, s), ease((s - (fin - fundido)) / fundido))
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()
    print(ruta, f'{total:.0f} s', f'{os.path.getsize(ruta) / 1e6:.1f} MB')


# ---------- Etsy (4:3, sin texto) ----------

def video_etsy(estilo=ESTILO, nombre='etsy-rosa-12s.mp4'):
    S = (1440, 1080)
    foto, ret, salon = abrir(estilo['foto']), abrir(estilo['retrato']), abrir(estilo['salon'])
    marcos, tamanos, previa = abrir(A('etsy', 'foto-marcos.jpg')), abrir(A('etsy', 'foto-tamanos.jpg')), abrir(A('etsy', 'foto-vista-previa.jpg'))
    escenas = [
        (2.4, lambda t: kenburns(salon, S, t, 1.35, 1.12, (.5, .35), (.5, .4)), []),   # cuadro en la pared (gancho)
        (2.0, lambda t: sobre_papel(foto, S, .86, t), []),                              # foto original del móvil
        (2.4, lambda t: sobre_papel(ret, S, .86, t, (1.0, 1.06)), []),                  # retrato resultante
        (1.8, lambda t: kenburns(previa, S, t, 1.0, 1.05), []),                         # vista previa en 48 h
        (1.7, lambda t: kenburns(marcos, S, t, 1.0, 1.05), []),                         # marcos
        (1.7, lambda t: kenburns(salon, S, t, 1.0, 1.08, (.5, .5), (.5, .45)), []),     # cierre en el salón
    ]
    render(nombre, S, escenas)


# ---------- Reels / TikTok (9:16) ----------
# Zona segura: evitar ~250 px arriba y ~420 px abajo (botones, descripción y barra de la app).

TXT = {
    'es': {
        'pov1': [('Le hice esto a mi perra', 'b'), ('con una foto del móvil', '')],
        'pov2': [('Una foto…', 'b')],
        'pov3': [('…un recuerdo para siempre', 'b')],
        'pov4': [('Vista previa en 48 h', 'b'), ('Nada se imprime sin tu OK', 'i')],
        'como0': [('Cómo se hace un retrato', 'b'), ('de tu mascota', 'b')],
        'como1': [('1 · Nos envías tus fotos', 'b')],
        'como2': [('2 · Vista previa en 48 h', 'b'), ('2 rondas de cambios incluidas', 'i')],
        'como3': [('3 · Lo recibes enmarcado', 'b'), ('listo para colgar', 'i')],
        'marc0': [('¿Qué marco elegirías?', 'b')],
        'marc1': [('Blanco · Madera · Negro', 'b')],
        'marc2': [('20×25 · 30×40 · 50×70 cm', 'b')],
        'marc3': [('Pide el tuyo', 'b'), ('Enlace en el perfil', 'i')],
    },
    'en': {
        'pov1': [('POV: you turned your dog\'s', 'b'), ('phone photo into this', 'b')],
        'pov2': [('One photo…', 'b')],
        'pov3': [('…a portrait forever', 'b')],
        'pov4': [('Digital proof in 48h', 'b'), ('Nothing prints without your OK', 'i')],
        'como0': [('How a custom pet', 'b'), ('portrait is made', 'b')],
        'como1': [('1 · Send us your photos', 'b')],
        'como2': [('2 · Proof in 48 hours', 'b'), ('2 rounds of changes included', 'i')],
        'como3': [('3 · Framed & ready to hang', 'b'), ('shipped with tracking', 'i')],
        'marc0': [('Which frame would you pick?', 'b')],
        'marc1': [('White · Wood · Black', 'b')],
        'marc2': [('8×10" · 12×16" · 20×28"', 'b')],
        'marc3': [('Order yours', 'b'), ('Link in bio', 'i')],
    },
}


def reels(estilo=ESTILO):
    S = (1080, 1920)
    foto, ret, salon = abrir(estilo['foto']), abrir(estilo['retrato']), abrir(estilo['salon'])
    marcos, tamanos, previa = abrir(A('etsy', 'foto-marcos.jpg')), abrir(A('etsy', 'foto-tamanos.jpg')), abrir(A('etsy', 'foto-vista-previa.jpg'))
    marcos, tamanos = sin_titulo(marcos), sin_titulo(tamanos)
    ARR, TOPE, ABA = 260, 190, 1330  # alturas de rótulo dentro de la zona segura
    for lang, T in TXT.items():
        # 1 · POV antes → después (8 s): gancho en el 1.er segundo con el resultado, no con la foto
        render(f'reel-{lang}-1-antes-despues-8s.mp4', S, [
            (2.2, lambda t: kenburns(salon, S, t, 1.9, 1.6, (.47, .42), (.47, .42)), [(T['pov1'], ARR, 0, 1)]),
            (1.8, lambda t: kenburns(foto, S, t, 1.0, 1.1, (.6, .55), (.6, .5)), [(T['pov2'], ABA, .05, 1)]),
            (2.2, lambda t: sobre_papel(ret, S, .64, t, (1.0, 1.06)), [(T['pov3'], TOPE, .05, 1)]),
            (1.8, lambda t: kenburns(salon, S, t, 1.6, 1.25, (.47, .42), (.47, .45)), [(T['pov4'], ARR, .05, 1)]),
        ])
        # 2 · Cómo funciona (10 s)
        render(f'reel-{lang}-2-como-funciona-10s.mp4', S, [
            (2.0, lambda t: kenburns(salon, S, t, 1.7, 1.5, (.47, .42), (.47, .42)), [(T['como0'], ARR, 0, 1)]),
            (2.4, lambda t: kenburns(foto, S, t, 1.0, 1.08), [(T['como1'], ABA, .05, 1)]),
            (2.8, lambda t: kenburns(previa, S, t, 1.0, 1.05, (.76, .5), (.76, .52)), [(T['como2'], ARR, .05, 1)]),
            (2.8, lambda t: kenburns(salon, S, t, 1.5, 1.2, (.47, .45), (.47, .45)), [(T['como3'], ARR, .05, 1)]),
        ])
        # 3 · Marcos y tamaños (8 s): pregunta = comentarios = alcance
        render(f'reel-{lang}-3-marcos-8s.mp4', S, [
            (2.0, lambda t: sobre_papel(ret, S, .64, t, (1.0, 1.05)), [(T['marc0'], TOPE, 0, 1)]),
            (2.2, lambda t: kenburns(marcos, S, t, 1.0, 1.06, (.3, .5), (.7, .5)), [(T['marc1'], ARR, .05, 1)]),
            (2.0, lambda t: kenburns(tamanos, S, t, 1.0, 1.06, (.35, .5), (.65, .5)), [(T['marc2'], ARR, .05, 1)]),
            (1.8, lambda t: kenburns(salon, S, t, 1.3, 1.1, (.47, .45), (.47, .45)), [(T['marc3'], ARR, .05, 1)]),
        ])


if __name__ == '__main__':
    que = sys.argv[1] if len(sys.argv) > 1 else 'todo'
    if que in ('todo', 'etsy'):
        video_etsy()
    if que in ('todo', 'reels'):
        reels()
