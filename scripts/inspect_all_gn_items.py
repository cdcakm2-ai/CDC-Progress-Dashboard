import csv
import json
import re
from collections import defaultdict

# Let's inspect all items per GN
from meticulous_dedup import by_gn

print(f"Number of GNs with records: {len(by_gn)}")
# Let's print out all activities for GNs where len(items) > 1
for gn, items in sorted(by_gn.items()):
    if len(items) > 1:
        print(f"\n=======================================================")
        print(f"GN: {gn} ({len(items)} raw activity items)")
        for idx, it in enumerate(items, 1):
            p_cnt = len(it['photos'])
            print(f"  [{idx}] {it['sheet']} R{it['row']} B{it['block']} | Date: {it['date_raw']} | Photos: {p_cnt} | Desc: {it['desc']}")
