import openpyxl
from collections import defaultdict

sheet_files = [
    ('Main Cumulative (Nov-Jul)', 'raw_drive_data/new_imports/sheet_main_responses.xlsx'),
    ('June Monthly Responses', 'raw_drive_data/new_imports/sheet_officers_monthly_responses.xlsx'),
    ('July Monthly Responses', 'raw_drive_data/new_imports/sheet_monthly_responses.xlsx'),
    ('August Monthly Responses', 'raw_drive_data/new_imports/sheet_august_copy.xlsx'),
    ('September Monthly Responses', 'raw_drive_data/new_imports/sheet_august_copy_copy.xlsx'),
]

# Let's inspect 152 පිලාන in August, and 109/ ජී ඇටඹගස්මුල්ල in Main Cumulative
for title, fpath in sheet_files:
    wb = openpyxl.load_workbook(fpath, data_only=True)
    ws = wb['Form responses 1']
    rows = list(ws.iter_rows(values_only=True))[1:]
    
    for r_idx, r in enumerate(rows):
        if not r or len(r) < 3 or not r[2]: continue
        gn = str(r[2]).strip()
        if 'පිලාන' in gn or 'ඇටඹගස්මුල්ල' in gn:
            print(f"\n[{title}] Row {r_idx+2} - GN: {gn} - Officer: {r[1]} - Timestamp: {r[0]}")
            # print all non-empty activity slots
            for s in range(8):
                d = r[4 + s*4] if (4 + s*4) < len(r) else None
                desc = r[5 + s*4] if (5 + s*4) < len(r) else None
                ph = r[6 + s*4] if (6 + s*4) < len(r) else None
                if d or desc or ph:
                    print(f"  Slot {s+1}: Date={d} | Desc={str(desc)[:60]} | Photos={'Yes' if ph else 'No'}")
