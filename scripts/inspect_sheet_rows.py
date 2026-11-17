import openpyxl
import os
import glob

files = glob.glob('raw_drive_data/new_imports/*.xlsx')
print(f"Found {len(files)} files: {files}")

for f in sorted(files):
    wb = openpyxl.load_workbook(f, data_only=True)
    sheet = wb.active
    print(f"\n==========================================")
    print(f"File: {os.path.basename(f)}")
    print(f"Sheet name: {sheet.title}, Rows: {sheet.max_row}, Cols: {sheet.max_column}")
    
    headers = [str(sheet.cell(1, c).value or '').strip() for c in range(1, sheet.max_column + 1)]
    for idx, h in enumerate(headers, 1):
        if h and any(k in h for k in ['වසම', 'ග්‍රාම', 'GN', 'Grama', 'කොට්ඨාස', 'නම', 'Timestamp', 'මුද්දරය']):
            print(f"  Col {idx}: {h[:80]}")
            
    # Print sample of first 3 rows for GN column
    # Let's see which column actually has the GN division
    for r in range(2, min(5, sheet.max_row + 1)):
        row_vals = [str(sheet.cell(r, c).value or '').strip() for c in range(1, min(10, sheet.max_column + 1))]
        print(f"  Row {r}: {row_vals[:6]}")
