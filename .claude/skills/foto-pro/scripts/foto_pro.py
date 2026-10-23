import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from rembg import remove, new_session

SRC = sys.argv[1]           # carpeta con fotos originales
OUT = sys.argv[2]           # carpeta de salida
FILES = sys.argv[3].split(",")
TITLE = sys.argv[4]
SUB = sys.argv[5]
PRICE = sys.argv[6]
CONTACT = "WhatsApp 5544-9803 · San Miguel Petapa"

os.makedirs(OUT, exist_ok=True)
session = new_session("isnet-general-use")
F = "C:/Windows/Fonts/"
fb = lambda s: ImageFont.truetype(F + "segoeuib.ttf", s)
fr = lambda s: ImageFont.truetype(F + "segoeui.ttf", s)

W = H = 1080
for i, name in enumerate(FILES, 1):
    src = Image.open(os.path.join(SRC, name)).convert("RGB")
    src.thumbnail((1600, 1600))
    cut = remove(src, session=session)
    bbox = cut.getbbox()
    cut = cut.crop(bbox)
    # fondo degradado claro
    bg = Image.new("RGB", (W, H), (245, 246, 248))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        c = int(250 - 22 * y / H)
        d.line([(0, y), (W, y)], fill=(c, c, c + 2))
    # producto centrado en zona 860x700
    cut.thumbnail((860, 690))
    x = (W - cut.width) // 2
    y = 130 + (690 - cut.height) // 2
    # sombra suave
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ell = ImageDraw.Draw(sh)
    ell.ellipse([x + cut.width * 0.1, y + cut.height - 25, x + cut.width * 0.9, y + cut.height + 30], fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    bg.paste(sh, (0, 0), sh)
    bg.paste(cut, (x, y), cut)
    d = ImageDraw.Draw(bg)
    # franja superior
    d.rectangle([0, 0, W, 105], fill=(17, 24, 39))
    d.text((W // 2, 52), TITLE, font=fb(46), fill=(255, 255, 255), anchor="mm")
    # etiqueta de precio
    d.rounded_rectangle([W - 330, 830, W - 40, 935], radius=22, fill=(220, 38, 38))
    d.text((W - 185, 882), PRICE, font=fb(64), fill=(255, 255, 255), anchor="mm")
    d.text((60, 860), SUB, font=fb(36), fill=(17, 24, 39), anchor="lm")
    # franja inferior
    d.rectangle([0, H - 95, W, H], fill=(17, 24, 39))
    d.text((W // 2, H - 48), CONTACT, font=fr(36), fill=(255, 255, 255), anchor="mm")
    out = os.path.join(OUT, f"{i:02d}_" + os.path.splitext(name)[0] + "_PRO.jpg")
    bg.save(out, quality=93)
    print(out)
