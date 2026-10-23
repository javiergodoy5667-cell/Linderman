"""Subtítulos automáticos palabra por palabra (estilo Hormozi) para clips donde alguien habla.
Escucha el audio con Whisper local (gratis, sin internet después de bajar el modelo), arma el video 9:16,
pinta la palabra que se dice, y nivela el volumen para redes (-14 LUFS).
Uso: python -I subtitulos.py <video_entrada> <salida.mp4> [color_resaltado_hex=FFD400] [modelo=small]
"""
import sys, os, subprocess, shutil, tempfile

FFMPEG = shutil.which("ffmpeg") or os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe")
src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
hl = sys.argv[3] if len(sys.argv) > 3 else "FFD400"
modelo = sys.argv[4] if len(sys.argv) > 4 else "small"
W, H, POR_GRUPO = 1080, 1920, 3
ass_col = "&H00%s%s%s&" % (hl[4:6], hl[2:4], hl[0:2])  # ASS usa BGR

import numpy as np
from faster_whisper import WhisperModel
# audio a 16 kHz mono con FFmpeg (el lector interno de faster-whisper choca con la versión de "av")
pcm = subprocess.run([FFMPEG, "-loglevel", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
m = WhisperModel(modelo, device="cpu", compute_type="int8")
# vocabulario del negocio para que no se equivoque con marcas, lugares y moneda
VOCAB = "Bosch, Toyota, 4Runner, Tacoma, quetzales, Petapa, Zacapa, camarón, mariscos, libra, WhatsApp, Marketplace"
segs, _ = m.transcribe(audio, language="es", word_timestamps=True, vad_filter=True, initial_prompt=VOCAB)
import re
CORRIGE = {"boch": "Bosch", "bosh": "Bosch"}  # agregar aquí cada error nuevo que aparezca
palabras = []
for s in segs:
    for w in s.words:
        p = re.sub(r"[^\wáéíóúüñÁÉÍÓÚÜÑ$%Q-]", "", w.word.strip())  # sin puntuación, estilo limpio
        if p:
            palabras.append((w.start, w.end, CORRIGE.get(p.lower(), p)))
if not palabras:
    sys.exit("No se escuchó voz en el video.")

def t(x):
    h, r = divmod(max(0, x), 3600); mi, s = divmod(r, 60)
    return f"{int(h)}:{int(mi):02d}:{s:05.2f}"

ass = [
    "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, MarginL, MarginR, MarginV, Outline, Shadow, BorderStyle",
    # centro-abajo pero FUERA del 35% inferior que tapa la app; márgenes = 6% de lado
    f"Style: S,Segoe UI Black,88,&H00FFFFFF&,&H00000000&,&H80000000&,1,2,70,70,{int(H*0.37)},7,3,1", "",
    "[Events]", "Format: Layer, Start, End, Style, Text",
]
grupos = [palabras[i:i + POR_GRUPO] for i in range(0, len(palabras), POR_GRUPO)]
for gi, g in enumerate(grupos):
    fin_grupo = grupos[gi + 1][0][0] if gi + 1 < len(grupos) else g[-1][1] + 0.4
    for j, (ini, fin, _) in enumerate(g):
        hasta = g[j + 1][0] if j + 1 < len(g) else min(fin_grupo, fin + 0.6)
        txt = " ".join(("{\\c%s\\fscx108\\fscy108}%s{\\r}" % (ass_col, p.upper())) if k == j else p.upper()
                       for k, (_, _, p) in enumerate(g))
        # la primera palabra del grupo entra con un pequeño "pop"
        pop = "{\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)}" if j == 0 else ""
        ass.append(f"Dialogue: 0,{t(ini)},{t(hasta)},S,{pop}{txt}")

tmp = tempfile.mkdtemp()
open(os.path.join(tmp, "s.ass"), "w", encoding="utf-8").write("\n".join(ass))
# vertical: si el clip es horizontal, fondo desenfocado + clip al centro
vf = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:2,eq=brightness=-0.12[bg];"
      f"[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,subtitles=s.ass[v]")
subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-filter_complex", vf, "-map", "[v]", "-map", "0:a",
                "-af", "loudnorm=I=-14:TP=-1:LRA=11", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
               check=True, cwd=tmp)
shutil.rmtree(tmp, ignore_errors=True)
print(out, len(palabras), "palabras")
print(" ".join(p for _, _, p in palabras))
