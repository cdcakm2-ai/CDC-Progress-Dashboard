"""
Single-run Google Drive Sync for Akmeemana CDC Progress Dashboard
Polls the authorized Google Drive folder and sheets once, detects new files or edits,
re-runs the advanced deduplication pipeline, and syncs dist.
"""

import time
import os
import sys
import hashlib
import subprocess
import urllib.request
import json
from datetime import datetime

DRIVE_FOLDER_ID = "1jBY0y_QWiinEPXEpEU6OwesPmlIna33C"

SHEETS = [
    ('1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk', 'sheet_main_responses'),
    ('1H_bwTOUUGj_cpIZKfBxs74Omt0xIgtTVeWhaRA3G7WI', 'sheet_august_copy_copy'),
    ('1hpi6sILX89-6WVCEOvopcb5MdfndJz6DK4LbnqzmP0g', 'sheet_august_copy'),
    ('1zZFmJvE_TVQUXU7XtrTPEBhM6jzpd6stlj2Feyt6-Nk', 'sheet_monthly_responses'),
    ('1U0pyKHbVHDFyOwW82hhXA4pNC4dYZ4Cp7a5t0IMujuw', 'sheet_officers_monthly_responses'),
]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def discover_drive_folder_sheets():
    folder_url = f"https://drive.google.com/embeddedfolderview?id={DRIVE_FOLDER_ID}"
    discovered_ids = []
    try:
        req = urllib.request.Request(folder_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        import re
        raw_ids = set(re.findall(r'id="entry-([a-zA-Z0-9_-]{25,})"', html) + 
                      re.findall(r'/spreadsheets/d/([a-zA-Z0-9_-]{25,})', html) +
                      re.findall(r'/file/d/([a-zA-Z0-9_-]{25,})', html))
        known_ids = {s[0] for s in SHEETS}
        for fid in raw_ids:
            if fid not in known_ids and fid != DRIVE_FOLDER_ID:
                discovered_ids.append(fid)
    except Exception as e:
        print(f"Discovery notice: {e}")
    return discovered_ids

def get_file_hash(filepath):
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def sync_once():
    changed = False
    os.makedirs('raw_drive_data/new_imports', exist_ok=True)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking Google Drive folder ({DRIVE_FOLDER_ID})...")
    
    # 1. Check for newly discovered sheets in Drive folder
    new_ids = discover_drive_folder_sheets()
    for nid in new_ids:
        export_url = f"https://docs.google.com/spreadsheets/d/{nid}/export?format=xlsx"
        final_path = f"raw_drive_data/new_imports/sheet_dynamic_{nid[:8]}.xlsx"
        if not os.path.exists(final_path):
            req = urllib.request.Request(export_url, headers=HEADERS)
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    content = resp.read()
                if content.startswith(b'PK\x03\x04'):
                    with open(final_path, 'wb') as out_f:
                        out_f.write(content)
                    SHEETS.append((nid, f"sheet_dynamic_{nid[:8]}"))
                    print(f" -> Found NEW Google Sheet: {nid}")
                    changed = True
            except Exception as dl_err:
                pass

    # 2. Check existing sheets for edits/updates
    for sid, name in SHEETS:
        dest = f'raw_drive_data/new_imports/{name}.xlsx'
        old_hash = get_file_hash(dest)
        url = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=xlsx'
        temp_dest = dest + '.tmp'
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp, open(temp_dest, 'wb') as out:
                out.write(resp.read())
            
            new_hash = get_file_hash(temp_dest)
            if new_hash != old_hash:
                os.replace(temp_dest, dest)
                print(f" -> Detected changes in {name}")
                changed = True
            else:
                if os.path.exists(temp_dest):
                    os.remove(temp_dest)
        except Exception as e:
            if os.path.exists(temp_dest):
                try: os.remove(temp_dest)
                except: pass

    if changed:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Re-running data compilation pipeline...")
        subprocess.run([sys.executable, 'scripts/export_all_xlsx_to_csv.py'], check=True)
        subprocess.run([sys.executable, 'scripts/generate_canonical_v10.py'], check=True)
        subprocess.run([sys.executable, 'scripts/export_canonical_v10_to_js.py'], check=True)
        subprocess.run([sys.executable, 'scripts/sync_dist.py'], check=True)
        
        version_data = {
            "version": int(time.time()),
            "lastSync": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "updated"
        }
        with open('data_version.json', 'w', encoding='utf-8') as f:
            json.dump(version_data, f, indent=2)
        print(" -> Pipeline finished! New version generated.")
        return True
    else:
        print(" -> Everything is up-to-date! No changes detected in Google Drive.")
        return False

if __name__ == '__main__':
    res = sync_once()
    sys.exit(0 if not res else 0)
