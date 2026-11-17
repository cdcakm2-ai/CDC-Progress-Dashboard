with open('js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== Scanning js/app.js for financial terms ===")
for idx, line in enumerate(lines, 1):
    if any(k in line for k in ['spentLKR', 'budgetLKR', 'යෙදවූ මුදල', 'වියදම (රු.)', 'මුදල (රු.)', 'මුළු වියදම']):
        print(f"{idx}: {line.strip()[:100]}")
