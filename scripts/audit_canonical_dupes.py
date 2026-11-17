import json
from collections import defaultdict
from difflib import SequenceMatcher

with open('raw_drive_data/canonical_v10.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

acts = data['activities']
print(f"Total canonical activities: {len(acts)}")

def extract_photo_ids(act):
    p_ids = set()
    for p in act.get('photos', []):
        if isinstance(p, dict):
            p_ids.add(p.get('id') or p.get('fullUrl') or p.get('driveUrl') or str(p))
        elif isinstance(p, str):
            p_ids.add(p)
    return p_ids

by_gn = defaultdict(list)
for a in acts:
    by_gn[a['gnDivision']].append(a)

potential_dupes = []

for gn, gn_acts in by_gn.items():
    n = len(gn_acts)
    for i in range(n):
        for j in range(i + 1, n):
            a1 = gn_acts[i]
            a2 = gn_acts[j]
            
            p1 = extract_photo_ids(a1)
            p2 = extract_photo_ids(a2)
            common_photos = p1.intersection(p2)
            
            t1 = str(a1.get('title', '')).strip().lower()
            t2 = str(a2.get('title', '')).strip().lower()
            d1 = str(a1.get('description', '')).strip().lower()
            d2 = str(a2.get('description', '')).strip().lower()
            
            sim_t = SequenceMatcher(None, t1, t2).ratio()
            sim_d = SequenceMatcher(None, d1, d2).ratio()
            same_date = (a1.get('date') == a2.get('date'))
            
            if common_photos:
                potential_dupes.append({
                    'type': 'SHARED_PHOTOS',
                    'gn': gn,
                    'act1': (a1['id'], a1.get('date'), a1.get('title')[:50], len(p1)),
                    'act2': (a2['id'], a2.get('date'), a2.get('title')[:50], len(p2)),
                    'common_photos': len(common_photos)
                })
            elif (sim_t > 0.80 or sim_d > 0.80) and same_date:
                potential_dupes.append({
                    'type': 'SAME_DATE_SIMILAR_TEXT',
                    'gn': gn,
                    'act1': (a1['id'], a1.get('date'), a1.get('title')[:50]),
                    'act2': (a2['id'], a2.get('date'), a2.get('title')[:50]),
                    'sim_t': round(sim_t, 2),
                    'sim_d': round(sim_d, 2)
                })
            elif sim_t > 0.90 or sim_d > 0.90:
                potential_dupes.append({
                    'type': 'HIGH_TEXT_SIMILARITY',
                    'gn': gn,
                    'act1': (a1['id'], a1.get('date'), a1.get('title')[:50]),
                    'act2': (a2['id'], a2.get('date'), a2.get('title')[:50]),
                    'sim_t': round(sim_t, 2),
                    'sim_d': round(sim_d, 2)
                })

print(f"Total potential duplicates found: {len(potential_dupes)}")
for p in potential_dupes:
    print(p)
