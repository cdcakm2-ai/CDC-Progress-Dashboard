import csv

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = list(csv.reader(f))

gns = [
    '109/බී ඉහළගොඩ දකුණ',
    '152 ඒ අමුකොටුව',
    '133/ ඒ තල්පෙ උතුර',
    '133 /ඊ තල්පෙගොඩ',
    '130 /ඩී ජම්බුකැටිය'
]

for gn in gns:
    print(f"\n==========================================")
    print(f"GN: {gn}")
    for r_idx, row in enumerate(reader[1:], 1):
        if row[2].strip() == gn:
            print(f"Row {r_idx} | TS: {row[0]} | Claimed: {row[3]}")
            for b in range(8):
                d = row[4 + b*4].strip()
                desc = row[5 + b*4].strip()
                if d or desc:
                    print(f"  B{b+1}: Date: {d} | Desc: {desc}")
