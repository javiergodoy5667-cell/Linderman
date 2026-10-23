"""Limpia un clip crudo del teléfono antes de diseñarlo o subtitularlo:
1) estabiliza (vid.stab, 2 pasadas) 2) quita silencios y pausas (cortes de salto con 0.12 s de colchón)
3) limpia el audio (quita zumbido grave y ruido de fondo) 4) corrige luz y color suave.
Uso: python -I limpiar_clip.py <entrada> <salida.mp4> [--sin-estabilizar] [--sin-cortes] [--umbral_db=-35] [--pausa=0.45]
"""
import sys, os, re, subprocess, shutil, tempfile

FFMPEG = shutil.which("ffmpeg") or os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe")
FFPROBE = FFMPEG.replace("ffmpeg.exe", "ffprobe.exe")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
ops = {a.split("=")[0]: (a.split("=")[1] if "=" in a else True) for a in sys.argv[1:] if a.startswith("--")}
src, out = os.path.abspath(args[0]), os.path.abspath(args[1])
umbral, pausa, PAD = float(ops.get("--umbral_db", -35)), float(ops.get("--pausa", 0.45)), 0.12
tmp = tempfile.mkdtemp()
dur = float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                           capture_output=True, text=True).stdout)

# 1) estabilizar: pasada de análisis (se corre dentro de tmp para que transforms.trf no tenga ruta con espacios)
vf = []
if "--sin-estabilizar" not in ops:
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-vf", "vidstabdetect=shakiness=6:accuracy=12:result=t.trf",
                    "-f", "null", "-"], check=True, cwd=tmp)
    vf.append("vidstabtransform=input=t.trf:smoothing=12:zoom=2:optzoom=0,unsharp=5:5:0.6")
vf.append("eq=contrast=1.05:saturation=1.08:gamma=1.02")  # luz y color suave, no "filtro"

# 2) partes con voz (todo lo que NO es silencio largo)
partes = [(0.0, dur)]
def por_palabras():
    """Con ruido de fondo el 'silencio' no existe: se corta donde NO hay palabras (Whisper)."""
    import numpy as np
    from faster_whisper import WhisperModel
    pcm = subprocess.run([FFMPEG, "-loglevel", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = WhisperModel("base", device="cpu", compute_type="int8").transcribe(audio, language="es", word_timestamps=True)
    w = [(x.start, x.end) for s in segs for x in s.words]
    if not w: return None
    res, a, b = [], w[0][0], w[0][1]
    for s, e in w[1:]:
        if s - b > pausa: res.append((max(0, a - PAD), min(dur, b + PAD))); a = s
        b = e
    res.append((max(0, a - PAD), min(dur, b + PAD + 0.15)))
    return res

if "--sin-cortes" not in ops and (r := por_palabras()):
    partes = r
elif "--sin-cortes" not in ops:
    log = subprocess.run([FFMPEG, "-i", src, "-af", f"silencedetect=noise={umbral}dB:d={pausa}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    partes, t = [], 0.0
    for s, e in zip(ini, fin + [dur] * (len(ini) - len(fin))):
        if s - t > 0.05:
            partes.append((max(0, t - PAD), min(dur, s + PAD)))
        t = e
    if dur - t > 0.05:
        partes.append((max(0, t - PAD), dur))
    partes = partes or [(0.0, dur)]

# 3) armar: cada parte recortada, unidas, audio limpio
af = "highpass=f=80,afftdn=nr=12:nf=-40:tn=1,lowpass=f=14000,loudnorm=I=-14:TP=-1:LRA=11,alimiter=limit=0.89:level=false"
g = []
for i, (a, b) in enumerate(partes):
    g.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
             f"afade=t=in:d=0.02,afade=t=out:st={max(0, b - a - 0.02):.3f}:d=0.02[a{i}]")  # micro-fundido: sin "clics"
g.append("".join(f"[v{i}][a{i}]" for i in range(len(partes))) + f"concat=n={len(partes)}:v=1:a=1[vc][ac]")
g.append(f"[vc]{','.join(vf)}[v];[ac]{af}[a]")
subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-filter_complex", ";".join(g), "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", out], check=True, cwd=tmp)
nuevo = sum(b - a for a, b in partes)
shutil.rmtree(tmp, ignore_errors=True)
print(out, f"{dur:.1f}s -> {nuevo:.1f}s", f"{len(partes)} partes")
