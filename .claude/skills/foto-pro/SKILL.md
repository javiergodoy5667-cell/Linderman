---
name: foto-pro
description: Convertir fotos de producto de Javier en fotos profesionales (sin fondo, fondo limpio, título, precio y WhatsApp) y ponerlas en Marketplace o la página. Usar cuando diga "fotos profesionales", "las fotos se ven chafas", "mejora las fotos".
---

# Fotos profesionales de producto

## Pasos
1. Buscar la foto ORIGINAL (alta calidad) en la PC: Escritorio, Imágenes, Descargas (PowerShell Get-ChildItem *.jpg recientes). Las de Facebook están comprimidas: no sirven.
2. Correr (Python 3.12, rembg ya instalado):
   `python -I .claude/skills/foto-pro/scripts/foto_pro.py "<carpeta origen>" "<carpeta salida>" "<foto1.jpg,foto2.jpg>" "<Título>" "<subtítulo>" "<Precio>"`
   Salida 1080x1080: fondo degradado claro, sombra, franja oscura con título, etiqueta roja de precio, franja con WhatsApp 5544-9803 · San Miguel Petapa.
3. Revisar cada resultado con Read: descartar las que salgan con la mano pegada o borrosas.
4. Guardar las buenas en Escritorio\Fotos Marketplace PRO\<producto>.
5. Para subir a Facebook: copiarlas al scratchpad (Chrome solo sube archivos de carpetas de la sesión), abrir marketplace/edit/?listing_id=..., subir con file_upload al input de foto, borrar las viejas ("Eliminar foto N de M"), dejar la de frente primero, Actualizar.

## Errores encontrados
- Canva gratis NO quita fondos (pide Pro) → usar rembg local (modelo isnet-general-use).
- Si la mano tapa el producto, rembg la deja pegada: usar fotos donde el producto esté solo o casi solo.
- Fotos del interior/etiquetas: mejor dejarlas originales (prueban autenticidad).
- Consejo para Javier al tomar fotos: producto sobre mesa o pared lisa, luz de día, sin mano, de frente y de lado.
