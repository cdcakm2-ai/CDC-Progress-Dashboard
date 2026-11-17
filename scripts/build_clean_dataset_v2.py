import csv
import json
import re
from collections import defaultdict
from datetime import datetime

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s1_rows = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2_rows = list(csv.reader(f))

def clean_gn_name(g):
    s = re.sub(r'\s+', ' ', g).strip()
    s = s.replace('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල')
    s = s.replace('109 ඉහලගොඩ බටහිර', '109 ඉහළගොඩ බටහිර')
    s = s.replace('112/සී කිරින්ඳගොඩ', '112/සී කිරින්දගොඩ')
    return s

def clean_desc(d):
    s = re.sub(r'[\r\n\t]+', ' ', d)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

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
            elif p2 < 100:
                year = 2000 + p2
                if p1 > 12 and p0 <= 12: p0, p1 = p1, p0
                return f"{year:04d}-{p1:02d}-{p0:02d}"
        except:
            pass
    return d_str.strip()

# 10 Official Categories based on keywords
CATEGORIES = [
    ("dengue", "ඩෙංගු මර්දන වැඩසටහන්", "#EF4444", "bi-shield-check", [
        "ඩෙංගු", "ඩෙන්ගු", "දිරාපත්", "කීට", "පරිශ්‍ර පරීක්ෂා", "දුමාර", "මදුරු"
    ]),
    ("environment", "පරිසර හා ශ්‍රමදාන", "#10B981", "bi-tree-fill", [
        "ශ්‍රමදාන", "පිරිසිදු", "කාණු", "පරිසර", "පැළ", "රුක් රෝපණ", "ගස්", "පිරිසිදුකිරීම", "ප්ලාස්ටික්", "කසල", "රුක්රෝපණ", "අත්තම", "සුසාන"
    ]),
    ("infrastructure", "යටිතල පහසුකම් සංවර්ධනය", "#3B82F6", "bi-building", [
        "මාර්ග", "මාගය", "පාර", "පාලම්", "ජල", "විදුලි", "ගොඩනැගිලි", "අලුත්වැඩියා", "කොන්ක්‍රීට්", "කොන්ක්‍රිට්", "බෝක්කු", "ගල්බැම්ම", "බැම්ම", "නල", "ළිං", "ප්‍රතිසංස්කරණ", "ප්‍රතිසංස්කරණය", "ඉදිකිරිම", "ඉදිකිරීම", "සොල්ලා", "ලයිට්", "වාරි", "අමුණ"
    ]),
    ("welfare", "සමාජ සුභසාධන වැඩසටහන්", "#EC4899", "bi-heart-pulse-fill", [
        "වැඩිහිටි", "ආධාර", "වියළි ආහාර", "වියලි", "උපකරණ", "නිවාස", "නිවස", "සුභසාධන", "විශේෂ අවශ්‍යතා", "සහනාධාර", "ආපදා", "විපතට", "ජංගම සේවය", "සත්කාර", "ප්‍රතිලාභ", "සනීපාරක්ෂක", "තමන්ගේම තැනක්"
    ]),
    ("agriculture", "කෘෂිකාර්මික හා ගෙවතු වගා", "#84CC16", "bi-flower1", [
        "ගෙවතු", "වගා", "බීජ", "පොහොර", "කෘෂි", "එළවළු", "පළතුරු", "බිම්මල්", "කොම්පෝස්ට්", "පැළ බෙදා", "පොකුරු ගම්මාන", "ධාන්‍ය", "ගම්මිරිස්", "තේ ගම්මාන", "පොල් වගාව"
    ]),
    ("health", "සෞඛ්‍ය හා වෛද්‍ය සායන", "#06B6D4", "bi-hospital-fill", [
        "සායන", "සෞඛ්‍ය", "වෛද්‍ය", "ලේ දන්දීමේ", "ලේ පරිත්‍යාග", "සුවනාරි", "දන්ත", "ඇස්", "පෝෂණ", "ඖෂධ", "සුව දිවිය"
    ]),
    ("livelihood", "ස්වයං රැකියා හා ජීවනෝපාය", "#F59E0B", "bi-briefcase-fill", [
        "ස්වයං රැකියා", "ස්වයංරැකියා", "ජීවනෝපාය", "පුහුණු", "පුහුනු", "මහන", "අත්කම්", "ආහාර නිෂ්පාදන", "ව්‍යවසායක", "ඉටිපන්දම්", "ඉටි පන්දම්", "රූපලාවන්‍ය", "රුපලාවනය", "කොණ්ඩ", "කොන්ඩ", "බාබර්", "කේක්", "මල් සැකසුම්", "විසිතුරු සතුන්", "පොල පැවැත්වීම", "සංචාරක සංගමය", "පොළ ආරම්භ", "අවුරුදු පොළ"
    ]),
    ("education", "අධ්‍යාපන, ළමා හා ක්‍රීඩා", "#8B5CF6", "bi-book-half", [
        "පෙරපාසල්", "පාසල්", "ළමා", "ළමුන්", "ක්‍රීඩා", "ක්‍රිකට්", "පොත්", "ශිෂ්‍ය", "පුස්තකාල", "දරු", "සංගීත", "චිත්‍ර", "නිපුණතා", "ශිෂ්‍යත්ව", "සිනමා", "චිත්‍රපට"
    ]),
    ("religious", "ආගමික හා සංස්කෘතික", "#D97706", "bi-stars", [
        "පෙරහැර", "බෝධි පූජා", "පිරිත්", "දාන", "දන්සල", "පන්සල්", "ආගමික", "සංස්කෘතික", "අවුරුදු", "බක්මහ", "වෙසක්", "පොසොන්", "පූජාව", "සැමරුම", "නිදහස් දින", "වෛශාක්‍ය", "පින්කම", "සෙත් පතා", "boodi puujaavak", "ඉෆ්තාර්", "DJ", "සංගීත සැදෑව"
    ]),
    ("awareness", "ප්‍රජා දැනුවත් කිරීම් හා ධාරිතා", "#6366F1", "bi-megaphone-fill", [
        "දැනුවත්", "සමිතිය", "රැස්වීම", "දේශන", "වැඩමුළු", "නීති", "මහජන", "ධාරිතා", "සාකච්ඡා", "කමිටු", "තොරතුරු දැනගැනීමේ", "ඵලදායිතා"
    ]),
]

def classify_activity(text):
    text_lower = text.lower()
    for cat_id, cat_name, color, icon, keywords in CATEGORIES:
        for kw in keywords:
            if kw in text_lower:
                return cat_id, cat_name, color, icon
    return "community", "ප්‍රජා සේවා හා සංවර්ධන", "#94A3B8", "bi-people-fill"

all_acts = []
for s_name, rows in [("Sheet 1", s1_rows), ("Sheet 2", s2_rows)]:
    for r_idx, r in enumerate(rows[1:], 1):
        if len(r) < 4: continue
        gn = clean_gn_name(r[2])
        for b in range(8):
            col_d = 4 + b * 4
            col_desc = 5 + b * 4
            col_p = 6 + b * 4
            if col_d >= len(r) or col_desc >= len(r): break
            d = r[col_d].strip()
            desc = clean_desc(r[col_desc])
            p = r[col_p].strip() if col_p < len(r) else ""
            if not d and not desc: continue
            
            photos = []
            f1 = re.findall(r'id=([a-zA-Z0-9_-]{15,})', p)
            f2 = re.findall(r'/d/([a-zA-Z0-9_-]{15,})', p)
            for fid in f1 + f2:
                if fid not in photos: photos.append(fid)
                
            all_acts.append({
                'id': f"{s_name[:2].upper()}-R{r_idx}-B{b+1}",
                'sheet': s_name,
                'row': r_idx,
                'block': b + 1,
                'gn': gn,
                'date_raw': d,
                'date': parse_d(d),
                'desc': desc,
                'photos': photos
            })

by_gn = defaultdict(list)
for a in all_acts:
    by_gn[a['gn']].append(a)

canonical_acts = []
duplicates_log = []

for gn, items in by_gn.items():
    handled = set()
    for i in range(len(items)):
        if i in handled: continue
        it_a = items[i]
        dups = []
        for j in range(i + 1, len(items)):
            if j in handled: continue
            it_b = items[j]
            
            p_a = set(it_a['photos'])
            p_b = set(it_b['photos'])
            d_a = it_a['desc'].lower()
            d_b = it_b['desc'].lower()
            
            is_dup = False
            reason = ""
            
            # 1. Exact same photos
            if p_a and p_b and (p_a == p_b or len(p_a.intersection(p_b)) >= 1):
                is_dup = True; reason = "එකම ඡායාරූප (Same photo links)"
            # 2. Exact same desc
            elif d_a == d_b:
                is_dup = True; reason = "සර්වසම විස්තරය (Exact description)"
            # 3. Known resubmissions
            elif "109/ ජී ඇටඹගස්මුල්ල" in gn:
                if "ක්‍රිකට්" in d_a and "ක්‍රිකට්" in d_b:
                    is_dup = True; reason = "ක්‍රිකට් තරගාවලිය (Resubmitted cricket match)"
                elif ("බක්මහ" in d_a or "බක් මහ" in d_a) and ("බක්මහ" in d_b or "බක් මහ" in d_b):
                    is_dup = True; reason = "බක්මහ අවුරුදු උළෙල (Resubmitted Bakmaha festival)"
                elif "පහන්" in d_a and "පහන්" in d_b:
                    is_dup = True; reason = "පහන් පූජාව (Resubmitted pahan pooja)"
                elif "පාන්" in d_a and "පාන්" in d_b and "දන්සල" in d_a and "දන්සල" in d_b:
                    is_dup = True; reason = "පාන් දන්සල (Resubmitted bread dansala)"
                elif "ඩෙංගු" in d_a and "ඩෙංගු" in d_b and it_a['date'] == it_b['date']:
                    is_dup = True; reason = "2026-06-27 ඩෙංගු මර්දන වැඩසටහන (Resubmitted dengue program)"
            elif "155/ ඊ හියාරේ ඉහළ" in gn:
                if "ශ්‍රමදාන" in d_a and "ශ්‍රමදාන" in d_b and it_a['date'] == it_b['date']:
                    is_dup = True; reason = "2026-06-26 ශ්‍රමදාන වැඩසටහන (Resubmitted shramadana)"
                elif "15/07/2026" in it_a['date_raw'] and "15/07/2026" in it_b['date_raw']:
                    is_dup = True; reason = "2026-07-15 ප්‍රජා ශක්ති කමිටු වැඩසටහන (Resubmitted committee program)"
            elif "109/බී ඉහළගොඩ දකුණ" in gn:
                if "ඉටිපන්දම්" in d_a and "ඉටිපන්දම්" in d_b:
                    is_dup = True; reason = "2026-06-25 ඉටිපන්දම් පුහුණු වැඩසටහන (Resubmitted candle training)"
            elif "152 /බී තලහිටියාව" in gn:
                if "ඩෙංගු" in d_a and "ඩෙංගු" in d_b and "25/07/2026" in it_a['date_raw'] and "25/07/2026" in it_b['date_raw']:
                    is_dup = True; reason = "2026-07-25 ඩෙංගු මර්දනය ශ්‍රමදානය (Resubmitted dengue shramadana)"
            elif "133 /ඊ තල්පෙගොඩ" in gn:
                if "ඩෙංගු" in d_a and "ඩෙංගු" in d_b and "27/06/2026" in it_a['date_raw'] and "27/06/2026" in it_b['date_raw']:
                    is_dup = True; reason = "2026-06-27 ඩෙංගු දැනුවත් කිරීම (Resubmitted dengue awareness)"
            elif "133/සී නාගහවත්ත" in gn:
                if "dj" in d_a and "dj" in d_b and "05/09/2026" in it_a['date_raw'] and "05/09/2026" in it_b['date_raw']:
                    is_dup = True; reason = "2026-09-05 DJ සංගීත සැදෑව (Sheet 1 vs Sheet 2 duplicate)"
            elif "130/ ඊ අම්බලන්වත්ත" in gn:
                if ("කොණ්ඩා" in d_a or "කොන්ඩා" in d_a) and ("කොණ්ඩා" in d_b or "කොන්ඩා" in d_b) and it_a['date'] == it_b['date']:
                    is_dup = True; reason = "2026-09-12 රූපලාවන්‍ය හා කොණ්ඩා කැපීමේ වැඩසටහන (Sheet 1 vs Sheet 2 duplicate)"
                    
            if is_dup:
                dups.append((it_b, reason))
                handled.add(j)
                
        best_desc = it_a['desc']
        for dup_item, _ in dups:
            if len(dup_item['desc']) > len(best_desc):
                best_desc = dup_item['desc']
        all_p = list(dict.fromkeys(it_a['photos'] + [p for d_it, _ in dups for p in d_it['photos']]))
        
        can_item = dict(it_a)
        can_item['desc'] = best_desc
        can_item['photos'] = all_p
        can_item['dup_count'] = len(dups)
        canonical_acts.append(can_item)
        
        for d_it, r_text in dups:
            duplicates_log.append({
                'gn': gn,
                'canonical': it_a,
                'dup': d_it,
                'reason': r_text
            })

print(f"Total Canonical Unique Activities: {len(canonical_acts)}")
print(f"Total Filtered Duplicates: {len(duplicates_log)}")
print(f"Total Attached Photo IDs: {sum(len(a['photos']) for a in canonical_acts)}")

# Check date formatting & months
si_months = {
    '01': 'ජනවාරි', '02': 'පෙබරවාරි', '03': 'මාර්තු', '04': 'අප්‍රේල්',
    '05': 'මැයි', '06': 'ජූනි', '07': 'ජූලි', '08': 'අගෝස්තු',
    '09': 'සැප්තැම්බර්', '10': 'ඔක්තෝබර්', '11': 'නොවැම්බර්', '12': 'දෙසැම්බර්'
}

# Fix 3 year typos for sorting/aggregating cleanly:
for a in canonical_acts:
    d = a['date']
    if '3025-06-25' in d: a['date'] = '2026-06-25'
    elif '2926-06-22' in d: a['date'] = '2026-06-22'
    elif '2027-05-28' in d: a['date'] = '2026-05-28'
    
    # reporting month
    m_key = a['date'][:7] if len(a['date']) >= 7 else '2026-07'
    p = m_key.split('-')
    m_si = f"{si_months.get(p[1], p[1])} {p[0]}" if len(p) == 2 else m_key
    a['month_key'] = m_key
    a['month_si'] = m_si
    
    cat_id, cat_name, cat_color, cat_icon = classify_activity(a['desc'])
    a['cat_id'] = cat_id
    a['cat_name'] = cat_name
    a['cat_color'] = cat_color
    a['cat_icon'] = cat_icon

print("Successfully verified and processed clean dataset v2!")
