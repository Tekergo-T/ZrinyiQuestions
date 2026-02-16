#!/usr/bin/env python3
"""
Master script to rebuild the Zrínyi Questions database from scratch.
1. Runs manual_insert_questions.py (inserts ~425 base text questions)
2. Runs add_image_questions.py (inserts ~50 programmatic image questions)
3. Ensures db_data.js is exported and ready for app.js

Usage:
  python3 rebuild_db.py
"""

import os
import subprocess
import sys
import sqlite3

def run_script(script_name):
    print(f"\n=== Running {script_name} ===")
    try:
        # Run the script and stream output
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            text=True,
            capture_output=False
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
        sys.exit(1)
    print(f"✅ {script_name} completed.")

def print_stats():
    print("\n=== Final Database Stats ===")
    if not os.path.exists("zrinyi_questions.db"):
        print("❌ Database file not found!")
        return

    conn = sqlite3.connect("zrinyi_questions.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM questions")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM questions WHERE image IS NOT NULL")
    images = c.fetchone()[0]
    c.execute("SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty ORDER BY difficulty")
    stats = c.fetchall()
    
    print(f"  Total Questions: {total}")
    print(f"  Image Questions: {images}")
    print("  Difficulty Breakdown:")
    for d, count in stats:
        print(f"    - {d}: {count}")
    conn.close()

def main():
    # Ensure we are in the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Step 0: Clean old DB
    if os.path.exists("zrinyi_questions.db"):
        os.remove("zrinyi_questions.db")
        print("🗑️  Deleted old database.")

    # Step 1: Base questions
    run_script("manual_insert_questions.py")

    # Step 2: Image questions
    run_script("add_image_questions.py")

    # Step 3: Verify
    print_stats()
    print("\n🎉 Rebuild complete! Open index.html to play.")

if __name__ == "__main__":
    main()
