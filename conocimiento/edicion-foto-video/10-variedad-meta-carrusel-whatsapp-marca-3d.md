# Ronda 6: variedad creativa (Meta Andromeda), carruseles, estados de WhatsApp, kit de marca, 3D, control de calidad

Fuentes: agencias sobre Andromeda (Atria, Jetfuel, 303 London, Skaleit, Nikhil.pro, Chatterbuzz) [blog-sin-verificar; Meta no publica los números]; HubSpot DE y Strike Social (carruseles) [blog]; Lightricks, Infobip (cita IDC), Greenbook (WhatsApp en Latinoamérica) [blog/industria]; Elegant Themes, Zoviz (kit de marca) [blog]; BlenderNation, CGTrader (escaneo 3D con teléfono) [experto/comunidad].

## 1. Por qué la VARIEDAD es obligatoria (Meta Andromeda, 2025-2026)
- El sistema de Meta agrupa los anuncios que se PARECEN (misma toma, mismo concepto, solo cambia el color o el texto) como si fueran UNO solo ("ID de entidad"). 10 anuncios casi iguales = 1 boleto a la subasta.
- Lo que cuenta como distinto: otro FORMATO (demo vs. testimonio vs. unboxing vs. foto de estudio) u otro CONCEPTO/ángulo (precio, frescura, entrega, confianza). Cambiar fondo, botón o una palabra no cuenta.
- Mínimo citado: ~6 creatividades realmente distintas por conjunto de anuncios; cuentas grandes 15-25. [agencias, sin dato oficial]
- Esto confirma la regla de Javier: NADA de plantillas. Cada pieza con concepto propio.
Para Javier (presupuesto chico): 3-6 piezas distintas por campaña, por ejemplo: (1) Javier hablando con subtítulos, (2) demostración/unboxing, (3) diseño animado con precio, (4) captura de chat o testimonio de cliente.

## 2. Carrusel (feed de Facebook/Instagram)
- Las tarjetas deben verse como UNA serie coordinada (misma paleta y letra); 10 fotos sueltas sin relación no convencen.
- Tarjeta 1 = gancho (la razón para deslizar); las siguientes cuentan una historia o un paso a paso; la última = precio + llamada a la acción.
- Truco de continuidad: un elemento que "cruza" de una tarjeta a la siguiente invita a deslizar.
- Medida usada: 1080x1350 (4:5) o 1080x1080. [confirmar en la guía de Meta; las fuentes no lo citan]
Herramienta: `render_html.py diseño.html salida_%02d.png` con `window.FOTOS = [t1, t2, ...]` = todas las tarjetas del mismo diseño.

## 3. Estados de WhatsApp (canal #1 en Guatemala)
- +90% de los latinoamericanos usa WhatsApp; 51.3% prefiere recibir ofertas por WhatsApp Business (IDC citado por Infobip).
- El estado dura 24 h y lo ven SOLO tus contactos → sirve para clientes que ya tienes (recompra), no para clientes nuevos.
- Qué subir: "llegó hoy" (frescura), cuenta regresiva de oferta, detrás de cámaras (pesando, empacando, entregando), producto nuevo, testimonios.
- Formato: vertical 9:16; videos cortos (WhatsApp corta los videos largos en partes; ~30 s por parte según uso común [verificar en ayuda oficial]).
- No saturar: pocos estados con oferta de valor; demasiados = la gente deja de verlos.

## 4. Kit de marca (lo mínimo para un negocio chico como Don Gencho)
1. Logo principal + versión simple (ícono) + versiones para fondo claro y oscuro, en PNG transparente.
2. Paleta corta con códigos exactos (hex) — 1 dominante, 1 secundario, 1 acento.
3. Dos tipos de letra (titular y texto).
4. Reglas de uso del logo (espacio alrededor, tamaño mínimo, qué no hacer).
5. Voz de la marca: 3 palabras (ej. "fresco, directo, de confianza") + una frase de ejemplo.
6. Plantillas base: portada de página, estado, tarjeta de precio, firma de WhatsApp.
Regla: la marca da CONSISTENCIA (se reconoce), el concepto de cada pieza da VARIEDAD (Andromeda). Las dos cosas juntas.

## 5. 3D del producto
- Camino gratis: escanear el producto con el teléfono (app KIRI Engine, gratis con límites) → limpiar y animar en Blender (gratis) → video girando 360° o en escena.
- Los archivos salen pesados (hasta ~2 GB) y Blender pide buena PC. Vale la pena para productos de valor (herramientas, repuestos), no para mariscos.
- Alternativa sin 3D: girar el producto en una base (plato giratorio) y grabar 360° con el teléfono fijo.

## 6. Control de calidad antes de entregar (`revisar.py`)
Revisa: proporción y resolución, códec compatible con Meta, fps, duración (6-15 s ideal, 30 máx.), volumen (-14 LUFS, pico ≤ -1 dB), cuadros negros, imagen congelada (>1.2 s = pierde ritmo), movimiento en los primeros 3 s (gancho), y hoja de cuadros con las zonas que tapa la app en rojo.
Se corre SIEMPRE antes de mostrarle una pieza a Javier.
