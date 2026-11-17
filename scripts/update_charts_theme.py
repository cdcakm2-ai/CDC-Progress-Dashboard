with open('js/charts.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_tooltip = """  getTooltipConfig() {
    return {
      backgroundColor: "#FFFFFF",
      titleColor: "#243B64",
      bodyColor: "#526078",
      borderColor: "#E5EAF2",
      borderWidth: 1.5,"""

new_tooltip = """  getTooltipConfig() {
    return {
      backgroundColor: "rgba(15, 23, 42, 0.94)",
      titleColor: "#FFFFFF",
      bodyColor: "#CBD5E1",
      borderColor: "rgba(255, 255, 255, 0.15)",
      borderWidth: 1,"""

if old_tooltip in text:
    text = text.replace(old_tooltip, new_tooltip)
    print("Updated tooltip config")

text = text.replace('color: "#E5EAF2"', 'color: "rgba(255, 255, 255, 0.08)"')
text = text.replace('color: "#526078"', 'color: "#CBD5E1"')
text = text.replace('color: "#243B64"', 'color: "#FFFFFF"')
text = text.replace('color: "#8793A6"', 'color: "#94A3B8"')

with open('js/charts.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated charts.js successfully")
