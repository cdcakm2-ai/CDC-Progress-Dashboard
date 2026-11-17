with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

replacements = [
    ('sec.totalBeneficiaries.toLocaleString()', '(sec.totalBeneficiaries || 0).toLocaleString()'),
    ('totalBeneficiaries.toLocaleString()', '(totalBeneficiaries || 0).toLocaleString()'),
    ('totalBen.toLocaleString()', '(totalBen || 0).toLocaleString()'),
    ('cBen.toLocaleString()', '(cBen || 0).toLocaleString()'),
    ('cSpent.toLocaleString()', '(cSpent || 0).toLocaleString()'),
]

for orig, rep in replacements:
    code = code.replace(orig, rep)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Safely guarded all remaining toLocaleString calls in js/app.js!")
