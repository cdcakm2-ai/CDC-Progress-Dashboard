import openpyxl, os, re

sheet_files = [
    ('Main Cumulative', 'raw_drive_data/new_imports/sheet_main_responses.xlsx'),
    ('June Monthly', 'raw_drive_data/new_imports/sheet_officers_monthly_responses.xlsx'),
    ('July Monthly', 'raw_drive_data/new_imports/sheet_monthly_responses.xlsx'),
    ('August Monthly', 'raw_drive_data/new_imports/sheet_august_copy.xlsx'),
    ('September Monthly', 'raw_drive_data/new_imports/sheet_august_copy_copy.xlsx'),
]

singlish_slots = []
for sheet_title, fpath in sheet_files:
    if not os.path.exists(fpath): continue
    wb = openpyxl.load_workbook(fpath, data_only=True)
    ws = wb['Form responses 1']
    rows = list(ws.iter_rows(values_only=True))
    for r_idx, row in enumerate(rows[1:], 2):
        gn_raw = str(row[2] or "").strip()
        for s_idx in range(8):
            d_col = 4 + s_idx * 4
            desc_col = 5 + s_idx * 4
            p_col = 6 + s_idx * 4
            raw_d = str(row[d_col] or "").strip() if d_col < len(row) else ""
            raw_desc = str(row[desc_col] or "").strip() if desc_col < len(row) else ""
            if re.search(r'[a-zA-Z]{4,}', raw_desc):
                singlish_slots.append({
                    'sheet': sheet_title,
                    'row': r_idx,
                    'slot': s_idx + 1,
                    'gn': gn_raw,
                    'date': raw_d,
                    'desc': raw_desc
                })

print(f"Total slots with English/Singlish text: {len(singlish_slots)}\n")
for s in singlish_slots:
    print(f"[{s['sheet']} R{s['row']} S{s['slot']}] GN: {s['gn']} | Date: {s['date']}")
    print(f"   Desc: {s['desc'][:80]}")
