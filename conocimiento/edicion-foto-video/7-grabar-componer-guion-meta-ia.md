# Ronda 3: grabar con el teléfono, componer, guion de anuncio, mariscos, portadas, IA de Meta

Fuentes: Pro Video Coalition (regla de 180°), UCLA Arts (*Mobile Video Recording Best Practices*), St. Lawrence Univ., Teleprompter.com [curso/experto]; Nikon USA, UNC, Univ. de Newcastle (composición y tipos de plano) [experto]; Motion y Selzee (guiones UGC) [industria]; Champagne Tastes y PicBackMan (foto de mariscos) [blog]; Planoly, SocialKit, Templated (portadas de Reels) [blog, se contradicen]; AdsUploader, Flighted, SparkUGC, Leapbuzz (Advantage+ creativo 2026) [blog-sin-verificar].

## 1. Grabar con el teléfono (lo que Javier hace)
1. Limpiar el lente con la camisa (la causa #1 de video "lechoso").
2. **Bloquear exposición y enfoque:** mantener el dedo en el producto hasta que diga "Bloqueo AE/AF" (iPhone) o tocar y bloquear (Android). Si no, la luz "respira" y se ve aficionado.
3. 1080p o 4K a **30 fps** para redes; **60 fps** solo si se quiere cámara lenta (camarón cayendo al hielo, aserrín saltando).
4. Regla de 180°: obturador = 2 × fps (1/60 a 30 fps). En modo automático no se controla; con la app gratis **Blackmagic Camera** sí.
5. Teléfono vertical, a la altura del producto, apoyado (pared, vaso, trípode barato). Moverse despacio, nunca zoom digital.
6. Audio: lugar callado, sin ventilador ni tráfico; teléfono a menos de 1 metro de la boca, o un micrófono de solapa (~Q100-200). Afuera: tapar el micrófono del viento.
7. Grabar 3-5 segundos de más al inicio y al final de cada toma (para cortar limpio).

## 2. Lista de tomas para un producto (10-15 tomas de 3-5 s)
- **General:** el producto completo en su lugar.
- **Medio:** el producto en uso (manos).
- **Detalle (primer plano):** textura, marca, etiqueta, número de parte, frescura.
- **Acción:** lo que hace (corta, enciende, se cocina).
- **Persona:** Javier a cámara diciendo el precio y la oferta.
- **Reacción/resultado:** el corte terminado, el plato servido, la planta alumbrando.
Composición: regla de tercios (producto en un tercio, no siempre al centro); con persona, ojos en el tercio superior; dejar espacio hacia donde mira o se mueve. Un plano muy cerrado no lleva "aire" arriba.

## 3. Guion de anuncio (estructura que se repite en los que ganan)
**Gancho → Problema → Solución → Prueba → Llamada a la acción.**
- Gancho: 2-3 s máximo.
- Velocidad al hablar: ~2.5 palabras/segundo → 15 s ≈ 40 palabras; 30 s ≈ 75 palabras.
- Probar 3-5 ganchos distintos con el mismo cuerpo.
- Si es oferta de bienvenida, la oferta puede ir de primero.
Ejemplo mariscos (15 s, ~40 palabras): "¿Camarón que huele a congelador? [problema] Este llegó hoy, mírelo: firme y brillante [prueba]. Jumbo a Q50 la libra, se lo llevo a su casa en Petapa [oferta]. Escríbame al WhatsApp y aparte el suyo [CTA]."

## 4. Mariscos en foto y video (para página y anuncios; Marketplace los prohíbe)
- Luz suave de ventana o sombra; nunca flash ni sol directo (quema el brillo y cambia el color).
- Hielo picado = frescura y contraste. Bandeja blanca o plato mate blanco y poco hondo.
- Crudo: brillo con un rocío de agua justo antes de la toma. Cocinado: fotografiar en los primeros minutos (se arruga y se opaca al enfriar); mejor un poco crudo que pasado.
- Salsas al lado o debajo, no encima.
- Tomas que venden: mano levantando un camarón jumbo (tamaño real), camarón cayendo al hielo en cámara lenta, la báscula marcando la libra, la bolsa sellada lista para entrega.

## 5. Portada de Reels
- Diseñar a 1080x1920, pero todo lo importante (texto, cara, producto) en la franja central de 1080x1350: el perfil la recorta (las fuentes dicen 4:5, 3:4 o 1:1; probar).
- Subir portada propia, no dejar un cuadro al azar (sale con la boca abierta o borroso).
- Texto corto y de alto contraste: en miniatura lo sutil desaparece.

## 6. Lo que Meta edita solo (Advantage+ creativo) — revisar ANTES de publicar
Meta puede, por su cuenta: retocar la imagen, agregar música, mover o reescribir el texto, ampliar la imagen/video con IA para otras medidas, animar imágenes, agregar superposiciones y tarjetas finales. Varias vienen ENCENDIDAS por defecto y Meta cambia los interruptores seguido.
- **Apagar:** mejoras de texto (cambia el mensaje), superposiciones, música (si el video ya trae audio), animación de imagen, ampliación generada y el "set de prueba con IA".
- **Se pueden dejar:** retoques visuales y ampliación si el producto no se deforma.
- Revisar la vista previa en cada ubicación (Reels, Historias, feed) antes de publicar.

## 7. Estilos disponibles en `video_pro.py` (parámetro 6)
- `premium`: oscuro + dorado, lento (gorra, sierra).
- `catalogo`: claro + azul técnico, datos de compatibilidad (kit Toyota).
- `oferta`: rojo + amarillo, rápido con rebote (liquidaciones, mariscos por libra).
