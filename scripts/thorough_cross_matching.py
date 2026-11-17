import json
import csv
import re
import os
from difflib import SequenceMatcher

# 1. Load canonical v4
with open('raw_drive_data/canonical_v4.json', 'r', encoding='utf-8') as f:
    v4 = json.load(f)
existing_activities = v4['activities']
print(f"Loaded existing canonical activities: {len(existing_activities)}")

# Map existing activities by their photo IDs
existing_by_photo_id = {}
for act in existing_activities:
    for po in act.get('photoObjects', []):
        pid = po.get('id')
        if pid:
            existing_by_photo_id[pid] = act

# 2. Load nw.docx entries
docx_entries = []
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
        docx_entries.append({
            'gn': cur_gn,
            'title': m_act.group(1).strip(),
            'date': m_act.group(2).strip(),
            'desc': m_act.group(3).strip(),
            'raw': line
        })
    else:
        m_date = re.search(r'(\d{4}-\d{2}-\d{2})', line)
        if m_date:
            parts = line.split(m_date.group(1))
            docx_entries.append({
                'gn': cur_gn,
                'title': parts[0].replace('-', '').strip(),
                'date': m_date.group(1),
                'desc': parts[1].strip() if len(parts) > 1 else "",
                'raw': line
            })

print(f"Loaded {len(docx_entries)} docx entries across {len(set(e['gn'] for e in docx_entries))} GN divisions.")

# Helper to extract drive IDs from raw text
def get_drive_ids(text):
    if not text:
        return []
    ids = []
    for m in re.finditer(r'id=([a-zA-Z0-9_-]{25,})', str(text)):
        ids.append(m.group(1))
    for m in re.finditer(r'/d/([a-zA-Z0-9_-]{25,})', str(text)):
        ids.append(m.group(1))
    return sorted(list(set(ids)))

def norm_text(t):
    if not t:
        return ""
    t = re.sub(r'[\s\.\,\-\_\*\(\)\:\;\/]+', '', t.lower())
    return t

# 3. Read ALL newly added sheets:
# - June Form (sheet_officers_monthly_responses_Form responses 1.csv)
# - July Form (sheet_monthly_responses_Form responses 1.csv)
# - August Updated Form (sheet_august_copy_Form responses 1.csv)
# - Also check if any unique entries in 'Sheet1' or 'All_Programs' or 'Calc_Data'

new_sheets_to_process = [
    ('June Sheet (Responses)', 'raw_drive_data/new_imports/csvs/sheet_officers_monthly_responses_Form responses 1.csv'),
    ('July Sheet (Responses)', 'raw_drive_data/new_imports/csvs/sheet_monthly_responses_Form responses 1.csv'),
    ('August Updated Sheet (Responses)', 'raw_drive_data/new_imports/csvs/sheet_august_copy_Form responses 1.csv'),
]

all_new_blocks = []

for sheet_label, path in new_sheets_to_process:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for r_idx, row in enumerate(reader):
            if not row or not any(row):
                continue
            ts = row[0].strip() if len(row) > 0 else ""
            officer = row[1].strip() if len(row) > 1 else ""
            gn = row[2].strip() if len(row) > 2 else ""
            
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
                        all_new_blocks.append({
                            'sheet': sheet_label,
                            'row': r_idx + 2,
                            'block': b_idx + 1,
                            'timestamp': ts,
                            'officer': officer,
                            'gn': gn,
                            'date': raw_date,
                            'desc': raw_desc,
                            'photo_ids': p_ids,
                            'raw_photos': raw_photos
                        })

print(f"Total blocks in new sheets: {len(all_new_blocks)}")

# Now test duplicate detection against existing canonical activities
duplicate_blocks = []
genuine_new_blocks = []

for b in all_new_blocks:
    # 1. Check if ANY photo ID exists in canonical dataset
    matched_by_photo = None
    for pid in b['photo_ids']:
        if pid in existing_by_photo_id:
            matched_by_photo = existing_by_photo_id[pid]
            break
    
    if matched_by_photo:
        duplicate_blocks.append({
            'new': b,
            'match_type': 'EXACT_PHOTO',
            'matched': matched_by_photo
        })
        continue
    
    # 2. Check if text + GN is identical or near-identical
    matched_by_text = None
    b_gn_norm = norm_text(b['gn'])
    b_desc_norm = norm_text(b['desc'])
    
    for ex in existing_activities:
        ex_gn_norm = norm_text(ex.get('gnNameSi', ''))
        ex_desc_norm = norm_text(ex.get('description', ''))
        
        # If GN has same number/root and descriptions are > 80% similar
        if b_gn_norm and ex_gn_norm and (b_gn_norm in ex_gn_norm or ex_gn_norm in b_gn_norm):
            sim = SequenceMatcher(None, b_desc_norm, ex_desc_norm).ratio()
            if sim > 0.80:
                matched_by_text = (ex, sim)
                break
    
    if matched_by_text:
        duplicate_blocks.append({
            'new': b,
            'match_type': f'HIGH_TEXT_SIMILARITY ({matched_by_text[1]:.2f})',
            'matched': matched_by_text[0]
        })
        continue
    
    genuine_new_blocks.append(b)

print(f"\nResults:")
print(f"  Duplicate blocks identified: {len(duplicate_blocks)}")
print(f"  Genuine NEW blocks to add: {len(genuine_new_blocks)}")

# Let's inspect the genuine new blocks!
print("\n--- Summary of Genuine NEW Blocks by Sheet ---")
new_by_sheet = {}
for g in genuine_new_blocks:
    new_by_sheet[g['sheet']] = new_by_sheet.get(g['sheet'], 0) + 1
for s, c in new_by_sheet.items():
    print(f"  {s}: {c} new activities")

print("\n--- Sample of Genuine NEW Blocks ---")
for i, g in enumerate(genuine_new_blocks[:20]):
    print(f"[{i+1}] Sheet: {g['sheet']} (R{g['row']} B{g['block']}) | GN: {g['gn']} | Date: {g['date']} | Photos: {len(g['photo_ids'])}")
    print(f"     Desc: {g['desc'][:100]}")
