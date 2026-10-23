# Uso eficiente de Claude (plan Pro) — que el límite rinda más

Estudiado 2026-10-23. Sirve para cualquier uso de Claude Code o claude.ai, no solo Linderman.

## Cómo funciona el límite [oficial]
- Pro tiene **dos límites**: una ventana de **5 horas** (empieza con el primer mensaje) y un **límite semanal**. Anthropic no publica números exactos. Los blogs dicen ~45 mensajes de Claude Code por ventana, pero es solo una estimación [blog-sin-verificar].
- **Todo sale de la misma bolsa:** el chat de claude.ai (web, PC, teléfono), Claude Code y las **rutinas programadas** en la nube.
- Al llegar al límite: esperar a que se reinicie, activar créditos extra (pago aparte y opcional) o subir a Max.
- Ver cuánto queda: `/usage` (o `/status`). En la ventana de `/usage` aparece **qué gasta más** con recomendaciones. Con la tecla `f` aplica algunas solas.

## Por qué se gasta [oficial]
1. **En cada mensaje se reenvía TODA la conversación.** Una pregunta de una línea en una sesión larga cuesta como toda la sesión. Esto es lo que más gasta.
2. **Caché (memoria rápida):** Claude guarda lo ya leído y releerlo cuesta mucho menos. En Pro esa memoria dura **1 hora sin actividad**. Si uno vuelve después de más de 1 hora a una sesión larga, se procesa todo de nuevo a precio completo.
3. **Cosas que borran la caché (mensaje caro):** cambiar de modelo a mitad de sesión, conectar o quitar herramientas (MCP), activar el modo rápido, acumular muchas imágenes y actualizar Claude Code.
4. **Pensamiento interno:** cuenta como texto escrito. Bajar el esfuerzo (`/effort low`) para tareas simples gasta menos. En los modelos 5.5 cambiar el esfuerzo NO borra la caché.
5. **Ayudantes (subagentes):** cada uno es otra conversación aparte y gasta por su lado.
6. **`/compact`** también gasta, porque tiene que leer todo para resumirlo. **`/clear` no cuesta nada.**
7. **CLAUDE.md** se carga en cada mensaje: mantenerlo corto (menos de 200 líneas) y pasar instrucciones especiales a habilidades, que solo se cargan cuando se usan.

## Reglas prácticas (de mayor a menor efecto)
1. **`/clear` al cambiar de tema.** Antes, `/rename` si quieres volver a esa sesión con `/resume`.
2. **Si dejaste la sesión más de 1 hora:** mejor empezar una nueva (`/clear`) que seguir en una sesión larga y fría.
3. **Elegir modelo y esfuerzo AL INICIO** de la sesión, no a mitad. Sonnet para lo simple y Opus para planes o estudios difíciles.
4. **Un mensaje completo y específico** en vez de muchos cortos o vagos. Si una respuesta salió mal, corregir pronto (Esc o `/rewind`) en vez de amontonar correcciones.
5. **`/compact` solo en pausas naturales**, no a mitad de una tarea. Se le puede decir qué guardar: `/compact guarda solo los precios y pendientes`.
6. **Pocas imágenes y capturas.**
7. **Revisar `/usage` una vez por semana** para ver qué está gastando más.

## Aplicado a Javier
- Las 2 rutinas diarias (6:30 am y 8:00 pm) gastan de su misma bolsa todos los días: conviene que sean cortas.
- Lo que hable desde el teléfono también cuenta.
- El arranque de Linderman bajó de ~30 KB a ~10 KB por sesión (2026-10-23).

## Fuentes
- [oficial] https://code.claude.com/docs/en/costs
- [oficial] https://code.claude.com/docs/en/prompt-caching
- [oficial] https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan
- [blog-sin-verificar] https://www.morphllm.com/claude-code-usage-limits · https://www.kdnuggets.com/7-practical-ways-to-reduce-claude-code-token-usage · https://aiblewmymind.substack.com/p/claude-usage-limit-tips

## Fuentes del método de 9 que no aplican
No hay libros, biografías ni podcasts serios sobre este tema; es documentación técnica que cambia seguido. Las fuentes oficiales son la verdad. Volver a revisarlas cada 2-3 meses.
