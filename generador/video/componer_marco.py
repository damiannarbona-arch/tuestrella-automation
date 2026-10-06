"""Encaja un retrato real dentro del marco gris liso (#BDBDBD) de un vídeo generado con IA, fotograma a fotograma.

La IA solo genera el movimiento (manos, persona, marco con el interior gris); el retrato nunca pasa por la IA, así que
sale idéntico y nítido. Por fotograma: máscara del gris → 4 esquinas (si el marco se sale por un borde, las de ese lado
se deducen de la proporción del marco) → suavizado temporal → perspectiva → luz del gris aplicada al retrato →
solo se pinta donde había gris (los dedos que tapan el marco quedan delante).

Uso: python3 generador/video/componer_marco.py VIDEO RETRATO SALIDA.mp4 [--papel r,g,b]
"""
import argparse, subprocess
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image
from scipy import ndimage

PROP = 25 / 20      # alto / ancho del hueco del marco (20×25)


def mascara_gris(a):
    a = a.astype(np.int16)
    v = a.mean(2)
    m = (np.abs(a[..., 0] - a[..., 1]) < 11) & (np.abs(a[..., 1] - a[..., 2]) < 13) & (v > 120) & (v < 215)
    lab, n = ndimage.label(m)
    if not n:
        return None
    tam = ndimage.sum(m, lab, range(1, n + 1))
    m = lab == (tam.argmax() + 1)
    m = ndimage.binary_closing(m, np.ones((9, 9)), iterations=2)
    return ndimage.binary_fill_holes(m)


def esquinas(m, prev):
    """TL, TR, BR, BL del hueco gris. Si toca el borde superior o inferior, completa con la proporción del marco."""
    H, W = m.shape
    ys, xs = np.nonzero(m)
    s, d = xs + ys, xs - ys
    q = np.array([(xs[k], ys[k]) for k in (s.argmin(), d.argmax(), s.argmax(), d.argmin())], float)
    arriba, abajo = ys.min() <= 2, ys.max() >= H - 3
    if (arriba or abajo) and prev is not None:
        alto_prev = np.linalg.norm(prev[3] - prev[0]) / max(np.linalg.norm(prev[1] - prev[0]), 1)
        if arriba:   # bajas fiables → subir con la proporción
            bl, br = q[3], q[2]
            ancho = np.linalg.norm(br - bl)
            n = np.array([(br - bl)[1], -(br - bl)[0]]) / max(ancho, 1)
            h = ancho * alto_prev
            q = np.array([bl + n * h, br + n * h, br, bl])
        else:
            tl, tr = q[0], q[1]
            ancho = np.linalg.norm(tr - tl)
            n = np.array([-(tr - tl)[1], (tr - tl)[0]]) / max(ancho, 1)
            h = ancho * alto_prev
            q = np.array([tl, tr, tr + n * h, tl + n * h])
    return q


def retrato_con_papel(ret, papel):
    """El retrato (2:3) dentro del hueco 4:5, con papel a los lados, como el impreso."""
    w = int(ret.height / PROP)
    lienzo = Image.new('RGB', (w, ret.height), papel)
    lienzo.paste(ret, ((w - ret.width) // 2, 0))
    return np.asarray(lienzo)


def componer(video, retrato, salida, papel=(247, 241, 230)):
    ret = Image.open(retrato).convert('RGB')
    ret = ret.resize((1200, int(1200 * ret.height / ret.width)), Image.LANCZOS)
    src = retrato_con_papel(ret, papel)
    sh, sw = src.shape[:2]
    origen = np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]])
    gen = imageio_ffmpeg.read_frames(video, pix_fmt='rgb24')
    meta = next(gen)
    W, H = meta['size']
    fps = meta.get('fps') or 24
    frames, quads, masks = [], [], []
    prev = None
    for f in gen:
        a = np.frombuffer(f, np.uint8).reshape(H, W, 3).copy()
        m = mascara_gris(a)
        if m is not None and m.sum() < 15000:      # marca de agua u otro gris pequeño: no es el marco
            m = None
        q = esquinas(m, prev) if m is not None else None
        frames.append(a); quads.append(q); masks.append(m)
        if m is not None and m[:3].sum() == 0 and m[-3:].sum() == 0:
            prev = q
    # fotogramas en que el marco está tapado a medias (una puerta, una mano) o no se ve: el encuadre del marco
    # completo más cercano; como solo se pinta donde hay gris, lo tapado sigue tapado
    areas = np.array([m.sum() if m is not None else 0 for m in masks], float)
    ref = np.median(areas[areas > 0]) if (areas > 0).any() else 0
    validos = [i for i, (q, ar) in enumerate(zip(quads, areas)) if q is not None and ar > .5 * ref]
    if not validos:
        raise SystemExit('No se encuentra el marco gris en el vídeo')
    for i in range(len(quads)):
        if i not in validos:
            quads[i] = quads[min(validos, key=lambda j: abs(j - i))]
    Q = np.array(quads)
    Qs = ndimage.uniform_filter1d(Q, size=5, axis=0, mode='nearest')     # sin temblores
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{W}x{H}', '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', salida]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for a, q, m in zip(frames, Qs, masks):
        q = q.mean(0) + (q - q.mean(0)) * 1.015   # un pelo más grande: sin línea gris en los bordes
        M = cv2.getPerspectiveTransform(origen, np.float32(q))
        warp = cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_LANCZOS4)
        zona = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(zona, np.int32(np.round(q)), 1)
        if m is None:       # el marco no se ve en este fotograma
            p.stdin.write(a.tobytes())
            continue
        zona &= ndimage.binary_dilation(m, iterations=6).astype(np.uint8)   # lo que tapa el gris queda delante
        # luz: el gris del fotograma marca sombras y degradados; se aplican al retrato
        g = cv2.GaussianBlur(a.mean(2).astype(np.float32), (0, 0), 25)
        ref = np.median(a.mean(2)[zona > 0]) if zona.any() else 180
        luz = np.clip(g / max(ref, 1), .8, 1.12)[..., None]
        out = np.clip(warp * luz, 0, 255)
        alfa = cv2.GaussianBlur(zona.astype(np.float32), (0, 0), 1.2)[..., None]
        comp = (a * (1 - alfa) + out * alfa).astype(np.uint8)
        p.stdin.write(comp.tobytes())
    p.stdin.close(); p.wait()
    print(salida, len(frames), 'fotogramas')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('video'); ap.add_argument('retrato'); ap.add_argument('salida')
    ap.add_argument('--papel', default='247,241,230')
    a = ap.parse_args()
    componer(a.video, a.retrato, a.salida, tuple(int(x) for x in a.papel.split(',')))
