import csv
import json
import re
from collections import defaultdict

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = list(csv.reader(f))

# Let's inspect each of the 14 multi-row GNs
multi_gns = [
    '134/ බී කදුරුදූව',
    '133/සී නාගහවත්ත',
    '109/ ජී ඇටඹගස්මුල්ල',
    '155/ ඊ හියාරේ ඉහළ',
    '109/බී ඉහළගොඩ දකුණ',
    '152 ඒ අමුකොටුව',
    '152 /බී තලහිටියාව',
    '133/ ඒ තල්පෙ උතුර',
    '133 /ඊ තල්පෙගොඩ',
    '130 /ඩී ජම්බුකැටිය',
    '112/සී කිරින්ඳගොඩ',
    '113/බී නුගදූව',
    '110 අංකොක්කාවල',
    '113 බටදූව'
]

gn_rows = defaultdict(list)
for r_idx, row in enumerate(reader[1:], 1):
    gn_rows[row[2].strip()].append(r_idx)

for gn in multi_gns:
    rows = gn_rows[gn]
    print(f"\n=======================================================")
    print(f"GN: '{gn}' (Rows {rows})")
    for r in rows:
        row = reader[r]
        print(f"--- Row {r} (TS: {row[0]}, Officer: {row[1]}, Claimed: {row[3]}) ---")
        for b in range(8):
            d = row[4 + b*4].strip()
            desc = row[5 + b*4].strip()
            p = bool(row[6 + b*4].strip())
            if d or desc:
                print(f"  B{b+1} | Date: {d} | Desc: {desc[:70]}")
