import csv
import json
import re
from collections import defaultdict
from datetime import datetime

# 1. Load both sheets
with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s1_rows = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2_rows = list(csv.reader(f))

# Normalization of GN names (preserve exact sheet name format while fixing minor typos)
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
            
            # Rule 1: Exact photo links match
            if p_a and p_b and (p_a == p_b or len(p_a.intersection(p_b)) >= 1):
                is_dup = True; reason = "එකම ඡායාරූප (Same photo links)"
            # Rule 2: Exact description match
            elif d_a == d_b:
                is_dup = True; reason = "සර්වසම විස්තරය (Exact description)"
            # Rule 3: Resubmitted identical activities in known GNs
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

print(f"Canonical activities: {len(canonical_acts)}")
print(f"Duplicates filtered: {len(duplicates_log)}")
print(f"Total photos attached: {sum(len(a['photos']) for a in canonical_acts)}")

# Month names dictionary
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

# Sort canonical activities by date descending (newest first)
canonical_acts.sort(key=lambda x: x['date'], reverse=True)

# Build formatted activities
formatted_activities = []
for idx, a in enumerate(canonical_acts, 1):
    act_id = f"ACT-{idx:03d}"
    
    # Title from first clause or up to 60 chars of description
    clean = a['desc'].replace('\n', ' ').strip()
    parts = re.split(r'[\.\n\r]+', clean)
    title = parts[0].strip() if parts and len(parts[0].strip()) >= 5 else clean[:50]
    if len(title) > 65:
        title = title[:62] + "..."
        
    # Photos array with direct Google CDN URLs
    photo_objects = []
    for pid in a['photos']:
        photo_objects.append({
            'id': pid,
            'thumbnail': f"https://lh3.googleusercontent.com/d/{pid}=s400",
            'full': f"https://lh3.googleusercontent.com/d/{pid}=s1200",
            'driveUrl': f"https://drive.google.com/file/d/{pid}/view?usp=sharing"
        })
        
    formatted_activities.append({
        'id': act_id,
        'titleSi': title,
        'gnNameSi': a['gn'],
        'sabhaNameSi': f"{a['gn']} ප්‍රජා සංවර්ධන සභාව",
        'date': a['date'],
        'dateRaw': a['date_raw'],
        'reportingMonth': a['month_key'],
        'monthSi': a['month_si'],
        'category': a['cat_id'],
        'categoryNameSi': a['cat_name'],
        'categoryColor': a['cat_color'],
        'categoryIcon': a['cat_icon'],
        'description': a['desc'],
        'images': [p['full'] for p in photo_objects],
        'photoObjects': photo_objects,
        'photoCount': len(photo_objects),
        'source': f"{a['sheet']} R{a['row']} B{a['block']}",
        'statusLabelSi': 'සම්පූර්ණයි'
    })

# Master 63 GN Divisions
# 53 active from sheets + 10 pending
pending_10 = [
    {"nameSi": "109 බදුන්ගොඩ", "series": 109},
    {"nameSi": "112 වලහන්දූව", "series": 112},
    {"nameSi": "112 යග්ගහ", "series": 112},
    {"nameSi": "118 ගනේගොඩ", "series": 118},
    {"nameSi": "130 හාලිවල", "series": 130},
    {"nameSi": "130 කැරැන්විල ජනපදය", "series": 130},
    {"nameSi": "135 මීගොඩ", "series": 135},
    {"nameSi": "135 මැලෑගොඩ", "series": 135},
    {"nameSi": "135 ගල්ගමුව", "series": 135},
    {"nameSi": "135 දිවුලාන", "series": 135}
]

gn_acts_map = defaultdict(list)
for fa in formatted_activities:
    gn_acts_map[fa['gnNameSi']].append(fa)

all_63_gn_divisions = []
# 53 reporting
for gn_name, acts in sorted(gn_acts_map.items()):
    series_match = re.search(r'\b(109|110|112|113|118|130|133|134|135|152|155)\b', gn_name)
    series_num = int(series_match.group(1)) if series_match else 100
    
    unique_days = len(set(a['date'] for a in acts if a['date']))
    unique_cats = len(set(a['category'] for a in acts))
    cat_counts = defaultdict(int)
    for a in acts: cat_counts[a['categoryNameSi']] += 1
    key_sector = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)[0][0] if cat_counts else "ප්‍රජා සංවර්ධන"
    
    dates_sorted = sorted([a['date'] for a in acts if a['date']])
    last_d = dates_sorted[-1] if dates_sorted else ""
    
    all_63_gn_divisions.append({
        'nameSi': gn_name,
        'sabhaNameSi': f"{gn_name} ප්‍රජා සංවර්ධන සභාව",
        'series': series_num,
        'totalProjects': len(acts),
        'completed': len(acts),
        'activeDays': unique_days,
        'diversity': unique_cats,
        'keySectorSi': key_sector,
        'lastReportDate': last_d,
        'statusBadge': 'සම්පූර්ණයි',
        'isReported': True
    })

# 10 pending
for p in pending_10:
    all_63_gn_divisions.append({
        'nameSi': p['nameSi'],
        'sabhaNameSi': f"{p['nameSi']} ප්‍රජා සංවර්ධන සභාව",
        'series': p['series'],
        'totalProjects': 0,
        'completed': 0,
        'activeDays': 0,
        'diversity': 0,
        'keySectorSi': 'වාර්තා අපේක්ෂිතයි',
        'lastReportDate': 'වාර්තා ලැබී නොමැත',
        'statusBadge': 'වාර්තා අපේක්ෂිතයි',
        'isReported': False
    })

# Sort divisions: reporting first by project count desc, then pending
all_63_gn_divisions.sort(key=lambda x: (not x['isReported'], -x['totalProjects'], x['nameSi']))

# Monthly Stats
monthly_map = defaultdict(lambda: {'count': 0, 'active_days': set(), 'divisions': set()})
for a in formatted_activities:
    m = a['reportingMonth']
    monthly_map[m]['count'] += 1
    if a['date']: monthly_map[m]['active_days'].add(a['date'])
    monthly_map[m]['divisions'].add(a['gnNameSi'])

sorted_months = sorted(monthly_map.keys())
monthly_stats = []
cumulative_count = 0

for i, m in enumerate(sorted_months):
    cnt = monthly_map[m]['count']
    cumulative_count += cnt
    year, mo = m.split('-')
    m_name = si_months.get(mo, mo)
    m_si = f"{m_name} {year}"
    
    prev_cnt = monthly_map[sorted_months[i-1]]['count'] if i > 0 else None
    mom = round(((cnt - prev_cnt) / prev_cnt * 100), 1) if prev_cnt else None
    
    monthly_stats.append({
        'monthKey': m,
        'monthSi': m_si,
        'year': int(year),
        'monthNameSi': m_name,
        'count': cnt,
        'completed': cnt,
        'activeDays': len(monthly_map[m]['active_days']),
        'reportingDivisions': len(monthly_map[m]['divisions']),
        'cumulativeCount': cumulative_count,
        'momChangePct': mom
    })

# Weekday Analytics
weekday_counts = {'සඳුදා': 0, 'අඟහරුවාදා': 0, 'බදාදා': 0, 'බ්‍රහස්පතින්දා': 0, 'සිකුරාදා': 0, 'සෙනසුරාදා': 0, 'ඉරිදා': 0}
si_days = ['සඳුදා', 'අඟහරුවාදා', 'බදාදා', 'බ්‍රහස්පතින්දා', 'සිකුරාදා', 'සෙනසුරාදා', 'ඉරිදා']

weekday_total = 0
weekend_total = 0
for a in formatted_activities:
    if a['date']:
        try:
            dt = datetime.strptime(a['date'], '%Y-%m-%d')
            day_idx = dt.weekday()
            day_name = si_days[day_idx]
            weekday_counts[day_name] += 1
            if day_idx < 5: weekday_total += 1
            else: weekend_total += 1
        except:
            pass

total_dated = weekday_total + weekend_total
weekday_pct = round(weekday_total / total_dated * 100, 1) if total_dated else 0
weekend_pct = round(weekend_total / total_dated * 100, 1) if total_dated else 0

weekday_order = ["සඳුදා", "අඟහරුවාදා", "බදාදා", "බ්‍රහස්පතින්දා", "සිකුරාදා", "සෙනසුරාදා", "ඉරිදා"]
weekday_analytics = [
    {
        "daySi": day,
        "count": weekday_counts.get(day, 0),
        "pct": round(weekday_counts.get(day, 0) / len(formatted_activities) * 100, 1)
    }
    for day in weekday_order
]

# Calendar Heatmap
daily_counts = {}
for a in formatted_activities:
    if a['date'] and len(a['date']) == 10 and int(a['date'][:4]) <= 2026:
        daily_counts[a['date']] = daily_counts.get(a['date'], 0) + 1

heatmap_data = [{"date": d, "count": cnt} for d, cnt in sorted(daily_counts.items())]

# Peak Dates
peak_dates = [{"date": d, "count": cnt, "labelSi": f"{d} ({cnt} වැඩසටහන්)"}
              for d, cnt in sorted(daily_counts.items(), key=lambda x: x[1], reverse=True)[:10]]

# Category Stats
cat_counter = defaultdict(int)
for a in formatted_activities:
    cat_counter[a['categoryNameSi']] += 1

analytical_categories = []
for cid, cname, color, icon, _ in CATEGORIES:
    cnt = cat_counter[cname]
    pct = round(cnt / len(formatted_activities) * 100, 1)
    analytical_categories.append({
        'id': cid,
        'nameSi': cname,
        'count': cnt,
        'pct': pct,
        'color': color,
        'icon': icon
    })
# Community fallback
if cat_counter["ප්‍රජා සේවා හා සංවර්ධන"] > 0:
    cnt = cat_counter["ප්‍රජා සේවා හා සංවර්ධන"]
    analytical_categories.append({
        'id': 'community',
        'nameSi': 'ප්‍රජා සේවා හා සංවර්ධන',
        'count': cnt,
        'pct': round(cnt / len(formatted_activities) * 100, 1),
        'color': '#94A3B8',
        'icon': 'bi-people-fill'
    })
analytical_categories.sort(key=lambda x: x['count'], reverse=True)

# Overview Metrics (ONLY Real Sheet Metrics - ZERO fake financial or beneficiary numbers)
overview_metrics = {
    "totalActivities": len(formatted_activities),
    "reportingGnDivisions": len(gn_acts_map),
    "pendingGnDivisions": len(pending_10),
    "totalGNDivisions": 63,
    "totalPhotos": sum(a['photoCount'] for a in formatted_activities),
    "totalActiveDays": len(daily_counts),
    "coveragePercent": round(len(gn_acts_map) / 63 * 100, 1),
    "avgProgrammesPerDivision": round(len(formatted_activities) / len(gn_acts_map), 2),
    "weekdayPct": weekday_pct,
    "weekendPct": weekend_pct,
    "weekdayCount": weekday_total,
    "weekendCount": weekend_total,
    "reportingPeriodSi": "2025 නොවැම්බර් 01 සිට 2026 ඔක්තෝබර් දක්වා",
    "telephone": "+94 91 2242236",
    "email": "info@akmeemana.ds.gov.lk",
    "addressSi": "ප්‍රාදේශීය ලේකම් කාර්යාලය, පින්නදූව, අක්මීමන, ගාල්ල"
}

# Data Quality Log
data_quality_log = {
    'summary': {
        'totalSubmissions': 95,
        'rawActivityBlocks': 290,
        'canonicalActivities': len(formatted_activities),
        'confirmedDuplicates': len(duplicates_log),
        'photosCount': sum(a['photoCount'] for a in formatted_activities),
        'divisionsReported': len(gn_acts_map),
        'divisionsPending': len(pending_10),
        'totalDivisions': 63,
        'coveragePercent': round(len(gn_acts_map) / 63 * 100, 1)
    },
    'duplicates': duplicates_log,
    'pendingDivisions': [p['nameSi'] for p in pending_10]
}

# Save as JSON and generate JS
full_dataset = {
    'overview': overview_metrics,
    'categories': analytical_categories,
    'monthlyStats': monthly_stats,
    'gnDivisions': all_63_gn_divisions,
    'activities': formatted_activities,
    'dataQualityLog': data_quality_log,
    'weekdayAnalytics': weekday_analytics,
    'heatmapData': heatmap_data,
    'peakDates': peak_dates
}

with open('raw_drive_data/canonical_v3.json', 'w', encoding='utf-8') as f:
    json.dump(full_dataset, f, ensure_ascii=False, indent=2)

print("\nSuccessfully compiled canonical_v3.json!")
print(f"Activities: {len(formatted_activities)}")
print(f"GN Divisions: {len(all_63_gn_divisions)} (53 reported, 10 pending)")
print(f"Total Photos: {sum(a['photoCount'] for a in formatted_activities)}")
