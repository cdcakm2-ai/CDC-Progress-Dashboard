import re

with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'const ALL_63_GN_DIVISIONS\s*=\s*(\[[\s\S]*?\n\]);', text)
if match:
    code = match.group(1)
    names = re.findall(r'"nameSi":\s*"([^"]+)"', code)
    print(f"Total GN divisions: {len(names)}")
    for i, n in enumerate(names, 1):
        print(f"{i}: {n}")
