import json

with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'window.PSS_DATA = '
start = text.find(prefix) + len(prefix)
end = text.find(';\n\nif (typeof module')
data = json.loads(text[start:end])

acts = data.get('activities', [])
print(f"Total authentic activities: {len(acts)}")

# Check duplicate IDs or duplicate (gn, date, title)
seen_keys = set()
dupes = 0
for a in acts:
    key = (a.get('gnNameSi'), a.get('date'), a.get('titleSi', '')[:30])
    if key in seen_keys:
        dupes += 1
        print("Duplicate found:", key)
    seen_keys.add(key)

print(f"Duplicates found among 442: {dupes}")

# Check total photos
total_photos = sum(len(a.get('images', [])) for a in acts)
print(f"Total photos attached across activities: {total_photos}")

# Check GN divisions distribution
gn_counts = {}
for a in acts:
    gn = a.get('gnNameSi', 'Unknown')
    gn_counts[gn] = gn_counts.get(gn, 0) + 1

print(f"Distinct reporting GN divisions: {len(gn_counts)}")

# Check for any empty activities or missing descriptions
missing_desc = [a['id'] for a in acts if not (a.get('titleSi') or a.get('description'))]
print(f"Activities with missing description: {len(missing_desc)}")
