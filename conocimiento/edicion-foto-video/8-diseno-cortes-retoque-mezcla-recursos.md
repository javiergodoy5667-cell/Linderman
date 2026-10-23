# Ronda 4: diseño gráfico, cortes y transiciones, retoque, mezcla de audio, recursos con licencia, premiados

Fuentes: Robin Williams, *The Non-Designer's Design Book* (vía Presentation Zen), Figma (biblioteca de principios) [experto]; VideoProc, 4K Shooters, CapCut (cortes) [blog]; Adobe (separación de frecuencias), PHLearn, Creative Bloq, Fstoppers (retoque) [experto]; BBC y radiodifusión alemana citadas en un paper de la Univ. de Salford, CapCut, Corel, SmartSound (mezcla) [académico/oficial + blog]; FAQ oficial de Pixabay [oficial]; HGTV/Piktochart/UX Planet (color) [blog]; Contagious, LBB (Cannes Lions 2024-2026) [industria].

## 1. Diseño gráfico (vale para foto, portada, carrusel y cada cuadro de video)
- **Contraste:** lo más importante es lo más distinto (tamaño, color, grosor). Un elemento chico de alto contraste le gana a uno grande apagado.
- **Repetición:** misma letra, color y forma en todas las piezas de una marca = se reconoce.
- **Alineación:** todo alineado a una cuadrícula invisible (bordes o centro). Nada "flotando" al azar.
- **Proximidad:** lo que va junto se ve como un grupo; el espacio vacío separa ideas.
- **Jerarquía:** decidir qué se ve 1.º, 2.º y 3.º (ej. producto → precio → botón).
- Gestalt: semejanza, continuidad, cierre, figura-fondo (el producto debe "despegarse" del fondo).
- **Color 60-30-10:** 60% dominante (fondo), 30% secundario, 10% acento (precio/botón). Armonías: complementarios = choque y atención (oferta); análogos = calma (lujo, salud); neutros para respirar. Sacar la paleta DEL PRODUCTO (`recortar.py` da sus colores).

## 2. Cortes y transiciones (y cuándo usar cada una)
| Corte | Qué es | Cuándo |
|---|---|---|
| Corte por coincidencia (match cut) | Pasa de una toma a otra que comparte forma, color o movimiento | Unir dos ideas (camarón en la mano → camarón en el plato) |
| Salto (jump cut) | Corte brusco en la misma toma | Quitar pausas al hablar, dar ritmo; estilo creador |
| Barrido (whip pan) | Movimiento rápido que se desenfoca y esconde el corte | Pasar de producto a producto con energía |
| Corte de golpe (smash cut) | Contraste brusco: silencio → ruido, quieto → acción | Sorpresa, gancho, revelar el precio |
| Corte J | El sonido de la próxima escena empieza ANTES que su imagen | Crear expectativa (se oye la sierra antes de verla) |
| Corte L | El sonido sigue sobre la escena siguiente | Voz que continúa mientras se ve el producto |
Regla: la transición debe tener una razón. Efectos de "plantilla" (cubos, estrellas) = aficionado.

## 3. Retoque de fotos (orden profesional)
1. Limpiar: polvo, rayones, etiquetas sueltas, bordes de mesa.
2. Corregir lo que afecta color y textura juntos ANTES de separar.
3. **Separación de frecuencias:** una capa con la textura y otra con color/sombras, para arreglar manchas sin perder textura.
4. **Esquivar y quemar (dodge & burn):** aclarar y oscurecer a mano para dar volumen (brillos donde pega la luz, sombras en los bordes). Se pinta a muy baja intensidad (~1%) y se revisa con una curva exagerada para ver parches.
5. Composición: extender o cambiar fondo, sombra de contacto suave, reflejo en superficie si aplica.
Lo hago con: rembg (recorte), Pillow/numpy (luz y color), HTML/CSS (composición, sombras, reflejos en diseño).

## 4. Mezcla de audio
- Voz siempre arriba. Música debajo: bajarla 6-12 dB cuando habla (la BBC prueba con -4 dB; la radio alemana pide al menos 7 LU de diferencia entre voz y fondo).
- **Ducking:** la música baja sola cuando hay voz; ataque 30-80 ms, liberación 250-700 ms (suave, sin "bombeo").
- La voz se entiende por las consonantes: música densa en la misma frecuencia la tapa.
- Volumen final redes ~-14 LUFS, picos por debajo de -1 dB.
- Efectos en el cuadro exacto del movimiento: whoosh en transición, golpe en el texto que entra, campana/ding en el precio o el botón.
Herramienta: `sonido.py` sintetiza los efectos (sin derechos de autor), hace el ducking y nivela.

## 5. Recursos gratis con licencia comercial (para anuncios)
- **Pixabay** (música, video, efectos, fotos): uso comercial sin atribución según su FAQ oficial; NO revender el archivo solo; ojo con marcas o personas que aparezcan. Riesgo: algún usuario sube algo que no es suyo → usar pistas de autores conocidos.
- **Pexels** (video/foto): uso comercial gratis según reseñas; no usar personas para dar a entender que recomiendan el producto. [confirmar en su página]
- Música dentro de Meta y CapCut comercial: usarla desde la misma app al crear el anuncio.
- Lo más seguro: efectos sintetizados por Linderman + música con licencia comprobada.

## 6. Lecciones de anuncios premiados (Cannes Lions, Film Craft)
- **Telstra 2025 (Grand Prix):** 26 cortos de 15 s en stop-motion, cada uno de un pueblo distinto, con voces de gente real del lugar. Lección: muchas piezas cortas, locales y con gente real > un solo comercial caro.
- **Hornbach 2024:** todo filmado en 1:1 dentro de "un metro cuadrado". Lección: una restricción creativa clara (un formato, un espacio) vuelve memorable una pieza barata.
- **Hyundai "Night Fishing" 2025:** película original que se ganó la atención sin gran pauta. Lección: el contenido que la gente quiere ver se distribuye solo.
- **Coinbase 2026:** ganó Film Craft (sin detalle de edición en las fuentes).
Aplicado a Javier: serie de videos cortos con clientes reales de Petapa; una restricción creativa por serie (ej. "todo en la tabla de cortar", "todo en 7 segundos").
