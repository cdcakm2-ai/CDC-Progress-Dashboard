import urllib.request
import urllib.error
import json

API_KEY = "AQ.Ab8RN6KKciiwuasDRLkBi3E6iiFCDZc_-ytLnhJzSScA1UGTdw"
FOLDER_ID = "1jBY0y_QWiinEPXEpEU6OwesPmlIna33C"
SHEET_ID = "1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk"

endpoints = [
    ("Drive API v3 (List files in folder)", f"https://www.googleapis.com/drive/v3/files?q='{FOLDER_ID}'+in+parents&key={API_KEY}"),
    ("Drive API v3 (Get folder metadata)", f"https://www.googleapis.com/drive/v3/files/{FOLDER_ID}?key={API_KEY}"),
    ("Sheets API v4 (Get Spreadsheet)", f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?key={API_KEY}"),
    ("Gemini Models API", f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}")
]

for name, url in endpoints:
    print(f"\n--- Testing {name} ---")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("SUCCESS! Status 200")
            print("Response preview:", str(data)[:300])
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        print(f"HTTPError {e.code}: {e.reason}")
        print("Error details:", err_body[:300])
    except Exception as e:
        print(f"Error: {e}")
