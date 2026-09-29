"""Banner del canal de YouTube (2560×1440). Todo lo importante dentro de la zona segura 1546×423 centrada
(x 507–2053, y 508–931), que es lo único que se ve en el móvil; el resto solo se ve en tele/ordenador.

Uso: python3 generador/banner_youtube.py  → assets/redes/perfiles/youtube-banner.jpg
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'casos'))
from caso_real import marco  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FU = lambda n, s: ImageFont.truetype(os.path.join(RAIZ, 'generador', 'fuentes', n), s)
W, H = 2560, 1440
PAPEL, SALVIA, TINTA, GRIS = (246, 242, 236), (63, 81, 72), (44, 51, 47), (80, 86, 85)
SX0, SX1, SY0, SY1 = 507, 2053, 508, 931
CORTE = 1400  # donde empieza la escena del salón


def banner(salida):
    im = Image.new('RGB', (W, H), PAPEL)
    # retratos enmarcados (sin IA): la cara de cada uno cae dentro de la zona segura
    d = ImageDraw.Draw(im)
    d.rectangle((CORTE - 40, 1180, W, H), fill=(226, 212, 192))       # balda
    d.rectangle((CORTE - 40, 1180, W, 1196), fill=(236, 226, 210))
    miau = Image.open(os.path.join(RAIZ, 'assets', 'casos', 'miau', 'retrato-lavanda-en.jpg')).convert('RGB')
    luna = Image.open(os.path.join(RAIZ, 'assets', 'despues-retrato-luna-v2.webp')).convert('RGB')
    marco(im, miau, (1470, 250, 1470 + 620, 250 + 900), (196, 150, 102), True)
    marco(im, luna, (2170, 640, 2170 + 360, 640 + 520), (250, 250, 248))
    d = ImageDraw.Draw(im)
    cx = (SX0 + CORTE) / 2 + 10
    d.text((cx, 600), 'Kivoa', font=FU('Trirong-Light.ttf', 150), fill=SALVIA, anchor='mm')
    d.text((cx, 735), 'Su retrato, para siempre en tu pared', font=FU('Trirong-LightItalic.ttf', 50), fill=TINTA, anchor='mm')
    d.text((cx, 805), 'Their portrait, forever on your wall', font=FU('QuattrocentoSans-Italic.ttf', 40), fill=GRIS, anchor='mm')
    d.line((cx - 60, 858, cx + 60, 858), fill=(216, 167, 160), width=3)  # único acento rosa
    d.text((cx, 895), 'CUSTOM PET PORTRAITS  ·  RETRATOS DE MASCOTAS', font=FU('QuattrocentoSans-Regular.ttf', 26),
           fill=GRIS, anchor='mm')
    im.save(salida, quality=90, optimize=True)
    # comprobación: lo que se ve en el móvil
    im.crop((SX0, SY0, SX1, SY1)).save(salida.replace('.jpg', '-movil.jpg'), quality=85)
    print(salida, os.path.getsize(salida) // 1024, 'KB')


if __name__ == '__main__':
    banner(os.path.join(RAIZ, 'assets', 'redes', 'perfiles', 'youtube-banner.jpg'))
