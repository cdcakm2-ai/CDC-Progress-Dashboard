import csv
import json
import re
from collections import defaultdict

def extract_all_activities(sheet_path, sheet_label):
    activities = []
    with open(sheet_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = list(csv.reader(f))
        for r_idx, row in enumerate(reader[1:], 1):
            if len(row) < 4:
                continue
            ts = row[0].strip()
            officer = row[1].strip()
            gn_raw = row[2].strip()
            claimed = row[3].strip()
            
            # Inspect blocks
            # Up to 8 blocks: block i: start_col = 4 + i*4
            for b in range(8):
                d_idx = 4 + b * 4
                desc_idx = 5 + b * 4
                p_idx = 6 + b * 4
                
                if d_idx >= len(row) or desc_idx >= len(row):
                    break
                
                raw_d = row[d_idx].strip()
                raw_desc = row[desc_idx].strip()
                raw_p = row[p_idx].strip() if p_idx < len(row) else ""
                
                if not raw_d and not raw_desc:
                    continue
                
                activities.append({
                    'sheet': sheet_label,
                    'row': r_idx,
                    'block': b + 1,
                    'timestamp': ts,
                    'officer': officer,
                    'gn_raw': gn_raw,
                    'date': raw_d,
                    'desc': raw_desc,
                    'photos': raw_p
                })
    return activities

s1_acts = extract_all_activities('raw_drive_data/sheet1_form_responses_1.csv', 'Sheet1')
s2_acts = extract_all_activities('raw_drive_data/sheet2_form_responses_1.csv', 'Sheet2')

print(f"Total extracted activities from Sheet 1: {len(s1_acts)}")
print(f"Total extracted activities from Sheet 2: {len(s2_acts)}")
print(f"Total raw activities: {len(s1_acts) + len(s2_acts)}")

# Let's inspect duplicates:
# 1. Exact same description & same GN
desc_gn_map = defaultdict(list)
for a in s1_acts + s2_acts:
    # clean description for comparison
    clean_d = re.sub(r'\s+', ' ', a['desc']).strip().lower()
    clean_gn = re.sub(r'\s+', ' ', a['gn_raw']).strip()
    key = (clean_gn, clean_d)
    desc_gn_map[key].append(a)

duplicates = {k: v for k, v in desc_gn_map.items() if len(v) > 1}
print(f"\nUnique (GN, Description) pairs: {len(desc_gn_map)}")
print(f"Duplicate groups found: {len(duplicates)}")
for (gn, desc), occurrences in duplicates.items():
    print(f"\n--- DUPLICATE GROUP ---")
    print(f"GN: '{gn}'")
    print(f"Desc: '{desc[:80]}...'")
    for occ in occurrences:
        print(f"   [{occ['sheet']} Row {occ['row']} Block {occ['block']}] Date: {occ['date']} | TS: {occ['timestamp']}")

# 2. Check if between Sheet 1 and Sheet 2 there are identical activities
cross_sheet_dups = []
for (gn, desc), occurrences in duplicates.items():
    sheets = set(o['sheet'] for o in occurrences)
    if len(sheets) > 1:
        cross_sheet_dups.append((gn, desc, occurrences))

print(f"\nCross-sheet duplicate groups (in BOTH Sheet 1 and Sheet 2): {len(cross_sheet_dups)}")
for gn, desc, occs in cross_sheet_dups:
    print(f"  Cross GN: {gn} | Desc: {desc[:60]}")
