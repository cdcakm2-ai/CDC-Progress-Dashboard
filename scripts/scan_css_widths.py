import re

for css_name in ['css/style.css', 'css/glassmorphism.css', 'css/responsive.css']:
    with open(css_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n=== Scanning {css_name} ===")
    for m in re.finditer(r'([^{}]+\{[^{}]*min-width:\s*(\d{3,})px[^{}]*\})', content):
        selector_block = m.group(1).strip().replace('\n', ' ')
        px = int(m.group(2))
        if px > 320:
            print(f"min-width {px}px: {selector_block[:100]}")
    
    for m in re.finditer(r'([^{}]+\{[^{}]*width:\s*(\d{3,})px[^{}]*\})', content):
        selector_block = m.group(1).strip().replace('\n', ' ')
        px = int(m.group(2))
        if px > 380:
            print(f"width {px}px: {selector_block[:100]}")
