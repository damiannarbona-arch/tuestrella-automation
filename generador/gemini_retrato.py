"""Retrato con Gemini (API de Google) a partir de la plantilla del estilo + la foto de la mascota.

Sustituye la conversación con ChatGPT: mismo prompt que generador/prompts/estilo-desde-plantilla.md
(círculos vacíos, sin frase, polaroids en gris o sin polaroids). Después se sigue igual:
polaroids.py → rasgos.py → marca_agua.py.

Necesita la variable de entorno GEMINI_API_KEY (Google AI Studio → Get API key).

Uso:
  python3 generador/gemini_retrato.py PLANTILLA FOTO NOMBRE [--salida DIR] [--n 2] [--modelo lite|flash|pro] [--sin-polaroids]
  p. ej. … assets/casos/bizcocho/oficial-clasico-es.webp assets/casos/avelino/foto-principal.jpg Avelino --sin-polaroids
"""
import argparse, base64, io, os, sys, time
import requests
from PIL import Image, ImageOps

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# precios por imagen (AI Studio, 02/10/2026): lite 0,034 $ (sin etiqueta de pago) · flash 0,067 $ · pro 0,134 $
MODELOS = {'lite': 'gemini-3.1-flash-lite-image', 'flash': 'gemini-3.1-flash-image', 'pro': 'gemini-3-pro-image'}
URL = 'https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent'

PROMPT = """Crea un retrato ilustrado de mascota siguiendo EXACTAMENTE el mismo diseño, composición, paleta de colores, técnica y tipografías que la PRIMERA imagen (la plantilla del estilo). La SEGUNDA imagen es la mascota que debe aparecer en el retrato. Sustituye a la mascota de la plantilla por esta y cambia solo lo que te indico; todo lo demás debe quedar igual.

MASCOTA
- Dibuja a la mascota de la segunda imagen con total fidelidad: especie, raza, forma de la cabeza y las orejas, color y dibujo exacto del pelaje y las manchas, color de cada ojo y expresión.
- Misma posición, tamaño, encuadre y técnica de ilustración que la mascota de la plantilla.

TEXTOS
- Nombre: "{nombre}", con la misma tipografía caligráfica, tamaño y posición que el nombre de la plantilla, y su subrayado.
- Rasgos: mantén la fila de 6 círculos de acuarela en la misma posición y tamaño, pero VACÍOS: sin iconos dentro y sin palabras debajo.
- Frase: NO escribas ninguna frase; deja su espacio limpio y conserva solo el trazo curvo que la acompaña.
- Elimina cualquier otro texto de la plantilla y deja el fondo limpio.

{polaroids}

REGLAS
- Formato vertical 2:3, mismos márgenes que la plantilla, sin recortar nada por los bordes.
- No cambies la paleta, las fuentes, los adornos ni la posición de ningún elemento. No añadas marcos exteriores, marcas de agua ni texto extra."""

CON_POLAROIDS = """FOTOS PEQUEÑAS
- Si la plantilla tiene fotos tipo polaroid, mantenlas en la misma posición, tamaño y ángulo, pero con el interior VACÍO, relleno de un gris liso #BDBDBD, sin imagen, sin textura y sin sombra dentro."""
SIN_POLAROIDS = """FOTOS PEQUEÑAS
- Si la plantilla tiene fotos tipo polaroid, elimínalas por completo y rellena ese espacio con el mismo fondo y adornos de la plantilla, como si nunca hubieran estado. No agrandes ni muevas a la mascota."""


def parte_imagen(ruta, lado=1536):
    im = ImageOps.exif_transpose(Image.open(ruta)).convert('RGB')
    im.thumbnail((lado, lado), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'JPEG', quality=92)
    return {'inline_data': {'mime_type': 'image/jpeg', 'data': base64.b64encode(b.getvalue()).decode()}}


def generar(plantilla, foto, nombre, salida, n=2, modelo='flash', polaroids=True):
    clave = os.environ.get('GEMINI_API_KEY')
    if not clave:
        sys.exit('Falta GEMINI_API_KEY en el entorno (configuración del entorno → variables de entorno).')
    texto = PROMPT.format(nombre=nombre, polaroids=CON_POLAROIDS if polaroids else SIN_POLAROIDS)
    cuerpo = {
        'contents': [{'parts': [{'text': texto}, parte_imagen(plantilla), parte_imagen(foto)]}],
        'generationConfig': {'responseModalities': ['TEXT', 'IMAGE'], 'imageConfig': {'aspectRatio': '2:3'}},
    }
    os.makedirs(salida, exist_ok=True)
    hechas = []
    for i in range(1, n + 1):
        r = requests.post(URL.format(MODELOS[modelo]), params={'key': clave}, json=cuerpo, timeout=300)
        if r.status_code != 200:
            print(f'Intento {i}: error {r.status_code}: {r.text[:400]}')
            time.sleep(3)
            continue
        partes = r.json().get('candidates', [{}])[0].get('content', {}).get('parts', [])
        imgs = [p for p in partes if 'inlineData' in p or 'inline_data' in p]
        if not imgs:
            print(f'Intento {i}: sin imagen. Respuesta: ' + ' '.join(p.get('text', '') for p in partes)[:400])
            continue
        datos = (imgs[0].get('inlineData') or imgs[0]['inline_data'])['data']
        ruta = os.path.join(salida, f'{nombre.lower()}-{modelo}-{i}.png')
        Image.open(io.BytesIO(base64.b64decode(datos))).save(ruta)
        print(ruta)
        hechas.append(ruta)
    return hechas


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('plantilla'); p.add_argument('foto'); p.add_argument('nombre')
    p.add_argument('--salida', default=os.path.join(RAIZ, 'assets', 'gemini'))
    p.add_argument('--n', type=int, default=2)
    p.add_argument('--modelo', choices=MODELOS, default='flash')
    p.add_argument('--sin-polaroids', action='store_true')
    a = p.parse_args()
    generar(a.plantilla, a.foto, a.nombre, a.salida, a.n, a.modelo, not a.sin_polaroids)
