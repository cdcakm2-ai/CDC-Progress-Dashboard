import json
import re
from difflib import SequenceMatcher

with open('raw_drive_data/canonical_v5.json', encoding='utf-8') as f:
    d = json.load(f)

activities = d['activities']
print(f"Total current activities: {len(activities)}")

# Group activities by standardized GN division
gn_groups = {}
for act in activities:
    gn = act['gnNameSi']
    if gn not in gn_groups:
        gn_groups[gn] = []
    gn_groups[gn].append(act)

def norm_si(text):
    if not text: return ""
    t = str(text).lower()
    t = re.sub(r'[\s\.\,\-\_\/\(\)]+', ' ', t).strip()
    return t

# Common keywords for programs
keywords = [
    "දන්සල", "දන්සැල", "ක්‍රිකට්", "අවුරුදු", "බක්මහ", "පහන්", "ඩෙංගු", "ශ්‍රමදාන", 
    "තණකොළ", "පොළ", "බෝධි", "පූජා", "පුහුණු", "මහන", "බිම්මල්", "පැළ", "පැල", 
    "පොත්", "ආධාර", "ආශිර්වාද", "වැසිකිලි", "මාර්ග", "පාලම", "අමුණ", "කාණු", 
    "වෙසක්", "පොසොන්", "ලේ දන්දීම", "වෛද්‍ය", "සායන", "ගර්භනී", "වැඩිහිටි"
]

potential_duplicates = []

for gn, acts in gn_groups.items():
    n = len(acts)
    if n < 2:
        continue
    for i in range(n):
        for j in range(i + 1, n):
            a1 = acts[i]
            a2 = acts[j]
            
            d1 = a1['date']
            d2 = a2['date']
            t1 = norm_si(a1['titleSi'] + " " + a1['description'])
            t2 = norm_si(a2['titleSi'] + " " + a2['description'])
            
            sim = SequenceMatcher(None, t1, t2).ratio()
            
            # Check shared keywords
            shared_kws = [k for k in keywords if (k in t1 and k in t2)]
            
            # Check date match or closeness
            is_same_date = (d1 == d2)
            same_month = (d1[:7] == d2[:7])
            
            # Reasons for suspicion:
            suspicious = False
            reason = ""
            
            if is_same_date:
                suspicious = True
                reason = f"Exact same date ({d1}) in same GN ({gn})"
            elif same_month and len(shared_kws) > 0:
                suspicious = True
                reason = f"Same month ({d1[:7]} vs {d2[:7]}) + shared keyword {shared_kws} in {gn}"
            elif len(shared_kws) >= 2:
                suspicious = True
                reason = f"Strong keyword overlap {shared_kws} ({d1} vs {d2}) in {gn}"
            elif sim > 0.45:
                suspicious = True
                reason = f"Text similarity {sim:.2f} ({d1} vs {d2}) in {gn}"
                
            if suspicious:
                potential_duplicates.append({
                    'gn': gn,
                    'reason': reason,
                    'act1': {
                        'id': a1['id'], 'date': d1, 'title': a1['titleSi'], 
                        'desc': a1['description'][:70], 'photos': len(a1.get('images', []))
                    },
                    'act2': {
                        'id': a2['id'], 'date': d2, 'title': a2['titleSi'], 
                        'desc': a2['description'][:70], 'photos': len(a2.get('images', []))
                    }
                })

print(f"Total potential duplicate pairs flagged: {len(potential_duplicates)}\n")

# Print first 40 flagged pairs
for idx, p in enumerate(potential_duplicates[:40]):
    print(f"[{idx+1}] GN: {p['gn']} | Reason: {p['reason']}")
    print(f"     A1 ({p['act1']['id']}): {p['act1']['date']} | {p['act1']['title']} ({p['act1']['photos']} photos)")
    print(f"         {p['act1']['desc']}")
    print(f"     A2 ({p['act2']['id']}): {p['act2']['date']} | {p['act2']['title']} ({p['act2']['photos']} photos)")
    print(f"         {p['act2']['desc']}")
    print("-" * 80)
