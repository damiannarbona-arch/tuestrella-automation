"""Vídeo de producto para la ficha de la web (4:5, 1080×1350, ~13 s, sin texto ni audio).

Uso:
  python3 generador/video/video_producto.py miau lavanda
  → assets/videos/producto-<caso>-<estilo>.mp4

Secuencia: foto real → retrato → en la caja de regalo → en la pared → detalle de la cara → tamaños.
Todo sale del retrato real (maquetas de generador/mockups.py), sin IA de vídeo.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from videos import kenburns, sobre_papel, render, abrir  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = lambda caso, *p: os.path.join(RAIZ, 'assets', 'casos', caso, *p)
S = (1080, 1350)


def video(caso, estilo):
    foto = abrir(C(caso, 'foto-principal.jpg'))
    ret = abrir(C(caso, f'retrato-{estilo}.jpg'))
    caja = abrir(C(caso, f'mockup-{estilo}-caja.jpg'))
    salon = abrir(C(caso, f'mockup-{estilo}-salon.jpg'))
    tam = abrir(C(caso, 'anuncio', f'{estilo}-5-tamanos.jpg')).crop((180, 380, 2220, 1680))  # solo marcos y medidas
    render(f'producto-{caso}-{estilo}.mp4', S, [
        (2.2, lambda t: kenburns(foto, S, t, 1.0, 1.08, (.5, .45), (.52, .42)), []),
        (2.6, lambda t: sobre_papel(ret, S, .9, t, (1.0, 1.05)), []),
        (2.6, lambda t: kenburns(caja, S, t, 1.0, 1.12, (.5, .5), (.52, .45)), []),
        (2.6, lambda t: kenburns(salon, S, t, 1.9, 1.35, (.51, .36), (.51, .38)), []),
        (2.0, lambda t: kenburns(ret, S, t, 1.5, 1.9, (.6, .36), (.62, .37)), []),
        (2.4, lambda t: sobre_papel(tam, S, .62, t, (1.0, 1.03), sombra=False), []),
    ], fundido=.6)


if __name__ == '__main__':
    video(*sys.argv[1:3])
