import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="sidebar-nav"')
if idx != -1:
    end_idx = text.find('</nav>', idx)
    print(text[idx-20:end_idx+6])
