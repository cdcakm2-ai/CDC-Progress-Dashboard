import json

p = r'C:\Users\M.A.D.C.RATHNAYAKA\.gemini\antigravity\brain\f9b6cbbc-715b-41df-835c-8b0b109c2abd\browser_sandbox\outputs\step_69.json'
with open(p, 'r', encoding='utf-8') as f:
    d = json.load(f)

print(json.dumps(d, indent=2))
