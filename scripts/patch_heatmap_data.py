with open('scripts/generate_js_data.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """# Calendar Heatmap summary by month
heatmap_data = []
for ms in dataset['monthlyStats']:
    heatmap_data.append({
        "monthKey": ms['monthKey'],
        "monthSi": ms['monthSi'],
        "count": ms['count'],
        "activeDays": ms['activeDays'],
        "reportingDivisions": ms['reportingDivisions']
    })"""

replacement = """# Calendar Heatmap Data (Daily activity dates)
daily_counts = {}
for a in formatted_activities:
    d_str = a['date']
    if d_str and len(d_str) == 10 and int(d_str[:4]) <= 2026:
        daily_counts[d_str] = daily_counts.get(d_str, 0) + 1

heatmap_data = []
for d_str in sorted(daily_counts.keys()):
    heatmap_data.append({
        "date": d_str,
        "count": daily_counts[d_str]
    })"""

if target in code:
    code = code.replace(target, replacement)
    with open('scripts/generate_js_data.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully updated heatmap generation in generate_js_data.py!")
else:
    print("Target not found in generate_js_data.py")
