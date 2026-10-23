"""Convierte un diseño HTML/CSS/JS en video (o en foto). Sin plantillas: cualquier diseño que se pueda
hacer en una página web (letras, capas, máscaras, 3D CSS, partículas, canvas) se vuelve MP4.
El HTML debe definir window.frame(t) que dibuja el instante t (segundos) y window.DURACION.
Uso: python -I render_html.py <diseño.html> <salida.mp4|salida.png> [ancho=1080] [alto=1920] [fps=30] [musica.mp3|-]
Para foto (.png/.jpg): renderiza el instante window.FOTO_T (o 0).
"""
import sys, os, subprocess, shutil, pathlib
from playwright.sync_api import sync_playwright

FFMPEG = shutil.which("ffmpeg") or os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe")
html, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1080
H = int(sys.argv[4]) if len(sys.argv) > 4 else 1920
FPS = int(sys.argv[5]) if len(sys.argv) > 5 else 30
musica = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] not in ("", "-") else None

with sync_playwright() as p:
    nav = p.chromium.launch(channel="chrome", headless=True)  # usa el Chrome ya instalado
    pg = nav.new_page(viewport={"width": W, "height": H})
    pg.goto(pathlib.Path(html).as_uri())
    pg.wait_for_function("typeof window.frame === 'function'")
    pg.evaluate("document.fonts.ready")
    if out.lower().endswith((".png", ".jpg", ".jpeg")):
        pg.evaluate("t => window.frame(t)", pg.evaluate("window.FOTO_T || 0"))
        pg.screenshot(path=out, type="png" if out.lower().endswith(".png") else "jpeg")
        print(out); sys.exit()
    dur = pg.evaluate("window.DURACION")
    n = int(dur * FPS)
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-"]
    cmd += ["-i", musica] if musica else ["-f", "lavfi", "-t", f"{dur:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
    if musica:
        cmd += ["-af", f"afade=t=in:d=0.3,afade=t=out:st={dur - 1:.2f}:d=1,loudnorm=I=-14:TP=-1"]
    cmd += ["-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{dur:.2f}", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        pg.evaluate("t => window.frame(t)", i / FPS)
        ff.stdin.write(pg.screenshot(type="png"))
    ff.stdin.close(); ff.wait()
    nav.close()
print(out, f"{dur:.1f}s", f"{W}x{H}")
