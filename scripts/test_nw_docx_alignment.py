import json
import re
from difflib import SequenceMatcher

with open('raw_drive_data/canonical_v5_draft.json', 'r', encoding='utf-8') as f:
    v5 = json.load(f)

acts = v5['master_activities']

with open('raw_drive_data/new_imports/nw_docx_extracted.txt', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

docx_items = []
cur_gn = ""
for line in lines:
    m_gn = re.match(r'^\d+\.\s*([0-9]+[^\n]+?)\s*වසම\s*$', line)
    if m_gn:
        cur_gn = m_gn.group(1).strip()
        continue
    m_act = re.match(r'^([^-]+?)\s*-\s*(\d{4}-\d{2}-\d{2})\s*(.*)$', line)
    if m_act:
        docx_items.append({
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
            docx_items.append({
                'gn': cur_gn,
                'title': parts[0].replace('-', '').strip(),
                'date': m_date.group(1),
                'desc': parts[1].strip() if len(parts) > 1 else "",
                'raw': line
            })

print(f"Total docx items: {len(docx_items)}")

# Match acts to docx
matched = 0
date_adjustments = []

for act in acts:
    act_desc = act['desc']
    act_gn = act['gn']
    
    best_item = None
    best_score = 0.0
    for doc in docx_items:
        # Check GN number prefix match (e.g. 109, 113, 133)
        m1 = re.match(r'^(\d+)', act_gn)
        m2 = re.match(r'^(\d+)', doc['gn'])
        if m1 and m2 and m1.group(1) == m2.group(1):
            sim = SequenceMatcher(None, act_desc, doc['desc']).ratio()
            t_sim = SequenceMatcher(None, act_desc, doc['title']).ratio()
            score = max(sim, t_sim)
            if score > best_score and score > 0.55:
                best_score = score
                best_item = doc
    
    if best_item:
        matched += 1
        if act['date'] != best_item['date']:
            date_adjustments.append((act['gn'], act['desc'][:40], act['date'], best_item['date'], best_item['title']))

print(f"Activities matched with docx: {matched}")
print(f"Dates adjusted based on docx reference: {len(date_adjustments)}")
print("\nSample Date Adjustments:")
for gn, d, old_d, new_d, t in date_adjustments[:15]:
    print(f"  [{gn}] '{t}' | Old: {old_d} -> Adjusted to docx: {new_d} ({d})")
