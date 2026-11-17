import csv
import json
import re
from datetime import datetime
from collections import defaultdict

# Import previous test_extractor logic or run inline
from test_extractor import raw_activities, names_63

print(f"Total raw activities to analyze: {len(raw_activities)}")

# 1. Date range analysis
dates = [a['date'] for a in raw_activities if a['date']]
dates.sort()
min_date = dates[0]
max_date = dates[-1]
print(f"Earliest activity date: {min_date}")
print(f"Latest activity date: {max_date}")

# Check future dates (relative to today, e.g. 2026-11-16)
future_dates = [a for a in raw_activities if a['date'] > '2026-11-16']
print(f"Activities with future dates: {len(future_dates)}")
for a in future_dates:
    print(f"  Future: {a['date']} - GN: {a['gn_name']} - Desc: {a['description'][:50]}")

# 2. Sheet 1 vs Sheet 2 date distribution
month_counts_sheet1 = defaultdict(int)
month_counts_sheet2 = defaultdict(int)
for a in raw_activities:
    m = a['date'][:7]
    if 'Sheet 1' in a['sheet']:
        month_counts_sheet1[m] += 1
    else:
        month_counts_sheet2[m] += 1

print("\n=== Month Distribution by Sheet ===")
print("Sheet 1 (Nov 2025 - Jul 2026 Responses):")
for m in sorted(month_counts_sheet1.keys()):
    print(f"  {m}: {month_counts_sheet1[m]} activities")

print("\nSheet 2 (August 2026 Responses):")
for m in sorted(month_counts_sheet2.keys()):
    print(f"  {m}: {month_counts_sheet2[m]} activities")

# 3. Deduplication logic
# Clean string for comparison: strip punctuation, extra whitespace
def clean_text(t):
    return re.sub(r'[\s\.,\-\/]+', ' ', t).strip().lower()

# Check confirmed duplicates:
# A confirmed duplicate is when the same GN division submits the identical activity
# with same date and same description (or same photos).
seen_exact = {}
confirmed_duplicates = []
possible_duplicates = []
unique_activities = []

# Group by GN
gn_groups = defaultdict(list)
for a in raw_activities:
    gn_groups[a['gn_name']].append(a)

for gn, acts in gn_groups.items():
    # Sort by date
    acts.sort(key=lambda x: x['date'] or '')
    
    handled = set()
    for i in range(len(acts)):
        if i in handled:
            continue
        act1 = acts[i]
        c_desc1 = clean_text(act1['description'])
        p_set1 = set(act1['photos'])
        
        duplicates_for_this = []
        possible_for_this = []
        
        for j in range(i + 1, len(acts)):
            if j in handled:
                continue
            act2 = acts[j]
            c_desc2 = clean_text(act2['description'])
            p_set2 = set(act2['photos'])
            
            # Exact match on date and description
            if act1['date'] == act2['date'] and (c_desc1 == c_desc2 or (p_set1 and p_set1 == p_set2)):
                duplicates_for_this.append(act2)
                handled.add(j)
            # Possible duplicate: same date and description overlap > 70% or same photos
            elif act1['date'] == act2['date'] and (c_desc1 in c_desc2 or c_desc2 in c_desc1 or (p_set1 and p_set1.intersection(p_set2))):
                possible_for_this.append(act2)
                # Note: don't automatically drop possible duplicates, but flag them
            # Or adjacent dates (difference <= 1 day) and exact same description
            elif c_desc1 and c_desc1 == c_desc2 and act1['date'] and act2['date']:
                d1 = datetime.strptime(act1['date'], '%Y-%m-%d')
                d2 = datetime.strptime(act2['date'], '%Y-%m-%d')
                if abs((d2 - d1).days) <= 1:
                    possible_for_this.append(act2)
                    
        if duplicates_for_this:
            for dup in duplicates_for_this:
                confirmed_duplicates.append({
                    'original': act1,
                    'duplicate': dup,
                    'reason': 'සමාන වසම, දිනය හා විස්තරය/ඡායාරූප (Exact duplicate)'
                })
        if possible_for_this:
            for p_dup in possible_for_this:
                possible_duplicates.append({
                    'original': act1,
                    'possible': p_dup,
                    'reason': 'සමාන දිනයක හෝ ආසන්න දිනයක සමාන කාර්යයක් (Possible duplicate)'
                })
                
        # The primary canonical activity is act1
        # Merge photo links if duplicates had additional photos
        combined_photos = list(dict.fromkeys(act1['photos'] + [p for d in duplicates_for_this for p in d['photos']]))
        canonical_entry = dict(act1)
        canonical_entry['photos'] = combined_photos
        canonical_entry['duplicate_count'] = len(duplicates_for_this)
        unique_activities.append(canonical_entry)

print("\n=== Deduplication Summary ===")
print(f"Total raw activity submissions: {len(raw_activities)}")
print(f"Confirmed exact duplicates detected & filtered: {len(confirmed_duplicates)}")
print(f"Possible duplicates flagged for review: {len(possible_duplicates)}")
print(f"Total Canonical Unique Activities: {len(unique_activities)}")

if confirmed_duplicates:
    print("\nConfirmed Duplicates Preview:")
    for c in confirmed_duplicates:
        orig = c['original']
        dup = c['duplicate']
        print(f"  GN: {orig['gn_name']} | Date: {orig['date']} | Desc: {orig['description'][:40]} | Orig Sheet: {orig['sheet']} vs Dup Sheet: {dup['sheet']}")

if possible_duplicates:
    print("\nPossible Duplicates Preview:")
    for c in possible_duplicates:
        orig = c['original']
        dup = c['possible']
        print(f"  GN: {orig['gn_name']} | Date: {orig['date']} vs {dup['date']} | Desc: {orig['description'][:30]} vs {dup['description'][:30]}")
