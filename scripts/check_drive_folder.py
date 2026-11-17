import urllib.request
import re

url = 'https://drive.google.com/drive/folders/1jBY0y_QWiinEPXEpEU6OwesPmlIna33C?usp=sharing'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print('Folder loaded, length:', len(html))
        # Find Google Sheet links or file names
        sheet_ids = set(re.findall(r'1[a-zA-Z0-9_-]{30,}', html))
        print('Found candidate IDs:', len(sheet_ids))
        for s in sheet_ids:
            print(s)
except Exception as e:
    print('Error:', e)
