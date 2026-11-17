import json
import re
import os
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict
import openpyxl

with open('raw_drive_data/canonical_v4.json', encoding='utf-8') as f:
    v4 = json.load(f)

official_gn_list = [g['nameSi'] for g in v4['gnDivisions']]

def norm_text(text):
    if not text: return ""
    t = str(text).lower()
    return re.sub(r'[\s\.\,\-\_\/\(\)\[\]\:\;]+', ' ', t).strip()

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
    for r_idx, row in enumerate(rows[1:]):
        if not row or not any(row): continue
        gn_raw = str(row[2] or "").strip()
        if not gn_raw: continue
        gn = standardize_gn(gn_raw)
        
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
                    'row': r_idx + 2,
                    'slot': s_idx + 1,
                    'gn': gn,
                    'date': clean_date,
                    'desc': raw_desc,
                    'photos': p_ids
                })

print(f"Total raw slots: {len(raw_records)}")

# Now let's see how many items in the same GN were merged in V7
import sys
sys.path.append('scripts')
from generate_canonical_v7 import are_duplicates

records_by_gn = defaultdict(list)
for r in raw_records:
    records_by_gn[r['gn']].append(r)

suspect_merges = []
for gn_name, items in records_by_gn.items():
    gn_master = []
    for item in items:
        matched = None
        reason = None
        for m in gn_master:
            is_dup, r = are_duplicates(item, m)
            if is_dup:
                matched = m
                reason = r
                break
        if matched:
            # Check if this merge looks suspicious (e.g. from the same sheet & row! or different text)
            same_sheet_and_row = (item['sheet'] == matched['sheet'] and item['row'] == matched['row'])
            t1 = item['desc']
            t2 = matched['desc']
            sim = SequenceMatcher(None, norm_text(t1), norm_text(t2)).ratio()
            
            # Check shared photos
            shared_p = set(item['photos']).intersection(set(matched['photos']))
            has_photo_match = len(shared_p) > 0
            
            if same_sheet_and_row or (sim < 0.6 and not has_photo_match):
                suspect_merges.append({
                    'gn': gn_name,
                    'item1': f"[{item['sheet']} R{item['row']} S{item['slot']}] {item['date']} | {t1[:45]}",
                    'item2': f"[{matched['sheet']} R{matched['row']} S{matched['slot']}] {matched['date']} | {t2[:45]}",
                    'sim': sim,
                    'reason': reason,
                    'same_row': same_sheet_and_row,
                    'shared_photos': len(shared_p)
                })
        else:
            gn_master.append(item)

print(f"\nTotal suspect merges found: {len(suspect_merges)}")
for idx, s in enumerate(suspect_merges[:20], 1):
    print(f"\n{idx}. GN: {s['gn']} (Sim: {s['sim']:.2f}, Same Row: {s['same_row']}, Shared Photos: {s['shared_photos']})")
    print(f"   A: {s['item1']}")
    print(f"   B: {s['item2']}")
    print(f"   Reason: {s['reason']}")
