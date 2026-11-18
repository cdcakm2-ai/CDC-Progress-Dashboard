import json

p = r'C:\Users\M.A.D.C.RATHNAYAKA\.gemini\antigravity\brain\a80b24a4-61f4-413c-8d3c-55d0d0c3b3b9\.system_generated\logs\transcript.jsonl'
with open(p, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('step_index') in [3, 4, 5]:
            print(f"=== Step {obj.get('step_index')} ===")
            print("Content:", (obj.get('content') or '')[:300])
            print("Thinking:", (obj.get('thinking') or '')[:300])
            if obj.get('tool_calls'):
                print("Tool calls:", obj.get('tool_calls'))
