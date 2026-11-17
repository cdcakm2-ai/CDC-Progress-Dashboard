import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== Inline min-width ===")
for m in re.finditer(r'style="[^"]*min-width:\s*([^;"]+)', html):
    val = m.group(1).strip()
    print(f"min-width: {val} | line snippet: {html[max(0, m.start()-40):min(len(html), m.end()+40)].strip()}")

print("\n=== Tables in index.html ===")
for m in re.finditer(r'<table[^>]*>', html):
    print(m.group(0))

print("\n=== Elements with fixed px widths >= 360 ===")
for m in re.finditer(r'style="[^"]*width:\s*(\d{3,})px', html):
    w = int(m.group(1))
    if w >= 360:
        print(f"width: {w}px | line snippet: {html[max(0, m.start()-40):min(len(html), m.end()+40)].strip()}")
