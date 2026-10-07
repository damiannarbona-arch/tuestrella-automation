# Ejemplo IA «Bruno» (teckel miniatura de pelo corto, negro y fuego)

Regla de oro del realismo: **fotos y vídeos que podría haber hecho el dueño con su móvil** (altura de una persona, encuadre imperfecto, velocidad real). Nada de drones, cámara a ras de suelo que se desliza ni cámara lenta.

## Bloque «foto de móvil» (pegar al final de cada prompt de foto)
> Shot on an iPhone by the owner, 26 mm wide lens, natural available light only, slightly imperfect casual framing, real-life clutter, true-to-life colours, fine sensor noise, normal depth of field (background slightly soft, not heavily blurred). Photorealistic, not a studio photo, not cinematic, no text, no watermark. Vertical 4:5.

## 1 · Foto principal (la base de todo: retrato y resto de fotos)
> A real photo of a miniature smooth-haired dachshund, black and tan, adult, about 5 years old, slightly grey hairs on the muzzle, shiny short coat, long floppy ears, warm brown eyes, a thin red collar. He sits on a light grey fabric sofa wrapped halfway in a beige knitted blanket, looking up at the camera with his head slightly tilted. The photo is taken by the owner standing in front of the sofa, phone held at chest height pointing slightly down. Spanish flat living room in the afternoon: daylight from a window on the left, a cushion with a slight crease, a TV remote and a phone charger cable on the sofa, a wooden coffee table edge in the foreground, a plant in the corner. [bloque foto de móvil]

Desde aquí, **adjuntar siempre la foto 1** y empezar con:
> Use the attached photo. Keep this exact dog identical: same face, same black and tan markings, same ears, same grey hairs on the muzzle, same red collar.

## 2 · De paseo
> … He walks on a leash along a narrow street of a Spanish town in the morning: cobblestones, whitewashed walls, a green door, potted geraniums. Photo taken from the owner's height looking down at him: the owner's sneakers and the beginning of the leash are in the frame at the bottom, the dog looks back over his shoulder at the camera. Soft morning sun with real shadows. [bloque foto de móvil]

## 3 · Al sol en casa
> … He lies stretched out on his side in a patch of sunlight on a Spanish hydraulic tile floor (patterned grey and white tiles) next to a balcony door, eyes half closed, relaxed. Photo taken by the owner kneeling at about one metre, phone held horizontally at waist height. Real-life details: a slipper, a water bowl, a sheer curtain moving slightly. [bloque foto de móvil]

## 4 · Escondido en la manta (gesto típico del teckel)
> … Only his head pokes out from under a white duvet in an unmade bed, ears messy, looking at the camera sleepily. Photo taken by the owner sitting on the bed, phone close and a bit from above. Morning light through blinds, wrinkled sheets, a bedside table with a lamp and a book. [bloque foto de móvil]

## 5 · Imagen de partida del vídeo (con el marco gris)
> … The same living room as the first photo, wider view. On the wall above the sofa hangs a light oak picture frame with a wide white mat and, inside, a perfectly flat solid neutral grey rectangle (#BDBDBD), evenly lit, fully visible, no sunlight or shadows on it. The dog stands on the floor in the middle of the room holding a small beige knitted blanket in his mouth, looking at the camera. Photo taken by the owner standing at the doorway, phone at chest height. Neutral daylight, no lamps switched on. Leave the bottom-right corner empty (plain floor). [bloque foto de móvil, pero vertical 9:16]

Revisar antes del vídeo: perro idéntico a la foto 1 y el gris **gris** (sin tono naranja).

## Vídeo (Dola / Seedance 2.5, 10 s, 9:16, imagen 5)
> Real smartphone video filmed by the owner, handheld at chest height from the doorway, real-time speed, natural slight hand shake, one continuous shot with no cuts. The dachshund trots across the living room dragging the little knitted blanket in his mouth, jumps up onto the sofa with a small effort, turns around twice, drops the blanket and burrows underneath it until only his nose and eyes stick out, then looks at the camera, content. In the last 3 seconds the owner slowly and naturally tilts the phone up from the sofa to the picture frame on the wall above it and holds still; the frame does not move and nothing appears inside it. Neutral natural daylight, no warm lamp light. Normal everyday colours, not cinematic, no slow motion, no gimbal or drone movement, no zoom. Keep the dog identical to the image: same face, black and tan markings, ears and red collar. No text, no logos.

### Plan B (si sale raro el salto al sofá)
> … The dachshund is already on the sofa and pulls the blanket over himself with his snout and paws, burrows underneath until only his nose sticks out … (resto igual)

## Montaje (lo hacemos nosotros)
Retrato real en el marco con `marco_en_video.py`. Textos: «Cada noche, el mismo ritual» → «Manta, vuelta y vuelta… y a dormir» → plano del marco: «Ahora su sitio también está en la pared» → «Un cuadro personalizado, no un cuadro cualquiera».
