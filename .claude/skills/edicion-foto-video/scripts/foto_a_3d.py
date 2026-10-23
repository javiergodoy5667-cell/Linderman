"""Foto -> modelo 3D (.glb) con modelos abiertos y gratis en Hugging Face (corren en SUS servidores, no en la PC).
Prueba en orden: Stable Fast 3D (rápido), TRELLIS.2 (Microsoft, MIT), Hunyuan3D-2.1 (Tencent).
Sin cuenta: pocos minutos gratis al día. Con cuenta gratis: Javier guarda su token como variable HF_TOKEN
(Linderman nunca lo ve ni lo escribe).
Uso: python -I foto_a_3d.py <foto> <salida.glb>
"""
import sys, os, shutil
from gradio_client import Client, handle_file

foto, out = sys.argv[1], sys.argv[2]
tok = os.environ.get("HF_TOKEN")

def glb_de(r):
    for x in (r if isinstance(r, (list, tuple)) else [r]):
        x = x.get("value", x) if isinstance(x, dict) else x
        if isinstance(x, str) and x.lower().endswith(".glb"):
            return x

def sf3d():
    c = Client("stabilityai/stable-fast-3d", hf_token=tok, verbose=False)
    return glb_de(c.predict(handle_file(foto), 0.85, "None", -1, 1024, api_name="/run_button"))

def trellis():
    c = Client("microsoft/TRELLIS.2", hf_token=tok, verbose=False)
    c.predict(api_name="/start_session")
    img = c.predict(handle_file(foto), api_name="/preprocess_image")
    c.predict(handle_file(img), 0, "1024", api_name="/image_to_3d")
    return glb_de(c.predict(200000, 2048, api_name="/extract_glb"))

def hunyuan():
    c = Client("tencent/Hunyuan3D-2.1", hf_token=tok, verbose=False)
    return glb_de(c.predict(image=handle_file(foto), api_name="/generation_all"))

for nombre, f in (("Stable Fast 3D", sf3d), ("TRELLIS.2", trellis), ("Hunyuan3D-2.1", hunyuan)):
    try:
        g = f()
        if g:
            shutil.copy(g, out); print("OK", nombre, out); sys.exit(0)
    except Exception as e:
        print("falló", nombre, "->", str(e)[:160])
sys.exit("Ningún modelo respondió (límite diario gratis o servidor caído). Reintentar mañana o con HF_TOKEN.")
