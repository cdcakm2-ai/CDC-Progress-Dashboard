import urllib.request
import re

for s_id, s_name in [
    ("1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk", "Sheet 1"),
    ("1H_bwTOUUGj_cpIZKfBxs74Omt0xIgtTVeWhaRA3G7WI", "Sheet 2")
]:
    url = f"https://docs.google.com/spreadsheets/d/{s_id}/edit?usp=sharing"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for sheet tabs / names in bootstrap data
            sheets = re.findall(r'\[(\d+),\"([^\"]+)\",\d+,\d+\]', html)
            print(f"=== {s_name} tabs ===")
            for gid, name in sheets:
                print(f"  gid: {gid}, name: {name}")
            
            # Also find any other sheet names
            tabs = re.findall(r'\"name\":\"([^\"]+)\",\"sheetId\":(\d+)', html)
            for name, gid in tabs:
                print(f"  name: {name}, gid: {gid}")
    except Exception as e:
        print(f"Error for {s_name}: {e}")
