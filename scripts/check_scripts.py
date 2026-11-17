with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"][^>]*></script>', text)
print("Scripts found:")
for m in matches:
    print(" -", m)

print("\nLast 30 lines of index.html:")
lines = text.splitlines()
for l in lines[-30:]:
    print(l)
