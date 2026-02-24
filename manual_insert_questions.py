import sqlite3
import os
import base64

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "zrinyi_questions.db"
)
JS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_data.js")

# Manually curated high-quality logic questions
QUESTIONS = [
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "C",
        "options": ["0", "1", "2", "3", "A gondolt szám felét"],
        "question": "Gondolj egy számra. Szorzod 3-mal. Hozzáadsz 6-ot. Elosztod 3-mal. Kivonod az eredeti számot. Mit kapsz mindig?",
        "comment": "Legyen a szám x. ((x*3)+6)/3 - x = (3x+6)/3 - x = x+2 - x = 2. Mindig 2-t kapsz.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "D",
        "options": [
            "Nem lehet megoldani",
            "1 kapcsoló fel, bemegyek",
            "2 kapcsoló fel, bemegyek",
            "1-et felkapcsolok pár percre, lekapcsolom, másikat felkapcsolom, bemegyek",
            "Véletlenszerű próbálgatás",
        ],
        "question": "Egy szobában 3 lámpa van. Kint 3 kapcsoló. Egyszer mehetsz be a szobába. Hogyan tudod biztosan megállapítani, melyik kapcsoló melyik lámpához tartozik?",
        "comment": "Egyet felkapcsolsz, vársz → az felmelegszik. Leoltod, másikat felkapcsolsz, bemész: Ami ég → második. Ami meleg, de nem ég → első. Ami hideg → harmadik.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "D",
        "options": ["Anna", "Béla", "Csaba", "Dóra", "Endre"],
        "question": "Öten állnak sorban. Anna az első. Endre Anna mögött áll. Dóra Endre mögött áll. Csaba Dóra mögött áll. Béla az utolsó. Ki áll középen?",
        "comment": "A sorrend: Anna – Endre – Dóra – Csaba – Béla. A középső helyen Dóra áll.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "C",
        "options": ["Pista", "Béla", "Cili", "Nem dönthető el", "Mind egyforma"],
        "question": "Pista magasabb, mint Béla. Béla magasabb, mint Cili. Ki a legalacsonyabb?",
        "comment": "Ha P > B és B > C, akkor C a legkisebb.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "C",
        "options": ["2", "3", "4", "6", "8"],
        "question": "2 ember 2 perc alatt megy át. 4 ember mennyi idő alatt megy át, ha egyszerre csak ketten mehetnek, és mindenki ugyanannyi idő alatt megy át?",
        "comment": "Első két ember: 2 perc. Második két ember: még 2 perc. Összesen 4 perc.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "A",
        "options": [
            "Igen",
            "Nem",
            "Csak szerencsével",
            "Csak ha tudjuk, hogy nehezebb",
            "Csak páros számnál",
        ],
        "question": "Van 8 érme, 1 hamis (könnyebb). Kétszer mérhetsz kétkarú mérlegen. Megtalálható biztosan?",
        "comment": "Első mérés: 3 vs 3. Ha egyenlő → a hamis a maradék 2 között van. Ha nem egyenlő → a könnyebb oldalon van a hamis a 3 közül. Második mérés: 1 vs 1 → kiderül.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "B",
        "options": ["0", "2", "3", "5", "Nem lehet tudni"],
        "question": "Ég 5 gyertya. Kettőt elfújunk. Hány gyertya marad végül?",
        "comment": "A három ég tovább, és leég. A kettő, amit elfújtunk, megmarad.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "B",
        "options": ["8", "10", "12", "14", "16"],
        "question": "Anna – 8 perc, Béla – 6 perc, Cili – 4 perc. 2 asztal van. Mi a legrövidebb idő, hogy mindhárman végezzenek?",
        "comment": "Első asztal: 8 perc. Második asztal: 6 perc → utána 4 perc. Teljes idő: 10 perc.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "C",
        "options": ["3", "4", "5", "6", "8"],
        "question": "Egy 4 fokos lépcsőn 1 vagy 2 lépcsőt lehet lépni egyszerre. Hányféleképpen lehet felmenni?",
        "comment": "Lehetséges sorrendek: 1-1-1-1, 1-1-2, 1-2-1, 2-1-1, 2-2. Összesen 5.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "C",
        "options": ["3", "4", "5", "6", "Soha"],
        "question": "5 gyerek ül körben. Minden percben mindenki átül a jobb oldalán lévő székre. Hány perc múlva ül mindenki újra a saját eredeti helyén?",
        "comment": "Minden percben mindenki eggyel arrébb megy. Ahhoz, hogy visszaérjen az eredeti helyére, teljes kört kell megtennie. 5 szék van → 5 lépés után lesz mindenki a helyén.",
    },
    {
        "class": "2",
        "difficulty": "hard",
        "correct": "A",
        "options": ["1", "2", "3", "4", "Nem lehet biztosan megoldani"],
        "question": "Három láda van: az egyikben csak alma, a másikban csak körte, a harmadikban vegyesen van gyümölcs. Mindhárom ládán rossz címke van. Egyetlen gyümölcsöt húzhatsz ki egyetlen ládából. Hány húzás biztosan elég a helyes címkézéshez?",
        "comment": "Ha a „Vegyes” feliratú ládából húzol, az biztosan nem vegyes. Amit húzol, az mutatja, mi van benne. Onnan a másik kettő már logikusan következik. Ezért 1 húzás elég.",
    },
    {
        "class": "2",
        "correct": "C",
        "difficulty": "medium",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Egy 36 darabos csokoládétáblát 4 gyerek között egyenlően osztunk szét. Hány kocka jut egy "
        "gyereknek?",
        "comment": "36 / 4 = 9, tehát egy gyerek 9 kockát kap.",
    },
    {
        "class": "2",
        "correct": "B",
        "difficulty": "medium",
        "options": [
            "1 csirke, 2 kutya",
            "2 csirke, 1 kutya",
            "3 csirke, 0 kutya",
            "0 csirke, 3 kutya",
            "1 csirke, 1 kutya",
        ],
        "question": "A baromfiudvarban csirkék és kutyák vannak. Összesen 3 fejük és 8 lábuk van. Hány csirke és hány "
        "kutya lehet?",
    },
    {
        "class": "2",
        "comment": "2 nyúl (8 láb) és 4 csirke (8 láb) összesen 6 fej és 16 láb. Tehát 2 nyúl van.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Az udvaron csirkék és nyulak vannak. Összesen 6 fejük és 16 lábuk van. Hány nyúl van?",
    },
    {
        "class": "2",
        "comment": "Két egymás melletti szám összege 21: x + (x+1) = 21 => 2x = 20 => x = 10.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["9", "10", "11", "12", "13"],
        "question": "Kinyitottam egy könyvet. A két egymás melletti látható oldalszám összege 21. Melyik a bal oldali "
        "szám?",
    },
    {
        "class": "2",
        "comment": "10 - 4 + 1 = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Egy könyv 4. oldalától a 10. oldaláig (a 4. és 10. oldalt is beleértve) hány oldalt olvastam el?",
    },
    {
        "class": "2",
        "comment": "3 lehetőség az első jegyre és 3 a másodikra: 3 * 3 = 9.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Hány kétjegyű szám írható fel csak az 1, 2 és 3 számjegyek segítségével, ha a számjegyek "
        "ismétlődhetnek?",
    },
    {
        "class": "2",
        "comment": "Egy négyzetet egy átló mentén kettévágva 2 háromszöget kapunk.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Hány háromszög látható az ábrán, ha egy négyzetet az egyik átlója mentén félbevágunk?",
    },
    {
        "class": "2",
        "comment": "Tegnap előtt péntek, tegnap szombat, ma vasárnap. Holnap hétfő lesz.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["Szombat", "Vasárnap", "Hétfő", "Kedd", "Szerda"],
        "question": "Tegnap előtt péntek volt. Milyen nap lesz holnap?",
    },
    {
        "class": "2",
        "comment": "Ha 2-t veszünk, lehet mindkettő kék. Ha 3-at veszünk, legalább egy piros biztosan lesz.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Egy kosárban piros és kék almák vannak. Legalább hány almát kell kivennünk csukott szemmel, hogy "
        "biztosan legyen köztük piros, ha 3 piros és 2 kék alma van?",
    },
    {
        "class": "2",
        "comment": "x + 5 = 2x - 4 => x = 9.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Gondoltam egy számra. Ha hozzáadok 5-öt, ugyanannyit kapok, mint ha a szám kétszereséből 4-et "
        "levonok. Melyik számra gondoltam?",
    },
    {
        "class": "2",
        "comment": "Előtte 7-en vannak, ő a 8.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["6.", "7.", "8.", "9.", "10."],
        "question": "Anna versenyezett. Előtte 7 gyerek futott be, mögötte 5 gyerek. Hányadik helyen végzett Anna?",
    },
    {
        "class": "2",
        "comment": "12 - 4 - 3 = 5.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["3", "4", "5", "6", "7"],
        "question": "Egy dobozban 12 csokoládé van. Zsuzsi megevett 4-et, Peti pedig 3-at. Hány maradt?",
    },
    {
        "class": "2",
        "comment": "Indulás: 7:30. 10 perc út, 10 perc vissza, 5 perc keresés, 25 perc út: 10+10+5+25 = 50 perc. 7:30 "
        "+ 50 perc = 8:20.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["8:00", "8:05", "8:10", "8:15", "8:20"],
        "question": "Anna 7:30-kor indul iskolába. 10 perc múlva visszafordul, 5 percig keres valamit, majd újra "
        "elindul. Innentől az út 25 percig tart. Mikor ér oda?",
    },
    {
        "class": "2",
        "comment": "x + 7 - 4 = 10 => x + 3 = 10 => x = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Péter gondolt egy számra, hozzáadott 7-et, majd elvett belőle 4-et és 10-et kapott. Melyik számra "
        "gondolt?",
    },
    {
        "class": "2",
        "comment": "Rosszabb esetben az első kettő különböző (piros, zöld). A harmadik biztosan vagy piros, vagy zöld "
        "lesz.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Öt alma közül 2 piros, 3 zöld. Legalább hány almát kell kivennem bekötött szemmel, hogy biztosan "
        "legyen köztük 2 egyforma színű?",
    },
    {
        "class": "2",
        "comment": "4 * 4 = 16.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["8", "12", "16", "20", "24"],
        "question": "Egy négyzet minden oldala 4 cm hosszú. Ha összeadjuk a négy oldal hosszát, hány centimétert "
        "kapunk?",
    },
    {
        "class": "2",
        "comment": "(28 + x) = 2 * (4 + x) => 28 + x = 8 + 2x => x = 20.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["16", "18", "20", "22", "24"],
        "question": "Anya 28 éves, lánya 4 éves. Hány év múlva lesz anya kétszer olyan idős, mint a lánya?",
    },
    {
        "class": "2",
        "comment": "Ha elölről a 4., akkor előtte 3-an, mögötte 6-an vannak. Hátulról nézve a 6 ember után ő a 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5.", "6.", "7.", "8.", "9."],
        "question": "Tíz gyerek sorban áll. Gabi elölről a 4. Hányadik ő hátulról?",
    },
    {
        "class": "2",
        "comment": "A kismutató 3 és 4 között, a nagymutató 6-on, ez 3 óra 30 perc.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["3:00", "3:30", "4:00", "4:30", "6:00"],
        "question": "Egy órán a kismutató a 3 és 4 között van, a nagymutató a 6-on. Hány óra van?",
    },
    {
        "class": "2",
        "comment": "Ha Karcsi a 8. és ő az utolsó, akkor összesen 8-an vannak.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["7", "8", "9", "14", "15"],
        "question": "Karcsi a sorban a 8. gyerek. Előtte 7-en állnak. Hány gyerek van összesen a sorban, ha Karcsi az "
        "utolsó?",
    },
    {
        "class": "2",
        "comment": "11 - 2 - 1 = 8 maradt. Mivel ugyanannyi maradt, mindkettőből 4-4 darab. Kezdetben fehér: 4 + 2 = "
        "6.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["5", "6", "7", "8", "9"],
        "question": "A táblán fehér és barna kréta volt, összesen 11. Elhasználtunk 2 fehéret és 1 barnát. Ezután "
        "ugyanannyi fehér maradt, mint barna. Hány fehér kréta volt kezdetben?",
    },
    {
        "class": "2",
        "comment": "3 + (2 * 3) = 3 + 6 = 9.",
        "correct": "E",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Feri 3 cukorkát evett meg délelőtt, délután kétszer annyit. Hány cukorkát evett összesen?",
    },
    {
        "class": "2",
        "comment": "2. Péter nyerte. 1. Mari vagy Péter. De minden játékban más, szóval 1.-t nem Péter (Péter a 2.-t "
        "nyerte) és nem Anna (megadott), tehát Mari.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Anna", "Péter", "Mari", "Nem volt győztes", "Nem lehet tudni"],
        "question": "Három gyerek (Anna, Péter, Mari) három játékot játszott. Minden játékban más nyert. Az elsőt nem "
        "Anna nyerte. A másodikat Péter nyerte. A harmadikat nem Mari nyerte. Ki nyerte az első játékot?",
    },
    {
        "class": "2",
        "comment": "50 - 15 - 20 = 15.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["10", "15", "20", "25", "30"],
        "question": "Anna könyvének 50 oldala van. Ma 15 oldalt, holnap 20-at olvas. Hány oldal marad még?",
    },
    {
        "class": "2",
        "comment": "x + 3x = 20 => 4x = 20 => x = 5. A nagyobb szám 3x = 15.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["5", "10", "12", "15", "18"],
        "question": "Két szám összege 20. Az egyik háromszor akkora, mint a másik. Melyik lehet a nagyobb szám?",
    },
    {
        "class": "2",
        "comment": "8:00 + 5 óra = 13:00.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["11:00", "12:00", "13:00", "14:00", "15:00"],
        "question": "Peti reggel 8 órakor ment iskolába, és 5 órát töltött ott. Hány órakor indult haza?",
    },
    {
        "class": "2",
        "comment": "x + (x+3) = 13 => 2x = 10 => x = 5. Kék golyók száma: 5 + 3 = 8.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Egy zacskóban piros és kék golyók vannak összesen 13. A kékek száma 3-mal több, mint a pirosaké. "
        "Hány kék golyó van?",
    },
    {
        "class": "2",
        "comment": "10 - 3 = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Mari 10 ceruzát vett. Ajándékozott belőlük 3-at. Hány ceruzája maradt?",
    },
    {
        "class": "2",
        "comment": "(x+2) + x + x = 14 => 3x = 12 => x = 4. A legtöbbet kapó: 4 + 2 = 6.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Az óvodában 14 kockát osztottak szét 3 gyerek között. Az egyik gyerek 2-vel többet kapott, mint a "
        "másik kettő (akik ugyanannyit kaptak). Hány kockát kapott a legtöbbet kapó gyerek?",
    },
    {
        "class": "2",
        "comment": "24 / 3 = 8.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Három barát összesen 24 almát gyűjtött. Ha mindenki egyforma mennyiséget szed, hány almát szedett "
        "egy-egy gyerek?",
    },
    {
        "class": "2",
        "comment": "9:00 + 3 óra = 12:00.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["11:00", "11:30", "12:00", "12:15", "12:30"],
        "question": "Egy vonat 9:00-kor indul, és 3 óra múlva érkezik meg. Mikor ér célba?",
    },
    {
        "class": "2",
        "comment": "50 - 20 = 30.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["20", "25", "30", "35", "40"],
        "question": "Egy könyvben 50 oldal van. Eddig 20 oldalt olvastam. Hány oldal van még hátra?",
    },
    {
        "class": "2",
        "comment": "18 / 3 = 6.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["3", "4", "5", "6", "7"],
        "question": "Pistának 18 golyója van, ami háromszor annyi, mint Lacának. Hány golyója van Lacának?",
    },
    {
        "class": "2",
        "comment": "(x+2) + x = 12 => 2x = 10 => x = 5. Lányok: 5 + 2 = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Egy csoportban 12 gyerek van. A lányok száma 2-vel több, mint a fiúké. Hány lány van?",
    },
    {
        "class": "2",
        "comment": "4 * 6 = 24.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["18 m", "20 m", "22 m", "24 m", "30 m"],
        "question": "Egy négyzetes kertet kerítünk körbe. Egy oldala 6 méter hosszú. Hány méter kerítés kell "
        "összesen?",
    },
    {
        "class": "2",
        "comment": "14 / 2 = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Egy szám kétszerese 14. Melyik ez a szám?",
    },
    {
        "class": "2",
        "comment": "50 - 25 = 25 perc.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["15", "20", "25", "30", "35"],
        "question": "Hány perccel később van 10:50, mint 10:25?",
    },
    {
        "class": "2",
        "comment": "30 - 5 = 25.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["20", "22", "25", "28", "30"],
        "question": "Apa 30 éves, a fia 5 éves. Hány évvel idősebb az apa a fiánál?",
    },
    {
        "class": "2",
        "comment": "5 + 6 = 11.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["4 és 7", "5 és 5", "5 és 6", "6 és 7", "7 és 8"],
        "question": "Két egymást követő szám összege 11. Melyik a két szám?",
    },
    {
        "class": "2",
        "comment": "49 / 7 = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Hány hét van 49 napban?",
    },
    {
        "class": "2",
        "comment": "2 * (5 + 10) = 30.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["20 cm", "25 cm", "30 cm", "35 cm", "40 cm"],
        "question": "Egy téglalap egyik oldala 5 cm, a másik oldala 10 cm. Mekkora a kerülete?",
    },
    {
        "class": "2",
        "comment": "100 - 40 - 25 = 35.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["25 Ft", "30 Ft", "35 Ft", "40 Ft", "45 Ft"],
        "question": "Eszter 100 Ft-ot kapott. Vett egy radírt 40 Ft-ért és egy ceruzát 25 Ft-ért. Mennyi pénze "
        "maradt?",
    },
    {
        "class": "2",
        "comment": "3 * 3 = 9.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Hány oldala van összesen három háromszögnek?",
    },
    {
        "class": "2",
        "comment": "20 * 3 = 60.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["40 km", "50 km", "60 km", "70 km", "80 km"],
        "question": "Egy autó 20 km-t tesz meg egy óra alatt. Mennyi utat tesz meg 3 óra alatt?",
    },
    {
        "class": "2",
        "comment": "5 - 3 = 2.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["1 liter", "1,5 liter", "2 liter", "2,5 liter", "3 liter"],
        "question": "Egy 5 literes kanna nincs tele. Ha még 3 litert beleöntünk, tele lesz. Mennyi víz volt benne "
        "előtte?",
    },
    {
        "class": "2",
        "comment": "8 - 3 = 5.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["3", "4", "5", "6", "7"],
        "question": "Egy torta 8 szeletre van vágva. Ha 3 szeletet megettem, hány szelet maradt?",
    },
    {
        "class": "2",
        "comment": "27 / 3 = 9.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Egy zacskóban ugyanannyi piros, kék és zöld golyó van. Összesen 27 golyó van a zacskóban. Hány "
        "piros golyó van?",
    },
    {
        "class": "2",
        "comment": "10 / 2 = 5.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["2 cm", "3 cm", "4 cm", "5 cm", "10 cm"],
        "question": "Egy 10 cm hosszú szalagot kettévágunk. Mekkora egy darab hossza?",
    },
    {
        "class": "2",
        "comment": "x + (x+4) = 20 => 2x = 16 => x = 8.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Anna és Béla együtt 20 éves. Anna 4 évvel fiatalabb, mint Béla. Hány éves Anna?",
    },
    {
        "class": "2",
        "comment": "24 / 6 = 4.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Egy dobozban 24 szem cukorka van. Elosztjuk 6 gyerek között egyenlően. Hány cukorka jut "
        "mindenkinek?",
    },
    {
        "class": "2",
        "comment": "x + (x+2) = 24 => 2x = 22 => x = 11. Nagyobb: 13.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["10", "11", "12", "13", "14"],
        "question": "Két szám összege 24. A nagyobb szám 2-vel nagyobb, mint a kisebb. Mennyi a nagyobb szám?",
    },
    {
        "class": "2",
        "comment": "5 * 3 = 15.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["12", "13", "15", "18", "20"],
        "question": "Egy parkban 5 pad van. Minden padon 3 ember ül. Hány ember ül összesen?",
    },
    {
        "class": "2",
        "comment": "3, 4, 5, 6, 7, 8, 9. Összesen 7.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Hány egész szám van 2 és 10 között (2-t és 10-et nem számítva)?",
    },
    {
        "class": "2",
        "comment": "45 / 5 = 9.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Öt egyforma matrica együtt 45 Ft. Mennyi 1 matrica?",
    },
    {
        "class": "2",
        "comment": "x + (x+2) = 14 => 2x = 12 => x = 6. Kedden: 6 + 2 = 8.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Péter két nap alatt összesen 14 km-t biciklizett. Kedden 2 km-rel többet ment, mint hétfőn. Hány "
        "km-t ment kedden?",
    },
    {
        "class": "2",
        "comment": "30 / 3 = 10.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["8", "9", "10", "11", "12"],
        "question": "Egy dobozban 30 golyó van. Minden harmadik golyó piros, a többi kék. Hány piros golyó van?",
    },
    {
        "class": "2",
        "comment": "36 - 10 - 11 = 15.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["12", "13", "14", "15", "16"],
        "question": "Három szám összege 36. Kettő közülük 10 és 11. Mennyi a harmadik szám?",
    },
    {
        "class": "2",
        "comment": "60 / 3 = 20.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["10 km", "15 km", "20 km", "25 km", "30 km"],
        "question": "Egy biciklis 60 km-t tett meg 3 óra alatt. Hány kilométert tett meg egy óra alatt, ha minden "
        "órában ugyanannyit ment?",
    },
    {
        "class": "2",
        "comment": "80 - 35 - 20 = 25.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["20 Ft", "22 Ft", "25 Ft", "27 Ft", "30 Ft"],
        "question": "Mari 80 Ft-ot kapott. Költött 35 Ft-ot, majd még 20 Ft-ot. Mennyi pénze maradt?",
    },
    {
        "class": "2",
        "comment": "16 * 2 = 32.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["24", "28", "30", "32", "36"],
        "question": "Egy szám fele 16. Melyik ez a szám?",
    },
    {
        "class": "2",
        "comment": "5 - 3 - 1 = 1.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["0", "1", "2", "3", "4"],
        "question": "Egy csapat 5 meccset játszott. 3-at megnyert, 1-et döntetlenre hozott. Hány meccset veszített?",
    },
    {
        "class": "2",
        "comment": "2 * (8 + 6) = 28.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["24 cm", "26 cm", "28 cm", "30 cm", "32 cm"],
        "question": "Egy téglalap egyik oldala 8 cm, a másik oldala 6 cm. Mekkora a kerülete?",
    },
    {
        "class": "2",
        "comment": "20 - (3 + 4 + 5 + 6) = 20 - 18 = 2.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Öt szám összege 20. Négy szám: 3, 4, 5, 6. Mennyi az ötödik szám?",
    },
    {
        "class": "2",
        "comment": "A kockának 8 sarka (csúcsa) van.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["6", "8", "10", "12", "14"],
        "question": "Hány sarka van egy kockának?",
    },
    {
        "class": "2",
        "comment": "20 * 2 = 40.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["30 Ft", "35 Ft", "40 Ft", "45 Ft", "50 Ft"],
        "question": "Anna pénzének fele 20 Ft. Mennyi pénze van összesen?",
    },
    {
        "class": "2",
        "comment": "30 / 3 = 10.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5 km", "8 km", "10 km", "12 km", "15 km"],
        "question": "Egy biciklis 30 km-t tett meg 3 óra alatt. Hány kilométert tett meg egy óra alatt, ha minden "
        "órában ugyanannyit ment?",
    },
    {
        "class": "2",
        "correct": "C",
        "difficulty": "medium",
        "options": ["30", "36", "40", "42", "48"],
        "question": "Egy szám felét és negyedét összeadjuk, 30-at kapunk. Melyik ez a szám?",
    },
    {
        "class": "2",
        "comment": "(25 - 5) / 2 = 10.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["8", "9", "10", "11", "12"],
        "question": "Gondoltam egy számra. Kétszereséhez 5-öt adtam, és 25-öt kaptam. Melyik számra gondoltam?",
    },
    {
        "class": "2",
        "comment": "15 - 9 = 6.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Egy csoportban 15 gyerek van. 9 lány. Hány fiú van?",
    },
    {
        "class": "2",
        "comment": "32 / 4 = 8.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["6 cm", "7 cm", "8 cm", "9 cm", "10 cm"],
        "question": "Egy négyzet kerülete 32 cm. Mennyi az oldalhossza?",
    },
    {
        "class": "2",
        "comment": "40 - 12 = 28.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["24", "26", "28", "30", "32"],
        "question": "Egy kosárban 40 alma van. 12 zöld, a többi piros. Hány piros alma van?",
    },
    {
        "class": "2",
        "comment": "2 * 60 + 30 = 120 + 30 = 150.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["120", "130", "140", "150", "160"],
        "question": "Egy film 2 perc 30 másodpercig tart. Hány másodpercig tart összesen?",
    },
    {
        "class": "2",
        "comment": "4 + 3 + 5 = 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["10", "11", "12", "13", "14"],
        "question": "Manci 4 almát, 3 körtét és 5 szilvát tett a kosarába. Hány gyümölcs van a kosárban?",
    },
    {
        "class": "2",
        "comment": "30 - 15 = 15.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["10", "15", "20", "25", "45"],
        "question": "Gondoltam egy számra. Hozzáadtam 15-öt és 30-at kaptam. Melyik számra gondoltam?",
    },
    {
        "class": "2",
        "comment": "Legyen a nyulak száma x, a tyúkoké y. Ekkor x+y=5 és 4x+2y=14. A két egyenletből x=2, y=3, tehát 3 tyúk van.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Az udvaron tyúkok és nyulak vannak. Összesen 5 fejük és 14 lábuk van. Hány tyúk van?",
    },
    {
        "class": "2",
        "comment": "6 + 6 - 6 + 6 + 6 - 6 = 12.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["6", "12", "18", "24", "36"],
        "question": "Mennyi 6+6-6+6+6-6?",
    },
    {
        "class": "2",
        "comment": "Két hét után újra hétfő. +3 nap: kedd, szerda, csütörtök.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat"],
        "question": "Julika hétfőn ment a nagymamához. Két hét és három nap múlva jött haza. Melyik napon jött haza?",
    },
    {
        "class": "2",
        "comment": "B (A) R (N) A => BRA.",
        "correct": "A",
        "difficulty": "medium",
        "options": ["BRA", "ARN", "BAN", "ANA", "RNA"],
        "question": "BARNA nevéből minden második betűt leírjuk. Mit kapunk?",
    },
    {
        "class": "2",
        "comment": "(♦ + 4) + ♦ = 20 => 2♦ = 16 => ♦ = 8. ♥ = 8 + 4 = 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["10", "11", "12", "13", "14"],
        "question": "Ha ♥ + ♦ = 20 és ♥ = ♦ + 4, akkor mennyi a ♥?",
    },
    {
        "class": "2",
        "comment": "Páros és >50: 82. Páratlan és <40: 35. Tehát 35 és 82.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["28 és 35", "35 és 53", "35 és 82", "28 és 82", "53 és 82"],
        "question": "Kati négy kártyára számokat írt: 28, 35, 53, 82. Kivett két kártyát: az egyik páros és nagyobb "
        "50-nél, a másik páratlan és kisebb 40-nél. Melyik két számot vette ki?",
    },
    {
        "class": "2",
        "comment": "5 * 3 = 15.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["8", "12", "15", "18", "20"],
        "question": "Egy busz 5 megállónál áll meg. Minden megállónál 3 utas száll fel. Hány utas szállt fel "
        "összesen?",
    },
    {
        "class": "2",
        "comment": "H(2) + K(4) + Sze(6) + Cs(2+4=6) + P(4+6=10) = 2 + 4 + 6 + 6 + 10 = 28.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["24", "26", "28", "30", "32"],
        "question": "Anna hétfőn 2, kedden 4, szerdán 6 matricát kapott. Csütörtökön annyit kap, mint hétfőn és kedden "
        "együtt, pénteken annyit, mint kedden és szerdán együtt. Hány matricát kapott összesen hétfőtől "
        "péntekig?",
    },
    {
        "class": "2",
        "comment": "8 - 5 = 3.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["2", "3", "4", "5", "6"],
        "question": "A tortát 8 egyenlő szeletre vágtuk. Elfogyott 5 szelet. Hány szelet maradt?",
    },
    {
        "class": "2",
        "comment": "x fiú + (x+2) lány = 12 => 2x = 10 => x = 5.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Egy csoportban 12 gyerek van. Ha minden fiú mellé 1 lányt állítunk párba, akkor 2 lány marad pár "
        "nélkül. Hány fiú van?",
    },
    {
        "class": "2",
        "comment": "4 * 8 = 32.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["24", "28", "32", "36", "40"],
        "question": "Egy vonat 4 kocsiból áll. Minden kocsiban 8 ablak van. Hány ablak van összesen?",
    },
    {
        "class": "2",
        "comment": "Péntek előtt 2 nap: szerda. Szerdán érkezett. 5 nap (Sze, Cs, P, Szo, V): vasárnap ment haza.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Péntek", "Szombat", "Vasárnap", "Hétfő", "Kedd"],
        "question": "Zoli péntek előtt 2 nappal érkezett a táborba, és 5 nap múlva ment haza (az érkezés napját is "
        "beleszámolva). Melyik napon ment haza?",
    },
    {
        "class": "2",
        "comment": "15 - 6 + 2 = 11.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["9", "10", "11", "12", "13"],
        "question": "A polcon 15 könyv van. Elviszek 6-ot, majd visszahozok 2-t. Hány könyv van a polcon?",
    },
    {
        "class": "2",
        "comment": "x + 2x = 18 => 3x = 18 => x = 6.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Két szám közül a nagyobb kétszer akkora, mint a kisebb. Az összegük 18. Mennyi a kisebb szám?",
    },
    {
        "class": "2",
        "comment": "20 / 2 = 10.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "8", "10", "12", "15"],
        "question": "Nagymama 20 kiflit sütött. A fele mákos. Hány mákos kifli van?",
    },
    {
        "class": "2",
        "comment": "8:00 + 30m + 20m + 10m + 15m = 9:15.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["9:05", "9:10", "9:15", "9:20", "9:25"],
        "question": "Lacika 8-kor kelt. 30 percig reggelizett, 20 perc alatt öltözött, majd 10 percig keresgélt, aztán "
        "15 perc alatt ért az iskolába. Mikor ért oda?",
    },
    {
        "class": "2",
        "comment": "Ha egy piramisnak 4 háromszög alakú oldallapja van, akkor négyszög alapú. Ennek 4 alapcsúcsa és 1 csúcsa van, összesen 5.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["3", "4", "5", "6", "8"],
        "question": "Egy piramisnak 4 háromszög alakú oldallapja van (és négyszög alakú alapja). Hány csúcsa van a piramisnak?",
    },
    {
        "class": "2",
        "comment": "4 * 3 + 3k = 21 => 12 + 3k = 21 => 3k = 9 => k = 3.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["2 Ft", "3 Ft", "4 Ft", "5 Ft", "6 Ft"],
        "question": "4 alma és 3 körte együtt 21 Ft. 1 alma 3 Ft. Mennyibe kerül 1 körte?",
    },
    {
        "class": "2",
        "comment": "16 / 4 = 4.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Kati 16 golyóját egyenlően szétosztja 4 barátja között. Hányat kap mindenki?",
    },
    {
        "class": "2",
        "comment": "Az ISKOLA szó betűi: I-S-K-O-L-A. A magánhangzók (I, O, A) X-ek, a mássalhangzók (S, K, L) O-k, ezért a minta: XOOXOX.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["XOOXOX", "XOOXXO", "XOXOXX", "OXOXOX", "XOXOXO"],
        "question": "Az ISKOLA szóban a magánhangzókat X-szel, a mássalhangzókat O-val helyettesítjük. Mit kapunk?",
    },
    {
        "class": "2",
        "comment": "35 + 28 = 63.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["53", "58", "63", "68", "73"],
        "question": "A könyvtárban 35 mese- és 28 ismeretterjesztő könyv van. Hány könyv van összesen?",
    },
    {
        "class": "2",
        "comment": "x / 3 = 7 => x = 21. (21 + 3) / 2 = 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["10", "11", "12", "13", "14"],
        "question": "Egy számot 3-mal osztva 7-et kapunk. A számhoz 3-at adunk, majd a kapott szám felét vesszük. "
        "Mennyi az eredmény?",
    },
    {
        "class": "2",
        "comment": "14 - 5 - 6 = 3.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["2 Ft", "3 Ft", "4 Ft", "5 Ft", "6 Ft"],
        "question": "Zolinak van 14 Ft-ja. Vesz egy 5 Ft-os cukorkát és egy 6 Ft-os csokit. Mennyi pénze marad?",
    },
    {
        "class": "2",
        "comment": "12, 13, 21, 23, 31, 32. Összesen 6.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["3", "4", "5", "6", "9"],
        "question": "Hány különböző kétjegyű számot írhatunk az 1, 2, 3 számjegyekből, ha mindegyik csak egyszer "
        "szerepelhet?",
    },
    {
        "class": "2",
        "comment": "A szabály +3: 11 + 3 = 14.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["12", "13", "14", "15", "16"],
        "question": "A sorozat: 2, 5, 8, 11, ... Melyik szám jön következőnek?",
    },
    {
        "class": "2",
        "comment": "(x+4) + x = 20 => 2x = 16 => x = 8.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Péter és Pál együtt 20 éves. Péter 4 évvel idősebb. Hány éves Pál?",
    },
    {
        "class": "2",
        "comment": "Ha mind az 5 kéket kiveszed, a 6. már biztosan piros lesz.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["5.", "6.", "7.", "8.", "12."],
        "question": "Egy dobozban 7 piros és 5 kék labda van. Hányadik kivételkor lesz biztosan piros?",
    },
    {
        "class": "2",
        "comment": "🔴 + 🔴 + 🔴 = 9 => 🔴 = 3. 🔵 = 3 + 3 = 6.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["2", "4", "5", "6", "8"],
        "question": "Ha 🔵 + 🔴 = 9 és 🔵 = 🔴 + 🔴, akkor mennyi a 🔵?",
    },
    {
        "class": "2",
        "comment": "6 - 3 = 3.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Ádám a harmadik emeletről a hatodikra megy lifttel. Hány emeletet emelkedik a lift?",
    },
    {
        "class": "2",
        "comment": "Mari eredetileg a 13. volt (12 elöl). Ha 2-t kizárnak előtte, akkor 12-2=10-en lesznek előtte. Ő a "
        "11.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["9.", "10.", "11.", "12.", "13."],
        "question": "Egy versenyen 30-an indultak. Mari előtt 12-en értek célba, mögötte 17-en. Később kiderült, hogy "
        "Mari előtt 2 versenyzőt kizártak. Hányadik lett Mari hivatalosan?",
    },
    {
        "class": "2",
        "comment": "2 * 6 = 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["8", "10", "12", "14", "16"],
        "question": "Egy tábla csokoládé 6 kockából áll. Hány kocka van 2 ugyanilyen tábla csokoládéban?",
    },
    {
        "class": "2",
        "comment": "M-A-T-E-M-A-T-I-K-A: 3 darab A betű van.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["2", "3", "4", "5", "6"],
        "question": "A MATEMATIKA szóban hány A betű van?",
    },
    {
        "class": "2",
        "comment": "Minden 3.-ból 1 lány és 2 fiú. 15 / 3 = 5 csoport, 5 * 2 = 10 fiú.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["5", "8", "9", "10", "12"],
        "question": "Ha minden harmadik gyerek lány egy 15 fős csoportban, hány fiú van?",
    },
    {
        "class": "2",
        "comment": "18 - 5 + 3 = 16.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["14", "15", "16", "17", "18"],
        "question": "Pistinek 18 golyója volt. Elveszített 5-öt, majd kapott 3-at. Hány golyója van most?",
    },
    {
        "class": "2",
        "comment": "65 - 40 = 25.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["15", "20", "25", "30", "35"],
        "question": "Nagypapa 65 éves. 40 évvel ezelőtt hány éves volt?",
    },
    {
        "class": "2",
        "comment": "50 - 3 * 10 = 20.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["10 Ft", "15 Ft", "20 Ft", "25 Ft", "30 Ft"],
        "question": "Katinak van 50 Ft-ja. Vett 3 darab 10 Ft-os cukorkát. Mennyi pénze maradt?",
    },
    {
        "class": "2",
        "comment": "Csilla(1), Anna(2), Béla(3). Anna a második.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1.", "2.", "3.", "4.", "5."],
        "question": "Öt gyerek sorban áll. Anna a Béla előtt, de Csilla mögött áll. Ha Csilla az első, hányadik helyen "
        "áll Anna?",
    },
    {
        "class": "2",
        "comment": "P-A-P-A-G-Á-J: 2 darab P betű van.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["1", "2", "3", "4", "5"],
        "question": "A PAPAGÁJ szóban hány P betű van?",
    },
    {
        "class": "2",
        "comment": "A + (A+5) + (A+5+3) = 28 => 3A + 13 = 28 => 3A = 15 => A = 5. Cili: 5+5+3 = 13.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["11", "12", "13", "14", "15"],
        "question": "Három gyerek kapott pénzt. Bence 5 forinttal többet kapott Annánál, Cili 3 forinttal többet "
        "Bencénél. Összesen 28 forintot kaptak. Hány forintot kapott Cili?",
    },
    {
        "class": "2",
        "comment": "4 * 3 = 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["7", "10", "12", "14", "16"],
        "question": "Egy ház előtt 4 fa áll. Minden fán 3 madár ül. Hány madár van összesen?",
    },
    {
        "class": "2",
        "comment": "80 - 35 = 45.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["35", "40", "45", "50", "55"],
        "question": "Egy könyvben 80 oldal van. Már 35 oldalt olvastam. Hány oldal van még hátra?",
    },
    {
        "class": "2",
        "comment": "x - 12 + 8 + 12 - 10 = 40 => x - 2 = 40 => x = 42.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["40", "41", "42", "43", "44"],
        "question": "Egy vonaton ismeretlen számú utas utazik. Az első megállónál leszáll 12 és felszáll 8. A második "
        "megállónál annyian szállnak fel, mint amennyien az elsőn leszálltak, és 10-en leszállnak. A "
        "második megálló után 40 utas van a vonaton. Hányan utaztak a vonaton induláskor?",
    },
    {
        "class": "2",
        "comment": "7 - 4 = 3.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["2", "3", "4", "5", "11"],
        "question": "Péter 7 éves, húga 4 évvel fiatalabb. Hány éves a húga?",
    },
    {
        "class": "2",
        "comment": "Rosszabb esetben 2 pirosat és 2 kéket veszel (összesen 4). Az 5. labda bármilyen színű, az már a "
        "3. lesz abból a színből.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Egy zsákban 5 piros és 4 kék labda van. Legalább hány labdát kell kivennem csukott szemmel, hogy "
        "biztosan legyen köztük 3 azonos színű?",
    },
    {
        "class": "2",
        "comment": "Este 8-tól éjfélig 4 óra. Éjféltől reggel 7-ig 7 óra. 4 + 7 = 11 óra.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["9", "10", "11", "12", "13"],
        "question": "Évike 8-kor feküdt le. Reggel 7-kor ébredt. Hány órát aludt?",
    },
    {
        "class": "2",
        "comment": "(x+y) = 20, (x-y) = 4. Összeadva: 2x = 24 => x = 12.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["8", "10", "11", "12", "14"],
        "question": "Két szám összege 20, különbségük 4. Melyik a nagyobb szám?",
    },
    {
        "class": "2",
        "comment": "24 / 2 = 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["8", "10", "12", "14", "16"],
        "question": "A kosárban 24 tojás van. A fele fehér, a másik fele barna. Hány fehér tojás van?",
    },
    {
        "class": "2",
        "comment": "1. nap végén: 2m. 2. nap: 4m. 3. nap: 6m. 4. nap: 8m. 5. nap: reggel 8m-ről indul, és 3m-t mászik, "
        "így felér a 10m-es fal tetejére.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "10"],
        "question": "Egy csiga naponta 3 métert mászik fel, de éjjel 1 métert visszacsúszik. Hány nap alatt ér fel egy "
        "10 méteres falra?",
    },
    {
        "class": "2",
        "comment": "2 + 3 + 4 = 9.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Gábor 2 almát, 3 banánt és 4 narancsot vett. Hány gyümölcsöt vett összesen?",
    },
    {
        "class": "2",
        "comment": "Dani mögött egy gyerek (utolsó előtti). Bence Dani előtt (második). Anna nem az első (tehát "
        "negyedik). Így Cili az első.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Anna", "Bence", "Cili", "Dani", "Nem lehet tudni"],
        "question": "Négy gyerek sorban áll: Anna, Bence, Cili, Dani. Dani mögött pontosan egy gyerek áll. Bence "
        "közvetlenül Dani előtt áll. Anna nem az első. Ki áll elöl?",
    },
    {
        "class": "2",
        "comment": "4 * 5 = 20.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["15", "18", "20", "22", "25"],
        "question": "Egy vonat 5 perc alatt tett meg egy megállót. Hány perc alatt tesz meg 4 megállót?",
    },
    {
        "class": "2",
        "comment": "5 + 5 + ● = 17 => 10 + ● = 17 => ● = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "A ▲ + ▲ + ● = 17 és ▲ = 5. Mennyi a ●?",
    },
    {
        "class": "2",
        "comment": "25 - 8 = 17.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["15", "16", "17", "18", "19"],
        "question": "Lacinak volt 25 matricája. Az öccsének adott 8-at. Hány matricája maradt?",
    },
    {
        "class": "2",
        "comment": "Febr. 20 (Hé). +7 nap = Febr. 27 (Hé). Febr. 28 (Ke). Márc. 1 (Sze), Márc. 2 (Cs), Márc. 3 (P), "
        "Márc. 4 (Szo), Márc. 5 (V).",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Péntek", "Szombat", "Vasárnap", "Hétfő", "Kedd"],
        "question": "Február 28 napos. Ha február 20-án hétfő van, milyen nap lesz március 5-én?",
    },
    {
        "class": "2",
        "comment": "6 + 5 = 11.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["9", "10", "11", "12", "13"],
        "question": "Marcika 6 éves. 5 év múlva hány éves lesz?",
    },
    {
        "class": "2",
        "comment": "18 + 15 - 30 = 3.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Az osztályban 30 tanuló van. 18-an fociznak, 15-en kosaraznak. Mindenki legalább egy sportot űz. "
        "Hányan sportolnak mindkettőben?",
    },
    {
        "class": "2",
        "comment": "I, Á: 2 darab magánhangzó.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["1", "2", "3", "4", "5"],
        "question": "A VIRÁG szóban hány magánhangzó van?",
    },
    {
        "class": "2",
        "comment": "3:45 + 10m + 5m + 20m = 3:45 + 35m = 4:20.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["4:05", "4:10", "4:15", "4:20", "4:25"],
        "question": "Az óra 3:45. 10 percet játszom, 5 percet pakolok, majd 20 percet sétálok. Mikor érek haza?",
    },
    {
        "class": "2",
        "comment": "8 + 5 = 13.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["11", "12", "13", "14", "15"],
        "question": "Nyolc gyerek játszik a parkban. Még 5 gyerek jön hozzájuk. Hányan játszanak a parkban?",
    },
    {
        "class": "2",
        "comment": "14 + 6 = 20.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["18", "19", "20", "21", "22"],
        "question": "Mennyi 14 + 6?",
    },
    {
        "class": "2",
        "comment": "20 - 9 = 11.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["9", "10", "11", "12", "13"],
        "question": "Mennyi 20 − 9?",
    },
    {
        "class": "2",
        "comment": "Egy óra 60 percből áll.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["30", "45", "50", "60", "90"],
        "question": "Hány perc egy óra?",
    },
    {
        "class": "2",
        "comment": "Á: 1 darab magánhangzó.",
        "correct": "A",
        "difficulty": "medium",
        "options": ["1", "2", "3", "4", "5"],
        "question": "A HÁZ szóban hány magánhangzó van?",
    },
    {
        "class": "2",
        "comment": "A szabály +5: 15 + 5 = 20.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["16", "18", "20", "22", "25"],
        "question": "Melyik szám hiányzik: 5, 10, 15, ?",
    },
    {
        "class": "2",
        "comment": "30 - 14 = 16.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["14", "15", "16", "17", "18"],
        "question": "Mennyi 30 − 14?",
    },
    {
        "class": "2",
        "comment": "A 19 a legkisebb a felsoroltak közül.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["27", "19", "31", "22", "25"],
        "question": "Melyik kisebb?",
    },
    {
        "class": "2",
        "comment": "16 + 7 = 23.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["21", "22", "23", "24", "25"],
        "question": "Mennyi 16 + 7?",
    },
    {
        "class": "2",
        "comment": "M-A-C-S-K-A: 6 betű.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Hány betű van a MACSKA szóban?",
    },
    {
        "class": "2",
        "comment": "4:00 és 4:30 között 30 perc van.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["20", "25", "30", "35", "40"],
        "question": "Az óra 4:00. Hány perc múlva lesz 4:30?",
    },
    {
        "class": "2",
        "comment": "x + (x+3) = 11 => 2x = 8 => x = 4. A számjegyek 7 és 4. Tehát 74.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["74", "65", "83", "47", "71"],
        "question": "Egy kétjegyű szám tízesek számjegye 3-mal nagyobb, mint az egyesek számjegye. A számjegyek "
        "összege 11. Melyik szám lehet ez?",
    },
    {
        "class": "2",
        "comment": "P - 4 = Z, P + Z = 32. P + (P-4) = 32 => 2P = 36 => P = 18.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["14", "16", "18", "20", "22"],
        "question": "Egy kosárban 32 alma van, piros és zöld. Ha 4 piros almát kiveszünk, akkor ugyanannyi piros "
        "marad, mint zöld. Hány piros alma volt eredetileg?",
    },
    {
        "class": "2",
        "comment": "A szabály: +3, +4, +5... Következő: +6. 14 + 6 = 20.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["18", "19", "20", "21", "22"],
        "question": "Melyik szám hiányzik: 2, 5, 9, 14, ?",
    },
    {
        "class": "2",
        "comment": "3:20 + 15m + 10m + 20m = 3:20 + 45m = 4:05.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["4:00", "4:05", "4:10", "4:15", "4:20"],
        "question": "Az óra 3:20-at mutat. 15 percet olvasok, utána 10 perc szünetet tartok, majd még 20 percet "
        "játszom. Hány óra lesz?",
    },
    {
        "class": "2",
        "comment": "Kékben nem 6, tehát 5 vagy 7. Piros < Kék. Ha Kék=7, Piros lehet 5 vagy 6. Ha Kék=5, Piros nem "
        "lehet semmi. Tehát Kék=7. Piros < 7 és Zöld > Piros. Ha Piros=5, akkor Zöld=6. (Mert 7 már "
        "foglalt).",
        "correct": "B",
        "difficulty": "hard",
        "options": ["5", "6", "7", "8", "Nem lehet tudni"],
        "question": "Három doboz van: piros, kék, zöld. Az egyikben 5 golyó, a másikban 6, a harmadikban 7 van. A "
        "pirosban kevesebb van, mint a kékben. A zöldben több van, mint a pirosban. A kékben nem 6 golyó "
        "van. Hány golyó van a zöld dobozban?",
    },
    {
        "class": "2",
        "comment": "8 + 30 = 38.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["22", "30", "35", "38", "40"],
        "question": "Peti 8 éves, az apukája 30 évvel idősebb nála. Hány éves az apukája?",
    },
    {
        "class": "2",
        "comment": "14 + 6 = 20.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["8", "18", "20", "22", "24"],
        "question": "Egy dobozban 14 piros és 6 kék ceruza van. Hány ceruza van a dobozban?",
    },
    {
        "class": "2",
        "comment": "A szabály +10: 30 + 10 = 40.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["35", "40", "45", "60", "100"],
        "question": "Melyik szám hiányzik: 10, 20, 30, __, 50?",
    },
    {
        "class": "2",
        "comment": "I, O, A: 3 darab magánhangzó.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Hány magánhangzó van a 'ISKOLA' szóban?",
    },
    {
        "class": "2",
        "correct": "D",
        "difficulty": "medium",
        "options": ["4", "10", "15", "20", "25"],
        "question": "Gondoltam egy számot, elvettem belőle 8-at és 12-t kaptam. Mi volt a szám?",
        "comment": "Ha x - 8 = 12, akkor x = 20.",
    },
    {
        "class": "2",
        "correct": "C",
        "difficulty": "medium",
        "options": ["4", "6", "8", "10", "12"],
        "question": "Hány sarka van két téglalapnak összesen?",
        "comment": "Egy téglalapnak 4 sarka van, ezért kettőnek 2 * 4 = 8.",
    },
    {
        "class": "2",
        "comment": "20 - 5 - 3 = 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["8", "10", "12", "15", "17"],
        "question": "Anni 20 szem cukorkát kapott. Megevett belőle 5-öt, és 3-at adott a húgának. Hány maradt?",
    },
    {
        "class": "2",
        "comment": "1 óra = 60 perc, fél óra = 30 perc.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["15", "20", "30", "45", "60"],
        "question": "Hány perc van fél órában?",
    },
    {
        "class": "2",
        "comment": "20 + 20 = 40.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["15+15", "20+20", "30+5", "10+20", "25+25"],
        "question": "Melyik két szám összege 40?",
    },
    {
        "class": "2",
        "comment": "2 * 7 = 14.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["7", "10", "12", "14", "20"],
        "question": "Hány nap van két hétben?",
    },
    {
        "class": "2",
        "comment": "15 * 2 = 30.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["10", "20", "25", "30", "35"],
        "question": "Zoli 15 matricát gyűjtött, Sanyi kétszer annyit. Hány matricája van Sanyinak?",
    },
    {
        "class": "2",
        "comment": "70 - 30 = 40.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["30", "40", "50", "80", "100"],
        "question": "Melyik szám a 70 és a 30 különbsége?",
    },
    {
        "class": "2",
        "comment": "A 13-nál kisebb kétjegyű számok: 10, 11, 12. Összesen 3.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["2", "3", "4", "12", "13"],
        "question": "Hány kétjegyű szám van, ami 13-nál kisebb?",
    },
    {
        "class": "2",
        "comment": "30 - 18 = 12.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["10", "12", "14", "16", "20"],
        "question": "Mennyit kell adni a 18-hoz, hogy 30-at kapjunk?",
    },
    {
        "class": "2",
        "comment": "8 + 3 = 11, ami páratlan szám.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["10+4", "15-5", "8+3", "20-2", "6+6"],
        "question": "Melyik művelet eredménye páratlan?",
    },
    {
        "class": "2",
        "comment": "Január, Február, Március, Április (4.).",
        "correct": "B",
        "difficulty": "medium",
        "options": ["Március", "Április", "Május", "Június", "Július"],
        "question": "Melyik hónap az év 4. hónapja?",
    },
    {
        "class": "2",
        "comment": "20 / 2 + 5 = 10 + 5 = 15.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["10", "15", "20", "25", "30"],
        "question": "Mennyi a 20 fele plusz 5?",
    },
    {
        "class": "2",
        "comment": "2 * 4 = 8.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["2", "4", "6", "8", "10"],
        "question": "Egy pizzát 4 szeletre vágtak. Hány szelet van 2 ugyanilyen pizzában?",
    },
    {
        "class": "2",
        "comment": "45 + 15 = 60.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["50", "55", "60", "65", "70"],
        "question": "Mennyi a 45 és 15 összege?",
    },
    {
        "class": "2",
        "comment": "5 * 8 = 40.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["30", "35", "40", "45", "50"],
        "question": "Hány lába van összesen 5 póknak? (A pók 8 lábú)",
    },
    {
        "class": "2",
        "comment": "A 29 a legkisebb a felsoroltak közül.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["34", "43", "29", "92", "30"],
        "question": "Melyik a legkisebb szám: 34, 43, 29, 92, 30?",
    },
    {
        "class": "2",
        "comment": "50 + 20 = 70. 70 / 10 = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Hány tízforintost ér egy 50 forintos és egy 20 forintos együtt?",
    },
    {
        "class": "2",
        "comment": "A 9 páratlan szám, a többi páros.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["2", "4", "6", "9", "10"],
        "question": "Melyik szám a kakukktojás: 2, 4, 6, 9, 10?",
    },
    {
        "class": "2",
        "comment": "Délután 1 óra az 13 órának felel meg. 13 - 9 = 4 óra.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["3", "4", "5", "6", "7"],
        "question": "Hány óra telik el reggel 9 és délután 1 óra között?",
    },
    {
        "class": "2",
        "comment": "4 gombóc fagyi az 2 * 2 gombóc, tehát 2 * 40 = 80 forint.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["40", "60", "80", "100", "120"],
        "question": "Ha 2 gombóc fagyi 40 forint, mennyibe kerül 4 gombóc?",
    },
    {
        "class": "2",
        "comment": "Csak az 5 és a 15 tartalmaz 5-öst. Tehát 2 darab van.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Hány darab 5-ös számjegy van 1-től 20-ig?",
    },
    {
        "class": "2",
        "comment": "10 / 2 = 5.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["2", "4", "5", "8", "10"],
        "question": "Egy karkötőn 10 gyöngy van. Minden második kék. Hány kék gyöngy van rajta?",
    },
    {
        "class": "2",
        "comment": "88 - 11 = 77.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["66", "77", "88", "99", "100"],
        "question": "Mennyi a 88 és 11 különbsége?",
    },
    {
        "class": "2",
        "comment": "3 * 10 = 30.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["3", "10", "20", "30", "40"],
        "question": "Hány milliméter 3 centiméter?",
    },
    {
        "class": "2",
        "comment": "3 * 10 = 30.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["15", "30", "45", "60", "75"],
        "question": "Hány ujja van 3 gyereknek összesen?",
    },
    {
        "class": "2",
        "comment": "Szerda előtt kedd van.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"],
        "question": "Melyik nap van ma, ha a holnap az szerda?",
    },
    {
        "class": "2",
        "comment": "3 * 15 = 45.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["30", "40", "45", "50", "60"],
        "question": "Mennyi 15 + 15 + 15?",
    },
    {
        "class": "2",
        "comment": "100 - 20 = 80.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["60", "70", "80", "90", "100"],
        "question": "Melyik számot kell a 20-hoz adni, hogy 100-at kapjunk?",
    },
    {
        "class": "2",
        "comment": "12 emberre kell 12 / 4 = 3 alma. Van 2, kell még 1. Boltban csak párosat adnak, így legalább 2-t "
        "kell vennie.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Fanni gyümölcssalátát készít 12 embernek. 4 személyre 1 alma kell. Otthon már van 2 almája, de a "
        "boltban csak páros számú almát lehet venni. Hány almát kell még vennie legalább?",
    },
    {
        "class": "2",
        "comment": "x + (x+1) = 15 => 2x = 14 => x = 7.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Egy könyvben két egymás melletti oldalszám összege 15. Melyik a kisebb szám?",
    },
    {
        "class": "2",
        "comment": "H(4), K(6), Sze(4+6=10), Cs(10-6=4).",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Hétfőn 4 mm eső esett. Kedden 2 mm-rel több, szerdán annyi, mint hétfőn és kedden együtt. "
        "Csütörtökön annyi, mint szerdán és kedden a különbség. Hány mm esett csütörtökön?",
    },
    {
        "class": "2",
        "comment": "x-4+6-10=1 (alsó fok) => x=9. Mivel a 9. a középső, a létrának 2*9-1 = 17 foka van.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["15", "16", "17", "18", "19"],
        "question": "Egy tűzoltó a létra középső fokán áll. Lemegy 4 fokot, felmegy 6-ot, majd 10 fokot lefelé haladva "
        "az alsó fokra jut. Hány fokos a létra?",
    },
    {
        "class": "2",
        "comment": "Kedd + 2 nap = csütörtök. Csütörtök - 3 nap = hétfő.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["Hétfő", "Kedd", "Szerda", "Vasárnap", "Szombat"],
        "question": "Pistike szerint 3 nap múlva olyan nap lesz, ami kedd után 2 nappal van. Melyik nap van ma?",
    },
    {
        "class": "2",
        "comment": "x + 5 - 3 = 8 => x = 6.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "8"],
        "question": "A villamosra felszállt 5 utas, leszállt 3. Az utolsó megállóban leszállt mind a 8 utas. Hányan "
        "voltak rajta eredetileg?",
    },
    {
        "class": "2",
        "comment": "Az 5. és a 10. (5+4+1=10) szakadt el. Tehát 10 palacsintát sütött.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["8", "9", "10", "11", "12"],
        "question": "Kati palacsintát süt. Az 5. és az utolsó elszakadt. Közöttük 4 szép lett. Hányat sütött "
        "összesen?",
    },
    {
        "class": "2",
        "comment": "H(X) A(X) L(X) -> HXAXLX.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["HXAXLX", "HXAXXL", "HXAL", "XHALX", "HAAAX"],
        "question": "Tudorka gépe minden betű után ír egy 'X'-et. Mit látunk, ha a 'HAL' szót gépelte be?",
    },
    {
        "class": "2",
        "comment": "2 kutya (8 láb) + 2 kacsa (4 láb) = 12 láb, 4 fej.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "0"],
        "question": "Egy udvaron kutyák és kacsák vannak. 4 fejük és 12 lábuk van. Hány kutya van?",
    },
    {
        "class": "2",
        "comment": "6 darabhoz 5 vágás kell.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Hány vágással tudunk egy rudat 6 darabra vágni?",
    },
    {
        "class": "2",
        "comment": "x/2 = x/4 + 10 => x/4 = 10 => x = 40.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["20", "30", "40", "50", "60"],
        "question": "Gondoltam egy számot. A fele 10-zel több, mint a negyede. Mennyi a szám?",
    },
    {
        "class": "2",
        "comment": "A szabály: +1, +2, +3, +4... 11 + 5 = 16.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["12", "14", "15", "16", "18"],
        "question": "Melyik szám a következő: 1, 2, 4, 7, 11, ...?",
    },
    {
        "class": "2",
        "comment": "10 - 3 + 1 = 8.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["6.", "7.", "8.", "9.", "10."],
        "question": "Egy sorban 10 gyerek áll. Anna elölről a 3. Hányadik hátulról?",
    },
    {
        "class": "2",
        "comment": "13, 22, 31, 40. Összesen 4.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Hány olyan kétjegyű szám van, aminek a jegyei összege 4?",
    },
    {
        "class": "2",
        "comment": "Tegnapelőtt 7 volt, tegnap betöltötte a 8-at. Ma is 8, jövőre 9 lesz.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["8", "9", "10", "11", "12"],
        "question": "Bence tegnapelőtt 7 éves volt. Jövőre hány éves lesz?",
    },
    {
        "class": "2",
        "comment": "2, 12, 20, 21, 22 (két darab), 23, 24, 25. Összesen 9.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["5", "7", "8", "9", "10"],
        "question": "Hány darab 2-es számjegyet írunk le 1-től 25-ig?",
    },
    {
        "class": "2",
        "comment": "Egy sarok helyett két új sarok keletkezik. 4 - 1 + 2 = 5.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["3", "4", "5", "6", "7"],
        "question": "Egy asztalnak 4 sarka van. Levágunk egy sarkot egyenesen. Hány sarka marad?",
    },
    {
        "class": "2",
        "comment": "P - 1 = K + 1. P + K = 10. Összeadva: 2P = 12 => P = 6.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Egy tálban 10 golyó van, piros és kék. Ha 1 piros golyót kékre festünk, akkor ugyanannyi piros "
        "lesz, mint kék. Hány piros golyó volt eredetileg?",
    },
    {
        "class": "2",
        "comment": "Az út 20 percig tartott összesen. Megállások nélkül 20 - 6 = 14 perc.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["12", "14", "16", "18", "20"],
        "question": "11:50-kor elindulunk, 12:10-kor megérkezünk. Útközben kétszer 3 percet állunk. Mennyi ideig "
        "mentünk megállás nélkül?",
    },
    {
        "class": "2",
        "comment": "A 8. nap végén 8 méteren van. A 9. napon 8 méterről indul, felmászik 2 métert, így eléri a 10 "
        "métert. Tehát a 9. napon ér fel.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["8.", "9.", "10.", "11.", "12."],
        "question": "Egy 10 méter mély kútból a csiga nappal 2 métert mászik fel, éjjel 1-et visszacsúszik. Hányadik "
        "napon ér fel?",
    },
    {
        "class": "2",
        "comment": "Cili, Dani, Emma sorrend nem lehet. Emma mindenképpen Ciliék előtt van (Emma... Cili, Dani). Anna "
        "nem első. Bence lehet az első, ekkor: Bence, Emma, Cili, Dani, Anna.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["Anna", "Bence", "Cili", "Dani", "Emma"],
        "question": "Egy sorban 5 gyerek áll: Anna, Bence, Cili, Dani, Emma. Dani közvetlenül Cili mögött áll. Anna "
        "nem az első. Emma Dani előtt áll, de nem közvetlenül. Ki áll legelöl?",
    },
    {
        "class": "2",
        "comment": "Adott a nagyobb válasz (55), ha x=55, akkor y=30. x-y=25. 3x-3y=75. Ez nem 5. Valószínűleg a "
        "kérdésben a 5-tel több helyett 75-tel több kellene.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["40", "45", "50", "55", "60"],
        "question": "Két szám összege 85. A nagyobb szám háromszorosa 75-tel nagyobb, mint a kisebb háromszorosa. "
        "Mennyi a nagyobb szám?",
    },
    {
        "class": "2",
        "comment": "10, 20, 30, 40, 50, 60, 70, 80, 90 (9 db) + 100 (2 db) = 11.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["9", "10", "11", "12", "20"],
        "question": "Hány darab 0-t írunk le 1-től 100-ig (az 1-et és a 100-at is beleértve)?",
    },
    {
        "class": "2",
        "comment": "2 * 10 + 4 * 5 = 20 + 20 = 40. Összesen 2 + 4 = 6 érme.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Peti 40 forintot fizet csak 5 és 10 forintosokkal. Összesen 6 érméje van. Hány 10 forintosa van?",
    },
    {
        "class": "2",
        "comment": "A 98 kétjegyű, páros, és a jegyei különbözőek.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["99", "98", "96", "88", "90"],
        "question": "Melyik a legnagyobb kétjegyű páros szám, aminek a jegyei különbözőek?",
    },
    {
        "class": "2",
        "comment": "A 2 lány ugyanannak a 2 fiúnak a testvére. Tehát 2 + 2 = 4 gyerek.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["2", "4", "6", "8", "10"],
        "question": "Egy családban 2 lány van, mindegyiknek van 2 fiútestvére. Hány gyerek van?",
    },
    {
        "class": "2",
        "comment": "6h + 8p = 64, h + p = 10. 6(10 - p) + 8p = 64 => 60 + 2p = 64 => p = 2.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Egy dobozban hangyák és pókok vannak. Összesen 10 állat és 64 láb van. Hány pók van? (A hangyának "
        "6, a póknak 8 lába van.)",
    },
    {
        "class": "2",
        "comment": "12:50 + 20 perc = 13:10. 13:10 + 35 perc = 13:45.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["13:25", "13:35", "13:40", "13:45", "13:55"],
        "question": "Az óra 12:50. 20 perc múlva kezdődik az edzés, és 35 percig tart. Mikor lesz vége?",
    },
    {
        "class": "2",
        "comment": "1x + 2y = 11, x + y = 8. (8 - y) + 2y = 11 => y = 3.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Csak 1 és 2 forintosokkal fizetek. Összesen 8 érmét adok, és pontosan 11 forintot fizetek. Hány "
        "darab 2 forintosom van?",
    },
    {
        "class": "2",
        "comment": "x/2 = x/4 + 6 => x/4 = 6 => x = 24. A szám fele 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["6", "8", "10", "12", "14"],
        "question": "Gondoltam egy számot. A fele 6-tal több, mint a negyede. Mennyi a szám fele?",
    },
    {
        "class": "2",
        "comment": "4 kis háromszög + 4 közepes háromszög (amik az oldalakból állnak) = 8.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["2", "4", "6", "8", "10"],
        "question": "Hány háromszög van egy olyan négyzetben, amit mindkét átlójával elvágtunk?",
    },
    {
        "class": "2",
        "comment": "Eredetileg 6 * 4 = 24 lap látszik. Levéve a sarkot, 3 lap eltűnik, de 3 új belső lap válik "
        "láthatóvá, marad 24.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["21", "22", "23", "24", "25"],
        "question": "Egy 2×2×2-es nagy kockát kis kockákból raktunk ki. Leemelünk egy sarokkockát. Hány kis négyzetlap "
        "látszik kívülről ezután?",
    },
    {
        "class": "2",
        "comment": "A 8. nap végén 8 méteren van. A 9. nap nappal felmászik 2 métert, így eléri a 10 méteres peremet, tehát a 9. napon ér fel.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["8.", "9.", "10.", "11.", "12."],
        "question": "Egy 10 méter mély kútból a csiga nappal 2 métert mászik fel, éjjel 1-et visszacsúszik. Hányadik "
        "napon ér fel a peremre?",
    },
    {
        "class": "2",
        "comment": "12 / 3 = 4 szakasz, amihez 4 + 1 = 5 oszlop kell.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["3", "4", "5", "6", "12"],
        "question": "Egy 12 méter hosszú egyenes kerítéshez 3 méterenként kell egy oszlop. Hány oszlop kell, ha a két "
        "végén is áll egy-egy?",
    },
    {
        "class": "2",
        "correct": "D",
        "difficulty": "medium",
        "options": ["12", "13", "14", "15", "16"],
        "question": "Hat barát találkozik, és mindenki mindenkivel pontosan egyszer kezet fog. Hány kézfogás történik "
        "összesen?",
        "comment": "A kézfogások száma: 6*5/2 = 15.",
    },
    {
        "class": "2",
        "comment": "Minden levágott sarok helyett két új keletkezik: 3 * 2 = 6.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["3", "4", "5", "6", "9"],
        "question": "Hány sarka lesz egy háromszög alakú papírnak, ha mind a három sarkát levágjuk egy-egy egyenes "
        "vágással?",
    },
    {
        "class": "2",
        "comment": "(15 + 5) / 2 = 10.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["5", "10", "15", "20", "25"],
        "question": "Gondoltam egy számot, megdupláztam, majd elvettem belőle 5-öt és 15-öt kaptam. Mi volt az eredeti "
        "szám?",
    },
    {
        "class": "2",
        "comment": "4 + 7 - 1 = 10.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["9", "10", "11", "12", "13"],
        "question": "Egy sorban Anna elölről a 4., hátulról pedig a 7. Hányan állnak összesen a sorban?",
    },
    {
        "class": "2",
        "comment": "Mind a 8 kiskocka sarokkocka, tehát mind a 8-nak 3 piros oldala lesz.",
        "correct": "E",
        "difficulty": "medium",
        "options": ["0", "2", "4", "6", "8"],
        "question": "Egy kockát minden oldalán pirosra festünk, majd 8 egyforma kiskockára vágunk. Hány kiskockának "
        "lesz pontosan 3 oldala piros?",
    },
    {
        "class": "2",
        "comment": "1, 10, 11 (2db), 12, 13, 14, 15, 16, 17, 18, 19. Összesen 12.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["10", "11", "12", "13", "14"],
        "question": "Hány darab 1-es számjegyet kell leírnunk, ha 1-től 20-ig minden egész számot leírunk?",
    },
    {
        "class": "2",
        "correct": "B",
        "difficulty": "medium",
        "options": ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Vasárnap"],
        "question": "Tegnapelőtt azt mondtam, hogy holnapután kedd lesz. Milyen nap van ma?",
        "comment": "Tegnapelőtt a 'holnapután' a tegnap volt, tehát tegnap kedd volt. Ezért ma szerda van.",
    },
    {
        "class": "2",
        "comment": "3 kutya (12 láb) + 3 kacsa (6 láb) = 18 láb, 6 fej.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Egy udvaron kutyák és kacsák vannak. Összesen 6 fejük és 18 lábuk van. Hány kutya van?",
    },
    {
        "class": "2",
        "comment": "10 / 2 = 5 darabhoz 4 vágás kell.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["3", "4", "5", "6", "10"],
        "question": "Hány vágással tudunk egy 10 méteres kötelet 2 méteres darabokra vágni?",
    },
    {
        "class": "2",
        "comment": "Peti tőle balra 4. és jobbra 4. ugyanaz, tehát ő a 8. helyen ülne egy sorban, de körben ez 8 fős "
        "asztalt jelent.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Peti egy kerek asztalnál ül. Ha tőle balra 4 széket számolunk, ugyanahhoz a gyerekhez jutunk, "
        "mint ha tőle jobbra 4 széket számolunk. Hányan ülnek az asztalnál Petivel együtt?",
    },
    {
        "class": "2",
        "comment": "A 9 tükörképe a 3.",
        "correct": "A",
        "difficulty": "medium",
        "options": ["3:00", "6:00", "9:00", "12:00", "kiszámíthatatlan"],
        "question": "Egy mutatós óra a tükörben pontosan 9 órát mutat. Mennyi a valódi idő?",
    },
    {
        "class": "2",
        "comment": "1 szint különbség 20 fok, 1-ről 4-re 3 szint van: 3 * 20 = 60.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["40", "60", "80", "100", "120"],
        "question": "Az 1. emeletről a 2.-ra 20 lépcsőfok vezet. Hány fokot kell mászni az 1.-ről a 4. emeletre?",
    },
    {
        "class": "2",
        "comment": "3a + 1k = 1a + 2k => 2a = 1k.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["1", "2", "3", "4", "5"],
        "question": "3 alma és 1 körte ugyanannyit nyom, mint 1 alma és 2 körte. Hány alma súlya ér fel 1 körtével?",
    },
    {
        "class": "2",
        "comment": "x / 2 + 4 = 14 => x / 2 = 10 => x = 20.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["10", "15", "18", "20", "24"],
        "question": "A buszról leszállt az utasok fele, majd felszállt 4 ember. Így 14-en lettek. Hányan indultak?",
    },
    {
        "class": "2",
        "comment": "a + b = 10, a = b + 4. (b + 4) + b = 10 => 2b = 6 => b = 3.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["2", "3", "4", "6", "7"],
        "question": "Egy tálban 10 gyümölcs van, almák és barackok. 4-gyel több az alma. Hány barack van?",
    },
    {
        "class": "2",
        "comment": "11:45-től 12:15-ig 30 perc telik el.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["15", "20", "30", "45", "60"],
        "question": "Hány perc telik el délelőtt 11:45 és délután 12:15 között?",
    },
    {
        "class": "2",
        "comment": "25 mező van. Ha az első sötét, akkor 13 sötét és 12 világos mező lesz.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["10", "11", "12", "13", "14"],
        "question": "Hány sötét mező van egy 5x5-ös kicsi sakktáblán, ha a bal felső sarka sötét?",
    },
    {
        "class": "2",
        "comment": "Csütörtök + 2 nap = szombat. Szombat - 4 nap = kedd.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["hétfő", "kedd", "szerda", "csütörtök", "szombat"],
        "question": "Pistike a kishúgának azt mondta: négy nap múlva olyan nap lesz, ami csütörtök után két nappal "
        "van. Melyik napon mondta ezt Pistike?",
    },
    {
        "class": "2",
        "comment": "x + 8 - 5 = 10 => x + 3 = 10 => x = 7.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["3", "7", "13", "18", "23"],
        "question": "Egy villamosra az utolsó előtti megállóban felszállt 8 utas, és leszállt róla 5 utas. Az utolsó "
        "megállóban leszállt a villamoson lévő mind a 10 utas. Hány utas volt a villamoson, amikor "
        "beérkezett az utolsó előtti megállóba?",
    },
    {
        "class": "2",
        "comment": "A 10. volt az első rossz. Utána 8 jó következett (ez a 18.-ig tartott), majd az utolsó (a 19.) "
        "megint rossz lett.",
        "correct": "E",
        "difficulty": "medium",
        "options": ["9", "10", "17", "18", "19"],
        "question": "Kati palacsintát sütött. Csak a tizedik és az utolsó nem sikerült szépre, mert ezek egy kicsit "
        "elszakadtak. A két szakadt palacsinta megsütése között nyolc szépet sütött. Hány palacsintát "
        "sütött Kati?",
    },
    {
        "class": "2",
        "comment": "L(A) A(A) P(A) -> LAAAPA.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["ALAPA", "LAAPA", "LAAAPA", "LAAP", "ALAAAPA"],
        "question": "Tudorka számítógépe rosszul működik. Minden betű begépelésekor közvetlenül a begépelt betű képe "
        "után a képernyőn megjelenik egy A betű. Mi látható a számítógép képernyőjén, ha Tudorka a LAP "
        "szót gépelte be?",
    },
    {
        "class": "2",
        "comment": "x + (x + 1) = 29 => 2x = 28 => x = 14.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["12", "13", "14", "15", "16"],
        "question": "Az Abacus újság a kedvenc rovatomnál van nyitva. A két látható oldalszám összege 29. Melyik a két "
        "oldalszám közül a kisebb?",
    },
    {
        "class": "2",
        "comment": "H(4), K(6), Sze(8), Cs(10), P(12), Szo(14), V(16). Összesen: 4+6+8+10+12+14+16 = 70.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["16", "40", "60", "70", "80"],
        "question": "A nyáron volt egy olyan hét, amikor minden nap esett az eső. Azon a héten hétfőn 4 milliméter "
        "hullott, és minden utána következő napon 2 milliméterrel több, mint az előző napon. Hány "
        "milliméter eső esett azon a héten?",
    },
    {
        "class": "2",
        "comment": "A 2 oldalon festett kockák az éleken vannak (a csúcsok kivételével). 12 él van, mindegyiken 1 "
        "ilyen kocka.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["8", "12", "18", "24", "27"],
        "question": "Egy 3x3x3-as kockát minden oldalán pirosra festünk, majd 1x1x1-es kiskockákra vágunk. Hány "
        "kiskockának lesz pontosan 2 oldala piros?",
    },
    {
        "class": "2",
        "comment": "(20 / 2) + 5 = 15.",
        "correct": "B",
        "difficulty": "medium",
        "options": ["10", "15", "20", "25", "30"],
        "question": "Gondoltam egy számot, elvettem belőle 5-öt, majd megdupláztam és 20-at kaptam. Mi volt az eredeti "
        "szám?",
    },
    {
        "class": "2",
        "comment": "14 / 2 = 7.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Hány pár zoknit tudunk összeállítani 14 darab zokniból?",
    },
    {
        "class": "2",
        "comment": "20 és 29 közös része a 2-es számjegy és a Mackó. Tehát 2=Mackó. Ebből 20-nál: 0=Nyuszi. 35-nél: "
        "3=Oroszlán. Így a 30: (Oroszlán, Nyuszi).",
        "correct": "A",
        "difficulty": "hard",
        "options": [
            "(Oroszlán, Nyuszi)",
            "(Oroszlán, Róka)",
            "(Róka, Nyuszi)",
            "(Csibe, Nyuszi)",
            "(Mackó, Oroszlán)",
        ],
        "question": "Az ábrán három szám titkosírással leírt alakja látható: 20 -> (Mackó, Nyuszi), 29 -> (Mackó, "
        "Róka), 35 -> (Oroszlán, Csibe). Mindegyik számjegyet egy állat helyettesít. Melyik válasz jelöli "
        "a 30-at?",
    },
    {
        "class": "2",
        "comment": "Középső fok = x. x - 8 + 14 - 18 = 1 (alsó fok). x - 12 = 1 => x = 13. Ha a 13. a középső, akkor "
        "2*13 - 1 = 25 foka van.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["18", "24", "25", "26", "27"],
        "question": "Egy tűzoltó a létra középső fokán áll, és oltja a tüzet. Amikor a tűz erősödik, kénytelen 8 "
        "fokkal lejjebb jönni a hőség miatt. Pár perc múlva a tűz csendesedik, s így 14 fokkal feljebb "
        "mászva folytatja a lángokkal való küzdelmet. Innen a tűz eloltása után 18 fokot lefelé haladva "
        "jut el a létra legalsó fokára. Hány fok van a létrán?",
    },
    {
        "class": "2",
        "comment": "4 híd és 3 alagút: 4 * 3 = 12 különböző útvonal.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["3", "4", "5", "7", "12"],
        "question": "Törpapa szeretne eljutni a patakon és a hegyen túl lakó Hókuszpókhoz. A patakon négy híd van, a "
        "hegyen három alagút vezet keresztül. A kettő között egy kerítés van, amin nem lehet átmászni. "
        "Hányféle utat választhat Törpapa, ha mindkét akadályon át kell jutnia?",
    },
    {
        "class": "2",
        "comment": "4 különböző betűből 3-at 4*3*2 = 24-féleképpen rakhatunk össze. Mivel 3 betűt választunk a 4-ből, "
        "mindenképpen lesz benne mássalhangzó és magánhangzó is (mert csak 2 van mindegyikből), így mind a "
        "24 szó szabályos.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["4", "12", "16", "24", "36"],
        "question": "Tündérországban csak 2 magánhangzót és 2 mássalhangzót használnak. A szavakban legalább 1 "
        "mássalhangzó és legalább 1 magánhangzó van. Hány különböző hárombetűs szó létezik, ha azonos "
        "betűk nincsenek benne?",
    },
    {
        "class": "2",
        "comment": "8:00-8:10 munka (10 perc * 4 = 40). 8:10-8:12 pihenő. 8:12-8:15 munka (3 perc * 4 = 12). Összesen "
        "40 + 12 = 52.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["15", "23", "40", "52", "60"],
        "question": "Tomi a nyári bográcsos főzéshez gyújtóst készített úgy, hogy szőlővesszőket tört össze, egy perc "
        "alatt négyet. Tíz perc munka után két perc pihenőt tartott, majd folytatta. A munkát reggel 8 "
        "órakor kezdte és 8 óra 15 perckor hagyta abba. Hány szőlővesszőt tört össze?",
    },
    {
        "class": "2",
        "comment": "A kényszerfeltételek alapján az egyetlen lehetséges párosítás az üléseken: (A,E), (B,F), (C,D). "
        "Tehát Anna Eszter mellett ült.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["Bea", "Csilla", "Dóri", "Eszter", "nem meghatározható"],
        "question": "Az autóbuszban 3 sorban egymás mögött, soronként 2 üléssel, összesen 6 szabad hely van. Anna (A), "
        "Bea (B), Csilla (C), Dóri (D), Eszter (E) és Fanni (F) leültek. A nem B mellett, B nem C és nem D "
        "mellett, D nem A, nem C és nem E mellett ült. Ki mellett ült Anna?",
    },
    {
        "class": "2",
        "comment": "A számok: 102, 111, 120, 201, 210, 300. Összesen 6.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["3", "4", "5", "6", "9"],
        "question": "Hány olyan háromjegyű szám van, amelynek a számjegyeinek összege pontosan 3?",
    },
    {
        "class": "2",
        "comment": "Az 5 oldal és a belső pont pontosan 5 háromszöget alkot.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["5", "10", "15", "20", "25"],
        "question": "Hány háromszög látható egy olyan ötszögben, amelynek minden csúcsát összekötöttük egy belső "
        "ponttal?",
    },
    {
        "class": "2",
        "comment": "8 sarok + 12 él = 20.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["14", "16", "18", "20", "24"],
        "question": "Hány sarka és hány éle van egy kockának összesen?",
    },
    {
        "class": "2",
        "comment": "Ha hármat veszünk, lehet mindhárom különböző (P, K, Z). A negyedik biztosan megegyezik "
        "valamelyikkel.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Egy dobozban 5 piros, 5 kék és 5 zöld golyó van. Legalább hány golyót kell becsukott szemmel "
        "kivennünk, hogy biztosan legyen köztük két azonos színű?",
    },
    {
        "class": "2",
        "comment": "Holnapután utáni nap = ma + 3 nap. Ma + 3 = szombat, tehát ma szerda. Tegnapelőtt hétfő volt.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["hétfő", "kedd", "szerda", "szombat", "vasárnap"],
        "question": "Hanna ma azt mondta: 'A holnapután utáni nap szombat lesz'. Melyik nap volt tegnapelőtt?",
    },
    {
        "class": "2",
        "comment": "A számok: 101, 110, 200. Összesen 3.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Hány olyan háromjegyű szám van, amelyben a számjegyek összege 2?",
    },
    {
        "class": "2",
        "comment": "Csak a legbelső kocka nem kap festéket. 27 = 3x3x3, a belső mag egyetlen 1x1x1-es kocka.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["0", "1", "2", "4", "8"],
        "question": "Egy nagy kockát 27 kis kockából raktunk össze, majd a külsejét befestettük sárgára. Hány kis "
        "kockának nem maradt egyetlen oldala sem sárga?",
    },
    {
        "class": "2",
        "comment": "A 2. és 8. között 6 különbség van. A kör másik felén is 6 különbség kell legyen, tehát 6 * 2 = 12 "
        "gyerek.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["10", "12", "14", "16", "18"],
        "question": "Peti és barátai körben ülnek. Peti a 2. gyerek, és vele szemben ül a 8. gyerek. Hányan ülnek "
        "összesen a körben, ha mindenki között ugyanakkora a távolság?",
    },
    {
        "class": "2",
        "comment": "23 + 32 = 55. A hiányzó számjegy a 3.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["0", "1", "2", "3", "5"],
        "question": "Melyik számjegyet kell a * helyére tenni, hogy az összeadás helyes legyen: 2* + *2 = 55?",
    },
    {
        "class": "2",
        "comment": "10, 20, 30, 40, 50, 60, 70, 80, 90 (9 db) és a 100 (2 db). Összesen 11.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["9", "10", "11", "12", "20"],
        "question": "Hány darab 0-t kell leírnunk, ha 1-től 100-ig minden egész számot leírunk?",
    },
    {
        "class": "2",
        "comment": "A szám 1-gyel nagyobb, mint 6 többszöröse (mert 2-vel és 3-mal osztva is 1 a maradék). Egynél több cukorka esetén a legkisebb ilyen szám: 7.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Egy zacskóban cukorkák vannak. Ha kettesével vesszük ki, 1 marad. Ha hármasával, akkor is 1 "
        "marad. Legalább hány cukorka van a zacskóban, ha tudjuk, hogy egynél több van benne?",
    },
    {
        "class": "2",
        "comment": "Anna szavaiból látszik, hogy eggyel több lány van, mint fiú. Gábor szavaiból: L = 2(F-1). Mivel "
        "L=F+1, így F+1 = 2F-2, amiből F=3. Tehát 3 fiú és 4 lány van, összesen 7 gyerek.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Anna azt mondja: „Ugyanannyi lánytestvérem van, mint fiú.” Gábor, az Anna öccse viszont azt "
        "mondja: „Kétszer annyi nővérem van, mint bátyám.” Hányan vannak a gyerekek?",
    },
    {
        "class": "2",
        "comment": "Az első ember 3-mal fog kezet, a második már csak 2 újjal, a harmadik 1-gyel. 3+2+1=6.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["4", "5", "6", "8", "10"],
        "question": "Négy barát egy teniszverseny után mindenki mindenkivel kezet fogott egyszer. Hány kézfogás "
        "történt összesen?",
    },
    {
        "class": "2",
        "comment": "Gabi mögött 4-en állnak. Előtte 2*4=8-an. Összesen 8+1+4=13.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["10", "12", "13", "14", "15"],
        "question": "A tornasorban Gabi hátulról az ötödik. Előtte pontosan kétszer annyian állnak, mint mögötte. "
        "Hányan vannak összesen a sorban?",
    },
    {
        "class": "2",
        "comment": "Egy emelet 18 fok. A harmadik emeletig 3 emeletnyi távolságot kell megtenni: 3 * 18 = 54.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["36", "48", "54", "60", "72"],
        "question": "A földszintről az első emeletre 18 lépcsőfok vezet. Hány lépcsőfokot kell megmászni a "
        "földszintről a harmadik emeletre, ha az emeletek között mindenhol ugyanannyi lépcső van?",
    },
    {
        "class": "2",
        "comment": "A két golyó együtt 11-3=8 kg-ot nyom. Egy golyó tehát 4 kg.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2 kg", "3 kg", "4 kg", "5 kg", "8 kg"],
        "question": "Két egyforma golyó és egy 3 kg-os súly egyensúlyban van egy 11 kg-os súllyal a mérlegen. Mennyit "
        "nyom egy golyó?",
    },
    {
        "class": "2",
        "comment": "Ha mindenki tücsök lenne, 8*6=48 láb lenne. A maradék 54-48=6 láb a pókok plusz 2-2 lába. 6/2=3 "
        "pók van.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "A dobozban tücskök (6 lábúak) és pókok (8 lábúak) vannak. Összesen 8 fejet és 54 lábat számoltunk "
        "meg. Hány pók van a dobozban?",
    },
    {
        "class": "2",
        "comment": "Két egymás utáni szám szorzata 110: 10 * 11 = 110. Összegük: 10 + 11 = 21.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["19", "20", "21", "22", "23"],
        "question": "Egy könyvben kinyitottam két egymás melletti oldalt. Az oldalszámok szorzata 110. Mennyi a két "
        "oldalszám összege?",
    },
    {
        "class": "2",
        "comment": "15 / 3 = 5 köz, amihez 6 oszlop szükséges.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "15"],
        "question": "Egy 15 méter hosszú egyenes kerítéshez 3 méterenként kell egy oszlop. Hány oszlop kell összesen, "
        "ha a kerítés mindkét végén is áll egy oszlop?",
    },
    {
        "class": "2",
        "comment": "Reggel 8 és délután 1 között 5 óra telt el. 5 * 2 = 10 percet késett, tehát 12:50-et mutat.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["12:40", "12:48", "12:50", "13:00", "13:10"],
        "question": "Kati órája minden órában 2 percet késik. Reggel 8-kor állították be pontosan. Mit mutat az óra "
        "délután 1 órakor?",
    },
    {
        "class": "2",
        "comment": "Minden hónap legalább 28 napos.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["1", "4", "7", "11", "12"],
        "question": "Hány hónapnak van legalább 28 napja egy évben?",
    },
    {
        "class": "2",
        "comment": "Egy nyuszi három perc alatt egy répát eszik meg. Így hat nyuszi is három perc alatt végez a saját "
        "répájával.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1", "3", "6", "9", "12"],
        "question": "Három nyuszi három perc alatt három répát eszik meg. Hány perc alatt eszik meg hat nyuszi a hat "
        "répát?",
    },
    {
        "class": "2",
        "comment": "Visszafelé: 40 / 2 = 20, majd 20 + 5 = 25.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["15", "20", "25", "30", "35"],
        "question": "Gondoltam egy számra. Levontam belőle 5-öt, az eredményt megdupláztam, és 40-et kaptam. Melyik "
        "számra gondoltam?",
    },
    {
        "class": "2",
        "comment": "Az elektromos vonatnak nincs füstje.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["Északra", "Délre", "Keletre", "Nyugatra", "Nincs füstje"],
        "question": "Egy elektromos vonat észak felé halad, a szél viszont délről fúj. Merre száll a vonat füstje?",
    },
    {
        "class": "2",
        "comment": "Az utolsó előtti helyére lépsz, tehát te leszel az utolsó előtti.",
        "correct": "B",
        "difficulty": "hard",
        "options": [
            "Utolsó",
            "Utolsó előtti",
            "Harmadik",
            "Második",
            "Nem meghatározható",
        ],
        "question": "Ha egy futóversenyen lehagyod az utolsó előtti versenyzőt, hányadik helyen állsz majd?",
    },
    {
        "class": "2",
        "comment": "15 - 5 + 8 = 18 utas. Plusz a sofőr, összesen 19 ember.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["17", "18", "19", "23", "24"],
        "question": "Egy buszon 15 utas van. Hány ember van a buszon összesen a sofőrrel együtt, ha az első megállóban "
        "leszáll 5 ember, és felszáll 8?",
    },
    {
        "class": "2",
        "comment": "Te vagy az egyik, jobbra van 3 gyerek, veled szemben 1, balra 3. 1+3+1+3=8.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Egy kerek asztalnál ülsz. Tőled jobbra a 4. gyerek ugyanaz, mint aki tőled balra a 4. Hányan "
        "ültök összesen az asztalnál?",
    },
    {
        "class": "2",
        "comment": "Ha egy tégla = 1kg + fél tégla, akkor a fél tégla 1kg. Egy egész tégla 2kg. 3 tégla 6kg.",
        "correct": "E",
        "difficulty": "medium",
        "options": ["3 kg", "4 kg", "4,5 kg", "5 kg", "6 kg"],
        "question": "Egy tégla súlya 1 kg meg egy fél tégla. Mennyi három ilyen tégla súlya összesen?",
    },
    {
        "class": "2",
        "comment": "A sarkokat kétszer számolnánk, így 4 * 4 - 4 = 12.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["10", "12", "14", "16", "20"],
        "question": "Egy négyzet alakú kert minden oldalára 4 fát ültettünk úgy, hogy a sarkokon is van egy-egy fa. "
        "Hány fát ültettünk összesen?",
    },
    {
        "class": "2",
        "comment": "Holnapután tegnapelőttje az a mai nap.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Vasárnap"],
        "question": "A naptárban ma kedd van. Mi lesz a holnapután tegnapelőttje?",
    },
    {
        "class": "2",
        "comment": "4. nap végén 8 méteren van. Az 5. napon felmászik 4-et, és eléri a 12 métert.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["3.", "4.", "5.", "6.", "7."],
        "question": "Egy csiga 12 méter mély kútból mászik ki. Nappal 4 métert halad, éjjel 2 métert csúszik vissza. "
        "Hányadik napon ér fel a kút peremére?",
    },
    {
        "class": "2",
        "comment": "A nagyapa egy apa, az apa egy apa és egy fiú, a legkisebb egy fiú. 2 apa, 2 fiú.",
        "correct": "C",
        "difficulty": "hard",
        "options": [
            "Ikrek vannak",
            "Nincs rajta fiú",
            "Nagyapa, Apa és a fia",
            "Két család",
            "Hiba van a kérdésben",
        ],
        "question": "Egy fényképen 2 apa és 2 fiú látható, de mégis csak 3 ember szerepel a képen. Hogyan lehetséges "
        "ez?",
    },
    {
        "class": "2",
        "comment": "200 / 20 = 10 darab lesz, ehhez 9 vágás kell.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["8", "9", "10", "11", "20"],
        "question": "Hány vágással lehet egy 2 méter hosszú szalagot 20 centiméteres darabokra vágni?",
    },
    {
        "class": "2",
        "comment": "6 * 500 + 2 * 1000 = 3000 + 2000 = 5000 bankjegy, és 6+2=8 db.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2", "4", "6", "7", "8"],
        "question": "Ötszáz- és ezerforintos bankjegyekkel összesen 5000 forintom van. Összesen 8 bankjegyem van. Hány "
        "ötszázasom van?",
    },
    {
        "class": "2",
        "comment": "Minden harmadik piros: 3., 6., 9., 12. Összesen 4.",
        "correct": "C",
        "difficulty": "medium",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Egy karkötőt fűzöl. Minden 3. gyöngy piros, a többi fehér. Hány piros gyöngy van egy 12 gyöngyből "
        "álló karkötőben?",
    },
    {
        "class": "2",
        "comment": "Minden szám az előző kétszerese: 24 * 2 = 48.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["30", "36", "40", "48", "60"],
        "question": "Melyik szám következik a sorozatban: 3, 6, 12, 24, ...?",
    },
    {
        "class": "2",
        "comment": "1, 10, 11 (2db), 12, 13, 14, 15, 16, 17, 18, 19, 21. Összesen 13 db.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["10", "11", "12", "13", "14"],
        "question": "Hány darab 1-es számjegyet kell leírnunk összesen 1-től 30-ig?",
    },
    {
        "class": "2",
        "comment": "Kettő lehet különböző. A harmadik már biztosan egyezni fog az egyikkel.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "10"],
        "question": "Egy sötét szobában 5 pár piros és 5 pár kék kesztyű van összekeverve. Legalább hány darab "
        "kesztyűt kell kivenned, hogy biztosan legyen köztük két egyforma színű?",
    },
    {
        "class": "2",
        "comment": "Péternél Mari 3, Anna 5 évvel idősebb. Tehát Anna a legidősebb.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Mari", "Péter", "Anna", "Egyidősek", "Nem meghatározható"],
        "question": "Mari 3 évvel idősebb Péternél, Péter pedig 5 évvel fiatalabb Annánál. Ki a legidősebb?",
    },
    {
        "class": "2",
        "comment": "2, 12, 20. Összesen 3-szor.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Egy kisvárosban a házakat 1-től 20-ig számozták. Hányszor szerepel a 2-es számjegy a "
        "házszámokban?",
    },
    {
        "class": "2",
        "comment": "Az 1. oldal 3-féle, a 2. oldal 2-féle (nem ugyanaz), a 3. oldal 1-féle (nem az 1. és nem a 2. "
        "színű). 3×2×1 = 6.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["3", "6", "9", "12", "18"],
        "question": "Három szín közül választhatsz: piros, kék, zöld. Egy háromszög mindhárom oldalát ki szeretnéd "
        "festeni, de a szomszédos oldalak nem lehetnek ugyanolyan színűek. Hányféleképpen teheted meg?",
    },
    {
        "class": "2",
        "comment": "3 alma = 6 eper → 1 alma = 2 eper. 1 alma + 2 eper = 1 körte → 2+2 = 4 eper = 1 körte.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "A mérleg mindkétszer egyensúlyban van. 3 alma nyom annyit, mint 6 eper. 1 alma és 2 eper nyom "
        "annyit, mint 1 körte. Hány szem eper nyom annyit, mint 1 körte?",
    },
    {
        "class": "2",
        "comment": "Ha a kisebb szám x, akkor x + (x+10) = 50 → 2x = 40 → x = 20. A nagyobb: 30.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["20", "25", "28", "30", "35"],
        "question": "Két szám összege 50, különbségük 10. Melyik a nagyobb szám?",
    },
    {
        "class": "2",
        "comment": "Tízes=1: 10 (1db). Tízes=2: 20,21 (2db). … Tízes=9: 90-98 (9db). 1+2+3+…+9 = 45.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["25", "36", "40", "45", "50"],
        "question": "Hány olyan kétjegyű szám létezik, amelyben a tízesek számjegye nagyobb, mint az egyeseké?",
    },
    {
        "class": "2",
        "comment": "10a+b - (10b+a) = 27 → 9(a-b) = 27 → a-b = 3. Ha a+b = 9 és a-b = 3, akkor a = 6, b = 3. A szám: "
        "63.",
        "correct": "D",
        "difficulty": "medium",
        "options": ["36", "45", "54", "63", "72"],
        "question": "Gondoltam egy kétjegyű számra. Ha felcserélem a számjegyeit, 27-tel kisebb számot kapok. Mennyi "
        "lehetett az eredeti szám, ha a számjegyeinek összege 9?",
    },
    {
        "class": "2",
        "comment": "a+f=50. 5 éve: (a-5)=3(f-5) → a-5=3f-15 → a=3f-10. (3f-10)+f=50 → 4f=60 → f=15.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["10", "12", "14", "15", "16"],
        "question": "Apa és fia együtt 50 évesek. 5 évvel ezelőtt apa háromszor annyi idős volt, mint a fia. Hány éves "
        "a fia most?",
    },
    {
        "class": "2",
        "comment": "Egy 2×2-es négyzet bal felső sarka 3×3 = 9 helyen lehet (1-3 sor, 1-3 oszlop).",
        "correct": "D",
        "difficulty": "hard",
        "options": ["4", "6", "8", "9", "16"],
        "question": "Egy 4×4-es sakktáblán (16 mező) hány 2×2-es négyzet található?",
    },
    {
        "class": "2",
        "comment": "A pirossal szemben bármelyik másik 5 szín állhat felülre (a kockát forgathatjuk). Tehát 5.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Egy kocka minden lapját más színűre festjük (6 szín). Ha a pirosat az asztalra tesszük, hány "
        "különböző színű lap lehet felül?",
    },
    {
        "class": "2",
        "comment": "100 gyertya → 10 gyertya a maradékból → 1 gyertya annak maradékából. 100+10+1 = 111.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["100", "109", "110", "111", "120"],
        "question": "Egy mécsesgyár naponta 100 gyertyát készít. A viaszmaradékból minden 10 elkészült gyertya után 1 "
        "újat lehet önteni. A maradékok maradékából is készíthető gyertya. Hány gyertyát tudnak összesen "
        "készíteni 100 adag viaszból?",
    },
    {
        "class": "2",
        "comment": "Minden meccsen 1 ember esik ki. 99 embert kell kiejteni → 99 meccs.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["50", "64", "99", "100", "128"],
        "question": "Egy versenyen 100 induló van. Kiesés rendszerben, minden meccsen a vesztes kiesik. Hány meccset "
        "kell lejátszani, hogy legyen egy győztes?",
    },
    {
        "class": "2",
        "comment": "Mindenki 6 levelet küld (a többi 6-nak). 7 × 6 = 42. (Nem kézfogás — a leveleknél az irány is "
        "számít!)",
        "correct": "D",
        "difficulty": "hard",
        "options": ["21", "28", "35", "42", "49"],
        "question": "7 barát levelez egymással. Mindenki mindenkinek pontosan egy levelet küld. Hány levelet küldenek "
        "összesen?",
    },
    {
        "class": "2",
        "comment": "100 / 7 = 14 hét és 2 nap. Csütörtök + 2 nap = szombat.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["Hétfő", "Kedd", "Szerda", "Szombat", "Vasárnap"],
        "question": "Ma csütörtök van. 100 nap múlva milyen nap lesz?",
    },
    {
        "class": "2",
        "comment": "Hétfőtől péntekig 4 nap telt el. 4 × 3 = 12 perc sietés. Az óra 8:12-t mutat.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["7:48", "7:52", "8:08", "8:12", "8:15"],
        "question": "Egy óra naponta 3 percet siet. Hétfő reggel 8:00-kor pontosan beállítottuk. Péntek reggel "
        "8:00-kor — a valóságban — mit mutat az óra?",
    },
    {
        "class": "2",
        "comment": "Fibonacci-sorozat: minden szám az előző kettő összege. 5 + 8 = 13.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["10", "11", "12", "13", "15"],
        "question": "Mi a sorozat következő tagja: 1, 1, 2, 3, 5, 8, ...?",
    },
    {
        "class": "2",
        "comment": "Különbségek: 4, 6, 8, 10 → a következő +12. 30+12 = 42. (Vagy: n×(n+1): 1×2, 2×3, 3×4, 4×5, 5×6, "
        "6×7=42.)",
        "correct": "D",
        "difficulty": "hard",
        "options": ["36", "38", "40", "42", "44"],
        "question": "A sorozatban a számok: 2, 6, 12, 20, 30, ... Mi a következő szám?",
    },
    {
        "class": "2",
        "comment": "1+2+9, 1+3+8, 1+4+7, 1+5+6, 2+3+7, 2+4+6, 3+4+5. Összesen 7.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["3", "5", "7", "9", "10"],
        "question": "Három különböző, egyjegyű, nullánál nagyobb szám összege 12. Hányféleképpen választhatjuk ki a "
        "három számot? (A sorrend nem számít.)",
    },
    {
        "class": "2",
        "comment": "Legrosszabb eset: 4 db egy színből + 2+1+1 másokból = 8 labda, de abból csak 1 pár. A 9. labda "
        "biztosítja a 2. párt is.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["5", "6", "7", "8", "9"],
        "question": "Egy zsákban 4 piros, 4 kék, 4 zöld és 4 sárga labda van. Legalább hány labdát kell kivenned "
        "csukott szemmel, hogy biztosan legyen köztük legalább 2 azonos színű pár (azaz legalább 2 szín, "
        "amelyből 2-2 darab van)?",
    },
    {
        "class": "2",
        "comment": "3 jobbra + 3 lefelé lépés kell. Ezek sorrendje: 6!/(3!×3!) = 20.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["6", "10", "15", "20", "24"],
        "question": "Egy 3×3-as rácson az S pontból a C pontba kell eljutnod, de csak jobbra (→) vagy lefelé (↓) "
        "léphetsz. Hányféleképpen tudsz eljutni S-ből C-be?",
    },
    {
        "class": "2",
        "comment": "Jegy-halmazok: {1,2,3}→6db, {0,1,5}→4db (0 nem lehet az első), {0,2,4}→4db. Összesen 6+4+4 = 14.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["6", "10", "12", "14", "18"],
        "question": "Egy papírlapra írsz egy háromjegyű számot. Minden jegye különböző, és a jegyek összege 6. Hány "
        "ilyen háromjegyű szám létezik?",
    },
    {
        "class": "2",
        "comment": "Az 1. sorból 1-et fehérre cserélünk úgy, hogy az a 4. sor oszlopába essen → mindkét sor rendben "
        "lesz. 1 csere elég.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Egy 4×4-es rácsban fekete és fehér golyók vannak. Legkevesebb hány golyó színét kell "
        "megváltoztatni, hogy MINDEN sorban és MINDEN oszlopban pontosan 2 fekete golyó legyen, ha "
        "jelenleg az 1. sorban 3, a 2. sorban 2, a 3. sorban 2, a 4. sorban 1 fekete golyó van?",
    },
    {
        "class": "2",
        "comment": "Ha kiveszünk 3 zoknit, lehet, hogy mind különböző színű (piros, kék, zöld). A negyedik zokni "
        "biztosan valamelyik színű lesz a már kivettek közül, így lesz egy pár.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["3", "4", "5", "6", "7"],
        "question": "Egy fiókban 5 pár piros, 5 pár kék és 5 pár zöld zokni van összekeveredve. Legalább hány darab "
        "zoknit kell kivennünk csukott szemmel ahhoz, hogy biztosan legyen köztük egy egyszínű pár?",
    },
    {
        "class": "2",
        "comment": "Kati nem 1. és nem 2., tehát Kati a 3. Peti nem 1., és a 3. már foglalt, így Peti a 2. Marad az 1. "
        "hely Sanyinak.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["Első", "Második", "Harmadik", "Negyedik", "Nem lehet tudni"],
        "question": "Peti, Kati és Sanyi futóversenyen indultak. Peti nem lett az első. Kati nem lett a második, és "
        "nem is ő nyert. Hányadik lett Sanyi?",
    },
    {
        "class": "2",
        "comment": "20 - 2 = 18 gyerek sportol. Focizik + Kosarazik = 12 + 10 = 22. Ez 4-gyel több, mint 18, tehát "
        "4-en mindkettőt szeretik.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Az osztályban 20 tanuló van. 12-en szeretnek focizni, 10-en kosarazni. 2-en egyik sportot sem "
        "szeretik. Hányan szeretik mindkettőt?",
    },
    {
        "class": "2",
        "comment": "50 napban van 7 teljes hét (7 * 7 = 49 nap) és még 1 nap. 49 nap múlva újra szerda lenne, +1 nap "
        "az csütörtök.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"],
        "question": "Ma szerda van. Milyen nap lesz 50 nap múlva?",
    },
    {
        "class": "2",
        "comment": "9 db kicsi (1x1), 4 db közepes (2x2) és 1 db nagy (3x3). Összesen: 9 + 4 + 1 = 14.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["9", "10", "13", "14", "15"],
        "question": "Egy 3x3-as négyzetrácsban hány négyzet látható összesen (bármekkora méretű)?",
    },
    {
        "class": "2",
        "comment": "A számok: 14, 23, 32, 41, 50. Ez összesen 5 darab.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["3", "4", "5", "6", "7"],
        "question": "Hány olyan kétjegyű szám van, amelyben a számjegyek összege 5?",
    },
    {
        "class": "2",
        "comment": "Ha Anna ad 2 almát Bélának, akkor egyenlők lesznek: A-2 = B+2, tehát A-B = 4. Mivel együtt 16 almájuk van, A+B = 16. Innen A = 10.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Annának és Bélának összesen 16 almája van. Ha Anna ad Bélának 2 almát, akkor ugyanannyi almájuk "
        "lesz. Hány almája volt Annának eredetileg?",
    },
    {
        "class": "2",
        "comment": "A végén mindkettőnek 10-10 lesz. Anna adott 2-t, tehát előtte 10+2=12 volt neki.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["8", "10", "12", "14", "16"],
        "question": "Annának és Bélának összesen 20 almája van. Ha Anna ad Bélának 2 almát, akkor ugyanannyi almájuk "
        "lesz. Hány almája volt Annának eredetileg?",
    },
    {
        "class": "2",
        "comment": "Előtte 6, mögötte 7 gyerek áll. Összesen: 6 + 1 (Misi) + 7 = 14.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["13", "14", "15", "16", "17"],
        "question": "Egy sorban gyerekek állnak. Misi elölről a 7., hátulról a 8. Hány gyerek áll a sorban?",
    },
    {
        "class": "2",
        "comment": "Hétfő reggel 10 Ft van benne. Mivel minden reggel duplázódik: kedd 20, szerda 40, csütörtök 80, péntek 160. Először pénteken lesz 100 Ft-nál több.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"],
        "question": "Egy bűvös doboz minden reggel megduplázza a benne lévő pénzt. Hétfő reggel betettünk 10 Ft-ot. "
        "Mikor lesz a dobozban először több mint 100 Ft?",
    },
    {
        "class": "2",
        "comment": "Hétfő este: 10. Kedd este: 20. Szerda este: 40. Csütörtök este: 80. Tehát csütörtök.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"],
        "question": "Egy bűvös dobozban minden nap végére kétszer annyi érme lesz, mint reggel volt. Hétfő reggel 5 "
        "érme volt benne. Melyik nap végére lesz benne először több mint 50 érme?",
    },
    {
        "class": "2",
        "comment": "4 kis háromszög (negyedek). Bármelyik kettő szomszédos is kiad egy nagyobbat (a négyzet fele), "
        "ebből van 4. Összesen 4+4=8.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["4", "5", "6", "8", "10"],
        "question": "Hány háromszög látható az alábbi leírás alapján: Egy négyzetet mindkét átlója mentén átvágtunk.",
    },
    {
        "class": "2",
        "comment": "Becsapós kérdés! Amelyiket elfújta, az megmarad. A többi tövig leég. Tehát 3 maradt meg.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["3", "5", "8", "0", "11"],
        "question": "Kati születésnapi tortáján 8 gyertya égett. Elfújt belőle 3-at. Hány gyertya maradt meg (nem "
        "égett le)?",
    },
    {
        "class": "2",
        "comment": "Az első helyre 2, a másodikra 2, a harmadikra 2 szám kerülhet. 2 * 2 * 2 = 8. (111, 112, 121, 122, "
        "211, 212, 221, 222).",
        "correct": "C",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Hány olyan háromjegyű szám van, amit csak az 1 és 2 számjegyekből írunk fel?",
    },
    {
        "class": "2",
        "comment": "Ha a lány most 10 éves, anya 30. 10 év múlva lány 20, anya 40. 40 pont a kétszerese 20-nak. Tehát "
        "10 éves.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["8", "10", "12", "15", "20"],
        "question": "Anya most háromszor annyi idős, mint a lánya. 10 év múlva kétszer annyi idős lesz. Hány éves most "
        "a lánya?",
    },
    {
        "class": "2",
        "comment": "A különbségek nőnek: +1, +2, +3, +4. A következő különbség +5 lesz. 11 + 5 = 16.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["14", "15", "16", "17", "18"],
        "question": "Mi a következő szám a sorozatban: 1, 2, 4, 7, 11, ...?",
    },
    {
        "class": "2",
        "comment": "Reggel 8-tól este 8-ig 12 óra telik el. 12 * 2 = 24 percet késik.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["12 perc", "20 perc", "24 perc", "30 perc", "48 perc"],
        "question": "Egy óra minden órában 2 percet késik. Reggel 8-kor pontosra állítottuk. Hány percet késik "
        "összesen este 8-kor?",
    },
    {
        "class": "2",
        "comment": "Kati előtt 9-en vannak, Kati után is 9-en. Összesen: 9 + 1 (Kati) + 9 = 19.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["18", "19", "20", "21", "22"],
        "question": "Egy sorban állnak a gyerekek. Ha balról számoljuk, Kati a 10. Ha jobbról számoljuk, akkor is a "
        "10. Hány gyerek áll a sorban?",
    },
    {
        "class": "2",
        "comment": "Első hajtás: 2 réteg. Második hajtás: 4 réteg. Harmadik hajtás: 8 réteg.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["3", "4", "6", "8", "12"],
        "question": "Egy papírlapot háromszor félbehajtottunk. Hány réteg papír van most egymáson?",
    },
    {
        "class": "2",
        "comment": "Párba állítás: 5-tel 4 pár, 10-zel 3 pár (amit nem számoltunk), 20-szal 2 pár, 50-nel 1 pár. "
        "4+3+2+1=10.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["5", "8", "9", "10", "15"],
        "question": "Van ötféle érménk: 5, 10, 20, 50, 100 Ft. Hányféle összeget tudunk kifizetni pontosan két "
        "különböző érmével?",
    },
    {
        "class": "2",
        "comment": "15 + 12 - 8 = 19. (Mert a 8 közös gyereket kétszer számoltuk, egyszer le kell vonni).",
        "correct": "B",
        "difficulty": "hard",
        "options": ["15", "19", "20", "27", "35"],
        "question": "A sportkörben 15-en úsznak, 12-en futnak. Mindenki sportol valamit. 8-an mindkettőt csinálják. "
        "Hány gyerek jár a sportkörbe?",
    },
    {
        "class": "2",
        "comment": "Naponta 1 métert halad (3-2). 7 nap alatt 7 méteren van. A 8. nap reggelén felmászik 3 métert, "
        "eléri a 10-et és kiér (nem csúszik vissza).",
        "correct": "B",
        "difficulty": "hard",
        "options": ["7", "8", "9", "10", "11"],
        "question": "Egy csiga nappal 3 métert mászik fel a falon, éjjel 2 métert csúszik vissza. Hány nap alatt ér "
        "fel a 10 méter magas fal tetejére?",
    },
    {
        "class": "2",
        "comment": "Először mérjünk 3-3 golyót. Ha egyenlő, a maradék 2 közül az egyik a könnyebb (második mérés). Ha "
        "valamelyik 3-as csoport könnyebb, mérjünk abból 1-1-et. Ha egyenlő, a harmadik a könnyebb. Ha nem, "
        "akkor a könnyebbik. Tehát 2 mérés elég.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Van egy serpenyős mérlegünk és 8 egyforma kinézetű golyónk. Az egyik kicsit könnyebb a többinél. "
        "Hányszor kell mérnünk a mérleggel, hogy biztosan megtaláljuk a könnyebbet?",
    },
    {
        "class": "2",
        "comment": "A szó 44 betűből áll.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["40", "42", "44", "45", "50"],
        "question": "Hány betűs a 'MEGSZENTSÉGTELENÍTHETETLENSÉGESKEDÉSEITEKÉRT' szó?",
    },
    {
        "class": "2",
        "comment": "Ha mind motor lenne: 10 * 2 = 20 kerék. Hiányzik 16 kerék. Minden autó 2-vel több kereket ad. 16 / "
        "2 = 8 autó. Ellenőrzés: 8 autó (32 kerék) + 2 motor (4 kerék) = 36 kerék.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["6", "7", "8", "9", "10"],
        "question": "Egy parkolóban autók és motorok állnak. Összesen 10 jármű és 36 kerék van. Hány autó van a "
        "parkolóban?",
    },
    {
        "class": "2",
        "comment": "4 kicsi, 2 vízszintes kettes, 2 függőleges kettes, 1 nagy. Összesen: 4 + 2 + 2 + 1 = 9.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["4", "5", "8", "9", "10"],
        "question": "Hány téglalap látható ezen az ábrán, ha egy nagy téglalapot egy vízszintes és egy függőleges "
        "vonallal négy kisebb téglalapra osztunk?",
    },
    {
        "class": "2",
        "comment": "Mindenki öregszik 5 évet. 3 gyerek van, tehát 3 * 5 = 15 évvel nő az összeg. 20 + 15 = 35.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["25", "30", "35", "40", "45"],
        "question": "Három testvér életkorának összege 20 év. Hány év lesz a három testvér életkorának összege 5 év "
        "múlva?",
    },
    {
        "class": "2",
        "comment": "A vonatnak meg kell tennie a saját hosszát + az alagút hosszát, hogy a vége is kiérjen. 100 + 100 "
        "= 200 méter. 200 / 100 = 2 perc.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["1 perc", "2 perc", "3 perc", "4 perc", "5 perc"],
        "question": "Egy vonat hossza 100 méter. Egy 100 méter hosszú alagúton halad át 100 méter/perc sebességgel. "
        "Mennyi idő alatt ér át teljesen az alagúton?",
    },
    {
        "class": "2",
        "comment": "Laci és Feri állításai egymás ellentétei: egyik szerint Feri hazudik, a másik szerint Laci hazudik. A feltételek alapján nem dönthető el egyértelműen, hogy közülük ki az igazmondó.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["Laci", "Feri", "Mindkettő", "Egyik sem", "Nem lehet tudni"],
        "question": "Két testvér, Laci és Feri közül az egyik mindig igazat mond, a másik mindig hazudik. Laci azt "
        "mondja: 'A testvérem mindig hazudik'. Feri azt mondja: 'Laci mindig hazudik'. Ki mond "
        "igazat?",
    },
    {
        "class": "2",
        "comment": "Ha A igazmondó lenne, akkor igaz lenne, hogy 'mindketten hazugok', tehát ő is hazug lenne. Ez "
        "ellentmondás. Tehát A biztosan hazug. Ha A hazug, akkor az állítása ('mindketten hazugok') hamis. "
        "Tehát nem mindketten hazugok. Mivel A hazug, ezért B-nek igazmondónak kell lennie.",
        "correct": "D",
        "difficulty": "hard",
        "options": [
            "A és B is hazug",
            "A és B is igazmondó",
            "A igazmondó, B hazug",
            "A hazug, B igazmondó",
            "Nem lehet tudni",
        ],
        "question": "Egy szigeten kétféle ember él: az igazmondók (mindig igazat mondanak) és a hazugok (mindig "
        "hazudnak). Találkozol két emberrel, A-val és B-vel. A azt mondja: 'Mindketten hazugok vagyunk'. "
        "Milyen ember A és B?",
    },
    {
        "class": "2",
        "comment": "Tegyük fel, hogy Aranyban van. Akkor: Arany felirat IGAZ ('itt van'). Ezüst felirat IGAZ ('nem itt "
        "van', mert Aranyban van). Két igaz lenne -> NEM JÓ. Tegyük fel, hogy Bronzban van. Arany felirat "
        "HAMIS. Ezüst felirat IGAZ ('nem itt'). Bronz felirat IGAZ ('nem Aranyban'). Két igaz -> NEM JÓ. "
        "Tegyük fel, hogy Ezüstben van. Arany felirat HAMIS ('nincs ott'). Ezüst felirat HAMIS ('itt van' a "
        "valóság, de felirat: 'nem itt'). Bronz felirat IGAZ ('nem Aranyban'). Csak 1 igaz van! Tehát a "
        "kincs az Ezüstben van.",
        "correct": "B",
        "difficulty": "hard",
        "options": [
            "Az Aranyban",
            "Az Ezüstben",
            "A Bronzban",
            "Mindegyikben",
            "Egyikben sem",
        ],
        "question": "Három doboz van előttünk: Arany, Ezüst és Bronz. Az egyikben kincs van. A dobozokon feliratok "
        "vannak, de csak EGY felirat igaz.\n"
        "Arany: 'A kincs itt van.'\n"
        "Ezüst: 'A kincs nem itt van.'\n"
        "Bronz: 'A kincs nem az Aranyban van.'\n"
        "Hol van a kincs?",
    },
    {
        "class": "2",
        "comment": "Béla nem dob, nem zongora -> Béla hegedül. Anna nem zongora, (hegedű foglalt) -> Anna dobol. Cili "
        "zongorázik. Tehát Anna dobol.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["Anna", "Béla", "Cili", "Nem lehet tudni", "Senki"],
        "question": "Három barát: Anna, Béla és Cili háromféle hangszeren játszik: hegedű, zongora és dob. Mindenki "
        "csak egy hangszeren játszik. Anna nem zongorázik. Béla nem dobol és nem zongorázik. Ki játszik a "
        "dobon?",
    },
    {
        "class": "2",
        "comment": "Nagy úr lakik Kovács úr alatt -> Tehát Kovács nem lehet az 1., és Nagy nem lehet a 3. Kovács nem "
        "3. (megadva). Tehát Kovács csak a 2. lehet (mert 1. nem lehet, mert van alatta valaki). Ha Kovács "
        "2., akkor Nagy 1. Szabó maradt a 3. (ami stimmel, mert nem legalsó). Tehát a 2. emeleten Kovács úr "
        "lakik.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["Kovács úr", "Szabó úr", "Nagy úr", "Senki", "Nem lehet tudni"],
        "question": "Egy háromemeletes házban lakik Kovács úr, Szabó úr és Nagy úr (az 1., 2. és 3. emeleten). Kovács "
        "úr nem a legfelsőn lakik. Szabó úr nem a legalsón lakik. Nagy úr lakik Kovács úr alatt. Ki lakik "
        "a 2. emeleten?",
    },
    {
        "class": "2",
        "comment": "A feltételek szerint a szám páros, 16-nál nagyobb, 20-nál kisebb, és osztható 3-mal. Ezek közül csak a 18 felel meg.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["12", "14", "15", "16", "18"],
        "question": "Gondoltam egy számra. A szám páros. Nagyobb, mint 16, de kisebb, mint 20. Osztható 3-mal. Melyik "
        "ez a szám?",
    },
    {
        "class": "2",
        "comment": "12-nél nagyobb, tehát 12 nem jó. 14 nem osztható 3-mal. 15 nem páros. 18 páros és osztható 3-mal. "
        "20 nem jó.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["12", "14", "15", "18", "20"],
        "question": "Gondoltam egy számra. A szám páros. Nagyobb, mint 12, de kisebb, mint 22. Osztható 3-mal. Melyik "
        "ez a szám?",
    },
    {
        "class": "2",
        "comment": "Felső: P. Középső: F vagy Z (2 lehetőség). Alsó: Ha közép F -> P vagy Z (2). Ha közép Z -> P vagy "
        "F (2). Összesen 2 * 2 = 4 lehetőség. (P-F-P, P-F-Z, P-Z-P, P-Z-F).",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Zászlót színezünk 3 vízszintes sávval. Piros, fehér és zöld színeket használhatunk. Minden sávot "
        "ki kell színezni, és két egymás melletti sáv nem lehet egyforma színű. Hányféle zászlót "
        "készíthetünk, ha a felső sáv biztosan PIROS?",
    },
    {
        "class": "2",
        "comment": "D az utolsó (4.). A nem szélen -> A a 2. vagy 3. B közvetlenül C mögött -> (C, B) pár. Mivel D a "
        "4., a (C, B) pár csak az 1-2. helyen vagy 2-3. helyen lehet. Ha 2-3., akkor A lenne az 1. (szélen) "
        "- ez tilos. Tehát (C, B) az 1-2. helyen van. C az első. A a 3., D a 4.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["A", "B", "C", "D", "Nem lehet tudni"],
        "question": "Négy gyerek (A, B, C, D) sorban áll. A nem áll a szélen. B közvetlenül C mögött áll. D az utolsó. "
        "Ki áll az első helyen?",
    },
    {
        "class": "2",
        "comment": "A szám 2-vel, 3-mal és 5-tel osztva is 1 maradékot ad. Tehát a szám-1 osztható 2-vel, 3-mal, "
        "5-tel. A legkisebb közös többszörös (2,3,5) = 30. Tehát a szám 30 + 1 = 31.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["11", "16", "21", "31", "41"],
        "question": "Egy kosárban almák vannak. Ha kettesével veszem ki, 1 marad. Ha hármasával, akkor is 1 marad. Ha "
        "ötösével, akkor is 1 marad. Legalább hány alma van a kosárban?",
    },
    {
        "class": "any",
        "comment": "Ha az arany az 1. ládában lenne: 1. felirat igaz, 2. felirat igaz, 3. felirat hamis. (2 igaz)\n"
        "Ha az arany a 2. ládában lenne: 1. felirat hamis, 2. felirat hamis, 3. felirat igaz. (1 igaz) -> "
        "Ez a megoldás.\n"
        "Ha az arany a 3. ládában lenne: 1. felirat hamis, 2. felirat igaz, 3. felirat igaz. (2 igaz)",
        "correct": "B",
        "difficulty": "hard",
        "options": [
            "1. láda",
            "2. láda",
            "3. láda",
            "Mindegyikben lehet",
            "Egyikben sem lehet",
        ],
        "question": "Három ládikó közül az egyikben arany van, a másik kettő üres. Mindegyik ládikón van egy-egy "
        "felirat, de tudjuk, hogy a feliratok közül pontosan egy igaz.\n"
        "1. láda: Az arany ebben a ládában van.\n"
        "2. láda: Az arany nem ebben a ládában van.\n"
        "3. láda: Az arany nem az első ládában van.\n"
        "Melyik ládában van az arany?",
    },
    {
        "class": "any",
        "comment": "A lehetséges számjegyek kombinációi (sorrendtől eltekintve):\n"
        "- {9, 9, 7}: 997, 979, 799 (3 darab)\n"
        "- {9, 8, 8}: 988, 898, 889 (3 darab)\n"
        "Összesen: 3 + 3 = 6.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "8"],
        "question": "Hány olyan háromjegyű pozitív egész szám van, amelyben a számjegyek összege pontosan 25?",
    },
    {
        "class": "2",
        "comment": "A számok: 102, 111, 120, 201, 210, 300. Összesen 6.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["1", "2", "4", "5", "6"],
        "question": "Hány olyan háromjegyű pozitív egész szám van, melyben a számjegyek összege 3?",
    },
    {
        "class": "2",
        "comment": "Legyen x a középső fok. x - 8 + 14 - 18 = 1 => x = 13. A fokok száma: 2 * 13 - 1 = 25.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["18", "24", "25", "26", "27"],
        "question": "Egy tűzoltó a létra középső fokán áll. 8 fokkal lejön, majd 14 fokkal felmászik. Innen 18 fokot "
        "lefelé haladva jut el a legalsó fokra. Hány fok van a létrán?",
    },
    {
        "class": "2",
        "comment": "Mesi: 8 * 25 - 14 = 186. Misi: (186 - 5) - 5 = 176. Összesen: 186 + 176 = 362.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["176", "181", "352", "362", "367"],
        "question": "Mesi mókusnak 14 szem dió hiányzik a 8 teli 25-ös zsákhoz. Ha 5-öt adna Misinek, ugyanannyi "
        "diójuk lenne. Hány diójuk van összesen?",
    },
    {
        "class": "2",
        "comment": "Ha egy mond igazat, akkor 4 hazudik. Ezt egyedül Vadócka állítja, tehát ő mond igazat.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["Törpiri", "Törpörgő", "Törtyögő", "Vadócka", "Zöldőr"],
        "question": "Öt törpifjonc közül csak egy mondott igazat. Törpiri: 1 hazudik. Törpörgő: 2 hazudik. Törtyögő: 3 "
        "hazudnak. Vadócka: Rajtam kívül mindenki hazudik. Zöldőr: Mind az öten hazudunk. Ki mondott "
        "igazat?",
    },
    {
        "class": "2",
        "comment": "Betűkódolás: S:P, E:Á, J:V, T:A, V:F, Á:É, R:K. VÉKA visszafejtve: JÁRT.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["FEJT", "JÁRT", "JÁVA", "PÁRT", "VERT"],
        "question": "Peti összecserélte a billentyűket. SEJT -> PÁVA, VÁR -> FÉK. Melyik szót gépelte be, ha a "
        "képernyőn a VÉKA szó jelent meg?",
    },
    {
        "class": "2",
        "comment": "20 -> 40 -> 80 -> 160. Tehát 160 éves volt, 160 - 20 = 140 évet fiatalodott.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["40", "60", "100", "140", "160"],
        "question": "A tündérkirálynő 3 kortyot ivott a fiatalító vízből, és újra 20 éves lett. Hány évet fiatalodott, "
        "ha minden korty után felére csökkent az évei száma?",
    },
    {
        "class": "2",
        "comment": "Ha 6 volt, akkor az öccse állítása igaz (6 > 5), de Annáé nem (6 nem > 6). Ezért 6 vendég volt.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["4", "5", "6", "7", "Nem meghatározható"],
        "question": "Anna: 'hatnál több vendég volt'. Öccse: 'ötnél több vendég volt'. Csak egyikük állítása igaz. "
        "Hány vendég volt?",
    },
    {
        "class": "2",
        "comment": "Tavaly 8, idén 9, jövőre 10 éves lesz.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["2", "8", "9", "10", "18"],
        "question": "Katica tavaly február 16-án lett 8 éves. Hány éves lesz Katica jövőre február 16-án?",
    },
    {
        "class": "2",
        "comment": "x + 8 - 5 = 10 => x + 3 = 10 => x = 7.",
        "correct": "B",
        "difficulty": "hard",
        "options": ["3", "7", "13", "18", "23"],
        "question": "A villamosra az utolsó előtti megállóban felszállt 8 utas, és leszállt 5. Az utolsóban leszállt a "
        "villamoson lévő mind a 10 utas. Hány utas volt a villamoson az utolsó előtti megálló előtt?",
    },
    {
        "class": "2",
        "comment": "Két lehetőség van: (Lili, Barna, Piroska) vagy (Barna, Piroska, Lili) jelmezsorrend.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Piroska, Lili és Barna piros, lila és barna jelmezt húztak. Senki sem a nevükhöz illő színt vette "
        "fel. Hányféleképpen öltözhettek fel?",
    },
    {
        "class": "2",
        "comment": "10. (rossz) + 8 (jó) + utolsó (19., rossz). Összesen 19.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["9", "10", "17", "18", "19"],
        "question": "Kati palacsintát sütött. Csak a tizedik és az utolsó szakadt el. A kettő között nyolc szépet "
        "sütött. Hány palacsintát sütött összesen?",
    },
    {
        "class": "4",
        "comment": "N/5 = N/7 + 10 => 2N/35 = 10 => N = 175. Számjegyek összege: 1+7+5 = 13.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["7", "8", "9", "13", "15"],
        "question": "Dani ötösével, Jáni hetesével köti össze kártyáit. Daninak 10-zel több csomagja lett. "
        "Egyikőjüknek sem maradt ki kártyája. Mennyi Dani kártyái számában a számjegyek összege?",
    },
    {
        "class": "2",
        "comment": "x + 4x = 100 => 5x = 100 => x = 20. Nem fájó: 4 * 20 = 80.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["20", "25", "60", "75", "80"],
        "question": "Egy bicegő százlábú így panaszkodik: 'Fájó lábaim száma éppen egynegyed része a nem fájó lábaim "
        "számának.' Hány lába nem fáj a százlábúnak?",
    },
    {
        "class": "4",
        "comment": "A 6 gyerek között 5 időköz van: 5 * 3 = 15 év. 36 - 15 = 21 éves volt az elsőnél.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["17", "18", "19", "20", "21"],
        "question": "Egy anya 36 éves volt, amikor hatodik gyermeke született. A gyerekek között 3 év korkülönbség "
        "van. Hány éves volt az anya az első születésekor?",
    },
    {
        "class": "2",
        "comment": "u-2 = s+2 => u-s = 4. u+s = 14 => 2u = 18 => u = 9.",
        "correct": "E",
        "difficulty": "hard",
        "options": ["5", "6", "7", "8", "9"],
        "question": "A 14 fejű sárkány vezérének néhány feje megsérült. Ha kettővel több sérült volna meg, annyi "
        "sértetlenje lenne, mint sérült. Hány sértetlen feje maradt?",
    },
    {
        "class": "2",
        "comment": "K=2(B+G), K+B+G=9 => 3(B+G)=9 => B+G=3. Lábak: 4B+2G=10 => 2B+G=5. Kivonva: B=2, G=1.",
        "correct": "A",
        "difficulty": "hard",
        "options": ["1", "2", "3", "4", "5"],
        "question": "Mocsárban kígyók, békák és gólyák vannak. Összesen 9 fej és 10 láb. Kígyók száma kétszerese a "
        "többinek együtt. Hány gólya van?",
    },
    {
        "class": "2",
        "comment": "Betűpárok: S:T, Á:U, L:D, R:K, Ó:É, K:R, A:I. FUKAR visszafejtve: PÁROK.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["KÁROK", "KÁROS", "PÁROK", "PÁROM", "PÁROS"],
        "question": "Peti billentyűi: SÁL -> TUD, RÓKA -> KÉRI. Melyik szót gépelte be, ha a képernyőn a FUKAR szó "
        "jelent meg?",
    },
    {
        "class": "2",
        "comment": "Öt péntek lehet: 3, 10, 17, 24, 31. Összegük: 85.",
        "correct": "D",
        "difficulty": "hard",
        "options": ["46", "71", "78", "85", "92"],
        "question": "Törpilla minden pénteken annyi virágot kap, ahanyadika van. Mennyi a kapott virágok száma egy "
        "hónapban, ha a lehető legnagyobb?",
    },
    {
        "class": "2",
        "comment": "Ha Tréfi nyert, akkor Ügyi igazat mond, Törpilla és Tréfi hazudik, Okoska hazudik. Ez 1 igaz. Ha "
        "más nyert, több igaz is lehet.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["Okoska", "Törpilla", "Tréfi", "Ügyi", "Nem meghatározható"],
        "question": "Tréfi, Okoska, Ügyi és Törpilla versenyeztek. Csak egy mondott igazat. Törpilla: Nem Tréfi. Ügyi: "
        "Tréfi nyert. Okoska: Törpilla nyert. Tréfi: Nem én. Ki nyert?",
    },
    {
        "class": "2",
        "comment": "P: 17+7=24, K: 17-7=10. Különbség: 14.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["7", "10", "14", "17", "24"],
        "question": "Gombóc Artúr kék és piros dobozában is 17 csoki van. Áttesz 7-et kékből pirosba. Mennyivel lett "
        "több a pirosban?",
    },
    {
        "class": "2",
        "comment": "Legalább 2 fiú és 2 lány kell. Összesen 4.",
        "correct": "C",
        "difficulty": "hard",
        "options": ["2", "3", "4", "5", "6"],
        "question": "Hány gyermek van abban a családban, ahol mindenki legalább egy fiú és egy lány testvérrel "
        "rendelkezik?",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Sorban állásnál Zsófi elölről a 3., hátulról a 4. Hányan állnak a sorban?",
        "options": ["5", "6", "7", "8", "9"],
        "comment": "Zsofi a 3., tehát előtte 2-en vannak. Hátulról a 4., mögötte 3-an. Összesen: 2 (előtte) + 1 (Zsófi) + 3 (mögötte) = 6.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy könyvet olvasok. A 12. oldalnál tartok, és tegnap a 8. oldalnál kezdtem. Hány oldalt olvastam el eddig a könyvből (ha a 8. és a 12. oldalt is beleszámoljuk)?",
        "options": ["3", "4", "5", "6", "7"],
        "comment": "Megszámolva: 8, 9, 10, 11, 12. Ez pontosan 5 oldal.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy szalagot 4 helyen vágtunk el ollóval. Hány darab szalagunk lett így?",
        "options": ["3", "4", "5", "6", "10"],
        "comment": "Minden vágás növeli a darabok számát. 1 vágás = 2 darab, 4 vágás = 5 darab.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Holnapután szerda lesz. Milyen nap volt tegnapelőtt?",
        "options": ["Péntek", "Szombat", "Vasárnap", "Hétfő", "Kedd"],
        "comment": "Ha holnapután szerda, akkor ma hétfő van. Hétfő előtt tegnapelőtt szombat volt.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy udvaron 2 kutya és 3 tyúk van. Hány lábuk van összesen?",
        "options": ["10", "12", "14", "16", "18"],
        "comment": "2 kutya = 8 láb. 3 tyúk = 6 láb. 8 + 6 = 14 láb.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Egy családban 3 lánytestvér van. Minden lánynak van 1 fiútestvére. Hány gyerek van összesen a családban?",
        "options": ["3", "4", "5", "6", "7"],
        "comment": "Az az 1 fiú mindhárom lánynak a testvére. Összesen 3 lány + 1 fiú = 4 gyerek.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy négyzet alakú papírlapot az egyik sarkától a szemközti sarkáig (átlósan) kettévágunk. Milyen alakzatokat kapunk?",
        "options": [
            "2 téglalapot",
            "2 négyzetet",
            "2 háromszöget",
            "4 háromszöget",
            "1 háromszöget és 1 téglalapot",
        ],
        "comment": "Az átlós vágás két egyforma háromszögre osztja a négyzetet.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Petinek 8 évesen feleannyi idős volt a húga, mint ő. Peti most 12 éves. Hány éves a húga?",
        "options": ["4", "6", "8", "10", "12"],
        "comment": "Amikor Peti 8 volt, a húga 4, tehát a korkülönbség 4 év. Most, hogy Peti 12, a húga 12 - 4 = 8 éves.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Anna magasabb, mint Béla, de alacsonyabb, mint Csaba. Ki a legmagasabb hármuk közül?",
        "options": ["Anna", "Béla", "Csaba", "Egyforma magasak", "Nem lehet tudni"],
        "comment": "Csaba > Anna > Béla. Így Csaba a legmagasabb.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "D",
        "question": "Egy lift a 2. emeletről indul. Felmegy 3 emeletet, majd leereszkedik 1 emeletet. Hányadik emeleten van most?",
        "options": ["1.", "2.", "3.", "4.", "5."],
        "comment": "2. emeletről 3 fel = 5. emelet. 1 le = 4. emelet.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Ha 3 gyerek egyszerre fog kezet mindenkivel, hány kézfogás történik összesen?",
        "options": ["1", "2", "3", "4", "6"],
        "comment": "Az első kezet fog a másik kettővel (2 kézfogás). A második már csak a harmadikkal (1 kézfogás). 2 + 1 = 3.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy fiókban 3 pár piros és 2 pár kék zokni van. Hány darab zokni van a fiókban összesen?",
        "options": ["5", "8", "10", "12", "15"],
        "comment": "Összesen 5 pár zokni van, ami páronként 2 darab, azaz 5 * 2 = 10 darab zokni.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "A",
        "question": "Peti gyorsabban fut, mint Gergő. Tomi lassabban fut, mint Gergő. Ki a leggyorsabb?",
        "options": ["Peti", "Gergő", "Tomi", "Egyformán gyorsak", "Nem lehet tudni"],
        "comment": "Peti gyorsabb Gergőnél, Gergő pedig Tominál. Tehát Peti a leggyorsabb.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Egy futóversenyen megelőzöd a 2. helyen futó versenyzőt. Hányadik helyen futsz most?",
        "options": ["1.", "2.", "3.", "Utolsó", "Nem lehet tudni"],
        "comment": "Ha megelőzöd a másodikat, akkor te veszed át az ő helyét, tehát te leszel a 2.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Egy kerítés 3 egyforma szakaszát 30 perc alatt festi le Tomi. Hány percig tart neki lefesteni 1 szakaszt?",
        "options": ["5", "10", "15", "20", "30"],
        "comment": "Ha 3 szakasz 30 perc, akkor 1 szakasz 30 / 3 = 10 perc.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Egy sötét szobában a fiókban 5 fekete és 5 fehér zokni van összekeveredve. Legalább hány zoknit kell kivenned, hogy biztosan legyen egy egyforma pár?",
        "options": ["2", "3", "5", "6", "10"],
        "comment": "Ha kiveszel kettőt, lehetnek felemásak. De a harmadik már biztosan passzolni fog az egyikhez, mert csak 2 szín van.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "A",
        "question": "A szárítókötélen 1 póló 1 óra alatt szárad meg. Hány óra alatt szárad meg 5 póló, ha mindet egyszerre teregetik ki?",
        "options": ["1", "2", "3", "4", "5"],
        "comment": "Ha egyszerre száradnak, akkor ugyanúgy 1 óra kell mindegyiknek.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Egy vonatban a büfékocsi elölről számolva a 3., hátulról számolva a 4. kocsi. Hány kocsiból áll a vonat?",
        "options": ["5", "6", "7", "8", "9"],
        "comment": "3 (elölről) + 4 (hátulról) - 1 (maga a büfékocsi) = 6.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy 10 fokos lépcsőn állsz az 1. fokon. Felmész 4-et, majd lemész 2-t, és újra felmész 3-at. Hányadik lépcsőfokon állsz?",
        "options": ["4.", "5.", "6.", "7.", "8."],
        "comment": "1 + 4 = 5. Majd 5 - 2 = 3. Végül 3 + 3 = 6. lépcsőfok.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "A polcon a matekkönyv bal oldalán 2 könyv van, jobb oldalán pedig 4. Hány könyv van összesen a polcon?",
        "options": ["5", "6", "7", "8", "9"],
        "comment": "2 könyv balra + a matekkönyv + 4 könyv jobbra = 7 könyv.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Az asztalon van 5 alma. Ha elveszel belőle 3-at, hány almád lesz?",
        "options": ["0", "2", "3", "5", "8"],
        "comment": "Te vetted el, tehát neked pontosan annyi van, amennyit elvettél: 3 almád lesz.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "D",
        "question": "Kettő darab, kettőbe vágott alma hány darab almafelet jelent összesen?",
        "options": ["1", "2", "3", "4", "6"],
        "comment": "1 darab alma 2 felet jelent. 2 darab alma tehát 2 x 2 = 4 felet.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Melyik szám következik a sorban: 2, 4, 6, 8, ...?",
        "options": ["9", "10", "11", "12", "14"],
        "comment": "A páros számok növekednek kettesével, tehát a következő a 10.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Melyik szó nem illik a többi közé logikailag?",
        "options": ["Kutya", "Macska", "Asztal", "Tehén", "Ló"],
        "comment": "Az asztal egy bútor, a többi mind élőlény (állat).",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "A zsebemben lévő 3 érme összege pont 15 forint. Milyen érmék ezek, ha csak 5, 10 vagy 20 forintosok léteznek?",
        "options": [
            "1 db 5 Ft és 1 db 10 Ft",
            "3 db 5 Ft",
            "2 db 5 Ft és 1 db 10 Ft",
            "Nem lehet 3 érméből kirakni",
            "1 db 10 Ft és 1 db 20 Ft",
        ],
        "comment": "5 + 5 + 5 = 15, így 3 db 5 forintos érme.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy csiga egy 5 méter mély kútból mászik kifelé. Nappal felmászik 3 métert, éjjel visszacsúszik 2 métert. Hányadik napon ér ki a kútból?",
        "options": ["1.", "2.", "3.", "4.", "5."],
        "comment": "1. nap: 1m. 2. nap: 2m. 3. nap nappal felmászik 3 métert, így eléri az 5 métert és kiér.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "A",
        "question": "Egy béka előre ugrik 2-t, majd hátra 1-et. Hányat kell ugrania összesen, hogy 3 lépésnyire távolodjon el a kezdőponttól?",
        "options": ["3", "4", "5", "6", "7"],
        "comment": "Ugrások: +2, -1, +2. Ekkor 0-ról 3-ra jut, tehát összesen 3 ugrás kell.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Anna, Béla, Cili és Dóra körbeülnek egy asztalt. Anna szemben ül Bélával. Cili Anna jobb oldalán ül. Ki ül Anna bal oldalán?",
        "options": ["Béla", "Cili", "Dóra", "Egyikük sem", "Nem tudjuk"],
        "comment": "Mivel 4-en vannak, és 3 hely már elfoglalt, Anna bal oldalán csak Dóra ülhet.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Apának van két 10 forintosa és három 5 forintosa a zsebében. Mennyi pénze van összesen?",
        "options": ["25 Ft", "30 Ft", "35 Ft", "40 Ft", "45 Ft"],
        "comment": "2 x 10 = 20 forint. 3 x 5 = 15 forint. 20 + 15 = 35 forint.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Bújócskát játszik 10 gyerek. Egyikük a hunyó. Már megtalált 6 gyereket. Hányan vannak még elbújva?",
        "options": ["2", "3", "4", "5", "6"],
        "comment": "Összesen 10 gyerek, mínusz 1 hunyó = 9 bújik el. 9-ből megtalált 6-ot, tehát 3 maradt.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "3 szál egyforma hosszú gyufából milyen zárt síkidomot tudsz kirakni anélkül, hogy eltörnéd őket?",
        "options": ["Négyzetet", "Háromszöget", "Kört", "Téglalapot", "Hatszöget"],
        "comment": "3 oldalú zárt síkidom a háromszög.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "D",
        "question": "Hány pötty van azon a hagyományos dominón, amelyiknek mindkét felén a lehető legtöbb pötty van?",
        "options": ["6", "8", "10", "12", "14"],
        "comment": "A dupla hatos dominó mindkét oldalán 6 pötty van, 6 + 6 = 12.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy kocsikeréknek 4 küllője van. Hány egyforma részre osztják a kereket ezek a küllők?",
        "options": ["2", "3", "4", "5", "6"],
        "comment": "4 küllő pontosan 4 cikkelyre osztja a kört.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Misi minden nap megeszik pontosan 2 almát. Hány nap alatt fogy el neki 10 alma?",
        "options": ["3", "4", "5", "6", "10"],
        "comment": "10 alma, elosztva napi 2-vel, az 5 nap.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Pontban délben elindultam arra, amerről a nap sütött. Milyen égtáj felé sétáltam?",
        "options": ["Észak", "Dél", "Kelet", "Nyugat", "Felfelé"],
        "comment": "A nap délben mindig déli irányban látszik (az északi féltekén).",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Gabi bal keze felől fúj a szél. Merre dőlnek a fák a kertben emiatt?",
        "options": ["Balra", "Jobbra", "Előre", "Hátra", "Nem dőlnek semerre"],
        "comment": "A szél a maga irányába fújja a fákat, tehát ha balról fúj, jobbra dőlnek el.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "A",
        "question": "Van 3 macska. Mindegyik macska előtt van 2 macska. Hogy lehet ez?",
        "options": [
            "Körben ülnek",
            "Egy sorban állnak",
            "Ketten szemben, egy oldalt",
            "A tükörbe néznek",
            "Nem lehetséges",
        ],
        "comment": "Ha körben ülnek egymás farkát figyelve, akkor mindegyikük 2 macskát lát maga előtt a kör mentén.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Melyik az a szám a nullán kívül, amelyiket ha összeadjuk önmagával, és megszorozzuk önmagával, ugyanazt az eredményt kapjuk?",
        "options": ["1", "2", "3", "4", "5"],
        "comment": "2 + 2 = 4, és 2 x 2 = 4.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "D",
        "question": "Peti egy hideg, sötét szobában van. Van nála egy gyertya, egy olajlámpa és egy papírrakás, de csak egyetlen gyufája van. Mit gyújt meg legelőször?",
        "options": [
            "A gyertyát",
            "Az olajlámpát",
            "A papírt",
            "A gyufát",
            "Mindegyiket egyszerre",
        ],
        "comment": "Bármi mást csak akkor tud meggyújtani, ha először a gyufát gyújtja meg.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Hány ujj van összesen 10 emberi kézen összegyűjtve?",
        "options": ["10", "20", "50", "100", "Nem lehet tudni"],
        "comment": "1 kézen 5 ujj van. 10 x 5 = 50 ujj.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Egy papírra felírtam a 86-os számot. Hogyan csinálhatok belőle nagyobbat anélkül, hogy átírnám vagy hozzáírnék a számhoz?",
        "options": [
            "Radírozással",
            "Fejjel lefelé fordítom a papírt",
            "Tükörbe nézem",
            "Nem lehet",
            "Kiszínezem",
        ],
        "comment": "Ha fejjel lefelé fordítjuk a papírt, a 86-os számból 98 lesz, ami nagyobb.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "D",
        "question": "Egy kosárban 5 alma van. Hogyan tudod úgy szétosztani 5 gyerek között, hogy mindenki kapjon egy almát, de 1 alma mégis a kosárban maradjon?",
        "options": [
            "Kettévágva az almákat",
            "Az egyik gyerek nem kap",
            "Senki sem kap almát",
            "Az utolsó gyerek a kosárral együtt kapja az almát",
            "Lehetetlen",
        ],
        "comment": "Az ötödik gyereknek a kosárban benne hagyva adjuk oda az utolsó almát.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "E",
        "question": "Az év melyik hónapjában van 28 nap?",
        "options": [
            "Csak februárban",
            "Májusban",
            "Augusztusban",
            "Októberben",
            "Minden hónapban",
        ],
        "comment": "Minden hónapban van legalább 28 nap.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Ha egy orvos 3 tablettát ír fel, és azt mondja, hogy fél óránként vegyél be egyet, mennyi idő alatt fogy el az összes tabletta?",
        "options": ["Fél óra", "1 óra", "Másfél óra", "2 óra", "3 óra"],
        "comment": "Az elsőt beveszed most. Fél óra múlva a másodikat. Fél óra múlva a harmadikat. Összesen 1 óra.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Két apa és két fiú horgászik. Összesen 3 halat fognak, és mindegyikük pontosan egy halat visz haza. Hogyan lehetséges ez?",
        "options": [
            "Az egyik hal aranyhal volt",
            "Egymástól lopták a halat",
            "Valójában ez egy nagyapa, az ő fia, és annak a fia (az unoka)",
            "Volt egy harmadik fiú is",
            "Két halat megettek ott a helyszínen",
        ],
        "comment": "A fiú egyszerre apa (az unokának) és fiú (a nagyapának). Így hárman vannak összesen.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "D",
        "question": "Melyik az a betű, amelyik a VÍZ szóban benne van, de a JÉG szóban nincs?",
        "options": ["J", "É", "G", "V", "Egyik sem"],
        "comment": "A V betű szerepel a Víz-ben, de nem a Jég-ben.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "B",
        "question": "Tomi 1-től 10-ig összeadta a számokat. Zoli 1-től 10-ig összeszorozta a számokat. Vajon melyik fiú eredménye lett a nagyobb?",
        "options": ["Tomié", "Zolié", "Egyenlő", "Mindkettő 0", "Nem lehet kiszámolni"],
        "comment": "A szorzás sokkal gyorsabban növeli a számot (pl. már csak az 5*6*7 is jóval több az összegnél).",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "D",
        "question": "Gergőnek 3 nővére és 2 bátyja van. Hány gyerek van ebben a családban összesen?",
        "options": ["3", "4", "5", "6", "7"],
        "comment": "Gergő + 3 nővér + 2 báty = 6 gyerek.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "C",
        "question": "Egy dobókockának hány lapja van?",
        "options": ["4", "5", "6", "8", "12"],
        "comment": "A kockának 6 négyzet alakú oldala (lapja) van.",
    },
    {
        "class": "2",
        "difficulty": "easy",
        "correct": "A",
        "question": "A fán 6 madár ült. Egy vadász elsütött egy durranó puskát és egyet eltalált. Hány madár maradt a fán?",
        "options": ["0", "1", "4", "5", "6"],
        "comment": "A nagy zajtól az összes többi madár elrepült, egy sem maradt a fán.",
    },
]


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute(
        """
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
    """
    )

    count = 0
    for q in QUESTIONS:
        # Check if exists
        cursor.execute("SELECT id FROM questions WHERE question = ?", (q["question"],))
        if cursor.fetchone():
            continue

        # Get correct answer val to match options
        # In my manual list, "correct" is the letter (A, B, C...) which maps to options idx provided

        # Mapping logic
        # q["correct"] is 'A'...'E'.

        cursor.execute(
            """
            INSERT INTO questions (class, difficulty, question, option_a, option_b, option_c, option_d, option_e, correct_answer, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                q["class"],
                q["difficulty"],
                q["question"],
                q["options"][0],
                q["options"][1],
                q["options"][2],
                q["options"][3],
                q["options"][4],
                q["correct"],
                q.get("comment"),
            ),
        )
        count += 1

    conn.commit()
    conn.close()

    print(f"Manually inserted {count} logic questions.")

    # Export to db_data.js
    with open(DB_PATH, "rb") as f:
        db_bytes = f.read()
    b64_data = base64.b64encode(db_bytes).decode("utf-8")
    with open(JS_PATH, "w") as f:
        f.write(f"const DB_BASE64 = '{b64_data}';\n")
    print(f"Exported database to {JS_PATH}")


if __name__ == "__main__":
    main()
