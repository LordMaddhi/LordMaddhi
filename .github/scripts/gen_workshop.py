"""Generates assets/workshop.svg: animated pixel-art scene of maddhi's dev room.
Run: py .github/scripts/gen_workshop.py
Coordinates are in "pixels" (1 pixel = P real px).
"""
import os
import random

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "workshop.svg")

P = 6
GW, GH = 128, 66
random.seed(7)
el = []


def r(x, y, w, h, c, extra=""):
    el.append(f'<rect x="{x * P}" y="{y * P}" width="{w * P}" height="{h * P}" fill="{c}"{extra}/>')


def group(inner, attrs=""):
    el.append(f"<g{attrs}>")
    inner()
    el.append("</g>")


# ---------- 3x5 pixel font ----------
FONT = {
    "M": ["101", "111", "111", "101", "101"], "A": ["010", "101", "111", "101", "101"],
    "D": ["110", "101", "101", "101", "110"], "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"], ".": ["000", "000", "000", "000", "010"],
    "E": ["111", "100", "110", "100", "111"], "V": ["101", "101", "101", "101", "010"],
}


def text(s, x, y, c):
    for i, ch in enumerate(s):
        for dy, row in enumerate(FONT[ch]):
            for dx, b in enumerate(row):
                if b == "1":
                    r(x + i * 4 + dx, y + dy, 1, 1, c)


# ---------- wall & floor ----------
r(0, 0, GW, GH, "#241c3a")
for y in range(0, 52, 4):  # wallpaper stripes
    r(0, y, GW, 1, "#2a2142")
r(0, 52, GW, 1, "#3b2f5c")  # baseboard
r(0, 53, GW, GH - 53, "#3d2b22")
for y in range(55, GH, 3):
    r(0, y, GW, 1, "#33241c")
for x in range(6, GW, 17):
    r(x, 53, 1, GH - 53, "#33241c")

# ---------- window with night sky ----------
r(6, 6, 30, 26, "#5c4636")
r(7, 7, 28, 24, "#0d1433")
r(7, 22, 28, 9, "#141d45")
stars = [(9, 9), (14, 12), (20, 8), (11, 17), (24, 15), (31, 19), (17, 20), (33, 9)]
for i, (sx, sy) in enumerate(stars):
    el.append(f'<rect x="{sx * P}" y="{sy * P}" width="{P}" height="{P}" fill="#fff6c8">'
              f'<animate attributeName="opacity" values="1;.2;1" dur="{1.6 + i * .37:.2f}s" repeatCount="indefinite"/></rect>')
r(27, 9, 4, 4, "#f4e7b0"); r(26, 10, 1, 2, "#f4e7b0"); r(28, 10, 2, 2, "#d9c98c")  # moon
# Skyline
for bx, bh in [(7, 5), (10, 8), (14, 4), (17, 7), (21, 3), (24, 9), (28, 5), (31, 7)]:
    r(bx, 31 - bh, 3, bh, "#070b1f")
    for wy in range(31 - bh + 1, 30, 2):
        if random.random() < .45:
            r(bx + 1, wy, 1, 1, "#ffd76a")
r(20, 7, 1, 24, "#5c4636"); r(7, 18, 28, 1, "#5c4636")  # window cross
r(4, 32, 34, 2, "#6e5442")  # window sill

# ---------- neon sign ----------
el.append('<g><animate attributeName="opacity" values="1;1;1;.35;1;1;.6;1" dur="4s" repeatCount="indefinite"/>')
r(46, 3, 42, 9, "#1a1230")
text("MADDHI.DEV", 47, 5, "#ff4fd8")
el.append("</g>")

# ---------- pinboard ----------
r(46, 14, 42, 10, "#8a5a36"); r(47, 15, 40, 8, "#b07a4a")
for nx, ny, c, pin in [(49, 16, "#fff27a", "#e33"), (56, 17, "#7af0ff", "#33e"), (63, 16, "#ff9ad5", "#e33"),
                       (70, 17, "#a8ff8a", "#fc0"), (78, 16, "#ffffff", "#e33")]:
    r(nx, ny, 5, 5, c); r(nx + 2, ny, 1, 1, pin)
    r(nx + 1, ny + 2, 3, 1, "#00000033"); r(nx + 1, ny + 3, 2, 1, "#00000033")

# ---------- shelf with books ----------
BOOKS = ["#7f52ff", "#6db33f", "#2496ed", "#3178c6", "#c49a6c", "#e44857", "#f7df1e", "#ed2b88", "#e76f00", "#ffffff"]


def shelf(y):
    x = 94
    i = 0
    while x < 121:
        h = random.choice([6, 7, 8])
        w = random.choice([2, 2, 3])
        if x + w > 121:
            break
        c = BOOKS[(i + y) % len(BOOKS)]
        r(x, y - h, w, h, c)
        r(x, y - h + 1, w, 1, "#00000040")
        x += w
        i += 1
    r(92, y, 32, 2, "#6e5442")


shelf(14)
shelf(28)
r(92, 30, 1, 2, "#4a382c"); r(123, 30, 1, 2, "#4a382c")

# ---------- lamp with light cone ----------
el.append(f'<polygon points="{24 * P},{34 * P} {32 * P},{34 * P} {40 * P},{44 * P} {14 * P},{44 * P}" fill="#ffe9a0" opacity=".12">'
          '<animate attributeName="opacity" values=".12;.16;.12" dur="3s" repeatCount="indefinite"/></polygon>')
r(23, 31, 10, 3, "#e8c04a"); r(24, 30, 8, 1, "#c99e2e")
r(27, 34, 2, 10, "#444"); r(24, 43, 8, 1, "#333")

# ---------- desk ----------
r(2, 44, 124, 2, "#8b5e3c"); r(2, 46, 124, 1, "#6e4a30")
r(5, 47, 3, 13, "#5a3d27"); r(120, 47, 3, 13, "#5a3d27")
r(94, 47, 26, 9, "#6e4a30"); r(105, 50, 4, 1, "#c9a26b")  # drawer

# ---------- plant ----------
r(10, 40, 7, 4, "#c0623a"); r(10, 40, 7, 1, "#a04e2c")
el.append('<g><animateTransform attributeName="transform" type="rotate" values="0 81 240;-3 81 240;0 81 240;2 81 240;0 81 240" dur="5s" repeatCount="indefinite"/>')
for lx, ly in [(13, 33), (11, 35), (15, 35), (10, 37), (16, 37), (12, 38), (14, 38), (13, 36)]:
    r(lx, ly, 2, 2, "#3fa34d")
r(12, 36, 1, 1, "#62c96d"); r(15, 34, 1, 1, "#62c96d")
el.append("</g>")

# ---------- monitor with scrolling code ----------
MX, MY, MW, MH = 48, 25, 32, 17
r(MX, MY, MW, MH, "#1b1b24"); r(MX + 1, MY + 1, MW - 2, MH - 2, "#0b1020")
r(62, 42, 4, 2, "#2a2a35"); r(59, 43, 10, 1, "#2a2a35")
el.append(f'<clipPath id="scr"><rect x="{(MX + 1) * P}" y="{(MY + 1) * P}" width="{(MW - 2) * P}" height="{(MH - 2) * P}"/></clipPath>')
SYN = ["#c678dd", "#61afef", "#98c379", "#e5c07b", "#abb2bf", "#56b6c2", "#e06c75"]
lines = []
indent = 0
for i in range(14):
    if i % 5 == 0:
        indent = 0
    segs, x = [], 2 + indent
    for _ in range(random.randint(1, 3)):
        w = random.randint(2, 6)
        if x + w > MW - 4:
            break
        segs.append((x, w, random.choice(SYN)))
        x += w + 1
    lines.append(segs)
    indent = min(indent + 2, 6) if random.random() < .5 else max(indent - 2, 0)
el.append('<g clip-path="url(#scr)"><g>')
block = len(lines) * 2
el.append(f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {-block * P}" dur="9s" repeatCount="indefinite"/>')
for rep in range(2):
    for i, segs in enumerate(lines):
        y = MY + 2 + rep * block + i * 2
        for sx, w, c in segs:
            r(MX + sx, y, w, 1, c)
el.append("</g>")
el.append(f'<rect x="{(MX + 3) * P}" y="{(MY + MH - 3) * P}" width="{P}" height="{P}" fill="#fff">'
          '<animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></rect>')
el.append("</g>")
r(MX + 1, MY + 1, MW - 2, 1, "#ffffff10")  # screen glare

# ---------- keyboard & mouse ----------
r(54, 42, 20, 2, "#3a3a48")
for kx in range(55, 73, 2):
    r(kx, 42, 1, 1, "#5a5a6e")
r(77, 42, 2, 2, "#3a3a48")

# ---------- headphones on a stand, with music notes ----------
HB, HB_D, CUP, CUP_D, CUP_L = "#d8d8e4", "#9a9ab0", "#ff4fd8", "#a02a88", "#ff9ae8"
r(85, 43, 9, 1, "#2a2a35"); r(86, 42, 7, 1, "#3a3a48")                 # stand base
r(89, 32, 1, 10, "#3a3a48")                                             # stand pole
r(85, 29, 9, 1, HB); r(84, 30, 1, 1, HB); r(94, 30, 1, 1, HB)           # headband
r(83, 31, 1, 3, HB); r(95, 31, 1, 3, HB); r(86, 30, 7, 1, HB_D)         # band sides + padding
for cx in (81, 95):                                                     # ear cups
    r(cx, 34, 4, 6, CUP_D); r(cx + 1, 34, 2, 6, CUP); r(cx + 1, 35, 1, 2, CUP_L)
NOTE = [(1, 0), (2, 0), (3, 1), (1, 1), (1, 2), (1, 3), (0, 3), (0, 4), (1, 4)]  # pixel eighth note
for i, (nx, col) in enumerate([(84, "#79c0ff"), (90, "#ff4fd8"), (78, "#a8ff8a")]):
    el.append(f'<g opacity="0">'
              f'<animateTransform attributeName="transform" type="translate" values="0 0;{(i - 1) * 2 * P} {-6 * P}" '
              f'dur="3s" begin="{i:.0f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;1;1;0" dur="3s" begin="{i:.0f}s" repeatCount="indefinite"/>')
    for dx, dy in NOTE:
        r(nx + dx, 24 + dy, 1, 1, col)
    el.append("</g>")

# ---------- camera ----------
SIL, SIL_D, BODY, GRIP = "#d0d0dc", "#8a8a9e", "#1e1e26", "#3a3a48"
CX = 107                                                                # left edge
r(CX + 3, 36, 4, 2, SIL); r(CX + 3, 36, 4, 1, "#f0f0f8")                # viewfinder hump
r(CX + 9, 37, 2, 1, "#e33")                                             # red shutter button
r(CX, 38, 13, 1, SIL)                                                   # top plate
r(CX, 39, 13, 5, BODY); r(CX, 40, 13, 3, GRIP)                          # body + leather grip
r(CX + 4, 39, 5, 5, SIL_D)                                              # lens ring
r(CX + 5, 40, 3, 3, BODY); r(CX + 5, 40, 2, 2, "#2a5a9a")               # lens + glass
el.append(f'<rect x="{(CX + 5) * P}" y="{40 * P}" width="{P}" height="{P}" fill="#fff">'
          f'<animate attributeName="opacity" values=".9;.4;.9" dur="4s" repeatCount="indefinite"/></rect>')  # soft glint
# flash: only the camera's flash window lights up with a small star around it (the room stays dark)
FX, FY = CX + 10, 39
r(FX, FY, 2, 1, "#e8e8f0")                                              # flash window
FL = 'values="0;0;1;0;0" keyTimes="0;.9;.92;.97;1" dur="7s" repeatCount="indefinite"'
el.append(f'<g opacity="0"><animate attributeName="opacity" {FL}/>')
r(FX, FY, 2, 1, "#ffffff")
for dx, dy in [(0, -2), (1, -2), (0, -3), (1, -3), (-2, 0), (-1, 0), (2, 0), (3, 0),
               (-1, -1), (2, -1), (-1, 1), (2, 1), (0, 1), (1, 1)]:
    r(FX + dx, FY + dy, 1, 1, "#fffbe0")
el.append("</g>")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{GW * P}" height="{GH * P}" viewBox="0 0 {GW * P} {GH * P}" shape-rendering="crispEdges">\n'
       + "\n".join(el) + "\n</svg>\n")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(svg)
print("wrote:", OUT)
