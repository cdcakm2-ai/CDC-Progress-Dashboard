with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Add secretariatInfo: overview in PSS_DATA
target = "overview: {"
replacement = "overview: overview,\n  secretariatInfo: overview,"

# Check how overview is declared in PSS_DATA
idx = text.find("const PSS_DATA = {")
if idx != -1:
    idx_overview = text.find("overview:", idx)
    text = text[:idx_overview] + "overview: overview,\n  secretariatInfo: overview,\n  " + text[text.find("categories:", idx_overview):]
    with open('js/data.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added secretariatInfo alias in js/data.js")
else:
    print("Could not find PSS_DATA in js/data.js")
