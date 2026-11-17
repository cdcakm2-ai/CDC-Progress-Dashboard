import json

with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()
prefix = 'window.PSS_DATA = '
start = text.find(prefix) + len(prefix)
end = text.find(';\n\nif (typeof module')
data = json.loads(text[start:end])
acts = data['activities']

photo_owners = {}
shared = []
for a in acts:
    for p in a.get('photos', []):
        fid = p.get('driveFileId')
        if fid:
            if fid in photo_owners:
                shared.append((fid, photo_owners[fid], a['id']))
            else:
                photo_owners[fid] = a['id']

print(f"Total unique photos: {len(photo_owners)}")
print(f"Total shared photo collisions: {len(shared)}")
for s in shared[:5]:
    print("Shared:", s)
