import json
import re

with open('raw_drive_data/canonical_v9.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

merges = data.get('mergesLog', [])

suspicious_indices = [2, 14, 20, 25, 39, 40, 41, 50, 56, 58, 60, 61, 67]

# Let's inspect all 77 merges for potential distinct activities!
print(f"Total merges in log: {len(merges)}\n")

for idx, m in enumerate(merges, 1):
    reason = m['reason']
    # Check if reason had low similarity or empty common elements
    if 'sim=0.' in reason or 'common elements ([],' in reason or idx in suspicious_indices:
        print(f"=== Check #{idx:02d} [{m['gn']}] ===")
        print(f"Reason: {reason}")
        print(f"KEPT: {m['kept']}")
        print(f"DUP : {m['duplicate']}")
        print()
