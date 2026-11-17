# Patch js/app.js line 3700 with safe guard
with open('js/app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

target = """      heatmapData.forEach(d => {
        const mKey = d.date.substring(0, 7);
        if (!monthsMap[mKey]) monthsMap[mKey] = [];
        monthsMap[mKey].push(d);
      });"""

replacement = """      heatmapData.forEach(d => {
        const dStr = d.date || (d.monthKey ? d.monthKey + '-01' : null);
        if (!dStr) return;
        const mKey = dStr.substring(0, 7);
        if (!monthsMap[mKey]) monthsMap[mKey] = [];
        monthsMap[mKey].push({
          date: dStr,
          count: d.count || 1
        });
      });"""

if target in app_code:
    app_code = app_code.replace(target, replacement)
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(app_code)
    print("Successfully patched heatmapData loop in js/app.js!")
else:
    print("Target not found in js/app.js")
