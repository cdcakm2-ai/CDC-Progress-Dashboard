import urllib.request
import base64
import json

email = "akmeemana.praja.gov@gmail.com"
password = "AkmeemanaPraja2026Secure!"

auth = base64.b64encode(f"{email}:{password}".encode()).decode()
req = urllib.request.Request(
    "https://netlib.surge.sh/token",
    headers={
        "Authorization": f"Basic {auth}",
        "User-Agent": "surge/0.23.0"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        token = resp.read().decode().strip()
        print("Obtained SURGE_TOKEN successfully:", token[:10] + "...")
        with open("scripts/surge_token.txt", "w") as tf:
            tf.write(token)
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
except Exception as e:
    print("Error:", e)
