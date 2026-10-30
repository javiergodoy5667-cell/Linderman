---
name: buscar-clientes
description: Buscar negocios reales que puedan comprarle a Javier (cualquier producto, cualquier zona). Usar cuando diga "búscame clientes", "a quién le vendo", o abra una zona/producto nuevo.
---

> **HUMANO Y EXPERTO, SIEMPRE (orden de Javier, 2026-10-30):** todo lo que salga de esta habilidad (mensajes a Javier, textos para clientes, anuncios, publicaciones, CV, propuestas, guiones, prompts, documentos, textos de videos) pasa por `cero-generico` antes de entregarse: suena a persona experta de Guatemala, nunca a robot ni a IA; frases cortas, palabras de la calle, números y nombres reales; nada genérico.

# Buscar clientes

> **ALCANCE (regla de Javier, 2026-10-23): conocimiento GENERAL de experto.** Sirve para cualquier producto, servicio, negocio, campaña o publicación nueva, hoy o en el futuro. Los mariscos, la sierra, la planta, etc. son solo EJEMPLOS de aplicación; las reglas del negocio actual de Javier (pago contra entrega, sin cuenta bancaria, precios) están marcadas como tales y cambian con el tiempo.


## Pasos
1. Datos mínimos (preguntar solo lo que falte en conocimiento/ventas/precios.md): producto, zona de entrega, precio, pedido mínimo.
2. Buscar en paralelo (WebSearch "extended"): "[tipo de negocio] [municipio] Guatemala" para cada tipo que compra el producto (marisquerías, cevicherías, restaurantes, comedores de mercado, hoteles).
3. Anotar SOLO datos que trae la fuente: nombre, dirección, teléfono/Facebook. Nunca inventar teléfonos.
4. Guardar en conocimiento/ventas/clientes-potenciales.md por zona, con columna Estado (Por contactar / Contactado / Respondió / Cliente / No interesa) y las fuentes.
5. Escribir el mensaje de venta (sin precio en el primer mensaje; preguntar cuántas libras usan).
6. Poner en la agenda quién contactar hoy y a quién visitar.
7. Dar a Javier links wa.me con el mensaje listo (yo no puedo enviar mensajes: el sistema lo bloquea).

## Errores encontrados
- Mandar WhatsApp por Chrome está bloqueado por seguridad; Javier envía con un toque.
- No mandar mensajes de madrugada: después de las 8 am.
- Los datos de directorios pueden estar viejos: avisar "confirmar antes de ir".
- **Google Maps en volumen (2026-10-27, probado: 144 fichas en ~15 min):** WebFetch a páginas amarillas da 403 y los artículos no traen datos. Lo que SÍ funciona con Chrome: en una pestaña de google.com, cargar cada búsqueda `/maps/search/<consulta>?hl=es` dentro de un IFRAME, bajar el `div[role=feed]`, juntar `a.hfpxzc` (href + aria-label), y abrir cada ficha en 3 iframes en paralelo leyendo `h1.DUwDvf`, `button[data-item-id="address"]`, `button[data-item-id^="phone"]`, `a[data-item-id="authority"]`, `div.F7nice`. Guardar en localStorage. Errores evitados: (1) hacer clic en las tarjetas a veces navega la página entera y mata el script; (2) en pestañas en segundo plano Chrome frena los temporizadores (usar Worker para esperar) y NO pinta el panel (datos de otra ficha) → una sola pestaña visible; (3) escribir en el buscador con eventos de teclado no refresca la lista; (4) la salida de javascript_tool se corta ~1,000 caracteres → sacar en trozos de 7 filas; (5) 3 iframes pesados congelan la pestaña al final → leer localStorage desde otra pestaña (google.com/robots.txt). Filtrar por nombre/categoría de mariscos (la búsqueda trae cafeterías e italianos). Excel con `ventas/scripts/excel-clientes.py`.
- Google Maps NO muestra el dueño: columna "preguntar en visita".
