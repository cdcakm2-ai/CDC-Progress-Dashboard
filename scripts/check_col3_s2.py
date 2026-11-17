import csv

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2 = list(csv.reader(f))

diffs = []
for r_idx, r in enumerate(s2[1:], 1):
    gn = r[2].strip()
    c3 = r[3].strip()
    blocks = 0
    for b in range(8):
        d_col = 4 + b * 4
        desc_col = 5 + b * 4
        if d_col < len(r) and desc_col < len(r):
            d = r[d_col].strip()
            desc = r[desc_col].strip()
            if d or desc:
                blocks += 1
    try:
        val = int(c3)
        if val != blocks:
            diffs.append((r_idx, gn, val, blocks))
    except:
        diffs.append((r_idx, gn, c3, blocks))

print(f"Sheet 2 rows where Col 3 != blocks count: {len(diffs)}")
for d in diffs:
    print(f"Row {d[0]}: GN={d[1]}, Col3 stated={d[2]}, Actual blocks filled={d[3]}")
