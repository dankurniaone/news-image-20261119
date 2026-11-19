#!/usr/bin/env python3
"""Draw the 19 November 2026 front page to entry.png.

Pure Pillow, no network, no clock, no randomness: the same news.json
always renders the same bytes. Render at 2x, then LANCZOS-downscale to
680x1024 so the type stays smooth. Run from the repo root:

    python3 tools/render19.py
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = "/usr/share/fonts/truetype/dejavu"

# --- palette: light newsprint, one red accent, one dark neon band ---
PAPER = (250, 246, 236)
INK = (20, 20, 18)
SOFT = (104, 98, 88)
RED = (178, 34, 34)
NAVY = (30, 58, 95)
SEA = (198, 216, 228)
LAND = (233, 224, 198)
DUSK_TOP = (36, 16, 64)
DUSK_LOW = (255, 122, 47)
SUN = (255, 196, 66)
SILHOUETTE = (18, 8, 31)

SCALE = 2
W, H = 680 * SCALE, 1024 * SCALE
MARGIN = 36 * SCALE
CW = W - 2 * MARGIN


def load(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def serif_b(size):
    return load("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load("DejaVuSerif.ttf", size)


def sans(size):
    return load("DejaVuSans.ttf", size)


def sans_b(size):
    return load("DejaVuSans-Bold.ttf", size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, fill, max_w, leading):
    """Draw a wrapped paragraph; return the y just below it."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tracked(d, cx, y, text, fnt, fill, gap):
    """Draw text centred on cx with extra tracking between letters."""
    widths = [d.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=fnt, fill=fill)
        x += w + gap
    return y + fnt.size


def centred(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def star_points(cx, cy, outer, inner):
    pts = []
    for i in range(10):
        r = outer if i % 2 == 0 else inner
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_us(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            sx = x + cw * (c + 0.5) / 6
            sy = y + ch * (r + 0.5) / 5
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star_points(x + w * 0.18, y + h * 0.28, h * 0.22, h * 0.09),
              fill=(255, 222, 0))
    for sx, sy in [(0.38, 0.14), (0.46, 0.28), (0.44, 0.48), (0.34, 0.58)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.08, h * 0.033),
                  fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    third = h / 3
    d.rectangle([x, y, x + w, y + third], fill=(255, 255, 255))
    d.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 0, 50))
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=2)


def gulf_map(d, x, y, w, h):
    """Schematic Persian Gulf: a diagonal sea band, four marked places."""
    d.rectangle([x, y, x + w, y + h], fill=LAND)
    d.line([(x + 30, y + h - 30), (x + w - 30, y + 30)],
           fill=SEA, width=64)
    d.ellipse([x + 4, y + h - 56, x + 56, y + h - 4], fill=SEA)
    d.ellipse([x + w - 56, y + 4, x + w - 4, y + 56], fill=SEA)
    marks = [
        ("KUWAIT", 0.14, 0.30),
        ("BAHRAIN", 0.42, 0.44),
        ("QESHM", 0.72, 0.30),
        ("RIYADH", 0.30, 0.82),
    ]
    lab = sans_b(20)
    for name, fx, fy in marks:
        px, py = x + w * fx, y + h * fy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], outline=(255, 255, 255), width=2)
        d.text((px + 12, py - 11), name, font=lab, fill=INK)
    d.text((x + 8, y + 6), "PERSIAN GULF", font=sans_b(20), fill=NAVY)
    d.text((x + w - 190, y + h - 30), "STRAIT OF HORMUZ", font=sans_b(18), fill=NAVY)


def kerch_diagram(d, x, y, w, h):
    """Kerch Bridge: two shores, a deck with its road span down."""
    d.rectangle([x, y, x + w, y + h], fill=LAND)
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=SEA)
    d.rectangle([x, y, x + w * 0.30, y + h * 0.55], fill=(210, 198, 168))
    d.rectangle([x + w * 0.70, y, x + w, y + h * 0.55], fill=(210, 198, 168))
    d.text((x + 14, y + 10), "RUSSIA", font=sans_b(20), fill=INK)
    d.text((x + w - 110, y + 10), "CRIMEA", font=sans_b(20), fill=INK)
    deck_y = y + h * 0.30
    d.rectangle([x, deck_y - 5, x + w * 0.42, deck_y + 5], fill=INK)
    d.rectangle([x + w * 0.58, deck_y - 5, x + w, deck_y + 5], fill=INK)
    d.line([(x + w * 0.42, deck_y + 5), (x + w * 0.50, y + h * 0.62)],
           fill=INK, width=8)
    d.line([(x + w * 0.58, deck_y + 5), (x + w * 0.50, y + h * 0.62)],
           fill=INK, width=8)
    d.text((x + w * 0.36, y + h * 0.66), "ROAD SPAN DOWN", font=sans_b(19), fill=RED)
    d.text((x + 10, y + h - 30), "KERCH STRAIT", font=sans_b(18), fill=NAVY)


def vice_skyline(d, x, y, w, h):
    """Neon dusk over Vice City: gradient sky, sun, silhouettes, palms."""
    for row in range(h):
        t = row / h
        r = int(DUSK_TOP[0] + (DUSK_LOW[0] - DUSK_TOP[0]) * t)
        g = int(DUSK_TOP[1] + (DUSK_LOW[1] - DUSK_TOP[1]) * t)
        b = int(DUSK_TOP[2] + (DUSK_LOW[2] - DUSK_TOP[2]) * t)
        d.line([(x, y + row), (x + w, y + row)], fill=(r, g, b))
    sun_cx, sun_cy, sun_r = x + w * 0.72, y + h * 0.58, h * 0.38
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=SUN)
    horizon = y + h * 0.72
    heights = [0.30, 0.45, 0.22, 0.55, 0.38, 0.62, 0.28, 0.48, 0.34, 0.58, 0.26]
    bw = w / len(heights)
    for i, frac in enumerate(heights):
        bh = h * 0.42 * frac + h * 0.08
        d.rectangle([x + i * bw + 2, horizon - bh, x + (i + 1) * bw - 2, horizon],
                    fill=SILHOUETTE)
    d.rectangle([x, horizon, x + w, y + h], fill=(12, 6, 24))
    d.ellipse([sun_cx - 14, horizon + 6, sun_cx + 14, y + h - 8], fill=(255, 150, 60))

    def palm(px, py, s):
        d.line([(px, py), (px + 4, py - 70 * s)], fill=SILHOUETTE, width=5)
        top = (px + 4, py - 70 * s)
        for ang in (-70, -35, 0, 35, 70):
            a = math.radians(-90 + ang)
            ex = top[0] + 46 * s * math.cos(a)
            ey = top[1] + 46 * s * math.sin(a) * 0.45
            d.line([top, (ex, ey)], fill=SILHOUETTE, width=4)

    palm(x + w * 0.10, horizon + 4, 1.0)
    palm(x + w * 0.22, horizon + 4, 0.8)


def render():
    with open(os.path.join(ROOT, "news.json")) as f:
        n = json.load(f)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    cx = W // 2
    y = 40

    # masthead
    d.rectangle([MARGIN, y, W - MARGIN, y + 6], fill=RED)
    y += 22
    y = centred(d, cx, y, n["masthead"], serif_b(108), INK)
    y += 6
    y = tracked(d, cx, y, n["masthead_tag"], sans_b(30), INK, 14)
    y += 10
    y = centred(d, cx, y, n["date"].upper(), sans(28), SOFT)
    y += 12
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 14
    y = centred(d, cx, y, n["strapline"], serif(26), SOFT)

    # lead: Shenzhen trilateral
    y += 18
    d.text((MARGIN, y), n["lead"]["kicker"], font=sans_b(26), fill=RED)
    y += 40
    y = para(d, MARGIN, y, n["lead"]["headline"], serif_b(72), INK, CW, 84)
    y += 8
    y = para(d, MARGIN, y, n["lead"]["deck"], serif(31), INK, CW, 42)
    y += 14
    fy = y
    fw, fh, gap = 392, 170, 20
    flag_us(d, MARGIN, fy, fw, fh)
    flag_cn(d, MARGIN + fw + gap, fy, fw, fh)
    flag_ru(d, MARGIN + 2 * (fw + gap), fy, fw, fh)
    y = fy + fh + 12
    y = centred(d, cx, y, n["lead"]["visual_caption"], sans(21), SOFT)
    y += 12
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 14

    # two-column row: Gulf | Kerch
    col_w = (CW - 40) // 2
    col_x = [MARGIN, MARGIN + col_w + 40]
    row_top = y
    col_bottom = []
    for i, key in enumerate(("gulf", "kerch")):
        s = n[key]
        x = col_x[i]
        yy = row_top
        d.text((x, yy), s["kicker"], font=sans_b(24), fill=RED)
        yy += 38
        yy = para(d, x, yy, s["headline"], serif_b(38), INK, col_w, 46)
        yy += 8
        yy = para(d, x, yy, s["deck"], serif(27), INK, col_w, 36)
        yy += 14
        if key == "gulf":
            gulf_map(d, x, yy, col_w, 170)
        else:
            kerch_diagram(d, x, yy, col_w, 170)
        yy += 170 + 10
        yy = para(d, x, yy, s["map_caption"] if key == "gulf" else s["diagram_caption"],
                  sans(20), SOFT, col_w, 26)
        col_bottom.append(yy)
    row_bottom = max(col_bottom)
    d.line([(MARGIN + col_w + 20, row_top), (MARGIN + col_w + 20, row_bottom)],
           fill=(200, 192, 176), width=2)
    y = row_bottom + 16

    # GTA band
    d.rectangle([MARGIN, y, W - MARGIN, y + 330], fill=DUSK_TOP)
    vice_skyline(d, MARGIN, y + 170, CW, 170)
    by = y + 22
    d.text((MARGIN + 24, by), n["gta"]["kicker"], font=sans_b(24), fill=SUN)
    by += 38
    by = para(d, MARGIN + 24, by, n["gta"]["headline"], serif_b(54), (255, 255, 255),
              CW - 48, 64)
    by += 6
    para(d, MARGIN + 24, by, n["gta"]["deck"], serif(29), (235, 228, 215),
         CW - 48, 38)
    y += 330 + 16

    # Jeffries
    d.text((MARGIN, y), n["jeffries"]["kicker"], font=sans_b(24), fill=RED)
    y += 38
    y = para(d, MARGIN, y, n["jeffries"]["headline"], serif_b(38), INK, CW, 46)
    y += 8
    y = para(d, MARGIN, y, n["jeffries"]["deck"], serif(29), INK, CW, 38)
    y += 14

    # ticker (auto-fit: shrink until it fits the content width)
    d.rectangle([MARGIN, y, W - MARGIN, y + 56], fill=RED)
    tsize = 25
    while tsize > 14:
        tf = sans_b(tsize)
        tw = d.textlength(n["ticker"], font=tf)
        if tw <= CW - 40:
            break
        tsize -= 1
    d.text((cx - tw / 2, y + (56 - tsize) // 2 - 2), n["ticker"], font=tf, fill=(255, 255, 255))
    y += 56 + 14

    # footer
    y = para(d, MARGIN, y, n["footer"], sans(20), SOFT, CW, 26)
    y += 12
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    assert y <= H - 30, f"page overflow: y={y} of {H}"

    small = img.resize((680, 1024), Image.LANCZOS)
    small.save(os.path.join(ROOT, "entry.png"), optimize=True)
    print(f"entry.png: {os.path.getsize(os.path.join(ROOT, 'entry.png'))} bytes")


if __name__ == "__main__":
    render()
