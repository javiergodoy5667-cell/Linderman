"""Video PRO de producto (estilo anuncio de marca): estudio oscuro, producto recortado flotando,
texto animado con acento de color, tarjeta final con precio y botón. Cuadro por cuadro con Pillow -> FFmpeg.
Uso: python -I video_pro.py <salida.mp4> <guion.txt> [musica.mp3|-] [9x16|4x5] [acento_hex]
guion.txt (una escena por línea, separado por "|"):
  ruta_foto | KICKER | Titular            -> recorta el producto (fondo fuera)
  ruta_foto | KICKER | Titular | marco     -> foto completa con esquinas redondeadas (etiquetas, placas)
  FINAL | Q600 | Escríbeme hoy | Entrega en Petapa | ruta_foto_producto
"""
import sys, os, subprocess, shutil, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from scipy import ndimage

FFMPEG = shutil.which("ffmpeg") or os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe")
F_BLACK, F_BOLD, F_REG = (r"C:\Windows\Fonts\seguibl.ttf", r"C:\Windows\Fonts\segoeuib.ttf",
                          r"C:\Windows\Fonts\segoeui.ttf")
FPS, D, X = 30, 2.7, 0.45  # duración escena, cruce entre escenas

out, guion = sys.argv[1], sys.argv[2]
musica = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] not in ("", "-") else None
formato = sys.argv[4] if len(sys.argv) > 4 else "9x16"
ACC = tuple(int((sys.argv[5] if len(sys.argv) > 5 else "F2B33D")[i:i + 2], 16) for i in (0, 2, 4))
W, H = (1080, 1920) if formato == "9x16" else (1080, 1350)
TOP = 0.15 if formato == "9x16" else 0.07  # debajo de la zona ocupada por la app

ease = lambda t: 1 - (1 - max(0, min(1, t))) ** 3  # salida suave

def fondo():
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / W) ** 2 + ((y - H * 0.55) / H) ** 2)
    v = np.clip(1 - r * 1.6, 0, 1)
    c0, c1 = np.array([12, 14, 18]), np.array([44, 48, 56])  # carbón, centro más claro
    img = (c0 + (c1 - c0) * v[..., None]).astype("uint8")
    img = img + np.random.default_rng(1).integers(0, 3, img.shape, dtype="uint8")  # grano anti-bandas
    return Image.fromarray(img).convert("RGBA")

_ses = None
def recorte(ruta):
    global _ses
    from rembg import remove, new_session
    _ses = _ses or new_session("isnet-general-use")
    im = Image.open(ruta).convert("RGB"); im.thumbnail((1800, 1800))
    cut = remove(im, session=_ses, alpha_matting=True, alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
    al = np.array(cut.getchannel("A")); lab, n = ndimage.label(al > 60)
    if n > 1:
        keep = 1 + int(np.argmax(ndimage.sum(np.ones_like(al), lab, range(1, n + 1))))
        cut.putalpha(Image.fromarray(np.where(ndimage.binary_dilation(lab == keep, iterations=3), al, 0).astype("uint8")))
    cut = cut.crop(cut.getbbox())
    rgb = ImageEnhance.Contrast(cut.convert("RGB")).enhance(1.08)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.3)
    return Image.merge("RGBA", (*rgb.split(), cut.getchannel("A")))

def marco(ruta):
    im = Image.open(ruta).convert("RGB"); im.thumbnail((1600, 1600))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=int(im.width * 0.04), fill=255)
    im = im.convert("RGBA"); im.putalpha(m); return im

def ajustar(p, maxw, maxh):
    s = min(maxw / p.width, maxh / p.height); return p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS)

def sombra(p):
    a = p.getchannel("A").point(lambda v: 150 if v > 40 else 0)
    sh = Image.new("RGBA", p.size, (0, 0, 0, 0)); sh.putalpha(a)
    sh = sh.resize((int(p.width * 0.9), max(10, int(p.height * 0.08))))
    lienzo = Image.new("RGBA", (sh.width + 160, sh.height + 160), (0, 0, 0, 0))
    lienzo.paste(sh, (80, 80)); return lienzo.filter(ImageFilter.GaussianBlur(26))

def texto_img(txt, font, color, espacio=0):
    f = ImageFont.truetype(*font)
    if espacio:
        anchos = [f.getlength(c) + espacio for c in txt]; w = int(sum(anchos))
    else:
        w = int(f.getlength(txt))
    h = int(f.size * 1.35)
    im = Image.new("RGBA", (w + 20, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if espacio:
        x = 10
        for c, a in zip(txt, anchos): d.text((x, 0), c, font=f, fill=color); x += a
    else:
        d.text((10, 0), txt, font=f, fill=color)
    return im

def partir(txt, font, maxw):
    f = ImageFont.truetype(*font); lineas, act = [], ""
    for p in txt.split():
        prueba = (act + " " + p).strip()
        if f.getlength(prueba) <= maxw: act = prueba
        else: lineas.append(act); act = p
    return lineas + [act]

def pegar(base, im, x, y, alpha):
    if alpha <= 0: return
    if alpha < 1:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(x), int(y)))

# ---------- preparar escenas ----------
BG = fondo()
escenas = []
for ln in open(guion, encoding="utf-8"):
    if not ln.strip() or ln.startswith("#"): continue
    c = [v.strip() for v in ln.split("|")]
    if c[0].upper() == "FINAL":
        prod = ajustar(recorte(c[4]), W * 0.62, H * 0.20) if len(c) > 4 and c[4] else None
        escenas.append(dict(tipo="final", precio=c[1], cta=c[2], sub=c[3] if len(c) > 3 else "", prod=prod,
                            sh=sombra(prod) if prod else None))
    else:
        es_marco = len(c) > 3 and c[3].lower() == "marco"
        p = marco(c[0]) if es_marco else recorte(c[0])
        p = ajustar(p, W * (0.80 if es_marco else 0.86), H * (0.36 if formato == "9x16" else 0.48))
        tit = partir(c[2], (F_BLACK, 84), W * 0.84)
        escenas.append(dict(tipo="prod", prod=p, sh=None if es_marco else sombra(p), marco=es_marco,
                            kick=texto_img(c[1].upper(), (F_BOLD, 34), ACC + (255,), espacio=6),
                            tit=[texto_img(l, (F_BLACK, 84), (255, 255, 255, 255)) for l in tit]))

def cuadro_escena(e, t):
    im = BG.copy()
    if e["tipo"] == "prod":
        k = ease(t / 0.6); s = (0.94 + 0.06 * k) * (1 + 0.035 * t / D)  # entra y sigue acercándose
        p = e["prod"]; pw, ph = int(p.width * s), int(p.height * s); pr = p.resize((pw, ph), Image.BILINEAR)
        cy = H * (0.60 if formato == "9x16" else 0.62)
        x, y = (W - pw) / 2, cy - ph / 2 + 30 * (1 - k)
        if e["sh"]:
            sh = e["sh"].resize((int(e["sh"].width * s), e["sh"].height))
            pegar(im, sh, (W - sh.width) / 2, y + ph - sh.height / 2 - 10, k)
        elif e["marco"]:
            sm = Image.new("RGBA", (pw + 120, ph + 120), (0, 0, 0, 0))
            ImageDraw.Draw(sm).rounded_rectangle([60, 70, pw + 60, ph + 70], radius=40, fill=(0, 0, 0, 170))
            pegar(im, sm.filter(ImageFilter.GaussianBlur(28)), x - 60, y - 60, k)
        pegar(im, pr, x, y, k)
        y0 = H * TOP
        kk = ease((t - 0.15) / 0.5)
        pegar(im, e["kick"], (W - e["kick"].width) / 2, y0 + 20 * (1 - kk), kk)
        lw = int(90 * ease((t - 0.3) / 0.5))  # línea de acento que se dibuja
        if lw > 2:
            ImageDraw.Draw(im).rectangle([W / 2 - lw / 2, y0 + 62, W / 2 + lw / 2, y0 + 67], fill=ACC + (255,))
        yy = y0 + 90
        for j, l in enumerate(e["tit"]):
            kt = ease((t - 0.35 - 0.12 * j) / 0.55)
            pegar(im, l, (W - l.width) / 2, yy + 40 * (1 - kt), kt); yy += l.height - 8
    else:
        y0 = H * TOP
        k1 = ease((t - 0.1) / 0.5)
        kick = texto_img("PRECIO", (F_BOLD, 34), ACC + (255,), espacio=6)
        pegar(im, kick, (W - kick.width) / 2, y0, k1)
        pr = texto_img(e["precio"], (F_BLACK, 210), (255, 255, 255, 255))
        k2 = ease((t - 0.25) / 0.6)
        pegar(im, pr, (W - pr.width) / 2, y0 + 50 + 30 * (1 - k2), k2)
        if e["sub"]:
            sb = texto_img(e["sub"], (F_REG, 44), (200, 204, 212, 255))
            pegar(im, sb, (W - sb.width) / 2, y0 + 340, ease((t - 0.5) / 0.5))
        if e["prod"]:
            kp = ease((t - 0.4) / 0.7); p = e["prod"]; s = 0.95 + 0.05 * kp
            pr2 = p.resize((int(p.width * s), int(p.height * s)), Image.BILINEAR)
            yp = H * (0.47 if formato == "9x16" else 0.55) - pr2.height / 2
            pegar(im, e["sh"], (W - e["sh"].width) / 2, yp + pr2.height - e["sh"].height / 2 - 10, kp)
            pegar(im, pr2, (W - pr2.width) / 2, yp, kp)
        kb = ease((t - 0.8) / 0.5)  # botón con latido suave
        pul = 1 + 0.03 * math.sin(max(0, t - 1.3) * 5)
        f = ImageFont.truetype(F_BLACK, 52); tw = f.getlength(e["cta"])
        bw, bh = int((tw + 140) * pul), int(118 * pul)
        btn = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); db = ImageDraw.Draw(btn)
        db.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=bh // 2, fill=ACC + (255,))
        db.text(((bw - tw) / 2, (bh - 70) / 2), e["cta"], font=f, fill=(18, 18, 20, 255))
        yb = H * (0.60 if formato == "9x16" else 0.80)
        pegar(im, btn, (W - bw) / 2, yb + 30 * (1 - kb), kb)
    return im

# ---------- línea de tiempo y render ----------
inicio = [i * (D - X) for i in range(len(escenas))]
total = inicio[-1] + D
nfr = int(total * FPS)
cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
cmd += ["-i", musica] if musica else ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
af = [f"-af", f"afade=t=in:d=0.4,afade=t=out:st={total - 1.2:.2f}:d=1.2"] if musica else []
cmd += ["-map", "0:v", "-map", "1:a"] + af + ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.2f}", out]
ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for n in range(nfr):
    T = n / FPS
    act = [(i, T - s) for i, s in enumerate(inicio) if s <= T < s + D]
    if len(act) == 1:
        fr = cuadro_escena(escenas[act[0][0]], act[0][1])
    else:
        a = cuadro_escena(escenas[act[0][0]], act[0][1]); b = cuadro_escena(escenas[act[1][0]], act[1][1])
        fr = Image.blend(a, b, ease(act[1][1] / X))
    ff.stdin.write(fr.convert("RGB").tobytes())
ff.stdin.close(); ff.wait()
print(out, f"{total:.1f}s", f"{W}x{H}")
