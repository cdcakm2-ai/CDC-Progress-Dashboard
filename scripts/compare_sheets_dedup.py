import json
import csv
import re
import os
from difflib import SequenceMatcher

# 1. Load canonical v4 (290 activities)
with open('raw_drive_data/canonical_v4.json', 'r', encoding='utf-8') as f:
    v4 = json.load(f)
existing_activities = v4['activities']
print(f"Loaded existing canonical activities: {len(existing_activities)}")

# 2. Helper to clean Drive IDs
def extract_drive_ids(text):
    if not text:
        return set()
    ids = set()
    for m in re.finditer(r'id=([a-zA-Z0-9_-]{25,})', str(text)):
        ids.add(m.group(1))
    for m in re.finditer(r'/d/([a-zA-Z0-9_-]{25,})', str(text)):
        ids.add(m.group(1))
    return ids

# Helper to normalize GN division string
def norm_gn(text):
    if not text:
        return ""
    t = str(text).strip()
    t = re.sub(r'\s+', ' ', t)
    # Extract number prefix if any, e.g. "109/ ජී" -> "109"
    return t

# Helper for text similarity
def text_sim(a, b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.strip(), b.strip()).ratio()

# 3. Extract all activities from the new sheets
def extract_sheet_rows(csv_path, source_label):
    if not os.path.exists(csv_path):
        return []
    records = []
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for r_idx, row in enumerate(reader):
            if not row or not any(row):
                continue
            timestamp = row[0].strip() if len(row) > 0 else ""
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
                        p_ids = extract_drive_ids(raw_photos)
                        records.append({
                            'source': source_label,
                            'row': r_idx + 2,
                            'block': b_idx + 1,
                            'timestamp': timestamp,
                            'officer': officer,
                            'gn': gn,
                            'date': raw_date,
                            'desc': raw_desc,
                            'photo_ids': p_ids,
                            'raw_photos': raw_photos
                        })
    return records

june_records = extract_sheet_rows('raw_drive_data/new_imports/csvs/sheet_officers_monthly_responses_Form responses 1.csv', 'June_Form')
july_records = extract_sheet_rows('raw_drive_data/new_imports/csvs/sheet_monthly_responses_Form responses 1.csv', 'July_Form')
aug_updated_records = extract_sheet_rows('raw_drive_data/new_imports/csvs/sheet_august_copy_Form responses 1.csv', 'Aug_Updated_Form')

print(f"\nExtracted from new sheets:")
print(f"  June Form: {len(june_records)} records")
print(f"  July Form: {len(july_records)} records")
print(f"  August Updated Form: {len(aug_updated_records)} records")

# 4. Check matches with existing canonical activities
all_new_records = june_records + july_records + aug_updated_records

matched_count = 0
unmatched_new = []

for r in all_new_records:
    # Match criteria:
    # 1. Shared photo IDs (very strong proof of same activity)
    # 2. Or same GN + high text similarity (> 0.7) + close date
    is_match = False
    match_reason = ""
    matched_existing = None
    
    r_photos = r['photo_ids']
    
    for ex in existing_activities:
        ex_photos = extract_drive_ids(" ".join(ex.get('photos', [])))
        # Check photo overlap
        if r_photos and ex_photos and len(r_photos.intersection(ex_photos)) > 0:
            is_match = True
            match_reason = f"Shared photo ID ({len(r_photos.intersection(ex_photos))} shared)"
            matched_existing = ex
            break
        
        # Check GN and description similarity
        if norm_gn(r['gn']) == norm_gn(ex.get('gnDivision', '')):
            sim = text_sim(r['desc'], ex.get('description', ''))
            title_sim = text_sim(r['desc'], ex.get('title', ''))
            if sim > 0.65 or title_sim > 0.65:
                is_match = True
                match_reason = f"Same GN and high text similarity ({max(sim, title_sim):.2f})"
                matched_existing = ex
                break
    
    if is_match:
        matched_count += 1
    else:
        unmatched_new.append(r)

print(f"\nCross-Analysis Summary:")
print(f"  Total records in new sheets: {len(all_new_records)}")
print(f"  Already in previous sheets (duplicates): {matched_count}")
print(f"  Brand NEW records not in previous sheets: {len(unmatched_new)}")

print(f"\n--- Sample of Brand NEW Records Found ({len(unmatched_new)}) ---")
for i, nr in enumerate(unmatched_new[:25]):
    print(f"[{i+1}] Source: {nr['source']} (Row {nr['row']}, Block {nr['block']}) | GN: {nr['gn']} | Date: {nr['date']} | Photos: {len(nr['photo_ids'])}")
    print(f"     Desc: {nr['desc'][:100]}")
