"""Video vertical de producto (Reels/Historias/anuncio Meta) a partir de fotos.
Uso: python -I video_producto.py <salida.mp4> <guion.txt> [musica.mp3] [formato 9x16|4x5]
guion.txt: una línea por escena -> ruta_foto | texto (texto opcional; "|" sin texto = escena limpia)
Cada escena dura 2.4 s con acercamiento suave, texto dentro de la zona segura y fundido entre escenas.
"""
import sys, os, subprocess, tempfile, shutil, textwrap
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageChops

FFMPEG = shutil.which("ffmpeg") or os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe")
FONT = r"C:\Windows\Fonts\seguibl.ttf"  # Segoe UI Black: gruesa y limpia
FPS, DUR, FADE = 30, 2.4, 0.35

out, guion = sys.argv[1], sys.argv[2]
musica = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] not in ("", "-") else None
formato = sys.argv[4] if len(sys.argv) > 4 else "9x16"
W, H = (1080, 1920) if formato == "9x16" else (1080, 1350)

escenas = []
for ln in open(guion, encoding="utf-8"):
    if ln.strip() and not ln.startswith("#"):
        foto, _, texto = ln.partition("|")
        escenas.append((foto.strip(), texto.strip()))

tmp = tempfile.mkdtemp()

def base(foto):
    """Fondo = la misma foto ampliada, desenfocada y oscurecida; encima la foto completa."""
    im = Image.open(foto).convert("RGB")
    bg = im.copy()
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1))
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.55)
    # recortar margen vacío (fotos de estudio) para que el producto se vea grande
    esquina = Image.new("RGB", im.size, im.getpixel((5, 5)))
    caja = ImageChops.difference(im, esquina).convert("L").point(lambda p: 255 if p > 28 else 0).getbbox()
    fg = im
    if caja:
        pad = int(0.06 * max(caja[2] - caja[0], caja[3] - caja[1]))
        fg = im.crop((max(0, caja[0] - pad), max(0, caja[1] - pad),
                      min(im.width, caja[2] + pad), min(im.height, caja[3] + pad)))
    fg = fg.copy()
    fg.thumbnail((int(W * 0.94), int(H * (0.58 if formato == "9x16" else 0.66))), Image.LANCZOS)
    cy = 0.60 if formato == "9x16" else 0.60
    bg.paste(fg, ((W - fg.width) // 2, int(H * cy - fg.height / 2)))
    return bg

def capa_texto(texto):
    """Texto blanco grueso con sombra suave, dentro de la zona segura (arriba 14%, lados 6%)."""
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if not texto:
        return capa
    f = ImageFont.truetype(FONT, 78 if len(texto) < 28 else 64)
    lineas = textwrap.wrap(texto, width=18 if len(texto) < 28 else 22)
    alto = sum(f.getbbox(l)[3] + 14 for l in lineas)
    y = int(H * 0.15) if formato == "9x16" else int(H * 0.06)
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds, d = ImageDraw.Draw(sombra), ImageDraw.Draw(capa)
    yy = y
    for l in lineas:
        w = f.getlength(l)
        ds.text(((W - w) / 2 + 3, yy + 4), l, font=f, fill=(0, 0, 0, 200))
        d.text(((W - w) / 2, yy), l, font=f, fill=(255, 255, 255, 255))
        yy += f.getbbox(l)[3] + 14
    sombra = sombra.filter(ImageFilter.GaussianBlur(6))
    return Image.alpha_composite(sombra, capa)

entradas, filtros = [], []
for i, (foto, texto) in enumerate(escenas):
    b = os.path.join(tmp, f"b{i}.png"); t = os.path.join(tmp, f"t{i}.png")
    base(foto).resize((W * 2, H * 2), Image.LANCZOS).save(b)  # 2x para que el zoom no tiemble
    capa_texto(texto).save(t)
    entradas += ["-loop", "1", "-t", str(DUR), "-i", b, "-loop", "1", "-t", str(DUR), "-i", t]
    n = int(DUR * FPS)
    zoom = "1+0.06*on/%d" % n if i % 2 == 0 else "1.06-0.06*on/%d" % n  # alterna acercar/alejar
    filtros.append(
        f"[{2*i}:v]zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},setsar=1[z{i}];"
        f"[{2*i+1}:v]format=rgba,fade=in:st=0.15:d=0.3:alpha=1[tx{i}];"
        f"[z{i}][tx{i}]overlay=0:0:shortest=1,format=yuv420p[e{i}]")

cadena, prev, t_acum = [], "e0", DUR
for i in range(1, len(escenas)):
    off = t_acum - FADE
    cadena.append(f"[{prev}][e{i}]xfade=transition=fade:duration={FADE}:offset={off:.2f}[x{i}]")
    prev, t_acum = f"x{i}", off + DUR
total = t_acum
graf = ";".join(filtros + cadena)

cmd = [FFMPEG, "-y", "-loglevel", "error"] + entradas
if musica:
    cmd += ["-i", musica]
    graf += f";[{2*len(escenas)}:a]atrim=0:{total:.2f},afade=t=in:d=0.5,afade=t=out:st={total-1:.2f}:d=1,volume=0.8[a]"
else:
    cmd += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
cmd += ["-filter_complex", graf, "-map", f"[{prev}]",
        "-map", "[a]" if musica else f"{2*len(escenas)}:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{total:.2f}", out]
subprocess.run(cmd, check=True)
shutil.rmtree(tmp, ignore_errors=True)
print(out, f"{total:.1f}s", f"{W}x{H}")
