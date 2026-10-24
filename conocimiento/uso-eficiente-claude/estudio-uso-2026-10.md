# Estudio real de uso de Claude (5 al 24 oct 2026)

Fuente: los registros de Claude Code en esta PC (`~/.claude/projects`, 30 sesiones). Medido con script, no estimado.

## Lo que NO se ve (sin datos ocultos)
- Uso en claude.ai web y en el teléfono: no queda en esta PC. Gasta de la misma bolsa, así que el uso real es MAYOR que esto.
- Las rutinas diarias (6:30 am y 8 pm) corren en la nube: tampoco están aquí.
- Si tuvo Pro antes del 5 oct, ese uso no aparece (no hay registros previos).
- Anthropic no publica la fórmula exacta del límite; el "costo API" de abajo es la mejor medida comparable.

## Números
| Dato | Valor |
|---|---|
| Días con uso | 14 de 20 |
| Respuestas de Claude | 4,300 (100% Opus 5.5, 0% Sonnet) |
| Mensajes de Javier | ~512 |
| Tokens procesados | 1,352 millones (98% = releer la conversación desde la caché) |
| Texto escrito por Claude | 3.4 millones de tokens |
| Veces que chocó con el límite de 5 h | 3 (12 oct, 23 oct tarde, 23 oct noche). Límite semanal: ninguna vez |
| Si eso se pagara por API (Opus 5.5) | ~US$ 430-490 en 20 días |
| Lo que pagó (Pro) | US$ 20/mes |

Precios API Opus 5.5: US$4 entrada, US$20 salida, US$0.20 lectura de caché, por millón (skill claude-api, 2026-10-06).

## Dónde se va el límite
1. **Sesiones gigantes.** 22 oct: 1 sesión de 635 respuestas (300 M tokens). 23 oct: 1 sesión de 691 (316 M). Solo esas dos = 46% de todo el uso. El 43% de las respuestas se dieron con más de 300 mil tokens de conversación encima: cada mensaje releía todo eso.
2. **Fotos dentro de la conversación.** ~400 fotos leídas (jpg/png) + capturas de Chrome. Cada foto se queda pegada y se relee en cada mensaje siguiente.
3. **Chrome.** 2,300 acciones de navegador; las más pesadas después de las fotos.
4. **Siempre Opus.** Nada pasó por Sonnet, ni lo simple (agenda, recordatorios, textos cortos).
5. El arranque ya es liviano: ~47 mil tokens por sesión nueva (bien).

## Optimización (ordenada por ahorro)
1. `/clear` al cambiar de tema y al pasar ~200 mil tokens (barra de estado ahora avisa al 20%). Ahorro estimado: 50-70% del uso.
2. Fotos y Chrome en su propia sesión: editar/publicar → `/clear` al terminar.
3. Sonnet (`/model sonnet` al iniciar) para agenda, recordatorios, mensajes a clientes. Opus solo para estudios, planes, CV, edición difícil.
4. Un mensaje completo en vez de varios cortos.

## ¿Pro Max?
- Max 5x = US$100/mes (Q≈780). Max 20x = US$200/mes. Pro = US$20.
- Chocó 3 veces en 20 días, siempre por sesiones gigantes, nunca el límite semanal.
- Con efectivo Q0 y deuda en mora: **NO conviene hoy**. Primero aplicar el punto 1 dos semanas.
- Regla: si con `/clear` aplicado sigue chocando el límite de 5 h más de 2 veces por semana, o choca el semanal, Y hay ingreso que lo pague (ej. primer cliente de IA), subir a Max 5x por 1 mes y medir.

## ¿Pasar a Hermes Agent?
- Hermes (Nous Research) es un programa aparte que usa el modelo que le conectés. Con plan Pro NO puede usar tu suscripción: necesita API pagada por uso (o Max + créditos extra).
- Con tu ritmo actual, por API saldría ~US$400-500/mes con Opus y ~US$350+ con Sonnet (la caché cuesta igual). Pro te da eso por US$20.
- Linderman ya hace lo de Hermes: memoria, conocimiento, habilidades propias, rutinas, teléfono vía GitHub.
- **Veredicto: quedarse en Claude Code + Pro.** Revisar solo si Anthropic cambia reglas o si un cliente paga la API.

## Fuentes
- https://ai.zenken.co.jp/en/post/claude-pro-vs-max-comparison/
- https://dupple.com/learn/claude-pro-vs-max
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://github.com/NousResearch/hermes-agent/issues/25267
- https://codenote.net/en/posts/hermes-agent-claude-third-party-extra-usage-http-400/
