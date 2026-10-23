"""Diseño de sonido: efectos sintetizados (sin derechos de autor) puestos en el segundo exacto,
música opcional que BAJA sola cuando hay voz (ducking), y volumen final para redes (-14 LUFS).
Uso: python -I sonido.py <video> <salida.mp4> "<t:efecto,t:efecto,...>" [musica.mp3|-] [vol_musica=0.35]
Efectos: golpe, whoosh, campana, clic, subida, ding, bajo (golpe grave de cine)
Ej:  "0.15:whoosh,0.45:golpe,3.6:campana,7.1:golpe,7.9:ding"
"""
import sys, os, subprocess, shutil, tempfile, wave
import numpy as np

FFMPEG = shutil.which("ffmpeg") or os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe")
SR = 48000
rng = np.random.default_rng(3)

def env(n, a, d):  # ataque y caída exponencial
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-np.maximum(t - a, 0) / d)

def lp(x, k):  # filtro paso-bajo simple (suaviza el ruido)
    return np.convolve(x, np.ones(k) / k, mode="same")

def golpe():
    n = int(.5 * SR); t = np.arange(n) / SR
    cuerpo = np.sin(2 * np.pi * (55 + 90 * np.exp(-t * 30)) * t) * env(n, .002, .16)
    chasquido = lp(rng.standard_normal(n), 4) * env(n, .001, .025) * .5
    return cuerpo + chasquido

def bajo():
    n = int(1.4 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (38 + 40 * np.exp(-t * 6)) * t) * env(n, .005, .45)

def whoosh():
    n = int(.55 * SR); t = np.arange(n) / SR
    ruido = rng.standard_normal(n)
    k = (3 + 40 * (1 - np.sin(np.pi * t / t[-1]))).astype(int)  # el "barrido": filtro que abre y cierra
    out = np.array([ruido[max(0, i - k[i]):i + 1].mean() for i in range(n)])
    return out * np.sin(np.pi * t / t[-1]) ** 2 * 2.2

def campana():
    n = int(2.2 * SR); t = np.arange(n) / SR
    parc = [(1, 1), (2.76, .5), (5.4, .25), (8.93, .12)]  # parciales inarmónicos de campana de ring
    return sum(a * np.sin(2 * np.pi * 820 * f * t) * np.exp(-t * (1.4 + f * .6)) for f, a in parc) * env(n, .001, 5) * .6

def clic():
    n = int(.06 * SR); return lp(rng.standard_normal(n), 2) * env(n, .0005, .008) * .8

def ding():
    n = int(1.0 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1318 * t) + .4 * np.sin(2 * np.pi * 2637 * t)) * env(n, .002, .25) * .5

def subida():
    n = int(1.2 * SR); t = np.arange(n) / SR
    tono = np.sin(2 * np.pi * (200 + 900 * (t / t[-1]) ** 2) * t) * .3
    return (tono + lp(rng.standard_normal(n), 6) * .4) * (t / t[-1]) ** 2

EF = dict(golpe=golpe, bajo=bajo, whoosh=whoosh, campana=campana, clic=clic, ding=ding, subida=subida)

src, out, lista = sys.argv[1], sys.argv[2], sys.argv[3]
musica = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] not in ("", "-") else None
vol_m = float(sys.argv[5]) if len(sys.argv) > 5 else 0.35

dur = float(subprocess.run([FFMPEG.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
pista = np.zeros(int((dur + 2.5) * SR))
for item in [x for x in lista.split(",") if x.strip()]:
    t0, nombre = item.split(":")
    s = EF[nombre.strip()](); i = int(float(t0) * SR)
    pista[i:i + len(s)] += s[:len(pista) - i]
pista = pista[:int(dur * SR)]
pista = pista / max(1e-6, np.abs(pista).max()) * .8

tmp = tempfile.mkdtemp(); fx = os.path.join(tmp, "fx.wav")
with wave.open(fx, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((pista * 32767).astype("<i2").tobytes())

# 0:a = audio original (voz o silencio), 1:a = efectos, 2:a = música (baja cuando suena la voz)
cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", src, "-i", fx]
if musica:
    cmd += ["-stream_loop", "-1", "-i", musica]
    graf = (f"[0:a]asplit=2[voz][llave];[2:a]atrim=0:{dur:.2f},volume={vol_m},"
            f"afade=t=out:st={dur - 1.2:.2f}:d=1.2[m];"
            "[m][llave]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=500[mduck];"
            "[voz][1:a][mduck]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1:LRA=11,alimiter=limit=0.89:level=false[a]")
else:
    graf = "[0:a][1:a]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=11,alimiter=limit=0.89:level=false[a]"
cmd += ["-filter_complex", graf, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-t", f"{dur:.2f}", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
shutil.rmtree(tmp, ignore_errors=True)
print(out)
