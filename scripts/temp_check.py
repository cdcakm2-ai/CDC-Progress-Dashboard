import re, json

with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read(150000)

m = re.search(r'"monthlyProgress":\s*(\[[\s\S]*?\n\s*\])', text)
if m:
    data = json.loads(m.group(1))
    print("Found monthlyProgress rows:", len(data))
    for r in data:
        print(r)
else:
    print("Could not find monthlyProgress")
