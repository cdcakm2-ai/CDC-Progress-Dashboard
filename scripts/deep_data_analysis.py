import csv
import json
from collections import defaultdict

def inspect():
    for path, name in [('raw_drive_data/sheet1_form_responses_1.csv', 'Sheet1'),
                       ('raw_drive_data/sheet2_form_responses_1.csv', 'Sheet2')]:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            reader = list(csv.reader(f))
            print(f"=== {name} ({len(reader)-1} data rows) ===")
            gn_counts = defaultdict(list)
            for r_idx, row in enumerate(reader[1:], 1):
                timestamp = row[0]
                officer = row[1]
                gn = row[2]
                claimed = row[3]
                gn_counts[gn].append((r_idx, timestamp, claimed))
            
            print(f"Unique GN Division strings: {len(gn_counts)}")
            multi_subs = {k: v for k, v in gn_counts.items() if len(v) > 1}
            print(f"GNs with multiple rows: {len(multi_subs)}")
            for gn, rows in multi_subs.items():
                print(f"  GN: '{gn}' -> rows: {rows}")

inspect()
