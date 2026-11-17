import json
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import datetime

with open('raw_drive_data/canonical_v8.json', encoding='utf-8') as f:
    data = json.load(f)

acts = data['activities']
by_gn = defaultdict(list)
for a in acts:
    by_gn[a['gnNameSi']].append(a)

pairs = []
for gn, glist in sorted(by_gn.items()):
    for i in range(len(glist)):
        for j in range(i+1, len(glist)):
            a1, a2 = glist[i], glist[j]
            d1, d2 = a1.get('date'), a2.get('date')
            try:
                diff_d = abs((datetime.strptime(d1[:10], "%Y-%m-%d") - datetime.strptime(d2[:10], "%Y-%m-%d")).days)
            except:
                diff_d = 999
            if diff_d <= 3:
                t1, t2 = (a1.get('description') or '').strip(), (a2.get('description') or '').strip()
                c1 = ''.join(t1.split()).lower()
                c2 = ''.join(t2.split()).lower()
                sim = SequenceMatcher(None, c1, c2).ratio()
                pairs.append({
                    'gn': gn,
                    'diff_d': diff_d,
                    'sim': sim,
                    'a1': a1,
                    'a2': a2
                })

print(f"Total pairs within 3 days: {len(pairs)}")
for idx, p in enumerate(pairs, 1):
    a1, a2 = p['a1'], p['a2']
    print(f"[{idx:02d}] GN: {p['gn']} | DaysDiff: {p['diff_d']} | Sim: {p['sim']:.2f}")
    print(f"     A1 [{a1['id']}]: ({a1.get('sourceSheet')}) Date: {a1['date']} | Photos: {len(a1['images'])}")
    print(f"         {a1['description']}")
    print(f"     A2 [{a2['id']}]: ({a2.get('sourceSheet')}) Date: {a2['date']} | Photos: {len(a2['images'])}")
    print(f"         {a2['description']}")
    print("-" * 80)
