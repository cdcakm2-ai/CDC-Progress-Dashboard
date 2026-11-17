import urllib.request
import os
import re

os.makedirs('raw_drive_data/new_imports', exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

files = [
    ('1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk', 'sheet_main_responses'),
    ('1H_bwTOUUGj_cpIZKfBxs74Omt0xIgtTVeWhaRA3G7WI', 'sheet_august_copy_copy'),
    ('1hpi6sILX89-6WVCEOvopcb5MdfndJz6DK4LbnqzmP0g', 'sheet_august_copy'),
    ('1zZFmJvE_TVQUXU7XtrTPEBhM6jzpd6stlj2Feyt6-Nk', 'sheet_monthly_responses'),
    ('1U0pyKHbVHDFyOwW82hhXA4pNC4dYZ4Cp7a5t0IMujuw', 'sheet_officers_monthly_responses'),
]

# 1. Download XLSX for each spreadsheet so we have ALL sheets and ALL tabs
for sid, name in files:
    xlsx_url = f'https://docs.google.com/spreadsheets/d/{sid}/export?format=xlsx'
    dest = f'raw_drive_data/new_imports/{name}.xlsx'
    print(f"Downloading {name} as XLSX from {xlsx_url}...")
    try:
        req = urllib.request.Request(xlsx_url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(dest, 'wb') as out:
            out.write(resp.read())
        print(f"  -> Saved {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"  -> Error downloading XLSX for {name}: {e}")

# 2. Download the Word DOCX file: 17TwjFeActCnIZgpaLq4S4DjimJ6A1xIK
docx_urls = [
    'https://drive.google.com/uc?export=download&id=17TwjFeActCnIZgpaLq4S4DjimJ6A1xIK',
    'https://docs.google.com/document/d/17TwjFeActCnIZgpaLq4S4DjimJ6A1xIK/export?format=docx'
]
docx_dest = 'raw_drive_data/new_imports/nw.docx'
for durl in docx_urls:
    print(f"Attempting download of nw.docx from {durl}...")
    try:
        req = urllib.request.Request(durl, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(docx_dest, 'wb') as out:
                    out.write(data)
                print(f"  -> Successfully saved {docx_dest} ({len(data)} bytes)")
                break
            else:
                print(f"  -> Response too small ({len(data)} bytes), possibly HTML confirmation page")
    except Exception as e:
        print(f"  -> Error: {e}")
