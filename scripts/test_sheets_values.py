import urllib.request
import urllib.error
import json

API_KEY = "AQ.Ab8RN6KKciiwuasDRLkBi3E6iiFCDZc_-ytLnhJzSScA1UGTdw"
SHEET_ID = "1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk"

url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/Form%20Responses%201?key={API_KEY}"
print("Testing values endpoint:", url)
try:
    with urllib.request.urlopen(url) as resp:
        print("Success:", resp.status)
        data = json.loads(resp.read().decode('utf-8'))
        print("Rows returned:", len(data.get('values', [])))
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.read().decode('utf-8')[:300]}")
except Exception as e:
    print("Error:", e)
