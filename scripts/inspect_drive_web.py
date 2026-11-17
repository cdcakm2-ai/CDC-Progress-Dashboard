import urllib.request
import re
import json

url = 'https://drive.google.com/drive/folders/1jBY0y_QWiinEPXEpEU6OwesPmlIna33C?usp=sharing'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    print('HTML len:', len(html))
    with open('raw_drive_data/drive_folder_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Saved raw_drive_data/drive_folder_page.html')
except Exception as e:
    print('Error:', e)
