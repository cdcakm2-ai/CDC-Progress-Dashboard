import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.findall(r'<section[^>]*id=["\']([^"\']+)["\']', text)
print(f"Total sections found: {len(sections)}")
for s in sections:
    print(f"  - {s}")
