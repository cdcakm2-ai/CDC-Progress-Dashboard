import csv
import json
import re
from collections import defaultdict

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s1_rows = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2_rows = list(csv.reader(f))

def clean_gn_name(g):
    s = re.sub(r'\s+', ' ', g).strip()
    s = s.replace('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල')
    s = s.replace('ඉහලගොඩ බටහිර', 'ඉහළගොඩ බටහිර')
    return s

all_acts = []

def parse_d(d_str):
    if not d_str: return ""
    d_clean = d_str.strip().replace('.', '/').replace('-', '/').replace(' ', '')
    p = d_clean.split('/')
    if len(p) == 3:
        try:
            p0, p1, p2 = int(p[0]), int(p[1]), int(p[2])
            if p2 >= 2000:
                if p1 > 12 and p0 <= 12: p0, p1 = p1, p0
                return f"{p2:04d}-{p1:02d}-{p0:02d}"
            elif p0 >= 2000:
                return f"{p0:04d}-{p1:02d}-{p2:02d}"
        except:
            pass
    return d_str.strip()

for s_idx, (rows, s_name) in enumerate([(s1_rows, "Sheet 1"), (s2_rows, "Sheet 2")]):
    for r_idx, r in enumerate(rows[1:], 1):
        if len(r) < 4: continue
        gn = clean_gn_name(r[2])
        for b in range(8):
            col_d = 4 + b * 4
            col_desc = 5 + b * 4
            col_p = 6 + b * 4
            if col_d >= len(r) or col_desc >= len(r): break
            d = r[col_d].strip()
            desc = r[col_desc].strip()
            p = r[col_p].strip() if col_p < len(r) else ""
            if not d and not desc: continue
            
            photos = []
            f1 = re.findall(r'id=([a-zA-Z0-9_-]{15,})', p)
            f2 = re.findall(r'/d/([a-zA-Z0-9_-]{15,})', p)
            for fid in f1 + f2:
                if fid not in photos: photos.append(fid)
                
            all_acts.append({
                'sheet': s_name,
                'row': r_idx,
                'block': b + 1,
                'gn': gn,
                'date_raw': d,
                'date': parse_d(d),
                'desc': desc.replace('\r\n', '\n').strip(),
                'photos': photos
            })

print(f"Total raw activity items extracted from both sheets: {len(all_acts)}")

# Group by GN
by_gn = defaultdict(list)
for a in all_acts:
    by_gn[a['gn']].append(a)

print(f"Total GN divisions in sheets: {len(by_gn)}")
for gn, items in sorted(by_gn.items()):
    print(f"  {gn}: {len(items)} items")
