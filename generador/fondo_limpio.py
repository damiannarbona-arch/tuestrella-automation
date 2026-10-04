"""Limpia el fondo de una foto de mascota: borra a las personas y difumina el fondo (efecto "modo retrato").

1. Recorta a la(s) mascota(s) con rembg (birefnet-general-lite: respeta las orejas delante de una persona) y a las personas con u2net_human_seg.
2. Rellena el hueco de la persona con cv2.inpaint, a baja resolución, y difumina todo el fondo
   (el difuminado esconde las marcas del relleno y centra la mirada en la mascota).
3. Pega la mascota nítida encima, con el borde suavizado.

Uso: python3 generador/fondo_limpio.py FOTO [SALIDA] [--blur 14] [--sin-persona]
     sin SALIDA → <foto>-limpia.jpg
"""
import argparse, os
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from rembg import new_session, remove

_SES = {}


def mascara(im, modelo):
    if modelo not in _SES:
        _SES[modelo] = new_session(modelo)
    return remove(im, session=_SES[modelo], only_mask=True, post_process_mask=True)


def limpiar(ruta, salida=None, blur=14, quitar_persona=True):
    im = ImageOps.exif_transpose(Image.open(ruta)).convert('RGB')
    perro = mascara(im, 'birefnet-general-lite')
    fondo = np.array(im)
    if quitar_persona:
        persona = np.array(mascara(im, 'u2net_human_seg'))
        persona[np.array(perro) > 128] = 0                         # nunca borrar al perro
        persona = cv2.dilate((persona > 60).astype(np.uint8) * 255, np.ones((41, 41), np.uint8))
        k = 4                                                      # relleno a 1/4: más rápido y más suave
        peq = cv2.resize(fondo, None, fx=1 / k, fy=1 / k, interpolation=cv2.INTER_AREA)
        mp = cv2.resize(persona, (peq.shape[1], peq.shape[0]), interpolation=cv2.INTER_NEAREST)
        rel = cv2.inpaint(peq, mp, 25, cv2.INPAINT_TELEA)
        rel = cv2.resize(rel, (fondo.shape[1], fondo.shape[0]), interpolation=cv2.INTER_CUBIC)
        m = cv2.GaussianBlur(persona, (0, 0), 12)[..., None] / 255.0
        fondo = (fondo * (1 - m) + rel * m).astype(np.uint8)
    fondo = Image.fromarray(fondo).filter(ImageFilter.GaussianBlur(blur))
    borde = perro.filter(ImageFilter.GaussianBlur(1.5))
    fondo.paste(im, (0, 0), borde)
    salida = salida or os.path.splitext(ruta)[0] + '-limpia.jpg'
    fondo.save(salida, quality=93)
    print(salida)
    return salida


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('foto'); p.add_argument('salida', nargs='?')
    p.add_argument('--blur', type=float, default=14); p.add_argument('--sin-persona', action='store_true')
    a = p.parse_args()
    limpiar(a.foto, a.salida, a.blur, not a.sin_persona)
