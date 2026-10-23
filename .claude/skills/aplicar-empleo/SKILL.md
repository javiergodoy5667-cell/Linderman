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
