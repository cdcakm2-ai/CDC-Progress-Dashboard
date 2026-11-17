import json
import re

with open('raw_drive_data/canonical_v5_draft.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load official 63 GN divisions from canonical_v4.json
with open('raw_drive_data/canonical_v4.json', 'r', encoding='utf-8') as f:
    v4 = json.load(f)
official_gns = [g['nameSi'] for g in v4['gnDivisions']]
print(f"Total official GN divisions in master list: {len(official_gns)}")

# Check GN names in draft v5
v5_gns = {}
for act in data['master_activities']:
    gn = act['gn']
    v5_gns[gn] = v5_gns.get(gn, 0) + 1

print(f"\nGN names in draft v5: {len(v5_gns)}")

# Check exact matches vs non-exact matches
matched = []
unmatched = []
for gn, count in sorted(v5_gns.items()):
    if gn in official_gns:
        matched.append((gn, count))
    else:
        unmatched.append((gn, count))

print(f"Exact matches with official list: {len(matched)}")
print(f"Unmatched variants: {len(unmatched)}")
for gn, count in unmatched:
    print(f"  Unmatched: '{gn}' ({count} activities)")
    # Suggest closest official match
    from difflib import get_close_matches
    closest = get_close_matches(gn, official_gns, n=2, cutoff=0.5)
    print(f"     -> Suggestion: {closest}")
