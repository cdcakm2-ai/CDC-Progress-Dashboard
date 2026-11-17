from test_extractor import raw_activities, CATEGORIES
from collections import Counter

# Let's inspect categories
cat_counts = Counter()
other_descs = []

for a in raw_activities:
    cat_counts[a['cat_name']] += 1
    if a['cat_name'] == "වෙනත් / බහුවිධ සංවර්ධන":
        other_descs.append((a['gn_name'], a['description']))

print("=== Category Distribution ===")
for cat, cnt in cat_counts.most_common():
    print(f"  {cat}: {cnt} ({cnt/len(raw_activities)*100:.1f}%)")

print(f"\nUncategorized ('වෙනත්'): {len(other_descs)}")
print("Sample uncategorized descriptions:")
for gn, d in other_descs[:20]:
    print(f"  [{gn}] {d}")
