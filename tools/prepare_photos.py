"""
FORME — prepare supplied photography for the web.

Takes the team's source images, fits them to the layout's 4:5 frames, and writes
compressed progressive JPEGs into /assets. Also builds the 1200x630 Open Graph
card from the hero shot.

Run:  python3 tools/prepare_photos.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "/root/.claude/uploads/aaeffc57-e054-517d-a735-377637371281/"
OUT = "assets/"

JOBS = [
    ("bcc87c28-image.png", "hero-debut-collection.jpg", (1100, 1375), 82),
    ("e70822de-image.png", "product-essential-tee.jpg", (800, 1000), 80),
    ("8f38f1c5-image.png", "product-everyday-hoodie.jpg", (800, 1000), 80),
    ("c978b32b-image.png", "product-relaxed-trouser.jpg", (800, 1000), 80),
    ("3b6e42d8-image.png", "product-studio-overshirt.jpg", (800, 1000), 80),
]

POPPINS = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
INK = (25, 25, 25)
BURGUNDY = (99, 45, 57)
IVORY = (245, 242, 236)


def cover(im, size):
    """Resize to fill `size` exactly, cropping the overflow from the center."""
    tw, th = size
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


for src, dst, size, q in JOBS:
    im = Image.open(SRC + src).convert("RGB")
    im = cover(im, size)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=32, threshold=3))
    im.save(OUT + dst, "JPEG", quality=q, optimize=True, progressive=True)
    print(f"{OUT + dst}  {size[0]}x{size[1]}")


def tracked(d, xy, text, f, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x


def og_cover(path):
    """Left: ivory type panel. Right: the hero photograph."""
    W, H = 1200, 630
    panel_w = 660
    im = Image.new("RGB", (W, H), IVORY)

    photo = cover(Image.open(SRC + "bcc87c28-image.png").convert("RGB"), (W - panel_w, H))
    im.paste(photo, (panel_w, 0))

    d = ImageDraw.Draw(im)
    title = ImageFont.truetype(LORA, 104)
    sub = ImageFont.truetype(POPPINS, 26)
    small = ImageFont.truetype(POPPINS, 20)

    tracked(d, (84, 168), "FORME", title, INK, 22)
    d.line([(84, 330), (panel_w - 84, 330)], fill=INK, width=1)
    d.text((84, 360), "Less noise. More you.", font=sub, fill=INK)
    d.text((84, 402), "Unisex everyday essentials.", font=sub, fill=(112, 106, 98))
    d.rectangle([84, 470, 244, 474], fill=BURGUNDY)
    d.text((84, 498), "Student project · fictional brand", font=small, fill=(134, 128, 120))

    im.save(path, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"{path}  {W}x{H}")


og_cover(OUT + "og-cover.jpg")
