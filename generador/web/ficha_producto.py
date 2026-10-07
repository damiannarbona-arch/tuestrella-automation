"""Fotos cuadradas (2000×2000) para el carrusel de la ficha de producto, con la paleta de la web.

Orden del carrusel de cada artículo:
  1 frente · 2 tres marcos (rotulada) · 3 detalle → escenas de ChatGPT con el diseño (escenas_ficha.py)
  4 «De sus fotos a su retrato» · 5 «Tu vista previa en 48 h» (este script)
  6 vídeo sin música ni letras
  (marcos_tamanos queda como alternativa dibujada; no va en el carrusel)

Uso:
  python3 generador/web/ficha_producto.py            (genera los 4 artículos)
  python3 generador/web/ficha_producto.py rosa       (solo uno)
→ assets/web/ficha/<estilo>-4-sus-fotos.jpg y -5-vista-previa.jpg
"""
import os, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'casos'))
from caso_real import abrir, polaroid, marco, sombra, flecha, centrado, F, SERIF, ITAL, TINTA, GRIS  # noqa: E402
from fotos_etsy import check, redondear  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from marca_agua import vista_previa as con_marca  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = lambda *p: os.path.join(RAIZ, 'assets', *p)
L = 2000
FONDO = (246, 242, 236)          # #F6F2EC, fondo de la web
SALVIA = (63, 81, 71)            # #3F5147
ARENA = (220, 213, 202)          # #DCD5CA

# artículo → (nombre, retrato terminado, foto principal, fotos extra)
ARTICULOS = {
    'rosa': ('Penny', A('casos/penny/retrato-rosa.jpg'), A('casos/penny/familia-2.jpg'),
             [A('casos/penny/familia-1.jpg'), A('casos/penny/familia-3.jpg'), A('casos/penny/foto-paisaje.jpg')]),
    'clasico': ('Curro', A('casos/curro/retrato-clasico-es.jpg'), A('casos/curro/foto-principal.jpg'),
                [A(f'casos/curro/extra-{i}.jpg') for i in (1, 2, 3)]),
    'lavanda': ('Miau', A('retratos/miau-lavanda.jpg'), A('casos/miau/foto-principal.jpg'),
                [A(f'casos/miau/extra-{i}.jpg') for i in (1, 2, 3)]),
    'aventurero': ('Sonic', A('casos/sonic/retrato-aventurero-es.jpg'), A('casos/sonic/foto-principal.jpg'),
                   [A(f'casos/sonic/extra-{i}.jpg') for i in (1, 2, 3)]),
    # sin caso real todavía: diseño de ejemplo (IA), así que NO lleva «De sus fotos a su retrato»
    'caballos': ('Thor', A('ejemplos-ia/thor/diseno-caballos.webp'), None, []),
}


def lienzo():
    im = Image.new('RGB', (L, L), FONDO)
    return im, ImageDraw.Draw(im)


def cabecera(d, titulo, sub):
    centrado(d, L / 2, 170, titulo, F(SERIF, 104), TINTA)
    centrado(d, L / 2, 270, sub, F(ITAL, 50), GRIS)


def etiqueta(d, x, y, txt):
    """Píldora salvia con texto blanco (la misma que en la web)."""
    f = F(SERIF, 50)
    w = d.textlength(txt, font=f) + 64
    d.rounded_rectangle((x - w / 2, y - 40, x + w / 2, y + 40), radius=40, fill=SALVIA)
    centrado(d, x, y, txt, f, (255, 255, 255))


def sus_fotos(estilo, salida):
    nombre, retrato, principal, extras = ARTICULOS[estilo]
    im, d = lienzo()
    cabecera(d, 'De sus fotos a su retrato', 'Nos envías fotos de tu móvil y las convertimos en su retrato')
    fotos = [abrir(principal)] + [abrir(p) for p in extras]
    for foto, c, a in zip(fotos, [(300, 640), (650, 690), (310, 1080), (660, 1120)], [-5, 4, 3, -4]):
        polaroid(im, foto, c, 330, a)
    d = ImageDraw.Draw(im)
    flecha(d, 880, 1040, 880)
    ret = abrir(retrato)
    rh = 1300
    rw = int(ret.width * rh / ret.height)
    x0, y0 = 1080 + (840 - rw) // 2, 380
    sombra(im, (x0, y0, x0 + rw, y0 + rh), r=6)
    im.paste(ret.resize((rw, rh), Image.LANCZOS), (x0, y0))
    d = ImageDraw.Draw(im)
    centrado(d, 480, 1420, 'Sus fotos', F(SERIF, 60), TINTA)
    centrado(d, 480, 1490, 'la principal + hasta 3 más', F(ITAL, 42), GRIS)
    centrado(d, x0 + rw / 2, 1750, 'Su retrato', F(SERIF, 60), TINTA)
    etiqueta(d, L / 2, 1880, f'Caso real · {nombre}')
    im.save(salida, quality=92)


def marcos_tamanos(estilo, salida):
    nombre, retrato, *_ = ARTICULOS[estilo]
    im, d = lienzo()
    cabecera(d, '3 marcos · 3 tamaños', 'Elige el marco y el tamaño que mejor quede en tu casa')
    d.rectangle((0, 1530, L, L), fill=ARENA)                       # balda
    d.rectangle((0, 1530, L, 1546), fill=(232, 226, 216))
    ret = abrir(retrato)
    base = 1500
    # tamaños a escala real entre sí (20×25, 30×40, 50×70); un marco de cada color
    for (x0, x1, alto), med, col, veta, nom in (((170, 410, 300), '20×25 cm', (250, 250, 248), False, 'Blanco'),
                                              ((560, 920, 480), '30×40 cm', (196, 150, 102), True, 'Madera natural'),
                                              ((1080, 1840, 1060), '50×70 cm', (34, 34, 34), False, 'Negro')):
        marco(im, ret, (x0, base - alto, x1, base), col, veta)
        d = ImageDraw.Draw(im)
        centrado(d, (x0 + x1) / 2, 1640, med, F(SERIF, 60), TINTA)
        centrado(d, (x0 + x1) / 2, 1710, nom, F(ITAL, 44), GRIS)
    etiqueta(d, L / 2, 1860, 'Cualquier marco en cualquier tamaño')
    im.save(salida, quality=92)


def vista_previa(estilo, salida):
    nombre, retrato, *_ = ARTICULOS[estilo]
    im, d = lienzo()
    cabecera(d, 'Tu vista previa en 48 h', 'Antes de imprimir, ves su retrato y lo apruebas tú')
    # puntos a la izquierda
    x, y = 150, 720
    for txt, sub in (('Te la enviamos por mensaje', 'en menos de 48 horas'),
                     ('2 rondas de cambios', 'incluidas en el precio'),
                     ('Nada se imprime', 'sin tu aprobación')):
        check(d, x + 40, y + 40, True, r=44)
        d.text((x + 115, y), txt, font=F(SERIF, 60), fill=TINTA)
        d.text((x + 115, y + 78), sub, font=F(ITAL, 44), fill=GRIS)
        y += 260
    # teléfono a la derecha con la vista previa con marca de agua
    pw, ph = 720, 1440
    px, py = 1150, 440
    sombra(im, (px, py, px + pw, py + ph), r=100, off=(14, 24), alfa=90)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((px, py, px + pw, py + ph), 100, fill=(30, 32, 34))
    m = 24
    sx0, sy0, sx1, sy1 = px + m, py + m, px + pw - m, py + ph - m
    d.rounded_rectangle((sx0, sy0, sx1, sy1), 80, fill=(250, 249, 246))
    d.rounded_rectangle((px + pw / 2 - 100, sy0 + 20, px + pw / 2 + 100, sy0 + 64), 22, fill=(30, 32, 34))
    d.line((sx0, sy0 + 180, sx1, sy0 + 180), fill=(225, 220, 212), width=3)
    d.ellipse((sx0 + 36, sy0 + 100, sx0 + 106, sy0 + 170), fill=SALVIA)
    centrado(d, sx0 + 71, sy0 + 135, 'K', F(SERIF, 42), 'white')
    d.text((sx0 + 128, sy0 + 135), 'Kivoa', font=F(SERIF, 44), fill=TINTA, anchor='lm')
    tmp = os.path.join(os.path.dirname(salida), f'.{estilo}-previa.jpg')
    prev = abrir(con_marca(retrato, tmp, lado=900))
    os.remove(tmp)
    bx0, by0, bx1 = sx0 + 32, sy0 + 220, sx1 - 90
    rw = bx1 - bx0 - 50
    rh = round(rw * prev.height / prev.width)
    prev = prev.resize((rw, rh), Image.LANCZOS)
    d.rounded_rectangle((bx0, by0, bx1, by0 + rh + 170), 32, fill=(236, 232, 224))
    d.text((bx0 + 25, by0 + 24), f'¡La vista previa de {nombre}!', font=F(SERIF, 34), fill=TINTA)
    im.paste(prev, (bx0 + 25, by0 + 80), redondear(prev, 14))
    d.text((bx0 + 25, by0 + 80 + rh + 22), '¿Quieres cambiar algo?', font=F(ITAL, 32), fill=GRIS)
    ry0 = by0 + rh + 205
    txt, f = '¡Me encanta! Adelante', F(SERIF, 36)
    tw = d.textlength(txt, font=f)
    d.rounded_rectangle((sx1 - 32 - tw - 64, ry0, sx1 - 32, ry0 + 84), 42, fill=SALVIA)
    d.text((sx1 - 32 - tw - 32, ry0 + 42), txt, font=f, fill='white', anchor='lm')
    im.save(salida, quality=92)


if __name__ == '__main__':
    out = A('web', 'ficha')
    os.makedirs(out, exist_ok=True)
    for e in (sys.argv[1:] or ARTICULOS):
        if ARTICULOS[e][2]:           # solo con caso real
            sus_fotos(e, os.path.join(out, f'{e}-4-sus-fotos.jpg'))
        vista_previa(e, os.path.join(out, f'{e}-5-vista-previa.jpg'))
        print(e, 'ok')
