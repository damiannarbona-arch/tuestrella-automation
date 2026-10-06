# Escenas minimalistas para las fichas de producto (versión final, 06-10)

## Reparto del trabajo
- **ChatGPT hace 3 escenas vacías** (A, B y C), con el hueco del cuadro en gris liso #BDBDBD. Son las mismas para todos los estilos.
- **El resto lo hacemos nosotros**: insertar cada diseño (`generador/marco_en_imagen.py`), de sus fotos a su retrato, marcos, tamaños y el vídeo sin música ni letras. Todo con la plantilla y los colores de las publicaciones.

## Paleta Kivoa (la misma que la web)
| Uso | Color |
|---|---|
| Fondo / pared | crema cálido #F6F2EC |
| Detalles cálidos | arena #DCD5CA |
| Acento | verde salvia #3F5147 (eucalipto, textil) |
| Madera | roble claro natural |
| Texto | carbón #2C332F |

Cómo se consigue que todo tenga el mismo tono:
1. Los prompts piden la pared crema #F6F2EC, la madera de roble claro y el eucalipto verde salvia, que son los colores de la web.
2. Al montar cada foto, aplicamos a la escena una misma corrección de color: balance cálido y blancos llevados a #F6F2EC. Así las 3 escenas y las fotos que hacemos nosotros encajan entre sí, aunque ChatGPT varíe un poco la luz.
3. Todas las fotos son cuadradas (1:1), que es el formato del carrusel de la ficha.

## Cómo pedírselo a ChatGPT
1. Abre un chat nuevo y adjunta las 2 referencias de estilo:
   - `assets/mockups/pared-dos-marcos.webp`
   - `assets/casos/penny/producto-real/estudio-79.jpg`
2. Pega primero el **mensaje inicial** y después cada prompt, uno por uno, en el mismo chat, para que las 3 escenas salgan con la misma luz y la misma pared.
3. Para cada marco (madera, blanco, negro), pide de nuevo la misma escena con la línea de cambio de marco del final.

### Mensaje inicial
> I'm going to ask you for 3 product photos for my online shop of framed pet portraits. Use the two attached images ONLY as a reference for the mood: minimalist, warm, airy and realistic. In all 3 photos, keep exactly the same room, wall colour, wood tone, light and decoration, as if they were taken in the same session. The artwork inside the frame must ALWAYS be a flat solid grey rectangle (#BDBDBD) because I will insert the real portrait later. Never draw any artwork, text or animal inside the frame.

### Escena A: de frente (foto 1, la portada del artículo)
> Photo 1 of 3. A single light natural oak picture frame hanging centered on a smooth, plain, warm cream wall (#F6F2EC), straight-on front view, perfectly level, the frame occupying about 55 % of the image height. Below it, the top edge of a low light-oak sideboard with one small matte white ceramic vase holding a single sage-green eucalyptus branch, placed to the right, not touching the frame. Soft natural window light from the left, a very subtle diagonal window shadow on the wall, gentle realistic contact shadows. Inside the frame: a thin white mat and, inside the mat, a perfectly flat, uniform solid grey (#BDBDBD) rectangle with an exact 2:3 ratio (taller than wide), with crisp straight edges, no texture, no reflection, no glare, nothing covering it. Photorealistic interior product photo, 50 mm lens, high detail, calm and minimalist, lots of empty space, no clutter, no text, no logos, no people. Square 1:1 image.

### Escena B: apoyado en un mueble (foto 2)
> Photo 2 of 3, same room and light as photo 1. The same light natural oak picture frame standing on a light-oak sideboard, leaning slightly back against the same warm cream wall (#F6F2EC), three-quarter view from the front-left, camera at sideboard height, the frame in the centre-left of the image. Next to it on the right, the same small matte white vase with one sage-green eucalyptus branch and a folded sand-coloured (#DCD5CA) linen cloth. Soft morning window light from the left, a gentle linen-curtain shadow on the wall. Inside the frame: a thin white mat and a perfectly flat, uniform solid grey (#BDBDBD) rectangle with an exact 2:3 ratio, with crisp straight edges, no texture, no reflection, no glare, fully visible. Photorealistic, 50 mm lens, minimalist, airy, no clutter, no text, no logos, no people. Square 1:1 image.

### Escena C: detalle de cerca (foto 4)
> Photo 3 of 3, same room and light. Close-up of the same light natural oak picture frame standing on the light-oak sideboard, slight angle from above and from the right, shallow depth of field: the frame in sharp focus, the cream wall softly blurred behind, the eucalyptus branch blurred at the left edge of the image. The frame fills about 80 % of the image height. Inside the frame: a thin white mat and a perfectly flat, uniform solid grey (#BDBDBD) rectangle with an exact 2:3 ratio, with crisp straight edges, no texture, no reflection, no glare, fully visible. Photorealistic, macro-like product photo, warm and calm, no text, no logos, no people. Square 1:1 image.

### Cambio de marco (repetir A, B y C)
> Now give me exactly the same image, with the same composition, light and decoration, but with a **white painted wooden frame** instead of the oak one.

> Now the same image again, but with a **matte black thin wooden frame**.

### Si el gris sale mal
> The grey area is not usable: it must be one perfectly flat solid #BDBDBD colour from edge to edge, with no gradient, no shadow, no reflection, no texture and nothing overlapping it, and with an exact 2:3 ratio. Please regenerate the same image fixing only that.

## Qué rechazar
- Gris con degradado, sombra, reflejo o tapado por algo.
- Pared que no sea crema cálido (blanca fría, gris o beige oscuro).
- Más de un adorno, plantas grandes, cuadros extra o texto.
- En la escena A, un marco torcido o visto en perspectiva.

## Diseño de cada artículo
| Artículo | Caso | Diseño |
|---|---|---|
| Rosa | Penny | `assets/casos/penny/retrato-rosa.jpg` |
| Clásico | Curro | `assets/casos/curro/diseno-clasico-v2.webp` |
| Lavanda | Miau | `assets/retratos/miau-lavanda.jpg` |
| Aventurero | Sonic | `assets/casos/sonic/diseno-aventurero-es.png` |
| Caballos | pendiente de caso real | se mantienen las fotos actuales |

## Formato fijo de cada artículo (6 elementos)
| # | Contenido | Quién |
|---|---|---|
| 1 | Escena A con su diseño | ChatGPT (escena) + nosotros (diseño) |
| 2 | Escena B con su diseño | ChatGPT (escena) + nosotros (diseño) |
| 3 | De sus fotos a su retrato (su caso real) | Nosotros |
| 4 | Escena C, detalle | ChatGPT (escena) + nosotros (diseño) |
| 5 | Los 3 marcos y los 3 tamaños | Nosotros |
| 6 | Vídeo corto sin música ni letras | Nosotros |
