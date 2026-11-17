import json
import re
import os
import csv
from datetime import datetime
from difflib import SequenceMatcher

# 1. Load official GN divisions
with open('raw_drive_data/canonical_v4.json', encoding='utf-8') as f:
    v4 = json.load(f)

official_gn_list = [g['nameSi'] for g in v4['gnDivisions']]
official_gn_meta = {g['nameSi']: g for g in v4['gnDivisions']}

def norm_text(text):
    if not text: return ""
    t = str(text).lower()
    t = re.sub(r'[\s\.\,\-\_\/\(\)\[\]\:\;]+', ' ', t).strip()
    return t

def standardize_gn(raw_gn):
    raw_norm = norm_text(raw_gn)
    for off in official_gn_list:
        if norm_text(off) == raw_norm:
            return off
    m_num = re.match(r'^([0-9]+(?:\s*[\/\-]?\s*[a-zA-Z\u0D80-\u0DFF]+)?)', raw_gn.strip())
    if m_num:
        prefix = norm_text(m_num.group(1))
        for off in official_gn_list:
            if norm_text(off).startswith(prefix):
                return off
    best_match = None
    best_sim = 0.0
    for off in official_gn_list:
        s = SequenceMatcher(None, raw_norm, norm_text(off)).ratio()
        if s > best_sim and s > 0.65:
            best_sim = s
            best_match = off
    return best_match if best_match else raw_gn.strip()

# 2. Load nw.docx
docx_items = []
with open('raw_drive_data/new_imports/nw_docx_extracted.txt', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

cur_gn = ""
for line in lines:
    m_gn = re.match(r'^\d+\.\s*([0-9]+[^\n]+?)\s*වසම\s*$', line)
    if m_gn:
        cur_gn = m_gn.group(1).strip()
        continue
    m_act = re.match(r'^([^-]+?)\s*-\s*(\d{4}-\d{2}-\d{2})\s*(.*)$', line)
    if m_act:
        docx_items.append({
            'gn': standardize_gn(cur_gn),
            'title': m_act.group(1).strip(),
            'date': m_act.group(2).strip(),
            'desc': m_act.group(3).strip(),
            'raw': line
        })
    else:
        m_date = re.search(r'(\d{4}-\d{2}-\d{2})', line)
        if m_date:
            parts = line.split(m_date.group(1))
            docx_items.append({
                'gn': standardize_gn(cur_gn),
                'title': parts[0].replace('-', '').strip(),
                'date': m_date.group(1),
                'desc': parts[1].strip() if len(parts) > 1 else "",
                'raw': line
            })

def get_drive_ids(text):
    if not text: return []
    ids = []
    for m in re.finditer(r'id=([a-zA-Z0-9_-]{25,})', str(text)):
        ids.append(m.group(1))
    for m in re.finditer(r'/d/([a-zA-Z0-9_-]{25,})', str(text)):
        ids.append(m.group(1))
    seen = set()
    res = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            res.append(i)
    return res

def normalize_date(raw_date, desc_text, gn_name):
    raw = str(raw_date).strip()
    norm_d = norm_text(desc_text)
    norm_g = norm_text(gn_name)
    
    best_docx = None
    best_sim = 0.0
    for doc in docx_items:
        if norm_text(doc['gn']) == norm_g or norm_text(doc['gn']) in norm_g or norm_g in norm_text(doc['gn']):
            s1 = SequenceMatcher(None, norm_d, norm_text(doc['desc'])).ratio()
            s2 = SequenceMatcher(None, norm_d, norm_text(doc['title'])).ratio()
            score = max(s1, s2)
            if score > best_sim and score > 0.50:
                best_sim = score
                best_docx = doc
    
    if best_docx:
        return best_docx['date'], best_docx['title'], 'docx_verified'
    
    raw = raw.replace('3025-', '2026-').replace('/3025', '/2026').replace('46266', '2026-08-19')
    
    m = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', raw)
    if m:
        yr = int(m.group(1))
        if yr < 2024: yr = 2026
        return f"{yr:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}", None, 'parsed'
    
    m = re.match(r'^(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})', raw)
    if m:
        yr = int(m.group(3))
        if yr < 2024: yr = 2026
        return f"{yr:04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}", None, 'parsed'
    
    m_in = re.search(r'(202[4-6])[\.\/\-](\d{1,2})[\.\/\-](\d{1,2})', desc_text)
    if m_in:
        return f"{int(m_in.group(1)):04d}-{int(m_in.group(2)):02d}-{int(m_in.group(3)):02d}", None, 'desc_extracted'
    
    return "2026-08-01", None, 'default'

# Harvest raw blocks
sheets_to_read = [
    ('Main Cumulative (Nov-Jul)', 'raw_drive_data/new_imports/csvs/sheet_main_responses_Form responses 1.csv'),
    ('June Monthly Responses', 'raw_drive_data/new_imports/csvs/sheet_officers_monthly_responses_Form responses 1.csv'),
    ('July Monthly Responses', 'raw_drive_data/new_imports/csvs/sheet_monthly_responses_Form responses 1.csv'),
    ('August Monthly Responses', 'raw_drive_data/new_imports/csvs/sheet_august_copy_Form responses 1.csv'),
    ('September Monthly Responses', 'raw_drive_data/new_imports/csvs/sheet_august_copy_copy_Form responses 1.csv'),
]

raw_records = []
for sheet_title, csv_path in sheets_to_read:
    if not os.path.exists(csv_path): continue
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for r_idx, row in enumerate(reader):
            if not row or not any(row): continue
            ts = row[0].strip() if len(row) > 0 else ""
            officer = row[1].strip() if len(row) > 1 else ""
            gn_raw = row[2].strip() if len(row) > 2 else ""
            gn = standardize_gn(gn_raw)
            for b_idx in range(6):
                d_col = 4 + b_idx * 4
                desc_col = 5 + b_idx * 4
                photo_col = 6 + b_idx * 4
                if d_col < len(row) and desc_col < len(row):
                    raw_date = row[d_col].strip()
                    raw_desc = row[desc_col].strip()
                    raw_photos = row[photo_col].strip() if photo_col < len(row) else ""
                    if raw_desc or raw_photos or (raw_date and raw_date != '0' and len(raw_date) > 4):
                        p_ids = get_drive_ids(raw_photos)
                        clean_date, docx_title, date_src = normalize_date(raw_date, raw_desc, gn)
                        raw_records.append({
                            'sheet': sheet_title,
                            'row': r_idx + 2,
                            'block': b_idx + 1,
                            'timestamp': ts,
                            'officer': officer,
                            'gn': gn,
                            'raw_date': raw_date,
                            'date': clean_date,
                            'docx_title': docx_title,
                            'date_src': date_src,
                            'desc': raw_desc,
                            'photo_ids': p_ids
                        })

print(f"Total raw activity blocks: {len(raw_records)}")

DISTINCT_KEYWORDS = [
    "දන්සල", "දන්සැල", "ක්‍රිකට්", "අවුරුදු", "බක්මහ", "පහන්", "ඩෙංගු", "ශ්‍රමදාන", 
    "තණකොළ", "පොළ", "බෝධි", "පූජා", "පුහුණු", "මහන", "බිම්මල්", "පැළ", "පැල", 
    "පොත්", "ආධාර", "ආශිර්වාද", "වැසිකිලි", "මාර්ග", "පාලම", "අමුණ", "කාණු", 
    "වෙසක්", "පොසොන්", "ලේ දන්දීම", "වෛද්‍ය", "සායන", "ගර්භනී", "වැඩිහිටි",
    "කවි මඩුව", "භක්ති ගීත", "බුලත්", "ඉටිපන්දම්", "නිවාස", "සර්ව ආගමික", "ගල්බැම්ම"
]

def days_diff(d1_str, d2_str):
    try:
        dt1 = datetime.strptime(d1_str[:10], "%Y-%m-%d")
        dt2 = datetime.strptime(d2_str[:10], "%Y-%m-%d")
        return abs((dt1 - dt2).days)
    except:
        return 999

def are_duplicates(item, m):
    if norm_text(item['gn']) != norm_text(m['gn']):
        return False, None
    
    item_photos = set(item['photo_ids'])
    m_photos = set(m['photo_ids'])
    
    # 1. Shared Google Drive Photo ID
    if item_photos and m_photos and len(item_photos.intersection(m_photos)) > 0:
        return True, "Shared Google Drive Photo ID"
    
    # 2. Both aligned with the SAME nw.docx title
    if item.get('docx_title') and m.get('docx_title') and norm_text(item['docx_title']) == norm_text(m['docx_title']):
        return True, f"Aligned with same nw.docx entry: {item['docx_title']}"
    
    d1 = item['date']
    d2 = m['date']
    t1 = norm_text((item.get('docx_title') or '') + " " + (item.get('desc') or ''))
    t2 = norm_text((m.get('docx_title') or '') + " " + (m.get('desc') or ''))
    
    diff_days = days_diff(d1, d2)
    same_month = (d1[:7] == d2[:7])
    
    shared_kws = [k for k in DISTINCT_KEYWORDS if (k in t1 and k in t2)]
    sim = SequenceMatcher(None, t1, t2).ratio()
    
    # 3. High text similarity
    if sim > 0.65:
        return True, f"High text similarity ({sim:.2f})"
        
    # 4. Exact Same Date
    if d1 == d2:
        if sim > 0.20 or len(shared_kws) > 0 or t1 in t2 or t2 in t1:
            return True, f"Exact same date ({d1}) + shared theme {shared_kws or f'sim={sim:.2f}'}"
            
    # 5. Very close date (within 3 days)
    if diff_days <= 3:
        if len(shared_kws) > 0 or sim > 0.35:
            return True, f"Close dates ({d1} vs {d2}, {diff_days}d) + shared keyword {shared_kws}"
            
    # 6. Same month with strong shared distinct event keyword
    HIGH_SPECIFICITY_KWS = ["දන්සල", "දන්සැල", "ක්‍රිකට්", "අවුරුදු", "බක්මහ", "පහන්", "ලේ දන්දීම", "බිම්මල්", "බුලත්", "ඉටිපන්දම්", "කවි මඩුව", "පොළ"]
    shared_high = [k for k in HIGH_SPECIFICITY_KWS if (k in t1 and k in t2)]
    if same_month and len(shared_high) > 0:
        return True, f"Same month ({d1[:7]}) + specific annual/community event '{shared_high[0]}'"
        
    # 7. Check month/day swap
    m1 = re.match(r'^2026-(\d{2})-(\d{2})$', d1)
    m2 = re.match(r'^2026-(\d{2})-(\d{2})$', d2)
    if m1 and m2:
        if m1.group(1) == m2.group(2) and m1.group(2) == m2.group(1) and len(shared_kws) > 0:
            return True, f"Date month/day transposed ({d1} vs {d2}) + shared keyword {shared_kws}"

    return False, None

master_pool = []
merged_records_log = []

for item in raw_records:
    match = None
    match_reason = ""
    for m in master_pool:
        is_dup, reason = are_duplicates(item, m)
        if is_dup:
            match = m
            match_reason = reason
            break
            
    if match:
        merged_records_log.append({
            'gn': item['gn'],
            'reason': match_reason,
            'primary_title': match.get('docx_title') or match['desc'][:60],
            'primary_date': match['date'],
            'primary_source': match['sources'][0],
            'duplicate_title': item.get('docx_title') or item['desc'][:60],
            'duplicate_date': item['date'],
            'duplicate_source': f"{item['sheet']} R{item['row']}"
        })
        for pid in item['photo_ids']:
            if pid not in match['photo_ids']:
                match['photo_ids'].append(pid)
        if len(item['desc']) > len(match['desc']):
            match['desc'] = item['desc']
        if item.get('docx_title') and not match.get('docx_title'):
            match['docx_title'] = item['docx_title']
            match['date'] = item['date']
        if item['sheet'] not in match['sources']:
            match['sources'].append(item['sheet'])
    else:
        master_pool.append({
            'gn': item['gn'],
            'date': item['date'],
            'raw_date': item['raw_date'],
            'docx_title': item.get('docx_title'),
            'date_src': item.get('date_src'),
            'desc': item['desc'],
            'photo_ids': list(item['photo_ids']),
            'sources': [item['sheet']],
            'first_seen': f"{item['sheet']} R{item['row']} B{item['block']}"
        })

print(f"\n==================== DEDUPLICATION RESULTS ====================")
print(f"Total raw blocks: {len(raw_records)}")
print(f"Duplicates merged: {len(merged_records_log)}")
print(f"Clean canonical activities remaining: {len(master_pool)}")

etamba_res = [m for m in master_pool if 'ඇටඹගස්' in m['gn']]
print(f"\nEtambagasmulla remaining activities: {len(etamba_res)}")
for i, e in enumerate(etamba_res):
    print(f"  {i+1}. {e['date']} | {e.get('docx_title') or e['desc'][:40]} | {len(e['photo_ids'])} photos | sources: {e['sources']}")
