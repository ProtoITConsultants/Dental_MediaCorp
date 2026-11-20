# -*- coding: utf-8 -*-
# Put the Dental Connect screen on a monitor in perspective, on a soft grey background (3840 x 2560).
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 3840, 2560
SS = 2  # supersample the shapes for smooth edges

def coeffs(dst, src):
    """PIL PERSPECTIVE coefficients mapping output (dst) points back to input (src) points."""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()

def rounded(size, r, fill):
    im = Image.new('RGBA', (size[0] * SS, size[1] * SS), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] * SS - 1, size[1] * SS - 1], r * SS, fill=fill)
    return im.resize(size, Image.LANCZOS)

# ---- background: soft warm grey with a gentle light from the top left
bg = Image.new('RGB', (W, H), (226, 229, 227))
yy, xx = np.mgrid[0:H, 0:W]
d = np.sqrt(((xx - W * 0.35) / W) ** 2 + ((yy - H * 0.2) / H) ** 2)
light = np.clip(1 - d * 1.15, 0, 1)[..., None]
base = np.array([214, 218, 216], float)
top = np.array([238, 241, 239], float)
bg = Image.fromarray((base + (top - base) * light).astype('uint8'))

# ---- the flat monitor: thin silver rim, black bezel, the screen inside
screen = Image.open(os.path.join(HERE, 'screen.png')).convert('RGB')  # 3840 x 2400
sw, sh = screen.size
bez, rim = 64, 14
mw, mh = sw + 2 * (bez + rim), sh + 2 * (bez + rim)
mon = rounded((mw, mh), 96, (196, 199, 198, 255))                          # silver rim
mon.alpha_composite(rounded((mw - 2 * rim, mh - 2 * rim), 84, (16, 18, 18, 255)), (rim, rim))  # bezel
scr = screen.copy().convert('RGBA')
mask = rounded((sw, sh), 26, (255, 255, 255, 255)).split()[3]
scr.putalpha(mask)
mon.alpha_composite(scr, (rim + bez, rim + bez))

# ---- where it lands: the left edge nearer (taller), the right edge further away
TL, TR, BR, BL = (300, 250), (3560, 470), (3540, 2020), (280, 2290)
dst = [TL, TR, BR, BL]
src = [(0, 0), (mw, 0), (mw, mh), (0, mh)]

# stand: a slim silver neck under the monitor
stand = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(stand)
sd.polygon([(1640, 2060), (2080, 2080), (2060, 2560), (1660, 2560)], fill=(184, 188, 187, 255))
sd.polygon([(1640, 2060), (1700, 2063), (1716, 2560), (1660, 2560)], fill=(206, 209, 208, 255))

# shadow behind the monitor
sh_im = Image.new('L', (W, H), 0)
ImageDraw.Draw(sh_im).polygon([(TL[0] + 140, TL[1] + 220), (TR[0] + 100, TR[1] + 260), (BR[0] + 90, BR[1] + 170), (BL[0] + 140, BL[1] + 170)], fill=120)
sh_im = sh_im.filter(ImageFilter.GaussianBlur(120))
shadow = Image.new('RGBA', (W, H), (40, 46, 44, 0))
shadow.putalpha(sh_im)

warped = mon.transform((W, H), Image.PERSPECTIVE, coeffs(dst, src), Image.BICUBIC)

out = bg.convert('RGBA')
out.alpha_composite(shadow)
out.alpha_composite(stand)
out.alpha_composite(warped)
out = out.convert('RGB')
out.save(os.path.join(HERE, 'dashboard-hero.png'))
out.resize((1280, 853), Image.LANCZOS).save(os.path.join(HERE, 'dashboard-hero-view.jpg'), quality=90)
print('ok', out.size)
