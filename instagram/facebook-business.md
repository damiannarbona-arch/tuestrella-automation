# Kivoa · Configurar Meta Business (Facebook + Instagram + Shopify)

Tiempo: ≈ 40 min + revisión de Meta (de horas a ~1 semana). Hazlo **desde el ordenador**: en el móvil faltan opciones.
Meta cambia los menús a menudo; si un nombre no coincide, busca la palabra clave en el buscador de la configuración.

---

## 0. Requisito: tu perfil personal de Facebook
Meta no permite crear una página ni una cartera comercial sin un perfil personal que la administre. Usa **tu perfil real** (con uno falso o recién creado Meta suele bloquear la cartera).
- Activa la **autenticación en dos pasos** en ese perfil antes de empezar: la cartera la exige a los administradores.

## 1. Página de Facebook "Kivoa"
`facebook.com/pages/create`
- **Nombre**: `Kivoa`
- **Categoría**: `Tienda de regalos` (añade también `Artista` si te deja una segunda).
- **Biografía**: `Custom pet portraits from your photos. Digital proof in 48h · Nothing prints without your OK. Framed & ready to hang.`
- **Foto de perfil**: la misma que en Instagram.
- **Portada**: el banner de Etsy (`assets/etsy-banner-3360x840.jpg`). Facebook recorta a ~2,7:1 en ordenador: revisa que no se corte el texto.
- **Contacto**: web `https://kivoa.es` · email `contacto@kivoa.es` · **sin teléfono ni dirección**.
- Botón de acción: **Comprar** → `https://kivoa.es`.

## 2. Cartera comercial (Business Portfolio)
`business.facebook.com` → **Crear una cartera comercial**
- **Nombre**: `Kivoa`
- **Tu nombre**: el real.
- **Email de la empresa**: `contacto@kivoa.es` → confirma el correo que te llega.

## 3. Añadir la página y el Instagram a la cartera
`business.facebook.com/settings` (*Configuración de la empresa*):
1. **Cuentas → Páginas → Añadir → Añadir una página** → Kivoa.
2. **Cuentas → Cuentas de Instagram → Añadir** → inicia sesión con el Instagram de Kivoa.
3. Comprueba en **Cuentas vinculadas** de la página que aparece el Instagram. Si no: en la app de Instagram → *Editar perfil → Página → Conectar* → Kivoa.

## 4. Seguridad (evita perder la cuenta)
- *Centro de seguridad* → exigir **2FA a todos los administradores**.
- Añade un **segundo administrador de confianza**. Meta bloquea cuentas sin avisar y con un único administrador la recuperación puede tardar semanas.
- Nunca respondas a mensajes de "tu página infringe normas / copyright" con enlaces: Meta solo avisa dentro de *Calidad de la cuenta*.

## 5. Verificar el dominio kivoa.es
*Configuración de la empresa → Seguridad de la marca → Dominios → Añadir* → `kivoa.es`.

Método: **registro TXT en el DNS** (no la metaetiqueta). Motivo: la metaetiqueta va en el código del tema, y al publicar Horizon en lugar de Craft se perdería y Meta retiraría la verificación.

1. Meta te da un valor: `facebook-domain-verification=xxxxxxxx`.
2. **Si el dominio está gestionado en Shopify**: *Shopify → Configuración → Dominios → kivoa.es → Configuración de dominio → Editar configuración de DNS → Añadir registro personalizado → TXT* · Nombre `@` · Valor el de Meta.
   **Si está en otro registrador** (IONOS, GoDaddy, DonDominio…): lo mismo en la zona DNS de ese registrador.
3. Espera 10–60 min → **Verificar** en Meta.

## 6. Conectar Shopify (catálogo, píxel y tienda de Instagram)
*Shopify → Aplicaciones → Tienda de apps* → **Facebook & Instagram** (desarrollador: Meta) → Instalar → **Empezar configuración**:
1. Conectar tu cuenta de Facebook.
2. **Cartera comercial**: Kivoa · **Página**: Kivoa · **Instagram**: el de Kivoa.
3. **Cuenta publicitaria**: crea una nueva ("Kivoa Ads"), moneda **EUR**, zona horaria **Madrid**. No gasta nada hasta que crees un anuncio; la moneda no se puede cambiar después.
4. **Píxel / Conjunto de datos**: crea uno nuevo, "Kivoa". **Uso compartido de datos: Máximo** (API de conversiones). Es lo que permitirá medir y, más adelante, que los anuncios funcionen.
5. **Catálogo**: crea uno nuevo, "Kivoa". Sincronización automática.
6. Acepta los términos → **Solicitar aprobación** de la tienda (Facebook e Instagram).

## 7. Después de la aprobación
- **Commerce Manager** (`business.facebook.com/commerce`): revisa que los 5 productos estén "Aprobados". Los rechazos suelen deberse a la descripción o a la imagen; corrígelo en Shopify, no en Meta.
- Instagram → *Configuración → Empresa → Compras* → elige el catálogo Kivoa.
- Ya puedes **etiquetar productos** en las publicaciones y aparece el botón **Ver tienda** en el perfil.

## Problemas habituales
| Síntoma | Causa / solución |
|---|---|
| "No puedes crear una cartera comercial" | Perfil personal muy nuevo o con restricciones → espera unos días y usa tu perfil real. No crees perfiles extra. |
| El Instagram no aparece al conectar | La cuenta no es de Empresa → cámbiala (§1 de `configuracion-instagram.md`). |
| La tienda se rechaza | Dominio sin verificar, web sin políticas visibles o pocas publicaciones → repasa §5 y publica las primeras piezas. Puedes pedir una revisión en Commerce Manager. |
| Productos rechazados | Palabras como "memorial" no son el problema; sí lo son las afirmaciones no demostrables ("hecho a mano", "el mejor"). |
