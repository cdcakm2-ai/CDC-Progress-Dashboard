import json

p = r'C:\Users\M.A.D.C.RATHNAYAKA\.gemini\antigravity\brain\a80b24a4-61f4-413c-8d3c-55d0d0c3b3b9\.system_generated\logs\transcript.jsonl'
with open(p, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('step_index') == 4:
            print(obj.get('content'))
