import json

with open('raw_drive_data/merges_log_v9.json', encoding='utf-8') as f:
    logs = json.load(f)

print(f"Total merges in v9: {len(logs)}\n")
for i, m in enumerate(logs, 1):
    print(f"[{i:02d}] GN: {m['gn']} | Reason: {m['reason']}")
    print(f"     KEPT: {m['kept']}")
    print(f"     DUP : {m['duplicate']}")
    print("-" * 80)
