"""Pixel-art building blocks for the README (same style as workshop.svg):
  assets/bookshelf.svg      bookshelf, one book per technology
  assets/sign-*.svg         hanging wooden signs used as section headings
  assets/btn-*.svg          pixel buttons for links
Run: py .github/scripts/gen_pixel_ui.py
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A = os.path.join(ROOT, "assets")
os.makedirs(A, exist_ok=True)

# ---------- 3x5 pixel font ----------
G = {
    "A": "010101111101101", "B": "110101110101110", "C": "011100100100011", "D": "110101101101110",
    "E": "111100110100111", "F": "111100110100100", "G": "011100101101011", "H": "101101111101101",
    "I": "111010010010111", "J": "001001001101010", "K": "101101110101101", "L": "100100100100111",
    "M": "101111111101101", "N": "110101101101101", "O": "010101101101010", "P": "110101110100100",
    "Q": "010101101110011", "R": "110101110101101", "S": "011100010001110", "T": "111010010010010",
    "U": "101101101101111", "V": "101101101101010", "W": "101101111111101", "X": "101101010101101",
    "Y": "101101010010010", "Z": "111001010100111", "0": "111101101101111", "1": "010110010010111",
    "2": "110001010100111", "3": "110001010001110", "4": "101101111001001", "5": "111100110001110",
    "6": "011100111101111", "7": "111001010010010", "8": "111101111101111", "9": "111101111001110",
    ".": "000000000000010", "-": "000000111000000", "!": "010010010000010", " ": "000000000000000",
    ":": "000010000010000", "/": "001001010100100", "~": "000011110000000", ">": "100010001010100",
    "(": "010100100100010", ")": "010001001001010", "%": "101001010100101", "+": "000010111010000",
}


class Px:
    def __init__(self, p):
        self.p, self.el = p, []

    def r(self, x, y, w, h, c, extra=""):
        p = self.p
        self.el.append(f'<rect x="{x * p}" y="{y * p}" width="{w * p}" height="{h * p}" fill="{c}"{extra}/>')

    def text(self, s, x, y, c, shadow=None):
        for i, ch in enumerate(s.upper()):
            g = G.get(ch, G[" "])
            for k, b in enumerate(g):
                if b == "1":
                    if shadow:
                        self.r(x + i * 4 + k % 3 + 1, y + k // 3 + 1, 1, 1, shadow)
            for k, b in enumerate(g):
                if b == "1":
                    self.r(x + i * 4 + k % 3, y + k // 3, 1, 1, c)

    def vtext(self, s, x, y, c):  # book spine: letters stacked vertically
        for i, ch in enumerate(s.upper()):
            g = G.get(ch, G[" "])
            for k, b in enumerate(g):
                if b == "1":
                    self.r(x + k % 3, y + i * 6 + k // 3, 1, 1, c)

    def raw(self, s):
        self.el.append(s)

    def save(self, name, gw, gh):
        p = self.p
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{gw * p}" height="{gh * p}" '
               f'viewBox="0 0 {gw * p} {gh * p}" shape-rendering="crispEdges">\n' + "\n".join(self.el) + "\n</svg>\n")
        with open(os.path.join(A, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(svg)
        print("wrote:", name)


WOOD, WOOD_D, WOOD_L = "#8b5e3c", "#5a3d27", "#a8774f"
WALL, WALL_S = "#241c3a", "#2a2142"

# ---------- bookshelf ----------
BOOKS = [  # (name, book color, text color)
    ("KOTLIN", "#7f52ff", "#fff"), ("SPRING", "#6db33f", "#fff"), ("AURELIA", "#ed2b88", "#fff"),
    ("TS", "#3178c6", "#fff"), ("JS", "#f7df1e", "#222"), ("HTML", "#e34f26", "#fff"), ("CSS", "#1572b6", "#fff"),
    ("MARIADB", "#c49a6c", "#2b1a0e"), ("LIQUIBASE", "#2962ff", "#fff"), ("DOCKER", "#2496ed", "#fff"),
    ("GIT", "#f05032", "#fff"), ("INTELLIJ", "#fe315d", "#fff"),
    ("JAVA", "#e76f00", "#fff"), ("PYTHON", "#3776ab", "#ffd43b"), ("FLUTTER", "#02569b", "#fff"),
    ("DART", "#0175c2", "#fff"), ("LATEX", "#008080", "#fff"), ("FIGMA", "#a259ff", "#fff"),
    ("PHOTOSHOP", "#001e36", "#31a8ff"), ("RASPI", "#c51a4a", "#fff"),
]
P = 4
BW = 7          # book width
px = Px(P)


def books(x, y_board, wiggle):
    for i, (name, col, fg) in enumerate(BOOKS):
        h = len(name) * 6 + 7
        y = y_board - h
        if i in wiggle:  # now and then a book gets pulled halfway out
            px.raw(f'<g><animateTransform attributeName="transform" type="translate" '
                   f'values="0 0;0 0;0 {-4 * P};0 {-4 * P};0 0" keyTimes="0;.6;.7;.85;1" dur="6s" '
                   f'begin="{wiggle.index(i) * 3}s" repeatCount="indefinite"/>')
        px.r(x, y, BW, h, col)
        px.r(x, y, 1, h, "#ffffff30")
        px.r(x + BW - 1, y, 1, h, "#00000040")
        px.r(x, y + 1, BW, 1, "#00000030"); px.r(x, y + h - 3, BW, 1, "#00000030")
        px.vtext(name, x + 2, y + 3, fg)
        if i in wiggle:
            px.raw("</g>")
        x += BW + 1
    return x


def duck(x, yb):  # rubber duck for rubber-duck debugging
    Y = "#ffd43b"
    px.raw(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {-P};0 0" dur="1.2s" repeatCount="indefinite"/>')
    px.r(x, yb - 5, 8, 4, Y); px.r(x + 1, yb - 1, 6, 1, Y)
    px.r(x + 4, yb - 9, 4, 4, Y); px.r(x + 8, yb - 7, 2, 1, "#ff8a00"); px.r(x + 6, yb - 8, 1, 1, "#222")
    px.r(x + 1, yb - 4, 3, 1, "#e6b800")
    px.raw("</g>")
    return x + 10


def trophy(x, yb):
    Gd = "#f1c232"
    px.r(x + 1, yb - 10, 7, 5, Gd); px.r(x, yb - 10, 1, 3, Gd); px.r(x + 8, yb - 10, 1, 3, Gd)
    px.r(x + 3, yb - 5, 3, 3, Gd); px.r(x + 1, yb - 2, 7, 2, "#8a6d1a")
    px.r(x + 2, yb - 9, 1, 3, "#fff6b0")
    px.raw(f'<rect x="{(x + 7) * P}" y="{(yb - 12) * P}" width="{P}" height="{P}" fill="#fff">'
           f'<animate attributeName="opacity" values="0;1;0;0" dur="2s" repeatCount="indefinite"/></rect>')
    return x + 9


H = max(len(n) for n, _, _ in BOOKS) * 6 + 7
X0, T = 4, 3                     # cabinet outer edge, wall thickness
IN_X = X0 + T + 2
IN_W = len(BOOKS) * 8 + 2 + 10 + 2 + 9 + 2
YB = 4 + T + 3 + H               # inner floor
CW = IN_W + 2 * (T + 2)
GW = CW + 2 * X0
GH = YB + 3 + 5 + 3
px.r(0, 0, GW, GH, WALL)
for yy in range(0, GH, 4):
    px.r(0, yy, GW, 1, WALL_S)
# cabinet: back panel, sides, top, bottom, plinth
px.r(X0, 4, CW, YB - 4, "#3a2618")
for yy in range(4 + T, YB, 5):
    px.r(X0 + T, yy, CW - 2 * T, 1, "#33210f")
px.r(X0 - 1, 4 - 1, CW + 2, T, WOOD); px.r(X0 - 1, 3, CW + 2, 1, WOOD_L)
px.r(X0, 4, T, YB - 4 + 3, WOOD); px.r(X0 + CW - T, 4, T, YB - 4 + 3, WOOD)
px.r(X0, 4, 1, YB - 1, WOOD_L); px.r(X0 + CW - 1, 4, 1, YB - 1, WOOD_D)
px.r(X0, YB, CW, 3, WOOD); px.r(X0, YB, CW, 1, WOOD_L)
px.r(X0 + 1, YB + 3, CW - 2, 5, WOOD_D); px.r(X0 + 3, YB + 4, CW - 6, 3, "#4a3220")
x = books(IN_X, YB, [0, 13])
x = duck(x + 2, YB)
trophy(x + 2, YB)
px.save("bookshelf.svg", GW, GH)


# ---------- hanging signs ----------
def sign(name, label, accent):
    p = Px(5)
    w = len(label) * 4 + 9
    gw, gh = w + 8, 20
    cx = gw * 5 / 2
    p.raw(f'<g><animateTransform attributeName="transform" type="rotate" '
          f'values="-1.2 {cx} 0;1.2 {cx} 0;-1.2 {cx} 0" dur="4s" repeatCount="indefinite"/>')
    for kx in (8, gw - 9):  # chains
        for ky in range(0, 6, 2):
            p.r(kx, ky, 1, 1, "#9a9ab0"); p.r(kx, ky + 1, 1, 1, "#6a6a80")
    p.r(4, 6, gw - 8, 12, WOOD_D); p.r(5, 7, gw - 10, 10, WOOD); p.r(5, 7, gw - 10, 1, WOOD_L)
    for gx in range(7, gw - 6, 9):
        p.r(gx, 12, 3, 1, "#7a5033")
    p.r(7, 8, 1, 1, "#d0d0e0"); p.r(gw - 8, 8, 1, 1, "#d0d0e0")
    p.text(label, 9, 10, accent, shadow="#2b1a0e")
    p.raw("</g>")
    p.save(f"sign-{name}.svg", gw, gh)


sign("skills", "~ SKILLS ~", "#ffe39a")
sign("waka", "~ WAKA STATS (SINCE 2024) ~", "#ffe39a")
sign("contact", "~ KNOCK KNOCK ~", "#ffe39a")


# ---------- pixel buttons ----------
def button(name, label, col, dark):
    p = Px(4)
    w = len(label) * 4 + 13
    gw, gh = w + 2, 14
    p.r(1, 2, w, 11, "#00000060")  # shadow
    p.r(0, 0, w, 11, "#111"); p.r(1, 1, w - 2, 9, col)
    p.r(1, 1, w - 2, 1, "#ffffff70"); p.r(1, 9, w - 2, 1, dark)
    p.text(label, 4, 3, "#fff", shadow=dark)
    ax = len(label) * 4 + 5
    p.raw(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;4 0;0 0" dur="1s" repeatCount="indefinite"/>')
    p.text(">", ax, 3, "#fff")
    p.raw("</g>")
    p.save(f"btn-{name}.svg", gw, gh)


button("web", "MADDHI.DEV", "#ff4fd8", "#8a1f74")
