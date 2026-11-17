with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re, json
m = re.search(r'"monthlyProgress":\s*(\[\s*\{.*?\}\s*\])', text, re.DOTALL)
if not m:
    m = re.search(r'"monthlyProgress":\s*(\[.*?\])\s*,\s*"', text, re.DOTALL)

if m:
    data = json.loads(m.group(1))
    print(f"Total months: {len(data)}")
    for d in data:
        print(d)
else:
    print("Not matched")
