import csv
from collections import defaultdict

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s1 = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2 = list(csv.reader(f))

def clean_gn(g):
    g = g.strip()
    g = g.replace('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල')
    g = g.replace('109 ඉහලගොඩ බටහිර', '109 ඉහළගොඩ බටහිර')
    g = g.replace('112/සී කිරින්ඳගොඩ', '112/සී කිරින්දගොඩ')
    return g

# Count actual activity blocks in Sheet 1
s1_counts = defaultdict(int)
for r in s1[1:]:
    gn = clean_gn(r[2])
    for b in range(8):
        d_col = 4 + b * 4
        desc_col = 5 + b * 4
        if d_col < len(r) and desc_col < len(r):
            d = r[d_col].strip()
            desc = r[desc_col].strip()
            if d or desc:
                s1_counts[gn] += 1

# Count actual activity blocks in Sheet 2
s2_counts = defaultdict(int)
for r in s2[1:]:
    gn = clean_gn(r[2])
    for b in range(8):
        d_col = 4 + b * 4
        desc_col = 5 + b * 4
        if d_col < len(r) and desc_col < len(r):
            d = r[d_col].strip()
            desc = r[desc_col].strip()
            if d or desc:
                s2_counts[gn] += 1

all_gns = sorted(list(set(list(s1_counts.keys()) + list(s2_counts.keys()))))
print(f"Total reporting GN divisions across both sheets: {len(all_gns)}")
print(f"{'GN Division':<35} | {'Sheet 1':<8} | {'Sheet 2':<8} | {'Total':<8}")
print("-" * 65)

total_s1 = 0
total_s2 = 0
total_both = 0
for gn in all_gns:
    c1 = s1_counts[gn]
    c2 = s2_counts[gn]
    tot = c1 + c2
    total_s1 += c1
    total_s2 += c2
    total_both += tot
    print(f"{gn:<35} | {c1:<8} | {c2:<8} | {tot:<8}")

print("-" * 65)
print(f"{'TOTAL':<35} | {total_s1:<8} | {total_s2:<8} | {total_both:<8}")
