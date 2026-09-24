# Kivoa (kivoa.es) — Estado y plan · 24/09/2026

## 1. Auditoría de la tienda

| Área | Estado | Acción |
|---|---|---|
| Catálogo | 5 retratos de mascota (Rosa, Lavanda, Aventurero, Caballos, Clásico), desde 39,90 € | Ver §5 |
| Tema en vivo | Craft (familia Dawn, sin slider antes/después nativo) | Migrar a Horizon (ya instalado, sin publicar) |
| Opciones de variante | En inglés: "Size", "Frame", "White frame" | Traducir: Tamaño / Marco / Blanco-Madera-Negro |
| Texto del producto | Dice "marco de madera de pino, acabado natural" aunque se vende blanco y negro | Corregir por variante |
| Alt de imágenes | Son UUID (`7755321f-…`) | Alt descriptivo (SEO + accesibilidad) |
| URLs | `copy-of-retrato-personalizado-…-4` | `retrato-mascota-estilo-clasico`, etc. (con redirección 301) |
| SEO title/description | Vacíos | Rellenar |
| Apps | Printful **y** Gelato, Easify Options, Uploadfly | Dejar un único POD; desinstalar el otro |
| Políticas | Solo privacidad | ✅ Hecho hoy (ver §2) |
| Email/teléfono personales publicados | daminarby@gmail.com, móvil | Crear hola@kivoa.es (reenvío gratuito desde el dominio) |

## 2. Legal — hecho hoy

- `/pages/envios-y-devoluciones` reescrita. **Corregido un riesgo**: la versión anterior limitaba las reclamaciones a 14 días desde la recepción. Eso choca con la garantía legal de 3 años (art. 120 TRLGDCU) y puede considerarse abusivo. Ahora mantiene la exclusión del desistimiento (art. 103.c) y deja clara la garantía.
- `/pages/terminos-y-condiciones` creada (incluye licencia de uso de fotos, no publicar sin consentimiento y la cláusula de "proceso creativo").
- Menú del pie: Envíos y devoluciones · Términos · Privacidad · Contacto.
- Fuentes en `politicas/`.

**Pendiente (requiere acción manual):**
1. **Aviso legal (LSSI art. 10), obligatorio**: nombre y apellidos o razón social, NIF y domicilio. Falta tu NIF.
2. Cargar los textos también en *Configuración → Políticas* de Shopify, para que aparezcan en el checkout. La conexión de Claude no tiene el permiso `write_legal_policies`, así que es copiar y pegar desde `politicas/`.
3. No enlazar la plataforma ODR de la UE: se cerró el 20/07/2025.

## 3. Interfaz — qué funciona en 2026 y qué aplicar

Tendencias con impacto en conversión (no decorativas):
1. **Slider antes/después arrastrable** (foto real → retrato). Es *el* banner que describes, y para este nicho es la prueba de producto más convincente. Horizon lo trae de serie (bloque `comparison-slider`). En Craft necesitarías una app.
2. **Hero de vídeo corto** (6–10 s, en bucle y sin sonido): alguien desembala el cuadro y lo cuelga. El bloque `video` de Horizon lo soporta.
3. **Reseñas con foto**: Judge.me (plan gratuito). Importa las reseñas de Etsy y añade las estrellas del bloque `review` de Horizon y el marcado estructurado para Google. **Nunca reseñas inventadas**: son ilegales en la UE (Directiva Ómnibus) y Shopify y Google penalizan.
4. **Marquee de confianza**: "Envío con seguimiento · Garantía de 3 años · Diseñado y revisado uno a uno · Pago seguro". Bloque `marquee` de Horizon.
   ⚠️ No usar "hecho a mano" ni "pintado a mano": con diseños IA sería publicidad engañosa (y en Etsy, motivo de retirada).
5. **"Cómo funciona" en 3 pasos** (sube fotos → te enviamos vista previa → lo recibes listo para colgar).
6. **FAQ en acordeón** en la ficha: calidad de la foto, plazos, vista previa, marcos.
7. Sticky add-to-cart en móvil (Horizon lo trae).
8. Evitar: carruseles automáticos de 5 slides en el hero (cada vez convierten menos), pop-ups de entrada y fuentes pesadas.

**Plan de ejecución:** construir la portada y la ficha en Horizon (sin publicar), revisarlas con la vista previa, volver a añadir los bloques de Easify y Uploadfly en la plantilla de producto de Horizon, probar un pedido y publicar.

## 4. Etsy

### ¿Vincular con el proveedor o subir sin vincular para medir la demanda?
**Vincular desde el primer día, con aprobación manual de pedidos.** Motivos:
- Tu producto **no se puede producir automáticamente**: tras la compra tienes que crear la ilustración a partir de las fotos del cliente. El "filtro" en medio es obligatorio en la práctica.
- Gelato (y Printify) permiten *manual approval*: el pedido de Etsy se sincroniza y queda retenido hasta que adjuntas el diseño final y lo apruebas. Así mides la demanda igual (el anuncio es idéntico) sin riesgo de pedidos sin preparar.
- Con un anuncio sin vincular, cada pedido lo creas a mano en Gelato: más errores y no se sincroniza el seguimiento con Etsy. Los envíos tardíos bajan tu *Star Seller* y la visibilidad.

### Normas de Etsy que te afectan (2025–2026)
- Debes **declarar a Gelato como "production partner"** en la tienda y en cada anuncio.
- Si la ilustración se hace con IA, hay que **declararlo en la descripción**. No cumplirlo es la causa nº 1 de suspensiones en POD.
- Categoría correcta: "Designed by" (diseñado por ti, producido por un socio).

### Comisiones (vendedor en España)
0,20 $ por anuncio + 6,5 % de transacción + 4 % + 0,30 € de procesamiento de pago + 0,72 % de tasa regulatoria. Offsite Ads: 15 % (obligatorias a partir de 10.000 $ de ventas anuales). **Coste total aproximado: 12 % sin Offsite Ads y 27 % con ellas.** Hay que tenerlo en cuenta en el precio: en Etsy, precio un 10–15 % superior al de kivoa.es, o envío incluido en el precio.

### Por qué Etsy primero para validar
El nicho "pet memorial / pet portrait" tiene demanda probada en Etsy y mucha competencia en EE. UU. **La ventaja está en ES/EU**: anuncios en español, alemán, francés e italiano, con envío europeo en 4–8 días. Las reseñas de Etsy se importan después a Shopify con Judge.me.

## 5. Proveedores POD de cuadros enmarcados (EU)

| Proveedor | Modelo | Fortalezas | Debilidades | Encaje |
|---|---|---|---|---|
| **Gelato** | Red (140+ imprentas, 32 países) | Producción local en ES/EU, envío rápido, Etsy + Shopify, aprobación manual y Personalization Studio | La calidad varía según la imprenta; quejas de embalaje en formatos grandes/aluminio | ✅ Bueno para empezar |
| **Prodigi** | Propio (UK + EU) | Calidad de galería más consistente en papeles fine art y marcos | Más caro; menos marcos "baratos" | ⭐ Mejor calidad; candidato para una línea premium |
| **Printful** | Propio (incl. España y Letonia) | Control de calidad propio, marca blanca, planta en España | Precio más alto en pósters enmarcados que Gelato | Alternativa sólida |
| merchOne | Propio (PL, DE, LV) | Especialistas en wall art EU | Menos integraciones/personalización | Plan B |
| Printify | Red | Precio | Calidad muy variable según la imprenta; poco foco en marcos | ❌ Para cuadros, no |

**Conclusión:** Gelato está entre los 3 mejores para tu caso (producción en España/UE + Etsy + aprobación manual), pero no es el mejor en calidad pura: ese es Prodigi. Recomendación:
1. Pedir **muestras propias** a Gelato, Prodigi y Printful del mismo diseño (30×40 con marco de madera) a tu dirección. Evaluar papel, marco, embalaje y plazo real a Cádiz. Cuesta unos 100 € y es la mejor inversión del mes.
2. Quedarse con **un solo** proveedor en Shopify (ahora mismo están instalados Printful y Gelato: riesgo de pedidos duplicados o huérfanos).

## 6. Ampliación de catálogo (mismo diseño, más soportes)

Reutilizar la misma ilustración y el mismo flujo de fotos del cliente eleva el ticket medio sin trabajo creativo extra:

| Producto | Soporte POD | Por qué |
|---|---|---|
| Lienzo (canvas) | Gelato/Prodigi | Mayor precio percibido; upsell natural |
| Bola/adorno de Navidad con retrato | Printful/Gelato | Temporada Q4: empezar a anunciar en octubre |
| Taza con retrato | Todos | Ticket bajo, regalo para terceros |
| Manta/cojín | Printful | Alto margen, muy de "memorial" |
| Portarretratos de madera / pizarra grabada | Proveedor especializado | Tendencia "memorial stone" |
| Vela con etiqueta personalizada | Local o artesano | Tendencia pet loss 2026 |
| Tarjeta de condolencia + retrato digital | Descarga digital | Margen del 100 %; para veterinarios y amigos |
| **Pack "Recuerdo"**: cuadro + taza + tarjeta | Combo | AOV ×1,6 |

Nuevas líneas de estilo (mismo producto): acuarela, línea minimalista, "Arcoíris" (*Rainbow Bridge*), retrato de familia con mascota y retrato **en vida**. No solo memorial: el mercado de mascotas vivas es más grande y compra todo el año.

B2B: acuerdo con **clínicas veterinarias y crematorios de mascotas** de Cádiz/Málaga (tarjeta con QR y descuento). Es el canal de adquisición más barato y más cualificado del nicho.
