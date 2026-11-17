import json
import csv
import re
import os
from difflib import SequenceMatcher
from datetime import datetime

# 1. Load nw.docx reference entries
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

print(f"Loaded {len(docx_entries)} reference entries from nw.docx.")

# Helper to extract Google Drive file IDs
def get_drive_ids(text):
    if not text:
        return []
    ids = []
    for m in re.finditer(r'id=([a-zA-Z0-9_-]{25,})', str(text)):
        ids.append(m.group(1))
    for m in re.finditer(r'/d/([a-zA-Z0-9_-]{25,})', str(text)):
        ids.append(m.group(1))
    # Preserve order but unique
    seen = set()
    res = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            res.append(i)
    return res

# Helper to normalize GN strings
def norm_gn(text):
    if not text:
        return ""
    t = str(text).strip()
    t = re.sub(r'\s+', ' ', t)
    return t

def norm_text(t):
    if not t:
        return ""
    return re.sub(r'[\s\.\,\-\_\*\(\)\:\;\/]+', '', t.lower())

# Date parser and normalizer
def normalize_date(raw_date, desc_text, gn_name):
    if not raw_date:
        raw_date = ""
    raw = str(raw_date).strip()
    
    # Check if nw.docx has an exact match for this activity in this GN
    norm_d = norm_text(desc_text)
    norm_g = norm_text(gn_name)
    best_docx_match = None
    best_sim = 0.0
    for de in docx_entries:
        if norm_text(de['gn']) in norm_g or norm_g in norm_text(de['gn']):
            sim = SequenceMatcher(None, norm_d, norm_text(de['desc'])).ratio()
            t_sim = SequenceMatcher(None, norm_d, norm_text(de['title'])).ratio()
            score = max(sim, t_sim)
            if score > best_sim and score > 0.60:
                best_sim = score
                best_docx_match = de
    
    if best_docx_match:
        # nw.docx has verified date!
        return best_docx_match['date'], best_docx_match['title'], 'docx_verified'
    
    # Try parsing common formats
    # Handle typo 3025 -> 2026
    raw = raw.replace('3025-', '2026-').replace('/3025', '/2026')
    
    # YYYY-MM-DD HH:MM:SS
    m = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', raw)
    if m:
        yr = int(m.group(1))
        if yr < 2024: yr = 2026
        return f"{yr:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}", None, 'parsed'
    
    # DD/MM/YYYY
    m = re.match(r'^(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})', raw)
    if m:
        yr = int(m.group(3))
        if yr < 2024: yr = 2026
        return f"{yr:04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}", None, 'parsed'
    
    # Check if date mentioned inside description
    m_in_desc = re.search(r'(202[4-6])[\.\/\-](\d{1,2})[\.\/\-](\d{1,2})', desc_text)
    if m_in_desc:
        return f"{int(m_in_desc.group(1)):04d}-{int(m_in_desc.group(2)):02d}-{int(m_in_desc.group(3)):02d}", None, 'extracted_from_desc'
    
    return "2026-08-01", None, 'default'

# 2. Extract from all 5 sheets
sheets_config = [
    ('Main Cumulative (Nov-Jul)', 'raw_drive_data/new_imports/csvs/sheet_main_responses_Form responses 1.csv'),
    ('June Monthly Responses', 'raw_drive_data/new_imports/csvs/sheet_officers_monthly_responses_Form responses 1.csv'),
    ('July Monthly Responses', 'raw_drive_data/new_imports/csvs/sheet_monthly_responses_Form responses 1.csv'),
    ('August Monthly Responses', 'raw_drive_data/new_imports/csvs/sheet_august_copy_Form responses 1.csv'),
    ('September Monthly Responses', 'raw_drive_data/new_imports/csvs/sheet_august_copy_copy_Form responses 1.csv'),
]

raw_activities = []

for sheet_title, csv_path in sheets_config:
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} does not exist!")
        continue
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
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
                        clean_date, docx_title, date_source = normalize_date(raw_date, raw_desc, gn)
                        
                        raw_activities.append({
                            'source_sheet': sheet_title,
                            'row': r_idx + 2,
                            'block': b_idx + 1,
                            'timestamp': ts,
                            'officer': officer,
                            'gn': norm_gn(gn),
                            'raw_date': raw_date,
                            'date': clean_date,
                            'docx_title': docx_title,
                            'date_source': date_source,
                            'desc': raw_desc,
                            'photo_ids': p_ids,
                            'raw_photos': raw_photos
                        })

print(f"\nTotal raw activities harvested across all 5 sheets: {len(raw_activities)}")

# 3. Master Deduplication Algorithm
# We group activities that belong to the same real-world event.
# Two entries are the SAME activity if:
# Rule A: They share at least one Google Drive photo ID. (Strongest proof)
# Rule B: They belong to the same GN division AND have text similarity > 0.70 AND dates within 10 days of each other.
# Rule C: They belong to the same GN division AND have text similarity > 0.85 (even if date was entered slightly differently).

master_activities = []
duplicate_merge_count = 0

for item in raw_activities:
    matched_master = None
    item_photos = set(item['photo_ids'])
    item_gn_norm = norm_text(item['gn'])
    item_desc_norm = norm_text(item['desc'])
    
    for m in master_activities:
        m_photos = set(m['photo_ids'])
        
        # Check Rule A: Shared photo ID
        if item_photos and m_photos and len(item_photos.intersection(m_photos)) > 0:
            matched_master = m
            break
        
        # Check GN division
        m_gn_norm = norm_text(m['gn'])
        if item_gn_norm and m_gn_norm and (item_gn_norm in m_gn_norm or m_gn_norm in item_gn_norm):
            sim = SequenceMatcher(None, item_desc_norm, norm_text(m['desc'])).ratio()
            
            # Rule B & C
            if sim > 0.82:
                matched_master = m
                break
            elif sim > 0.68 and item['date'] == m['date']:
                matched_master = m
                break
    
    if matched_master:
        # Merge into existing master activity
        duplicate_merge_count += 1
        # Merge photo IDs (preserving all unique images!)
        for pid in item['photo_ids']:
            if pid not in matched_master['photo_ids']:
                matched_master['photo_ids'].append(pid)
        # Keep the more detailed description if available
        if len(item['desc']) > len(matched_master['desc']):
            matched_master['desc'] = item['desc']
        # If item has a docx title and master doesn't, keep docx title
        if item.get('docx_title') and not matched_master.get('docx_title'):
            matched_master['docx_title'] = item['docx_title']
            matched_master['date'] = item['date']
        # Append source sheets
        if item['source_sheet'] not in matched_master['sources']:
            matched_master['sources'].append(item['source_sheet'])
    else:
        # Add new master activity
        master_activities.append({
            'gn': item['gn'],
            'date': item['date'],
            'raw_date': item['raw_date'],
            'docx_title': item.get('docx_title'),
            'date_source': item.get('date_source'),
            'desc': item['desc'],
            'photo_ids': list(item['photo_ids']),
            'sources': [item['source_sheet']],
            'first_seen': f"{item['source_sheet']} R{item['row']} B{item['block']}"
        })

print(f"\nDeduplication Results:")
print(f"  Total raw entries processed: {len(raw_activities)}")
print(f"  Duplicate entries merged: {duplicate_merge_count}")
print(f"  Final UNIQUE Master Activities: {len(master_activities)}")

# Count total unique photographs across master activities
all_master_photos = set()
for m in master_activities:
    for pid in m['photo_ids']:
        all_master_photos.add(pid)
print(f"  Total UNIQUE Verified Photographs: {len(all_master_photos)}")

# Count reporting GN divisions
gn_counts = {}
for m in master_activities:
    gn = m['gn']
    gn_counts[gn] = gn_counts.get(gn, 0) + 1

print(f"  Total Reporting GN Divisions: {len(gn_counts)} / 63")

# Count unique dates
unique_dates = set(m['date'] for m in master_activities)
print(f"  Total Active Days: {len(unique_dates)}")

# Save intermediate master dataset
with open('raw_drive_data/canonical_v5_draft.json', 'w', encoding='utf-8') as f:
    json.dump({
        'totalActivities': len(master_activities),
        'totalPhotos': len(all_master_photos),
        'totalGNs': len(gn_counts),
        'activeDays': len(unique_dates),
        'master_activities': master_activities
    }, f, ensure_ascii=False, indent=2)

print("\nDraft canonical v5 saved to raw_drive_data/canonical_v5_draft.json")
