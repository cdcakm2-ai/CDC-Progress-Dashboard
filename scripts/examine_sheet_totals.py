import csv
import re
from collections import defaultdict

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s1 = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2 = list(csv.reader(f))

print(f"Sheet 1 header rows: 1, data rows: {len(s1)-1}")
print(f"Sheet 2 header rows: 1, data rows: {len(s2)-1}")

# For Sheet 1:
s1_col3_total = 0
s1_blocks_total = 0
s1_gn_col3 = defaultdict(int)
s1_gn_blocks = defaultdict(int)

for r_idx, r in enumerate(s1[1:], 1):
    gn = r[2].strip()
    c3 = r[3].strip()
    try:
        val = int(c3)
        s1_col3_total += val
        s1_gn_col3[gn] += val
    except:
        pass
    
    blocks_in_row = 0
    for b in range(8):
        d_col = 4 + b * 4
        desc_col = 5 + b * 4
        if d_col < len(r) and desc_col < len(r):
            d = r[d_col].strip()
            desc = r[desc_col].strip()
            if d or desc:
                blocks_in_row += 1
    s1_blocks_total += blocks_in_row
    s1_gn_blocks[gn] += blocks_in_row

# For Sheet 2:
s2_col3_total = 0
s2_blocks_total = 0
s2_gn_col3 = defaultdict(int)
s2_gn_blocks = defaultdict(int)

for r_idx, r in enumerate(s2[1:], 1):
    gn = r[2].strip()
    c3 = r[3].strip()
    try:
        val = int(c3)
        s2_col3_total += val
        s2_gn_col3[gn] += val
    except:
        if '3' in c3 or '03' in c3:
            s2_col3_total += 3
            s2_gn_col3[gn] += 3
    
    blocks_in_row = 0
    for b in range(8):
        d_col = 4 + b * 4
        desc_col = 5 + b * 4
        if d_col < len(r) and desc_col < len(r):
            d = r[d_col].strip()
            desc = r[desc_col].strip()
            if d or desc:
                blocks_in_row += 1
    s2_blocks_total += blocks_in_row
    s2_gn_blocks[gn] += blocks_in_row

print("\n=== SHEET 1 ===")
print(f"Col 3 Sum: {s1_col3_total}")
print(f"Filled Activity Blocks: {s1_blocks_total}")

print("\n=== SHEET 2 ===")
print(f"Col 3 Sum: {s2_col3_total}")
print(f"Filled Activity Blocks: {s2_blocks_total}")

print("\n=== COMBINED ===")
print(f"Total Col 3 stated: {s1_col3_total + s2_col3_total}")
print(f"Total Filled Activity Blocks: {s1_blocks_total + s2_blocks_total}")

print("\n=== SHEET 1 CALC DATA COMPARISON ===")
with open('raw_drive_data/sheet1_calc_data.csv', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())
