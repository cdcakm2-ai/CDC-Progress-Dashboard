import json
from difflib import SequenceMatcher
import re

with open('raw_drive_data/merges_without_shared_photos.txt', 'r', encoding='utf-8') as f:
    text = f.read()

entries = text.strip().split('\n\n')
print(f"Total entries: {len(entries)}")

# Let's write an analyzer that checks each entry
def norm(s):
    return re.sub(r'[\s\.\,\-\_\/\(\)\[\]\:\;]+', '', s.lower())

flagged_different = []
confident_dups = []

for entry in entries:
    lines = entry.strip().split('\n')
    if len(lines) < 4: continue
    hdr = lines[0] # #01 [109 ඉහළගොඩ බටහිර] Date: ...
    reason = lines[1]
    kept = lines[2]
    dup = lines[3]
    
    k_text = kept.split('): ', 1)[1] if '): ' in kept else kept
    d_text = dup.split('): ', 1)[1] if '): ' in dup else dup
    
    sim = SequenceMatcher(None, norm(k_text), norm(d_text)).ratio()
    
    # Check for obvious different topics
    different_indicators = [
        ("කසල", "ගෙවතු"), # waste management vs home gardening
        ("ක්‍රිකට්", "ශ්‍රමදාන"), # cricket vs shramadana
        ("තාක්ෂණ", "පුන්‍යග්‍රාම"), # tech training vs punyagrama
        ("ප්‍රේමලාල්", "තුශාර"), # two different individuals
        ("ආහාර සුරක්ෂිතතාවය", "පට්ටන්"),
        ("ප්‍රජාවගේ එකමුතුකම", "ශ්‍රී මාවත"),
        ("දන්සල", "ප්‍රජා ශක්‍ර්ති"),
        ("මහජන ආරක්ෂාව", "සිවිල් ආරක්ෂාව"),
        ("පොදු ළිද", "පොදු ළිද"),
    ]
    
    print(f"{hdr}")
    print(f"  SIM: {sim:.2f}")
    print(f"  KEPT: {k_text}")
    print(f"  DUP : {d_text}")
    print("-" * 60)
