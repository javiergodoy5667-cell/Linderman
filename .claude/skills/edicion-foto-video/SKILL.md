---
name: edicion-foto-video
description: Experto en edición de foto y video para vender: mejorar fotos originales, hacer Reels/Historias/anuncios 9:16 y 4:5 desde fotos o clips, con texto en zona segura y música. Usar cuando Javier diga "edita", "haz un video", "reel", "historia", "video para anuncio", "mejora esta foto" o mande fotos/clips para publicar.
---

# Edición de foto y video

Conocimiento: `conocimiento/edicion-foto-video/` (1 foto, 2 video corto, 3 herramientas, 4 expertos, 5 pepitas).
Foto de estudio con fondo quitado: usar la habilidad **foto-pro** (`foto_estudio.py`).

## Herramientas (ya instaladas)
- Python 3.12: `C:\Users\casaa\AppData\Local\Programs\Python\Python312\python.exe` (siempre con `-I`).
- FFmpeg 9.0 (winget): el script lo encuentra solo.
- Scripts en `.claude/skills/edicion-foto-video/scripts/`.

## Elegir qué hacer
| Caso | Herramienta |
|---|---|
| Producto solo, fondo simple, contorno limpio | foto-pro → `foto_estudio.py` |
| Producto en bolsa, hielo, vidrio, o Javier quiere la foto real | `foto_mejorar.py` (luz, color, nitidez; 1x1 Marketplace, 4x5 feed) |
| Video para Reels/Historias/anuncio desde fotos | `video_producto.py` formato 9x16 (y 4x5 para feed) |
| Video con voz o clips grabados | Pedir clips a Javier; recortar/unir con FFmpeg; subtítulos: Javier en CapCut/Clipchamp (automáticos) |

## Pasos video desde fotos
1. Escribir `guion.txt` (una escena por línea: `ruta_foto | texto`). Estructura 15 s: gancho (0-3 s) → prueba → oferta (precio, entrega) → llamada a la acción. 4-6 escenas, texto corto (máx. 5-6 palabras).
2. Correr: `python -I video_producto.py <salida.mp4> <guion.txt> [musica.mp3|-] [9x16|4x5]`. Cada escena dura 2.4 s con zoom suave y fundido.
3. Revisar sacando cuadros: `ffmpeg -i video.mp4 -vf "select='eq(n\,20)+eq(n\,95)+...',scale=270:-1,tile=4x1" -frames:v 1 hoja.jpg` y verla con Read. Revisar que el texto no tape el producto ni salga de la zona segura.
4. Guardar en `Escritorio\Fotos Marketplace PRO\Videos\` y abrirle la carpeta a Javier. Esperar su OK antes de publicar.
5. Música: solo con licencia (biblioteca de Meta/CapCut). Si no hay, el video sale con audio en silencio (válido para Meta).

## Reglas de calidad
- Primeros 3 s: producto o resultado + gancho. Nunca logo ni saludo.
- Texto: blanco grueso con sombra suave, arriba-centro (debajo del 14% superior). Nada en el 35% de abajo.
- Debe entenderse sin sonido.
- Marketplace: fotos SIN texto (regla de Javier). El texto va solo en videos/anuncios.
- Color +5-10% máximo.

## Errores encontrados
- Texto encima de la foto: el script recorta el margen vacío y pone el producto al 60% de la altura; textos largos (>28 letras) bajan a letra más chica.
- Zoom que tiembla: se trabaja la imagen al doble de tamaño antes del zoom.
- Recorte de fondo falla con bolsas transparentes → usar `foto_mejorar.py`.
- La página oficial de Meta (Ads Guide) no cargó con Chrome automatizado; medidas tomadas del estudio anterior de meta-ads.
