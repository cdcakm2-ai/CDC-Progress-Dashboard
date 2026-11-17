import json

with open(r'C:\Users\M.A.D.C.RATHNAYAKA\.gemini\antigravity\brain\f9b6cbbc-715b-41df-835c-8b0b109c2abd\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('step_index') in [1, 2, 3]:
            print(f"=== Step {obj.get('step_index')} ===")
            print("Content:", (obj.get('content') or '')[:300])
            print("Thinking:", (obj.get('thinking') or '')[:300])
            print("Tool calls:", obj.get('tool_calls'))
