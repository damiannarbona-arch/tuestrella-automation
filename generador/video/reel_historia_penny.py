"""Reel "historia" de Penny (1080×1920, ~16 s), solo con fotos (el vídeo de llegada no tiene calidad):
gancho (pregunta) → la historia → sus fotos → el diseño (no un cuadro cualquiera) → vista previa en 48 h
→ en su salón unos días después → llamada.

Uso: python3 generador/video/reel_historia_penny.py [idiomas]      (es por defecto)
Sin audio: la música se pone en la app.
"""
import os, sys
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
from tiktok_revelacion import render, S, ARR  # noqa: E402
from videos import kenburns, sobre_papel  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *p: os.path.join(RAIZ, 'assets', 'casos', 'penny', *p)

TXT = {
    'es': {'a': [('¿Has perdido a', 'b'), ('tu mascota, o conoces', 'b'), ('a alguien que sí?', 'b')],
           'b': [('Quédate y te cuento', 'b'), ('la historia de Penny', 'b')],
           'c': [('Su familia nos mandó', 'b'), ('sus fotos favoritas', 'b')],
           'd': [('No un cuadro cualquiera:', 'b'), ('su cara, su carácter y su frase', 'i')],
           'e': [('En 48 h tenían', 'b'), ('su vista previa', 'b')],
           'f': [('Y unos días después,', 'b'), ('en su salón', 'b')],
           'g': [('¿Hacemos el de', 'b'), ('tu mascota?', 'b'), ('Escríbenos · enlace en el perfil', 'i')]},
}


def montar(idiomas='es'):
    abrir = lambda p: ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    noche, casa = abrir(P('producto-real', 'lampara-83.jpg')), abrir(P('producto-real', 'web-principal.jpg'))
    diseno, previa = abrir(P('retrato-rosa.jpg')), abrir(P('vista-previa-rosa.jpg'))
    for lang in idiomas.split(','):
        T = TXT[lang]
        rot = lambda k: [(T[k], ARR, 0, 1)]
        render(f'reel-historia-penny-{lang}.mp4', [
            (2.8, lambda tl, x: kenburns(noche, S, x, 1.15, 1.4, (.5, .55), (.52, .45)), rot('a')),
            (2.0, lambda tl, x: kenburns(casa, S, x, 1.0, 1.1, (.4, .6), (.4, .58)), rot('b')),
            (2.6, lambda tl, x: kenburns(diseno, S, x, 1.9, 1.9, (.2, .14), (.2, .45)), rot('c')),
            (2.6, lambda tl, x: kenburns(diseno, S, x, 1.6, 1.05, (.6, .35), (.5, .55)), rot('d')),
            (2.2, lambda tl, x: sobre_papel(previa, S, .72, x), rot('e')),
            (2.4, lambda tl, x: kenburns(casa, S, x, 1.25, 1.0, (.4, .62), (.42, .56)), rot('f')),
            (2.4, lambda tl, x: kenburns(noche, S, x, 1.0, 1.08, (.5, .6), (.5, .6)), rot('g')),
        ])


if __name__ == '__main__':
    montar(*sys.argv[1:2])
