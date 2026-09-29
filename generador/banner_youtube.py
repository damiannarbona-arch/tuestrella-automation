"""Banner del canal de YouTube (2560×1440). Todo lo importante dentro de la zona segura 1546×423 centrada
(x 507–2053, y 508–931), que es lo único que se ve en el móvil; el resto solo se ve en tele/ordenador.

Escena: foto de ChatGPT con dos marcos reales y huecos grises (#BDBDBD aprox.), prompt en
generador/prompts/banner-youtube.md. Los retratos NO pasan por la IA: se pegan aquí en los huecos.

Uso: python3 generador/banner_youtube.py  → assets/redes/perfiles/youtube-banner.jpg (+ -movil.jpg)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from scipy import ndimage

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
A = lambda *p: os.path.join(RAIZ, 'assets', *p)
FU = lambda n, s: ImageFont.truetype(os.path.join(RAIZ, 'generador', 'fuentes', n), s)
W, H = 2560, 1440
SALVIA, TINTA, GRIS, ROSA = (63, 81, 72), (44, 51, 47), (80, 86, 85), (216, 167, 160)
SX0, SX1, SY0, SY1 = 507, 2053, 508, 931

ESCENA = A('mockups', 'pared-dos-marcos.webp')
X_ESC, Y_ESC = 400, 200   # posición de la escena escalada: baja 200 px para que la cara caiga en la zona segura
# retratos por hueco, de mayor a menor: (archivo, centrado del recorte)
RETRATOS = [(A('casos', 'miau', 'retrato-lavanda-en.jpg'), (.5, .5)),
            (A('despues-retrato-luna-v2.webp'), (.5, .5))]


def huecos(img):
    """Rectángulos grises planos de la escena, de mayor a menor (x0, y0, x1, y1)."""
    a = np.asarray(img).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (abs(r - g) < 8) & (abs(g - b) < 8) & (r > 160) & (r < 200)
    lab, _ = ndimage.label(m)
    cajas = [(s[1].start, s[0].start, s[1].stop, s[0].stop) for s in ndimage.find_objects(lab)]
    cajas = [c for c in cajas if (c[2] - c[0]) * (c[3] - c[1]) > 20000]
    return sorted(cajas, key=lambda c: -(c[2] - c[0]) * (c[3] - c[1]))


def rellenar(esc):
    for (x0, y0, x1, y1), (ruta, cen) in zip(huecos(esc), RETRATOS):
        x0, y0, x1, y1 = x0 - 1, y0 - 1, x1 + 1, y1 + 1   # tapa el borde suavizado del gris
        ret = ImageOps.fit(Image.open(ruta).convert('RGB'), (x1 - x0, y1 - y0), Image.LANCZOS, centering=cen)
        esc.paste(ret, (x0, y0))
        # sombra muy suave del paspartú sobre la lámina (arriba e izquierda), como en una foto real
        s = Image.new('L', esc.size, 0)
        d = ImageDraw.Draw(s)
        d.rectangle((x0, y0, x1, y0 + 2), fill=70)
        d.rectangle((x0, y0, x0 + 1, y1), fill=45)
        s = s.filter(ImageFilter.GaussianBlur(2))
        esc.paste(Image.new('RGB', esc.size, (60, 50, 40)), (0, 0), s)
    return esc


def banner(salida):
    esc = rellenar(Image.open(ESCENA).convert('RGB'))
    k = H / esc.height * 1.0
    esc = esc.resize((round(esc.width * k), H), Image.LANCZOS)
    im = Image.new('RGB', (W, H))
    # arriba: se prolonga la pared (estirando su primera franja); a la izquierda: se prolonga el borde de la pared
    im.paste(esc.crop((0, 0, esc.width, 4)).resize((esc.width, Y_ESC + 4)), (X_ESC, 0))
    im.paste(esc, (X_ESC, Y_ESC))
    borde = im.crop((X_ESC, 0, X_ESC + 4, H)).resize((X_ESC, H))
    im.paste(borde, (0, 0))
    im = im.crop((0, 0, W, H))

    d = ImageDraw.Draw(im)
    cx = 930
    d.text((cx, 600), 'Kivoa', font=FU('Trirong-Light.ttf', 150), fill=SALVIA, anchor='mm')
    d.text((cx, 735), 'Su retrato, para siempre en tu pared', font=FU('Trirong-LightItalic.ttf', 50), fill=TINTA, anchor='mm')
    d.text((cx, 805), 'Their portrait, forever on your wall', font=FU('QuattrocentoSans-Italic.ttf', 40), fill=GRIS, anchor='mm')
    d.line((cx - 60, 858, cx + 60, 858), fill=ROSA, width=3)  # único acento rosa
    d.text((cx, 895), 'CUSTOM PET PORTRAITS  ·  RETRATOS DE MASCOTAS', font=FU('QuattrocentoSans-Regular.ttf', 26),
           fill=GRIS, anchor='mm')
    im.save(salida, quality=90, optimize=True)
    im.crop((SX0, SY0, SX1, SY1)).save(salida.replace('.jpg', '-movil.jpg'), quality=85)
    print(salida, os.path.getsize(salida) // 1024, 'KB')


if __name__ == '__main__':
    banner(A('redes', 'perfiles', 'youtube-banner.jpg'))
