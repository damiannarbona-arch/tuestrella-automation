# Kivoa · Guía visual de redes

Una sola regla de fondo: **el feed debe parecer la web**. Mismas fuentes, mismos colores. Quien llega desde Instagram a kivoa.es o a Etsy no debe notar el cambio.

Ejemplo aplicado: `assets/redes/publicaciones/01-antes-despues/` (EN para Instagram y TikTok, ES para Facebook). Generador: `generador/redes/publicaciones.py`.

## 1. Colores

| Token | Hex | Uso | Proporción |
|---|---|---|---|
| **Papel** | `#F6F2EC` | Fondo de todas las piezas (el de la web) | ~60 % |
| **Foto** | — | Retratos y ambientes: aportan todo el color | ~30 % |
| **Salvia** | `#3F5147` | Marca: logotipo, botones, checks, etiquetas | ~10 % |
| **Tinta** | `#2C332F` | Titulares y texto | — |
| **Gris** | `#505655` | Texto secundario, contador | — |
| **Arena** | `#DCD5CA` | Fondo secundario (detrás de un retrato), líneas | — |
| **Rosa** | `#D8A7A0` | Acento sacado de la rosa de los retratos: **un solo detalle por pieza** (una línea, un corazón) | < 2 % |

Prohibido: fondos de color saturado, degradados, negro puro, blanco puro de fondo y más de un acento por pieza. El color lo ponen los retratos. Si el fondo compite con ellos, pierden los retratos.

## 2. Tipografía (la de kivoa.es)

- **Titulares:** Trirong Light, 70 px en diapositivas y 92 px en la de cierre. La segunda línea va en *cursiva* como acento emocional ("*…to a portrait forever*").
- **Texto y botones:** Quattrocento Sans (Regular, y Bold en botones).
- **Etiquetas:** Quattrocento Sans Bold en MAYÚSCULAS y salvia, 26 px ("01 · THE PHOTO").
- Máximo **2 líneas** de titular y **12 palabras** por diapositiva. Si hace falta más, va en el pie de foto, no en la imagen.
- Fuentes en `generador/fuentes/` (licencia OFL, uso comercial libre).

## 3. Maquetación (plantilla fija, 1080×1350, formato 4:5)

```
┌───────────────────────────┐
│ ETIQUETA                  │  ← y 118
│ Titular línea 1           │
│ *Titular línea 2*         │  ← hasta y ~300
│ ┌───────────────────────┐ │
│ │                       │ │  ← FOTO con margen de papel de 64 px
│ │   (el "paspartú")     │ │    (como un cuadro enmarcado: es el sello visual)
│ └───────────────────────┘ │
│ Kivoa              01 / 05│  ← pie común
└───────────────────────────┘
```

- **El paspartú es la firma**: toda foto va con margen de papel alrededor, como un cuadro enmarcado. Hace que cada pieza parezca "una obra en la pared" y el feed se ve ordenado aunque cambie el contenido.
- Los 64 px de margen también protegen el recorte: Instagram muestra el perfil en 3:4 y quita ~34 px por cada lado a las piezas 4:5.
- Contador `01 / 05` siempre visible: indica que hay más diapositivas y sube el deslizamiento.
- Última diapositiva = **cierre fijo**: titular centrado, 3 checks, retrato en polaroid y botón salvia con la llamada a la acción.
- TikTok (modo foto) y Stories: la misma plantilla en 1080×1920, con 250 px libres arriba y 420 abajo.

## 4. Orden del feed

Instagram muestra lo más nuevo arriba a la izquierda. El orden de publicación decide cómo se ve el perfil.

**Tipos de portada** (se alternan):
- **F · Foto**: portada con imagen grande (antes/después, ambiente, reel, marcos, qué foto enviar).
- **T · Tipográfica**: portada de papel con titular grande y poca imagen (cómo funciona, 5 estilos, por qué hay vista previa).

**Regla:** en cada fila de 3, **2 F + 1 T**, y nunca dos T juntas, ni en horizontal ni en vertical. Así el perfil respira sin volverse un muro de texto ni un catálogo.

Arranque (orden de publicación #1 → #9 y cómo queda el perfil):

```
Perfil (arriba = más reciente)
┌──────┬──────┬──────┐
│ #9 T │ #8 F │ #7 F │
├──────┼──────┼──────┤
│ #6 F │ #5 F │ #4 T │   ← #4 "5 estilos": portada tipográfica con mosaico pequeño
├──────┼──────┼──────┤
│ #3 F │ #2 T │ #1 F │
└──────┴──────┴──────┘
Fijadas (primera fila): #1 antes/después · #2 cómo funciona · #4 estilos
```

Si el desembalaje (#7) llega fuera de orden, se publica igual: es una F y se compensa con que la siguiente pieza sea una T.

**Portadas de reel:** misma plantilla (titular + foto con paspartú). Se sube como "portada" en el momento de publicar, para que el reel no rompa la cuadrícula con un fotograma cualquiera.

## 5. Tono de la imagen

- Luz cálida, hogar y madera. Nada de estudio frío ni de fondos blancos de catálogo.
- Memorial: recuerdo y cariño, nunca tristeza forzada (nada de velas encendidas con lágrimas).
- Siempre que haya foto real (muestra de Gelato, cliente con permiso), **prima sobre la generada**.
- Piezas con ambientes generados por IA: etiqueta "Información de IA" al publicar (ver `plan-publicaciones.md`).
