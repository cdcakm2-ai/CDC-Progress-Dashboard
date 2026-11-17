import json

with open('raw_drive_data/canonical_v3.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

acts = d['activities']
print(f'Total activities: {len(acts)}')

corrections = {
    'සන්වර්දනය': 'සංවර්ධනය',
    'මර්ගය': 'මාර්ගය',
    'මර්ග': 'මාර්ග',
    'හල්ගස්මුඅල්ල': 'හල්ගස්මුල්ල',
    'වැඩසටහණ': 'වැඩසටහන',
    'පැවැත්වීඹ': 'පැවැත්වීම',
    'දැනුවත්කීරීම': 'දැනුවත් කිරීම',
    'කිරිම': 'කිරීම',
    'ශ්‍රමදානය්': 'ශ්‍රමදානය',
}

found = 0
for a in acts:
    for wrong, right in corrections.items():
        if wrong in a['titleSi'] or wrong in a['description']:
            found += 1
            print(f"{a['id']} ({a['gnNameSi']}): '{wrong}' -> '{right}' in {a['titleSi']}")
            break

print(f'Found {found} activities with fixable typos')
