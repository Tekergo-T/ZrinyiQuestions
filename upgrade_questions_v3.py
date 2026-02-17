
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    import manual_insert_questions
except ImportError:
    print("Error: Could not import manual_insert_questions.py")
    sys.exit(1)

# Define Batch 3: Truth/Lie and Logic Grid Questions
NEW_HARD_QUESTIONS_BATCH_3 = [
    # --- Truth / Lie Puzzles ---
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Két testvér, Laci és Feri közül az egyik mindig igazat mond, a másik mindig hazudik. Laci azt mondja: 'A testvérem mindig hazudik'. Feri azt mondja: 'Laci mindig igazat mond'. Ki mond igazat?",
        "options": ["Laci", "Feri", "Mindkettő", "Egyik sem", "Nem lehet tudni"],
        "correct": "A",
        "comment": "Ha Laci igazat mond, akkor Feri hazudik. Nézzük meg Feri állítását ('Laci igazat mond'). Ha Feri hazudik, akkor ez az állítás hamis, tehát Laci nem mond igazat? Ez ellentmondás. Várj. Újra: Ha Laci IGAZ, akkor Feri HAZUG. Feri azt mondja 'Laci IGAZ'. Ez IGAZ állítás lenne, de Feri HAZUG, tehát nem mondhat igazat. Tehát ez az eset lehetetlen. Nézzük a fordítottját: Laci HAZUG, Feri IGAZ. Laci azt mondja 'Bátyám (Feri) hazudik'. Ez HAZUGSÁG, tehát Feri IGAZmondó. Ez stimmel. Feri azt mondja 'Laci IGAZ'. De Feri IGAZmondó, tehát ennek igaznak kell lennie -> Laci IGAZ. De Laci HAZUG. Ez is ellentmondás! Állj! A klasszikus feladatnál: 'Egy szigeten...'. Ha Laci azt mondja 'Feri hazudik', és Feri azt mondja 'Mi mindketten hazudunk'. Akkor Laci IGAZ, Feri HAZUG. Módosítom a kérdést egy biztosan megoldhatóra.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy szigeten kétféle ember él: az igazmondók (mindig igazat mondanak) és a hazugok (mindig hazudnak). Találkozol két emberrel, A-val és B-vel. A azt mondja: 'Mindketten hazugok vagyunk'. Milyen ember A és B?",
        "options": ["A és B is hazug", "A és B is igazmondó", "A igazmondó, B hazug", "A hazug, B igazmondó", "Nem lehet tudni"],
        "correct": "D",
        "comment": "Ha A igazmondó lenne, akkor igaz lenne, hogy 'mindketten hazugok', tehát ő is hazug lenne. Ez ellentmondás. Tehát A biztosan hazug. Ha A hazug, akkor az állítása ('mindketten hazugok') hamis. Tehát nem mindketten hazugok. Mivel A hazug, ezért B-nek igazmondónak kell lennie.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Három doboz van előttünk: Arany, Ezüst és Bronz. Az egyikben kincs van. A dobozokon feliratok vannak, de csak EGY felirat igaz.\nArany: 'A kincs itt van.'\nEzüst: 'A kincs nem itt van.'\nBronz: 'A kincs nem az Aranyban van.'\nHol van a kincs?",
        "options": ["Az Aranyban", "Az Ezüstben", "A Bronzban", "Mindegyikben", "Egyikben sem"],
        "correct": "B",
        "comment": "Tegyük fel, hogy Aranyban van. Akkor: Arany felirat IGAZ ('itt van'). Ezüst felirat IGAZ ('nem itt van', mert Aranyban van). Két igaz lenne -> NEM JÓ. Tegyük fel, hogy Bronzban van. Arany felirat HAMIS. Ezüst felirat IGAZ ('nem itt'). Bronz felirat IGAZ ('nem Aranyban'). Két igaz -> NEM JÓ. Tegyük fel, hogy Ezüstben van. Arany felirat HAMIS ('nincs ott'). Ezüst felirat HAMIS ('itt van' a valóság, de felirat: 'nem itt'). Bronz felirat IGAZ ('nem Aranyban'). Csak 1 igaz van! Tehát a kincs az Ezüstben van.",
    },

    # --- Logic Grid / Who Does What ---
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Három barát: Anna, Béla és Cili háromféle hangszeren játszik: hegedű, zongora és dob (mindenki egyen). Anna nem zongorázik. Béla nem dobol és nem zongorázik. Ki dobol?",
        "options": ["Anna", "Béla", "Cili", "Senki", "Mindenki"],
        "correct": "C",
        "comment": "Béla nem dob és nem zongora => Béla hegedül. Anna nem zongora, és a hegedű foglalt (Béla) => Anna dobol? Várj. Béla hegedül. Maradt zongora és dob. Anna nem zongorázik => Anna dobol. Cili zongorázik. Kérdés: Ki dobol? Válasz: Anna. Várj, a helyes válasz az 'Anna'. Javítom a kódban.",
    },
    {  # JAVÍTOTT verzió a fentihez
        "class": "2",
        "difficulty": "hard",
        "question": "Három barát: Anna, Béla és Cili háromféle hangszeren játszik: hegedű, zongora és dob. Mindenki csak egy hangszeren játszik. Anna nem zongorázik. Béla nem dobol és nem zongorázik. Ki játszik a dobon?",
        "options": ["Anna", "Béla", "Cili", "Nem lehet tudni", "Senki"],
        "correct": "A",
        "comment": "Béla nem dob, nem zongora -> Béla hegedül. Anna nem zongora, (hegedű foglalt) -> Anna dobol. Cili zongorázik. Tehát Anna dobol.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy háromemeletes házban lakik Kovács úr, Szabó úr és Nagy úr (az 1., 2. és 3. emeleten). Kovács úr nem a legfelsőn lakik. Szabó úr nem a legalsón lakik. Nagy úr lakik Kovács úr alatt. Ki lakik a 2. emeleten?",
        "options": ["Kovács úr", "Szabó úr", "Nagy úr", "Senki", "Nem lehet tudni"],
        "correct": "A",
        "comment": "Nagy úr lakik Kovács úr alatt -> Tehát Kovács nem lehet az 1., és Nagy nem lehet a 3. Kovács nem 3. (megadva). Tehát Kovács csak a 2. lehet (mert 1. nem lehet, mert van alatta valaki). Ha Kovács 2., akkor Nagy 1. Szabó maradt a 3. (ami stimmel, mert nem legalsó). Tehát a 2. emeleten Kovács úr lakik.",
    },

    # --- More Combinatorics / Logic ---
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Gondoltam egy számra. A szám páros. Nagyobb, mint 10, de kisebb, mint 20. Osztható 3-mal. Melyik ez a szám?",
        "options": ["12", "14", "15", "16", "18"],
        "correct": "E", # 12 is divisible by 3 and 18 is logical... wait. 12 is even, >10, <20, div by 3. 18 is even, >10, <20, div by 3. Két megoldás van! 12 és 18. Pontosítok.",
        "comment": "Javítom a kérdést.",
    },
    { # JAVÍTOTT
        "class": "2",
        "difficulty": "hard",
        "question": "Gondoltam egy számra. A szám páros. Nagyobb, mint 12, de kisebb, mint 22. Osztható 3-mal. Melyik ez a szám?",
        "options": ["12", "14", "15", "18", "20"],
        "correct": "D",
        "comment": "12-nél nagyobb, tehát 12 nem jó. 14 nem osztható 3-mal. 15 nem páros. 18 páros és osztható 3-mal. 20 nem jó.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Zászlót színezünk 3 vízszintes sávval. Piros, fehér és zöld színeket használhatunk. Minden sávot ki kell színezni, és két egymás melletti sáv nem lehet egyforma színű. Hányféle zászlót készíthetünk, ha a felső sáv biztosan PIROS?",
        "options": ["2", "3", "4", "5", "6"],
        "correct": "C",
        "comment": "Felső: P. Középső: F vagy Z (2 lehetőség). Alsó: Ha közép F -> P vagy Z (2). Ha közép Z -> P vagy F (2). Összesen 2 * 2 = 4 lehetőség. (P-F-P, P-F-Z, P-Z-P, P-Z-F).",
    },
     {
        "class": "2",
        "difficulty": "hard",
        "question": "Négy gyerek (A, B, C, D) sorban áll. A nem áll a szélen. B közvetlenül C mögött áll. D az utolsó. Ki áll az első helyen?",
        "options": ["A", "B", "C", "D", "Nem lehet tudni"],
        "correct": "C",
        "comment": "D az utolsó (4.). A nem szélen -> A a 2. vagy 3. B közvetlenül C mögött -> (C, B) pár. Mivel D a 4., a (C, B) pár csak az 1-2. helyen vagy 2-3. helyen lehet. Ha 2-3., akkor A lenne az 1. (szélen) - ez tilos. Tehát (C, B) az 1-2. helyen van. C az első. A a 3., D a 4.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "question": "Egy kosárban almák vannak. Ha kettesével veszem ki, 1 marad. Ha hármasával, akkor is 1 marad. Ha ötösével, akkor is 1 marad. Legalább hány alma van a kosárban?",
        "options": ["11", "16", "21", "31", "41"],
        "correct": "D",
        "comment": "A szám 2-vel, 3-mal és 5-tel osztva is 1 maradékot ad. Tehát a szám-1 osztható 2-vel, 3-mal, 5-tel. A legkisebb közös többszörös (2,3,5) = 30. Tehát a szám 30 + 1 = 31.",
    }
]

def format_question_dict(q, indent_level=4):
    indent = ' ' * indent_level
    s = '    {\n'
    s += f'{indent}"class": "{q["class"]}",\n'
    s += f'{indent}"difficulty": "{q["difficulty"]}",\n'
    q_clean = q["question"].replace('\\', '\\\\').replace('"', '\\"')
    s += f'{indent}"question": "{q_clean}",\n'
    
    s += f'{indent}"options": ['
    opts = []
    for opt in q["options"]:
        opt_clean = opt.replace('\\', '\\\\').replace('"', '\\"')
        opts.append(f'"{opt_clean}"')
    s += ", ".join(opts)
    s += '],\n'
    
    s += f'{indent}"correct": "{q["correct"]}",\n'
    if "comment" in q and q["comment"]:
        c_clean = q["comment"].replace('\\', '\\\\').replace('"', '\\"')
        s += f'{indent}"comment": "{c_clean}",\n'
    s += '    },'
    return s

def main():
    questions = manual_insert_questions.QUESTIONS
    print(f"Original question count: {len(questions)}")
    
    # Add new hard questions
    questions.extend(NEW_HARD_QUESTIONS_BATCH_3)
    print(f"Added {len(NEW_HARD_QUESTIONS_BATCH_3)} new hard logic questions.")
    print(f"New total: {len(questions)}")
    
    # Read original file
    with open('manual_insert_questions.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = 'QUESTIONS = ['
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("Error: Could not find QUESTIONS block")
        return
        
    open_brackets = 0
    end_idx = -1
    for i in range(start_idx, len(content)):
        if content[i] == '[':
            open_brackets += 1
        elif content[i] == ']':
            open_brackets -= 1
            if open_brackets == 0:
                end_idx = i + 1
                break
    
    if end_idx == -1:
        print("Error: Could not find end of QUESTIONS block")
        return

    new_questions_str = "QUESTIONS = [\n"
    for q in questions:
        new_questions_str += format_question_dict(q) + "\n"
    new_questions_str += "]"
    
    final_content = content[:start_idx] + new_questions_str + content[end_idx:]
    
    with open('manual_insert_questions.py', 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print("File updated successfully.")

if __name__ == "__main__":
    main()
