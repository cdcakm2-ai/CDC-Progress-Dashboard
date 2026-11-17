import json

with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()
prefix = 'window.PSS_DATA = '
start = text.find(prefix) + len(prefix)
end = text.find(';\n\nif (typeof module')
data = json.loads(text[start:end])
acts = data['activities']

div_map = {}
for a in acts:
    div = a.get('gnNameSi')
    div_map.setdefault(div, []).append(a)

for div in ['113/බී නුගදූව', '133/සී නාගහවත්ත', '130 කැරැන්විල ජනපදය', '152 /බී තලහිටියාව']:
    print(f"=== {div} ({len(div_map.get(div, []))} activities) ===")
    for a in div_map.get(div, []):
        t = (a.get("title") or "")[:40]
        d = (a.get("description") or "")[:40]
        p_ids = [p['driveFileId'] for p in a.get('photos', [])]
        print(f"[{a['id']}] {a['date']} | Title: {t} | Photos: {len(p_ids)} {p_ids[:2]}")
