---
name: prompt-para-ia
description: Escribir prompts profesionales para que OTRA IA (menos capaz) construya un proyecto sin problemas, y auditar después lo que entregue. Usar cuando Javier diga "hazme un prompt", "para que otra IA lo haga", "dáselo a ChatGPT/Cursor", o pida auditar un proyecto hecho por otra IA.
---

# Prompt para otra IA

Modelo probado: `conocimiento/prompts/buscador-ofertas-gt.md` (a Javier le encantó, 2026-10-27).

## Estructura obligatoria del prompt
1. **Rol:** experto senior; el usuario NO es programador; la IA ejecuta, prueba y corrige sola.
2. **Objetivo + resultado final** en lo que Javier verá (no en tecnicismos).
3. **Arquitectura ya decidida** (tabla herramienta → por qué). Preferir costo Q0: GitHub Actions + GitHub Pages (repo PÚBLICO; privado cobra US$4/mes por Pages), Telegram para avisos (WhatsApp API cuesta).
4. **Fuentes / datos a VERIFICAR**, nunca asumidas. Fase 0 de verificación con reporte.
5. **Reglas de negocio con números** (umbrales, niveles, fórmulas), no adjetivos.
6. **Fases** con entregable + prueba de aceptación cada una.
7. **Tabla de errores**: problema → cómo se detecta → qué hacer. Nada se cae entero por una pieza.
8. **Reglas**: prohibido inventar, respetar términos de sitios, secretos fuera del código, config editable sin tocar código, README en español.
9. **Lo único que se le pide a Javier**, con pasos exactos de clics.
10. **Cómo reporta** (máx 6 líneas, números reales, sin tecnicismos).
11. **Lista de "terminado"** con casillas comprobables.
12. **Entrega para auditoría**: archivo `ENTREGA.md` con pruebas de cada punto, tabla de estado, decisiones distintas al prompt, errores conocidos y links.

## Siempre incluir (sin que Javier lo pida)
- **Mejoras propias de valor real** en una fase final (a Javier le encantan): ej. lista de deseos, modo reventa/negocio, modo fechas fuertes, resumen diario.
- **Si es web/app: instalable como app (PWA)** — manifest + service worker, ícono en el celular, sin Play Store. Play Store solo si lo pide (US$25 una vez).
- Costos claros: qué es gratis, qué es opcional, qué cobra.

## Auditoría (cuando la otra IA termine)
1. Pedir link del repo. Leer primero `ENTREGA.md`, no todo el código (ahorro-creditos).
2. Verificar contra la lista de "terminado": correr/ver pruebas, revisar secretos expuestos, manejo de errores, datos inventados.
3. Entregar a Javier **un mensaje listo para pegar** a la otra IA con cada falla y su arreglo. Correcciones de 2 minutos → hacerlas yo.

## Errores encontrados
- Agregar mejoras DESPUÉS de que Javier ya pegó el prompt no sirve: incluir PWA y sección de auditoría desde la primera versión.
