"""Retrato real dentro del marco de un vídeo de IA cuando el «gris» salió teñido por la luz de la escena (p. ej.
lámpara cálida: el #BDBDBD pedido sale marrón) y solo en un tramo final (la cámara sube hasta el marco).

Diferencias con componer_marco.py:
- la máscara se busca por cercanía al color real del hueco (se mide en el último fotograma), no por gris neutro;
- solo se procesa desde DESDE segundos (antes el vídeo queda intacto: así no confunde suelos o paredes grises);
- el diseño (2:3) se rellena arriba/abajo con su propio papel hasta la proporción del hueco (no se recorta);
- luz y tono: el papel del impreso queda con el brillo y el color del paspartú que lo rodea.

Uso: python3 generador/video/marco_en_video.py VIDEO RETRATO SALIDA DESDE_SEGUNDOS
"""
import subprocess, sys, os
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
from componer_marco import esquinas, afinar, suavizar  # noqa: E402


def mascara(a, color, tol=24):
    d = np.abs(a.astype(np.int16) - np.array(color, np.int16)).max(2)
    m = d < tol
    lab, n = ndimage.label(m)
    if not n:
        return None
    tam = ndimage.sum(m, lab, range(1, n + 1))
    m = lab == (tam.argmax() + 1)
    m = ndimage.binary_fill_holes(ndimage.binary_closing(m, np.ones((7, 7)), iterations=2))
    ys, xs = np.nonzero(m)
    if m.sum() < 15000 or m.sum() / ((np.ptp(ys) + 1) * (np.ptp(xs) + 1)) < .85:   # tiene que ser un rectángulo
        return None
    return m


def componer(video, retrato, salida, desde):
    gen = imageio_ffmpeg.read_frames(video, pix_fmt='rgb24')
    meta = next(gen)
    W, H = meta['size']
    fps = meta.get('fps') or 24
    frames = [np.frombuffer(f, np.uint8).reshape(H, W, 3).copy() for f in gen]
    i0 = int(desde * fps)
    # de atrás hacia delante: en el último fotograma el marco se ve entero; el color se va siguiendo
    color = frames[-1][H // 2 - 40:H // 2 + 40, W // 2 - 40:W // 2 + 40].reshape(-1, 3).mean(0)
    masks = [None] * len(frames)
    colores = [None] * len(frames)
    for k in range(len(frames) - 1, i0 - 1, -1):
        m = mascara(frames[k], color, 20)
        if m is None:
            break
        masks[k] = m
        color = np.median(frames[k][m], 0)
        colores[k] = color
    val = [k for k, m in enumerate(masks) if m is not None]
    # cuadrilátero del hueco completo (último fotograma) y, en los que el marco sale cortado por arriba,
    # el mismo desplazado/escalado para que encaje con el borde inferior y los laterales visibles
    q_full = afinar(masks[-1], esquinas(masks[-1], None))
    ancho_full = np.linalg.norm(q_full[2] - q_full[3])
    quads = [None] * len(frames)
    # el marco está quieto en la pared y solo se mueve la cámara: en cada fotograma se miden con precisión
    # subpíxel el borde inferior y los laterales del hueco (promedio de cientos de columnas/filas) y el retrato
    # sigue ese movimiento tal cual. Sin suavizar: los vídeos de IA dan saltos de cámara (fotogramas perdidos)
    # y, si se suaviza, el retrato se desfasa del marco y parece que se balancea.
    medida = {}
    for k in val:
        a, m = frames[k], masks[k]
        d = np.abs(a.astype(np.float32) - colores[k]).max(2)
        w = np.clip((32 - d) / 16, 0, 1)
        ys, xs = np.nonzero(m)
        y1, x0, x1 = ys.max(), xs.min(), xs.max()
        cols = slice(int(x0 + .2 * (x1 - x0)), int(x1 - .2 * (x1 - x0)))
        yb = y1 - 30
        abajo = yb + w[yb:yb + 50, cols].sum(0).mean()
        filas = slice(max(ys.min(), y1 - 250), y1 - 30)
        xl = (x0 + 30) - w[filas, x0 - 20:x0 + 30].sum(1).mean()
        xr = (x1 - 30) + w[filas, x1 - 30:x1 + 20].sum(1).mean()
        medida[k] = ((xl + xr) / 2, abajo, xr - xl)
    # la forma la da el último fotograma; su base, medida con el mismo método, es el ancla
    bx0, by0, w0 = medida[val[-1]]
    for k in val:
        bx, by, wk = medida[k]
        quads[k] = (q_full - np.array([bx0, by0])) * (wk / w0) + np.array([bx, by])
    Q = np.array([quads[k] for k in val])
    q = q_full
    prop = (np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / (np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3]))
    ret = Image.open(retrato).convert('RGB')
    ret = ret.resize((1200, int(1200 * ret.height / ret.width)), Image.LANCZOS)
    papel = ret.getpixel((20, 20))
    lienzo = Image.new('RGB', (1200, max(ret.height, int(1200 * prop))), papel)
    lienzo.paste(ret, (0, (lienzo.height - ret.height) // 2))
    src = np.asarray(lienzo).astype(np.float32)
    sh, sw = src.shape[:2]
    origen = np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]])
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{W}x{H}', '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', salida]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k, a in enumerate(frames):
        m = masks[k]
        if m is None:
            p.stdin.write(a.tobytes()); continue
        q = Q[val.index(k)]
        q = q.mean(0) + (q - q.mean(0)) * 1.012
        M = cv2.getPerspectiveTransform(origen, np.float32(q))
        warp = cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
        zona = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(zona, np.int32(np.round(q)), 1)
        dentro = zona.astype(bool)
        anillo = ndimage.binary_dilation(dentro, iterations=26) & ~ndimage.binary_dilation(dentro, iterations=8)
        pasp = np.median(a[anillo], 0)                       # color y brillo del paspartú con esta luz
        # degradado de luz de la escena sobre el hueco, normalizado
        g = a.mean(2).astype(np.float32)
        luz = cv2.GaussianBlur(np.where(m, g, np.median(g[m])), (0, 0), 20) / np.median(g[m])
        out = warp / np.array(papel, np.float32) * pasp * .98   # el papel del impreso = el paspartú
        out *= np.clip(luz, .6, 1.3)[..., None]
        media = out[dentro].mean(0)
        out = media + (out - media) * .94                     # tras el cristal
        out = cv2.GaussianBlur(out, (0, 0), .6)
        alfa = cv2.GaussianBlur(zona.astype(np.float32), (0, 0), 1.0)[..., None]
        comp = np.clip(a * (1 - alfa) + np.clip(out, 0, 255) * alfa, 0, 255).astype(np.uint8)
        p.stdin.write(comp.tobytes())
    p.stdin.close(); p.wait()
    print(salida, f'marco desde el fotograma {val[0]}', f'proporción {prop:.2f}')


if __name__ == '__main__':
    componer(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]))
