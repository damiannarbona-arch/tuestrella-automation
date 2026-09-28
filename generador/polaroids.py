"""Coloca las fotos originales del cliente en las polaroids vacías (gris liso) del diseño de ChatGPT.

Uso:
  python3 generador/polaroids.py DISENO SALIDA FOTO1[:fx,fy,zoom] FOTO2[...] FOTO3[...]

- Las polaroids se detectan solas (interior gris liso, ver generador/prompts/estilo-rosa.md) y se
  rellenan de arriba abajo con FOTO1, FOTO2, FOTO3.
- fx,fy = punto de la foto que queda centrado (0–1; p. ej. la cara). zoom > 1 acerca.
- Las fotos no se retocan: solo se recortan y se encajan en perspectiva.
- Se trabaja a 3× la resolución del diseño para que las fotos queden nítidas.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scipy import ndimage

S = 3


def cuadros_grises(rgb):
    a = rgb.astype(int)
    gris = (abs(a[..., 0] - a[..., 1]) < 8) & (abs(a[..., 1] - a[..., 2]) < 8) & (abs(a[..., 0] - 178) < 14)
    lab, n = ndimage.label(gris)
    tam = ndimage.sum(gris, lab, range(1, n + 1))
    cuadros = []
    for i in np.argsort(-tam)[:3]:
        if tam[i] < 5000:
            break
        ys, xs = np.nonzero(lab == i + 1)
        s, d = xs + ys, xs - ys
        esq = [(xs[k], ys[k]) for k in (s.argmin(), d.argmax(), s.argmax(), d.argmin())]  # TL TR BR BL
        cuadros.append(np.array(esq, float))
    return sorted(cuadros, key=lambda q: q[:, 1].mean())


def perspectiva(dst, src):
    """Coeficientes PIL: punto de salida (dst) → punto de la foto (src)."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        b += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def recorte(foto, aspecto, fx=.5, fy=.5, zoom=1.0):
    w, h = foto.size
    cw = min(w, h * aspecto) / zoom
    ch = cw / aspecto
    x = min(max(fx * w - cw / 2, 0), w - cw)
    y = min(max(fy * h - ch / 2, 0), h - ch)
    return foto.crop((int(x), int(y), int(x + cw), int(y + ch)))


def componer(diseno, salida, fotos):
    base = Image.open(diseno).convert('RGB')
    rgb = np.asarray(base)
    quads = cuadros_grises(rgb)
    assert len(quads) == len(fotos) == 3, f'se esperaban 3 polaroids, detectadas {len(quads)}'
    grande = base.resize((base.width * S, base.height * S), Image.LANCZOS)
    oscuro = Image.fromarray(((rgb.mean(2) < 80) * 255).astype(np.uint8)).resize(grande.size, Image.LANCZOS)
    for q, (ruta, fx, fy, zoom) in zip(quads, fotos):
        # 2,5 px de margen hacia fuera para tapar el antialias del gris
        c = q.mean(0)
        q = c + (q - c) * (1 + 2.5 / np.linalg.norm(q - c, axis=1, keepdims=True))
        Q = q * S
        w = np.linalg.norm(Q[1] - Q[0])
        h = np.linalg.norm(Q[3] - Q[0])
        foto = recorte(ImageOps.exif_transpose(Image.open(ruta)).convert('RGB'), w / h, fx, fy, zoom)
        src = [(0, 0), (foto.width, 0), (foto.width, foto.height), (0, foto.height)]
        capa = foto.transform(grande.size, Image.PERSPECTIVE, perspectiva(Q, src), Image.BICUBIC)
        # máscara con antialias (dibujada a 4× y reducida) para que el borde no quede dentado
        A4 = 4
        mascara = Image.new('L', (grande.width * A4, grande.height * A4), 0)
        ImageDraw.Draw(mascara).polygon([tuple(p * A4) for p in Q], fill=255)
        mascara = mascara.resize(grande.size, Image.LANCZOS)
        grande.paste(capa, (0, 0), mascara)
        # los adornos dibujados encima de la polaroid (corazones, tinta casi negra) se conservan
        adorno = Image.composite(oscuro, Image.new('L', grande.size, 0), mascara)
        grande.paste(base.resize(grande.size, Image.LANCZOS), (0, 0), adorno)
    grande.save(salida, quality=95)
    print(salida, grande.size)


if __name__ == '__main__':
    fotos = []
    for arg in sys.argv[3:6]:
        ruta, _, p = arg.partition(':')
        vals = [float(v) for v in p.split(',')] if p else []
        fotos.append((ruta, *(vals + [.5, .5, 1.0][len(vals):])))
    componer(sys.argv[1], sys.argv[2], fotos)
