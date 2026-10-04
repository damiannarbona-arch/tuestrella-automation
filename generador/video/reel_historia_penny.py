"""Reel "historia" de Penny (1080×1920, ≤15 s). El cuadro no se ve hasta el final:
gancho sobre el cuadro difuminado → Penny en el campo → sus fotos pasando rápido (polaroids pequeñas)
→ "querían un cuadro personalizado, no uno cualquiera" (detalle de rasgos y frase) → vista previa por mensaje en el móvil, aprobada → el cuadro en casa → información de Kivoa sin imagen.

Uso: python3 generador/video/reel_historia_penny.py [idiomas]      (es por defecto)
Sin audio: la música se pone en la app.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'redes'))
from tiktok_revelacion import render, S, ARR  # noqa: E402
from videos import kenburns, ease  # noqa: E402
from publicaciones import (polaroid, check, boton, texto_centrado, PAPEL, TINTA, SALVIA, GRIS, ROSA,  # noqa: E402
                           TIT, TIT_I, MARCA, TXT, TXT_B)

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *p: os.path.join(RAIZ, 'assets', 'casos', 'penny', *p)
W, H = S

TXT_ = {
    'es': {'a': [('¿Has perdido a', 'b'), ('tu mascota, o conoces', 'b'), ('a alguien que sí?', 'b')],
           'b': [('Quédate y te cuento', 'b'), ('la historia de Penny', 'b')],
           'c': [('Su familia nos envió', 'b'), ('sus fotos favoritas', 'b')],
           'p': [('Querían un cuadro', 'b'), ('personalizado,', 'b'), ('no uno cualquiera', 'i')],
           'd': [('En 48 h recibieron', 'b'), ('su vista previa…', 'b'), ('…y la aprobaron', 'i')],
           'e': [('Unos días después,', 'b'), ('sigue junto a ellos', 'b'), ('en casa', 'i')],
           'chat': ('Kivoa', 'en línea', '¡Aquí tenéis a Penny!', '¿Queréis cambiar algo?', '¡Es ella! Adelante'),
           'info': (['Su recuerdo,', 'para siempre'], 'Retratos ilustrados de tu mascota',
                    ['Envíanos sus fotos', 'Vista previa en 48 h', 'No pagas hasta aprobarla'], 'Enlace en el perfil')},
}


def papel():
    return Image.new('RGBA', S, PAPEL + (255,))


def apaisada(foto):
    """Foto horizontal entera en vertical: la foto a todo el ancho sobre una versión ampliada y difuminada de sí misma."""
    fondo = ImageOps.fit(foto, S, Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
    h = round(W * foto.height / foto.width)
    fondo.paste(foto.resize((W, h), Image.LANCZOS), (0, (H - h) // 2 + 120))
    return fondo


def fotos_pasando(fotos):
    """Polaroids pequeñas que caen una encima de otra: se ven las fotos sin detenerse en las caras."""
    pos = [((400, 980), -7), ((680, 1120), 6), ((420, 1300), 3), ((650, 1000), -4)]
    etapas, im = [], papel()
    for foto, (c, a) in zip(fotos, pos):
        polaroid(im, foto, c, 640, a, foco=(.5, .5))
        etapas.append(im.copy())
    return etapas


def movil(previa, T, respuesta):
    """Chat en el móvil con la vista previa; con respuesta=True aparece la aprobación del cliente."""
    im = papel()
    d = ImageDraw.Draw(im)
    pw, ph = 720, 1300
    px, py = (W - pw) // 2, 560
    sombra = Image.new('RGBA', S, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((px + 10, py + 24, px + pw + 10, py + ph + 24), 96, fill=(40, 30, 20, 80))
    im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(26)))
    d.rounded_rectangle((px, py, px + pw, py + ph), 96, fill=(30, 32, 34))
    m = 22
    x0, y0, x1, y1 = px + m, py + m, px + pw - m, py + ph - m
    d.rounded_rectangle((x0, y0, x1, y1), 78, fill=(250, 249, 246))
    nombre, estado, msg, pregunta, ok = T['chat']
    d.line((x0, y0 + 150, x1, y0 + 150), fill=(225, 220, 212), width=3)
    d.ellipse((x0 + 34, y0 + 70, x0 + 104, y0 + 140), fill=SALVIA)
    d.text((x0 + 69, y0 + 105), 'K', font=MARCA(40), fill='white', anchor='mm')
    d.text((x0 + 124, y0 + 92), nombre, font=TXT_B(36), fill=TINTA, anchor='lm')
    d.text((x0 + 124, y0 + 126), estado, font=TXT(24), fill=GRIS, anchor='lm')
    bx0, by0, bx1 = x0 + 30, y0 + 180, x1 - 90
    rw = bx1 - bx0 - 40
    rh = round(rw * previa.height / previa.width)
    d.rounded_rectangle((bx0, by0, bx1, by0 + rh + 150), 30, fill=(236, 232, 224))
    d.text((bx0 + 20, by0 + 22), msg, font=TXT(30), fill=TINTA)
    im.paste(previa.resize((rw, rh), Image.LANCZOS), (bx0 + 20, by0 + 70))
    d.text((bx0 + 20, by0 + 84 + rh), pregunta, font=TXT(28), fill=GRIS)
    if respuesta:
        f = TXT_B(32)
        tw = d.textlength(ok, font=f)
        ry = by0 + rh + 175
        d.rounded_rectangle((x1 - 30 - tw - 60, ry, x1 - 30, ry + 76), 38, fill=SALVIA)
        d.text((x1 - 30 - tw - 30, ry + 38), ok, font=f, fill='white', anchor='lm')
    return im


def info(T):
    titular, sub, puntos, cta = T['info']
    im = papel()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 470), 'Kivoa', font=MARCA(170), fill=SALVIA, anchor='ms')
    d.line((W / 2 - 80, 540, W / 2 + 80, 540), fill=ROSA, width=5)
    y = texto_centrado(d, titular, 720, TIT(128), TINTA, 148)
    d.text((W / 2, y + 10), sub, font=TIT_I(62), fill=GRIS, anchor='ms')
    y += 190
    for p in puntos:
        check(d, 190, y - 18, r=34)
        d.text((254, y), p, font=TXT(64), fill=TINTA, anchor='ls')
        y += 120
    f = TXT_B(52)
    w = d.textlength(cta, font=f) + 150
    d.rounded_rectangle((W / 2 - w / 2, y + 40, W / 2 + w / 2, y + 160), 60, fill=SALVIA)
    d.text((W / 2, y + 102), cta, font=f, fill='white', anchor='mm')
    return im


def montar(idiomas='es'):
    abrir = lambda p: ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    noche, casa, campo = abrir(P('producto-real', 'lampara-83.jpg')), abrir(P('producto-real', 'web-principal.jpg')), abrir(P('foto-paisaje.jpg'))
    campo_v = apaisada(campo)
    previa, diseno = abrir(P('vista-previa-rosa.jpg')), abrir(P('retrato-rosa.jpg'))
    tapado = noche.filter(ImageFilter.GaussianBlur(26))
    fotos = [abrir(P(f'familia-{i}.jpg')) for i in (1, 2, 3)] + [campo]
    etapas = fotos_pasando(fotos)
    for lang in idiomas.split(','):
        T = TXT_[lang]
        rot = lambda k: [(T[k], ARR, 0, 1)]
        chat = [movil(previa, T, False), movil(previa, T, True)]
        fin = info(T)
        render(f'reel-historia-penny-{lang}.mp4', [
            (2.4, lambda tl, x: kenburns(tapado, S, x, 1.15, 1.3, (.5, .55), (.52, .5)), rot('a')),
            (2.0, lambda tl, x: kenburns(campo_v, S, x, 1.0, 1.06, (.5, .55), (.53, .56)), rot('b')),
            (1.9, lambda tl, x: etapas[min(int(x * 4.6), 3)], rot('c')),
            (2.1, lambda tl, x: kenburns(diseno, S, x, 1.45, 1.2, (.5, .82), (.5, .74)), rot('p')),
            (2.4, lambda tl, x: chat[x > .5], rot('d')),
            (2.2, lambda tl, x: kenburns(casa, S, x, 1.35, 1.0, (.4, .6), (.42, .56)), rot('e')),
            (2.0, lambda tl, x: fin, []),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:2])
