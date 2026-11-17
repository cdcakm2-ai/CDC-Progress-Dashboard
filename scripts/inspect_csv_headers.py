import csv
import glob
import os

csvs = glob.glob('raw_drive_data/new_imports/csvs/*.csv')
for cp in sorted(csvs):
    base = os.path.basename(cp)
    print(f"\n==================== {base} ====================")
    with open(cp, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header:
            print(f"Total cols: {len(header)}")
            print("First 8 cols:", header[:8])
            # Count rows
            rows = list(reader)
            print(f"Data rows: {len(rows)}")
            if rows:
                print("Row 1 sample (first 5 cols):", rows[0][:5])
                # Check what months / dates are present
                dates = []
                for r in rows:
                    for c in r:
                        if any(yr in str(c) for yr in ['2025', '2026', '2024']):
                            dates.append(str(c)[:10])
                print("Sample dates found in sheet:", list(set(dates))[:10])
