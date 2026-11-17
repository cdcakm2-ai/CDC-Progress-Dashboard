import json
from collections import defaultdict
from difflib import SequenceMatcher

with open('raw_drive_data/canonical_v8.json', encoding='utf-8') as f:
    data = json.load(f)

acts = data['activities']
by_gn = defaultdict(list)
for a in acts:
    by_gn[a['gnNameSi']].append(a)

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
            
            # Check for definite duplicates:
            # 1. Exact same date AND (sim > 0.35 or common words or substring)
            # 2. Same month AND sim > 0.60
            # 3. Very high sim > 0.70 within 15 days
            is_dup = False
            reason = ""
            
            if same_date:
                # check keywords
                keywords = ["ඩෙංගු", "දන්සල", "දන්සැල", "ශ්‍රමදාන", "ආරක්ෂක", "බැති ගී", "ජල", "පොසොන්", "අවුරුදු", "වෛද්‍ය", "පිරිසිදු"]
                common_kw = [k for k in keywords if (k in t1 and k in t2)]
                if sim > 0.30 or common_kw or (c1 in c2 or c2 in c1):
                    is_dup = True
                    reason = f"Same Date ({d1}) + common keywords {common_kw} + sim={sim:.2f}"
            elif same_month and sim > 0.60:
                is_dup = True
                reason = f"Same Month ({d1[:7]}) + sim={sim:.2f}"
            elif sim > 0.75:
                # check day diff
                try:
                    from datetime import datetime
                    dt1 = datetime.strptime(d1[:10], "%Y-%m-%d")
                    dt2 = datetime.strptime(d2[:10], "%Y-%m-%d")
                    diff = abs((dt1 - dt2).days)
                    if diff <= 31:
                        is_dup = True
                        reason = f"High sim={sim:.2f} within {diff} days ({d1} vs {d2})"
                except:
                    pass
                    
            if is_dup:
                dups.append({
                    'gn': gn,
                    'reason': reason,
                    'a1': a1,
                    'a2': a2
                })

print(f"Definite duplicate pairs found: {len(dups)}")
for idx, d in enumerate(dups, 1):
    a1, a2 = d['a1'], d['a2']
    print(f"[{idx:02d}] GN: {d['gn']} | {d['reason']}")
    print(f"     A1 [{a1['id']}]: Sheet: {a1.get('sourceSheet')} | Date: {a1['date']} | Photos: {len(a1['images'])}")
    print(f"        {a1['description']}")
    print(f"     A2 [{a2['id']}]: Sheet: {a2.get('sourceSheet')} | Date: {a2['date']} | Photos: {len(a2['images'])}")
    print(f"        {a2['description']}")
    print("-" * 80)
