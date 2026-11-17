import json
from collections import defaultdict
from difflib import SequenceMatcher

with open('raw_drive_data/canonical_v8.json', encoding='utf-8') as f:
    data = json.load(f)

acts = data['activities']
by_gn = defaultdict(list)
for a in acts:
    by_gn[a['gnNameSi']].append(a)

print(f'Checking {len(acts)} activities across {len(by_gn)} GNs...\n')

dups = []
for gn, glist in sorted(by_gn.items()):
    for i in range(len(glist)):
        for j in range(i+1, len(glist)):
            a1, a2 = glist[i], glist[j]
            t1, t2 = (a1.get('description') or '').strip(), (a2.get('description') or '').strip()
            d1, d2 = a1.get('date'), a2.get('date')
            
            c1 = ''.join(t1.split()).lower()
            c2 = ''.join(t2.split()).lower()
            sim = SequenceMatcher(None, c1, c2).ratio()
            
            same_date = (d1 == d2)
            same_month = (d1[:7] == d2[:7]) if (d1 and d2) else False
            
            reason = None
            if same_date and (sim > 0.35 or c1 in c2 or c2 in c1):
                reason = f"Same Date ({d1}) + sim={sim:.2f}"
            elif same_month and sim > 0.60:
                reason = f"Same Month ({d1[:7]}) + high sim={sim:.2f}"
            elif sim > 0.75:
                reason = f"Very high sim={sim:.2f} (d1={d1}, d2={d2})"
            elif same_month and (c1 in c2 or c2 in c1) and min(len(c1), len(c2)) > 15:
                reason = f"Substring in same month (d1={d1}, d2={d2})"
                
            if reason:
                dups.append((gn, reason, a1, a2))

print(f'Total duplicate suspects flagged: {len(dups)}')
for gn, r, a1, a2 in dups:
    print(f"GN: {gn} | Reason: {r}")
    print(f"   [1] ID: {a1['id']} | Date: {a1['date']} | Photos: {len(a1['images'])} | Desc: {a1['description'][:80]}")
    print(f"   [2] ID: {a2['id']} | Date: {a2['date']} | Photos: {len(a2['images'])} | Desc: {a2['description'][:80]}")
    print('-'*70)
