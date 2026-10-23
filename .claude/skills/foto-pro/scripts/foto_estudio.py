"""Foto de estudio profesional: producto recortado, fondo limpio, sombra natural, sin texto.
Uso: python -I foto_estudio.py <carpeta_origen> <carpeta_salida> <foto1.jpg,foto2.jpg> [blanco|gris]
"""
import sys, os
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from rembg import remove, new_session

src_dir, out_dir, files = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
fondo = sys.argv[4] if len(sys.argv) > 4 else "gris"
# opcional: borrar una zona del recorte, en fracciones del ancho/alto: "x0,y0,x1,y1"
borrar = [float(v) for v in sys.argv[5].split(",")] if len(sys.argv) > 5 else None
os.makedirs(out_dir, exist_ok=True)
session = new_session("isnet-general-use")
S = 1200

def fondo_estudio():
    if fondo == "blanco":
        return Image.new("RGB", (S, S), (255, 255, 255))
    # degradado radial suave tipo estudio (centro claro, bordes apenas más oscuros)
    bg = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(bg)
    for r in range(S, 0, -6):
        v = int(236 + 16 * (1 - r / S))
        d.ellipse([S / 2 - r, S / 2 - r * 0.9, S / 2 + r, S / 2 + r * 0.9], fill=v)
    return Image.merge("RGB", (bg, bg, bg)).filter(ImageFilter.GaussianBlur(40))

for i, name in enumerate(files, 1):
    img = Image.open(os.path.join(src_dir, name)).convert("RGB")
    img.thumbnail((2000, 2000))
    cut = remove(img, session=session, alpha_matting=True,
                 alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=15,
                 alpha_matting_erode_size=8)
    # dejar solo la pieza más grande (quita etiquetas sueltas y restos)
    import numpy as np
    from scipy import ndimage
    al = np.array(cut.getchannel("A"))
    lab, n = ndimage.label(al > 60)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(al), lab, range(1, n + 1))
        keep = 1 + int(np.argmax(sizes))
        mask = ndimage.binary_dilation(lab == keep, iterations=3)
        al = np.where(mask, al, 0).astype("uint8")
        cut.putalpha(Image.fromarray(al))
    cut = cut.crop(cut.getbbox())
    if borrar:
        w, h = cut.size
        ImageDraw.Draw(cut).rectangle([borrar[0]*w, borrar[1]*h, borrar[2]*w, borrar[3]*h], fill=(0,0,0,0))
        cut = cut.crop(cut.getbbox())
    # retoque suave: contraste y nitidez
    rgb, a = cut.convert("RGB"), cut.getchannel("A")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.06)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.25)
    cut = Image.merge("RGBA", (*rgb.split(), a))
    # producto ocupa ~78% del lienzo
    cut.thumbnail((int(S * 0.78), int(S * 0.72)), Image.LANCZOS)
    x = (S - cut.width) // 2
    y = int(S * 0.47 - cut.height / 2)
    bg = fondo_estudio().convert("RGBA")
    # sombra de contacto: silueta aplastada y difuminada
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sil = Image.new("RGBA", cut.size, (0, 0, 0, 120))
    sil.putalpha(a.resize(cut.size).point(lambda p: 110 if p > 40 else 0))
    sil = sil.resize((int(cut.width * 0.95), max(8, int(cut.height * 0.10))))
    sh.paste(sil, (x + int(cut.width * 0.025), y + cut.height - int(sil.height * 0.55)), sil)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    bg = Image.alpha_composite(bg, sh)
    bg.alpha_composite(cut, (x, y))
    out = os.path.join(out_dir, f"{i:02d}_estudio.jpg")
    bg.convert("RGB").save(out, quality=95)
    print(out)
