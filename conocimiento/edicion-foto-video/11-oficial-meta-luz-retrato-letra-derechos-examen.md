# Ronda 7 (final): especificaciones OFICIALES de Meta, luz en casa, retrato de marca personal, combinar letras, miniaturas, derechos, examen

Fuentes: **Guía de anuncios de Meta** (facebook.com/business/ads-guide, leída directo el 2026-10-23) [oficial]; Blackmagic Design, página oficial de entrenamiento DaVinci Resolve 20 [oficial]; Meta Transparency, norma "Brand endorsement" y Oversight Board, decisión FB-O7AI7UAX (2025) [oficial]; guías de luz de 3 puntos (GVM, Unique Photo, GoTranscript) [blog/experto]; LinkedIn Learning, Univ. de Huddersfield, McMaster (foto de perfil) [oficial/universidad]; SketchDeck, Visme, MyFonts, Adobe (combinar letras) [experto]; vidIQ, Miracamp (miniaturas) [blog].

## 1. Medidas OFICIALES de Meta (confirmadas en la guía de anuncios)
| | Feed de Facebook (video) | Facebook Reels |
|---|---|---|
| Proporción | **4:5** | **9:16** |
| Resolución recomendada | **1440 x 1800** | **1440 x 2560** |
| Video | MP4/MOV, H.264, píxeles cuadrados, fps fijos, escaneo progresivo | igual |
| Audio | AAC estéreo **128 kbps o más** | igual; sonido "muy recomendado" |
| Subtítulos | opcionales, recomendados | recomendados; los subtítulos automáticos de Meta **NO** funcionan en Reels → quemarlos en el video |
| Texto principal | 50-150 caracteres | **40 caracteres** |
| Título | 27 caracteres | 55 caracteres |
| Zona segura | — | dejar libre **14% arriba, 35% abajo, 6% a cada lado** (oficial) |
| Peso máximo | 4 GB | — |
Ojo: con objetivo "Reconocimiento" en feed móvil, el pie del anuncio (título, descripción, botón) NO se muestra → el mensaje y la llamada a la acción deben ir DENTRO del video.
Mis herramientas ya renderizan a 1440x2560 (render_html.py) y quemo subtítulos (subtitulos.py).

## 2. Luz para grabarse hablando (barato)
- Luz principal = ventana de lado (45°). Relleno = una pared blanca o la luz del cuarto del otro lado. Contraluz = una lámpara detrás, fuera de cuadro, que separa de la pared.
- Una buena luz principal vale más que varias mal puestas.
- Fondo más oscuro que la cara (si no, sale silueta).
- Teléfono a la altura de los ojos (más abajo = se ve "desde arriba" al público); ojos en el tercio superior, poco aire arriba. Trípode con pinza ~Q150-250.
- Para leer guion: el texto pegado al lente (app de teleprompter) y pararse un poco lejos para que no se note el movimiento de ojos.

## 3. Foto de perfil / marca personal (Javier como experto en IA)
- Luz suave: día nublado o de frente/lado a una ventana; nunca contraluz, flash ni foco fluorescente (verde, cansado).
- Teléfono a la altura de los ojos, alejarse y hacer un poco de zoom (de cerca deforma la nariz). Encuadre de pecho para arriba; la cara ~60% del cuadro.
- Fondo liso (pared gris/blanca/azul suave) o modo retrato.
- Mirar al lente con media sonrisa (se percibe más simpático y competente).
- Truco: grabar 10 s de video y sacar el mejor cuadro (más natural que 20 selfies tiesas).
- Ropa como para una reunión de negocios.

## 4. Combinar tipos de letra
- Lo más seguro: una con serifa + una sin serifa. Máximo 2-3 letras por pieza.
- Nunca dos letras casi iguales (se ve error); excepción: pesos distintos de la misma familia.
- Contraste por tamaño, grosor, espacio o color, no solo por tipo de letra.
- Letra "de exhibición" (Anton, Archivo Black, Playfair) solo para titulares; el texto en una sencilla.
- En pantalla, la diferencia de grosor tiene que ser grande (light vs. medium se ven iguales en el teléfono).
- Pares probados: Anton + Oswald (cartel de deporte, usado en la gorra), Archivo Black + IBM Plex Mono (técnico, usado en la sierra), Playfair Display + Montserrat (elegante).

## 5. Miniaturas (YouTube 1280x720 / portadas)
- 3 elementos máximo (cara expresiva o producto + 3-5 palabras + fondo de contraste).
- Texto que complementa el título, no lo repite.
- Lo importante al centro (la hora del video tapa la esquina de abajo a la derecha).
- Las cifras de "+CTR" son de vendedores: probar con las propias estadísticas.

## 6. Derechos y reglas (para no perder anuncios ni meterse en problemas)
- Meta prohíbe usar la imagen de un famoso como "carnada" para que la gente le dé clic, y las recomendaciones falsas o engañosas de figuras públicas (Oversight Board 2025).
- Prohíbe dar a entender que Facebook, Instagram o WhatsApp recomiendan o son socios del anunciante.
- **Gorra Benavidez:** se puede decir lo que ES ("gorra ThirtyOne x David Benavidez, original, numerada") porque es el nombre del producto. NO usar fotos de él, ni frases como "recomendada por Benavidez" o "el campeón te la manda". En Marketplace va bien; en un anuncio pagado hay riesgo de rechazo → poner al producto de protagonista.
- Música y efectos: solo con licencia o sintetizados (sonido.py).
- Personas en video (clientes): pedir permiso antes de publicar su cara.

## 7. Manual oficial de DaVinci Resolve 20
6 libros oficiales con PDF de descarga en blackmagicdesign.com (Principiantes, Editor, Audio Fairlight, Colorista, Efectos Visuales, Efectos Avanzados [este último pide la versión Studio de pago]). El PDF de principiantes pesa más de 10 MB y no se puede leer con mis herramientas sin descargarlo; sus temas (organizar material, editar, recortar, audio, color, entrega) ya están cubiertos en los archivos 2-9.

## 8. Examen final (2026-10-23): pieza completa desde cero
**Sierra Bosch, concepto "plano técnico"** (distinto al "cartel de pelea" de la gorra): fondo de plano azul con cuadrícula que se desliza, título que se escribe como en computadora, la sierra entra en el cuadro 1 con golpe de zoom, una línea de escáner, 4 llamadas con los datos REALES de la placa (0-2,800 cortes/min, 120 V · 12 A, carrera 32 mm, maletín) que se dibujan solas, sello rojo "PROBADA", y el cajetín del plano cambia a "PRECIO FINAL · Q600". Sonido sintetizado: clics en cada dato, golpe en el sello, whoosh y ding en el precio.
Revisión con revisar.py: la primera versión FALLÓ (gancho débil, 3 momentos quietos, pico +1 dB). Se corrigió: aparición en el cuadro 1, movimiento continuo, volumen en 2 pasos (medir → ajustar). Versión final: 1440x2560, 11 s, -15.2 LUFS, pico -1.5 dB, sin congelados, gancho con movimiento. **APROBADA.**
Archivo: `Escritorio\Fotos Marketplace PRO\Videos\sierra_plano.mp4` (fuente en disenos/sierra.html).
