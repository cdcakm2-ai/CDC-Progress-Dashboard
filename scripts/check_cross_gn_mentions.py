import openpyxl, glob, json, re

with open('raw_drive_data/canonical_v4.json', encoding='utf-8') as f:
    v4 = json.load(f)
official_gn_list = [g['nameSi'] for g in v4['gnDivisions']]

def get_base_name(gn):
    return re.sub(r'^[0-9\/\s\-a-zA-Z\u0D80-\u0DFF]+\s+', '', gn).strip()

# Check if any row mentions a DIFFERENT GN division in its description
for fpath in sorted(glob.glob('raw_drive_data/new_imports/*.xlsx')):
    wb = openpyxl.load_workbook(fpath, data_only=True)
    ws = wb['Form responses 1']
    rows = list(ws.iter_rows(values_only=True))[1:]
    for r_idx, r in enumerate(rows):
        if not r or len(r) < 3 or not r[2]: continue
        row_gn = str(r[2]).strip()
        for s in range(8):
            desc = str(r[5 + s*4] or "") if (5 + s*4) < len(r) else ""
            if not desc: continue
            # check if desc mentions another GN
            for off in official_gn_list:
                base = get_base_name(off)
                if len(base) > 4 and base in desc and base not in row_gn:
                    # check if it's a joint activity
                    # print(f"[{os.path.basename(fpath)}] Row {r_idx+2} ({row_gn}) Slot {s+1}: mentions '{base}' -> {desc[:60]}")
                    pass
