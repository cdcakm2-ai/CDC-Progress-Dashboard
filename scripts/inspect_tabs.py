with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'<button[^>]*data-tab="([^"]+)"[^>]*>([\s\S]*?)</button>', text)
for m in matches:
    clean_label = re.sub(r'<[^>]+>', ' ', m.group(2)).strip()
    print(f"data-tab: '{m.group(1)}' -> {clean_label}")
