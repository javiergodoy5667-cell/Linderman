---
name: aprender-tema
description: Estudio PROFUNDO e INTENSIVO para volverse experto en un tema (Meta Ads, finanzas, ventas, marca, etc.). Usar SIEMPRE que Javier diga "aprende", "vuélvete experto", "estudia", "investiga a fondo".
---

> **HUMANO Y EXPERTO, SIEMPRE (orden de Javier, 2026-10-30):** todo lo que salga de esta habilidad (mensajes a Javier, textos para clientes, anuncios, publicaciones, CV, propuestas, guiones, prompts, documentos, textos de videos) pasa por `cero-generico` antes de entregarse: suena a persona experta de Guatemala, nunca a robot ni a IA; frases cortas, palabras de la calle, números y nombres reales; nada genérico.

# Aprender un tema (método obligatorio de Javier, 2026-10-22)

Javier exige estudio profundo, nunca superficial, y que Linderman busque MÁS por su cuenta. Leer fuentes completas, no resúmenes de buscador.

## Las 9 fuentes que SIEMPRE se cubren
1. **Oficial:** entidades y documentación oficial del tema (gobierno, plataforma, reguladores). Leer completo (Chrome si WebFetch falla).
2. **Cursos gratis y legales en texto:** academias oficiales, universidades, plataformas (Blueprint, Khan Academy, etc.).
3. **Libros:** clásicos de dominio público leídos completos + modernos clave (resúmenes de calidad; completos solo si Javier tiene copia legal).
4. **Conferencias y charlas:** TED, eventos, entrevistas largas (leer transcripciones).
5. **Biografías de los mejores:** quiénes son, cómo lo lograron, sus reglas. Preferir lo que escribieron ellos mismos (cartas, blogs, ensayos gratis).
6. **Podcasts y audiolibros (Spotify, etc.):** Linderman NO puede escuchar audio → buscar transcripciones, notas del episodio y artículos del autor; listar los mejores para que Javier los escuche.
7. **Datos reales y actuales:** cifras de este año, locales (Guatemala) cuando aplique.
8. **Ejemplos reales:** casos, anuncios, negocios que lo hicieron.
9. **Pepitas de oro:** las ideas más valiosas y poco conocidas, en una lista corta y accionable.
+ **Búsqueda propia:** al terminar, buscar al menos 2 fuentes extra que nadie pidió.

## Pasos
1. Crear `conocimiento/<tema>/` con `PROGRESO.md` (las 9 fuentes como filas) y un archivo por bloque.
2. Buscar en paralelo (varias búsquedas a la vez, modo "extended" para lo difícil).
3. Leer completo; resumir con palabras propias (nunca copiar texto con derechos); marcar [oficial] / [experto] / [blog-sin-verificar].
4. Aplicar cada bloque al caso de Javier con números.
5. Guardar después de CADA bloque (INDICE, PROGRESO, commit y push).
6. Reportar a Javier en 3-5 líneas por bloque: lo que le sirve + qué sigue. Sin tablas generales de otros temas.
7. Al final: crear o mejorar la habilidad práctica del tema en `.claude/skills/` y actualizar % de experto.

## Límites
- Nada pirata (ni descargado ni leído en línea), aunque llegue por otra vía.
- Finanzas: no recomendar inversiones específicas (acciones, cripto, fondos).
- Si algo es video/audio sin transcripción: anotarlo en la lista para Javier.

## Errores encontrados
- Cursos en video (Skool/Tribu): no se pueden ver.
- Páginas de Meta y SIB bloquean WebFetch: usar Chrome con get_page_text.
- PDFs: WebFetch a veces da binario; probar versión _djvu.txt en archive.org.
- Blogs exageran cifras: no usarlas como verdad.
