"""Control de calidad ANTES de entregar una pieza (como director creativo).
Video: medida y proporción, duración, fps, códec, volumen (LUFS y pico), cuadros negros, imagen congelada,
cuánto se mueve en los primeros 3 s (gancho) y hoja de cuadros con las ZONAS QUE TAPA LA APP en rojo.
Foto: medida, proporción, peso, y la misma hoja con zonas.
Uso: python -I revisar.py <archivo> [9x16|4x5|1x1] [hoja.jpg]
"""
import sys, os, re, json, subprocess, shutil
from PIL import Image, ImageDraw

FFMPEG = shutil.which("ffmpeg") or os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe")
FFPROBE = FFMPEG.replace("ffmpeg.exe", "ffprobe.exe")
f = sys.argv[1]; meta = sys.argv[2] if len(sys.argv) > 2 else "9x16"
hoja = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(f)[0] + "_revision.jpg"
RAT = {"9x16": 9 / 16, "4x5": 4 / 5, "1x1": 1.0}[meta]
# zonas que tapa la interfaz (fracción): arriba, abajo, lados
ZONA = {"9x16": (0.14, 0.35, 0.06), "4x5": (0.0, 0.0, 0.0), "1x1": (0.0, 0.0, 0.0)}[meta]
ok, mal = [], []
chk = lambda cond, bien, malo: (ok if cond else mal).append(bien if cond else malo)

def zonas(im):
    im = im.convert("RGB"); w, h = im.size
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    t, b, s = ZONA
    for r in ([0, 0, w, h * t], [0, h * (1 - b), w, h], [0, 0, w * s, h], [w * (1 - s), 0, w, h]):
        d.rectangle(r, fill=(255, 0, 0, 70))
    return Image.alpha_composite(im.convert("RGBA"), capa).convert("RGB")

if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
    im = Image.open(f); w, h = im.size
    chk(abs(w / h - RAT) < 0.01, f"Proporción {meta} correcta ({w}x{h})", f"Proporción {w}x{h} NO es {meta}")
    chk(min(w, h) >= 1080, "Resolución suficiente", f"Resolución baja ({w}x{h}); mínimo 1080 de lado corto")
    kb = os.path.getsize(f) / 1024; chk(kb < 30 * 1024, f"Peso {kb:.0f} KB", f"Pesa {kb/1024:.1f} MB (>30 MB)")
    zonas(im).resize((540, int(540 * h / w))).save(hoja)
else:
    p = json.loads(subprocess.run([FFPROBE, "-v", "error", "-show_streams", "-show_format", "-of", "json", f],
                                  capture_output=True, text=True).stdout)
    v = next(s for s in p["streams"] if s["codec_type"] == "video"); a = [s for s in p["streams"] if s["codec_type"] == "audio"]
    w, h, dur = int(v["width"]), int(v["height"]), float(p["format"]["duration"])
    fps = eval(v["r_frame_rate"])
    chk(abs(w / h - RAT) < 0.01, f"Proporción {meta} correcta ({w}x{h})", f"Proporción {w}x{h} NO es {meta}")
    chk(min(w, h) >= 1080, "Resolución suficiente", f"Resolución baja ({w}x{h})")
    chk(v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p", "Códec H.264 yuv420p (compatible)", f"Códec {v['codec_name']}/{v.get('pix_fmt')} puede fallar en Meta")
    chk(24 <= fps <= 60, f"{fps:.0f} fps", f"fps raros: {fps}")
    chk(5 <= dur <= 30, f"Duración {dur:.1f} s (bien para anuncio)", f"Duración {dur:.1f} s (anuncio ideal 6-15 s, máx. 30)")
    chk(bool(a), "Tiene pista de audio", "Sin pista de audio (algunas ubicaciones la piden)")
    log = subprocess.run([FFMPEG, "-hide_banner", "-i", f, "-vf", "blackdetect=d=0.25:pix_th=0.06,freezedetect=n=0.003:d=1.2",
                          "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    if a:
        I = re.findall(r"I:\s+(-?[\d.]+) LUFS", log); pk = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
        if I:
            li = float(I[-1]); chk(-16 <= li <= -12 or li < -60, f"Volumen {li} LUFS", f"Volumen {li} LUFS (redes ~-14)")
        if pk:
            chk(float(pk[-1]) <= -0.9, f"Pico {pk[-1]} dB", f"Pico {pk[-1]} dB: puede distorsionar (máx. -1)")
    negros = re.findall(r"black_start:([\d.]+)", log); cong = re.findall(r"freeze_start: ([\d.]+)", log)
    chk(not negros, "Sin cuadros negros", f"Cuadros negros en {', '.join(negros)} s")
    chk(not cong, "Sin imagen congelada", f"Imagen quieta >1.2 s en {', '.join(cong)} s (¿pierde ritmo?)")
    # gancho: cuánto CAMBIA la imagen en los primeros 3 s (cortes o movimiento continuo)
    import numpy as np
    from io import BytesIO
    def cuadro(t):
        raw = subprocess.run([FFMPEG, "-loglevel", "error", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=180:-2",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        return np.asarray(Image.open(BytesIO(raw)).convert("L"), dtype=float)
    cs = [cuadro(t) for t in np.arange(0, min(3, dur - .1), .5)]
    mov = float(np.mean([np.abs(a - b).mean() for a, b in zip(cs, cs[1:])])) if len(cs) > 1 else 0
    chk(mov >= 4, f"Gancho: la imagen cambia {mov:.1f} (de 255) cada medio segundo en los primeros 3 s",
        f"Primeros 3 s casi quietos (cambio {mov:.1f}): gancho débil")
    # hoja de cuadros con zonas
    tiempos = [min(dur - .05, x) for x in (0.5, 1.5, 2.9, dur * .5, dur * .8, dur - .3)]
    cuadros = []
    for t in tiempos:
        raw = subprocess.run([FFMPEG, "-loglevel", "error", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-f", "image2pipe",
                              "-vcodec", "png", "-"], capture_output=True).stdout
        from io import BytesIO
        cuadros.append(zonas(Image.open(BytesIO(raw))).resize((270, int(270 * h / w))))
    s = Image.new("RGB", (270 * len(cuadros), cuadros[0].height), "white")
    for i, c in enumerate(cuadros): s.paste(c, (270 * i, 0))
    s.save(hoja)
print("BIEN:"); [print("  +", x) for x in ok]
print("CORREGIR:" if mal else "CORREGIR: nada"); [print("  -", x) for x in mal]
print("Hoja con zonas que tapa la app (rojo):", hoja)
