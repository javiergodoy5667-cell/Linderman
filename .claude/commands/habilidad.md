---
description: Guardar como habilidad lo que Linderman acaba de hacer, para repetirlo después
argument-hint: <nombre corto de la habilidad (opcional)>
---

Convierte la tarea que acabamos de hacer en esta conversación en una habilidad reutilizable. Nombre sugerido: $ARGUMENTS

1. Escribe `.claude/skills/<nombre-corto-sin-espacios>/SKILL.md` con este formato:
   ```
   ---
   name: <nombre-corto>
   description: <una frase: qué hace y cuándo usarla, con las palabras que Javier usaría para pedirla>
   ---
   # <Nombre>
   ## Cuándo usarla
   ## Qué necesito antes de empezar
   ## Pasos
   ## Errores que ya encontré y cómo evitarlos
   ```
   Escribe los pasos con lo que realmente funcionó, no con lo que se intentó y falló.
2. Si la habilidad ya existe, mejórala en lugar de crear otra.
3. Agrega o actualiza su línea en `habilidades.md`.
4. Dile a Javier en una línea qué habilidad quedó guardada y cómo pedirla la próxima vez.
