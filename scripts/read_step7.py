import json

with open(r'C:\Users\M.A.D.C.RATHNAYAKA\.gemini\antigravity\brain\64d0fee9-dd61-491d-9da9-bf17723a52ba\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('step_index') in [6, 7]:
            print(f"=== Step {obj.get('step_index')} ===")
            print("Tool calls:", obj.get('tool_calls'))
