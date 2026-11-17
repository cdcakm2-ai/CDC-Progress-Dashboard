with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    ('<div class="kpi-value gold-text-gradient" id="anKpiTotalActs">383</div>',
     '<div class="kpi-value gold-text-gradient" id="anKpiTotalActs">287</div>'),
    ('<div class="kpi-value" id="anKpiActiveDays" style="color: #38BDF8;">173</div>',
     '<div class="kpi-value" id="anKpiActiveDays" style="color: #38BDF8;">115</div>'),
    ('<div class="kpi-subtext">දින 173 ක් පුරා සක්‍රියයි</div>',
     '<div class="kpi-subtext">දින 115 ක් පුරා සක්‍රියයි</div>'),
    ('<span class="glass-badge blue">වැඩසටහන් 383 දක්වා</span>',
     '<span class="glass-badge blue">වැඩසටහන් 287 දක්වා</span>'),
    ('අගෝස්තු දක්වා සමුච්චිතව වැඩසටහන් 343 ක්ද, සැප්තැම්බර් මාසයේ වැඩසටහන් 40 ක්ද වශයෙන් සමස්ත වැඩසටහන් 383 සම්පූර්ණ වී ඇත.',
     'Google Drive දත්ත පත්‍රිකා 2 මගින් තහවුරු කළ අනන්‍ය වැඩසටහන් 287 ක් අක්මීමන වසම් 51 ක් පුරා සාර්ථකව පවත්වා ඇත.'),
    ('දින 173 ක් පුරා වැඩසටහන් 383 ක් පවත්වා ඇති අතර සාමාන්‍යයක් ලෙස එක් සක්‍රිය දිනයකදී වැඩසටහන් 2.21 ක් ක්‍රියාත්මක වී ඇත.',
     'දින 115 ක් පුරා වැඩසටහන් 287 ක් පවත්වා ඇති අතර සාමාන්‍යයක් ලෙස එක් සක්‍රිය දිනයකදී වැඩසටහන් 2.50 ක් ක්‍රියාත්මක වී ඇත.'),
    ('<div style="font-size: 1.4rem; font-weight: 800; color: #67E8F9;">දින 173 ක්</div>',
     '<div style="font-size: 1.4rem; font-weight: 800; color: #67E8F9;">දින 115 ක්</div>'),
    ('මාස 11 තුළ සක්‍රිය වූ දින 173 හි වැඩසටහන් සාන්ද්‍රණය',
     'වාර්තාකරණ කාලසීමාව තුළ සක්‍රිය වූ දින 115 හි වැඩසටහන් සාන්ද්‍රණය')
]

for orig, rep in replacements:
    if orig in text:
        text = text.replace(orig, rep)
        print(f"Replaced: {orig[:40]}...")
    else:
        print(f"NOT FOUND: {orig[:40]}...")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated index.html with real Google Drive figures!")
