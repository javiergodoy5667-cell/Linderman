# Generador de imágenes gratis (ComfyUI en Kaggle)

Hecho: 2026-10-31. Modelos: RealVisXL V5 (realismo), NoobAI-XL 1.1 (anime), FLUX.1 dev Q8 (opcional).
Corre en la tarjeta gratis de Kaggle (NVIDIA T4, 15 GB). ~30 h de tarjeta por semana, sesiones de hasta ~9-12 h.

## Una sola vez
1. Cree una cuenta en kaggle.com (mejor con un Gmail aparte, no el del negocio).
2. kaggle.com/settings → **Phone verification**: ponga su número y el código que le llega. Sin esto no le prestan tarjeta ni internet.
3. kaggle.com → **Create → New Notebook** → menú **File → Import Notebook** → suba `linderman_imagenes.ipynb`.
4. (Solo si va a usar Civitai) civitai.com → su perfil → Settings → **API Keys → Add API key**, copie la llave.
   En el cuaderno de Kaggle: **Add-ons → Secrets → Add Secret**, nombre `CIVITAI_TOKEN`, valor = la llave, y active el cuadrito.

## Cada vez que lo quiera usar
1. Abra el cuaderno en Kaggle.
2. Panel derecho: **Accelerator → GPU T4 x2** e **Internet → On**.
3. Arriba: **Run All**. La primera vez tarda 8-12 min. Las siguientes, igual (Kaggle borra todo al apagar).
4. Al final sale el botón verde **ABRIR GENERADOR**. Ese link sirve en la compu y en el teléfono.
5. Deje la pestaña de Kaggle abierta. Al terminar: botón ■ (Stop) y luego **Power off** (arriba a la derecha), para no gastar horas.
6. Sus imágenes: panel derecho → **Output → imagenes**. O corra la última celda y le arma un .zip.

## Cómo pedir buenas imágenes
- En inglés sale mejor. Diga qué es, dónde, la luz y el tipo de foto: `photo of a woman cooking shrimp ceviche in a beach kitchen, natural light, 35mm`.
- Realismo → "Fotos realistas (RealVisXL)". Anime/personajes → "Anime y personajes (NoobAI)".
- Si una imagen le gustó y quiere variarla poco: copie su **semilla** en "Más opciones" y cambie solo una palabra.
- Velocidad aproximada en la T4 (no medido aún): SDXL 20-40 s por imagen; FLUX 2-4 min.

## Agregar modelos de Civitai
- En la celda AJUSTES: `CIVITAI = [número]`. El número es el `modelVersionId` del link de Civitai.
- Solo acepta archivos **.safetensors** (los .ckpt pueden traer virus) y modelos SDXL, Pony o Illustrious.
- Los LoRA (estilos extra) aparecen en "Más opciones → Estilo extra".

## Si algo falla
- "No hay tarjeta" → Accelerator en GPU T4 x2.
- "Sin internet" → Internet On; si no aparece, falta la verificación del teléfono.
- "Algún archivo no bajó" → vuelva a correr esa celda; sigue donde se quedó.
- El link dejó de abrir → la celda 3 saca uno nuevo sola; búsquelo abajo.
- Cualquier otro error → copie lo rojo de Kaggle y páseselo a Linderman.

## Reglas
- Uso personal. No comparta el link ni lo cobre como servicio.
- Prohibido: caras de personas reales sin su permiso y cualquier cosa con menores.
