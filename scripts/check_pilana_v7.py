import json
from collections import defaultdict

with open('raw_drive_data/canonical_v7.json', encoding='utf-8') as f:
    v7 = json.load(f)

print(f"Total activities in canonical_v7: {len(v7['activities'])}")

acts_by_gn = defaultdict(list)
for a in v7['activities']:
    acts_by_gn[a['gnNameSi']].append(a)

# Check Pilana specifically
pilana_acts = acts_by_gn.get('152 පිලාන', [])
print(f"\n=== 152 පිලාන activities ({len(pilana_acts)}) ===")
for idx, a in enumerate(pilana_acts, 1):
    print(f"{idx}. [{a['date']}] {a['titleSi']} (Photos: {a.get('photoCount', len(a.get('images', [])))})")
    print(f"   Desc: {a['description'][:80]}...")
