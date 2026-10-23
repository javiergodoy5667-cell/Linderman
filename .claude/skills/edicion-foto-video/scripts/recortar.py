"""Recorta el producto y lo guarda como PNG transparente (para usarlo en cualquier diseño).
Uso: python -I recortar.py <foto> <salida.png>
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage
from rembg import remove, new_session

im = Image.open(sys.argv[1]).convert("RGB"); im.thumbnail((2000, 2000))
cut = remove(im, session=new_session("isnet-general-use"), alpha_matting=True,
             alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
al = np.array(cut.getchannel("A")); lab, n = ndimage.label(al > 60)
if n > 1:  # dejar solo la pieza más grande
    keep = 1 + int(np.argmax(ndimage.sum(np.ones_like(al), lab, range(1, n + 1))))
    cut.putalpha(Image.fromarray(np.where(ndimage.binary_dilation(lab == keep, iterations=3), al, 0).astype("uint8")))
cut.crop(cut.getbbox()).save(sys.argv[2])
# colores dominantes del producto (para la dirección de arte)
px = np.array(cut.convert("RGBA")).reshape(-1, 4); px = px[px[:, 3] > 200][:, :3]
q = (px // 32) * 32 + 16; vals, cnt = np.unique(q, axis=0, return_counts=True)
print(sys.argv[2], "colores:", ["#%02X%02X%02X" % tuple(v) for v in vals[np.argsort(-cnt)][:5]])
