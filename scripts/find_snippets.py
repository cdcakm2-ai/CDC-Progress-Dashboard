import re

with open('raw_drive_data/drive_folder_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for the titles found and print their surrounding 500 characters
queries = ['nw.docx', 'අගෝස්තු', 'ජූනි', 'ජූලි', 'Responses', 'Google Sheets']
for q in queries:
    print(f"\n==================== QUERY: {q} ====================")
    for m in re.finditer(re.escape(q), html):
        start = max(0, m.start() - 300)
        end = min(len(html), m.end() + 300)
        snippet = html[start:end]
        print("--- SNIPPET ---")
        print(snippet)
        print("----------------")
