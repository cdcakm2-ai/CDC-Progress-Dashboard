with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see the sidebar navigation
idx = text.find('class="nav-tab-btn"')
print(text[idx-100:idx+1500])
