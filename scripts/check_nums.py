with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['383', '343', '173']):
        print(f"L{i+1}: {l.rstrip()}")
