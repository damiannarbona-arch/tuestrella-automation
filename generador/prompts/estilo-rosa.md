# Prompt fijo · Estilo Rosa (ChatGPT)

Uso: nueva conversación en ChatGPT → adjuntar **1)** `assets/despues-retrato-luna-v2.webp` (referencia del patrón) y **2)** la foto principal de la mascota → pegar el prompt con los campos `[…]` rellenados.
Las 3 fotos secundarias **no** se pasan a ChatGPT: las coloca después el generador (`generador/penny/componer.py`) sin alterarlas.

```
Crea un retrato ilustrado de mascota siguiendo EXACTAMENTE el mismo diseño, composición y estilo que la PRIMERA imagen adjunta (plantilla "Estilo Rosa"). La SEGUNDA imagen es la mascota que debe aparecer en el retrato.

MASCOTA
- Dibuja a la mascota de la segunda imagen con total fidelidad: raza, forma de la cabeza y las orejas, color y dibujo exacto del pelaje, manchas, color de ojos y expresión. Si lleva collar o ropa en la foto, mantenlo.
- Solo cabeza, cuello y parte del pecho, mirando en la misma dirección y en la misma posición y tamaño que la mascota de la plantilla.
- Técnica: acuarela suave con detalle fino en el pelo; fondo de manchas de acuarela azul muy claro y rosa empolvado detrás de la mascota, como en la plantilla.

DISEÑO (idéntico a la plantilla)
- Formato vertical 2:3, fondo papel color crema con textura sutil.
- Arriba a la derecha: las fechas "[DD.MM.AAAA] — [DD.MM.AAAA]" con el pequeño corazón y los trazos debajo.
- Derecha: la rama vertical con una rosa rosa y hojas en acuarela.
- Izquierda: TRES marcos tipo polaroid inclinados, en la misma posición, tamaño y ángulo que en la plantilla, con borde blanco roto. IMPORTANTE: el interior de cada polaroid debe quedar VACÍO, relleno de un único color gris liso #BDBDBD, sin foto, sin dibujo, sin textura ni sombra dentro. Mantén los pequeños corazones y trazos decorativos que hay alrededor.
- Debajo de la mascota: el nombre "[NOMBRE]" en letra caligráfica negra, igual que "Luna" en la plantilla, con el corazón y el subrayado.
- Fila de 6 iconos en círculos de acuarela con estas palabras debajo, en este orden: "[RASGO 1]", "[RASGO 2]", "[RASGO 3]", "[RASGO 4]", "[RASGO 5]", "[RASGO 6]".
- Abajo, centrada, la frase: "[FRASE]", en la misma letra manuscrita y con los adornos de la plantilla.
- Huellas de acuarela en las esquinas inferiores.

REGLAS
- No cambies la paleta, las fuentes ni la posición de ningún elemento. No añadas elementos nuevos, marcos exteriores, marcas de agua ni texto extra.
- Escribe los textos exactamente como te los doy, respetando tildes y la letra ñ.
- No recortes ningún elemento por los bordes: deja el mismo margen que en la plantilla.
```

## Si sale mal (respuestas cortas en la misma conversación)
- Mascota poco parecida: `La mascota no se parece lo suficiente a la foto: corrige [color del pelaje / manchas / orejas / ojos] para que sea idéntica a la segunda imagen. No cambies nada más.`
- Polaroids con dibujo: `Deja el interior de las tres polaroids en gris liso #BDBDBD, sin ninguna imagen. No cambies nada más.`
- Texto con errores: `Corrige solo el texto: debe decir exactamente "[texto]". No cambies nada más.` (Si falla 2 veces, lo corrijo yo en el montaje.)
- Diseño distinto de la plantilla: nueva conversación; no insistir más de 3 veces en la misma.

## Después
Descargar la imagen (PNG) y pasármela junto con las 3 fotos secundarias → montaje de polaroids, revisión de textos, escalado a la resolución de impresión y vista previa con marca de agua.
