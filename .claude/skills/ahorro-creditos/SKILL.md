---
name: ahorro-creditos
description: Reglas para gastar menos créditos y que las sesiones de Javier (plan Pro) duren más. Aplicar SIEMPRE, en toda sesión, y cuando Javier diga "optimiza", "se me acaba el límite", "ahorra créditos".
---

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
8. **Nada de subagentes** (cada uno empieza de cero y gasta mucho) salvo que Javier lo pida.
9. **Imágenes:** no abrir fotos/capturas si no hace falta verlas; si se procesan, hacerlo con scripts sin mirarlas una por una.
10. **Memoria compacta:** si MEMORIA.md pasa de ~8 KB, juntar y resumir líneas viejas o pasarlas a PERFIL o a conocimiento/. Lo mismo con AGENDA: mover lo hecho a una línea.

## Lo que le toca a Javier (solo él puede)
- **Un tema por sesión.** Al terminar un tema: `/clear`. Si la sesión ya va larga y sigue el mismo tema: `/compact`.
- **Modelo según tarea:** para cosas simples (agenda, mensajes cortos, preguntas rápidas) usar `/model sonnet`, que gasta bastante menos del límite. Opus solo para estudio a fondo, planes o edición difícil.
- **Pedir directo:** un mensaje con todo lo que necesita, mejor que muchos mensajes cortos.
- Ver cuánto le queda: `/usage` (o `/status`).

## Errores encontrados
- 2026-10-23: el arranque leía 9 archivos (~30 KB, INDICE solo 10 KB) en cada sesión. Se cambió a arranque liviano.
- 2026-10-23: apagar Chrome por defecto molestaba a Javier; se dejó encendido y el ahorro se hace usándolo poco.
