"""
Gemini AI Integration for Google Drive & Sinhala CDC Text Processing
Uses Google Gemini API to parse unformatted documents, correct GN divisions, and verify duplicates.
"""

import os
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6KKciiwuasDRLkBi3E6iiFCDZc_-ytLnhJzSScA1UGTdw")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

def call_gemini(prompt_text):
    """Call Gemini 2.5 Flash with prompt text."""
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }

    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            return ""
    except Exception as e:
        print(f"Gemini API error: {e}")
        return ""

def test_connection():
    resp = call_gemini("Reply with 'CONNECTED' if you can read this message.")
    print("Gemini API connection test:", resp.strip())
    return "CONNECTED" in resp

if __name__ == "__main__":
    test_connection()
