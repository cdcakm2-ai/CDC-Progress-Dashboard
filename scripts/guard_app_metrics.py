import re

# 1. Update scripts/build_canonical_dataset.py
with open('scripts/build_canonical_dataset.py', 'r', encoding='utf-8') as f:
    build_code = f.read()

# Add budgetLKR, spentLKR, progress to gn_divisions_real
target_active = """            'statusBadge': 'සම්පූර්ණයි',
            'isReported': True
        })"""

replacement_active = """            'budgetLKR': 0,
            'spentLKR': 0,
            'progress': 100,
            'statusBadge': 'සම්පූර්ණයි',
            'isReported': True
        })"""

target_pending = """            'statusBadge': 'වාර්තා අපේක්ෂිතයි',
            'isReported': False
        })"""

replacement_pending = """            'budgetLKR': 0,
            'spentLKR': 0,
            'progress': 0,
            'statusBadge': 'වාර්තා අපේක්ෂිතයි',
            'isReported': False
        })"""

if target_active in build_code:
    build_code = build_code.replace(target_active, replacement_active)
if target_pending in build_code:
    build_code = build_code.replace(target_pending, replacement_pending)

with open('scripts/build_canonical_dataset.py', 'w', encoding='utf-8') as f:
    f.write(build_code)

print("Updated build_canonical_dataset.py with budgetLKR, spentLKR, progress.")

# 2. Comprehensive guard for toLocaleString in js/app.js
with open('js/app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

# Replace unguarded .toLocaleString() on property accesses like:
# gn.budgetLKR.toLocaleString() -> (gn.budgetLKR || 0).toLocaleString()
# gn.spentLKR.toLocaleString() -> (gn.spentLKR || 0).toLocaleString()
# gn.beneficiaries.toLocaleString() -> (gn.beneficiaries || 0).toLocaleString()
# act.budgetLKR.toLocaleString() -> (act.budgetLKR || 0).toLocaleString()
# act.spentLKR.toLocaleString() -> (act.spentLKR || 0).toLocaleString()
# g.budgetLKR.toLocaleString() -> (g.budgetLKR || 0).toLocaleString()
# g.spentLKR.toLocaleString() -> (g.spentLKR || 0).toLocaleString()
# g.beneficiaries.toLocaleString() -> (g.beneficiaries || 0).toLocaleString()
# m.spentLKR.toLocaleString() -> (m.spentLKR || 0).toLocaleString()
# m.cumulativeSpent.toLocaleString() -> (m.cumulativeSpent || 0).toLocaleString()
# s.spent.toLocaleString() -> (s.spent || 0).toLocaleString()
# s.beneficiaries.toLocaleString() -> (s.beneficiaries || 0).toLocaleString()

patterns = [
    (r'(\b[a-zA-Z0-9_]+\.(?:budgetLKR|spentLKR|beneficiaries|cumulativeSpent|spent|target))\s*\.\s*toLocaleString\(\)', r'(\1 || 0).toLocaleString()'),
    (r'\bgn\.(progress)\b(?!\s*!==|\s*===|\s*>|\s*<|\s*\?)', r'(gn.progress !== undefined ? gn.progress : (gn.totalProjects > 0 ? 100 : 0))'),
    (r'((?:gn|gnData|g)\.(?:spentLKR|budgetLKR))\s*/\s*1000000', r'(\1 || 0) / 1000000'),
]

for pat, rep in patterns:
    app_code = re.sub(pat, rep, app_code)

# Specifically fix lines 1056 & progress color calculation:
app_code = app_code.replace(
    'const progressVal = gn.progress;',
    'const progressVal = gn.progress !== undefined ? gn.progress : (gn.totalProjects > 0 ? 100 : 0);'
)
app_code = app_code.replace(
    'const pVal = gnData.progress;',
    'const pVal = gnData.progress !== undefined ? gnData.progress : (gnData.totalProjects > 0 ? 100 : 0);'
)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Safely guarded all metric properties and .toLocaleString() in js/app.js!")
