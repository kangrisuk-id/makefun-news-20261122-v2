#!/usr/bin/env python3
"""Draw 'THE WORLD TODAY - Sunday 22 November 2026' as one 1024x1024 PNG.

Every story was first reported on Sunday 22 November 2026 (researched and
verified from Reuters/AP/CNN/WSJ/Al Jazeera/Sky and market data wires).
Deterministic: fixed geometry, no randomness, no timestamps.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_O = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

PAPER = (247, 242, 231)
INK = (26, 26, 40)
MUTE = (96, 92, 84)
RULE = (26, 26, 40)
WHITE = (255, 255, 255)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(text, font):
    return d.textlength(text, font=font)


def ctext(cx, y, text, font, fill=INK):
    d.text((cx - tw(text, font) / 2, y), text, font=font, fill=fill)


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def panel(x, y, w, h, accent):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=(198, 190, 172), width=1)
    d.rectangle([x, y, x + w, y + 5], fill=accent)


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 86], fill=INK)
ctext(512, 10, "THE WORLD TODAY", F(SERIF_B, 44), (250, 246, 236))
ctext(512, 62, "SUNDAY 22 NOVEMBER 2026  ·  28 STORIES  ·  7 REGIONS  ·  ONE PAGE",
      F(SANS_B, 13), (216, 178, 92))
d.line([14, 90, 1010, 90], fill=RULE, width=2)

# ---------------------------------------------------------------- stat strip
STATS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed by air defences"),
    ("7", "sea drones sank a Russian warship"),
    ("24", "dead, Nigeria funeral boat capsize"),
    ("-8.6%", "S&P 500's worst week since Apr 2025"),
    ("~200", "nations at COP31, no deal reached"),
]
sx = 14
for i, (big, small) in enumerate(STATS):
    wcell = 166 if i < 5 else 162
    ctext(sx + wcell / 2, 96, big, F(SANS_B, 27), (166, 32, 32) if i in (0, 4) else INK)
    for j, ln in enumerate(wrap(small, F(SANS, 10), wcell - 8)):
        ctext(sx + wcell / 2, 126 + j * 12, ln, F(SANS, 10), MUTE)
    if i:
        d.line([sx - 3, 98, sx - 3, 146], fill=(198, 190, 172), width=1)
    sx += wcell
d.line([14, 150, 1010, 150], fill=RULE, width=2)

# ---------------------------------------------------------------- lead scenes
LEAD_Y, LEAD_H, LEAD_W = 158, 262, 326


def lead_head(x, accent, kicker, headline, sub):
    y = LEAD_Y + 148
    d.text((x + 10, y), kicker, font=F(SANS_B, 11), fill=accent)
    yy = y + 16
    for ln in wrap(headline, F(SANS_B, 16), LEAD_W - 20):
        d.text((x + 10, yy), ln, font=F(SANS_B, 16), fill=INK)
        yy += 20
    for ln in wrap(sub, F(SANS, 11), LEAD_W - 20):
        d.text((x + 10, yy), ln, font=F(SANS, 11), fill=MUTE)
        yy += 14


def scene_cop31(x):
    y0 = LEAD_Y + 6
    for i in range(142):
        c = (250 - i // 2, 196 - i // 3, 120 - i // 4)
        d.line([x + 1, y0 + i, x + LEAD_W - 1, y0 + i], fill=c)
    d.ellipse([x + 238, y0 + 14, x + 292, y0 + 68], fill=(232, 84, 40))
    # Antalya skyline silhouette
    sil = (74, 52, 44)
    for bx, bw, bh in [(6, 34, 52), (46, 26, 78), (78, 40, 60), (124, 24, 92),
                       (154, 36, 66), (196, 28, 84), (268, 44, 58)]:
        d.rectangle([x + bx, y0 + 142 - bh, x + bx + bw, y0 + 142], fill=sil)
    d.polygon([(x + 136, y0 + 44), (x + 142, y0 + 26), (x + 148, y0 + 44)], fill=sil)
    # thermometer of a warming world, front right
    tx = x + 292
    d.rounded_rectangle([tx, y0 + 18, tx + 16, y0 + 118], 8, fill=WHITE, outline=INK, width=2)
    d.rectangle([tx + 4, y0 + 46, tx + 12, y0 + 114], fill=(200, 40, 32))
    d.ellipse([tx - 5, y0 + 104, tx + 21, y0 + 130], fill=(200, 40, 32), outline=INK, width=2)
    d.text((tx - 14, y0 + 2), "+1.5C", font=F(SANS_B, 12), fill=(166, 32, 32))
    # cracked dry earth
    d.rectangle([x + 1, y0 + 132, x + LEAD_W - 1, y0 + 142], fill=(146, 104, 62))
    for cx0 in range(10, LEAD_W - 12, 34):
        d.line([x + cx0, y0 + 134, x + cx0 + 10, y0 + 140, x + cx0 + 20, y0 + 135],
               fill=(96, 66, 36), width=1)


def scene_benghazi(x):
    y0 = LEAD_Y + 6
    for i in range(142):
        c = (16 + i // 6, 34 + i // 4, 66 + i // 3)
        d.line([x + 1, y0 + i, x + LEAD_W - 1, y0 + i], fill=c)
    for sx_ in (30, 90, 210, 280):
        d.text((x + sx_, y0 + 10 + (sx_ % 3) * 9), ".", font=F(SANS_B, 14), fill=(220, 224, 235))
    # harbour wall
    d.rectangle([x + 1, y0 + 116, x + LEAD_W - 1, y0 + 142], fill=(38, 40, 48))
    # corvette Merkury silhouette, listing after the hit
    hull = (196, 200, 208)
    d.polygon([(x + 88, y0 + 112), (x + 250, y0 + 112), (x + 236, y0 + 126), (x + 104, y0 + 126)], fill=hull)
    d.rectangle([x + 132, y0 + 96, x + 196, y0 + 112], fill=hull)
    d.rectangle([x + 156, y0 + 78, x + 168, y0 + 96], fill=hull)
    d.line([x + 204, y0 + 80, x + 204, y0 + 112], fill=hull, width=4)
    d.polygon([(x + 196, y0 + 84), (x + 216, y0 + 90), (x + 196, y0 + 94)], fill=(200, 40, 32))
    # explosion + smoke at the stern
    ex, ey = x + 96, y0 + 96
    for r, col in [(26, (240, 120, 40)), (17, (250, 180, 60)), (9, (255, 230, 150))]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    for k in range(5):
        d.ellipse([ex - 8 + k * 7, ey - 58 + k * 4, ex + 16 + k * 7, ey - 30 + k * 4],
                  fill=(70, 70, 78))
    # two sea drones closing in
    for dx, dy in [(18, 122), (52, 130)]:
        d.polygon([(x + dx, y0 + dy), (x + dx + 26, y0 + dy - 4), (x + dx + 34, y0 + dy + 3),
                   (x + dx + 6, y0 + dy + 5)], fill=(230, 232, 238))
        d.line([x + dx - 8, y0 + dy + 3, x + dx, y0 + dy + 2], fill=(180, 200, 220), width=2)
    d.text((x + 236, y0 + 8), "BENGHAZI", font=F(SANS_B, 11), fill=(220, 224, 235))


def scene_hormuz(x):
    y0 = LEAD_Y + 6
    for i in range(142):
        c = (250 - i // 3, 214 - i // 2, 150 - i // 2)
        d.line([x + 1, y0 + i, x + LEAD_W - 1, y0 + i], fill=c)
    d.ellipse([x + 20, y0 + 12, x + 62, y0 + 54], fill=(240, 150, 50))
    # strait: two headlands, water between
    d.polygon([(x + 1, y0 + 88), (x + 108, y0 + 88), (x + 76, y0 + 142), (x + 1, y0 + 142)],
              fill=(150, 116, 74))
    d.polygon([(x + LEAD_W - 1, y0 + 84), (x + 224, y0 + 84), (x + 256, y0 + 142),
               (x + LEAD_W - 1, y0 + 142)], fill=(150, 116, 74))
    d.rectangle([x + 76, y0 + 108, x + 256, y0 + 142], fill=(52, 96, 138))
    # tanker mid-strait
    d.polygon([(x + 116, y0 + 104), (x + 224, y0 + 104), (x + 214, y0 + 116), (x + 126, y0 + 116)],
              fill=(40, 44, 54))
    d.rectangle([x + 140, y0 + 92, x + 196, y0 + 104], fill=(168, 44, 36))
    d.rectangle([x + 202, y0 + 88, x + 214, y0 + 104], fill=(40, 44, 54))
    # fire on deck + smoke
    fx = x + 168
    d.polygon([(fx - 9, y0 + 92), (fx, y0 + 66), (fx + 9, y0 + 92)], fill=(238, 110, 30))
    d.polygon([(fx - 4, y0 + 92), (fx, y0 + 78), (fx + 4, y0 + 92)], fill=(252, 200, 80))
    for k in range(4):
        d.ellipse([fx - 6 + k * 9, y0 + 40 - k * 3, fx + 14 + k * 9, y0 + 60 - k * 3],
                  fill=(84, 78, 72))
    # naval mines
    for mx, my in [(96, 124), (238, 128)]:
        d.ellipse([x + mx - 7, y0 + my - 7, x + mx + 7, y0 + my + 7], fill=(30, 32, 40))
        for a in range(0, 360, 60):
            import math
            d.line([x + mx, y0 + my, x + mx + 10 * math.cos(math.radians(a)),
                    y0 + my + 10 * math.sin(math.radians(a))], fill=(30, 32, 40), width=2)
    d.text((x + 10, y0 + 6), "STRAIT OF HORMUZ", font=F(SANS_B, 11), fill=(120, 60, 30))


LEADS = [
    (14, (178, 92, 30), scene_cop31, "CLIMATE · ANTALYA",
     "COP31 TALKS COLLAPSE WITHOUT A DEAL",
     "After two days of overtime, nearly 200 nations leave Türkiye split over fossil fuels and climate finance. Guterres: 'deeply disappointed.'"),
    (349, (32, 64, 110), scene_benghazi, "WAR AT SEA · LIBYA",
     "SEA DRONES SINK RUSSIAN WARSHIP IN LIBYA",
     "Seven Ukrainian naval drones sink the corvette Merkury at Benghazi, 2,400 km from the front, and hit the arms carrier Angara."),
    (684, (168, 44, 36), scene_hormuz, "MIDDLE EAST · HORMUZ",
     "TANKERS STRUCK AS HORMUZ CRISIS DEEPENS",
     "Two tankers hit near the strait; Bahrain says an Iranian attack set a Sitra industrial plant ablaze and injured two."),
]
for x, acc, scene, kick, head, sub in LEADS:
    panel(x, LEAD_Y, LEAD_W, LEAD_H, acc)
    scene(x)
    lead_head(x, acc, kick, head, sub)


# ---------------------------------------------------------------- small panels
def icon(kind, cx, cy, col):
    if kind == "drone":
        d.line([cx - 12, cy - 8, cx + 12, cy + 8], fill=col, width=3)
        d.line([cx - 12, cy + 8, cx + 12, cy - 8], fill=col, width=3)
        for dx, dy in [(-12, -8), (12, -8), (-12, 8), (12, 8)]:
            d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5], outline=col, width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=col)
    elif kind == "gavel":
        d.line([cx - 10, cy + 12, cx + 12, cy + 12], fill=col, width=3)
        d.polygon([(cx - 4, cy - 12), (cx + 8, cy - 12), (cx + 12, cy - 6), (cx, cy - 6)], fill=col)
        d.line([cx + 2, cy - 6, cx - 6, cy + 10], fill=col, width=4)
    elif kind == "flame":
        d.polygon([(cx, cy - 14), (cx + 9, cy + 2), (cx + 6, cy + 12), (cx - 6, cy + 12),
                   (cx - 9, cy + 2)], fill=col)
        d.polygon([(cx, cy - 2), (cx + 4, cy + 6), (cx + 2, cy + 12), (cx - 3, cy + 12),
                   (cx - 4, cy + 5)], fill=(250, 190, 80))
    elif kind == "boat":
        d.polygon([(cx - 14, cy + 2), (cx + 14, cy + 2), (cx + 9, cy + 11), (cx - 9, cy + 11)], fill=col)
        d.line([cx, cy + 2, cx, cy - 12], fill=col, width=3)
        d.polygon([(cx, cy - 12), (cx + 9, cy), (cx, cy)], fill=col)
        d.arc([cx - 15, cy + 8, cx + 15, cy + 20], 0, 180, fill=(52, 96, 138), width=2)
    elif kind == "flag":
        d.line([cx - 10, cy - 13, cx - 10, cy + 13], fill=col, width=3)
        d.polygon([(cx - 10, cy - 13), (cx + 12, cy - 9), (cx - 10, cy - 4)], fill=(32, 64, 140))
        d.polygon([(cx - 10, cy - 4), (cx + 12, cy), (cx - 10, cy + 5)], fill=(198, 48, 49))
    elif kind == "anchor":
        d.ellipse([cx - 4, cy - 13, cx + 4, cy - 5], outline=col, width=3)
        d.line([cx, cy - 5, cx, cy + 11], fill=col, width=3)
        d.line([cx - 8, cy - 1, cx + 8, cy - 1], fill=col, width=3)
        d.arc([cx - 12, cy - 2, cx + 12, cy + 16], 0, 180, fill=col, width=3)
    elif kind == "ball":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=col, width=2)
        d.polygon([(cx, cy - 6), (cx + 6, cy - 2), (cx + 4, cy + 5), (cx - 4, cy + 5),
                   (cx - 6, cy - 2)], fill=col)
    elif kind == "car":
        d.polygon([(cx - 15, cy + 4), (cx - 8, cy - 6), (cx + 6, cy - 6), (cx + 14, cy + 4)], fill=col)
        d.rectangle([cx - 16, cy + 4, cx + 16, cy + 9], fill=col)
        for wx in (-9, 9):
            d.ellipse([cx + wx - 4, cy + 6, cx + wx + 4, cy + 14], fill=INK)
    elif kind == "chart":
        d.line([cx - 13, cy + 12, cx + 13, cy + 12], fill=col, width=2)
        d.line([cx - 12, cy - 10, cx - 4, cy - 2, cx + 4, cy + 4, cx + 12, cy + 10],
               fill=(200, 40, 32), width=3)


def small(x, y, w, accent, kind, kicker, headline, sub):
    panel(x, y, w, 104, accent)
    icon(kind, x + 26, y + 34, accent)
    d.text((x + 48, y + 12), kicker, font=F(SANS_B, 9), fill=accent)
    yy = y + 25
    for ln in wrap(headline, F(SANS_B, 12), w - 56):
        d.text((x + 48, yy), ln, font=F(SANS_B, 12), fill=INK)
        yy += 15
    sy = max(yy + 2, y + 64)
    for ln in wrap(sub, F(SANS, 10), w - 18):
        d.text((x + 10, sy), ln, font=F(SANS, 10), fill=MUTE)
        sy += 12


ROW_A = [
    ((178, 60, 40), "drone", "UKRAINE", "186-DRONE BARRAGE BATTERS KYIV REGION",
     "Apartment block hit in Dymer, at least 3 dead; missiles kill 2 in Kryvyi Rih; Odesa loses power, water, heat."),
    ((120, 92, 30), "gavel", "THE HAGUE", "FRANCE PUSHES UN ACTION ON ROHINGYA VERDICT",
     "Myanmar rejects the ICJ genocide ruling; refugees demand justice."),
    ((150, 60, 90), "flame", "WEST BANK · GAZA", "SETTLER ATTACKS CONDEMNED AS 'TERRORISM'",
     "Israeli forces kill 2 in Gaza; Eisenkot blasts settler arson attacks."),
    ((30, 110, 90), "boat", "NIGERIA", "FUNERAL BOAT CAPSIZES: AT LEAST 24 DEAD",
     "Mourners' boat overturns in Bayelsa; 24 rescued, the driver flees and the vessel's manager is held."),
]
for i, (acc, kind, kick, head, sub) in enumerate(ROW_A):
    small(14 + i * 249, 428, 241, acc, kind, kick, head, sub)

# ---------------------------------------------------------------- markets chart
MX, MY, MW, MH = 14, 540, 500, 212
panel(MX, MY, MW, MH, (150, 30, 30))
d.text((MX + 12, MY + 12), "MARKETS · THE WEEK EVERYTHING FELL", font=F(SANS_B, 14), fill=INK)
d.text((MX + 12, MY + 32), "Indexed closes, Fri 13 Nov = 100  →  Fri 20 Nov", font=F(SANS, 11), fill=MUTE)
GX, GY, GW, GH = MX + 46, MY + 58, 322, 104
for gv in (100, 95, 90, 85):
    gy = GY + (100 - gv) / 20 * GH
    d.line([GX, gy, GX + GW, gy], fill=(214, 208, 194), width=1)
    d.text((MX + 8, gy - 6), str(gv), font=F(SANS, 10), fill=MUTE)
SERIES = [
    ("S&P 500 · 91.4", 91.39, (32, 64, 140)),
    ("GOLD · 91.0", 91.04, (178, 132, 30)),
    ("NASDAQ · 90.0", 89.98, (110, 60, 150)),
    ("BITCOIN · 86.2", 86.15, (200, 40, 32)),
]
prev_ly = None
for name, val, col in SERIES:
    y2 = GY + (100 - val) / 20 * GH
    d.line([GX, GY, GX + GW, y2], fill=col, width=3)
    d.ellipse([GX - 4, GY - 4, GX + 4, GY + 4], fill=col)
    d.ellipse([GX + GW - 4, y2 - 4, GX + GW + 4, y2 + 4], fill=col)
    ly = y2 - 6
    if prev_ly is not None and ly < prev_ly + 13:
        ly = prev_ly + 13
    d.line([GX + GW + 3, y2, GX + GW + 8, ly + 5], fill=col, width=1)
    d.text((GX + GW + 10, ly), name, font=F(SANS_B, 10), fill=col)
    prev_ly = ly
d.text((GX, GY + GH + 6), "13 NOV", font=F(SANS, 10), fill=MUTE)
d.text((GX + GW - 38, GY + GH + 6), "20 NOV", font=F(SANS, 10), fill=MUTE)
d.text((MX + 12, MY + MH - 20),
       "Closes: S&P 6,910 · Nasdaq 22,618 · gold $3,533 · BTC $58.8k (Sat low $55,130).",
       font=F(SANS, 11), fill=INK)

# ---------------------------------------------------------------- world map
PX, PY, PW, PH = 522, 540, 488, 212
panel(PX, PY, PW, PH, (30, 90, 110))
d.text((PX + 12, PY + 10), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
LAND = (196, 178, 138)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 49), (-117, 33), (-105, 20), (-97, 16), (-87, 13),
     (-83, 9), (-90, 14), (-97, 26), (-90, 21), (-87, 21), (-90, 29), (-81, 26),
     (-76, 35), (-70, 42), (-60, 46), (-66, 52), (-80, 58), (-95, 60), (-125, 60),
     (-152, 60), (-168, 66)],
    [(-79, 9), (-77, -3), (-80, -5), (-75, -15), (-70, -18), (-70, -23), (-71, -30),
     (-72, -38), (-74, -46), (-72, -52), (-68, -55), (-66, -48), (-65, -41), (-58, -32),
     (-52, -25), (-48, -16), (-41, -8), (-35, -6), (-38, -14), (-40, -21), (-48, -26),
     (-57, -33), (-62, -39), (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54),
     (-73, -44), (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-77, -12), (-80, -6),
     (-80, 1), (-77, 7), (-79, 9)],
    [(-9, 37), (-2, 37), (0, 39), (3, 42), (7, 44), (11, 44), (14, 42), (18, 40),
     (16, 38), (12, 38), (15, 36), (19, 36), (22, 37), (24, 36), (26, 38), (28, 41),
     (30, 41), (28, 46), (25, 49), (24, 52), (20, 52), (16, 50), (12, 49), (9, 47),
     (5, 48), (3, 48), (5, 50), (8, 54), (8, 57), (13, 55), (18, 56), (21, 55),
     (24, 58), (26, 60), (23, 65), (19, 69), (25, 71), (31, 70), (35, 66), (32, 62),
     (30, 60), (28, 57), (29, 54), (26, 54), (27, 51), (30, 50), (28, 47), (29, 43),
     (26, 41), (23, 40), (20, 42), (16, 44), (13, 46), (9, 46), (5, 44), (0, 46),
     (-2, 44), (-9, 43), (-9, 37)],
    [(-17, 15), (-10, 5), (-8, -2), (8, -12), (12, -18), (14, -22), (16, -28), (19, -33),
     (26, -34), (31, -29), (35, -24), (36, -20), (40, -12), (41, -4), (48, 2), (51, 10),
     (48, 12), (44, 12), (42, 15), (40, 20), (38, 22), (35, 24), (34, 27), (33, 29),
     (30, 31), (22, 33), (15, 32), (11, 34), (10, 37), (4, 37), (-2, 35), (-6, 35),
     (-10, 31), (-15, 27), (-17, 21), (-17, 15)],
    [(35, 36), (44, 38), (48, 38), (50, 36), (52, 34), (56, 30), (60, 28), (66, 25),
     (72, 22), (76, 20), (80, 15), (84, 12), (88, 8), (92, 8), (96, 10), (100, 8),
     (104, 4), (108, 2), (112, 4), (118, 8), (122, 12), (126, 18), (130, 24), (134, 30),
     (138, 34), (140, 38), (142, 44), (140, 50), (136, 54), (130, 58), (124, 60),
     (116, 62), (108, 64), (100, 66), (92, 68), (84, 70), (76, 70), (68, 68), (60, 66),
     (54, 62), (50, 58), (48, 52), (46, 48), (44, 44), (40, 40), (36, 38), (35, 36)],
    [(113, -22), (114, -28), (116, -34), (118, -35), (124, -33), (129, -32), (133, -32),
     (137, -35), (140, -38), (144, -38), (146, -39), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (141, -13), (136, -12), (132, -11), (126, -11),
     (122, -14), (118, -17), (115, -20), (113, -22)],
]
MAPX, MAPY, MAPW, MAPH = PX + 10, PY + 34, PW - 20, 150


def mxy(lon, lat):
    return (MAPX + (lon + 170) / 360 * MAPW, MAPY + (75 - lat) / 135 * MAPH)


for poly in CONTINENTS:
    d.polygon([mxy(lon, lat) for lon, lat in poly], fill=LAND)
MARKERS = [
    ("ANTALYA", 30.7, 36.9, -18, 10), ("BENGHAZI", 20.1, 32.1, -14, 9),
    ("KYIV", 30.5, 50.4, -40, -15), ("HORMUZ", 56.3, 26.6, 7, 7),
    ("BAYELSA", 6.1, 4.9, 7, -5), ("THE HAGUE", 4.3, 52.1, -52, -7),
    ("LAS VEGAS", -115.1, 36.2, 7, -5), ("LAHORE", 74.3, 31.5, 7, -13),
]
for name, lon, lat, ox, oy in MARKERS:
    cx, cy = mxy(lon, lat)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(178, 32, 32), outline=WHITE, width=1)
    d.text((cx + ox, cy + oy), name, font=F(SANS_B, 9), fill=INK)
d.text((PX + 12, PY + PH - 18), "Eight datelines, one Sunday.", font=F(SANS_O, 11), fill=MUTE)

# ---------------------------------------------------------------- small row B
ROW_B = [
    ((30, 90, 40), "flag", "BRITAIN · EU", "UK AND EU STRIKE TRADE AND TRAVEL DEALS",
     "London and Brussels pledge to rebuild ties a decade after Brexit, on trade, travel and defence."),
    ((90, 60, 120), "anchor", "BALTIC SEA", "DRONE-HIT RUSSIAN SHIP TOWED TO SAFETY",
     "Finland and Estonia help tow the stricken cargo vessel Sparta II out of Finnish waters overnight."),
    ((150, 30, 40), "ball", "FOOTBALL", "LIVERPOOL ROUT 10-MAN UNITED 4-0",
     "Pochettino's first match as United boss ends in an Anfield rout after Yoro's 8th-minute red card."),
    ((200, 120, 20), "car", "FORMULA 1", "VERSTAPPEN HOLDS OFF NORRIS IN LAS VEGAS",
     "A wild night race: the Ferrari pair collide, Russell fades late, and McLaren take both podium steps."),
]
for i, (acc, kind, kick, head, sub) in enumerate(ROW_B):
    small(14 + i * 249, 760, 241, acc, kind, kick, head, sub)

# ---------------------------------------------------------------- also today + footer
AY = 870
d.line([14, AY, 1010, AY], fill=RULE, width=2)
d.text((14, AY + 4), "ALSO TODAY", font=F(SANS_B, 13), fill=INK)
ALSO = [
    "France rout Argentina 45-17 to reach the Nations Championship final",
    "Alcaraz beats Zverev 6-2 7-6 for his first ATP Finals title in Turin",
    "China's bourses cut the margin ratio to 80%, effective 30 November",
    "Bessent presses Nvidia for answers over AI chips sold to China",
    "Taiwan warns Canada's Carney that deeper China ties carry risks",
    "Poland says Russia twice plotted to kill a Ukrainian-American rapper",
    "Lahore is the world's most polluted city again, air index over 500",
    "Nepal's PM Balendra Shah opens a two-day India visit in New Delhi",
    "Spain's Sanchez raises the stakes a week before the snap election",
    "UN warns 30 million in southern Africa are at risk from El Nino",
    "FBI investigates a reported intrusion into its national crime database",
    "Trump vows to work with Democrats on a 10% credit-card interest cap",
    "US Army to detonate lead chemicals in Iowa despite a court order",
    "ICE detentions at Seattle airport spark interfaith protests in Gilroy",
    "Jeweller Paolo Bulgari dies at 89; S. Africa's Mlambo-Ngcuka at 71",
    "Thai court upholds a royal-defamation conviction, cuts jail term to 3 yrs",
]
for i, item in enumerate(ALSO):
    col, row = i // 8, i % 8
    x = 14 + col * 502
    d.text((x, AY + 25 + row * 12), "· " + item, font=F(SANS, 10), fill=INK)
d.line([14, 990, 1010, 990], fill=RULE, width=2)
ctext(512, 996,
      "DATE CHECK: every story above was first reported on Sunday 22 November 2026 (Reuters · AP · CNN · WSJ · Al Jazeera · Sky).",
      F(SANS, 10), MUTE)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
