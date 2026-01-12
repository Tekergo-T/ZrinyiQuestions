import re
import json
import os

def parse_file(filename):
    questions = []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find questions starting with "1. ", "2. " etc.
    # It captures the number and the text until the next number or EOF
    # BUT we need to be careful about options.
    
    # Split by lines
    lines = content.split('\n')
    
    current_q = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for question start
        match = re.match(r'^(\d+)\.\s+(.*)', line)
        if match:
            # Save previous question
            if current_q:
                questions.append(current_q)
            
            current_q = {
                'number': int(match.group(1)),
                'question': match.group(2),
                'options_raw': [],
                'class': 2 # Assuming 2nd grade for these files
            }
        elif current_q:
            # Check if line looks like options
            # (A) ... (B) ...
            if '(A)' in line or '(B)' in line:
                current_q['options_raw'].append(line)
            else:
                # Append to question text if it's not an option and we haven't seen options yet
                if not current_q['options_raw']:
                    current_q['question'] += " " + line
                else:
                    # Maybe it's a multiline option?
                    current_q['options_raw'].append(line)
                    
    if current_q:
        questions.append(current_q)
        
    # Post-process options
    parsed_questions = []
    for q in questions:
        raw_opts = " ".join(q['options_raw'])
        # Try to split by (A), (B), (C), (D), (E)
        # Regex: \([A-E]\)
        parts = re.split(r'\(([A-E])\)', raw_opts)
        # parts[0] is empty or text before (A)
        # parts[1] is 'A', parts[2] is text for A, parts[3] is 'B', etc.
        
        options = {}
        if len(parts) >= 11: # We expect empty, A, txt, B, txt, C, txt, D, txt, E, txt
            for i in range(1, len(parts), 2):
                letter = parts[i]
                text = parts[i+1].strip()
                options[letter] = text
        
        q['parsed_options'] = options
        del q['options_raw']
        parsed_questions.append(q)
        
    return parsed_questions

def main():
    files = [
        'sample1_2osztaly.txt',
        'sample2_2osztaly.txt',
        # 'extracted_content.txt' # Skipping due to OCR mess for now, or will add later
    ]
    
    all_questions = []
    for f in files:
        path = os.path.join(os.path.dirname(__file__), f)
        if os.path.exists(path):
            print(f"Parsing {f}...")
            qs = parse_file(path)
            all_questions.extend(qs)
            
    # Deduplicate based on question text (first 50 chars)
    unique_questions = {}
    for q in all_questions:
        key = q['question'][:50]
        if key not in unique_questions:
            unique_questions[key] = q
            
    print(f"Found {len(unique_questions)} unique questions.")
    
    with open('extracted_questions.json', 'w', encoding='utf-8') as f:
        json.dump(list(unique_questions.values()), f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
