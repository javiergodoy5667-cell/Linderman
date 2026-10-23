# Ronda 5: editar clips reales, video con IA, narrativa y atención

Fuentes: documentación de vid.stab (Georg Martius, GitHub) y Paul Irish (estabilizar con FFmpeg) [oficial/experto]; documentación de filtros de FFmpeg (afftdn, silencedetect) y guías de AVPres/Tafrigh [oficial/experto]; Opus y Morphic (cambios de velocidad) [blog]; Frontiers in Psychology 2017, "Judgments at Gaze Value" (eye tracking en anuncios) [académico]; VidMob, 1.1 M de anuncios 2018-2020 [industria]; PPC Hero (efecto vampiro) [blog]; Kenn Adams / Pixar, *Story Spine* (Storyprompt, SocialRevver) [experto]; comparativas de video con IA 2026 (Rework, Lushbinary, Masonry, Fluxnote) [blog, precios se contradicen].

## 1. Flujo para un clip real del teléfono (lo que hago cuando Javier manda video)
1. **`limpiar_clip.py`:** estabiliza (2 pasadas: análisis + corrección con zoom mínimo y nitidez), corta pausas donde NO hay palabras (con ruido de fondo el "silencio" no existe; por eso se usa el reconocedor de voz, colchón 0.12 s y micro-fundido para que no se oigan clics), limpia el audio (quita zumbido bajo 80 Hz y ruido de fondo moderado; si se exagera la voz suena "acuática") y corrige luz/color suave.
2. **`subtitulos.py`:** subtítulos palabra por palabra, vertical 9:16, -14 LUFS.
3. **Diseño encima** (`render_html.py`): portada, gancho, precio, tarjeta final. **Sonido** (`sonido.py`): efectos en los cortes.
Prueba: clip de 11.3 s con temblor, ruido y pausas de 1.5-2 s → 7.2 s, 3 partes, subtítulos correctos.

## 2. Cambios de velocidad (speed ramp)
- Lento en el momento clave (el corte de la sierra, el camarón cayendo al hielo) y rápido en lo de relleno.
- Máximo 2-3 cambios por video: más = cansa.
- Para cámara lenta hay que GRABAR a 60 fps (o más); inventar cuadros se ve mal.

## 3. Atención: hacia dónde mira la gente
- Estudio con seguimiento de ojos (Frontiers 2017): cuando la persona del anuncio MIRA AL PRODUCTO, la gente mira más el producto y recuerda más la marca y el mensaje que cuando la persona mira a la cámara.
- **Efecto vampiro:** una cara llamativa puede robar toda la atención del producto. En videos donde alguien habla, la gente mira a quien habla.
- Aplicado: Javier a cámara para el gancho y la confianza; luego mira y señala el producto, y la toma pasa al producto.
- VidMob (1.1 M de anuncios): la dirección de la mirada cambia los clics y el retorno. [dato de empresa, sin revisión independiente]

## 4. Narrativa: la "espina de la historia" (Kenn Adams, usada por Pixar)
"Había una vez… / Todos los días… / Hasta que un día… / Por eso… / Por eso… / Hasta que finalmente… / Y desde entonces…"
Versión de 15 s para Javier: "Todos los días los restaurantes de Petapa compraban camarón congelado y viejo. Un día probaron el de Don Gencho, que llega fresco. Por eso sus platos salen mejor. Desde entonces piden cada semana. ¿Y usted? Escríbanos." Funciona en video corto porque no hay tiempo para dar contexto: la estructura lo da sola.

## 5. Video con IA en 2026 (para cuando haga falta)
| Herramienta | Fuerte en | Acceso / costo (aprox., se contradice entre fuentes) |
|---|---|---|
| Kling 3.0 | Mejor calidad por precio, foto → video | Gratis limitado; ~US$10/mes; API ~US$0.07-0.10/s |
| Runway Gen-4.5 | Más control creativo, video → video | 125 créditos gratis una vez; ~US$12-15/mes |
| Veo 3.1 (Google) | Genera audio y video juntos | Google AI Pro ~US$29/mes o dentro de Adobe Firefly |
| Sora 2 | Realismo | Una fuente dice que lo descontinuaron en sep-2026 [verificar] |
Uso correcto: fondos, tomas de ambiente o movimiento de un producto a partir de su foto. NUNCA mostrar el producto distinto a como es (en Marketplace y en anuncios eso es engaño y causa quejas). Javier no tiene presupuesto ahora: primero lo gratis.
