with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. window.scrollTo safe
code = code.replace(
    'window.scrollTo({ top: 0, behavior: "smooth" });',
    'if (typeof window !== "undefined" && typeof window.scrollTo === "function") { window.scrollTo({ top: 0, behavior: "smooth" }); }'
)

# 2. activePill.scrollIntoView safe
code = code.replace(
    'if (activePill) {',
    'if (activePill && typeof activePill.scrollIntoView === "function") {'
)

# 3. catSelect.options safe
code = code.replace(
    'if (catSelect && catSelect.options.length <= 1) {',
    'if (catSelect && catSelect.options && catSelect.options.length <= 1) {'
)

# 4. actSelect.options safe
code = code.replace(
    'if (actSelect && actSelect.options.length === 0) {',
    'if (actSelect && actSelect.options && actSelect.options.length === 0) {'
)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Second patch applied successfully!")
