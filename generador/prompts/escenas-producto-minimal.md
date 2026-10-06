# Escenas minimalistas para las fichas de producto

Objetivo: fotos de producto limpias, realistas y del mismo estilo en todos los artículos, para que la ficha no se vea cargada.

## Método (no cambiar)
1. ChatGPT crea **solo la escena con el marco vacío**: el hueco del cuadro va en **gris liso #BDBDBD**, en proporción 2:3 como nuestros diseños (1024×1536), para que no se deformen al insertarlos.
2. Nosotros insertamos el diseño real con `generador/marco_en_imagen.py`. Así la cara, el nombre y los rasgos salen exactos; si ChatGPT los dibuja, los deforma.
3. Si una escena no tiene el gris liso y plano, se pide otra.

Plantillas de referencia, por ser las más limpias que tenemos:
- `assets/mockups/pared-dos-marcos.webp`: pared lisa, mueble de madera clara, luz de ventana.
- `assets/casos/penny/producto-real/estudio-79.jpg`: foto real, marco apoyado en una mesa blanca, mucho aire.

Adjunta las dos a ChatGPT junto con el prompt.

## Bloque de estilo (pegar siempre al final)
> Photorealistic interior product photo, shot on a full-frame camera with a 50 mm lens, natural soft window light from the left, gentle realistic shadows. Minimalist Scandinavian style: smooth warm off-white wall (#F6F2EC), light oak wood, at most ONE small decorative object. Lots of empty space, calm and airy, no clutter, no text, no logos, no people's faces. The picture frame interior must be a perfectly flat, uniform solid grey (#BDBDBD) rectangle with no texture, no reflection and no glare, with crisp straight edges, fully visible and not covered by anything. Portrait-orientation frame with a thin white mat; the grey artwork area inside the mat has an exact 2:3 ratio (taller than wide). Do not draw any artwork inside the frame.

## Formato fijo de cada artículo (6 elementos, siempre en este orden)
| # | Contenido | Origen |
|---|---|---|
| 1 | Escena A: el cuadro protagonista, de frente | ChatGPT + nuestro diseño |
| 2 | Escena B: el cuadro apoyado en un mueble, en casa | ChatGPT + nuestro diseño (o foto real si existe) |
| 3 | De sus fotos a su retrato (caso real) | Ya existe (sus-fotos / antes-después) |
| 4 | Escena C: detalle de cerca (nombre, rasgos, frase) | ChatGPT + nuestro diseño |
| 5 | Tamaños o marcos | Ya existe |
| 6 | Vídeo corto sin música ni letras | Sacado de los reels |

## Prompts (uno por escena; cambia solo el [ACENTO] según el estilo)

**Escena A, de frente (foto 1, la que se ve en la tienda)**
> A single light-oak picture frame hanging centered on a plain warm off-white wall, front view, straight-on, the frame filling about 55 % of the image height. Below it, the top edge of a low light-oak sideboard with [ACENTO]. Square 1:1 image. + BLOQUE DE ESTILO

**Escena B, apoyado en un mueble (foto 2)**
> A light-oak picture frame standing on a white table, leaning slightly back against a plain warm off-white wall, three-quarter view from the front-left, camera at table height. Next to it, [ACENTO]. Soft morning light, a light linen curtain shadow on the wall. Square 1:1 image. + BLOQUE DE ESTILO

**Escena C, detalle (foto 4)**
> Close-up of the lower half of a light-oak picture frame standing on a light oak shelf, slight angle from above, shallow depth of field, the wall softly out of focus behind. The grey area is the lower part of the artwork. [ACENTO] slightly blurred at the edge of the image. Square 1:1 image. + BLOQUE DE ESTILO

## [ACENTO] por estilo (un solo objeto, pequeño)
| Estilo | Acento |
|---|---|
| Rosa | a small glass vase with two pale pink peonies |
| Lavanda | a small ceramic cup with a few sprigs of dried lavender |
| Clásico | a small white ceramic vase with a single eucalyptus branch |
| Aventurero | a single pine cone and a small sprig of pine |
| Caballos | a small bundle of dried wheat in a clear glass jar |

## Variantes de marco
Pide la misma escena en **blanco** y en **negro** cambiando "light-oak picture frame" por "white wooden picture frame" o "matte black picture frame". Así cada foto 1 coincide con el marco que se elige en la ficha.

## Qué rechazar
- Gris con degradado, reflejos, sombra dentro o tapado por la planta → no sirve para insertar.
- Más de un objeto decorativo, plantas grandes, textos o cuadros extra en la pared.
- Marco torcido o en perspectiva fuerte en la escena A (debe ser frontal).
