import csv

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    r1 = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    r2 = list(csv.reader(f))

for gn in ['109/ ජී ඇටඹගස්මුල්ල', '155/ ඊ හියාරේ ඉහළ', '152 /බී තලහිටියාව', '133/සී නාගහවත්ත', '109/බී ඉහළගොඩ දකුණ', '133 /ඊ තල්පෙගොඩ']:
    print(f"\n==========================================")
    print(f"GN: {gn}")
    count = 0
    for s_name, rows in [("Sheet1", r1), ("Sheet2", r2)]:
        for r_idx, row in enumerate(rows[1:], 1):
            if gn in row[2]:
                print(f"[{s_name} Row {r_idx}] TS: {row[0]}")
                for b in range(8):
                    d = row[4 + b*4].strip()
                    desc = row[5 + b*4].strip()
                    p = row[6 + b*4].strip()
                    if d or desc:
                        count += 1
                        print(f"  {count}. B{b+1} | Date: {d} | HasPhotos: {bool(p)} | Desc: {desc}")
