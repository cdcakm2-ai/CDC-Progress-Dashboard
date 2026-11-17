import json
import re

with open('raw_drive_data/merges_without_shared_photos.txt', 'r', encoding='utf-8') as f:
    text = f.read()

entries = text.strip().split('\n\n')

# Check all 77 merges
suspicious = []
for entry in entries:
    lines = entry.strip().split('\n')
    if len(lines) < 4: continue
    hdr = lines[0]
    reason = lines[1]
    k_line = lines[2]
    d_line = lines[3]
    k_desc = k_line.split('): ', 1)[1] if '): ' in k_line else k_line
    d_desc = d_line.split('): ', 1)[1] if '): ' in d_line else d_line
    
    # Are there any other conflicting keywords or names?
    # e.g. names of persons, completely different venues, different target groups
    # Let's check:
    k_words = set(re.findall(r'[\u0D80-\u0DFFa-zA-Z]{4,}', k_desc))
    d_words = set(re.findall(r'[\u0D80-\u0DFFa-zA-Z]{4,}', d_desc))
    common = k_words.intersection(d_words)
    
    # If very few common words and not singlish
    is_singlish = bool(re.search(r'[a-zA-Z]{4,}', k_desc) or re.search(r'[a-zA-Z]{4,}', d_desc))
    if len(common) <= 1 and not is_singlish:
        suspicious.append((hdr, reason, k_desc, d_desc, common))

print(f"Suspicious entries with <= 1 common word: {len(suspicious)}")
for s in suspicious:
    print(s[0])
    print(f"  Reason: {s[1]}")
    print(f"  KEPT: {s[2]}")
    print(f"  DUP : {s[3]}")
    print(f"  Common words: {s[4]}")
    print()
