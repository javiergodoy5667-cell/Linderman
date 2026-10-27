---
name: aplicar-empleo
description: Aplicar a un trabajo remoto o freelance para Javier haciendo que SOBRESALGA sobre todos los candidatos: CV, respuestas y mensaje personalizados para cada oferta. Usar cuando diga "aplica", "postúlame", "busca trabajo", "ofertas", "empleo", o pase un link de vacante.
---

# Aplicar a empleo (regla fija de Javier, 2026-10-23)

Javier exige: CADA aplicación personalizada. Adaptar CV, perfil y respuestas a la oferta concreta para destacar sobre todos los candidatos. Siempre.

## Pasos
1. Leer la oferta completa (get_page_text). Sacar: qué hacen, qué tareas, palabras clave, requisitos, qué valoran, sueldo.
2. Verificar que el link sea OFICIAL (LinkedIn a veces manda a agregadores como divulgavagas.com.br → ir a la web oficial de la empresa).
3. CV a la medida: copiar conocimiento/negocios-digitales/cv/cv-base.html → título dentro de su marca (cercano al rol, sin copiarlo), perfil de 3 líneas con SUS palabras clave, ordenar/reescribir viñetas de experiencia hacia lo que piden, 8 habilidades que coincidan con la oferta. Foto Jade (foto.jpg). Imprimir PDF con Chrome headless:
   chrome --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=<ruta.pdf> file:///<html>
   Nombre: CV-Javier-Arriaga-<Rol>.pdf. Copia en el escritorio. Guardar el html en cv/.
4. Respuestas: usar ejemplos reales y concretos del negocio de mariscos (libras, precios por talla, crédito 15 días, márgenes), Alorica, Nestlé, su agente de IA. Conectar cada respuesta con lo que la empresa vende.
5. Disponibilidad: lo que pida el trabajo (Javier quiere 40 h o lo necesario).
6. Tarifa: base USD 15/h (subir si la oferta paga más).
7. Mostrar resumen a Javier y enviar solo con su OK.
   AHORRO (2026-10-23): por defecto Linderman entrega CV + respuestas listas para copiar y Javier llena el formulario; usar Chrome (@browser) solo si Javier lo pide. Si se usa Chrome: leer solo la parte necesaria (find/JS acotado), pocas capturas y a escala 0.6.
8. Después de enviar: plan para sobresalir → mini demo del problema exacto de la empresa (n8n/Loom 60 s) + mensaje de 3 líneas al reclutador/fundador + preparación para la prueba. Anotar en agenda.
9. Registrar en conocimiento/negocios-digitales/ofertas-AAAA-MM-DD.md (estado, CV usado, respuestas).

## Reglas
- CV NATURAL, no forzado (Javier, 2026-10-23): no copiar el título exacto del puesto ni meter frases calcadas de la oferta. Usar su marca ("Consultor de IA" / "Consultor de IA y Automatización") y solo reordenar y resaltar lo que ya es verdad y relevante. Debe sonar como el mismo Javier en todas las aplicaciones.
- NUNCA inventar experiencia: si no sabe algo, preguntar y explicar. Lo que se exagera se cae en la prueba práctica.
- Nunca subir el CV viejo (trae DPI, NIT, dirección, antecedentes).
- No crear cuentas ni poner contraseñas: Javier lo hace; Linderman llena todo lo demás.
- Excel: declarar "básico" (es la verdad).

## Errores encontrados
- LinkedIn Easy Apply: el diálogo no aparece en read_page; usar find. Radios: el primer radio = Yes; verificar con JS (fieldset → input:checked).
- Subir archivos: interceptar HTMLInputElement.prototype.click para que no abra el selector, y luego file_upload al input type=file.
- Upwork: selects de fecha no toman el valor por defecto → elegir otro y luego el correcto.
- Buscar ofertas rápido: fetch a /jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=..&location=..&f_TPR=r604800 desde una pestaña de LinkedIn y sacar título/empresa/lugar con regex (DOMParser no sirve ahí). Ignora el filtro remoto. Esperar ~2 s entre consultas o da error 429 (bloqueo de minutos).
- Si Chrome no responde a capturas, la ventana está oculta/minimizada: pedir a Javier que la deje visible. Si la página se recarga, el formulario de Easy Apply se pierde (también el CV subido): volver a subirlo.
- Por ahora (2026-10-23) SOLO ofertas en español; descartar las que piden inglés fuerte, presencial o residir en otro país (muchas de Perú con planilla).
- Get on Board: editor de texto "lexxy" → poner HTML con `document.querySelector('lexxy-editor[input="<campo>"]').value = html`. Nivel de habilidad: radios beginner/elementary/intermediate/advanced/proficient + `form.requestSubmit()`. Al subir CV, Get on Board "lee" el CV pero no borra el perfil. Postular: modal de match → "Postular de todas formas"/"Postular ahora" → 3-4 pasos → vista previa → "Enviar postulación ahora".
- Computrabajo: los selects usan nice-select (div.nice-select junto al select oculto) → abrir y hacer clic en `li[data-value]`. Habilidades: escribir y hacer CLIC en la sugerencia exacta (Enter no sirve; un clic mal puesto agrega etiquetas raras como "Negociación policial"). Botón Guardar de las ventanas de experiencia está junto a "Eliminar": verificar coordenadas antes de hacer clic.
- No borrar archivos del usuario en ningún portal (CV viejo): pedírselo a Javier.
- Google Forms con "Agregar archivo": abre selector de Drive (iframe docs.google.com/picker). file_upload no llega al input y fetch a un servidor local se cuelga. No perder tiempo: llenar todo y pedir a Javier solo "Explorar → elegir PDF"; luego Linderman envía. LinkedIn a veces no muestra reclutador: buscar correo en la oferta.
- Gmail: atajos de teclado activos en la cuenta de Javier. No usar computer.type en el cuerpo (se va como atajos); usar JS: focus + document.execCommand("insertText"). Adjuntar: file_upload al input "Adjuntar archivos" sí funciona.
