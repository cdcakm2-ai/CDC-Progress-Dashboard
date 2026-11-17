import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.finditer(r'<section[^>]*id=["\']([^"\']+)["\'][^>]*>', text)
for m in matches:
    print(m.group(0))
