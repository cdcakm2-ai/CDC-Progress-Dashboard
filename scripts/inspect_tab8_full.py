with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-status"')
# find next view-content
idx2 = text.find('<div class="view-content"', idx + 20)
if idx2 == -1:
    idx2 = text.find('</main>', idx)
print(f"view-status length: {idx2 - idx}")
print(text[idx:idx2])
