---
name: foto-pro
description: Convertir fotos de producto de Javier en fotos profesionales (sin fondo, fondo limpio, título, precio y WhatsApp) y ponerlas en Marketplace o la página. Usar cuando diga "fotos profesionales", "las fotos se ven chafas", "mejora las fotos".
---

# Fotos profesionales de producto

> **ALCANCE (regla de Javier, 2026-10-23): conocimiento GENERAL de experto.** Sirve para cualquier producto, servicio, negocio, campaña o publicación nueva, hoy o en el futuro. Los mariscos, la sierra, la planta, etc. son solo EJEMPLOS de aplicación; las reglas del negocio actual de Javier (pago contra entrega, sin cuenta bancaria, precios) están marcadas como tales y cambian con el tiempo.


## ESTILO OBLIGATORIO (corrección de Javier, 2026-10-23)
Javier rechazó el diseño con franjas, etiqueta roja de precio y texto encima: "cosas de aficionados".
Lo profesional = **foto de estudio**: producto solo, recortado, fondo gris claro o blanco liso, sombra natural, SIN texto. Precio y contacto van en la descripción.
Usar `scripts/foto_estudio.py` (NO `foto_pro.py`, que queda solo como referencia de lo que NO gustó).
Siempre abrirle a Javier las fotos (carpeta en el Explorador) y esperar su OK antes de subirlas.

## Pasos
1. Buscar la foto ORIGINAL (alta calidad) en la PC: Escritorio, Imágenes, Descargas (PowerShell Get-ChildItem *.jpg recientes). Las de Facebook están comprimidas: no sirven.
2. Correr (Python 3.12, rembg y scipy ya instalados):
   `python -I .claude/skills/foto-pro/scripts/foto_estudio.py "<carpeta origen>" "<carpeta salida>" "<foto1.jpg,foto2.jpg>" gris ["x0,y0,x1,y1"]`
   Salida 1200x1200 estilo estudio. El último parámetro (opcional) borra una zona del recorte en fracciones (ej. etiqueta colgando: "0.72,0.84,1.0,1.0").
3. Revisar cada resultado con Read: descartar las que salgan con la mano pegada o borrosas.
4. Guardar las buenas en Escritorio\Fotos Marketplace PRO\<producto>.
5. Para subir a Facebook: copiarlas al scratchpad (Chrome solo sube archivos de carpetas de la sesión), abrir marketplace/edit/?listing_id=..., subir con file_upload al input de foto, borrar las viejas ("Eliminar foto N de M"), dejar la de frente primero, Actualizar.

## Errores encontrados
- Parchar la foto final copiando fondo deja un recuadro visible: borrar la zona en el recorte (parámetro x0,y0,x1,y1), no en la foto final.
- El script deja solo la pieza más grande (quita restos sueltos), pero no lo que está pegado al producto.
- Canva gratis NO quita fondos (pide Pro) → usar rembg local (modelo isnet-general-use).
- Si la mano tapa el producto, rembg la deja pegada: usar fotos donde el producto esté solo o casi solo.
- Fotos del interior/etiquetas: mejor dejarlas originales (prueban autenticidad).
- Piezas en BOLSA PLÁSTICA transparente: rembg las corta en pedazos y salen feas (kit Toyota, 2026-10-23). Pedir foto nueva con la pieza fuera de la bolsa.
- Si el recorte no sirve (bolsas): foto_mejorar.py en modo "libre" + recorte pegado al producto. NUNCA el modo 1x1/4x5 con relleno borroso: se ve de aficionado (kit, 23 oct). Portada = la pieza más clara con la etiqueta/número de parte legible.
- Consejo para Javier al tomar fotos: producto sobre mesa o pared lisa, luz de día, sin mano, de frente y de lado.
