import json

with open(r'C:\Users\M.A.D.C.RATHNAYAKA\.gemini\antigravity\brain\f9b6cbbc-715b-41df-835c-8b0b109c2abd\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('step_index') == 94:
            print(obj.get('content'))
