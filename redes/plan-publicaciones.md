# Kivoa · Plan de publicaciones (Instagram · TikTok · Facebook) · 29/09 – 25/10/2026

Objetivo: **clics a Etsy/kivoa.es y primeras ventas**, no seguidores. Cada pieza se produce una vez y se reutiliza en las 3 redes.

## 1. Reparto por red (qué va a cada una y por qué)

| Red | Idioma | Formato principal | Ritmo | Cómo se sube |
|---|---|---|---|---|
| **Instagram** | Inglés (decidido el 27/09) | Reels + carruseles | Semana 1: las 9 piezas del arranque · luego **lun · mié · sáb** | Meta Business Suite (programa Reels y carruseles) |
| **TikTok** | Inglés | Vídeo + modo foto (carrusel) | Semanas 1–2: **5/semana** (TikTok aprende rápido) · luego 3/semana | TikTok Studio web → *Programar* (hasta 10 días vista) |
| **Facebook** | **Español** (público local: Cádiz/Málaga, veterinarias, regalo) | Lo mismo que Instagram | Igual que Instagram | Misma publicación en Business Suite marcando también la página de Facebook y cambiando el texto a ES |

Opinión franca: Facebook aporta poco alcance orgánico en 2026, pero cuesta **cero** (mismo archivo, misma programación) y es donde está el público de 40–60 años que compra regalos memoriales en España. No producimos nada exclusivo para Facebook.
Pinterest (recomendado en el plan del 28/09) queda para la semana 3: es la red con tráfico más duradero hacia Etsy y se alimenta con las mismas imágenes.

**Horas (España):** Reels/TikTok **13:30** o **20:30–21:30** · Facebook **20:00–21:00**.

## 2. Material listo (en el repo)

Vídeos sin sonido: la música se pone **dentro de la app** (en cuenta de Empresa, solo la biblioteca comercial).

| Código | Archivo | Uso |
|---|---|---|
| **V1** | `assets/videos/reel-en-1-antes-despues-8s.mp4` (ES: `reel-es-1-…`) | Reel/TikTok: antes → después (gancho POV) |
| **V2** | `assets/videos/reel-en-2-como-funciona-10s.mp4` (ES: `reel-es-2-…`) | Reel/TikTok: 3 pasos |
| **V3** | `assets/videos/reel-en-3-marcos-8s.mp4` (ES: `reel-es-3-…`) | Reel/TikTok: marcos y tamaños (pregunta → comentarios) |
| **VE** | `assets/videos/etsy-rosa-12s.mp4` | Vídeo del anuncio de Etsy (Rosa) |
| C1 | `antes-foto-luna.jpg` → `despues-retrato-luna-v2.webp` → `banner-salon-luna.webp` | Carrusel antes/después |
| C2 | `assets/etsy/foto-como-funciona.jpg` + `foto-vista-previa.jpg` | Carrusel cómo funciona |
| C5 / C6 | `assets/etsy/foto-marcos.jpg` · `foto-tamanos.jpg` | Imagen marcos · tamaños |
| C8 | `assets/etsy/foto-que-foto-enviar.jpg` | Carrusel "qué foto enviar" |

Regenerar o adaptar: `python3 generador/video/videos.py` (ver cabecera del script).

⚠️ **Etiqueta de IA obligatoria** en V1, V2, V3 y VE (usan el salón generado `banner-salon-luna`): TikTok → *Contenido generado por IA*; Instagram/Facebook → *Información de IA*.

## 3. Calendario

Textos: Instagram/TikTok en `instagram/instagram-en.md` (§2) y `tiktok/configuracion-tiktok.md` (§7). Facebook: el texto ES de `instagram/configuracion-instagram.md`.

### Semana 1 · 29/09 – 04/10 · Arranque (perfil con 9 piezas antes de mover nada)

| Día | Instagram (+ Facebook) | TikTok |
|---|---|---|
| Mar 29 | #1 Carrusel antes/después (C1) 📌 · #2 Carrusel cómo funciona (C2) 📌 | V1 |
| Mié 30 | #3 Reel **V1** · #5 Marcos (C5) | Modo foto: antes/después (C1) |
| Jue 01 | #4 Carrusel 5 estilos 📌 (mockups de Etsy) · #6 Tamaños (C6) | V2 |
| Vie 02 | #8 Carrusel qué foto enviar (C8) | Modo foto: 5 estilos ("which would you pick? 1–5") |
| Sáb 03 | #9 Carrusel por qué hay vista previa | V3 |

La #7 (desembalaje) se publica el día que llegue la muestra de Gelato, fuera de calendario y como prioridad (es el único contenido 100 % real).

### Semanas 2–4 · patrón lun · mié · sáb

| Semana | Lunes · antes/después | Miércoles · proceso | Sábado · emoción/regalo |
|---|---|---|---|
| **2** (05–10/10) | Reel **V2** | Reel desembalaje de la muestra *(o V3 si no ha llegado)* | Carrusel "Regalo para quien acaba de perder a su mascota" (memorial, tono cariño) |
| **3** (12–17/10) | Reel antes/después **de otro estilo** (Lavanda o Aventurero) | Reel "detalle del cuadro real": papel, marco y kit de colgar (fotos de la muestra) | Primer contenido de **Navidad**: "Christmas gift for pet lovers" |
| **4** (19–24/10) | Reel antes/después **gato** (en cuanto haya un retrato de gato con permiso) | Reel "respuesta a comentario" (la pregunta más repetida) | Navidad: fechas límite de pedido para llegar el 24/12 |

TikTok en semana 2: además de lo anterior, 2 extras reutilizando V1/V2 con **otro gancho de texto** (se sube como vídeo nuevo; TikTok premia el gancho, no el material).

## 4. Rutina semanal (≈ 1 h 30 min en total)

- **Domingo (45 min):** programar las 3 piezas de IG/FB en Business Suite y las de TikTok en TikTok Studio. Medir (§5).
- **Diario (10 min):** responder comentarios y DM en la primera hora tras publicar. Las respuestas rápidas están en `instagram-en.md` §4.

## 5. Medición (cada domingo, 10 min)

1. Ventas y sesiones por `utm_source` (Shopify → Análisis) y visitas a Etsy por fuente (Etsy → Estadísticas).
2. Clics en el enlace del perfil (IG y TikTok).
3. **% de visualización completa** de cada vídeo: decide qué formato repetimos.
4. Guardados y compartidos.

Regla de decisión (25/10): el vídeo con mejor retención y más clics se convierte en **plantilla** (5 variantes con otros estilos) y es el candidato a promoción de pago (Spark Ads / Meta). Lo demás se deja de producir.

## 6. Pendiente para completar el plan

- [ ] Vídeos por estilo (Lavanda, Aventurero, Caballos, Clásico): el script ya lo admite; faltan las imágenes de cada estilo en local (retrato + ambientación). Descargarlas de Shopify (Contenido → Archivos) a `assets/estilos/<estilo>/` **o** permitir `cdn.shopify.com` en la red del entorno de Claude y las descargo yo.
- [ ] Retrato de **gato** y de **perro negro** (con permiso del dueño) para variedad.
- [ ] Muestra de Gelato: al llegar, grabar en vertical: desembalaje, detalle del papel, marco y colgado. Sin IA, así no necesita etiqueta.
