import csv
import re

with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'const ALL_63_GN_DIVISIONS\s*=\s*(\[[\s\S]*?\n\]);', text)
names_63 = re.findall(r'"nameSi":\s*"([^"]+)"', match.group(1))

raw_divisions = set()
for path in ['raw_drive_data/sheet1_form_responses_1.csv', 'raw_drive_data/sheet2_form_responses_1.csv']:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) > 2 and row[2].strip():
                raw_divisions.add(row[2].strip())

print(f"Total raw divisions in submissions: {len(raw_divisions)}")

def normalize_gn_name(raw):
    s = raw.strip()
    # Explicit mapping table for all variations in Google Forms:
    custom_map = {
        '109 ඉහලගොඩ බටහිර': 'ඉහළගොඩ බටහිර',
        '112/සී කිරින්ඳගොඩ': 'කිරින්දගොඩ',
        '113 /සී ආනන්ගොඩ': 'අනංගොඩ',
        '118 /ඒ තල්ගස්යාය': 'තැල්ගස්යාය',
        '130  ඒ/ ඇත්තිලිගොඩ උතුර': 'අත්තිලිගොඩ උතුර',
        '133 /ඊ තල්පෙගොඩ': 'තල්පගොඩ',
        '133 මැටරඹ': 'මීටරඹ',
        '133/ ඒ තල්පෙ උතුර': 'තල්පේ උතුර',
        '134  කළහෙ': 'කලේගාන',
        '134/ ඒ පනාගමුව': 'පනගමුව',
        '135 පැදින්නෝරුව': 'පෙදින්නොරුව',
        '152 /බී තලහිටියාව': 'තලාහිටියාව',
        '155/ ඊ හියාරේ ඉහළ': 'ඉහළ හියාචාර',
        '155/ බී හල්ගස්මුඅල්ල': 'හල්ගස්මුල්ල',
        '155/ඒච් කඳහේන': 'කන්දහේන',
        '155/සී කැටැන්දොළ': 'කැටන්දෝළ',
        'හියාරේ උතුර': 'හියාචාර උතුර',
        'හියාරේ දකුණ': 'හියාචාර දකුණ',
        'හියාරේ නැගෙනහිර': 'හියාචාර නැගෙනහිර',
        'ඉහල හියාරේ': 'ඉහළ හියාචාර',
        'ඉහළ හියාරේ': 'ඉහළ හියාචාර',
        'ජම්බුකැටිය': 'ජඹුකැටිය',
        'කැරන්විල ජනපදය': 'කැරැන්විල ජනපදය',
        'මැලැගොඩ': 'මැලෑගොඩ',
    }
    if s in custom_map:
        return custom_map[s]
    
    # Try exact match
    for off in names_63:
        if off == s or (off in s and len(off) > 3):
            return off
            
    # Substring in custom_map
    for k, v in custom_map.items():
        if k in s or s in k:
            return v
            
    return s

mapped = {}
unmapped = []
for raw in sorted(raw_divisions):
    norm = normalize_gn_name(raw)
    if norm in names_63:
        mapped[raw] = norm
    else:
        unmapped.append((raw, norm))

print(f"Successfully mapped: {len(mapped)} / {len(raw_divisions)}")
if unmapped:
    print(f"Still unmapped: {unmapped}")
else:
    print("ALL 54 RAW GN DIVISION STRINGS MAP 100% PERFECTLY TO OFFICIAL DIVISIONS!")

covered_divisions = set(mapped.values())
missing_divisions = [d for d in names_63 if d not in covered_divisions]
print(f"\nOfficial Divisions with reports: {len(covered_divisions)} / 63 ({len(covered_divisions)/63*100:.1f}%)")
print(f"Official Divisions with 0 reports (Pending/Not yet submitted): {len(missing_divisions)} / 63")
for i, m in enumerate(missing_divisions, 1):
    print(f"  {i}. {m}")
