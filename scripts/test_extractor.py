import csv
import json
import re
from datetime import datetime

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

# 63 Official names
with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'const ALL_63_GN_DIVISIONS\s*=\s*(\[[\s\S]*?\n\]);', text)
names_63 = re.findall(r'"nameSi":\s*"([^"]+)"', match.group(1))

def normalize_gn(raw):
    s = raw.strip()
    if s in custom_map:
        return custom_map[s]
    for off in names_63:
        if off == s or (off in s and len(off) > 3):
            return off
    for k, v in custom_map.items():
        if k in s or s in k:
            return v
    return s

def parse_date(date_str, default_year=2026):
    s = date_str.strip()
    if not s:
        return None, "හිස් දිනයක් (Empty date)"
    # Clean common typos
    s = s.replace('.', '/').replace('-', '/').replace(' ', '')
    # Check format DD/MM/YYYY or YYYY/MM/DD or D/M/YYYY
    parts = s.split('/')
    if len(parts) == 3:
        try:
            p0, p1, p2 = int(parts[0]), int(parts[1]), int(parts[2])
            # Check if p2 is year (e.g. 2025, 2026)
            if p2 >= 2000:
                # p0 is day, p1 is month (or vice versa)
                # In Sri Lankan contexts, DD/MM/YYYY is standard
                day, month, year = p0, p1, p2
                if month > 12 and day <= 12: # MM/DD swap
                    day, month = month, day
                dt = datetime(year, month, day)
                return dt.strftime('%Y-%m-%d'), None
            elif p0 >= 2000: # YYYY/MM/DD
                year, month, day = p0, p1, p2
                dt = datetime(year, month, day)
                return dt.strftime('%Y-%m-%d'), None
            elif p2 < 100: # 2-digit year e.g. 25, 26
                year = 2000 + p2
                day, month = p0, p1
                if month > 12 and day <= 12:
                    day, month = month, day
                dt = datetime(year, month, day)
                return dt.strftime('%Y-%m-%d'), None
        except Exception as e:
            return None, f"දිනය හඳුනාගත නොහැක: {s} ({str(e)})"
    elif len(parts) == 2: # e.g. 25/08
        try:
            day, month = int(parts[0]), int(parts[1])
            dt = datetime(default_year, month, day)
            return dt.strftime('%Y-%m-%d'), "වසර ස්වයංක්‍රීයව එක් කරන ලදී"
        except Exception as e:
            return None, f"දිනය වලංගු නැත: {s}"
    return None, f"නොදන්නා දින ආකෘතිය: {s}"

# Categories rules
CATEGORIES = [
    ("dengue", "ඩෙංගු මර්දන වැඩසටහන්", ["ඩෙංගු", "දිරාපත්", "කීට", "පරිශ්‍ර පරීක්ෂා", "දුමාර", "මදුරු"]),
    ("environment", "පරිසර හා ශ්‍රමදාන", ["ශ්‍රමදාන", "පිරිසිදු", "කාණු", "පාර", "පරිසර", "පැළ", "රුක් රෝපණ", "ගස්"]),
    ("agriculture", "කෘෂිකාර්මික හා ගෙවතු වගා", ["ගෙවතු", "වගා", "බීජ", "පොහොර", "කෘෂි", "එළවළු", "පළතුරු", "බිම්මල්"]),
    ("health", "සෞඛ්‍ය හා වෛද්‍ය සායන", ["සායන", "සෞඛ්‍ය", "වෛද්‍ය", "ලේ දන්දීමේ", "සුවනාරි", "දන්ත", "ඇස්", "පෝෂණ"]),
    ("education", "අධ්‍යාපන, ළමා හා ක්‍රීඩා", ["පෙරපාසල්", "පාසල්", "ළමා", "ක්‍රීඩා", "පොත්", "ශිෂ්‍ය", "පුස්තකාල", "දරු"]),
    ("welfare", "සමාජ සුභසාධන", ["වැඩිහිටි", "ආධාර", "වියළි ආහාර", "උපකරණ", "නිවාස", "සුභසාධන", "විශේෂ අවශ්‍යතා", "සහනාධාර"]),
    ("religious", "ආගමික හා සංස්කෘතික", ["පෙරහැර", "බෝධි පූජා", "පිරිත්", "දාන", "පන්සල්", "ආගමික", "සංස්කෘතික", "අවුරුදු", "වෙසක්", "පොසොන්"]),
    ("livelihood", "ස්වයං රැකියා හා ජීවනෝපාය", ["ස්වයං රැකියා", "ජීවනෝපාය", "පුහුණු", "මහන", "අත්කම්", "ආහාර නිෂ්පාදන", "ව්‍යවසායක"]),
    ("infrastructure", "යටිතල පහසුකම්", ["මාර්ග", "පාලම්", "ජල", "විදුලි", "ගොඩනැගිලි", "අලුත්වැඩියා", "කොන්ක්‍රීට්", "බෝක්කු"]),
    ("awareness", "ප්‍රජා දැනුවත් කිරීම්", ["දැනුවත්", "සමිතිය", "රැස්වීම", "දේශන", "වැඩමුළු", "නීති", "මහජන"]),
]

def classify_activity(text):
    text_lower = text.lower()
    for cat_id, cat_name, keywords in CATEGORIES:
        for kw in keywords:
            if kw in text_lower:
                return cat_id, cat_name
    return "other", "වෙනත් / බහුවිධ සංවර්ධන"

# Extract activities
raw_activities = []
date_issues = []
photo_links_count = 0

for sheet_idx, (sheet_file, default_month, label) in enumerate([
    ('raw_drive_data/sheet1_form_responses_1.csv', '2026-07', 'Sheet 1 (Nov 2025 - Jul 2026)'),
    ('raw_drive_data/sheet2_form_responses_1.csv', '2026-08', 'Sheet 2 (Aug - Oct 2026)')
]):
    with open(sheet_file, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row_num, row in enumerate(reader, 2):
            if len(row) < 4:
                continue
            timestamp = row[0].strip() if len(row) > 0 else ""
            officer_name = row[1].strip() if len(row) > 1 else "" # keep internal, never output in public UI
            raw_gn = row[2].strip() if len(row) > 2 else ""
            claimed_count = row[3].strip() if len(row) > 3 else "0"
            
            gn_norm = normalize_gn(raw_gn)
            
            # Inspect 8 blocks: block i: start_col = 4 + i*4
            for block in range(8):
                d_idx = 4 + block * 4
                desc_idx = 5 + block * 4
                p_idx = 6 + block * 4
                
                if d_idx >= len(row) or desc_idx >= len(row):
                    break
                    
                raw_date = row[d_idx].strip()
                raw_desc = row[desc_idx].strip()
                raw_photos = row[p_idx].strip() if p_idx < len(row) else ""
                
                if not raw_date and not raw_desc:
                    continue # empty block
                    
                parsed_d, date_err = parse_date(raw_date)
                if date_err:
                    date_issues.append({
                        'sheet': label,
                        'row': row_num,
                        'block': block + 1,
                        'gn': gn_norm,
                        'raw_date': raw_date,
                        'issue': date_err
                    })
                    
                # Extract photo URLs
                # photos can be comma-separated or space-separated URLs
                p_urls = []
                if raw_photos:
                    # find all drive ids or links
                    found = re.findall(r'id=([a-zA-Z0-9_-]+)', raw_photos)
                    for fid in found:
                        photo_links_count += 1
                        p_urls.append(fid)
                    if not found:
                        # try other drive link formats
                        found_alt = re.findall(r'/d/([a-zA-Z0-9_-]+)', raw_photos)
                        for fid in found_alt:
                            photo_links_count += 1
                            p_urls.append(fid)
                
                cat_id, cat_name = classify_activity(raw_desc)
                
                raw_activities.append({
                    'sheet': label,
                    'row': row_num,
                    'block': block + 1,
                    'timestamp': timestamp,
                    'gn_raw': raw_gn,
                    'gn_name': gn_norm,
                    'date_raw': raw_date,
                    'date': parsed_d,
                    'description': raw_desc,
                    'photos': p_urls,
                    'cat_id': cat_id,
                    'cat_name': cat_name
                })

print(f"Total raw activity blocks extracted: {len(raw_activities)}")
print(f"Total photo IDs extracted: {photo_links_count}")
print(f"Total date parsing issues: {len(date_issues)}")
if date_issues:
    print("Date issues preview:")
    for d in date_issues[:10]:
        print(f"  {d['sheet']} Row {d['row']}: {d['raw_date']} -> {d['issue']}")
