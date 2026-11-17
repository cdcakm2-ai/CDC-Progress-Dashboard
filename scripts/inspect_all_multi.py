import csv
from collections import defaultdict

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = list(csv.reader(f))

# Find all multi-row GNs
gn_rows = defaultdict(list)
for r_idx, row in enumerate(reader[1:], 1):
    gn_rows[row[2].strip()].append(r_idx)

multi_gns = {k: v for k, v in gn_rows.items() if len(v) > 1}

for gn, r_indices in multi_gns.items():
    print(f"\n==========================================")
    print(f"GN: '{gn}' -> Rows: {r_indices}")
    for r_idx in r_indices:
        row = reader[r_idx]
        print(f"  [Row {r_idx}] TS: {row[0]} | Officer: {row[1]} | Claimed: {row[3]}")
        for b in range(8):
            d = row[4 + b*4].strip()
            desc = row[5 + b*4].strip()
            p = row[6 + b*4].strip()
            if d or desc:
                print(f"     B{b+1}: Date: {d} | Desc: {desc}")
