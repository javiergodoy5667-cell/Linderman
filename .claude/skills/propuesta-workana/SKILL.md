---
name: propuesta-workana
description: Buscar proyectos en Workana que le sirvan a Javier y escribirle propuestas que ganen. Usar cuando diga "busca proyectos", "propuestas", "Workana", "trabajo remoto" o "freelance".
---

# Propuesta Workana

## Para qué
Conseguir los primeros clientes de Javier en Workana (servicio: automatización con IA y WhatsApp, ventas, Meta Ads) con pocas propuestas bien escogidas.

## Datos fijos
- Plan gratis: 2 propuestas por SEMANA (se renuevan). Cada una cuenta.
- Precio en QUETZALES. Comisión Workana 20% al inicio (cobra Q100 → recibe ~Q80).
- Prohibido poner teléfono, correo o links de contacto en la propuesta (bloquean la cuenta).
- Perfil: conocimiento/negocios-digitales/perfil-workana-linkedin.md

## Pasos
1. Buscar en Chrome: workana.com/jobs?language=es&query=whatsapp (también "chatbot", "n8n", "automatizacion", "community manager", "ventas").
2. Sacar lista con javascript_tool: `document.querySelectorAll('.project-item')` → título, propuestas, fecha.
3. Escoger 2: publicados hace <24 h, <15 propuestas, que Javier PUEDA entregar de verdad (WhatsApp Business, n8n, chatbots sencillos, Meta Ads, contenido, ventas). Descartar si piden años de experiencia/portafolio que no tiene.
4. Leer cada proyecto con get_page_text (fetch desde JS está bloqueado).
5. Escribir propuesta: 1) repetir el problema del cliente en una frase, 2) plan en 3-4 pasos con herramientas concretas, 3) qué entrega y en cuántos días, 4) una prueba real (su agente de IA, Alorica, negocio propio), 5) una pregunta que obligue a responder. Máx. 150 palabras, sin "estimado".
6. Precio: en la mitad baja del rango mientras tenga 0 reseñas.
7. Guardar en conocimiento/negocios-digitales/propuestas-AAAA-MM-DD.md con link, precio y estado.
8. Enviar SOLO con permiso de Javier.

## Errores encontrados
- Mientras el perfil está "en revisión" no se pueden enviar propuestas.
- fetch() desde javascript_tool queda bloqueado: navegar a cada proyecto.
- Muchos proyectos son casi iguales (plantillas): elegir por pocas propuestas y fecha reciente.
