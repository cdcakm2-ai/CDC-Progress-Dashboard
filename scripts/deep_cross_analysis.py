import csv
import re
import os

sources = [
    ('sheet_main_responses_Form responses 1.csv', 'Main_Nov_Jul'),
    ('sheet_august_copy_copy_Form responses 1.csv', 'Aug_Sep_Original'),
    ('sheet_august_copy_Form responses 1.csv', 'Aug_Sep_Updated'),
    ('sheet_monthly_responses_Form responses 1.csv', 'July_Responses'),
    ('sheet_officers_monthly_responses_Form responses 1.csv', 'June_Responses'),
]

def clean_drive_links(text):
    if not text:
        return []
    ids = set()
    for m in re.finditer(r'id=([a-zA-Z0-9_-]{25,})', text):
        ids.add(m.group(1))
    for m in re.finditer(r'/d/([a-zA-Z0-9_-]{25,})', text):
        ids.add(m.group(1))
    return sorted(list(ids))

all_extracted = []

for filename, tag in sources:
    path = os.path.join('raw_drive_data/new_imports/csvs', filename)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        print(f"\n--- Processing {tag} ({filename}) ---")
        for r_idx, row in enumerate(reader):
            if not row or not any(row):
                continue
            timestamp = row[0].strip() if len(row) > 0 else ""
            officer = row[1].strip() if len(row) > 1 else ""
            gn = row[2].strip() if len(row) > 2 else ""
            
            # The activity blocks:
            # Let's inspect column indices where dates and descriptions occur
            # Typically:
            # Block 1: col 4 (date), col 5 (desc), col 6 (photos)
            # Block 2: col 8 (date), col 9 (desc), col 10 (photos)
            # Block 3: col 12 (date), col 13 (desc), col 14 (photos)
            # Block 4: col 16 (date), col 17 (desc), col 18 (photos)
            # Block 5: col 20 (date), col 21 (desc), col 22 (photos)
            for b_idx in range(6):
                d_col = 4 + b_idx * 4
                desc_col = 5 + b_idx * 4
                photo_col = 6 + b_idx * 4
                
                if d_col < len(row) and desc_col < len(row):
                    raw_date = row[d_col].strip()
                    raw_desc = row[desc_col].strip()
                    raw_photos = row[photo_col].strip() if photo_col < len(row) else ""
                    
                    if raw_desc or raw_date or raw_photos:
                        photo_ids = clean_drive_links(raw_photos)
                        all_extracted.append({
                            'source': tag,
                            'row': r_idx + 2,
                            'block': b_idx + 1,
                            'timestamp': timestamp,
                            'gn': gn,
                            'date': raw_date,
                            'desc': raw_desc,
                            'photo_ids': photo_ids,
                            'photo_count': len(photo_ids)
                        })

print(f"\nTotal activity blocks extracted across all 5 sheets: {len(all_extracted)}")
source_counts = {}
for a in all_extracted:
    source_counts[a['source']] = source_counts.get(a['source'], 0) + 1
for s, c in source_counts.items():
    print(f"  {s}: {c} activity blocks")
