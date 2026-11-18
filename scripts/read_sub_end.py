import json

p = r'C:\Users\M.A.D.C.RATHNAYAKA\.gemini\antigravity\brain\67cc64c8-3759-427f-9f0a-69735f6cc585\.system_generated\logs\transcript.jsonl'
with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for l in lines[-5:]:
    obj = json.loads(l)
    print(f"=== Step {obj.get('step_index')} ===")
    print("Content:", (obj.get('content') or '')[:250])
    print("Thinking:", (obj.get('thinking') or '')[:250])
    if obj.get('tool_calls'):
        print("Tool calls:", obj.get('tool_calls'))
