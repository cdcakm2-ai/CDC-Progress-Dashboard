with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. history.replaceState safe
code = code.replace(
    'history.replaceState(null, null, `#${tabId}`);',
    'if (typeof window !== "undefined" && window.history && typeof window.history.replaceState === "function") { window.history.replaceState(null, null, `#${tabId}`); }'
)

# 2. optgroup.children safe
code = code.replace(
    'if (optgroup.children.length > 0) {',
    'if (optgroup.children && optgroup.children.length > 0) {'
)

# 3. gnSelect.options safe
code = code.replace(
    'if (gnSelect && gnSelect.options.length <= 1) {',
    'if (gnSelect && gnSelect.options && gnSelect.options.length <= 1) {'
)

# 4. mSelect.options safe
code = code.replace(
    'if (mSelect && mSelect.options.length <= 1) {',
    'if (mSelect && mSelect.options && mSelect.options.length <= 1) {'
)

# 5. refreshBtn dataset safe
code = code.replace(
    'if (refreshBtn && !refreshBtn.dataset.bound) {',
    'if (refreshBtn && (!refreshBtn.dataset || !refreshBtn.dataset.bound)) {\n      if (refreshBtn.dataset) refreshBtn.dataset.bound = "true";'
)
code = code.replace(
    'refreshBtn.dataset.bound = "true";\n      refreshBtn.addEventListener',
    'refreshBtn.addEventListener'
)

# 6. window.addEventListener load in bootloader safe
code = code.replace(
    'window.addEventListener("load", bootApp);',
    'if (typeof window !== "undefined" && typeof window.addEventListener === "function") { window.addEventListener("load", bootApp); }'
)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("js/app.js defensive hardening complete!")
