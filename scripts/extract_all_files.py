import re
import json

with open('raw_drive_data/drive_folder_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern for file entries in Drive bootstrap:
# Look for pattern: [[null,"FILE_ID"],null,null,null,"MIME_TYPE", ... "TITLE"
matches = re.findall(r'\[\[null,\"([a-zA-Z0-9_-]{20,})\"\][^]]+?\"(application\/[^\"]+)\"[^]]+?\[\[\[\"([^\"]+)\"', html)
print(f"Direct matches count: {len(matches)}")
for m in matches:
    print("MATCH:", m)

# Let's search broadly for all IDs and titles
# In Drive HTML: ["ID", ["PARENT_ID"], "NAME", "MIME_TYPE"]
matches2 = re.findall(r'\[\"([a-zA-Z0-9_-]{25,45})\",\[\"([a-zA-Z0-9_-]{25,45})\"\],\"([^\"]+)\",\"([^\"]+)\"', html)
print(f"\nBroad matches count: {len(matches2)}")
for fid, parent, name, mime in matches2:
    print(f"File: ID={fid} | Parent={parent} | Name={name.encode('utf-8').decode('unicode_escape', 'ignore')} | Mime={mime}")

# Also find any other occurrences of filenames or Google Doc IDs
pattern = r'data-id=\"([a-zA-Z0-9_-]{25,45})\"[^>]*data-tooltip=\"([^\"]+)\"'
matches3 = re.findall(pattern, html)
print(f"\nDOM tooltip matches count: {len(matches3)}")
for fid, name in matches3:
    print(f"DOM: ID={fid} | Tooltip={name}")
