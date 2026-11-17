import csv
import json
import re

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s1 = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2 = list(csv.reader(f))

def clean_gn_name(g):
    s = re.sub(r'\s+', ' ', g).strip()
    s = s.replace('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල')
    s = s.replace('109 ඉහලගොඩ බටහිර', '109 ඉහළගොඩ බටහිර')
    s = s.replace('112/සී කිරින්ඳගොඩ', '112/සී කිරින්දගොඩ')
    return s

def clean_text(t):
    s = re.sub(r'[\r\n\t]+', ' ', t)
    s = re.sub(r'\s+', ' ', s).strip()
    # minor typo corrections
    corrections = [
        ('සන්වර්දනය', 'සංවර්ධනය'),
        ('මර්ගය', 'මාර්ගය'),
        ('මර්ග', 'මාර්ග'),
        ('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල'),
        ('වැඩසටහණ', 'වැඩසටහන'),
        ('පැවැත්වීඹ', 'පැවැත්වීම'),
        ('දැනුවත්කීරීම', 'දැනුවත් කිරීම'),
        ('කිරිම', 'කිරීම'),
        ('ශ්‍රමදානය්', 'ශ්‍රමදානය'),
        ('දර්මපාල', 'ධර්මපාල'),
        ('අතුරැමාර්ගයෙ', 'අතුරුමාර්ගයේ'),
        ('ඉදිකිරිම', 'ඉදිකිරීම'),
        ('ක්‍රිඩාංගනය', 'ක්‍රීඩාංගනය')
    ]
    for w, r in corrections:
        s = s.replace(w, r)
    return s

def parse_date(d_str):
    if not d_str: return "2026-08-01"
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
            elif p2 < 100:
                year = 2000 + p2
                if p1 > 12 and p0 <= 12: p0, p1 = p1, p0
                return f"{year:04d}-{p1:02d}-{p0:02d}"
        except:
            pass
    return d_str.strip()

# Collect all 290 activities from Sheet 1 and Sheet 2
all_290 = []
act_counter = 1

for s_name, rows in [("Sheet 1", s1), ("Sheet 2", s2)]:
    for r_idx, r in enumerate(rows[1:], 1):
        if len(r) < 4: continue
        gn = clean_gn_name(r[2])
        for b in range(8):
            d_col = 4 + b * 4
            desc_col = 5 + b * 4
            p_col = 6 + b * 4
            if d_col >= len(r) or desc_col >= len(r): break
            d_raw = r[d_col].strip()
            desc = clean_text(r[desc_col])
            p_raw = r[p_col].strip() if p_col < len(r) else ""
            if not d_raw and not desc: continue

            # Photos
            f1 = re.findall(r'id=([a-zA-Z0-9_-]{15,})', p_raw)
            f2 = re.findall(r'/d/([a-zA-Z0-9_-]{15,})', p_raw)
            photo_ids = []
            for fid in f1 + f2:
                if fid not in photo_ids: photo_ids.append(fid)

            photo_objs = [{
                'id': fid,
                'thumbnail': f"https://lh3.googleusercontent.com/d/{fid}=s400",
                'full': f"https://lh3.googleusercontent.com/d/{fid}=s1200",
                'driveUrl': f"https://drive.google.com/file/d/{fid}/view?usp=sharing"
            } for fid in photo_ids]

            date_parsed = parse_date(d_raw)

            all_290.append({
                'id': f"ACT-{act_counter:03d}",
                'sheet': s_name,
                'row': r_idx,
                'block': b + 1,
                'gnNameSi': gn,
                'sabhaNameSi': f"{gn} ප්‍රජා සංවර්ධන සභාව",
                'dateRaw': d_raw,
                'date': date_parsed,
                'titleSi': desc[:60] if len(desc) > 60 else (desc or "ප්‍රජා සංවර්ධන වැඩසටහන"),
                'description': desc or "ප්‍රජා සංවර්ධන වැඩසටහන",
                'images': [p['full'] for p in photo_objs],
                'photoObjects': photo_objs,
                'photoCount': len(photo_objs),
                'statusLabelSi': "සම්පූර්ණයි",
                'source': f"{s_name} R{r_idx} B{b+1}"
            })
            act_counter += 1

print(f"Total extracted activities: {len(all_290)}")
print(f"Sheet 1 activities: {sum(1 for a in all_290 if a['sheet'] == 'Sheet 1')}")
print(f"Sheet 2 activities: {sum(1 for a in all_290 if a['sheet'] == 'Sheet 2')}")
total_photos = sum(a['photoCount'] for a in all_290)
print(f"Total photos linked: {total_photos}")
