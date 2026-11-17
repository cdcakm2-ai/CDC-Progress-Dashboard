import openpyxl
import json
import re
import os
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict

print("=== GENERATING CANONICAL DATASET V9 (440 AUTHENTIC ACTIVITIES) ===")

with open('raw_drive_data/canonical_v4.json', encoding='utf-8') as f:
    v4 = json.load(f)

official_gn_list = [g['nameSi'] for g in v4['gnDivisions']]
official_gn_meta = {g['nameSi']: g for g in v4['gnDivisions']}

def norm_text(text):
    if not text: return ""
    t = str(text).lower()
    return re.sub(r'[\s\.\,\-\_\/\(\)\[\]\:\;]+', '', t).strip()

def standardize_gn(raw_gn):
    raw_norm = norm_text(raw_gn)
    for off in official_gn_list:
        if norm_text(off) == raw_norm: return off
    m_num = re.match(r'^([0-9]+(?:\s*[\/\-]?\s*[a-zA-Z\u0D80-\u0DFF]+)?)', raw_gn.strip())
    if m_num:
        prefix = norm_text(m_num.group(1))
        for off in official_gn_list:
            if norm_text(off).startswith(prefix): return off
    best_match, best_sim = None, 0.0
    for off in official_gn_list:
        s = SequenceMatcher(None, raw_norm, norm_text(off)).ratio()
        if s > best_sim and s > 0.65:
            best_sim, best_match = s, off
    return best_match if best_match else raw_gn.strip()

sheet_files = [
    ('Main Cumulative', 'raw_drive_data/new_imports/sheet_main_responses.xlsx'),
    ('June Monthly', 'raw_drive_data/new_imports/sheet_officers_monthly_responses.xlsx'),
    ('July Monthly', 'raw_drive_data/new_imports/sheet_monthly_responses.xlsx'),
    ('August Monthly', 'raw_drive_data/new_imports/sheet_august_copy.xlsx'),
    ('September Monthly', 'raw_drive_data/new_imports/sheet_august_copy_copy.xlsx'),
]

def parse_date_str(raw, desc):
    raw = str(raw).strip().replace('3025-', '2026-').replace('/3025', '/2026').replace('46266', '2026-08-19')
    if ' ' in raw: raw = raw.split()[0]
    m = re.match(r'^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})', raw)
    if m:
        yr = int(m.group(1))
        if yr < 2024: yr = 2026
        return f"{yr:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = re.match(r'^(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})', raw)
    if m:
        yr = int(m.group(3))
        if yr < 2024: yr = 2026
        p1, p2 = int(m.group(1)), int(m.group(2))
        if p1 > 12 and p2 <= 12: return f"{yr:04d}-{p2:02d}-{p1:02d}"
        elif p2 > 12 and p1 <= 12: return f"{yr:04d}-{p1:02d}-{p2:02d}"
        else: return f"{yr:04d}-{p2:02d}-{p1:02d}"
    m_in = re.search(r'(202[4-6])[\.\/\-](\d{1,2})[\.\/\-](\d{1,2})', desc)
    if m_in:
        return f"{int(m_in.group(1)):04d}-{int(m_in.group(2)):02d}-{int(m_in.group(3)):02d}"
    return "2026-08-01"

def get_drive_ids(text):
    if not text: return []
    return list(dict.fromkeys(re.findall(r'[a-zA-Z0-9_-]{25,}', str(text))))

raw_records = []
for sheet_title, fpath in sheet_files:
    if not os.path.exists(fpath): continue
    wb = openpyxl.load_workbook(fpath, data_only=True)
    ws = wb['Form responses 1']
    rows = list(ws.iter_rows(values_only=True))
    for r_idx, row in enumerate(rows[1:], 2):
        if not row or not any(row): continue
        gn_raw = str(row[2] or "").strip()
        if not gn_raw: continue
        gn = standardize_gn(gn_raw)
        officer = str(row[1] or "").strip()
        
        for s_idx in range(8):
            d_col = 4 + s_idx * 4
            desc_col = 5 + s_idx * 4
            photo_col = 6 + s_idx * 4
            raw_date = str(row[d_col] or "").strip() if d_col < len(row) else ""
            raw_desc = str(row[desc_col] or "").strip() if desc_col < len(row) else ""
            raw_photos = str(row[photo_col] or "").strip() if photo_col < len(row) else ""
            
            if raw_desc or raw_photos or (raw_date and raw_date != '0' and len(raw_date) > 4):
                clean_date = parse_date_str(raw_date, raw_desc)
                p_ids = get_drive_ids(raw_photos)
                raw_records.append({
                    'sheet': sheet_title,
                    'row': r_idx,
                    'slot': s_idx + 1,
                    'officer': officer,
                    'gn_raw': gn_raw,
                    'gn': gn,
                    'date': clean_date,
                    'raw_date': raw_date,
                    'desc': raw_desc,
                    'photos': p_ids
                })

print(f"Total raw activity slots harvested: {len(raw_records)}")

def days_diff(d1_str, d2_str):
    try:
        dt1 = datetime.strptime(d1_str[:10], "%Y-%m-%d")
        dt2 = datetime.strptime(d2_str[:10], "%Y-%m-%d")
        return abs((dt1 - dt2).days)
    except:
        return 999

KEYWORD_GROUPS = [
    ["ඩෙංගු", "දන්සල", "දන්සැල", "ශ්‍රමදාන", "ආරක්ෂක", "බැති ගී", "ජල", "පොසොන්", "අවුරුදු", "වෛද්‍ය", "පිරිසිදු", "ලිඳ", "ලිද", "පොල්", "වී වගා", "පුහුණු", "රූපලාවන්‍ය", "සාහිත්‍ය", "ගම්මිරිස්", "බිම්මල්", "ඉටිපන්දම්", "ක්‍රිකට්", "සුසාන"],
]

def is_duplicate_activity(item, m):
    # Rule 1: Never merge slots from the exact same row unless exact same photos and desc
    if item['sheet'] == m['sheet'] and item['row'] == m['row']:
        if item['desc'] == m['desc'] and item['date'] == m['date']:
            return True, "Identical slot duplicate in same row"
        return False, None
        
    # Rule 2: Must be exact same GN
    if norm_text(item['gn']) != norm_text(m['gn']):
        return False, None
        
    # Rule 3: Shared Google Drive Photo file IDs (absolute physical proof of same event)
    shared_photos = set(item['photos']).intersection(set(m['photos']))
    if len(shared_photos) > 0:
        return True, f"Shared {len(shared_photos)} photo IDs"
        
    t1 = norm_text(item['desc'])
    t2 = norm_text(m['desc'])
    if not t1 or not t2:
        return False, None
        
    sim = SequenceMatcher(None, t1, t2).ratio()
    diff_d = days_diff(item['date'], m['date'])
    same_month = (item['date'][:7] == m['date'][:7])
    
    # Singlish / Sinhala cross-check
    is_dengue_cross = (("dengu" in t1 or "dendu" in t1) and "ඩෙංගු" in t2) or (("dengu" in t2 or "dendu" in t2) and "ඩෙංගු" in t1)
    is_coconut_cross = ("pola" in t1 and "පොල්" in t2) or ("pola" in t2 and "පොල්" in t1)
    
    # Rule 4: Same date duplicates
    if diff_d == 0:
        if is_dengue_cross or is_coconut_cross:
            return True, f"Cross-language (Sinhala/Singlish) on same date ({item['date']})"
            
        distinct_conflicts = [
            ("ඩෙංගු", "අවුරුදු"), ("ආහාර", "ධර්ම"), ("ජෑම්", "රැකියා"), ("පොහොය", "සල්පිල"), ("බෝධි", "දන්සල")
        ]
        is_distinct = False
        for k1, k2 in distinct_conflicts:
            if (k1 in t1 and k2 in t2) or (k2 in t1 and k1 in t2):
                is_distinct = True
                break
        if not is_distinct:
            common_kw = [k for k in KEYWORD_GROUPS[0] if (k in t1 and k in t2)]
            if len(common_kw) > 0 or sim >= 0.30 or t1 in t2 or t2 in t1:
                return True, f"Same date duplicate ({item['date']}) with common elements ({common_kw}, sim={sim:.2f})"
                
    # Rule 5: Days diff <= 2 with high similarity or specific event
    if diff_d <= 2:
        if is_dengue_cross or is_coconut_cross:
            return True, f"Cross-language (Sinhala/Singlish) within {diff_d} days"
        common_kw = [k for k in ["යෝග", "සුවසෙත", "ඇරබික්", "ඇසල", "පොසොන්", "ධර්ම", "ශ්‍රමදාන", "ආරක්ෂක", "ඩෙංගු", "බෝධි"] if (k in t1 and k in t2)]
        if len(common_kw) > 0 and (sim >= 0.35 or t1 in t2 or t2 in t1):
            return True, f"Same event within {diff_d} days ({common_kw}, sim={sim:.2f})"
            
    # Rule 6: High text similarity (same wording resubmitted)
    if sim >= 0.65 and diff_d <= 7:
        return True, f"High text similarity ({sim:.2f}) and close date ({diff_d}d)"
        
    # Rule 7: Text containment in same month
    if same_month and diff_d <= 5 and (t1 in t2 or t2 in t1) and len(min(t1, t2)) > 15:
        return True, f"Text containment in same month ({diff_d}d)"
        
    # Rule 8: Identical wording in same month
    if same_month and sim >= 0.75:
        return True, f"Very high text similarity ({sim:.2f}) in same month"
        
    return False, None

records_by_gn = defaultdict(list)
for r in raw_records:
    records_by_gn[r['gn']].append(r)

clean_pool = []
merges_log = []

for gn_name in sorted(records_by_gn.keys()):
    items = records_by_gn[gn_name]
    gn_master = []
    for item in items:
        matched = None
        reason = None
        for m in gn_master:
            is_dup, r = is_duplicate_activity(item, m)
            if is_dup:
                matched = m
                reason = r
                break
        if matched:
            merges_log.append({
                'gn': gn_name,
                'kept': f"[{matched['sheet']} R{matched['row']} S{matched['slot']}] {matched['date']} | {matched['desc'][:45]}",
                'duplicate': f"[{item['sheet']} R{item['row']} S{item['slot']}] {item['date']} | {item['desc'][:45]}",
                'reason': reason
            })
            for p in item['photos']:
                if p not in matched['photos']:
                    matched['photos'].append(p)
            if len(item['desc']) > len(matched['desc']) and not (re.search(r'[a-zA-Z]{5,}', item['desc']) and not re.search(r'[a-zA-Z]{5,}', matched['desc'])):
                matched['desc'] = item['desc']
        else:
            gn_master.append(item)
    clean_pool.extend(gn_master)

print(f"Total authentic canonical activities: {len(clean_pool)}")

# Helper to categorize
def categorize(desc):
    d = desc.lower()
    if any(k in d for k in ["ඩෙංගු", "දන්සල", "දන්සැල", "ආරෝග්‍ය", "වෛද්‍ය", "සායන", "සුව", "ලේ"]): return "health", "සෞඛ්‍ය හා සනීපාරක්ෂක", "#10B981"
    if any(k in d for k in ["ශ්‍රමදාන", "පිරිසිදු", "කසල", "ගස්", "පැල", "පැළ", "පරිසර", "කාණු"]): return "environment", "පරිසර සංරක්ෂණ හා ශ්‍රමදාන", "#059669"
    if any(k in d for k in ["මාර්ග", "පාලම", "අමුණ", "කොන්ක්‍රිට්", "නිවාස", "වැසිකිලි", "පොළ", "ළිඳ", "ළිද", "ජල"]): return "infrastructure", "යටිතල පහසුකම් සංවර්ධන", "#F59E0B"
    if any(k in d for k in ["පහන්", "පූජා", "වෙසක්", "පොසොන්", "අවුරුදු", "බක්මහ", "ක්‍රිකට්", "සමිතිය", "යෞවන", "ළමා", "සාහිත්‍ය", "භක්ති", "බෝධි"]): return "social", "සමාජ සුබසාධන හා ආගමික", "#3B82F6"
    if any(k in d for k in ["පුහුණු", "මහන", "බිම්මල්", "ආහාර", "ස්වයං", "වගා", "ගම්මිරිස්", "පොල්", "වී වගා"]): return "economic", "ආර්ථික හා ජීවනෝපාය සංවර්ධන", "#8B5CF6"
    return "social", "සමාජ සුබසාධන හා ප්‍රජා සංවර්ධන", "#3B82F6"

# Build final activity objects
all_activities = []
all_photos = []
all_dates = set()

# Sort by GN order first, then by date desc
gn_order = {g: i for i, g in enumerate(official_gn_list)}
clean_pool.sort(key=lambda x: (gn_order.get(x['gn'], 999), x['date'], x['desc']))

for idx, item in enumerate(clean_pool, 1):
    act_id = f"ACT-2026-{idx:04d}"
    cat_id, cat_name, cat_color = categorize(item['desc'])
    
    p_objs = []
    p_thumbs = []
    for p_idx, pid in enumerate(item['photos'], 1):
        p_obj_id = f"{act_id}-P{p_idx:02d}"
        thumb = f"https://lh3.googleusercontent.com/d/{pid}=w1200-h800"
        full = f"https://lh3.googleusercontent.com/d/{pid}=w1200-h800"
        drive_url = f"https://drive.google.com/file/d/{pid}/view?usp=sharing"
        p_data = {
            'id': p_obj_id,
            'activityId': act_id,
            'titleSi': item['desc'][:60],
            'gnDivision': item['gn'],
            'date': item['date'],
            'thumbnail': thumb,
            'full': full,
            'driveUrl': drive_url,
            'caption': f"{item['desc'][:70]} - {item['gn']}"
        }
        p_objs.append(p_data)
        p_thumbs.append(thumb)
        all_photos.append(p_data)
        
    all_dates.add(item['date'])
    
    act_obj = {
        'id': act_id,
        'titleSi': item['desc'][:70].strip(),
        'titleEn': item['desc'][:70].strip(),
        'category': cat_id,
        'categoryNameSi': cat_name,
        'categoryColor': cat_color,
        'gnId': f"GN-{gn_order.get(item['gn'], 999) + 1}",
        'gnNameSi': item['gn'],
        'gnNameEn': item['gn'],
        'sabhaNameSi': f"{item['gn']} ප්‍රජා සංවර්ධන සභාව",
        'date': item['date'],
        'year': int(item['date'][:4]),
        'month': item['date'][:7],
        'status': 'completed',
        'statusSi': 'සම්පූර්ණයි',
        'beneficiaries': 'ප්‍රදේශවාසී ගම්වාසීන්',
        'progress': 100,
        'locationSi': item['gn'],
        'purposeSi': f"{item['gn']} ප්‍රජා සංවර්ධන සභාව මගින් ග්‍රාමීය සංවර්ධනය හා ප්‍රජා සවිබලගැන්වීම.",
        'actionsSi': item['desc'],
        'resultsSi': 'ප්‍රජා සහභාගීත්වයෙන් සාර්ථකව නිම කරන ලදී.',
        'description': item['desc'],
        'photoCount': len(p_objs),
        'photoObjects': p_objs,
        'images': p_thumbs,
        'sourceSheet': item['sheet']
    }
    all_activities.append(act_obj)

print(f"Total generated activities: {len(all_activities)}")
print(f"Total photos: {len(all_photos)}")
print(f"Total distinct dates: {len(all_dates)}")

# Recalculate GN stats
gn_divisions = []
for g_orig in v4['gnDivisions']:
    gname = g_orig['nameSi']
    g_acts = [a for a in all_activities if a['gnNameSi'] == gname]
    g_photos = [p for p in all_photos if p['gnDivision'] == gname]
    g_dates = set(a['date'] for a in g_acts)
    g_cats = set(a['category'] for a in g_acts)
    last_d = max(g_dates) if g_dates else "2026-08-30"
    
    gn_divisions.append({
        'id': f"GN-{gn_order.get(gname, 999) + 1}",
        'nameSi': gname,
        'nameEn': gname,
        'sabhaNameSi': f"{gname} ප්‍රජා සංවර්ධන සභාව",
        'keySectorSi': g_orig.get('keySectorSi', 'සමාජ සුබසාධන'),
        'totalProjects': len(g_acts),
        'completed': len(g_acts),
        'ongoing': 0,
        'progress': 100,
        'activeDays': len(g_dates),
        'totalPhotos': len(g_photos),
        'diversity': max(1, len(g_cats)),
        'lastReportDate': last_d,
        'statusBadge': 'වාර්තා කර ඇත',
        'isReporting': len(g_acts) > 0
    })

# Monthly stats calculation
month_counts = defaultdict(int)
month_dates = defaultdict(set)
month_photos = defaultdict(int)
for a in all_activities:
    m = a['month']
    month_counts[m] += 1
    month_dates[m].add(a['date'])
    month_photos[m] += a['photoCount']

monthly_stats = []
for m in sorted(month_counts.keys()):
    monthly_stats.append({
        'month': m,
        'totalActivities': month_counts[m],
        'completed': month_counts[m],
        'activeDays': len(month_dates[m]),
        'totalPhotos': month_photos[m]
    })

# Category counts
cat_counts = defaultdict(int)
for a in all_activities:
    cat_counts[a['category']] += 1

categories = []
for c in v4.get('categories', []):
    cid = c['id']
    c_copy = dict(c)
    c_copy['count'] = cat_counts.get(cid, 0)
    categories.append(c_copy)

final_data = {
    'summary': {
        'totalActivities': len(all_activities),
        'totalCompleted': len(all_activities),
        'totalOngoing': 0,
        'overallProgress': 100,
        'totalReportingGNs': len([g for g in gn_divisions if g['totalProjects'] > 0]),
        'totalGNDivisions': 63,
        'totalActiveDays': len(all_dates),
        'totalPhotos': len(all_photos),
        'totalDuplicatesRemoved': len(merges_log),
        'lastUpdated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    'categories': categories,
    'gnDivisions': gn_divisions,
    'activities': all_activities,
    'photos': all_photos,
    'monthlyStats': monthly_stats,
    'monthlySummary': monthly_stats,
    'mergesLog': merges_log
}

with open('raw_drive_data/canonical_v9.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("Saved raw_drive_data/canonical_v9.json successfully!")
