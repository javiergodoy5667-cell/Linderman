"""Mejora fotos ORIGINALES sin recortar el fondo (cuando el recorte falla o Javier quiere la foto real).
Corrige luz y color, endereza tamaño a cuadrado 1:1 o vertical 4:5, y da nitidez.
Uso: python -I foto_mejorar.py <carpeta_origen> <carpeta_salida> <f1.jpg,f2.jpg> [1x1|4x5|libre]
"""
import sys, os
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

src, dst, files = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
marco = sys.argv[4] if len(sys.argv) > 4 else "libre"
os.makedirs(dst, exist_ok=True)

for i, name in enumerate(files, 1):
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, name))).convert("RGB")
    # balance de blancos "mundo gris": quita el tono amarillo/azul de la luz
    a = np.asarray(im).astype("float32")
    medias = a.reshape(-1, 3).mean(0)
    a *= (medias.mean() / medias) ** 0.6  # 0.6 = corrección suave, no total
    im = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
    im = ImageOps.autocontrast(im, cutoff=0.8)          # negros y blancos limpios
    im = ImageEnhance.Color(im).enhance(1.08)           # color apenas más vivo
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=3))
    if marco in ("1x1", "4x5"):
        r = 1.0 if marco == "1x1" else 0.8
        w, h = im.size
        # rellenar (no cortar el producto): fondo = la foto desenfocada
        cw, ch = (max(w, int(h * r)), max(h, int(w / r)))
        bg = im.resize((cw, ch)).filter(ImageFilter.GaussianBlur(30))
        bg = ImageEnhance.Brightness(bg).enhance(0.9)
        bg.paste(im, ((cw - w) // 2, (ch - h) // 2))
        im = bg
    im.thumbnail((2048, 2048), Image.LANCZOS)
    out = os.path.join(dst, f"{i:02d}_mejorada.jpg")
    im.save(out, quality=93)
    print(out, im.size)
