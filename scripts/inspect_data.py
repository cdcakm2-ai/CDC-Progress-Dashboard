import json

with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'window.PSS_DATA = '
start = text.find(prefix) + len(prefix)
end = text.find(';\n\nif (typeof module')
json_str = text[start:end]
data = json.loads(json_str)

print("Total activities:", len(data.get("activities", [])))
print("Total gnDivisions:", len(data.get("gnDivisions", [])))
print("Data audits:", data.get("dataAudits", {}))

print("\nMonthly progress:")
for m in data.get("monthlyProgress", []):
    print(m)

print("\nGN Division sample:")
print(data.get("gnDivisions", [])[0])
