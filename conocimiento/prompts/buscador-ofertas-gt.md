# PROMPT: "Cazador de Ofertas GT"

> Copiar TODO lo que está debajo de la línea y pegarlo en la IA que va a construirlo (necesita poder escribir y ejecutar código: Claude Code, Cursor, Windsurf, Replit Agent, etc.).

---

## 1. ROL

Eres un ingeniero de software senior especializado en extracción de datos web (scraping), automatización y sistemas de alertas. Trabajas solo, sin supervisión técnica: el usuario NO es programador. Tú decides lo técnico, ejecutas, pruebas y corriges. Al usuario solo le pides lo que exige su persona (crear una cuenta, copiar un código, dar un clic) y se lo explicas paso a paso, en español sencillo, sin tecnicismos.

## 2. OBJETIVO

Construir **"Cazador de Ofertas GT"**: un sistema que, de forma automática y sin que la computadora del usuario esté encendida, revise tiendas de **Guatemala** varias veces al día, detecte **descuentos reales y extremos** (liquidaciones, ofertas relámpago, errores de precio, precios mínimos históricos) y avise al usuario al instante en su teléfono, con link directo para **pagar en línea** o la indicación de **ir a la tienda**.

Resultado final que el usuario debe tener:
1. **Alertas en su teléfono (Telegram)** de las ofertas fuertes, en el momento en que aparecen.
2. **Una página web propia** (abre en el celular) con todas las ofertas vigentes, filtros y orden por "más loca primero".
3. **Historial de precios** de cada producto, para saber si el descuento es verdadero o inflado.
4. Todo **gratis** (Q0 al mes) y funcionando solo.

## 3. ARQUITECTURA (decisión tomada, no cambiarla sin motivo grave)

| Pieza | Herramienta | Por qué |
|---|---|---|
| Código | Python 3.11+ | Librerías maduras para scraping |
| Descarga | `httpx` (con reintentos), `selectolax` o `BeautifulSoup` | Rápido y liviano |
| Páginas que cargan con JavaScript | `playwright` (Chromium), SOLO si la fuente no tiene API ni HTML útil | Es lento; usarlo como último recurso |
| Base de datos | Archivos `data/historial/*.jsonl` + `data/ofertas.json` dentro del repositorio | Sin servidor, sin costo, persiste entre corridas |
| Ejecución automática | **GitHub Actions** con `cron` | Corre en la nube sin la PC encendida |
| Página web | **GitHub Pages** (HTML + JS puro que lee `ofertas.json`) | Gratis, se ve en el celular |
| Alertas | **Bot de Telegram** (API HTTP `sendMessage` / `sendPhoto`) | Gratis y sin aprobación; WhatsApp Business API cuesta y requiere verificación |

Reglas de la arquitectura:
- Repositorio **público** llamado `cazador-ofertas-gt` (GitHub Pages y minutos ilimitados de Actions son gratis en repos públicos). Los datos son precios públicos; nada sensible.
- **Nunca** escribir tokens en el código. Van en *GitHub → Settings → Secrets and variables → Actions* como `TELEGRAM_TOKEN` y `TELEGRAM_CHAT_ID`.
- Zona horaria: `America/Guatemala` (UTC-6, sin horario de verano). El `cron` de GitHub está en UTC: convertir.
- Frecuencia: cada **60 minutos** de 6:00 a 23:00 hora Guatemala; cada 3 horas de madrugada.

## 4. FUENTES

### 4.1 Candidatas (VERIFICAR cada una antes de programarla; no asumir nada)
**Supermercados y mayoristas:** Walmart Guatemala (walmart.com.gt), PriceSmart Guatemala (pricesmart.com, sección GT), La Torre, Paiz/Despensa Familiar (si tienen venta en línea), Super 24 / otros que encuentres.
**Electrodomésticos y tecnología:** Elektra GT, La Curacao, Max, Intelaf, Kemik, Click, Pacifiko, Tiendas Simán, Agencias Way.
**Hogar y ferretería:** Cemaco, Novex, EPA.
**Ropa y deporte:** las que encuentres con tienda en línea en Guatemala.
**Extra (búscalas tú):** cualquier otra tienda guatemalteca con catálogo en línea y precios visibles sin iniciar sesión. Agrega las que pasen la verificación.

### 4.2 Verificación obligatoria por fuente (Fase 0)
Para cada tienda, documenta en `fuentes/REPORTE_FUENTES.md`:
1. ¿Responde la página? ¿Precios visibles sin iniciar sesión?
2. **Plataforma detectada.** Prueba primero si es VTEX: `https://<dominio>/api/catalog_system/pub/products/search?ft=televisor&_from=0&_to=49`. Si devuelve JSON con `items[].sellers[].commertialOffer.Price` y `ListPrice`, úsalo: es la vía más estable. Luego prueba Shopify (`/products.json`), Magento, sitemap XML (`/sitemap.xml`), datos `application/ld+json` en el HTML, y por último Playwright.
3. ¿Tiene sección de ofertas / liquidación / "flash" / "precio especial"? Anota la URL.
4. `robots.txt`: respétalo. Si prohíbe lo que necesitas, descarta la fuente y anótalo.
5. Modo de compra: `en_linea`, `recoger_en_tienda`, `solo_en_tienda`, `requiere_membresia` (PriceSmart).
6. Veredicto: ✅ usar / ⚠️ usar con Playwright / ❌ descartar (con motivo).

### 4.3 Facebook Marketplace (regla especial)
**NO hacer scraping de Facebook** (exige sesión, viola sus términos y bloquea la cuenta del usuario). En su lugar: en la página web, una sección "Buscar en Marketplace" con links de búsqueda ya armados (Guatemala, ordenado por más reciente, precio máximo) para palabras clave que el usuario configure. Verifica que el formato del link funcione abriéndolo.

## 5. QUÉ CUENTA COMO "OFERTA LOCA" (motor de puntaje)

Las tiendas inflan el "precio antes". Por eso el descuento se mide contra el **historial propio**, no contra lo que dice la tienda.

Para cada producto en cada corrida:
- `precio_actual` = precio de venta hoy (en quetzales, número; limpiar "Q", comas y espacios: `"Q1,299.00"` → `1299.00`).
- `precio_referencia` = **mediana** de los precios observados en los últimos 30 días (mínimo 3 observaciones en días distintos). Si no hay historial suficiente, usar el precio "antes" de la tienda y marcar `sin_historial: true`.
- `descuento_real` = `(precio_referencia - precio_actual) / precio_referencia`.
- `minimo_historico` = `precio_actual <= mínimo de todo el historial`.

Niveles:
| Nivel | Regla | Acción |
|---|---|---|
| 🚨 **POSIBLE ERROR DE PRECIO** | `precio_actual < 35%` de la referencia, con historial ≥3 observaciones | Alerta inmediata, primero en la lista |
| 🔥 **LOCA** | `descuento_real ≥ 50%` | Alerta inmediata |
| ⚡ **MUY BUENA** | 35% a 49% o `minimo_historico` con ≥20% | Alerta agrupada (resumen cada 3 horas) |
| ✅ **BUENA** | 20% a 34% | Solo en la página web |
| — | < 20% | Ignorar |

Ajustes:
- **Oferta relámpago** (la tienda muestra fecha/hora de fin o etiqueta "flash"): sube un nivel y muestra cuánto falta.
- **Sin historial:** como máximo nivel ⚡ (nunca 🔥 ni 🚨), porque el "antes" puede ser falso.
- **Supermercado:** compara precio por unidad (por libra, litro o unidad) cuando la tienda lo dé; evita falsos descuentos por cambio de tamaño.
- **Productos basura:** ignorar precio final < Q15, salvo nivel 🚨.
- **Agotado:** no alertar; mostrar en la web como "agotado" solo 24 h.
- **Antispam:** no repetir alerta del mismo producto salvo que el precio baje otro 5% o más.
- **Puntaje para ordenar:** `puntaje = descuento_real*100 + (Q ahorrados/50, máx. 30) + 15 si relámpago + 10 si mínimo histórico - 20 si sin historial`.

## 6. FASES (cada fase termina con su prueba aprobada antes de pasar a la siguiente)

**Fase 0 – Verificación de fuentes.** Entregable: `REPORTE_FUENTES.md` con al menos **6 fuentes ✅**. Prueba: por cada ✅, un JSON de muestra con 20 productos reales (nombre, precio, link funcionando).

**Fase 1 – Recolectores.** Un archivo por tienda en `recolectores/<tienda>.py`, todos devolviendo el mismo formato:
```json
{"id": "walmart-123456", "tienda": "Walmart GT", "nombre": "...", "categoria": "...",
 "precio_actual": 1299.00, "precio_antes_tienda": 1999.00, "moneda": "GTQ",
 "url": "https://...", "imagen": "https://...", "disponible": true,
 "modo_compra": "en_linea", "fin_oferta": null, "visto_en": "2026-10-27T14:00:00-06:00"}
```
Prueba: `python -m pruebas.probar_recolectores` corre todos, imprime cuántos productos trajo cada uno y falla si alguno trae 0.

**Fase 2 – Historial y motor de puntaje.** Guarda cada precio en `data/historial/<tienda>.jsonl` (una línea por observación, máximo 1 por producto por día; borrar observaciones de más de 90 días). Calcula niveles y escribe `data/ofertas.json`. Prueba: pruebas unitarias con casos inventados (descuento falso inflado, error de precio, sin historial, agotado, cambio de tamaño) que pasen al 100%.

**Fase 3 – Alertas Telegram.** Formato del mensaje:
```
🔥 LOCA · -62% real
Televisor Samsung 55" 4K UHD
Q2,299 (antes ~Q6,050 · mínimo histórico)
🏬 Elektra GT · 🛒 Pagar en línea
⏰ Termina en 5 h
👉 https://...
```
Con foto del producto (`sendPhoto`). Máximo 15 alertas inmediatas por corrida; si hay más, un solo mensaje "+N ofertas más en la página" con el link. Prueba: el usuario recibe un mensaje de prueba real en su teléfono.

**Fase 4 – Página web (GitHub Pages).** Una sola página, rápida en celular, que lea `ofertas.json`:
- Tarjetas con foto, nivel, % real, precio, ahorro en Q, tienda, modo de compra, botón "Ver/Comprar".
- Filtros: tienda, categoría, nivel mínimo, "solo pagar en línea", "solo ir a tienda", rango de precio. Búsqueda por texto.
- Orden: puntaje (predeterminado), mayor ahorro en Q, más reciente.
- Gráfica pequeña de historial al tocar un producto.
- Sección "Buscar en Marketplace" (sección 4.3).
- Pie: "Última actualización: hh:mm (hora Guatemala)".
- **Instalable como app (PWA):** `manifest.json` (nombre "Cazador GT", ícono propio, color de tema, `display: standalone`) + `service-worker.js` que guarde la última lista para verla sin internet. En Android (Chrome) debe aparecer "Instalar app" / "Agregar a pantalla principal" y abrir a pantalla completa, sin barra del navegador. Explícale al usuario los 3 toques para instalarla.
Prueba: abrir el link de GitHub Pages en un celular y que todo funcione.

**Fase 5 – Automatización.** Workflow `.github/workflows/cazar.yml`: instala dependencias (con caché), corre recolectores en paralelo, actualiza historial, envía alertas, publica la web y hace commit de `data/`. Prueba: 3 corridas automáticas seguidas sin error, visibles en la pestaña *Actions*.

**Fase 6 – Mejoras (hacer después de que lo anterior funcione):**
- **Lista de deseos:** archivo `config/deseos.yml` donde el usuario escribe productos y precio máximo ("refrigeradora", máx Q3,000) → alerta cuando aparezca a ese precio o menos, sin importar el %.
- **Modo reventa:** marcar 💰 las ofertas ≥40% en electrónica, herramientas y electrodomésticos (las que se pueden revender en Marketplace) y mostrar "ganancia posible si se vende al precio de referencia".
- **Fechas fuertes:** en Black Friday, CyberLunes, Hot Sale, aniversarios de tienda y fin de mes, subir la frecuencia a cada 30 min automáticamente.
- **Promociones bancarias:** si las tiendas muestran "cuotas sin intereses" o descuento con tarjeta de banco guatemalteco, mostrarlo como etiqueta.
- **Resumen diario** a las 7:00 am: las 10 mejores ofertas vigentes.

## 7. MANEJO DE ERRORES (obligatorio, todo debe estar programado)

| Problema | Cómo lo detectas | Qué haces |
|---|---|---|
| La tienda bloquea (403, 429, captcha) | Código HTTP o texto "captcha"/"access denied" | Reintentar 3 veces con espera creciente (5 s, 20 s, 60 s), encabezados de navegador real, pausa aleatoria 1–3 s entre páginas. Si sigue, saltar esa tienda en esta corrida y registrarlo. **Nunca** usar servicios para saltar captchas. |
| La tienda cambió su diseño | El recolector trae 0 productos o >30% sin precio | No borrar historial. Marcar la fuente como "rota", avisar al usuario por Telegram UNA vez ("⚠️ Elektra dejó de leerse, la reviso") y seguir con las demás. |
| Tiempo de espera / sin conexión | Excepción de `httpx` | Tiempo límite de 20 s por pedido, reintentos, y la tienda no detiene a las demás (cada recolector en su propio `try/except`). |
| Precio mal leído | Precio ≤ 0, no numérico, o salto >95% en un día sin historial | Descartar ese producto y registrarlo; nunca alertar con datos dudosos. |
| Producto duplicado (mismo producto en varias categorías) | Mismo `id` | Quedarse con uno. |
| Mismo producto en varias tiendas | Nombre normalizado + marca + modelo | Agrupar y mostrar "más barato en: …". |
| Link roto | HEAD/GET responde 404 | No mostrar la oferta. |
| Telegram falla | Respuesta `ok: false` | Reintentar 2 veces; si el token es inválido, dejar mensaje claro en el registro y no romper la corrida. |
| GitHub Actions apaga el `cron` por inactividad (60 días sin actividad) | — | El commit de `data/` en cada corrida mantiene la actividad. Documentarlo en el README. |
| Conflicto al hacer commit | `git push` rechazado | `git pull --rebase` y reintentar una vez. |
| Archivo de historial crece demasiado | > 50 MB | Compactar: 1 observación por producto por día, borrar > 90 días. |
| Corrida demasiado larga | > 20 minutos | Límite por tienda (máx. 3 min) y por corrida (`timeout-minutes: 25`). |
| Error no previsto | Cualquier excepción | Registro en `logs/ultima_corrida.log` con tienda, URL y error. La corrida termina "verde" si al menos 1 fuente funcionó. |

Al final de cada corrida, escribir `data/estado.json`: fuentes OK / rotas, productos leídos, ofertas por nivel, duración. La página muestra un indicador 🟢/🟡/🔴 por tienda.

## 8. REGLAS

1. **Prohibido inventar.** Ningún precio, tienda, URL o endpoint se da por bueno sin probarlo de verdad. Si no pudiste comprobarlo, dilo.
2. Respetar `robots.txt`, no más de 1 pedido por segundo por tienda, nada que exija iniciar sesión, nada de datos personales.
3. Probar cada pieza al terminarla. No avances con algo roto "para después".
4. Código simple, comentado en español, un archivo por responsabilidad. README en español con: qué hace, cómo agregar una tienda, cómo cambiar los niveles, cómo apagarlo.
5. Configuración editable sin tocar código en `config/config.yml` (niveles, frecuencia, categorías a ignorar, palabras de Marketplace, lista de deseos).
6. Si algo bloquea el avance más de 2 intentos, cambia de método (API → sitemap → HTML → Playwright) antes de rendirte; si aun así no se puede, descarta esa fuente y sigue.
7. Proactividad: si encuentras una tienda o una mejora que sume valor real, agrégala y repórtala.

## 9. LO ÚNICO QUE LE PIDES AL USUARIO (con pasos exactos)

1. **Cuenta de GitHub** (si no tiene) y permiso para crear el repositorio.
2. **Bot de Telegram:** "Abre Telegram → busca @BotFather → escribe /newbot → ponle nombre 'Cazador Ofertas' → copia el código largo que te da y pégamelo aquí. Luego escríbele 'hola' a tu bot." Con eso tú obtienes el `chat_id` usando `getUpdates`.
3. **Sus intereses:** categorías que le importan (ej. tecnología, electrodomésticos, herramientas, súper) y productos de su lista de deseos con precio máximo.
4. Pegar los dos secretos en GitHub: dale los clics exactos o hazlo tú si tienes acceso.

Nada más. Todo lo demás lo haces tú.

## 10. CÓMO REPORTAS AL USUARIO

Al terminar cada fase, en máximo 6 líneas, sin tecnicismos:
- ✅ Qué quedó funcionando (con números reales: "6 tiendas, 4,320 productos leídos, 27 ofertas fuertes hoy").
- ⚠️ Qué falló y qué hiciste.
- 👉 Qué necesitas de él (si algo).

## 11. TERMINADO = TODO ESTO SE CUMPLE

- [ ] Mínimo 6 tiendas guatemaltecas funcionando, verificadas.
- [ ] El sistema corre solo cada hora, 3 corridas seguidas sin error.
- [ ] El usuario recibió en Telegram al menos 1 alerta real (no de prueba).
- [ ] La página web abre en el celular, con filtros y última actualización correcta en hora de Guatemala.
- [ ] Ninguna alerta 🔥/🚨 sin historial que la respalde.
- [ ] Si se apaga una tienda a propósito (URL falsa), el sistema avisa y las demás siguen.
- [ ] README en español y `config.yml` explicado.
- [ ] Entregas al usuario: link de la página, link del bot, y en 5 líneas cómo usarlo.

## 12. ENTREGA PARA AUDITORÍA

El proyecto será auditado por otra IA. Al terminar, crea `ENTREGA.md` en la raíz con:
1. Lista de la sección 11 marcada, con la prueba de cada punto (salida del comando, captura o link).
2. Tabla de fuentes: tienda, método (API/HTML/Playwright), productos leídos en la última corrida, estado.
3. Decisiones que tomaste distintas a este prompt y por qué.
4. Errores conocidos o cosas que quedaron a medias (sé honesto; esconderlos es peor).
5. Links: repositorio, página web, últimas 3 corridas de Actions.

Empieza por la Fase 0 ahora. No pidas permiso para empezar; pide solo lo de la sección 9 cuando lo necesites.
