with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(265, min(330, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")
