with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
keys = re.findall(r'^\s\s"([a-zA-Z0-9_]+)":', text, re.MULTILINE)
print("Top keys:", sorted(list(set(keys))))

# Check monthlyStats or monthlyProgress
m = re.findall(r'"month[a-zA-Z]*":', text)
print("Month keys:", set(m))
