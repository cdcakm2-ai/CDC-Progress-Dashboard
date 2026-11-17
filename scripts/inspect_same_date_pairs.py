import json
from collections import defaultdict
from difflib import SequenceMatcher

with open('raw_drive_data/canonical_v8.json', encoding='utf-8') as f:
    data = json.load(f)

acts = data['activities']
by_gn = defaultdict(list)
for a in acts:
    by_gn[a['gnNameSi']].append(a)

same_date_pairs = []
for gn, glist in sorted(by_gn.items()):
    for i in range(len(glist)):
        for j in range(i+1, len(glist)):
            a1, a2 = glist[i], glist[j]
            d1, d2 = a1.get('date'), a2.get('date')
            if d1 == d2:
                t1, t2 = (a1.get('description') or '').strip(), (a2.get('description') or '').strip()
                c1 = ''.join(t1.split()).lower()
                c2 = ''.join(t2.split()).lower()
                sim = SequenceMatcher(None, c1, c2).ratio()
                same_date_pairs.append({
                    'gn': gn,
                    'date': d1,
                    'sim': sim,
                    'a1': a1,
                    'a2': a2
                })

print(f"Total same-date pairs within same GN: {len(same_date_pairs)}")
for idx, p in enumerate(same_date_pairs, 1):
    a1, a2 = p['a1'], p['a2']
    print(f"[{idx:02d}] GN: {p['gn']} | Date: {p['date']} | Sim: {p['sim']:.2f}")
    print(f"     A1 [{a1['id']}]: ({a1.get('sourceSheet')}) {a1['description'][:90]}")
    print(f"     A2 [{a2['id']}]: ({a2.get('sourceSheet')}) {a2['description'][:90]}")
    print("-" * 80)
