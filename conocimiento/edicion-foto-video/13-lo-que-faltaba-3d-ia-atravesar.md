# Cómo resolví lo que me faltaba de Higgsfield (gratis)

Fuentes: Hugging Face Spaces (TRELLIS.2 de Microsoft —licencia MIT—, Stable Fast 3D de Stability, Hunyuan3D-2/2.1 de Tencent, TripoSG de VAST) probados en vivo [oficial]; triposr.org, trellis2.app, Cmarix, Cinevva, 3D AI Studio (comparativas de foto a 3D 2026) [blog]; Dreamina/CapCut, InVideo, Shhots, Pexo (planes gratis de foto a video 2026) [blog, cambian seguido]; HeyGen, Magic Hour (avatares) [vendedor]; Affiverse, Commonthread, CO/AI (etiqueta de IA de Meta 2026) [blog]; model-viewer de Google (visor 3D) [oficial].

## La PC de Javier
Intel i5-1135G7, gráficos Intel Iris Xe (sin tarjeta NVIDIA), 7.7 GB de RAM, 55 GB libres. → Los modelos de IA de video/3D NO corren en la PC. Solución: correrlos en servidores gratis (Hugging Face) controlados desde la PC, o usar los planes gratis de las páginas.

## 1. Girar el producto 360° desde UNA foto (Lazy Susan / 360 Orbit / Bullet Time)
**Paso A — foto → modelo 3D** con `foto_a_3d.py`: prueba en orden Stable Fast 3D → TRELLIS.2 → Hunyuan3D-2.1 en Hugging Face y guarda el .glb.
- Probado 2026-10-23: los 5 servidores responden; sin cuenta el límite es de ~3 minutos de servidor al día ("ZeroGPU quota") y se agotó en el primer intento → con **cuenta gratis de Hugging Face** el límite sube.
- Licencias: TRELLIS.2 = MIT (uso comercial libre). Stable Fast 3D = licencia comunitaria de Stability (gratis para negocios con menos de US$1 M al año). Hunyuan3D = licencia de Tencent (excluye UE, Reino Unido y Corea; revisar condiciones).
- Alternativas web gratis: 3D AI Studio (~100 créditos/mes), Hunyuan 3D de Tencent (~20 al día), Tripo (200-300 créditos/mes, NO comercial en gratis).
**Paso B — modelo 3D → video girando** con `orbita_3d.html` + `render_html.py` (visor 3D de Google dentro de Chrome): giro suave de 360°, la cámara sube un poco a la mitad, sombra en el piso, fondo según la dirección de arte. Probado con un modelo de muestra: funciona (4 s en 24 s de render).
Comando: `render_html.py "C:/.../orbita_3d.html?m=file:///C:/.../producto.glb&fondo=0b0d10&fondo2=2a2f38&dur=6" salida.mp4`
Ojo: la IA inventa la parte de atrás que no se ve en la foto → revisar que el producto se vea como el real; si no, NO usarlo en venta (sería engaño). Mejor: 2-3 fotos del producto (frente, lado, atrás) o la base giratoria real.

## 2. Que la cámara atraviese un objeto (Through Object)
`atravesar.html`: la cámara se mete dentro de la SILUETA del producto (recortada con recortar.py) y adentro aparece la escena siguiente; al final llena toda la pantalla. Hecho con canvas (las máscaras CSS no funcionan con archivos locales). Probado con la gorra: funciona.
Uso creativo: gorra → se atraviesa → aparece el ring; camarón → se atraviesa → aparece el plato servido; sierra → se atraviesa → aparece la madera cortada.

## 3. Video generado con IA (cuando la foto no alcanza)
Planes gratis 2026 (confirmar en cada página; cambian seguido):
| Página | Gratis | Uso comercial |
|---|---|---|
| Dreamina (Seedance, de CapCut) | ~120 créditos/día (EE. UU.; varía por país) | Permitido según varias guías, sin marca de agua |
| Google Flow / Veo | ~50 créditos/día | Revisar |
| Kling | 66 créditos/día | Con marca de agua y NO comercial en gratis |
| Hailuo (MiniMax) | Créditos al registrarse + diarios | Fuentes se contradicen |
| Runway | 125 créditos una sola vez | — |
Modelos abiertos (WAN) en Hugging Face también, con el mismo límite diario que el 3D.

## 4. Personas con IA (UGC) — con reglas
- Opción honesta y que más vende: **Javier como su propio avatar** (su cara y su voz). HeyGen (gratis con avatares de stock; avatar propio en plan de pago ~US$29/mes), Magic Hour (foto que habla, 3 usos/día gratis, 480p).
- **Meta 2026:** los anuncios con personas realistas hechas con IA llevan etiqueta "Información de IA"; Meta etiqueta solo si detecta IA (metadatos C2PA).
- **Prohibido/engaño:** testimonios falsos ("clienta feliz" que no existe), famosos falsos, mostrar el producto distinto. En Guatemala y en las reglas de Meta, el testimonio debe ser de un cliente real.
- Uso correcto: avatar de Javier explicando la oferta, voz en off, o una persona IA SOLO como "presentadora", nunca como cliente.

## 5. Lo que tiene que hacer Javier (yo no puedo crear cuentas ni manejar contraseñas o tokens)
1. Crear cuenta gratis en huggingface.co (con su correo).
2. En huggingface.co/settings/tokens → "Create new token" → tipo "Read" → copiarlo.
3. Abrir PowerShell y escribir él mismo: `setx HF_TOKEN "su_token"` (así queda guardado en su PC y yo nunca lo veo).
4. Opcional: cuenta gratis en Dreamina (dreamina.capcut.com) y en Google Flow para video con IA.
Después: Linderman corre foto_a_3d.py, orbita_3d.html, atravesar.html y arma las piezas.
