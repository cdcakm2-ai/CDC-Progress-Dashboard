import re
import json

with open('raw_drive_data/drive_folder_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for JSON arrays or file metadata in html
# In Google Drive folder html, files often appear in data-initial-data or embedded arrays:
# e.g., ["id", "title", mimeType, ...] or similar
print("Searching for file names...")
# Find common file patterns
names = re.findall(r'[\w\s\(\)\-\./_]{3,100}\.(?:xlsx|docx|doc|csv|pdf|png|jpg|pptx)', html, re.IGNORECASE)
print("File names found by extension:", set(names))

# Also search for Sinhala text or words like June, July, August, Form, Responses
keywords = ['June', 'July', 'August', 'ජූනි', 'ජූලි', 'අගෝස්තු', 'Word', 'Doc', 'docx', 'Sheet', 'Calc', 'Form']
for kw in keywords:
    matches = re.findall(r'[^"\'\[\]<>\\]{0,50}' + re.escape(kw) + r'[^"\'\[\]<>\\]{0,50}', html, re.IGNORECASE)
    if matches:
        print(f"Keyword '{kw}' matches (top 10):", list(set(matches))[:10])

# Search for Google Drive IDs (25-45 alphanumeric characters with _ and -)
# Usually paired with title
items = re.findall(r'\[\"([a-zA-Z0-9_-]{28,40})\"\,\[\"([^\"]+)\"', html)
print(f"Items found with [id, [title]]: {len(items)}")
for it in items[:30]:
    print(it)

# Also check for Drive folder items structure: ["id", "title", ...]
# Let's search for all file items in the raw JS objects
files_found = set()
for match in re.finditer(r'\"([a-zA-Z0-9_-]{28,45})\"[,\s]+\[\"([^\"]+)\"', html):
    files_found.add((match.group(1), match.group(2)))
for match in re.finditer(r'\[\"([a-zA-Z0-9_-]{28,45})\"[,\s]+\"([^\"]{3,80})\"', html):
    files_found.add((match.group(1), match.group(2)))

print(f"Total candidate files found: {len(files_found)}")
for fid, name in sorted(files_found, key=lambda x: x[1]):
    if any(term in name.lower() for term in ['june', 'july', 'august', 'sheet', 'doc', 'form', 'response', 'cdc', 'ප්‍රජා', 'සභාව', '2026', '2025']):
        print(f"  -> ID: {fid} | Name: {name}")
