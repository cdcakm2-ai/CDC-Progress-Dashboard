import openpyxl
import csv
import os

files = [
    'sheet_main_responses.xlsx',
    'sheet_august_copy_copy.xlsx',
    'sheet_august_copy.xlsx',
    'sheet_monthly_responses.xlsx',
    'sheet_officers_monthly_responses.xlsx'
]

os.makedirs('raw_drive_data/new_imports/csvs', exist_ok=True)

for xf in files:
    xpath = os.path.join('raw_drive_data/new_imports', xf)
    base_name = xf.replace('.xlsx', '')
    print(f"\nProcessing {xf}...")
    try:
        wb = openpyxl.load_workbook(xpath, data_only=True)
        for sname in wb.sheetnames:
            ws = wb[sname]
            clean_sname = "".join([c if c.isalnum() or c in (' ', '_') else '_' for c in sname]).strip()
            csv_path = f"raw_drive_data/new_imports/csvs/{base_name}_{clean_sname}.csv"
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                row_count = 0
                for row in ws.iter_rows(values_only=True):
                    # Check if row is not completely empty
                    if any(cell is not None for cell in row):
                        # Convert cells to string or empty
                        clean_row = [str(c) if c is not None else '' for c in row]
                        writer.writerow(clean_row)
                        row_count += 1
            print(f"  -> Sheet '{sname}': {row_count} rows saved to {csv_path}")
    except Exception as e:
        print(f"Error reading {xf}: {e}")
