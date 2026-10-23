# Meta oficial 6: pruebas A/B, reglas automáticas y qué hacer si no hay conversiones

Leído completo 2026-10-22. Resumen propio.

## Pruebas A/B (oficial)
- Conjuntos idénticos salvo UNA variable.
- Hipótesis medible (ej. "el video bajará el costo por conversación vs la foto").
- Público suficientemente grande y que NO esté en otra campaña activa al mismo tiempo (superposición arruina el resultado).
- Duración: **mínimo 7 días, máximo 30**. (Para WhatsApp, Blueprint recomienda 2 semanas.)
- Crear desde la barra "Prueba A/B" del Administrador o desde "Experimentos".
- **No hacer pruebas "a mano"** prendiendo y apagando campañas: entrega ineficiente y resultados no confiables.
- Una prueba activa no deja cambiar la variable. Cancelar la prueba no detiene el gasto: hay que pausar.

## Reglas automáticas
- Hacen cambios o mandan avisos cuando se cumple una condición; se revisan cada ~30 min.
- Crear: Administrador → seleccionar campaña/conjunto/anuncio → Más → Crear nueva regla (o página "Reglas automáticas" → + Crear regla).
- Partes: acción (apagar, avisar, subir/bajar presupuesto) + condiciones + intervalo de días de datos + frecuencia de revisión + suscriptor.
- Plantillas listas: "Reducir superposición en la subasta" y "Reducir fragmentación del público".
- Reglas útiles para negocio chico:
  1. **Aviso** si costo por conversación > tope (ej. Q10) en los últimos 3 días.
  2. **Apagar anuncio** si gastó más de X sin ninguna conversación.
  3. **Aviso** al gastar 80% del presupuesto total.
- Cuidado: una regla que sube/baja presupuesto seguido puede reiniciar el aprendizaje.

## Si Meta avisa que el conjunto NO logrará conversiones
1. **¿El evento ocurre ≥50 veces por semana?** Si no, elegir uno más frecuente (compras → agregar al carrito/visitas; en WhatsApp: compras → conversaciones). Solo cuentan los eventos dentro de la ventana de atribución elegida.
2. **Público poco relevante:** negocio local → solo la zona de entrega (nunca todo el país); idioma correcto; solo agregar segmentación si tienes información que Meta no tiene; excluir lo que sobra.
3. **Público muy acotado:** cubrir toda la zona de entrega; juntar conjuntos parecidos; quitar "acotar público"; si usas público personalizado/similar, no agregar más filtros; activar expansión.
4. **Puja:** con volumen más alto sin límite, la puja casi nunca es el problema. Con límite/objetivo de costo: subirlo. Calcular cuánto vale una conversión (incluyendo recompras futuras del cliente).
5. **Contenido:** el anuncio también compite por el valor para el usuario; formato flexible y personalización por ubicación.

## Fuentes
- https://www.facebook.com/business/help/290009911394576
- https://www.facebook.com/business/help/1738164643098669
- https://www.facebook.com/business/help/286876155019610
- https://www.facebook.com/business/help/644860419002064
- https://www.facebook.com/business/help/197634954160445
