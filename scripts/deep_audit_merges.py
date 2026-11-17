import json

with open('raw_drive_data/canonical_v9.json', 'r', encoding='utf-8') as f:
    v9 = json.load(f)

# Let's inspect the raw records that were merged
# We can load the 5 sheets or inspect the full text
import openpyxl, os, re

sheet_files = [
    ('Main Cumulative', 'raw_drive_data/new_imports/sheet_main_responses.xlsx'),
    ('June Monthly', 'raw_drive_data/new_imports/sheet_officers_monthly_responses.xlsx'),
    ('July Monthly', 'raw_drive_data/new_imports/sheet_monthly_responses.xlsx'),
    ('August Monthly', 'raw_drive_data/new_imports/sheet_august_copy.xlsx'),
    ('September Monthly', 'raw_drive_data/new_imports/sheet_august_copy_copy.xlsx'),
]

raw_map = {}
for sheet_title, fpath in sheet_files:
    if not os.path.exists(fpath): continue
    wb = openpyxl.load_workbook(fpath, data_only=True)
    ws = wb['Form responses 1']
    rows = list(ws.iter_rows(values_only=True))
    for r_idx, row in enumerate(rows[1:], 2):
        if not row or not any(row): continue
        gn_raw = str(row[2] or "").strip()
        officer = str(row[1] or "").strip()
        for s_idx in range(8):
            d_col = 4 + s_idx * 4
            desc_col = 5 + s_idx * 4
            p_col = 6 + s_idx * 4
            raw_d = str(row[d_col] or "").strip() if d_col < len(row) else ""
            raw_desc = str(row[desc_col] or "").strip() if desc_col < len(row) else ""
            raw_p = str(row[p_col] or "").strip() if p_col < len(row) else ""
            p_ids = list(dict.fromkeys(re.findall(r'[a-zA-Z0-9_-]{25,}', str(raw_p))))
            key = f"[{sheet_title} R{r_idx} S{s_idx+1}]"
            raw_map[key] = {
                'sheet': sheet_title,
                'row': r_idx,
                'slot': s_idx + 1,
                'gn_raw': gn_raw,
                'officer': officer,
                'date': raw_d,
                'desc': raw_desc,
                'photos': p_ids
            }

merges = v9.get('mergesLog', [])
print(f"Total merges: {len(merges)}")

distinct_candidates = []
true_dups = []

for idx, m in enumerate(merges, 1):
    k_key = m['kept'].split(']')[0] + ']'
    d_key = m['duplicate'].split(']')[0] + ']'
    k_obj = raw_map.get(k_key, {})
    d_obj = raw_map.get(d_key, {})
    
    k_desc = k_obj.get('desc', '')
    d_desc = d_obj.get('desc', '')
    k_photos = set(k_obj.get('photos', []))
    d_photos = set(d_obj.get('photos', []))
    shared_p = k_photos.intersection(d_photos)
    
    item_info = {
        'idx': idx,
        'gn': m['gn'],
        'reason': m['reason'],
        'k_key': k_key,
        'd_key': d_key,
        'k_date': k_obj.get('date'),
        'd_date': d_obj.get('date'),
        'k_desc': k_desc,
        'd_desc': d_desc,
        'k_photos': len(k_photos),
        'd_photos': len(d_photos),
        'shared_photos': len(shared_p)
    }
    
    # Check if there is physical proof of same event: shared photos
    if len(shared_p) > 0:
        true_dups.append((item_info, f"Shared {len(shared_p)} photos"))
        continue
        
    # Check text similarity and keywords
    t1 = k_desc.strip()
    t2 = d_desc.strip()
    
    distinct_candidates.append(item_info)

print(f"Definite true duplicates via shared photos: {len(true_dups)}")
print(f"Remaining merges to review text/content: {len(distinct_candidates)}")

with open('raw_drive_data/merges_without_shared_photos.txt', 'w', encoding='utf-8') as f:
    for item in distinct_candidates:
        f.write(f"#{item['idx']:02d} [{item['gn']}] Date: {item['k_date']} vs {item['d_date']}\n")
        f.write(f"   Reason: {item['reason']}\n")
        f.write(f"   KEPT ({item['k_key']}, {item['k_photos']} photos): {item['k_desc']}\n")
        f.write(f"   DUP  ({item['d_key']}, {item['d_photos']} photos): {item['d_desc']}\n\n")

print("Written to raw_drive_data/merges_without_shared_photos.txt")
