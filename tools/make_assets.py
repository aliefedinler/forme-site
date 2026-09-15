"""
FORME — placeholder asset generator.

The FORME collection is fictional, so this script renders *technical flats*
(line drawings of garment silhouettes) on a subtle woven ground instead of
photography. They are deliberately illustrative: no image on this site claims
to depict a real, manufactured product. Replace them with licensed product
photography before publishing — see README.md.

Run:  python3 tools/make_assets.py
"""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont

INK = (25, 25, 25)
BURGUNDY = (99, 45, 57)
SS = 3  # supersample factor for line art


# ---------------------------------------------------------------- ground -----
def octave(h, w, scale, rng):
    sh, sw = max(2, int(h / scale)), max(2, int(w / scale))
    small = rng.random((sh, sw)).astype(np.float32)
    img = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    img = img.filter(ImageFilter.GaussianBlur(scale * 0.3))
    return np.asarray(img).astype(np.float32) / 255.0


def ground(size, rgb, weave_kind="plain", seed=0):
    """A quiet textile ground: fine weave, a whisper of cloth grain, soft light."""
    w, h = size
    rng = np.random.default_rng(seed)
    field = octave(h, w, 260, rng) * 1.0 + octave(h, w, 90, rng) * 0.45
    field /= 1.45
    field -= field.mean()
    field /= (np.abs(field).max() or 1.0)

    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    if weave_kind == "jersey":
        tex = 0.009 * np.sin(yy * 2.0) + 0.007 * np.sin(xx * 2.7)
    elif weave_kind == "fleece":
        tex = 0.007 * np.sin(yy * 1.2 + np.sin(xx * 0.06) * 2.2)
    elif weave_kind == "twill":
        tex = 0.011 * np.sin((xx + yy) * 1.2)
    else:
        tex = 0.012 * np.sin(xx * 1.05) * np.sin(yy * 1.05)

    d = np.sqrt(((xx / w) - 0.36) ** 2 + ((yy / h) - 0.24) ** 2)
    key = (1.0 - np.clip(d / 1.25, 0, 1)) * 0.10 - 0.035

    shade = 1.0 + field * 0.055 + tex + key
    shade += (rng.random((h, w)).astype(np.float32) - 0.5) * 0.010
    base = np.array(rgb, np.float32).reshape(1, 1, 3) / 255.0
    return Image.fromarray((np.clip(base * shade[..., None], 0, 1) * 255).astype(np.uint8), "RGB")


# ------------------------------------------------------------- line art ------
def mirror(pts, cx=500):
    return [(2 * cx - x, y) for (x, y) in reversed(pts)]


def poly(d, pts, width, close=True, color=(25, 25, 25, 220)):
    p = list(pts) + ([pts[0]] if close else [])
    d.line([(x * SS, y * SS) for x, y in p], fill=color, width=width * SS, joint="curve")


def curve(d, p0, p1, p2, width, color=(25, 25, 25, 220), n=40):
    """Quadratic bezier as a polyline."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x * SS, y * SS))
    d.line(pts, fill=color, width=width * SS, joint="curve")


def flat_tee(d, lw):
    body = [(392, 272), (298, 292), (168, 452), (232, 534), (352, 432), (352, 470),
            (330, 980)]
    right = mirror(body)
    poly(d, body + right, lw, close=False)
    d.line([(330 * SS, 980 * SS), (670 * SS, 980 * SS)], fill=(25, 25, 25, 220), width=lw * SS)
    curve(d, (392, 272), (500, 342), (608, 272), lw)          # neckline
    curve(d, (378, 268), (500, 316), (622, 268), max(1, lw - 1))  # collar rib
    d.line([(232 * SS, 534 * SS), (352 * SS, 432 * SS)], fill=(25, 25, 25, 220), width=lw * SS)
    # sleeve hems
    curve(d, (196, 490), (232, 500), (272, 478), max(1, lw - 1))
    curve(d, (728, 478), (768, 500), (804, 490), max(1, lw - 1))


def flat_hoodie(d, lw):
    body = [(276, 330), (130, 566), (214, 652), (330, 492), (330, 512), (312, 990)]
    poly(d, body + mirror(body), lw, close=False)
    d.line([(312 * SS, 990 * SS), (688 * SS, 990 * SS)], fill=(25, 25, 25, 220), width=lw * SS)
    # hood
    curve(d, (276, 330), (500, 138), (724, 330), lw)
    curve(d, (330, 336), (500, 250), (670, 336), lw)
    # drawcords
    d.line([(452 * SS, 322 * SS), (444 * SS, 470 * SS)], fill=(25, 25, 25, 220), width=lw * SS)
    d.line([(548 * SS, 322 * SS), (556 * SS, 470 * SS)], fill=(25, 25, 25, 220), width=lw * SS)
    # kangaroo pocket
    poly(d, [(352, 706), (648, 706), (662, 872), (338, 872)], max(1, lw - 1))
    # ribbed hem + cuffs
    d.line([(316 * SS, 916 * SS), (684 * SS, 916 * SS)], fill=(25, 25, 25, 190), width=max(1, lw - 1) * SS)
    curve(d, (150, 602), (186, 624), (232, 606), max(1, lw - 1))
    curve(d, (768, 606), (814, 624), (850, 602), max(1, lw - 1))


def flat_trouser(d, lw):
    outline = [(332, 252), (668, 252), (678, 560), (702, 1010), (538, 1010),
               (500, 604), (462, 1010), (298, 1010), (322, 560)]
    poly(d, outline, lw)
    d.line([(330 * SS, 336 * SS), (670 * SS, 336 * SS)], fill=(25, 25, 25, 220), width=lw * SS)  # waistband
    d.line([(414 * SS, 350 * SS), (392 * SS, 996 * SS)], fill=(25, 25, 25, 170), width=max(1, lw - 1) * SS)
    d.line([(586 * SS, 350 * SS), (608 * SS, 996 * SS)], fill=(25, 25, 25, 170), width=max(1, lw - 1) * SS)
    curve(d, (352, 350), (398, 420), (420, 356), max(1, lw - 1))   # pockets
    curve(d, (580, 356), (602, 420), (648, 350), max(1, lw - 1))
    d.line([(486 * SS, 260 * SS), (486 * SS, 332 * SS)], fill=(25, 25, 25, 190), width=max(1, lw - 1) * SS)


def flat_overshirt(d, lw):
    body = [(396, 268), (296, 290), (206, 432), (192, 772), (300, 786), (332, 462),
            (332, 476), (320, 962)]
    poly(d, body + mirror(body), lw, close=False)
    d.line([(320 * SS, 962 * SS), (680 * SS, 962 * SS)], fill=(25, 25, 25, 220), width=lw * SS)
    # collar
    curve(d, (396, 268), (500, 336), (604, 268), lw)
    poly(d, [(396, 268), (442, 350), (500, 322)], max(1, lw - 1), close=False)
    poly(d, [(604, 268), (558, 350), (500, 322)], max(1, lw - 1), close=False)
    # placket + buttons
    d.line([(470 * SS, 330 * SS), (470 * SS, 962 * SS)], fill=(25, 25, 25, 200), width=max(1, lw - 1) * SS)
    d.line([(530 * SS, 330 * SS), (530 * SS, 962 * SS)], fill=(25, 25, 25, 200), width=max(1, lw - 1) * SS)
    for y in (420, 540, 660, 780, 900):
        r = 9 * SS
        d.ellipse([500 * SS - r, y * SS - r, 500 * SS + r, y * SS + r],
                  outline=(25, 25, 25, 210), width=max(1, lw - 1) * SS)
    # chest pockets
    poly(d, [(356, 452), (444, 452), (444, 556), (356, 556)], max(1, lw - 1))
    poly(d, [(556, 452), (644, 452), (644, 556), (556, 556)], max(1, lw - 1))
    # cuffs
    d.line([(198 * SS, 716 * SS), (306 * SS, 730 * SS)], fill=(25, 25, 25, 200), width=max(1, lw - 1) * SS)
    d.line([(694 * SS, 730 * SS), (802 * SS, 716 * SS)], fill=(25, 25, 25, 200), width=max(1, lw - 1) * SS)


FLATS = {"tee": flat_tee, "hoodie": flat_hoodie, "trouser": flat_trouser,
         "overshirt": flat_overshirt}


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


POPPINS = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"


def tracked(d, xy, text, f, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x


def plate(path, size, rgb, flat, weave_kind, label, colorway, seed,
          scale=1.0, quality=80, mark=True):
    w, h = size
    im = ground(size, rgb, weave_kind, seed).convert("RGBA")
    layer = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    art = Image.new("RGBA", (1000 * SS, 1250 * SS), (0, 0, 0, 0))
    ad = ImageDraw.Draw(art)
    FLATS[flat](ad, 5)
    target_w = int(w * 0.66 * scale)
    art = art.resize((target_w * SS, int(target_w * 1.25) * SS), Image.LANCZOS)
    layer.alpha_composite(art, ((w * SS - art.width) // 2, int(h * 0.5 * SS) - art.height // 2))

    m = int(w * 0.055)
    d.rectangle([m * SS, m * SS, (w - m) * SS, (h - m) * SS],
                outline=(25, 25, 25, 46), width=1 * SS)
    layer = layer.resize((w, h), Image.LANCZOS)
    im.alpha_composite(layer)

    d = ImageDraw.Draw(im)
    small = font(POPPINS, max(11, int(w * 0.016)))
    tracked(d, (m + int(w * 0.03), m + int(w * 0.03)), label.upper(), small, (25, 25, 25, 190),
            max(1.0, w * 0.0022))
    if colorway:
        tracked(d, (m + int(w * 0.03), h - m - int(w * 0.055)), colorway.upper(), small,
                (25, 25, 25, 150), max(1.0, w * 0.0022))
    if mark:
        d.rectangle([w - m - int(w * 0.03) - int(w * 0.05), h - m - int(w * 0.05),
                     w - m - int(w * 0.03), h - m - int(w * 0.05) + max(2, int(w * 0.004))],
                    fill=BURGUNDY)
    im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"{path}  {w}x{h}")


P = "assets/"

plate(P + "hero-debut-collection.jpg", (1100, 1375), (219, 211, 197), "hoodie", "plain",
      "FORME — debut collection", "technical flat · placeholder", 11, scale=1.02, quality=82)

plate(P + "product-essential-tee.jpg", (800, 1000), (230, 223, 210), "tee", "jersey",
      "Essential Tee", "Bone", 21)
plate(P + "product-everyday-hoodie.jpg", (800, 1000), (163, 160, 154), "hoodie", "fleece",
      "Everyday Hoodie", "Heather Grey", 22)
plate(P + "product-relaxed-trouser.jpg", (800, 1000), (204, 194, 178), "trouser", "twill",
      "Relaxed Trouser", "Stone", 23)
plate(P + "product-studio-overshirt.jpg", (800, 1000), (124, 124, 96), "overshirt", "plain",
      "Studio Overshirt", "Olive", 24)


def og_cover(path):
    w, h = 1200, 630
    im = ground((w, h), (245, 242, 236), "plain", 7)
    d = ImageDraw.Draw(im)
    title = font(LORA, 126)
    sub = font(POPPINS, 28)
    tracked(d, (92, 196), "FORME", title, INK, 24)
    d.line([(92, 386), (1108, 386)], fill=(25, 25, 25), width=1)
    d.text((92, 418), "Less noise. More you.", font=sub, fill=INK)
    d.text((92, 462), "The debut collection — unisex everyday essentials.",
           font=sub, fill=(112, 106, 98))
    d.rectangle([92, 534, 268, 538], fill=BURGUNDY)
    d.text((92, 560), "Student project · fictional brand", font=font(POPPINS, 22),
           fill=(134, 128, 120))
    im.save(path, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"{path}  {w}x{h}")


og_cover(P + "og-cover.jpg")
