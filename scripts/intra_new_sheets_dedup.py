import json
import re
from difflib import SequenceMatcher

# Let's import genuine_new_blocks from thorough_cross_matching
from thorough_cross_matching import genuine_new_blocks, existing_activities, docx_entries, norm_text, get_drive_ids

print(f"Initial genuine new blocks before intra-dedup: {len(genuine_new_blocks)}")

# Let's check duplicates within genuine_new_blocks:
# An officer might have submitted the same activity in June and again in July, or in August.
# Criteria for duplicate within new blocks:
# 1. Shared photo IDs (same photos = same activity)
# 2. Same GN + high text similarity (> 0.8) + same date

intra_unique = []
intra_duplicates = []

for b in genuine_new_blocks:
    is_dup = False
    b_photos = set(b['photo_ids'])
    b_gn = norm_text(b['gn'])
    b_desc = norm_text(b['desc'])
    
    for u in intra_unique:
        u_photos = set(u['photo_ids'])
        # 1. Photo overlap
        if b_photos and u_photos and len(b_photos.intersection(u_photos)) > 0:
            is_dup = True
            intra_duplicates.append((b, u, f"Shared photo with {u['sheet']} R{u['row']}"))
            break
        
        # 2. Same GN and high text similarity
        u_gn = norm_text(u['gn'])
        u_desc = norm_text(u['desc'])
        if b_gn and u_gn and (b_gn in u_gn or u_gn in b_gn):
            sim = SequenceMatcher(None, b_desc, u_desc).ratio()
            # If text similarity is very high (> 0.85)
            if sim > 0.85:
                is_dup = True
                intra_duplicates.append((b, u, f"Text similarity ({sim:.2f}) with {u['sheet']} R{u['row']}"))
                break
    
    if not is_dup:
        intra_unique.append(b)

print(f"Intra-new duplicates removed: {len(intra_duplicates)}")
print(f"Unique new genuine activities: {len(intra_unique)}")

# Now let's see: how many total activities will we have?
print(f"\nExisting activities (Sheet 1 + Sheet 2): {len(existing_activities)}")
print(f"New unique activities to add: {len(intra_unique)}")
print(f"Total Combined Master Activities: {len(existing_activities) + len(intra_unique)}")

# Let's inspect the duplicates removed between the new sheets
print("\n--- Sample of Duplicates between New Sheets ---")
for b, u, reason in intra_duplicates[:15]:
    print(f"DUP: [{b['sheet']} R{b['row']}] '{b['desc'][:50]}' <--> [{u['sheet']} R{u['row']}] ({reason})")
