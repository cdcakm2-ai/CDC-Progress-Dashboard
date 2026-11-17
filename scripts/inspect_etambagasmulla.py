import json

with open('raw_drive_data/canonical_v5.json', encoding='utf-8') as f:
    d = json.load(f)

etamba = [a for a in d['activities'] if 'ඇටඹගස්' in a['gnNameSi']]
print(f"Total in Etambagasmulla: {len(etamba)}\n")
for i, a in enumerate(etamba):
    print(f"[{i+1}] ID: {a['id']} | Date: {a['date']} (Raw: {a.get('dateRaw')}) | Title: {a['titleSi']} | Photos: {len(a.get('images', []))}")
    print(f"    Desc: {a['description']}")
    print(f"    Source: {a.get('source')}")
    print(f"    Image URLs/IDs: {a.get('images', [])}")
    print("-" * 80)
