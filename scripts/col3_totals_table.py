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

# Sum Col 3
s1_col3 = defaultdict(int)
for r in s1[1:]:
    gn = clean_gn(r[2])
    c3 = r[3].strip()
    try:
        s1_col3[gn] += int(c3)
    except:
        if 'නව' in c3: s1_col3[gn] += 1

s2_col3 = defaultdict(int)
for r in s2[1:]:
    gn = clean_gn(r[2])
    c3 = r[3].strip()
    try:
        s2_col3[gn] += int(c3)
    except:
        if '3' in c3 or '03' in c3: s2_col3[gn] += 3

all_gns = sorted(list(set(list(s1_col3.keys()) + list(s2_col3.keys()))))
print(f"{'GN Division':<35} | {'S1 Col3':<8} | {'S2 Col3':<8} | {'Total Col3':<10}")
print("-" * 68)

tot1 = 0
tot2 = 0
tot_all = 0
for gn in all_gns:
    c1 = s1_col3[gn]
    c2 = s2_col3[gn]
    t = c1 + c2
    tot1 += c1
    tot2 += c2
    tot_all += t
    print(f"{gn:<35} | {c1:<8} | {c2:<8} | {t:<10}")

print("-" * 68)
print(f"{'TOTAL':<35} | {tot1:<8} | {tot2:<8} | {tot_all:<10}")
