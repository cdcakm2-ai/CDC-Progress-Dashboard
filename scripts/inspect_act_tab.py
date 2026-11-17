with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('renderActivitiesTab() {')
print("idx:", idx)
if idx != -1:
    print(text[idx:idx+2500])
