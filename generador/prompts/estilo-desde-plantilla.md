# Prompt · Cualquier estilo a partir de su plantilla (Lavanda, Aventurero, Caballos, Clásico)

Iconos, rasgos y frase los pone después `generador/rasgos.py` en inglés y en español (1 generación → 2 retratos). Aventurero: los letreros de madera, `generador/casos/letreros.py`.

Uso: nueva conversación en ChatGPT → adjuntar **1)** la imagen del modelo del estilo (plantilla) y **2)** la foto principal de la mascota → pegar el prompt con los campos `[…]` rellenados. El Estilo Rosa tiene su prompt propio (`estilo-rosa.md`).

```
Crea un retrato ilustrado de mascota siguiendo EXACTAMENTE el mismo diseño, composición, paleta de colores, técnica y tipografías que la PRIMERA imagen adjunta (plantilla del "Estilo [ESTILO]"). La SEGUNDA imagen es la mascota que debe aparecer en el retrato. Sustituye a la mascota de la plantilla por esta y cambia solo los textos que te indico; todo lo demás debe quedar igual.

MASCOTA
- Dibuja a la mascota de la segunda imagen con total fidelidad: especie, forma de la cabeza y las orejas, color y dibujo exacto del pelaje y las manchas, color de cada ojo y expresión.
- Misma posición, tamaño, encuadre y técnica de ilustración que la mascota de la plantilla.

TEXTOS (escríbelos exactamente así, con sus tildes y la ñ)
- Nombre: "[NOMBRE]"
- Rasgos: mantén la fila de 6 círculos de la plantilla en la misma posición y tamaño, pero VACÍOS: sin ningún icono dentro y sin palabras debajo (fondo limpio).
- Frase: NO escribas ninguna frase; deja libre su espacio y mantén solo el adorno que la acompaña (trazo o subrayado).
- Fechas: [FECHAS o "ninguna: elimina las fechas y deja ese espacio limpio con el mismo fondo"]
- Si la plantilla tiene algún otro texto, elimínalo y deja el fondo limpio.

FOTOS PEQUEÑAS
- Si la plantilla tiene fotos pequeñas o marcos tipo polaroid, mantenlos en la misma posición, tamaño y ángulo, pero deja su interior VACÍO, relleno de un único color gris liso #BDBDBD, sin imagen, sin textura y sin sombra dentro.

REGLAS
- Formato vertical, mismos márgenes que la plantilla, sin recortar nada por los bordes.
- No cambies la paleta, las fuentes, los adornos ni la posición de ningún elemento. No añadas elementos nuevos, marcos exteriores, marcas de agua ni texto extra.
```

Correcciones: las mismas frases cortas de `estilo-rosa.md`, siempre terminadas en "No cambies nada más".
