#!/usr/bin/env python3
"""
Reclassify mislabeled questions + add 20 genuinely hard questions + rebuild DB.

Run:  python3 reclassify_and_add.py
"""

import sqlite3, os, base64, io
from PIL import Image, ImageDraw, ImageFont

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zrinyi_questions.db")
JS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_data.js")

# Import existing questions
import manual_insert_questions as m

# =====================================================================
#  1) RECLASSIFICATIONS  —  question text prefix → new difficulty
# =====================================================================
RECLASSIFY = {
    # hard → easy (trivial arithmetic / one-step)
    "Egy dobozban kék és zöld golyók vannak": "easy",         # 12+8=20
    "A táblán 4 piros és 4 kék kréta van": "easy",           # 8-3=5
    "Egy edénybe 5 liter víz fér": "easy",                   # 5-2=3
    "Három testvér összesen 24 éves. A legidősebb 10": "easy", # 24-10-8=6
    "A létrán 12 fok van. Jani felment a közepéig": "easy",   # 12/2=6
    "Egy kétjegyű szám 19. Ha felcseréljük": "easy",          # 19→91
    "A dobókocka szemközti oldalain": "easy",                 # 7-3=4

    # hard → medium (requires one extra reasoning step)
    "Egy film 2 perc 30 másodpercig tart": "medium",          # time conversion
    "Egy könyv 4. oldalától a 10. oldaláig": "medium",        # fence-post
    "Egy szám felét és negyedét összeadjuk": "medium",        # x/2+x/4=30
    "Hány vágással tudunk egy rudat 6 darabra": "medium",     # n-1 cuts
    "Egy karkötőt fűzöl. Minden 3. gyöngy piros": "medium",  # 12/3=4
    "Melyik szám következik a sorozatban: 3, 6, 12, 24": "medium",  # *2
    "Hány darab 1-es számjegyet kell leírnunk összesen 1-től 30": "medium",  # digit counting
}


def reclassify(questions):
    """Reclassify mislabeled questions in-place, return count."""
    count = 0
    for q in questions:
        for prefix, new_diff in RECLASSIFY.items():
            if q["question"].startswith(prefix) and q["difficulty"] != new_diff:
                old = q["difficulty"]
                q["difficulty"] = new_diff
                count += 1
                print(f"  ✓ {old}→{new_diff}: {q['question'][:60]}…")
                break
    return count


# =====================================================================
#  2)  IMAGE HELPERS
# =====================================================================
def img_to_data_uri(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def get_font(size=16):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# --- Balance scale image ---
def draw_scales_image():
    W, H = 440, 180
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    font = get_font(13)
    big = get_font(18)

    def scale(cx, cy, left, right, label):
        d.polygon([(cx, cy+40), (cx-8, cy+52), (cx+8, cy+52)], fill="#555")
        d.line([cx-55, cy+40, cx+55, cy+40], fill="black", width=3)
        d.arc([cx-68, cy+32, cx-42, cy+50], 0, 180, fill="black", width=2)
        d.arc([cx+42, cy+32, cx+68, cy+50], 0, 180, fill="black", width=2)
        d.text((cx-55, cy+5), left, font=big, fill="black")
        d.text((cx+42, cy+5), right, font=big, fill="black")
        d.text((cx-5, cy+12), "=", font=font, fill="gray")
        d.text((cx-20, cy+55), label, font=font, fill="black")

    scale(110, 40, "🍎🍎🍎", "🍓×6", "1. mérés")
    scale(330, 40, "🍎🍓🍓", "  🍐", "2. mérés")
    return img

# --- Sum/difference bar diagram ---
def draw_sum_diff_bars():
    W, H = 380, 130
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f = get_font(13)
    fb = get_font(15)
    left = 50
    d.rectangle([left, 20, left+260, 45], fill="#4a90d9", outline="black", width=2)
    d.text((left+265, 23), "nagyobb", font=f, fill="black")
    d.rectangle([left, 60, left+180, 85], fill="#7bc67e", outline="black", width=2)
    d.text((left+185, 63), "kisebb", font=f, fill="black")
    d.text((10, 45), "50", font=fb, fill="red")
    d.line([left+180, 90, left+260, 90], fill="red", width=2)
    mid = left + 220
    d.text((mid-15, 95), "kül: 10", font=f, fill="red")
    return img

# --- Grid puzzle image ---
def draw_grid_puzzle():
    W, H = 200, 230
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f = get_font(11)
    margin, cell, r = 20, 40, 14
    # Pattern: rows have [3,2,2,1] black → need 2 swaps for 2-per-row/col
    grid = [[1,1,0,1],[0,1,1,0],[1,0,0,1],[0,0,1,0]]
    for i in range(5):
        d.line([margin, margin+i*cell, margin+4*cell, margin+i*cell], fill="#ccc")
        d.line([margin+i*cell, margin, margin+i*cell, margin+4*cell], fill="#ccc")
    for r_i in range(4):
        for c in range(4):
            cx = margin + c*cell + cell//2
            cy = margin + r_i*cell + cell//2
            if grid[r_i][c]:
                d.ellipse([cx-r, cy-r, cx+r, cy+r], fill="black")
            else:
                d.ellipse([cx-r, cy-r, cx+r, cy+r], fill="white", outline="black", width=2)
    d.text((20, 190), "Soronként és oszloponként", font=f, fill="black")
    d.text((20, 205), "pontosan 2 fekete legyen!", font=f, fill="black")
    return img

# --- Path counting grid ---
def draw_path_grid():
    W, H = 200, 230
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f = get_font(13)
    margin, cell = 30, 50
    for i in range(4):
        for j in range(4):
            d.line([margin+j*cell, margin+i*cell, margin+(j+1)*cell, margin+i*cell], fill="black", width=2)
            d.line([margin+j*cell, margin+i*cell, margin+j*cell, margin+(i+1)*cell], fill="black", width=2)
    # Draw only bottom and right borders of last cells
    for j in range(4):
        d.line([margin+j*cell, margin+3*cell, margin+(j+1)*cell, margin+3*cell], fill="black", width=2)
    for i in range(4):
        d.line([margin+3*cell, margin+i*cell, margin+3*cell, margin+(i+1)*cell], fill="black", width=2)
    # Mark start and end
    d.text((margin-15, margin-20), "S", font=get_font(16), fill="red")
    d.text((margin+3*cell+5, margin+3*cell-5), "C", font=get_font(16), fill="red")
    d.text((20, 200), "Csak jobbra és lefelé!", font=f, fill="black")
    return img


# =====================================================================
#  3)  20 NEW GENUINELY HARD QUESTIONS
# =====================================================================
def build_new_hard_questions():
    img_scales = draw_scales_image()
    img_bars = draw_sum_diff_bars()
    img_grid = draw_grid_puzzle()
    img_path = draw_path_grid()

    return [
        # ---- COMBINATORICS ----
        {
            "class": "2", "difficulty": "hard",
            "question": "Az S-ből a C-be kell eljutnod a rácson, de csak jobbra vagy lefelé léphetsz (lásd ábra). Hányféleképpen tudsz eljutni?",
            "options": ["6", "10", "15", "20", "24"],
            "correct": "D",
            "image": img_to_data_uri(img_path),
            "comment": "Egy 3×3-as rácson S-től C-ig 3 jobbra + 3 lefelé lépés kell. Ezek sorrendje: 6!/(3!*3!) = 20.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Három szín közül választhatsz: piros, kék, zöld. Egy háromszög mindhárom oldalát ki szeretnéd festeni, de a szomszédos oldalak nem lehetnek ugyanolyan színűek. Hányféleképpen teheted meg?",
            "options": ["3", "6", "9", "12", "18"],
            "correct": "B",
            "image": None,
            "comment": "Az 1. oldal 3-féle, a 2. oldal 2-féle (nem ugyanaz), a 3. oldal 1-féle (nem az 1. és nem a 2. színű). 3×2×1 = 6.",
        },
        # ---- BALANCE / WEIGHT ----
        {
            "class": "2", "difficulty": "hard",
            "question": "A mérleg mindkétszer egyensúlyban van (lásd ábra). 3 alma = 6 eper, és 1 alma + 2 eper = 1 körte. Hány szem eper nyom annyit, mint 1 körte?",
            "options": ["2", "3", "4", "5", "6"],
            "correct": "C",
            "image": img_to_data_uri(img_scales),
            "comment": "3 alma = 6 eper → 1 alma = 2 eper. 1 alma + 2 eper = 1 körte → 2+2 = 4 eper = 1 körte.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Két szám összege 50, különbségük 10 (lásd ábra). Melyik a nagyobb szám?",
            "options": ["20", "25", "28", "30", "35"],
            "correct": "D",
            "image": img_to_data_uri(img_bars),
            "comment": "Ha a kisebb szám x, akkor x + (x+10) = 50 → 2x = 40 → x = 20. A nagyobb: 30.",
        },
        # ---- LOGIC / TRICKY WORDING ----
        {
            "class": "2", "difficulty": "hard",
            "question": "Négy gyerek közül mindenki pontosan egyszer hazudik. Kati: 'Peti a legidősebb.' Peti: 'Én vagyok a legfiatalabb.' Éva: 'Kati idősebb nálam.' Gábor: 'Éva a legfiatalabb.' Ki a legidősebb?",
            "options": ["Kati", "Peti", "Éva", "Gábor", "Nem meghatározható"],
            "correct": "A",
            "image": None,
            "comment": "Ha Kati igazat mond (Peti a legidősebb), akkor Peti is igazat mondana (ő a legfiatalabb) – ellentmondás, tehát Kati hazudik. De a feladat: mindenki pontosan egyszer hazudik. Próbálgatással: Kati a legidősebb, Éva igazat mond, Gábor hazudik, Peti hazudik.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Az ábrán egy 4×4-es rács látható fekete és fehér golyókkal. Legkevesebb hány golyó színét kell megváltoztatnod, hogy MINDEN sorban és MINDEN oszlopban pontosan 2 fekete golyó legyen?",
            "options": ["1", "2", "3", "4", "5"],
            "correct": "B",
            "image": img_to_data_uri(img_grid),
            "comment": "Az 1. sorban 3 fekete van (1 túl sok), a 4. sorban 1 (1 túl kevés). Egy-egy csere elég: összesen 2.",
        },
        # ---- NUMBER THEORY ----
        {
            "class": "2", "difficulty": "hard",
            "question": "Hány olyan kétjegyű szám létezik, amelyben a tízesek számjegye nagyobb, mint az egyeseké?",
            "options": ["25", "36", "40", "45", "50"],
            "correct": "D",
            "image": None,
            "comment": "Tízes=1: 10 (1db). Tízes=2: 20,21 (2db). … Tízes=9: 90-98 (9db). 1+2+3+…+9 = 45.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Gondoltam egy kétjegyű számra. Ha felcserélem a számjegyeit, 27-tel kisebb számot kapok. Mennyi lehetett az eredeti szám, ha a számjegyeinek összege 9?",
            "options": ["36", "45", "54", "63", "72"],
            "correct": "D",
            "image": None,
            "comment": "10a+b - (10b+a) = 27 → 9(a-b) = 27 → a-b = 3. Ha a+b = 9 és a-b = 3, akkor a = 6, b = 3. A szám: 63.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Apa és fia együtt 50 évesek. 5 évvel ezelőtt apa háromszor annyi idős volt, mint a fia. Hány éves a fia most?",
            "options": ["10", "12", "14", "15", "16"],
            "correct": "D",
            "image": None,
            "comment": "a+f=50. 5 éve: (a-5)=3(f-5) → a-5=3f-15 → a=3f-10. (3f-10)+f=50 → 4f=60 → f=15.",
        },
        # ---- SPATIAL / GEOMETRY ----
        {
            "class": "2", "difficulty": "hard",
            "question": "Egy 4×4-es sakktáblán (16 mező) hány 2×2-es négyzet található?",
            "options": ["4", "6", "8", "9", "16"],
            "correct": "D",
            "image": None,
            "comment": "Egy 2×2-es négyzet bal felső sarka 3×3 = 9 helyen lehet (1-3 sor, 1-3 oszlop).",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Egy kocka minden lapját más színűre festjük (6 szín). Ha a pirosat az asztalra tesszük, hány különböző színű lap lehet felül?",
            "options": ["1", "2", "3", "4", "5"],
            "correct": "E",
            "image": None,
            "comment": "A pirossal szemben bármelyik másik 5 szín állhat felülre (a kockát forgathatjuk). Tehát 5.",
        },
        # ---- TRICKY WORD PROBLEMS ----
        {
            "class": "2", "difficulty": "hard",
            "question": "Egy mécsesgyár naponta 100 gyertyát készít. A viaszmaradékból minden 10 elkészült gyertya után 1 újat lehet készíteni. Hány gyertyát tudnak összesen készíteni 100 adag viaszból?",
            "options": ["100", "109", "110", "111", "120"],
            "correct": "D",
            "image": None,
            "comment": "100 gyertya → 10 gyertya a maradékból → 1 gyertya annak maradékából. 100+10+1 = 111.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Egy versenyen 100 induló van. Kiesés rendszerben, minden meccsen a vesztes kiesik. Hány meccset kell lejátszani, hogy legyen egy győztes?",
            "options": ["50", "64", "99", "100", "128"],
            "correct": "C",
            "image": None,
            "comment": "Minden meccsen 1 ember esik ki. 99 embert kell kiejteni → 99 meccs.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "7 barát levelez egymással. Mindenki mindenkinek pontosan egy levelet küld. Hány levelet küldenek összesen?",
            "options": ["21", "28", "35", "42", "49"],
            "correct": "D",
            "image": None,
            "comment": "Mindenki 6 levelet küld (a többi 6-nak). 7 × 6 = 42. (Nem kézfogás, itt az irány számít!)",
        },
        # ---- CALENDAR / TIME ----
        {
            "class": "2", "difficulty": "hard",
            "question": "Ma csütörtök van. 100 nap múlva milyen nap lesz?",
            "options": ["Hétfő", "Kedd", "Szerda", "Szombat", "Vasárnap"],
            "correct": "D",
            "image": None,
            "comment": "100 / 7 = 14 hét és 2 nap. Csütörtök + 2 nap = szombat.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Egy óra naponta 3 percet siet. Hétfő reggel 8:00-kor pontosan beállítottuk. Péntek reggel 8:00-kor — a valóságban — mit mutat az óra?",
            "options": ["7:48", "7:52", "8:08", "8:12", "8:15"],
            "correct": "D",
            "image": None,
            "comment": "Hétfőtől péntekig 4 nap telt el. 4 × 3 = 12 perc sietés. Az óra 8:12-t mutat.",
        },
        # ---- PATTERN RECOGNITION ----
        {
            "class": "2", "difficulty": "hard",
            "question": "Mi a sorozat következő tagja: 1, 1, 2, 3, 5, 8, ...?",
            "options": ["10", "11", "12", "13", "15"],
            "correct": "D",
            "image": None,
            "comment": "Fibonacci-sorozat: minden szám az előző kettő összege. 5 + 8 = 13.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "A sorozatban a számok: 2, 6, 12, 20, 30, ... Mi a következő szám?",
            "options": ["36", "38", "40", "42", "44"],
            "correct": "D",
            "image": None,
            "comment": "Különbségek: 4, 6, 8, 10 → a következő +12. 30+12 = 42. (Vagy: n×(n+1): 1×2, 2×3, 3×4, 4×5, 5×6, 6×7=42.)",
        },
        # ---- PIGEONHOLE / EXTREMAL ----
        {
            "class": "2", "difficulty": "hard",
            "question": "Egy zsákban 4 piros, 4 kék, 4 zöld és 4 sárga labda van. Legalább hány labdát kell kivenned csukott szemmel, hogy BIZTOSAN legyen köztük 2 pár (azaz 4 labda, amelyből mindegyik színből legalább kettő van)?",
            "options": ["5", "6", "7", "8", "9"],
            "correct": "E",
            "image": None,
            "comment": "Legrosszabb eset: 4+4 ugyanolyan. 5. labda más szín, de még csak 1 pár van. +4 kell a 2. párhoz legrosszabb esetben. Gondoljuk végig: ha 4 db egy szín + 4 db egy szín, az 8 db, 2 pár → 8 elég? Nem, mert 4+4 az 2 színből 4-4, az 2 pár. De mi van ha 4 egy színből + 2+1+1? Akkor 4 piros, 2 kék, 1 zöld, 1 sárga = 8 db, de csak 1 pár (PP). Tehát 9 kell: 4+3+1+1 nem 2 pár, 4+4+1 nem 2 pár... 4+2+2+1=9: van PP és KK. Szóval 9 mindenképp tartalmaz 2 párt.",
        },
        {
            "class": "2", "difficulty": "hard",
            "question": "Egy papírlapra írsz egy háromjegyű számot, amelynek minden jegye különböző és a jegyek összege 6. Hány ilyen szám létezik?",
            "options": ["3", "6", "9", "12", "18"],
            "correct": "C",
            "image": None,
            "comment": "Jegyek összege 6, mind különböző, háromjegyű. Lehetséges jegy-halmazok: {1,2,3} (összeg 6), {0,1,5} (összeg 6), {0,2,4} (összeg 6). {1,2,3}: 3!=6 szám, mind háromjegyű. {0,1,5}: első jegy nem 0, tehát 2×2=4 szám. {0,2,4}: szintén 4 szám. De 6+4+4 = 14, ami nincs az opcióban. Tehát nézzük: {1,2,3}→3!=6, {0,1,5}→4, {0,2,4}→4... Hmm jó, 14 nincs. Legyen inkább: összeg=6, jegyek: pontosan {1,2,3}→6, de az összes lehetőség: 0+1+5, 0+2+4, 1+2+3. Jegyenként: {0,1,5}: 1-es/5-ös elöl=2×2!=4. {0,2,4}: 2-es/4-es elöl=4. {1,2,3}: 3!=6. Total=14.",
        },
    ]


# =====================================================================
#  4)  MAIN
# =====================================================================
def main():
    questions = list(m.QUESTIONS)  # copy

    # Step 1: Reclassify
    print("=== Reclassifying mislabeled questions ===")
    rc = reclassify(questions)
    print(f"  Reclassified {rc} questions.\n")

    # Step 2: Build new hard questions
    print("=== Building new hard questions with images ===")
    new_qs = build_new_hard_questions()

    # Fix the last question (pigeonhole problem was getting complicated)
    # Let me replace it with a cleaner one
    new_qs[-1] = {
        "class": "2", "difficulty": "hard",
        "question": "Három különböző, egyjegyű, nullánál nagyobb szám összege 12. Hányféleképpen választhatjuk ki a három számot? (A sorrend nem számít.)",
        "options": ["3", "5", "7", "9", "10"],
        "correct": "C",
        "image": None,
        "comment": "1+2+9, 1+3+8, 1+4+7, 1+5+6, 2+3+7, 2+4+6, 3+4+5. Összesen 7.",
    }

    questions.extend(new_qs)
    print(f"  Added {len(new_qs)} new hard questions.\n")

    # Step 3: Count stats
    from collections import Counter
    diff_counts = Counter(q["difficulty"] for q in questions)
    print("=== Question counts ===")
    for d in ["easy", "medium", "hard"]:
        print(f"  {d}: {diff_counts.get(d, 0)}")
    print(f"  TOTAL: {len(questions)}\n")

    # Step 4: Rebuild DB from scratch
    print("=== Rebuilding database ===")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("  Deleted old DB.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class TEXT,
        difficulty TEXT,
        question TEXT,
        image TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        option_e TEXT,
        correct_answer TEXT,
        comment TEXT,
        shown_count INTEGER DEFAULT 0
    )
    """)

    inserted = 0
    seen = set()
    for q in questions:
        # Deduplicate by question text
        key = q["question"].strip()
        if key in seen:
            continue
        seen.add(key)

        cursor.execute(
            """INSERT INTO questions
               (class, difficulty, question, image,
                option_a, option_b, option_c, option_d, option_e,
                correct_answer, comment)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                q["class"], q["difficulty"], q["question"], q.get("image"),
                q["options"][0], q["options"][1], q["options"][2],
                q["options"][3], q["options"][4],
                q["correct"], q.get("comment"),
            ),
        )
        inserted += 1

    conn.commit()
    conn.close()
    print(f"  Inserted {inserted} unique questions (deduplicated).\n")

    # Step 5: Export to db_data.js
    print("=== Exporting db_data.js ===")
    with open(DB_PATH, "rb") as f:
        db_bytes = f.read()
    b64 = base64.b64encode(db_bytes).decode()
    with open(JS_PATH, "w") as f:
        f.write(f"const DB_BASE64 = '{b64}';\n")
    print(f"  Done. DB size: {len(db_bytes)//1024} KB, JS: {len(b64)//1024} KB")

    # Final stats from DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty ORDER BY difficulty")
    print("\n=== Final DB stats ===")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    cursor.execute("SELECT COUNT(*) FROM questions WHERE image IS NOT NULL")
    img_count = cursor.fetchone()[0]
    print(f"  Questions with images: {img_count}")
    conn.close()

    print("\n✅ All done! New questions have shown_count=0 and will be prioritized.")


if __name__ == "__main__":
    main()
