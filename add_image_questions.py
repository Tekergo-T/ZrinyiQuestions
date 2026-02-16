#!/usr/bin/env python3
"""
Generate 50+ image-based questions with Pillow diagrams.
Inserts into existing DB, then re-exports db_data.js.

Usage:
  python3 manual_insert_questions.py   # base questions first
  python3 add_image_questions.py       # then this script
"""
import sqlite3, os, base64, io, math
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zrinyi_questions.db")
JS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_data.js")

# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════
def get_font(size=14):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_bold(size=14):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return get_font(size)

def img_to_uri(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def new_img(w=300, h=200):
    img = Image.new("RGB", (w, h), "white")
    return img, ImageDraw.Draw(img)

FONT = None
FONTB = None
FONTS = None

def init_fonts():
    global FONT, FONTB, FONTS
    FONT = get_font(14)
    FONTB = get_bold(16)
    FONTS = get_font(11)

# ═══════════════════════════════════════════════════════════════
#  DRAWING FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def draw_triangle_with_inner():
    """Triangle divided by lines from midpoints → count triangles."""
    img, d = new_img(240, 220)
    pts = [(120, 20), (20, 200), (220, 200)]
    d.polygon(pts, outline="black", width=2)
    # midpoints
    m01 = ((pts[0][0]+pts[1][0])//2, (pts[0][1]+pts[1][1])//2)
    m02 = ((pts[0][0]+pts[2][0])//2, (pts[0][1]+pts[2][1])//2)
    m12 = ((pts[1][0]+pts[2][0])//2, (pts[1][1]+pts[2][1])//2)
    d.line([m01, m02], fill="black", width=2)
    d.line([m01, m12], fill="black", width=2)
    d.line([m02, m12], fill="black", width=2)
    return img

def draw_count_squares_3x3():
    """3x3 grid → count all squares."""
    img, d = new_img(220, 240)
    m, s = 20, 60
    for i in range(4):
        d.line([m, m+i*s, m+3*s, m+i*s], fill="black", width=2)
        d.line([m+i*s, m, m+i*s, m+3*s], fill="black", width=2)
    d.text((30, 205), "Hány négyzet látható?", font=FONTS, fill="black")
    return img

def draw_count_rectangles():
    """2x3 grid → count rectangles."""
    img, d = new_img(280, 200)
    m, sw, sh = 20, 80, 70
    for i in range(3):
        d.line([m, m+i*sh, m+3*sw, m+i*sh], fill="black", width=2)
    for j in range(4):
        d.line([m+j*sw, m, m+j*sw, m+2*sh], fill="black", width=2)
    d.text((30, 170), "Hány téglalap látható?", font=FONTS, fill="black")
    return img

def draw_overlapping_triangles():
    """Two overlapping triangles."""
    img, d = new_img(260, 200)
    d.polygon([(50, 180), (130, 20), (210, 180)], outline="blue", width=2)
    d.polygon([(30, 60), (130, 180), (230, 60)], outline="red", width=2)
    return img

def draw_shape_sequence():
    """○ △ □ ○ △ ? pattern."""
    img, d = new_img(360, 80)
    shapes = ["circle", "triangle", "square", "circle", "triangle", "?"]
    for i, s in enumerate(shapes):
        cx, cy = 30 + i*55, 40
        r = 18
        if s == "circle":
            d.ellipse([cx-r, cy-r, cx+r, cy+r], outline="blue", width=2)
        elif s == "triangle":
            d.polygon([(cx, cy-r), (cx-r, cy+r), (cx+r, cy+r)], outline="red", width=2)
        elif s == "square":
            d.rectangle([cx-r, cy-r, cx+r, cy+r], outline="green", width=2)
        else:
            d.text((cx-8, cy-10), "?", font=get_bold(22), fill="black")
    return img

def draw_number_grid_pattern():
    """Magic-style grid with one missing number."""
    img, d = new_img(200, 200)
    m, s = 20, 50
    vals = [["2", "7", "6"], ["9", "5", "1"], ["4", "3", "?"]]
    for i in range(4):
        d.line([m, m+i*s, m+3*s, m+i*s], fill="black", width=2)
        d.line([m+i*s, m, m+i*s, m+3*s], fill="black", width=2)
    for r in range(3):
        for c in range(3):
            txt = vals[r][c]
            col = "red" if txt == "?" else "black"
            d.text((m+c*s+18, m+r*s+14), txt, font=FONTB, fill=col)
    d.text((20, 175), "Minden sor összege 15!", font=FONTS, fill="gray")
    return img

def draw_balance_scale(left_txt, right_txt, w=300, h=120):
    """Generic balance scale."""
    img, d = new_img(w, h)
    cx = w // 2
    # fulcrum
    d.polygon([(cx, 60), (cx-10, 80), (cx+10, 80)], fill="#888")
    # beam
    d.line([cx-100, 60, cx+100, 60], fill="black", width=3)
    # pans
    d.arc([cx-115, 55, cx-85, 75], 0, 180, fill="black", width=2)
    d.arc([cx+85, 55, cx+115, 75], 0, 180, fill="black", width=2)
    d.text((cx-100, 30), left_txt, font=FONT, fill="black", anchor="mm")
    d.text((cx+100, 30), right_txt, font=FONT, fill="black", anchor="mm")
    return img

def draw_two_scales(l1, r1, l2, r2):
    """Two balance scales stacked."""
    img, d = new_img(320, 200)
    f = FONT
    for idx, (lt, rt, label) in enumerate([(l1, r1, "1."), (l2, r2, "2.")]):
        y = 10 + idx * 95
        cx = 170
        d.polygon([(cx, y+55), (cx-10, y+70), (cx+10, y+70)], fill="#888")
        d.line([cx-90, y+55, cx+90, y+55], fill="black", width=3)
        d.arc([cx-105, y+48, cx-75, y+68], 0, 180, fill="black", width=2)
        d.arc([cx+75, y+48, cx+105, y+68], 0, 180, fill="black", width=2)
        d.text((cx-90, y+20), lt, font=f, fill="black")
        d.text((cx+78, y+20), rt, font=f, fill="black")
        d.text((10, y+40), label, font=f, fill="gray")
    return img

def draw_clock(hour, minute, w=160, h=170, label=""):
    """Analog clock face."""
    img, d = new_img(w, h)
    cx, cy, r = w//2, 75, 60
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline="black", width=2)
    f = get_font(10)
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        nx = cx + int((r-12) * math.cos(angle))
        ny = cy + int((r-12) * math.sin(angle))
        d.text((nx-4, ny-5), str(i if i else 12), font=f, fill="black")
    # hour hand
    h_angle = math.radians((hour % 12 + minute / 60) * 30 - 90)
    hx = cx + int(35 * math.cos(h_angle))
    hy = cy + int(35 * math.sin(h_angle))
    d.line([cx, cy, hx, hy], fill="black", width=3)
    # minute hand
    m_angle = math.radians(minute * 6 - 90)
    mx = cx + int(50 * math.cos(m_angle))
    my = cy + int(50 * math.sin(m_angle))
    d.line([cx, cy, mx, my], fill="blue", width=2)
    d.ellipse([cx-3, cy-3, cx+3, cy+3], fill="black")
    if label:
        d.text((cx-30, h-25), label, font=FONTS, fill="black")
    return img

def draw_two_clocks(h1, m1, h2, m2, lab1="", lab2=""):
    """Two clocks side by side."""
    c1 = draw_clock(h1, m1, label=lab1)
    c2 = draw_clock(h2, m2, label=lab2)
    img = Image.new("RGB", (340, 170), "white")
    img.paste(c1, (0, 0))
    img.paste(c2, (170, 0))
    return img

def draw_bar_chart(values, labels, title=""):
    """Simple bar chart."""
    n = len(values)
    w = max(280, n * 55 + 60)
    h = 200
    img, d = new_img(w, h)
    mx = max(values) if values else 1
    bw = 35
    gap = (w - 40) // n
    for i, (v, lb) in enumerate(zip(values, labels)):
        x = 30 + i * gap
        bh = int(v / mx * 120)
        d.rectangle([x, 160-bh, x+bw, 160], fill="#4a90d9", outline="black")
        d.text((x+5, 163), lb, font=FONTS, fill="black")
        d.text((x+8, 155-bh-12), str(v), font=FONTS, fill="black")
    if title:
        d.text((20, 5), title, font=FONTS, fill="gray")
    return img

def draw_dice(top, w=100, h=100):
    """Single die face."""
    img, d = new_img(w, h)
    d.rounded_rectangle([10, 10, 90, 90], radius=10, outline="black", width=2)
    positions = {
        1: [(50, 50)],
        2: [(30, 30), (70, 70)],
        3: [(30, 30), (50, 50), (70, 70)],
        4: [(30, 30), (70, 30), (30, 70), (70, 70)],
        5: [(30, 30), (70, 30), (50, 50), (30, 70), (70, 70)],
        6: [(30, 25), (70, 25), (30, 50), (70, 50), (30, 75), (70, 75)],
    }
    for px, py in positions.get(top, []):
        d.ellipse([px-6, py-6, px+6, py+6], fill="black")
    return img

def draw_two_dice(d1, d2):
    """Two dice side by side."""
    img = Image.new("RGB", (210, 100), "white")
    img.paste(draw_dice(d1), (0, 0))
    img.paste(draw_dice(d2), (110, 0))
    return img

def draw_dot_pattern(rows_cols):
    """Grid of dots with some filled."""
    rows = len(rows_cols)
    cols = max(len(r) for r in rows_cols)
    w, h = cols*30+40, rows*30+40
    img, d = new_img(w, h)
    for r, row in enumerate(rows_cols):
        for c, val in enumerate(row):
            cx, cy = 30+c*30, 30+r*30
            if val == 1:
                d.ellipse([cx-8, cy-8, cx+8, cy+8], fill="black")
            elif val == 0:
                d.ellipse([cx-8, cy-8, cx+8, cy+8], outline="gray", width=1)
            else:
                d.ellipse([cx-8, cy-8, cx+8, cy+8], outline="red", width=2)
                d.text((cx-4, cy-6), "?", font=FONTS, fill="red")
    return img

def draw_coins(values):
    """Row of coins with Ft values."""
    n = len(values)
    w = n * 55 + 20
    img, d = new_img(w, 70)
    for i, v in enumerate(values):
        cx = 35 + i * 55
        r = 22
        d.ellipse([cx-r, 35-r, cx+r, 35+r], fill="#FFD700", outline="#B8860B", width=2)
        d.text((cx-10, 28), f"{v}", font=FONTS, fill="#333")
    return img

def draw_path_grid(rows, cols, start="S", end="C"):
    """Grid for path counting."""
    s = 40
    w, h = cols*s+60, rows*s+80
    img, d = new_img(w, h)
    m = 25
    for i in range(rows+1):
        d.line([m, m+i*s, m+cols*s, m+i*s], fill="black", width=2)
    for j in range(cols+1):
        d.line([m+j*s, m, m+j*s, m+rows*s], fill="black", width=2)
    d.text((m-15, m-15), start, font=FONTB, fill="red")
    d.text((m+cols*s+5, m+rows*s-5), end, font=FONTB, fill="red")
    d.text((15, h-25), "Csak → és ↓ lépésekkel!", font=FONTS, fill="gray")
    return img

def draw_symmetry_shape():
    """Shape with symmetry line, ask to mirror."""
    img, d = new_img(240, 200)
    # dashed vertical line
    for y in range(0, 200, 8):
        d.line([120, y, 120, min(y+4, 200)], fill="red", width=1)
    # left half of an L-shape
    d.rectangle([40, 40, 120, 80], fill="#AED6F1", outline="black", width=2)
    d.rectangle([80, 80, 120, 160], fill="#AED6F1", outline="black", width=2)
    # question mark on the right
    d.text((155, 90), "?", font=get_bold(30), fill="red")
    d.text((30, 175), "Tükrözd!", font=FONTS, fill="gray")
    return img

def draw_paper_fold():
    """Paper folding: square folded and hole punched."""
    img, d = new_img(360, 120)
    f = FONTS
    # Step 1: full square
    d.rectangle([10, 20, 80, 90], outline="black", width=2)
    d.text((30, 95), "1.", font=f, fill="gray")
    # Step 2: folded in half
    d.rectangle([100, 20, 135, 90], outline="black", width=2)
    d.line([100, 20, 100, 90], fill="blue", width=2)
    d.text((108, 95), "2.", font=f, fill="gray")
    # Step 3: hole punched
    d.rectangle([155, 20, 190, 90], outline="black", width=2)
    d.line([155, 20, 155, 90], fill="blue", width=2)
    d.ellipse([165, 45, 180, 60], fill="white", outline="black", width=2)
    d.text((163, 95), "3.", font=f, fill="gray")
    # Arrow
    d.text((205, 45), "→ ?", font=get_bold(22), fill="red")
    # Options hint
    d.text((250, 30), "Kinyitva:", font=f, fill="gray")
    d.rectangle([250, 45, 320, 100], outline="black", width=2)
    d.ellipse([260, 55, 275, 70], outline="black", width=2)
    d.ellipse([295, 55, 310, 70], outline="black", width=2)
    return img

def draw_venn_two(a_only, both, b_only, la="A", lb="B"):
    """Two-circle Venn diagram."""
    img, d = new_img(280, 180)
    d.ellipse([30, 20, 170, 160], outline="blue", width=2)
    d.ellipse([110, 20, 250, 160], outline="red", width=2)
    d.text((70, 15), la, font=FONTB, fill="blue")
    d.text((190, 15), lb, font=FONTB, fill="red")
    d.text((80, 80), str(a_only), font=FONTB, fill="black")
    d.text((133, 80), str(both), font=FONTB, fill="black")
    d.text((185, 80), str(b_only), font=FONTB, fill="black")
    return img

def draw_number_line(start, end, marks=None, highlight=None):
    """Number line with marks."""
    w = 350
    img, d = new_img(w, 80)
    y = 35
    d.line([20, y, w-20, y], fill="black", width=2)
    d.polygon([(w-20, y-5), (w-10, y), (w-20, y+5)], fill="black")
    n = end - start
    step = (w - 60) / n
    for i in range(n + 1):
        x = 30 + int(i * step)
        d.line([x, y-5, x, y+5], fill="black", width=2)
        val = start + i
        if marks is None or val in (marks or []):
            d.text((x-5, y+10), str(val), font=FONTS, fill="black")
    if highlight is not None:
        x = 30 + int((highlight - start) * step)
        d.ellipse([x-6, y-6, x+6, y+6], fill="red")
        d.text((x-3, y-20), "?", font=FONTB, fill="red")
    return img

def draw_domino(top, bottom, w=60, h=110):
    """Single domino."""
    img, d = new_img(w, h)
    d.rounded_rectangle([5, 5, 55, 105], radius=5, outline="black", width=2)
    d.line([5, 55, 55, 55], fill="black", width=2)
    pos = {0:[], 1:[(30,30)], 2:[(20,20),(40,40)], 3:[(20,20),(30,30),(40,40)],
           4:[(20,20),(40,20),(20,40),(40,40)], 5:[(20,20),(40,20),(30,30),(20,40),(40,40)],
           6:[(20,17),(40,17),(20,30),(40,30),(20,43),(40,43)]}
    for px, py in pos.get(top, []):
        d.ellipse([px-4, py-4, px+4, py+4], fill="black")
    for px, py in pos.get(bottom, []):
        d.ellipse([px-4, py+50, px+4, py+58], fill="black")
    return img

def draw_fruit_equation():
    """Visual equation with fruit symbols."""
    img, d = new_img(340, 140)
    f = FONT
    fb = FONTB
    # Equation 1: apple + apple + cherry = 16
    d.text((10, 20), "🍎 + 🍎 + 🍒 = 16", font=fb, fill="black")
    # Equation 2: apple + cherry + cherry = 14
    d.text((10, 55), "🍎 + 🍒 + 🍒 = 14", font=fb, fill="black")
    # Question
    d.text((10, 95), "🍎 = ?    🍒 = ?", font=fb, fill="red")
    return img

def draw_colored_grid(grid, cell=35):
    """Grid with colored cells."""
    rows, cols = len(grid), len(grid[0])
    w, h = cols*cell+20, rows*cell+20
    img, d = new_img(w, h)
    colors = {"R": "#FF6B6B", "B": "#74B9FF", "G": "#55EFC4",
              "Y": "#FFEAA7", "W": "white", "?": "white"}
    m = 10
    for r in range(rows):
        for c in range(cols):
            x1, y1 = m+c*cell, m+r*cell
            v = grid[r][c]
            d.rectangle([x1, y1, x1+cell, y1+cell], fill=colors.get(v, "white"), outline="black", width=2)
            if v == "?":
                d.text((x1+12, y1+8), "?", font=FONTB, fill="red")
    return img

def draw_staircase(n):
    """Staircase pattern made of squares."""
    cell = 25
    w, h = n*cell+40, n*cell+40
    img, d = new_img(w, h)
    m = 10
    for i in range(n):
        for j in range(i+1):
            x1 = m + j*cell
            y1 = m + (n-1-i)*cell
            d.rectangle([x1, y1, x1+cell, y1+cell], fill="#AED6F1", outline="black", width=2)
    return img

def draw_simple_map():
    """Simple map with points and paths (graph)."""
    img, d = new_img(260, 200)
    pts = {"A": (40, 100), "B": (130, 30), "C": (220, 100), "D": (130, 170)}
    edges = [("A","B"), ("A","D"), ("B","C"), ("B","D"), ("D","C")]
    for a, b in edges:
        d.line([pts[a], pts[b]], fill="black", width=2)
    for name, (x, y) in pts.items():
        d.ellipse([x-12, y-12, x+12, y+12], fill="#4a90d9", outline="black", width=2)
        d.text((x-5, y-7), name, font=FONTB, fill="white")
    return img

# ═══════════════════════════════════════════════════════════════
#  ALL 50 QUESTIONS
# ═══════════════════════════════════════════════════════════════
def build_questions():
    init_fonts()
    QS = []

    # ─── GEOMETRY: COUNT SHAPES ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Hány háromszög látható az ábrán? (Egy nagy háromszög oldalfelező pontjait összekötöttük.)",
        "options": ["3", "4", "5", "6", "8"],
        "correct": "C",
        "comment": "4 kis háromszög + 1 nagy = 5.",
        "image": img_to_uri(draw_triangle_with_inner()),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Hány négyzet látható az ábrán összesen? (Nem csak a kicsik!)",
        "options": ["9", "10", "12", "14", "16"],
        "correct": "D",
        "comment": "9 kis (1×1) + 4 közepes (2×2) + 1 nagy (3×3) = 14.",
        "image": img_to_uri(draw_count_squares_3x3()),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Hány téglalap (beleértve a négyzeteket is) látható az ábrán?",
        "options": ["8", "12", "16", "18", "24"],
        "correct": "D",
        "comment": "Egy 2×3-as rácsból: C(3,2)×C(4,2) = 3×6 = 18.",
        "image": img_to_uri(draw_count_rectangles()),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "Két háromszög fedi egymást az ábrán. Hány zárt tartomány keletkezett?",
        "options": ["4", "5", "6", "7", "8"],
        "correct": "D",
        "comment": "Az átfedésnél a két háromszög 7 tartományt alkot: 2×2 szélső + 2 közepes + 1 közös közép = 7.",
        "image": img_to_uri(draw_overlapping_triangles()),
    })

    # ─── PATTERNS ───
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "Mi a következő elem a mintában? ○ △ □ ○ △ ?",
        "options": ["○", "△", "□", "◇", "★"],
        "correct": "C",
        "comment": "A minta: kör, háromszög, négyzet ismétlődik. A következő: négyzet (□).",
        "image": img_to_uri(draw_shape_sequence()),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "A bűvös négyzetben minden sor, oszlop és átló összege 15. Melyik szám van a ? helyén?",
        "options": ["4", "6", "7", "8", "9"],
        "correct": "D",
        "comment": "A 3. sor: 4 + 3 + ? = 15, tehát ? = 8.",
        "image": img_to_uri(draw_number_grid_pattern()),
    })

    # ─── BALANCE SCALES ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "A mérleg egyensúlyban van: 2 alma = 1 dinnye. Hány alma nyom annyit, mint 3 dinnye?",
        "options": ["3", "4", "5", "6", "8"],
        "correct": "D",
        "comment": "1 dinnye = 2 alma, tehát 3 dinnye = 6 alma.",
        "image": img_to_uri(draw_two_scales("🍎🍎", "🍈", "🍈🍈🍈", "? 🍎")),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "1. mérés: 3 kocka = 1 henger. 2. mérés: 1 henger + 1 kocka = 16 kg. Hány kg egy kocka?",
        "options": ["2", "3", "4", "5", "6"],
        "correct": "C",
        "comment": "3K=H. H+K=16 → 3K+K=16 → 4K=16 → K=4.",
        "image": img_to_uri(draw_two_scales("⬜⬜⬜", "🔵", "🔵 ⬜", "16kg")),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A mérleg egyensúlyban van: 5 alma = 15 eper. Hány eper nyom annyit, mint 1 alma?",
        "options": ["1", "2", "3", "4", "5"],
        "correct": "C",
        "comment": "5 alma = 15 eper → 1 alma = 3 eper.",
        "image": img_to_uri(draw_balance_scale("🍎×5", "🍓×15")),
    })

    # ─── CLOCKS ───
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "Hány órát mutat az óra az ábrán?",
        "options": ["2:00", "3:00", "4:00", "6:00", "9:00"],
        "correct": "B",
        "comment": "A kismutató a 3-ason, a nagymutató a 12-esen van: 3:00.",
        "image": img_to_uri(draw_clock(3, 0)),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "Az óra 7:45-öt mutat. Hány perccel van 8:00 előtt?",
        "options": ["10", "15", "20", "25", "30"],
        "correct": "B",
        "comment": "8:00 - 7:45 = 15 perc.",
        "image": img_to_uri(draw_clock(7, 45)),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "Az első óra 9:15-öt, a második 10:00-t mutat. Hány perc telt el a két időpont között?",
        "options": ["15", "30", "45", "50", "60"],
        "correct": "C",
        "comment": "10:00 - 9:15 = 45 perc.",
        "image": img_to_uri(draw_two_clocks(9, 15, 10, 0, "Előtte", "Utána")),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Az óra 11:40-et mutat. Egy óra és 35 perc múlva hány óra lesz?",
        "options": ["12:55", "13:05", "13:10", "13:15", "13:25"],
        "correct": "D",
        "comment": "11:40 + 1:35 = 13:15.",
        "image": img_to_uri(draw_clock(11, 40)),
    })

    # ─── BAR CHARTS ───
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "Az ábrán a gyerekek kedvenc gyümölcse újságolya. Hány gyerek szereti legjobban az almát?",
        "options": ["3", "5", "7", "8", "10"],
        "correct": "C",
        "comment": "Az alma oszlopa 7-et mutat.",
        "image": img_to_uri(draw_bar_chart([7, 5, 3, 8], ["Alma", "Banán", "Szőlő", "Eper"], "Kedvenc gyümölcs")),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A diagramon négy barát matricagyűjtését látod. Mennyivel több matricája van Péternek, mint Annának?",
        "options": ["5", "8", "10", "12", "15"],
        "correct": "C",
        "comment": "Péter: 25, Anna: 15. Különbség: 25-15 = 10.",
        "image": img_to_uri(draw_bar_chart([15, 25, 20, 10], ["Anna", "Péter", "Gabi", "Lili"], "Matricák száma")),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A diagramról olvasd le: összesen hány könyvet olvastak a gyerekek?",
        "options": ["12", "15", "18", "20", "24"],
        "correct": "C",
        "comment": "4+6+3+5 = 18.",
        "image": img_to_uri(draw_bar_chart([4, 6, 3, 5], ["Kati", "Bence", "Lili", "Dani"], "Olvasott könyvek")),
    })

    # ─── DICE ───
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "Két dobókockát dobunk. Az ábrán látható eredmények összege mennyi?",
        "options": ["5", "7", "8", "9", "10"],
        "correct": "D",
        "comment": "4 + 5 = 9.",
        "image": img_to_uri(draw_two_dice(4, 5)),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A dobókocka szemben lévő oldalain a pontok összege mindig 7. Ha felül 2 van, mennyi pontot látsz összesen az oldalain (nem az alján)?",
        "options": ["10", "12", "14", "16", "18"],
        "correct": "C",
        "comment": "Az oldalsó lapok páronként 7-et adnak. Két pár van, tehát 7+7=14.",
        "image": img_to_uri(draw_dice(2)),
    })

    # ─── PATH COUNTING ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "S-ből C-be csak jobbra (→) és lefelé (↓) léphetsz. Hányféleképpen juthatsz el a 2×2-es rácson?",
        "options": ["4", "5", "6", "8", "10"],
        "correct": "C",
        "comment": "2 jobbra + 2 lefelé: 4!/(2!×2!) = 6.",
        "image": img_to_uri(draw_path_grid(2, 2)),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "S-ből C-be csak jobbra (→) és lefelé (↓) léphetsz. Hányféleképpen juthatsz el a 2×3-as rácson?",
        "options": ["6", "8", "10", "12", "15"],
        "correct": "C",
        "comment": "2 le + 3 jobbra: 5!/(2!×3!) = 10.",
        "image": img_to_uri(draw_path_grid(2, 3)),
    })

    # ─── GRAPH / MAP ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "A térképen 4 város van (A, B, C, D), közöttük utak vezetnek (lásd ábra). Hányféleképpen juthatsz el A-ból C-be úgy, hogy minden utat legfeljebb egyszer használsz?",
        "options": ["2", "3", "4", "5", "6"],
        "correct": "C",
        "comment": "A→B→C, A→B→D→C, A→D→C, A→D→B→C. Összesen 4.",
        "image": img_to_uri(draw_simple_map()),
    })

    # ─── COINS ───
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "Az ábrán lévő érmék összesen mennyit érnek?",
        "options": ["45", "50", "55", "60", "65"],
        "correct": "C",
        "comment": "20 + 10 + 20 + 5 = 55 Ft.",
        "image": img_to_uri(draw_coins([20, 10, 20, 5])),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "Az ábrán lévő érmékből mennyit kell elvenni, hogy pontosan 50 Ft maradjon?",
        "options": ["5 Ft", "10 Ft", "20 Ft", "25 Ft", "30 Ft"],
        "correct": "C",
        "comment": "20+10+20+10+10 = 70 Ft. 70-50 = 20 Ft-ot kell elvenni.",
        "image": img_to_uri(draw_coins([20, 10, 20, 10, 10])),
    })

    # ─── VENN DIAGRAMS ───
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "Az ábrán a focizó (A) és kosárlabdázó (B) gyerekeket látod. Hányan sportolnak összesen?",
        "options": ["15", "18", "20", "22", "25"],
        "correct": "C",
        "comment": "8 + 4 + 8 = 20. (A csak-foci + mindkettő + csak-kosár.)",
        "image": img_to_uri(draw_venn_two(8, 4, 8, "Foci", "Kosár")),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Egy osztályban 25 gyerek van. 15 szeret rajzolni, 12 szeret énekelni, és 5 mindkettőt. Az ábrán hány gyerek nem szeret sem rajzolni, sem énekelni?",
        "options": ["1", "2", "3", "4", "5"],
        "correct": "C",
        "comment": "Rajzol VAGY énekel: 15+12-5 = 22. Egyik sem: 25-22 = 3.",
        "image": img_to_uri(draw_venn_two(10, 5, 7, "Rajz", "Ének")),
    })

    # ─── COLORED GRID PUZZLES ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "A 3×3-as rácsban minden sorban és oszlopban pontosan 1 piros (R), 1 kék (B) és 1 fehér (W) mező legyen. Mi kerül a ? helyére?",
        "options": ["Piros", "Kék", "Fehér", "Zöld", "Sárga"],
        "correct": "A",
        "comment": "Az oszlop- és sorszabály csak pirossal teljesül a ? helyén.",
        "image": img_to_uri(draw_colored_grid([["R","B","W"],["W","?","B"],["B","W","R"]])),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A rács mintáját kell folytatni. Pirossal (R) és kékkel (B) váltakozik sakkminta szerűen. Mi van a ? helyén?",
        "options": ["Piros", "Kék", "Zöld", "Sárga", "Fehér"],
        "correct": "B",
        "comment": "Sakkmintában a ?-os hely kék.",
        "image": img_to_uri(draw_colored_grid([["R","B","R"],["B","R","B"],["R","?","R"]])),
    })

    # ─── STAIRCASE ───
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A lépcsős alakzatban hány kocka van összesen?",
        "options": ["10", "12", "14", "15", "20"],
        "correct": "D",
        "comment": "1+2+3+4+5 = 15.",
        "image": img_to_uri(draw_staircase(5)),
    })
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "A lépcsős alakzatban hány kocka van összesen?",
        "options": ["4", "6", "8", "10", "12"],
        "correct": "D",
        "comment": "1+2+3+4 = 10.",
        "image": img_to_uri(draw_staircase(4)),
    })

    # ─── SYMMETRY ───
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A piros vonal a tükrözési tengely. Hány kocka kell a jobb oldalra, hogy szimmetrikus legyen az alakzat?",
        "options": ["2", "3", "4", "5", "6"],
        "correct": "C",
        "comment": "A bal oldalon 4 kockányi terület van, a jobb oldalon is 4 kell.",
        "image": img_to_uri(draw_symmetry_shape()),
    })

    # ─── PAPER FOLDING ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Egy négyzet alakú papírt félbehajtunk, majd lyukat vágunk bele (lásd ábra). Kinyitás után hány lyuk lesz?",
        "options": ["1", "2", "3", "4", "6"],
        "correct": "B",
        "comment": "Egy hajtásnál a lyuk megkettőződik. Tehát 2 lyuk lesz.",
        "image": img_to_uri(draw_paper_fold()),
    })

    # ─── NUMBER LINE ───
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "A számegyenesen hová esik a piros pont?",
        "options": ["5", "6", "7", "8", "9"],
        "correct": "C",
        "comment": "A pont a 7-nél van.",
        "image": img_to_uri(draw_number_line(0, 10, highlight=7)),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A számegyenesen a két piros pont közti távolság mennyi? (A pontok a 3-nál és a 11-nél vannak.)",
        "options": ["6", "7", "8", "9", "10"],
        "correct": "C",
        "comment": "11 - 3 = 8.",
        "image": img_to_uri(draw_number_line(0, 15, highlight=3)),
    })

    # ─── FRUIT EQUATIONS ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Az ábrán: 🍎 + 🍎 + 🍒 = 16 és 🍎 + 🍒 + 🍒 = 14. Mennyit ér egy 🍎?",
        "options": ["4", "5", "6", "7", "8"],
        "correct": "C",
        "comment": "Az 1. egyenletből: 2A+C=16. A 2.-ból: A+2C=14. Kivonva: A-C=2. Ezzel: A=6, C=4.",
        "image": img_to_uri(draw_fruit_equation()),
    })

    # ─── DOT PATTERNS ───
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A pontmintában minden sor és oszlop összege 3 legyen (fekete = 1, fehér = 0). A ?-os helyre tegyünk-e pontot?",
        "options": ["Igen", "Nem", "Mindegy", "Nem tudjuk", "Kettőt kell"],
        "correct": "A",
        "comment": "Az oszlopban 2 pont van, a sorozathoz 3 kell. Tehát igen, kell oda pont.",
        "image": img_to_uri(draw_dot_pattern([[1,1,1],[1,0,1],[1,2,0]])),
    })
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "Hány fekete pont van összesen az ábrán?",
        "options": ["6", "7", "8", "9", "10"],
        "correct": "C",
        "comment": "Sorról sorra: 2+3+3 = 8.",
        "image": img_to_uri(draw_dot_pattern([[1,0,1,0],[1,1,0,1],[0,1,1,1]])),
    })

    # ─── DOMINO ───
    QS.append({
        "class": "2", "difficulty": "easy",
        "question": "Hány pontot látsz összesen a dominón?",
        "options": ["7", "8", "9", "10", "11"],
        "correct": "D",
        "comment": "Felül 4, alul 6: 4+6 = 10.",
        "image": img_to_uri(draw_domino(4, 6)),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "Egy dominón felül 3 pont van. A felső és alsó pontok összege 8. Hány pont van alul?",
        "options": ["3", "4", "5", "6", "7"],
        "correct": "C",
        "comment": "8 - 3 = 5.",
        "image": img_to_uri(draw_domino(3, 5)),
    })

    # ─── GEOMETRY AREA ───
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A rajzon egy 5 lépcsős alakzat van kockákból. Hány kockát kell hozzáadni, hogy 5×5-ös négyzet legyen?",
        "options": ["6", "8", "10", "12", "15"],
        "correct": "C",
        "comment": "A lépcsőben 1+2+3+4+5=15, a 5×5 négyzetben 25. Kell: 25-15 = 10.",
        "image": img_to_uri(draw_staircase(5)),
    })

    # ─── MORE HARD BALANCE/LOGIC ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "1. mérés: 2 golyó + 1 kocka = 10 kg. 2. mérés: 1 golyó + 3 kocka = 9 kg. Hány kg egy golyó?",
        "options": ["2", "3", "4", "5", "6"],
        "correct": "B",
        "comment": "2G+K=10, G+3K=9. Az elsőből K=10-2G. Behelyettesítve: G+3(10-2G)=9 → G+30-6G=9 → -5G=-21 → hmm. Javítva: 2G+K=10 (1), G+3K=9 (2). (1)×3: 6G+3K=30. Kivonva (2): 5G=21. Ez nem egész. Javítom: 2G+K=11, G+3K=13. → K=11-2G, G+3(11-2G)=13 → G+33-6G=13 → -5G=-20 → G=4. K=3. Javítsuk a kérdést!",
        "image": img_to_uri(draw_two_scales("⚽⚽ ⬜", "11kg", "⚽ ⬜⬜⬜", "13kg")),
    })

    # Fix the above question's data
    QS[-1]["question"] = "1. mérés: 2 golyó + 1 kocka = 11 kg. 2. mérés: 1 golyó + 3 kocka = 13 kg. Hány kg egy golyó?"
    QS[-1]["comment"] = "2G+K=11, G+3K=13. K=11-2G → G+33-6G=13 → 5G=20 → G=4."
    QS[-1]["correct"] = "C"

    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Az I. óra 2:30-at, a II. óra 5:15-öt mutat. Hány perc telt el a két időpont között?",
        "options": ["135", "145", "155", "165", "175"],
        "correct": "D",
        "comment": "2:30 → 5:15 = 2 óra 45 perc = 165 perc.",
        "image": img_to_uri(draw_two_clocks(2, 30, 5, 15, "I.", "II.")),
    })

    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "A diagramról olvasd le: melyik hónapban volt a legtöbb esős nap, és mennyi?",
        "options": ["Március: 8", "Április: 12", "Május: 6", "Június: 10", "Április: 10"],
        "correct": "B",
        "comment": "Április oszlopa a legmagasabb: 12 esős nap.",
        "image": img_to_uri(draw_bar_chart([8, 12, 6, 10], ["Márc", "Ápr", "Máj", "Jún"], "Esős napok")),
    })

    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "A Venn-diagramon kutyás (A) és macskás (B) családokat látsz. 6 családnak csak kutyája, 3-nak mindkettő, 5-nek csak macskája van. Hány családnak van háziállata?",
        "options": ["8", "11", "14", "15", "20"],
        "correct": "C",
        "comment": "6 + 3 + 5 = 14.",
        "image": img_to_uri(draw_venn_two(6, 3, 5, "Kutya", "Macska")),
    })

    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A 4×4-es rácsban hány piros (R) mező van?",
        "options": ["4", "5", "6", "7", "8"],
        "correct": "C",
        "comment": "Megszámolva: 6 piros mező van.",
        "image": img_to_uri(draw_colored_grid([["R","B","R","B"],["B","R","B","W"],["R","W","R","B"],["B","R","W","W"]])),
    })

    # ─── EXTRA QUESTIONS TO REACH 50 ───
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Ha a 'Start' mezőről indulsz és 3-at lépsz jobbra, majd 2-t lefelé, melyik mezőre érkezel?",
        "options": ["A", "B", "C", "D", "E"],
        "correct": "D",
        "comment": "Start=bal felső. 3 jobbra = 4. oszlop. 2 le = 3. sor. Ott a 'D' betű van.",
        "image": img_to_uri(draw_colored_grid([["Start","","",""],["","","",""],["","","","D"],["","","",""]])),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "Mennyi az idő az órán?",
        "options": ["1:30", "2:30", "3:30", "4:30", "5:30"],
        "correct": "B",
        "comment": "A kismutató a 2 és 3 között, a nagy a 6-oson. 2:30.",
        "image": img_to_uri(draw_clock(2, 30)),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "Hány háromszög van az ábrán?",
        "options": ["3", "4", "5", "6", "7"],
        "correct": "C",
        "comment": "Egy nagy háromszög + benne egy fordított kisebb. Összesen 5 db (4 kicsi + 1 nagy).",
        "image": img_to_uri(draw_triangle_with_inner()),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "Melyik dominón van összesen 9 pont?",
        "options": ["A", "B", "C", "D", "E"],
        "correct": "D",
        "comment": "A: 2+5=7, B: 3+3=6, C: 4+4=8, D: 4+5=9, E: 5+5=10.",
        "image": img_to_uri(draw_domino(4, 5)),
    })
    QS.append({
        "class": "2", "difficulty": "hard",
        "question": "A mérleg egyensúlyban: 1 négyzet = 2 kör. Hány kör nyom annyit, mint 3 négyzet?",
        "options": ["3", "4", "5", "6", "8"],
        "correct": "D",
        "comment": "1N = 2K → 3N = 6K.",
        "image": img_to_uri(draw_balance_scale("🟦", "🔴🔴")),
    })
    QS.append({
        "class": "2", "difficulty": "medium",
        "question": "A számegyenesen a 10 és 20 között pontosan középen álló szám melyik?",
        "options": ["12", "14", "15", "16", "18"],
        "correct": "C",
        "comment": "(10+20)/2 = 15.",
        "image": img_to_uri(draw_number_line(10, 20, highlight=15)),
    })

    print(f"  Built {len(QS)} image questions.")
    return QS


# ═══════════════════════════════════════════════════════════════
#  MAIN – insert into DB
# ═══════════════════════════════════════════════════════════════
def main():
    print("Generating image questions…")
    questions = build_questions()

    if not os.path.exists(DB_PATH):
        print(f"ERROR: {DB_PATH} not found. Run manual_insert_questions.py first!")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Remove old image questions to avoid duplicates
    cur.execute("DELETE FROM questions WHERE image IS NOT NULL")
    removed = cur.execute("SELECT changes()").fetchone()[0]
    if removed:
        print(f"  Removed {removed} old image questions.")

    for q in questions:
        cur.execute("""
            INSERT INTO questions
            (class, difficulty, question, image,
             option_a, option_b, option_c, option_d, option_e,
             correct_answer, comment, shown_count)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,0)
        """, (
            q["class"], q["difficulty"], q["question"], q.get("image"),
            q["options"][0], q["options"][1], q["options"][2],
            q["options"][3], q["options"][4],
            q["correct"], q.get("comment"),
        ))

    conn.commit()

    # Stats
    cur.execute("SELECT COUNT(*) FROM questions")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM questions WHERE image IS NOT NULL")
    img_count = cur.fetchone()[0]
    cur.execute("SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty ORDER BY difficulty")
    stats = cur.fetchall()
    conn.close()

    print(f"\n  Inserted {len(questions)} image questions.")
    print(f"  Total questions in DB: {total}")
    print(f"  Questions with images: {img_count}")
    for d, c in stats:
        print(f"    {d}: {c}")

    # Export
    print("\nExporting db_data.js…")
    with open(DB_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    with open(JS_PATH, "w") as f:
        f.write(f"const DB_BASE64 = '{b64}';\n")
    print(f"Done. db_data.js = {len(b64)//1024} KB")


if __name__ == "__main__":
    main()
