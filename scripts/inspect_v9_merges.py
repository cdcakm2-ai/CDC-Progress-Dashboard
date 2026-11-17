import json

with open('raw_drive_data/canonical_v9.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

merges = data.get('mergesLog', [])
print(f"Total merges logged: {len(merges)}\n")

for idx, m in enumerate(merges, 1):
    print(f"#{idx:02d} [{m['gn']}] Reason: {m['reason']}")
    print(f"    KEPT: {m['kept']}")
    print(f"    DUP : {m['duplicate']}\n")
