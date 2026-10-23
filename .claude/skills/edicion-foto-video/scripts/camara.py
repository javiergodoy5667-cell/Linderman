"""Movimientos de cámara de cine sobre UNA foto (estilo Higgsfield), gratis y local.
Separa el producto del fondo (rembg), rellena el hueco del fondo (OpenCV) y mueve cada capa a distinta
velocidad -> sensación 3D (paralaje). Desenfoque de movimiento real en los movimientos rápidos.
Uso: python -I camara.py <foto> <salida.mp4> <movimiento> [segundos=3] [9x16|4x5|1x1]
Movimientos: dolly_in, dolly_out, super_dolly_in, dolly_zoom_in, dolly_zoom_out, crash_zoom_in, crash_zoom_out,
  yoyo_zoom, pan_left, pan_right, arc_left, arc_right, crane_up, crane_down, handheld, wiggle,
  focus_change, low_shutter, hero_cam, whip_pan, static
"""
import sys, os, math, shutil, subprocess
import numpy as np, cv2
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from scipy import ndimage

FFMPEG = shutil.which("ffmpeg") or os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe")
foto, out, mov = sys.argv[1], sys.argv[2], sys.argv[3]
DUR = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
fmt = sys.argv[5] if len(sys.argv) > 5 else "9x16"
W, H = {"9x16": (1080, 1920), "4x5": (1080, 1350), "1x1": (1080, 1080)}[fmt]
FPS = 30; N = int(DUR * FPS)

# ---- capas: producto (frente) y fondo rellenado, armadas en un lienzo fuente 20% más grande que la salida ----
from rembg import remove, new_session
im = Image.open(foto).convert("RGB"); im.thumbnail((2200, 2200))
cut = remove(im, session=new_session("isnet-general-use"))
al = np.array(cut.getchannel("A"))
lab, n = ndimage.label(al > 60)
if n > 1:
    keep = 1 + int(np.argmax(ndimage.sum(np.ones_like(al), lab, range(1, n + 1))))
    al = np.where(ndimage.binary_dilation(lab == keep, iterations=2), al, 0).astype("uint8")
# fondo: tapar el producto y rellenar (a baja resolución para que sea rápido y suave)
m = cv2.dilate((al > 20).astype("uint8") * 255, np.ones((25, 25), np.uint8))
k = 4; peq = cv2.resize(np.array(im), None, fx=1 / k, fy=1 / k); mp = cv2.resize(m, (peq.shape[1], peq.shape[0]))
rel = cv2.inpaint(peq, mp, 9, cv2.INPAINT_TELEA)
rel = cv2.GaussianBlur(cv2.resize(rel, (im.width, im.height)), (0, 0), 6)
mm = cv2.GaussianBlur(m, (0, 0), 8)[..., None] / 255.0
bg0 = Image.fromarray((np.array(im) * (1 - mm) + rel * mm).astype("uint8"))
# encuadre: el producto COMPLETO cabe (ancho 82% o alto 52% del cuadro), centrado un poco abajo
x0, y0, x1, y1 = Image.fromarray(al).getbbox()
IW, IH = int(W * 1.2), int(H * 1.2)
z = min(W * .82 / (x1 - x0), H * .52 / (y1 - y0))
px, py = IW / 2 - (x0 + x1) / 2 * z, IH * .53 - (y0 + y1) / 2 * z
foto_z = (int(im.width * z), int(im.height * z))
# lo que la foto no cubre: el mismo fondo ampliado y muy desenfocado (como "extender" la escena)
cov = max(IW / im.width, IH / im.height) * 1.05
ext = bg0.resize((int(im.width * cov), int(im.height * cov))).filter(ImageFilter.GaussianBlur(28))
bg = ext.crop(((ext.width - IW) // 2, (ext.height - IH) // 2, (ext.width - IW) // 2 + IW, (ext.height - IH) // 2 + IH))
borde = Image.new("L", foto_z, 0); ImageDraw.Draw(borde).rectangle([40, 40, foto_z[0] - 40, foto_z[1] - 40], fill=255)
bg.paste(bg0.resize(foto_z, Image.LANCZOS), (int(px), int(py)), borde.filter(ImageFilter.GaussianBlur(35)))
fg = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
fgi = im.copy(); fgi.putalpha(Image.fromarray(al)); fg.alpha_composite(fgi.resize(foto_z, Image.LANCZOS), (int(px), int(py)))

ease = lambda t: 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, t)))   # suave al inicio y al final
fast = lambda t: 1 - (1 - max(0, min(1, t))) ** 4                      # golpe rápido que frena

def capa(img, s, dx, dy, rot=0.0, blur=0.0):
    """Escala s, mueve dx/dy (px del lienzo), gira rot° alrededor del centro; devuelve lienzo W x H."""
    a = math.radians(rot); c, si = math.cos(a) / s, math.sin(a) / s
    cx, cy = IW / 2 - dx / s, IH / 2 - dy / s
    # matriz inversa: punto del lienzo -> punto de la imagen
    M = (c, si, cx - c * W / 2 - si * H / 2, -si, c, cy + si * W / 2 - c * H / 2)
    r = img.transform((W, H), Image.AFFINE, M, resample=Image.BICUBIC)
    return r.filter(ImageFilter.GaussianBlur(blur)) if blur > 0.3 else r

def estado(t):
    """(escala_fondo, escala_frente, dx_fondo, dx_frente, dy_fondo, dy_frente, giro, desenfoque_fondo, desenfoque_frente)"""
    e, f = ease(t), fast(t)
    P = dict(sb=1, sf=1, xb=0, xf=0, yb=0, yf=0, r=0, bb=0, bf=0)
    if mov == "dolly_in":        P.update(sb=1 + .06 * e, sf=1 + .12 * e)
    elif mov == "dolly_out":     P.update(sb=1.06 - .06 * e, sf=1.12 - .12 * e)
    elif mov == "super_dolly_in": P.update(sb=1 + .10 * e, sf=1 + .35 * e)
    elif mov == "dolly_zoom_in": P.update(sb=1 + .45 * e, sf=1.0)              # vértigo: el fondo se agranda, el producto igual
    elif mov == "dolly_zoom_out": P.update(sb=1.45 - .45 * e, sf=1.0)
    elif mov == "crash_zoom_in": P.update(sb=1 + .35 * f, sf=1 + .55 * f)
    elif mov == "crash_zoom_out": P.update(sb=1.35 - .35 * f, sf=1.55 - .55 * f)
    elif mov == "yoyo_zoom":
        y = math.sin(math.pi * t) ** 2; P.update(sb=1 + .25 * y, sf=1 + .4 * y)
    elif mov in ("pan_left", "pan_right"):
        d = -1 if mov == "pan_left" else 1; P.update(xb=d * 70 * (e - .5) * 2, xf=d * 150 * (e - .5) * 2, sb=1.03, sf=1.05)
    elif mov in ("arc_left", "arc_right"):
        d = -1 if mov == "arc_left" else 1
        P.update(xb=-d * 120 * (e - .5) * 2, xf=d * 60 * (e - .5) * 2, r=d * 2.5 * (e - .5) * 2, sb=1.06, sf=1.08 + .04 * e)
    elif mov in ("crane_up", "crane_down"):
        d = -1 if mov == "crane_up" else 1; P.update(yb=d * 90 * (e - .5) * 2, yf=d * 190 * (e - .5) * 2, sb=1.04, sf=1.06)
    elif mov == "handheld":
        sx = sum(math.sin(t * DUR * w + p) * a for w, p, a in ((1.3, 0, 9), (2.9, 1, 5), (6.1, 2, 2)))
        sy = sum(math.sin(t * DUR * w + p) * a for w, p, a in ((1.1, 3, 8), (3.3, 4, 4), (5.7, 5, 2)))
        P.update(xb=sx * .7, xf=sx, yb=sy * .7, yf=sy, r=.6 * math.sin(t * DUR * 1.7), sb=1.04, sf=1.05)
    elif mov == "wiggle":                                                         # efecto "3D" de ida y vuelta
        w = 1 if int(t * DUR * 8) % 2 == 0 else -1; P.update(xb=-w * 18, xf=w * 18, sb=1.03, sf=1.04)
    elif mov == "focus_change":                                                    # foco del fondo al producto
        P.update(bb=10 * e, bf=8 * (1 - e), sf=1 + .03 * e, sb=1 + .02 * e)
    elif mov == "hero_cam":                                                        # sube y empuja, el fondo se oscurece
        P.update(sb=1.02 + .05 * e, sf=1 + .14 * e, yf=60 * (1 - e), bb=3 * e)
    elif mov == "low_shutter":                                                     # empuje con estela
        P.update(sb=1 + .08 * e, sf=1 + .16 * e)
    elif mov == "whip_pan":                                                        # barrido rápido de salida
        P.update(xb=-300 * f ** 2, xf=-420 * f ** 2, sb=1.35, sf=1.40)  # sin salirse del cuadro: el barrido lo da el desenfoque
    return P

def cuadro(t):
    P = estado(t)
    lienzo = capa(bg, P["sb"], P["xb"], P["yb"], P["r"] * .6, P["bb"])
    if mov == "hero_cam":
        lienzo = ImageEnhance.Brightness(lienzo).enhance(1 - .25 * ease(t))
    lienzo = lienzo.convert("RGBA")
    lienzo.alpha_composite(capa(fg, P["sf"], P["xf"], P["yf"], P["r"], P["bf"]))
    if mov == "hero_cam":  # barrido de luz que cruza el producto
        luz = Image.new("L", (W, H), 0); d = ImageDraw.Draw(luz); x = -400 + 1900 * ease((t - .2) / .7)
        d.polygon([(x, 0), (x + 160, 0), (x - 340, H), (x - 500, H)], fill=60)
        lienzo = Image.composite(Image.new("RGBA", (W, H), (255, 255, 255, 255)), lienzo, luz.filter(ImageFilter.GaussianBlur(40)))
    return lienzo.convert("RGB")

rapido = mov in ("crash_zoom_in", "crash_zoom_out", "whip_pan", "yoyo_zoom", "low_shutter")
SUB = 6 if rapido else 1                                 # sub-cuadros = desenfoque de movimiento real
ff = subprocess.Popen([FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
                      stdin=subprocess.PIPE)
for i in range(N):
    if SUB == 1:
        fr = np.asarray(cuadro(i / (N - 1)), dtype=np.uint8)
    else:
        span = (3.0 if mov in ("low_shutter", "whip_pan") else 1.0) / (N - 1)   # obturador lento = estela más larga
        acc = sum(np.asarray(cuadro(max(0, i / (N - 1) - span * j / SUB)), dtype=np.float32) for j in range(SUB))
        fr = (acc / SUB).astype(np.uint8)
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
print(out, mov, f"{DUR}s", f"{W}x{H}")
