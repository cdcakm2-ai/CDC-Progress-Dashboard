import json
from collections import defaultdict
from test_perfect_dedup2 import clean_pool, official_gn_list

counts = defaultdict(int)
photo_counts = defaultdict(int)
for a in clean_pool:
    counts[a['gn']] += 1
    photo_counts[a['gn']] += len(a['photos'])

print(f"{'#':<3} | {'GN Division Name':<30} | {'Activities':<10} | {'Photos':<8}")
print("-" * 60)
for idx, gn in enumerate(official_gn_list, 1):
    c = counts.get(gn, 0)
    p = photo_counts.get(gn, 0)
    print(f"{idx:<3} | {gn:<30} | {c:<10} | {p:<8}")

print("-" * 60)
print(f"Total Divisions: {len(official_gn_list)}")
print(f"Divisions with Activities: {len([g for g in official_gn_list if counts[g] > 0])}")
print(f"Total Activities: {sum(counts.values())}")
print(f"Total Photos: {sum(photo_counts.values())}")
