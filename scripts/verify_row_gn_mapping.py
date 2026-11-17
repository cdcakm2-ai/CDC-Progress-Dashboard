import openpyxl, os, re, json
from difflib import SequenceMatcher

with open('raw_drive_data/canonical_v4.json', encoding='utf-8') as f:
    v4 = json.load(f)

official_gn_list = [g['nameSi'] for g in v4['gnDivisions']]

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

print("=== VERIFYING GN MAPPING FOR ALL ROWS ACROSS ALL SHEETS ===")
mismatches = []
for title, fpath in sheet_files:
    wb = openpyxl.load_workbook(fpath, data_only=True)
    ws = wb['Form responses 1']
    rows = list(ws.iter_rows(values_only=True))
    for r_idx, r in enumerate(rows[1:], 2):
        if not r or not any(r): continue
        raw_gn = str(r[2] or "").strip()
        officer = str(r[1] or "").strip()
        std = standardize_gn(raw_gn)
        
        # Check if std is in official_gn_list
        if std not in official_gn_list:
            mismatches.append((title, r_idx, officer, raw_gn, std, "NOT IN OFFICIAL LIST"))
            
        # Check if raw_gn number matches std number
        m_raw = re.match(r'^([0-9]+)', raw_gn)
        m_std = re.match(r'^([0-9]+)', std)
        if m_raw and m_std and m_raw.group(1) != m_std.group(1):
            mismatches.append((title, r_idx, officer, raw_gn, std, "NUMBER MISMATCH"))

print(f"Total rows inspected across 5 sheets: {221}")
print(f"Total mismatches or issues: {len(mismatches)}")
for m in mismatches:
    print(m)
