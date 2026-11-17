import re
from difflib import SequenceMatcher

def norm(s):
    return re.sub(r'[\s\.\,\-\_\/\(\)\[\]\:\;]+', '', s.lower())

with open('raw_drive_data/merges_without_shared_photos.txt', 'r', encoding='utf-8') as f:
    text = f.read()

entries = text.strip().split('\n\n')

print(f"Total entries: {len(entries)}")
low_sim_entries = []

for entry in entries:
    lines = entry.strip().split('\n')
    if len(lines) < 4: continue
    hdr = lines[0]
    reason = lines[1]
    kept = lines[2]
    dup = lines[3]
    
    k_text = kept.split('): ', 1)[1] if '): ' in kept else kept
    d_text = dup.split('): ', 1)[1] if '): ' in dup else dup
    
    sim = SequenceMatcher(None, norm(k_text), norm(d_text)).ratio()
    if sim < 0.50:
        low_sim_entries.append((hdr, reason, k_text, d_text, sim))

print(f"Entries with sim < 0.50: {len(low_sim_entries)}\n")
for item in low_sim_entries:
    print(item[0])
    print(f"  SIM: {item[4]:.2f}")
    print(f"  REASON: {item[1]}")
    print(f"  KEPT: {item[2]}")
    print(f"  DUP : {item[3]}")
    print()
