import openpyxl, glob, json
from collections import defaultdict

sheet_files = [
    ('Main Cumulative (Nov-Jul)', 'raw_drive_data/new_imports/sheet_main_responses.xlsx'),
    ('June Monthly Responses', 'raw_drive_data/new_imports/sheet_officers_monthly_responses.xlsx'),
    ('July Monthly Responses', 'raw_drive_data/new_imports/sheet_monthly_responses.xlsx'),
    ('August Monthly Responses', 'raw_drive_data/new_imports/sheet_august_copy.xlsx'),
    ('September Monthly Responses', 'raw_drive_data/new_imports/sheet_august_copy_copy.xlsx'),
]

# Let's inspect each sheet:
# How many rows?
# For each GN, how many rows were submitted in each sheet?
for title, fpath in sheet_files:
    wb = openpyxl.load_workbook(fpath, data_only=True)
    ws = wb['Form responses 1']
    rows = list(ws.iter_rows(values_only=True))[1:]
    gn_counts = defaultdict(int)
    for r in rows:
        if r and len(r) > 2 and r[2]:
            gn_counts[str(r[2]).strip()] += 1
            
    # Check if any GN has > 1 row in the SAME sheet!
    multi = {g: c for g, c in gn_counts.items() if c > 1}
    print(f"=== {title} ===")
    print(f"Total rows: {len(rows)}, Unique GNs: {len(gn_counts)}")
    if multi:
        print(f"  GNs with MULTIPLE submissions in this single sheet ({len(multi)}):")
        for g, c in sorted(multi.items()):
            print(f"    {g}: {c} submissions")
