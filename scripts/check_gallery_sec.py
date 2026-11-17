with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-gallery"')
print("idx:", idx)
if idx != -1:
    end_idx = text.find('</section>', idx)
    print(text[idx-30:end_idx+10])
