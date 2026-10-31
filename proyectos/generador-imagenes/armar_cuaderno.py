# Arma linderman_imagenes.ipynb (cuaderno para Kaggle) metiendo adentro app.html.
# Uso: python armar_cuaderno.py
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
APP = open(os.path.join(AQUI, "app.html"), encoding="utf-8").read()
assert "'''" not in APP

INTRO = """# Linderman Imágenes (ComfyUI gratis en Kaggle)

**Antes de darle Run All**, en el panel de la derecha (Settings / Session options):
1. **Accelerator → GPU T4 x2**
2. **Internet → On** (si no aparece, falta verificar su teléfono en kaggle.com/settings)

Luego arriba: **Run All**. Tarda unos 8-12 minutos la primera vez (baja los modelos).
Al final sale un botón verde **ABRIR GENERADOR**: ese link sirve en la compu y en el teléfono.

- Deje esta pestaña abierta mientras use el generador. Si la cierra, Kaggle apaga la máquina.
- Las imágenes se guardan en la carpeta `imagenes` (panel derecho → Output). Bájelas antes de apagar.
- No comparta el link: el que lo tenga puede usar su máquina.
"""

AJUSTES = """# ===== AJUSTES: lo único que se toca =====
MODELO_REALISTA = True    # RealVisXL V5: fotos que parecen reales (~7 GB)
MODELO_ANIME    = True    # NoobAI-XL 1.1: anime y personajes (~7 GB)
MODELO_FLUX     = False   # FLUX.1 dev: el más realista, pero 3-5 veces más lento (~18 GB)

# Modelos o estilos (LoRA) de Civitai: el número de VERSIÓN que sale en el link
# civitai.com/models/XXXX?modelVersionId=NUMERO  ->  ejemplo: CIVITAI = [1759168, 2071281]
# Necesita el secreto CIVITAI_TOKEN (Add-ons → Secrets). Solo modelos SDXL, Pony o Illustrious.
CIVITAI = []
"""

INSTALAR = r"""# ===== 1. Revisar la máquina e instalar ComfyUI =====
import os, sys, re, json, time, shutil, subprocess, urllib.request

class Alto(Exception):
    pass

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:]); print(r.stderr[-3000:])
        raise Alto("Falló este paso: " + cmd)
    return r.stdout

try:
    gpu = sh("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader").strip().splitlines()[0]
except Alto:
    raise Alto("No hay tarjeta. Panel derecho → Accelerator → GPU T4 x2, y vuelva a darle Run All.")
print("✅ Tarjeta:", gpu)
try:
    urllib.request.urlopen("https://huggingface.co", timeout=20)
except Exception:
    raise Alto("Sin internet. Panel derecho → Internet: On (necesita el teléfono verificado en Kaggle).")
print("✅ Internet")

BASE = max([d for d in ["/kaggle/temp", "/tmp"] if os.path.isdir(d)], key=lambda d: shutil.disk_usage(d).free)
COMFY = BASE + "/ComfyUI"
SALIDA = "/kaggle/working/imagenes"
os.makedirs(SALIDA, exist_ok=True)

if not os.path.exists(COMFY + "/main.py"):
    try:
        tag = json.load(urllib.request.urlopen("https://api.github.com/repos/comfyanonymous/ComfyUI/releases/latest", timeout=20))["tag_name"]
    except Exception:
        tag = "master"
    sh(f"git clone -q --depth 1 --branch {tag} https://github.com/comfyanonymous/ComfyUI {COMFY}")
    print("✅ ComfyUI", tag)
GGUF = COMFY + "/custom_nodes/ComfyUI-GGUF"
if not os.path.exists(GGUF):
    sh(f"git clone -q --depth 1 https://github.com/city96/ComfyUI-GGUF {GGUF}")

# Dependencias, sin tocar el torch que ya trae Kaggle (cambiarlo rompe la tarjeta)
reqs = [l for l in open(COMFY + "/requirements.txt").read().splitlines()
        if l.strip() and not l.startswith("#") and not re.match(r"^(torch|torchvision|torchaudio)\s*($|[<>=!~;])", l.strip())]
reqs += [l for l in open(GGUF + "/requirements.txt").read().splitlines() if l.strip() and not l.startswith("#")]
open(BASE + "/reqs.txt", "w").write("\n".join(reqs))
sh(f"{sys.executable} -m pip install -q --disable-pip-version-check -r {BASE}/reqs.txt")
print("✅ Dependencias")

# La página sencilla (se abre en  .../app)
APP_DIR = COMFY + "/custom_nodes/linderman_app"
os.makedirs(APP_DIR, exist_ok=True)
open(APP_DIR + "/app.html", "w", encoding="utf-8").write(APP_HTML)
open(APP_DIR + "/__init__.py", "w").write('''import os
from aiohttp import web
from server import PromptServer

_HTML = os.path.join(os.path.dirname(os.path.realpath(__file__)), "app.html")

@PromptServer.instance.routes.get("/app")
async def linderman_app(request):
    return web.FileResponse(_HTML, headers={"Cache-Control": "no-store"})

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
''')
print("✅ Página lista")
"""

MODELOS = r"""# ===== 2. Bajar los modelos =====
from concurrent.futures import ThreadPoolExecutor
import struct

HF = "https://huggingface.co/"
M = COMFY + "/models"
lista = [("vae", "sdxl_vae_fp16_fix.safetensors", HF + "madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors", 0.4)]
if MODELO_REALISTA:
    lista.append(("checkpoints", "RealVisXL_V5.0_fp16.safetensors", HF + "SG161222/RealVisXL_V5.0/resolve/main/RealVisXL_V5.0_fp16.safetensors", 7))
if MODELO_ANIME:
    lista.append(("checkpoints", "NoobAI-XL-v1.1.safetensors", HF + "Laxhar/noobai-XL-1.1/resolve/main/NoobAI-XL-v1.1.safetensors", 7))
if MODELO_FLUX:
    lista += [("unet", "flux1-dev-Q8_0.gguf", HF + "city96/FLUX.1-dev-gguf/resolve/main/flux1-dev-Q8_0.gguf", 12.7),
              ("clip", "t5xxl_fp8_e4m3fn.safetensors", HF + "comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors", 4.9),
              ("clip", "clip_l.safetensors", HF + "comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors", 0.3),
              ("vae", "ae.safetensors", HF + "Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors", 0.4)]

# Civitai: se pregunta qué es cada número antes de bajarlo
if CIVITAI:
    try:
        from kaggle_secrets import UserSecretsClient
        TOKEN = UserSecretsClient().get_secret("CIVITAI_TOKEN")
    except Exception:
        raise Alto("Falta el secreto CIVITAI_TOKEN (Add-ons → Secrets) o no tiene el cuadrito activado para este cuaderno.")
    for vid in CIVITAI:
        try:
            info = json.load(urllib.request.urlopen(urllib.request.Request(
                f"https://civitai.com/api/v1/model-versions/{vid}", headers={"Authorization": "Bearer " + TOKEN}), timeout=30))
        except Exception as e:
            print(f"⚠️ Civitai {vid}: no se encontró ({e}). Lo salto."); continue
        tipo, base = info["model"]["type"], info.get("baseModel", "")
        carpeta = {"Checkpoint": "checkpoints", "LORA": "loras", "LoCon": "loras"}.get(tipo)
        if not carpeta:
            print(f"⚠️ Civitai {vid}: es tipo {tipo}, la página solo usa modelos y LoRAs. Lo salto."); continue
        if not any(x in base for x in ["SDXL", "Pony", "Illustrious", "NoobAI"]):
            print(f"⚠️ Civitai {vid}: es para {base}; la página solo usa SDXL, Pony o Illustrious. Lo salto."); continue
        arch = [f for f in info["files"] if f["name"].endswith(".safetensors")]
        if not arch:
            print(f"⚠️ Civitai {vid}: no trae archivo .safetensors (los .ckpt pueden traer virus). Lo salto."); continue
        f = next((x for x in arch if x.get("primary")), arch[0])
        sep = "&" if "?" in f["downloadUrl"] else "?"
        lista.append((carpeta, f["name"], f["downloadUrl"] + sep + "token=" + TOKEN, f["sizeKB"] / 1024 / 1024))
        print(f"• Civitai {vid}: {info['model']['name']} ({tipo}, {base})")

falta = sum(t for c, n, u, t in lista if not os.path.exists(f"{M}/{c}/{n}"))
libre = shutil.disk_usage(BASE).free / 1e9
if falta * 1.07 + 3 > libre:
    raise Alto(f"No cabe: faltan {falta:.0f} GB y hay {libre:.0f} GB libres. Apague MODELO_FLUX o algún otro en AJUSTES.")

def archivo_bueno(ruta):
    # Revisa que sea un modelo de verdad y no una página de error
    with open(ruta, "rb") as fh:
        ini = fh.read(8)
        if ruta.endswith(".gguf"):
            return ini[:4] == b"GGUF"
        n = struct.unpack("<Q", ini)[0]
        if n > 100_000_000:
            return False
        json.loads(fh.read(n))
    return True

def bajar(item):
    carpeta, nombre, url, gb = item
    destino = f"{M}/{carpeta}/{nombre}"
    if os.path.exists(destino):
        return f"✅ {nombre} (ya estaba)"
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    inicio = time.time()
    for intento in range(3):
        r = subprocess.run(["curl", "-L", "--fail", "-s", "-S", "--retry", "5", "--retry-delay", "5",
                            "-C", "-", "-o", destino + ".part", url], capture_output=True, text=True)
        if r.returncode == 0:
            break
        time.sleep(5)
    else:
        return f"❌ {nombre}: no bajó ({r.stderr.strip()[-200:]})"
    try:
        ok = archivo_bueno(destino + ".part")
    except Exception:
        ok = False
    if not ok:
        os.remove(destino + ".part")
        return f"❌ {nombre}: llegó dañado (si es de Civitai, revise el token)"
    os.rename(destino + ".part", destino)
    return f"✅ {nombre}: {os.path.getsize(destino)/1e9:.1f} GB en {time.time()-inicio:.0f} s"

print(f"Bajando {len(lista)} archivos (~{falta:.0f} GB)…")
with ThreadPoolExecutor(3) as ex:
    resultados = list(ex.map(bajar, lista))
print("\n".join(resultados))
if any(r.startswith("❌") for r in resultados):
    raise Alto("Algún archivo no bajó. Vuelva a correr esta celda: sigue donde se quedó.")
"""

ARRANCAR = r"""# ===== 3. Prender el generador y sacar el link =====
from IPython.display import display, HTML

def cola(ruta, n=40):
    try:
        return "".join(open(ruta, errors="replace").readlines()[-n:])
    except Exception:
        return ""

def prender_comfy():
    subprocess.run("pkill -f 'ComfyUI/main.py'", shell=True)
    log = open(BASE + "/comfy.log", "w")
    p = subprocess.Popen([sys.executable, COMFY + "/main.py", "--listen", "127.0.0.1", "--port", "8188",
                          "--output-directory", SALIDA, "--preview-method", "none", "--disable-auto-launch"],
                         cwd=COMFY, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(300):
        if p.poll() is not None:
            print(cola(BASE + "/comfy.log"))
            raise Alto("ComfyUI no arrancó (el error está arriba). Mándele esa parte a Linderman.")
        try:
            urllib.request.urlopen("http://127.0.0.1:8188/app", timeout=3)
            return p
        except Exception:
            time.sleep(2)
    raise Alto("ComfyUI tardó demasiado en arrancar.\n" + cola(BASE + "/comfy.log"))

def prender_tunel():
    cf = BASE + "/cloudflared"
    if not os.path.exists(cf):
        sh(f"curl -L --fail -s -o {cf} https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && chmod +x {cf}")
    log = BASE + "/tunel.log"
    p = subprocess.Popen([cf, "tunnel", "--no-autoupdate", "--url", "http://127.0.0.1:8188"],
                         stdout=open(log, "w"), stderr=subprocess.STDOUT)
    for _ in range(60):
        m = re.search(r"https://[-a-z0-9]+\.trycloudflare\.com", cola(log, 200))
        if m:
            return p, m.group(0)
        if p.poll() is not None:
            break
        time.sleep(2)
    raise Alto("No salió el link.\n" + cola(log))

def mostrar(url):
    display(HTML(f'<a href="{url}/app" target="_blank" style="display:inline-block;background:#3fb27f;color:#06130d;'
                 f'padding:14px 22px;border-radius:10px;font:700 20px sans-serif;text-decoration:none">ABRIR GENERADOR</a>'
                 f'<p style="font-size:15px">{url}/app &nbsp;·&nbsp; ComfyUI completo: {url}</p>'))

comfy = prender_comfy()
print("✅ ComfyUI prendido")
tunel, url = prender_tunel()
time.sleep(5)  # el link nuevo tarda unos segundos en responder
mostrar(url)
print("Deje esta celda corriendo. Para apagar: botón ■ (Stop) arriba.")

try:
    while True:
        time.sleep(30)
        if comfy.poll() is not None:
            print(cola(BASE + "/comfy.log"))
            print("⚠️ ComfyUI se cayó (arriba está por qué). Lo vuelvo a prender…")
            comfy = prender_comfy()
        if tunel.poll() is not None:
            print("⚠️ Se cortó el link. Saco uno nuevo:")
            tunel, url = prender_tunel()
            mostrar(url)
except KeyboardInterrupt:
    tunel.terminate(); comfy.terminate()
    print("Apagado. Sus imágenes están en Output → imagenes.")
"""

ZIP = r"""# ===== 4. (Opcional) Juntar todas las imágenes en un .zip para bajarlas de una vez =====
# Primero pare la celda 3 con ■ y luego corra esta.
from IPython.display import FileLink
shutil.make_archive("/kaggle/working/imagenes_linderman", "zip", SALIDA)
FileLink("imagenes_linderman.zip")
"""

def md(t):
    return {"cell_type": "markdown", "metadata": {}, "source": t.splitlines(True)}

def code(t):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": t.splitlines(True)}

cuaderno = {
    "nbformat": 4, "nbformat_minor": 4,
    "metadata": {
        "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
        "language_info": {"name": "python"},
        "kaggle": {"accelerator": "nvidiaTeslaT4", "isInternetEnabled": True, "isGpuEnabled": True},
    },
    "cells": [md(INTRO), code(AJUSTES), code("APP_HTML = r'''" + APP + "'''\n"), code(INSTALAR), code(MODELOS), code(ARRANCAR), code(ZIP)],
}
cuaderno["cells"][2]["metadata"] = {"jupyter": {"source_hidden": True}}

with open(os.path.join(AQUI, "linderman_imagenes.ipynb"), "w", encoding="utf-8") as f:
    json.dump(cuaderno, f, ensure_ascii=False, indent=1)
print("Listo: linderman_imagenes.ipynb")
