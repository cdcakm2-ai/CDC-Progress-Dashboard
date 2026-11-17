import json

with open('raw_drive_data/canonical_v9.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

merges = data.get('mergesLog', [])

# Let's inspect all 77 merges in detail:
with open('raw_drive_data/detailed_merges_review.txt', 'w', encoding='utf-8') as out:
    for idx, m in enumerate(merges, 1):
        out.write(f"#{idx:02d} [{m['gn']}]\n")
        out.write(f"   Reason: {m['reason']}\n")
        out.write(f"   KEPT: {m['kept']}\n")
        out.write(f"   DUP : {m['duplicate']}\n\n")

print(f"Written all {len(merges)} merges to raw_drive_data/detailed_merges_review.txt")
