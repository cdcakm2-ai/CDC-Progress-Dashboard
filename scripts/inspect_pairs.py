import json

with open('raw_drive_data/canonical_v10.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

acts = {a['id']: a for a in data['activities']}

pairs = [
    ('ACT-2026-0028', 'ACT-2026-0030'),
    ('ACT-2026-0042', 'ACT-2026-0047'),
    ('ACT-2026-0046', 'ACT-2026-0050'),
    ('ACT-2026-0101', 'ACT-2026-0102'),
    ('ACT-2026-0140', 'ACT-2026-0141'),
    ('ACT-2026-0339', 'ACT-2026-0340'),
    ('ACT-2026-0394', 'ACT-2026-0395'),
    ('ACT-2026-0399', 'ACT-2026-0409'),
]

for id1, id2 in pairs:
    a1 = acts[id1]
    a2 = acts[id2]
    print(f"=== PAIR: {id1} vs {id2} in {a1['gnDivision']} ===")
    print(f"  [1] Date: {a1['date']} | Sheet: {a1['sourceSheet']} (Row {a1['sourceRow']})")
    print(f"      Title: {a1['title']}")
    print(f"      Desc : {a1['description'][:100]}")
    print(f"      Photos ({len(a1['photos'])}): {[p.get('id') if isinstance(p, dict) else p for p in a1['photos']]}")
    print(f"  [2] Date: {a2['date']} | Sheet: {a2['sourceSheet']} (Row {a2['sourceRow']})")
    print(f"      Title: {a2['title']}")
    print(f"      Desc : {a2['description'][:100]}")
    print(f"      Photos ({len(a2['photos'])}): {[p.get('id') if isinstance(p, dict) else p for p in a2['photos']]}")
    print()
