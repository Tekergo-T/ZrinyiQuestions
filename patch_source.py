#!/usr/bin/env python3
"""
Patch manual_insert_questions.py IN-PLACE:
1. Reclassify mislabeled 'hard' questions by finding their unique question text
2. Append 20 new genuinely hard questions to the QUESTIONS list
3. Re-run the main() to rebuild the database
"""
import re

SRC = "manual_insert_questions.py"

# ── 1) RECLASSIFICATIONS: unique question substring → new difficulty ──
RECLASS = {
    "Egy dobozban kék és zöld golyók vannak. A kékből 12": "easy",
    "A táblán 4 piros és 4 kék kréta van": "easy",
    "Egy edénybe 5 liter víz fér": "easy",
    "Három testvér összesen 24 éves. A legidősebb 10": "easy",
    "A létrán 12 fok van. Jani felment a közepéig": "easy",
    "Egy kétjegyű szám 19. Ha felcseréljük": "easy",
    "A dobókocka szemközti oldalain lévő pöttyök összege mindig 7": "easy",
    "Egy film 2 perc 30 másodpercig tart": "medium",
    "Egy könyv 4. oldalától a 10. oldaláig": "medium",
    "Egy szám felét és negyedét összeadjuk": "medium",
    "Hány vágással tudunk egy rudat 6 darabra": "medium",
    "Egy karkötőt fűzöl. Minden 3. gyöngy piros": "medium",
    "Melyik szám következik a sorozatban: 3, 6, 12, 24": "medium",
    "Hány darab 1-es számjegyet kell leírnunk összesen 1-től 30": "medium",
}

# ── 2) 20 NEW HARD QUESTIONS ──
NEW_QUESTIONS_TEXT = '''    {
        "class": "2",
        "difficulty": "hard",
        "question": "Három szín közül választhatsz: piros, kék, zöld. Egy háromszög mindhárom oldalát ki szeretnéd festeni, de a szomszédos oldalak nem lehetnek ugyanolyan színűek. Hányféleképpen teheted meg?",
        "options": ["3", "6", "9", "12", "18"],
        "correct": "B",
        "comment": "Az 1. oldal 3-féle, a 2. oldal 2-féle (nem ugyanaz), a 3. oldal 1-féle (nem az 1. és nem a 2. színű). 3×2×1 = 6.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "A mérleg mindkétszer egyensúlyban van. 3 alma nyom annyit, mint 6 eper. 1 alma és 2 eper nyom annyit, mint 1 körte. Hány szem eper nyom annyit, mint 1 körte?",
        "options": ["2", "3", "4", "5", "6"],
        "correct": "C",
        "comment": "3 alma = 6 eper → 1 alma = 2 eper. 1 alma + 2 eper = 1 körte → 2+2 = 4 eper = 1 körte.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Két szám összege 50, különbségük 10. Melyik a nagyobb szám?",
        "options": ["20", "25", "28", "30", "35"],
        "correct": "D",
        "comment": "Ha a kisebb szám x, akkor x + (x+10) = 50 → 2x = 40 → x = 20. A nagyobb: 30.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Hány olyan kétjegyű szám létezik, amelyben a tízesek számjegye nagyobb, mint az egyeseké?",
        "options": ["25", "36", "40", "45", "50"],
        "correct": "D",
        "comment": "Tízes=1: 10 (1db). Tízes=2: 20,21 (2db). … Tízes=9: 90-98 (9db). 1+2+3+…+9 = 45.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Gondoltam egy kétjegyű számra. Ha felcserélem a számjegyeit, 27-tel kisebb számot kapok. Mennyi lehetett az eredeti szám, ha a számjegyeinek összege 9?",
        "options": ["36", "45", "54", "63", "72"],
        "correct": "D",
        "comment": "10a+b - (10b+a) = 27 → 9(a-b) = 27 → a-b = 3. Ha a+b = 9 és a-b = 3, akkor a = 6, b = 3. A szám: 63.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Apa és fia együtt 50 évesek. 5 évvel ezelőtt apa háromszor annyi idős volt, mint a fia. Hány éves a fia most?",
        "options": ["10", "12", "14", "15", "16"],
        "correct": "D",
        "comment": "a+f=50. 5 éve: (a-5)=3(f-5) → a-5=3f-15 → a=3f-10. (3f-10)+f=50 → 4f=60 → f=15.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy 4×4-es sakktáblán (16 mező) hány 2×2-es négyzet található?",
        "options": ["4", "6", "8", "9", "16"],
        "correct": "D",
        "comment": "Egy 2×2-es négyzet bal felső sarka 3×3 = 9 helyen lehet (1-3 sor, 1-3 oszlop).",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy kocka minden lapját más színűre festjük (6 szín). Ha a pirosat az asztalra tesszük, hány különböző színű lap lehet felül?",
        "options": ["1", "2", "3", "4", "5"],
        "correct": "E",
        "comment": "A pirossal szemben bármelyik másik 5 szín állhat felülre (a kockát forgathatjuk). Tehát 5.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy mécsesgyár naponta 100 gyertyát készít. A viaszmaradékból minden 10 elkészült gyertya után 1 újat lehet önteni. A maradékok maradékából is készíthető gyertya. Hány gyertyát tudnak összesen készíteni 100 adag viaszból?",
        "options": ["100", "109", "110", "111", "120"],
        "correct": "D",
        "comment": "100 gyertya → 10 gyertya a maradékból → 1 gyertya annak maradékából. 100+10+1 = 111.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy versenyen 100 induló van. Kiesés rendszerben, minden meccsen a vesztes kiesik. Hány meccset kell lejátszani, hogy legyen egy győztes?",
        "options": ["50", "64", "99", "100", "128"],
        "correct": "C",
        "comment": "Minden meccsen 1 ember esik ki. 99 embert kell kiejteni → 99 meccs.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "7 barát levelez egymással. Mindenki mindenkinek pontosan egy levelet küld. Hány levelet küldenek összesen?",
        "options": ["21", "28", "35", "42", "49"],
        "correct": "D",
        "comment": "Mindenki 6 levelet küld (a többi 6-nak). 7 × 6 = 42. (Nem kézfogás — a leveleknél az irány is számít!)",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Ma csütörtök van. 100 nap múlva milyen nap lesz?",
        "options": ["Hétfő", "Kedd", "Szerda", "Szombat", "Vasárnap"],
        "correct": "D",
        "comment": "100 / 7 = 14 hét és 2 nap. Csütörtök + 2 nap = szombat.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy óra naponta 3 percet siet. Hétfő reggel 8:00-kor pontosan beállítottuk. Péntek reggel 8:00-kor — a valóságban — mit mutat az óra?",
        "options": ["7:48", "7:52", "8:08", "8:12", "8:15"],
        "correct": "D",
        "comment": "Hétfőtől péntekig 4 nap telt el. 4 × 3 = 12 perc sietés. Az óra 8:12-t mutat.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Mi a sorozat következő tagja: 1, 1, 2, 3, 5, 8, ...?",
        "options": ["10", "11", "12", "13", "15"],
        "correct": "D",
        "comment": "Fibonacci-sorozat: minden szám az előző kettő összege. 5 + 8 = 13.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "A sorozatban a számok: 2, 6, 12, 20, 30, ... Mi a következő szám?",
        "options": ["36", "38", "40", "42", "44"],
        "correct": "D",
        "comment": "Különbségek: 4, 6, 8, 10 → a következő +12. 30+12 = 42. (Vagy: n×(n+1): 1×2, 2×3, 3×4, 4×5, 5×6, 6×7=42.)",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Három különböző, egyjegyű, nullánál nagyobb szám összege 12. Hányféleképpen választhatjuk ki a három számot? (A sorrend nem számít.)",
        "options": ["3", "5", "7", "9", "10"],
        "correct": "C",
        "comment": "1+2+9, 1+3+8, 1+4+7, 1+5+6, 2+3+7, 2+4+6, 3+4+5. Összesen 7.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy zsákban 4 piros, 4 kék, 4 zöld és 4 sárga labda van. Legalább hány labdát kell kivenned csukott szemmel, hogy biztosan legyen köztük legalább 2 azonos színű pár (azaz legalább 2 szín, amelyből 2-2 darab van)?",
        "options": ["5", "6", "7", "8", "9"],
        "correct": "E",
        "comment": "Legrosszabb eset: 4 db egy színből + 2+1+1 másokból = 8 labda, de abból csak 1 pár. A 9. labda biztosítja a 2. párt is.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy 3×3-as rácson az S pontból a C pontba kell eljutnod, de csak jobbra (→) vagy lefelé (↓) léphetsz. Hányféleképpen tudsz eljutni S-ből C-be?",
        "options": ["6", "10", "15", "20", "24"],
        "correct": "D",
        "comment": "3 jobbra + 3 lefelé lépés kell. Ezek sorrendje: 6!/(3!×3!) = 20.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy papírlapra írsz egy háromjegyű számot. Minden jegye különböző, és a jegyek összege 6. Hány ilyen háromjegyű szám létezik?",
        "options": ["6", "10", "12", "14", "18"],
        "correct": "D",
        "comment": "Jegy-halmazok: {1,2,3}→6db, {0,1,5}→4db (0 nem lehet az első), {0,2,4}→4db. Összesen 6+4+4 = 14.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy 4×4-es rácsban fekete és fehér golyók vannak. Legkevesebb hány golyó színét kell megváltoztatni, hogy MINDEN sorban és MINDEN oszlopban pontosan 2 fekete golyó legyen, ha jelenleg az 1. sorban 3, a 2. sorban 2, a 3. sorban 2, a 4. sorban 1 fekete golyó van?",
        "options": ["1", "2", "3", "4", "5"],
        "correct": "A",
        "comment": "Az 1. sorból 1-et fehérre cserélünk úgy, hogy az a 4. sor oszlopába essen → mindkét sor rendben lesz. 1 csere elég.",
    },
'''

def main():
    with open(SRC, "r", encoding="utf-8") as f:
        content = f.read()

    # ── Step 1: Reclassify ──
    changed = 0
    for q_substr, new_diff in RECLASS.items():
        # Find the question text in the file
        idx = content.find(q_substr)
        if idx == -1:
            print(f"  ⚠ NOT FOUND: {q_substr[:50]}…")
            continue

        # Find the nearest preceding "difficulty": "hard" line
        # Search backwards from the question text position
        search_region = content[max(0, idx - 200):idx]
        # Find the last occurrence of "difficulty": "hard" before this question
        pattern = r'"difficulty":\s*"hard"'
        matches = list(re.finditer(pattern, search_region))
        if not matches:
            print(f"  ⚠ No 'hard' before: {q_substr[:50]}…")
            continue

        last_match = matches[-1]
        abs_start = max(0, idx - 200) + last_match.start()
        abs_end = max(0, idx - 200) + last_match.end()

        old_text = content[abs_start:abs_end]
        new_text = f'"difficulty": "{new_diff}"'
        content = content[:abs_start] + new_text + content[abs_end:]
        changed += 1
        print(f"  ✓ hard→{new_diff}: {q_substr[:60]}…")

    print(f"\n  Reclassified {changed} questions.\n")

    # ── Step 2: Append new questions ──
    # Find the closing ']' of the QUESTIONS list
    # It's the last ']' before 'def main'
    main_idx = content.find("\ndef main(")
    if main_idx == -1:
        main_idx = content.find("\ndef main(")
    
    # Find the last ']' before main()
    bracket_idx = content.rfind("]", 0, main_idx)
    if bracket_idx == -1:
        print("ERROR: Could not find closing ']' of QUESTIONS list!")
        return

    # Insert new questions before the ']'
    # First check: remove trailing whitespace/newlines before ']'
    insert_point = bracket_idx
    new_block = "\n    # --- 20 NEW GENUINELY HARD COMPETITION QUESTIONS ---\n" + NEW_QUESTIONS_TEXT
    content = content[:insert_point] + new_block + content[insert_point:]
    print(f"  Added 20 new hard questions before closing ']'.\n")

    # ── Step 3: Write back ──
    with open(SRC, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {SRC} updated in-place!\n")

    # ── Step 4: Count questions ──
    easy = content.count('"difficulty": "easy"')
    medium = content.count('"difficulty": "medium"')
    hard = content.count('"difficulty": "hard"')
    print(f"  easy: {easy}, medium: {medium}, hard: {hard}, total: {easy+medium+hard}")


if __name__ == "__main__":
    main()
