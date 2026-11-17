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

audit_results = []
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
            
            # Check day diff
            try:
                diff_d = abs((datetime.strptime(d1[:10], "%Y-%m-%d") - datetime.strptime(d2[:10], "%Y-%m-%d")).days)
            except:
                diff_d = 999
                
            # If same date OR same month with sim > 0.40 OR diff_d <= 7 with sim > 0.35 OR sim > 0.65
            if same_date or (same_month and sim > 0.40) or (diff_d <= 14 and sim > 0.45) or sim > 0.65:
                audit_results.append({
                    'gn': gn,
                    'sim': sim,
                    'diff_d': diff_d,
                    'same_date': same_date,
                    'same_month': same_month,
                    'a1': a1,
                    'a2': a2
                })

print(f"Total candidate pairs found: {len(audit_results)}")
for idx, c in enumerate(audit_results, 1):
    a1, a2 = c['a1'], c['a2']
    print(f"[{idx:02d}] GN: {c['gn']} | DaysDiff: {c['diff_d']} | Sim: {c['sim']:.2f}")
    print(f"     [A] ID={a1['id']} | Sheet={a1.get('sourceSheet')} | Date={a1['date']} | Photos={len(a1['images'])}")
    print(f"         {a1['description'][:90]}")
    print(f"     [B] ID={a2['id']} | Sheet={a2.get('sourceSheet')} | Date={a2['date']} | Photos={len(a2['images'])}")
    print(f"         {a2['description'][:90]}")
    print("-" * 80)
