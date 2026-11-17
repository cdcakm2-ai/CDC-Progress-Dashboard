with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-status"')
end_idx = text.find('</div>\n      </div>', idx)
print(text[idx:idx+4000])
