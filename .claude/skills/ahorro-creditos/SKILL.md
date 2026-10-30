---
name: ahorro-creditos
description: Reglas para gastar menos créditos y que las sesiones de Javier (plan Pro) duren más. Aplicar SIEMPRE, en toda sesión, y cuando Javier diga "optimiza", "se me acaba el límite", "ahorra créditos".
---

> **HUMANO Y EXPERTO, SIEMPRE (orden de Javier, 2026-10-30):** todo lo que salga de esta habilidad (mensajes a Javier, textos para clientes, anuncios, publicaciones, CV, propuestas, guiones, prompts, documentos, textos de videos) pasa por `cero-generico` antes de entregarse: suena a persona experta de Guatemala, nunca a robot ni a IA; frases cortas, palabras de la calle, números y nombres reales; nada genérico.

# Ahorro de créditos

## Para qué sirve
Que el límite del plan Pro de Javier rinda más. Cada palabra que leo o escribo gasta créditos: lo que más cuesta es leer archivos grandes, páginas web, imágenes y repetir cosas.

## Cuándo usarla
Siempre. Es la forma normal de trabajar, no un modo especial.

## Reglas para Linderman (las cumplo yo)
1. **Arranque liviano:** al empezar leo solo MEMORIA, AGENDA y RECORDATORIOS (en un solo comando). INDICE, PERFIL, METAS, VENTAS y ESPECIALIDAD solo si el tema los necesita. En INDICE busco con `grep` la palabra del tema; no lo leo completo.
2. **Leer lo justo:** buscar con `grep` y leer solo las líneas necesarias (`sed -n`, offset/limit). Nunca leer un archivo entero de conocimiento si basta una sección.
3. **No releer:** si ya edité o leí un archivo en la sesión, no lo vuelvo a leer para "verificar".
4. **Juntar comandos:** varias lecturas o cambios en un solo comando o en paralelo, no uno por uno.
5. **Ediciones chicas:** cambiar con `sed` o Edit; no reescribir archivos completos.
6. **Respuestas cortas:** 5-8 líneas, sin repetir, sin resúmenes al final.
7. **Web y Chrome:** búsqueda normal (no extendida) salvo que falle. En Chrome: nada de leer páginas completas enormes ni capturas de más; usar buscar dentro de la página. Javier da los clics de formularios.
   - **Chrome = 73% del uso (medido con /usage, 26 oct).** Reglas fijas:
     a) Leer con `javascript_tool` sacando solo el dato (texto recortado con .slice). Capturas solo para ubicar un clic, siempre `scale` 0.5-0.6.
     b) Juntar pasos en `browser_batch` (clic + escribir + esperar + captura en una sola llamada).
     c) Nunca `get_page_text` ni `read_page` de página entera; usar `find` o JS acotado.
     d) Si algo falla 2 veces, parar y pedirle el clic a Javier al momento (no buscar otra vía).
     e) Subidas de archivo que no son input normal (Google Forms/Drive, selectores en iframe): llenar todo y que Javier suba el archivo.
   - No editar la habilidad de Anthropic `chrome-browser` (se sincroniza y se borra); las reglas de ahorro van aquí.
8. **Nada de subagentes** (cada uno empieza de cero y gasta mucho) salvo que Javier lo pida.
9. **Imágenes:** no abrir fotos/capturas si no hace falta verlas; si se procesan, hacerlo con scripts sin mirarlas una por una.
10. **Memoria compacta:** si MEMORIA.md pasa de ~8 KB, juntar y resumir líneas viejas o pasarlas a PERFIL o a conocimiento/. Lo mismo con AGENDA: mover lo hecho a una línea.

## Lo que le toca a Javier (solo él puede)
- **Un tema por sesión.** Al terminar un tema: `/clear`. Si la sesión ya va larga y sigue el mismo tema: `/compact`.
- **Modelo AL INICIO de la sesión, no a mitad** (cambiarlo a mitad borra la caché y ese mensaje sale caro). Sonnet (`/model sonnet`) para lo simple; Opus solo para estudio a fondo, planes o edición difícil. Para lo simple también sirve `/effort low` (en modelos 5.5 no borra la caché).
- **Si dejó la sesión más de 1 hora:** `/clear` y empezar de nuevo; seguir una sesión larga y fría la procesa toda a precio completo.
- **`/clear` es gratis; `/compact` cuesta** (lee todo para resumir). Compact solo en pausas, nunca a mitad de una tarea.
- **Pedir directo:** un mensaje con todo lo que necesita, mejor que muchos mensajes cortos. Si la respuesta va mal: Esc o `/rewind`, en vez de amontonar correcciones.
- Ver cuánto le queda y qué gasta más: `/usage` (la tecla `f` aplica arreglos). Revisarlo una vez por semana.
- Recordar: chat del teléfono, claude.ai y las rutinas diarias salen de la MISMA bolsa.
- Ya automático (23 oct): barra de estado con % de conversación, límite 5 h y semana (~/.claude/statusline.py; avisa "/clear" al pasar 20%, cambiado de 60% el 24 oct); sugerencias de próximo mensaje apagadas; instrucciones de resumen en CLAUDE.md. NO se bajó el esfuerzo ni se cambió el modelo: Javier no quiere perder calidad.

- **Medido 24 oct:** 2 sesiones gigantes (600+ respuestas) = 46% del uso; 43% de respuestas con >300 mil tokens encima; ~400 fotos. Regla: `/clear` al 20% de conversación (~200 mil) o al cambiar de tema; fotos y Chrome en sesión aparte.

## Conocimiento base
`conocimiento/uso-eficiente-claude/guia.md` (fuentes oficiales de Anthropic).

## Errores encontrados
- 2026-10-23: el arranque leía 9 archivos (~30 KB, INDICE solo 10 KB) en cada sesión. Se cambió a arranque liviano.
- 2026-10-23: apagar Chrome por defecto molestaba a Javier; se dejó encendido y el ahorro se hace usándolo poco.
- 2026-10-26: en Ally Pro se gastó de más reintentando subir un CV por el selector de Drive (4 intentos + servidor local). Regla d) y e).
- 2026-10-24: el aviso de la barra al 60% llegaba tarde (60% de 1 millón = 600 mil tokens). Bajado a 20%.
