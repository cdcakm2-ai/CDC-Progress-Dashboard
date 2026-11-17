with open('js/charts.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace tooltip config
old_tooltip = '''  getTooltipConfig() {
    return {
      backgroundColor: "rgba(10, 18, 44, 0.96)",
      titleColor: "#38BDF8",
      bodyColor: "#F8FAFC",
      borderColor: "rgba(56, 189, 248, 0.4)",
      borderWidth: 1.5,
      padding: 12,
      cornerRadius: 10,
      titleFont: { family: this.defaultFont, size: 12.5, weight: "700" },
      bodyFont: { family: this.defaultFont, size: 12 },
      usePointStyle: true,
      boxPadding: 6
    };
  }'''

new_tooltip = '''  getTooltipConfig() {
    return {
      backgroundColor: "#FFFFFF",
      titleColor: "#243B64",
      bodyColor: "#526078",
      borderColor: "#E5EAF2",
      borderWidth: 1.5,
      padding: 12,
      cornerRadius: 10,
      titleFont: { family: this.defaultFont, size: 12.5, weight: "700" },
      bodyFont: { family: this.defaultFont, size: 12 },
      usePointStyle: true,
      boxPadding: 6
    };
  }'''

text = text.replace(old_tooltip, new_tooltip)

# Replace palette
old_pal = '''    // 10-Color Curated Premium Palette
    this.palette = [
      "#2563EB", // Royal Blue
      "#0D9488", // Teal
      "#059669", // Emerald
      "#7C3AED", // Violet
      "#4F46E5", // Indigo
      "#0891B2", // Cyan
      "#D97706", // Amber
      "#EA580C", // Coral
      "#EC4899", // Pink
      "#8B5CF6"  // Purple
    ];'''

new_pal = '''    // Curated Premium Light Palette
    this.palette = [
      "#3979D6", // Primary Blue
      "#159C91", // Teal
      "#36A47A", // Emerald
      "#8B68CC", // Violet
      "#E69B51", // Soft Orange
      "#E16F83", // Coral
      "#243B64", // Deep Navy
      "#0891B2", // Cyan
      "#F59E0B", // Amber
      "#6366F1"  // Indigo
    ];'''

text = text.replace(old_pal, new_pal)

# Replace grid lines and dark text
text = text.replace('"rgba(255, 255, 255, 0.05)"', '"#E5EAF2"')
text = text.replace('"rgba(255, 255, 255, 0.06)"', '"#E5EAF2"')
text = text.replace('"rgba(255, 255, 255, 0.08)"', '"#E5EAF2"')
text = text.replace('"rgba(10, 18, 44, 0.95)"', '"#FFFFFF"')
text = text.replace('color: "#E2E8F0"', 'color: "#526078"')
text = text.replace('color: "#F8FAFC"', 'color: "#243B64"')
text = text.replace('color: "#CBD5E1"', 'color: "#526078"')
text = text.replace('color: "#94A3B8"', 'color: "#8793A6"')

with open('js/charts.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated js/charts.js successfully with Light Theme parameters!")
