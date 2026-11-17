import re
with open('js/charts.js', encoding='utf-8') as f:
    text = f.read()

ids = set(re.findall(r'getElementById\(["\']([a-zA-Z0-9_-]+)["\']\)', text))
for i in sorted(ids):
    print(i)
