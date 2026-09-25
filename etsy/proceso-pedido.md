# Protocolo de pedido · Etsy (ByKivoa) + Gelato

## ANTES de la primera venta (comprobar una vez)

| ✔ | Qué | Dónde | Por qué |
|---|---|---|---|
| ☐ | **Aprobación manual de pedidos ACTIVADA** | Gelato → Settings → Order approval / Order submission → *Manual* | **Crítico.** Si está en automático, Gelato imprime el diseño de muestra (Luna/Penny) y lo envía al cliente sin esperarte. |
| ☐ | Tarjeta en Gelato | Gelato → Billing / Payment methods | Gelato cobra la producción al aprobar el pedido. Sin tarjeta, el pedido se queda parado. |
| ☐ | Personalización activada en cada anuncio | Etsy → anuncio → Personalización | Sin ella, el comprador no puede darte nombre, fecha ni frase. |
| ☐ | Envío gratis, sin Reino Unido | Etsy → Configuración de envío → perfil de Gelato | Evita cobrar el envío dos veces y el problema del IVA británico. |
| ☐ | Tiempo de preparación 3–6 días laborables | Etsy → perfil de preparación | Si Etsy promete fechas que no cumples, pierdes posicionamiento y Star Seller. |
| ☐ | App de Etsy Seller en el móvil con notificaciones | Móvil | Responder en < 24 h es obligatorio para Star Seller. |

---

## CUANDO ENTRA UN PEDIDO

### Día 0 · En menos de 24 h
1. **Etsy** te avisa del pedido y **Gelato** lo recibe como *"Awaiting approval"* (retenido). **No lo apruebes todavía.**
2. Revisa en el pedido de Etsy: **estilo, tamaño, marco** y el campo de **personalización** (nombre, fecha, frase, rasgos).
3. Etsy envía automáticamente el **Mensaje para compradores** pidiendo las fotos. Si a las 24 h no las ha mandado, recuérdaselo por **mensaje de Etsy** (nunca por email ni WhatsApp: todo por Etsy, queda registrado y te protege).
4. Revisa las fotos: nítidas, con buena luz y la cara visible. Si no valen, pide otras **ya**, antes de empezar a diseñar.

### Día 1–2 · Diseño (máximo 48 h laborables desde que tienes las fotos)
5. **Ilustración principal** en ChatGPT, con el prompt fijo del estilo.
6. **Montaje**: sustituir las fotos secundarias por las originales (generador) y revisar los textos **letra a letra** contra el campo de personalización (nombre, fechas en el formato pedido, tildes).
7. Exportar:
   - **Archivo de impresión** con la proporción y la resolución del tamaño comprado:
     - 20×25 → 2362×2953 px
     - 30×40 → 3543×4724 px
     - 50×70 → 5906×8268 px
   - **Vista previa** en baja resolución con marca de agua "VISTA PREVIA · KIVOA".

### Vista previa y cambios
8. Envía la **vista previa por mensaje de Etsy** con esta plantilla:
   > ¡Hola, [nombre]! Aquí tienes la vista previa del retrato de [mascota] 🐾
   > Revísala con calma: nombre, fecha, frase y fotos. Tienes 2 rondas de cambios incluidas (textos, colores, recortes, detalles).
   > Cuando esté perfecta, respóndeme con **"Apruebo"** y lo enviamos a producción (2–4 días laborables + envío con seguimiento).
9. Cambios: máximo **2 rondas**. Un cambio de estilo o fotos nuevas es un pedido nuevo (términos, apartado 6).
10. **No produzcas nada sin un "Apruebo" por escrito** en los mensajes de Etsy. Esa aprobación es tu protección ante reclamaciones.
11. Si no responde: el **día 7** mandas el recordatorio (plantilla en `plantillas/correos-vista-previa.md`). Si sigue sin responder, produces la última versión enviada y se lo avisas por mensaje.

### Producción (Gelato no permite cambiar el diseño de un pedido: se hace con pedido manual)
12. En **Gelato → Pedidos**, el pedido llega como *Pending approval* con el diseño de muestra. **Cancélalo** ("Cancel order"): no se cobra nada.
13. **Gelato → Pedidos → Crear pedido** (pedido manual):
    - Producto: *Classic Semi-Glossy Paper Wooden Mounted Framed Poster* · tamaño y marco **del pedido**.
    - Sube el **archivo final** con la proporción exacta (20×25 → 2362×2953 · 30×40 → 3543×4724 · 50×70 → 5906×8268 px).
    - Dirección del cliente: cópiala **exacta** del pedido de Shopify/Etsy (con el número y el piso).
    - Referencia: el número de pedido de Shopify/Etsy (ej. `#1001`), para cruzarlos después.
    - Revisa la vista previa (nada recortado) → **Pagar / Enviar a producción**.
14. Cuando Gelato envíe (2–4 días laborables), copia el **número de seguimiento** y:
    - **Shopify:** pedido → **Marcar como preparado** → pega transportista y seguimiento → el cliente recibe el aviso.
    - **Etsy:** pedido → **Marcar como enviado** → pega el seguimiento.
    (En un pedido manual el seguimiento no se sincroniza solo.)
### Después de la entrega
15. **2–3 días después de la entrega**, mensaje de seguimiento:
    > ¡Hola, [nombre]! ¿Ha llegado bien el retrato de [mascota]? Esperamos que os encante. Si te apetece, una reseña en Etsy nos ayuda muchísimo a seguir creando. ¡Gracias! 🐾
    (Nunca ofrezcas nada a cambio de la reseña: está prohibido.)
16. **Contabilidad**: guarda la factura de Gelato y apunta la venta (precio, IVA, comisiones de Etsy). Lo necesitas para el IVA y el IRPF.
17. **Privacidad**: borra las fotos del cliente **90 días** después de la entrega (lo prometemos en la política).

---

## Si algo sale mal
| Situación | Qué hacer |
|---|---|
| Llega dañado (roto, marco golpeado) | Pide fotos del cuadro **y del embalaje** → reclamación en Gelato (*Report an issue*) → Gelato suele reimprimir gratis. Al cliente: reimpresión o reembolso, lo que prefiera. |
| Error de texto **nuestro** (distinto de la vista previa aprobada) | Reimprimimos gratis. Lo pagas tú: por eso hay que revisar letra a letra. |
| Error de texto **del cliente** (aprobó la vista previa con el error) | No es un defecto. Le ofreces una nueva impresión con descuento, si quieres. |
| Quiere cancelar **antes** de aprobar | Reembolso íntegro desde Etsy. No se ha producido nada. |
| Quiere cancelar **después** de aprobar | No se admite: es un producto personalizado ya en producción. Explícalo con amabilidad y cita los términos. |
| No llega en plazo | Revisa el seguimiento en Gelato. Si está perdido, Gelato reenvía. |

---

## Tiempos objetivo (Star Seller)
- Responder mensajes: **< 24 h**
- Vista previa: **< 48 h laborables** desde que tienes las fotos
- Envío con seguimiento: **siempre**
- Enviar a tiempo: **≥ 95 %** de los pedidos
