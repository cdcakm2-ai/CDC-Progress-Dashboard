import openpyxl, glob, re, json
from difflib import SequenceMatcher

with open('raw_drive_data/canonical_v4.json', encoding='utf-8') as f:
    v4 = json.load(f)
official_gn_list = [g['nameSi'] for g in v4['gnDivisions']]

def norm_text(text):
    if not text: return ''
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

raw_gns = set()
for fpath in sorted(glob.glob('raw_drive_data/new_imports/*.xlsx')):
    wb = openpyxl.load_workbook(fpath, data_only=True)
    ws = wb['Form responses 1']
    for row in ws.iter_rows(values_only=True):
        if row and len(row) > 2 and row[2]:
            val = str(row[2]).strip()
            if val != 'ග්‍රාම නිලධාරී වසම' and val != 'None':
                raw_gns.add(val)

print(f"Total unique raw GN strings in all sheets: {len(raw_gns)}")
unmatched = []
mapped_diff = []
for g in sorted(raw_gns):
    std = standardize_gn(g)
    if std not in official_gn_list:
        unmatched.append(g)
    else:
        if std != g:
            mapped_diff.append((g, std))

print(f"Unmatched GNs ({len(unmatched)}): {unmatched}")
print(f"\nMapped with differences ({len(mapped_diff)}):")
for r, m in mapped_diff:
    print(f"  '{r}'  ===>  '{m}'")
