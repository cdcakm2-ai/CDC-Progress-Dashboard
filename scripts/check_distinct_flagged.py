import json
import re
from difflib import SequenceMatcher

with open('raw_drive_data/merges_without_shared_photos.txt', 'r', encoding='utf-8') as f:
    text = f.read()

entries = text.strip().split('\n\n')

flagged = []

for entry in entries:
    lines = entry.strip().split('\n')
    if len(lines) < 4: continue
    hdr = lines[0]
    reason = lines[1]
    kept = lines[2]
    dup = lines[3]
    
    k_text = kept.split('): ', 1)[1] if '): ' in kept else kept
    d_text = dup.split('): ', 1)[1] if '): ' in dup else dup
    
    # Check for specific distinct entities
    # 1. Names of beneficiaries (e.g. Vasantha Premalal vs Janaka Thushara)
    # 2. Distinct projects (e.g. Waste management vs Organic gardening)
    # 3. Distinct activities (e.g. Cricket vs Shramadana)
    
    is_distinct = False
    distinct_reason = ""
    
    if "ප්‍රේමලාල්" in k_text and "තුශාර" in d_text:
        is_distinct = True
        distinct_reason = "Different beneficiary families: Vasantha Premalal vs Janaka Thushara"
    elif "කසල" in k_text and "ගෙවතු" in d_text:
        is_distinct = True
        distinct_reason = "Different projects: Waste management vs Organic gardening"
    elif "සංගීත" in k_text and "හැඩිදෙමළකන්ද" in d_text:
        is_distinct = True
        distinct_reason = "Different events: DJ Musical evening vs Hadidemalakanda Shramadana"
        
    if is_distinct:
        flagged.append((hdr, reason, k_text, d_text, distinct_reason))

print(f"Flagged {len(flagged)} entries that are truly distinct activities:")
for f in flagged:
    print(f[0])
    print("  Reason merged:", f[1])
    print("  KEPT:", f[2])
    print("  DUP :", f[3])
    print("  DISCOVERY:", f[4])
    print()
