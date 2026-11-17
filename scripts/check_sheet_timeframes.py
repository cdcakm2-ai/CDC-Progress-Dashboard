import csv
import glob

files = [
    ('Main (Original Sheet 1)', 'raw_drive_data/new_imports/csvs/sheet_main_responses_Form responses 1.csv'),
    ('Aug/Sep Original (Original Sheet 2)', 'raw_drive_data/new_imports/csvs/sheet_august_copy_copy_Form responses 1.csv'),
    ('June Sheet', 'raw_drive_data/new_imports/csvs/sheet_officers_monthly_responses_Form responses 1.csv'),
    ('July Sheet', 'raw_drive_data/new_imports/csvs/sheet_monthly_responses_Form responses 1.csv'),
    ('August Updated Sheet', 'raw_drive_data/new_imports/csvs/sheet_august_copy_Form responses 1.csv'),
]

for label, path in files:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = list(reader)
        # Check timestamps
        timestamps = [r[0] for r in rows if r and r[0]]
        gns = [r[2] for r in rows if r and len(r) > 2 and r[2]]
        print(f"\n==================== {label} ====================")
        print(f"Total rows: {len(rows)}")
        print(f"Unique GNs: {len(set(gns))}")
        if timestamps:
            print(f"Earliest timestamp: {min(timestamps)}")
            print(f"Latest timestamp: {max(timestamps)}")
        # Check dates in col 4
        dates = [r[4] for r in rows if len(r) > 4 and r[4]]
        print(f"Sample activity dates in col 4: {dates[:5]}")
