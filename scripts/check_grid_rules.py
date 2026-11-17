for fn in ['css/style.css', 'css/glassmorphism.css', 'css/responsive.css']:
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    for term in ['stats-grid-4', 'stat-card-3d', 'overview-latest-month']:
        idx = 0
        while True:
            idx = text.find(term, idx)
            if idx == -1: break
            snippet = text[max(0, idx-30):min(len(text), idx+120)].replace('\n', ' ')
            print(f"{fn} [{term}]: {snippet}")
            idx += len(term)
