"""Vista previa protegida para enviar al cliente: baja resolución + marca de agua en diagonal.

La vista previa sirve para aprobar el diseño, no para imprimirlo: con 1200 px de lado largo y la marca
repetida por todo el retrato no se puede imprimir con calidad ni recortar la marca sin destrozar el dibujo.
El archivo bueno (alta resolución, sin marca) solo va a Gelato.

Uso: python3 generador/marca_agua.py RETRATO [SALIDA] [--texto "KIVOA · VISTA PREVIA"] [--lado 1200]
     sin SALIDA → <retrato>-vista-previa.jpg al lado del original
"""
import argparse, math, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LETRA = os.path.join(RAIZ, 'generador', 'fuentes', 'QuattrocentoSans-Bold.ttf')


def vista_previa(ruta, salida=None, texto='KIVOA · VISTA PREVIA', lado=1200, opacidad=.34):
    im = ImageOps.exif_transpose(Image.open(ruta)).convert('RGB')
    k = lado / max(im.size)
    if k < 1:
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    W, H = im.size
    tam = max(18, W // 22)
    f = ImageFont.truetype(LETRA, tam)
    # mosaico de la marca en una capa grande, girada 30° y recortada al retrato
    D = int(math.hypot(W, H)) + 2 * tam
    capa = Image.new('L', (D, D), 0)
    d = ImageDraw.Draw(capa)
    paso_x = d.textlength(texto, font=f) + tam * 2.5
    paso_y = tam * 4.2
    for fila, y in enumerate(range(0, D, int(paso_y))):
        x0 = -(fila % 2) * paso_x / 2
        x = x0
        while x < D:
            d.text((x, y), texto, font=f, fill=255)
            x += paso_x
    capa = capa.rotate(30, resample=Image.BICUBIC)
    capa = capa.crop(((D - W) // 2, (D - H) // 2, (D - W) // 2 + W, (D - H) // 2 + H))
    alfa = capa.point(lambda v: int(v * opacidad))
    # blanco con contorno oscuro suave: se ve sobre fondos claros y oscuros
    sombra = capa.point(lambda v: int(v * opacidad * .7))
    im.paste((40, 34, 30), (1, 1), sombra)
    im.paste((255, 255, 255), (0, 0), alfa)
    salida = salida or os.path.splitext(ruta)[0] + '-vista-previa.jpg'
    im.save(salida, quality=80)
    print(salida, im.size)
    return salida


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('retrato'); p.add_argument('salida', nargs='?')
    p.add_argument('--texto', default='KIVOA · VISTA PREVIA'); p.add_argument('--lado', type=int, default=1200)
    a = p.parse_args()
    vista_previa(a.retrato, a.salida, a.texto, a.lado)
