import urllib.request
import re

url = 'https://drive.google.com/embeddedfolderview?id=1jBY0y_QWiinEPXEpEU6OwesPmlIna33C'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    print('Fetched embeddedfolderview length:', len(html))
    ids = set(re.findall(r'id="entry-([a-zA-Z0-9_-]{25,})"', html) + 
              re.findall(r'/file/d/([a-zA-Z0-9_-]{25,})', html) + 
              re.findall(r'/spreadsheets/d/([a-zA-Z0-9_-]{25,})', html))
    print('Found IDs count:', len(ids))
    for i in ids:
        print(i)
except Exception as e:
    print('Error:', e)
