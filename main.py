import os
import struct
import zlib

W = 1024
H = 1024

CREAM = (250, 244, 224)
PAPER = (255, 251, 238)
INK = (18, 18, 18)
RED = (176, 32, 32)
RED_DARK = (140, 20, 20)
GREY = (90, 90, 90)
RULE = (200, 190, 170)
SEA = (178, 208, 228)
LAND = (84, 140, 84)
GREEN = (52, 110, 72)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '+': ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        for i in range(w * h):
            self.px[i * 3] = bg[0]
            self.px[i * 3 + 1] = bg[1]
            self.px[i * 3 + 2] = bg[2]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = c[0]
            self.px[i + 1] = c[1]
            self.px[i + 2] = c[2]

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def text(self, x, y, s, color, scale):
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == '1':
                        self.rect(x + col * scale, y + r * scale, scale, scale, color)
            x += 6 * scale

    def text_w(self, s, scale):
        if not s:
            return 0
        return len(s) * 6 * scale - scale

    def text_center(self, cx, y, s, color, scale):
        self.text(cx - self.text_w(s, scale) // 2, y, s, color, scale)

    def wrap(self, s, max_chars):
        words = s.split(' ')
        lines = []
        cur = ''
        for wd in words:
            if not cur:
                cur = wd
            elif len(cur) + 1 + len(wd) <= max_chars:
                cur = cur + ' ' + wd
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


def draw_globe(cv, cx, cy, r):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            dx = xx - cx
            dy = yy - cy
            if dx * dx + dy * dy <= r * r:
                cv.set(xx, yy, SEA)
    blobs = [(cx - 42, cy - 38, 52, 34), (cx + 48, cy - 30, 46, 30),
             (cx - 30, cy + 42, 58, 30), (cx + 52, cy + 44, 40, 26)]
    for (bx, by, rx, ry) in blobs:
        for yy in range(by - ry, by + ry + 1):
            for xx in range(bx - rx, bx + rx + 1):
                dx = (xx - bx) / float(rx)
                dy = (yy - by) / float(ry)
                ox = xx - cx
                oy = yy - cy
                if dx * dx + dy * dy <= 1.0 and ox * ox + oy * oy <= r * r:
                    cv.set(xx, yy, LAND)
    for a in range(360):
        import math
        ang = a * math.pi / 180.0
        x = int(cx + r * math.cos(ang))
        y = int(cy + r * math.sin(ang))
        cv.set(x, y, INK)
        cv.set(x + 1, y, INK)
        cv.set(x, y + 1, INK)
    cv.line(cx + 8, cy - r + 6, cx - 14, cy - 10, RED_DARK, 4)
    cv.line(cx - 14, cy - 10, cx + 10, cy + 22, RED_DARK, 4)
    cv.line(cx + 10, cy + 22, cx - 6, cy + r - 8, RED_DARK, 4)


def chip(cv, x, y, label, color):
    w = len(label) * 12 + 12
    cv.rect(x, y, w, 17, color)
    cv.text(x + 6, y + 3, label, WHITE, 2)
    return w


def draw_card(cv, x, y, w, h, label, title, body, chip_label, chip_color):
    cv.rect(x, y, w, h, PAPER)
    for xx in range(x, x + w):
        cv.set(xx, y, RULE)
        cv.set(xx, y + h - 1, RULE)
    for yy in range(y, y + h):
        cv.set(x, yy, RULE)
        cv.set(x + w - 1, yy, RULE)
    cv.text(x + 12, y + 10, label, RED, 2)
    ty = y + 30
    for ln in cv.wrap(title, 16):
        cv.text(x + 12, ty, ln, INK, 3)
        ty += 22
    by = ty + 6
    for ln in cv.wrap(body, 25):
        cv.text(x + 12, by, ln, INK, 2)
        by += 14
    chip(cv, x + 12, y + h - 27, chip_label, chip_color)


def build():
    cv = Canvas(W, H, CREAM)
    cv.rect(10, 10, W - 20, H - 20, PAPER)
    for t in range(3):
        cv.hline(10, 10 + t, W - 20, INK, 1)
        cv.hline(10, H - 11 - t, W - 20, INK, 1)
    for t in range(3):
        cv.rect(10 + t, 10, 1, H - 20, INK)
        cv.rect(W - 11 - t, 10, 1, H - 20, INK)

    cv.text_center(512, 26, "THE WORLD TODAY", INK, 6)
    cv.rect(24, 82, 976, 44, RED)
    cv.text_center(512, 90, "MONDAY 23 NOVEMBER 2026", WHITE, 4)
    cv.text_center(512, 134, "ONE DAY, ONE PAGE", INK, 3)
    cv.hline(24, 162, 976, INK, 2)

    # Hero left
    cv.text(24, 178, "CLIMATE - ANTALYA - MON 23", RED, 2)
    hy = 202
    for ln in ["COP31 ENDS", "WITH NO DEAL"]:
        cv.text(24, hy, ln, RED_DARK if ln == "WITH NO DEAL" else INK, 6)
        hy += 44
    hy += 6
    for ln in cv.wrap("THE EU AND 130 NATIONS REJECTED THE FINAL DRAFT. IT DID NOT NAME FOSSIL FUELS.", 33):
        cv.text(24, hy, ln, INK, 3)
        hy += 23
    hy += 4
    for ln in cv.wrap('"WE DID ALL THAT WE COULD." - MURAT KURUM', 33):
        cv.text(24, hy, ln, GREY, 3)
        hy += 23

    # Globe right
    draw_globe(cv, 820, 296, 108)
    cv.rect(700, 330, 240, 40, RED)
    cv.text_center(820, 338, "NO DEAL", WHITE, 4)
    cv.text_center(820, 412, "LONGEST SUMMIT EVER", GREY, 2)

    # Numbers box
    cv.hline(24, 452, 976, INK, 2)
    ny = 464
    for ln in ["2 WEEKS OF TALKS - 0 DEALS", "7 SEA DRONES, 1 WARSHIP",
               "34 MISSING IN CIKANDE"]:
        cv.text_center(512, ny, ln, INK, 3)
        ny += 24
    cv.hline(24, 540, 976, INK, 2)

    # Cards: 2 rows x 3 cols
    cw = 317
    ch = 152
    gap = 12
    x0 = 24
    y0 = 556
    cards = [
        ("LIBYA - BENGHAZI  MON 23", "UKRAINE HITS RUSSIAN WARSHIP",
         "7 SEA DRONES STRUCK THE MERKURY OFF BENGHAZI. KYIV CLAIMS IT SANK.",
         "CLAIMED", RED),
        ("GULF - BAHRAIN  SAT 21", "IRAN HITS BAHRAIN, HORMUZ",
         "MISSILES AND DRONES HIT US BASES IN BAHRAIN. 2 TANKERS HIT IN HORMUZ.",
         "CLAIMED", RED),
        ("CIKANDE, INDONESIA  MON 23", "SEARCH AT BURNT SWEET FACTORY",
         "24 BODY BAGS FOUND. 34 STILL MISSING. CAUSE UNDER INVESTIGATION.",
         "CONFIRMED", GREEN),
        ("UKRAINE - DYMER  MON 23", "STRIKE NEAR KYIV, 14 MISSING",
         "A RUSSIAN DRONE HIT FLATS IN DYMER. 14 PEOPLE MISSING.",
         "REPORTED", GREY),
        ("KOREA - SEOUL  MON 23", "MINISTER QUITS OVER EXAM CHAOS",
         "AI CHEATING SCANDAL SHOOK THE NATIONAL EXAM.",
         "REPORTED", GREY),
        ("MEXICO - GUASAVE  SAT 21", "EL CHAPO ISIDRO CAUGHT",
         "FBI MOST WANTED. $5 MILLION REWARD. 11 KILLED.",
         "CONFIRMED", GREEN),
    ]
    for i, (label, title, body, cl, cc) in enumerate(cards):
        cx = x0 + (i % 3) * (cw + gap)
        cy = y0 + (i // 3) * (ch + gap)
        draw_card(cv, cx, cy, cw, ch, label, title, body, cl, cc)

    # Also today
    ay = 888
    cv.hline(24, ay, 976, INK, 2)
    cv.text(24, ay + 10, "ALSO TODAY", RED, 2)
    cv.rect(24, ay + 34, 10, 10, RED)
    cv.text(42, ay + 32, "BELGIUM: ANTI-AUSTERITY STRIKE HALTS TRANSPORT. MON 23.", INK, 2)
    cv.rect(24, ay + 52, 10, 10, RED)
    cv.text(42, ay + 50, "CLEAN POWER PLEDGE: ABOUT 90 NATIONS BACK 35% BY 2035.", INK, 2)

    # Footer
    cv.hline(24, 962, 976, INK, 2)
    cv.text_center(512, 972, "SOURCES: REUTERS, AP, AFP, AL JAZEERA, BBC", GREY, 2)
    cv.text_center(512, 990, "HERO: MON 23 NOV. WEEKEND STORIES DATED IN TEXT.", GREY, 2)
    return cv


def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    c += struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
    return c


def write_png(cv, path):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw.extend(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not outdir:
        here = os.path.dirname(os.path.abspath(__file__))
        outdir = os.path.join(here, "out")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    cv = build()
    n = write_png(cv, path)
    print("wrote %s %d bytes" % (path, n))


if __name__ == "__main__":
    main()
