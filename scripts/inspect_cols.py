import csv
import json
import re

for sheet_name, path in [('Sheet 1', 'raw_drive_data/sheet1_form_responses_1.csv'),
                         ('Sheet 2', 'raw_drive_data/sheet2_form_responses_1.csv')]:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
        print(f"=== {sheet_name} ===")
        print(f"Total Rows: {len(rows)}")
        print(f"Header length: {len(header)}")
        for idx, col in enumerate(header):
            print(f"  Col {idx}: {col[:60]}")
