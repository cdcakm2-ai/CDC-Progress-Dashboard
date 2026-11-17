import re

with open('raw_drive_data/new_imports/nw_docx_extracted.txt', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

docx_entries = []
current_gn = ""

for line in lines:
    # Match GN header, e.g. "1. 109 /ඊ අඹගහවිල වසම" or "20. 133/සී නාගහවත්ත වසම"
    m_gn = re.match(r'^\d+\.\s*([0-9]+[^\n]+?)\s*වසම\s*$', line)
    if m_gn:
        current_gn = m_gn.group(1).strip()
        continue
    
    # Match activity line: e.g. "පාසල් උපකරණ ප්‍රදානය - 2026-01-24 අඹගහවිල වසමේ අඩු ආදායම්ලාභී දරුවන් වෙත..."
    # Format: <Title> - <Date> <Description>
    m_act = re.match(r'^([^-]+?)\s*-\s*(\d{4}-\d{2}-\d{2})\s*(.*)$', line)
    if m_act:
        title = m_act.group(1).strip()
        date = m_act.group(2).strip()
        desc = m_act.group(3).strip()
        docx_entries.append({
            'gn': current_gn,
            'title': title,
            'date': date,
            'desc': desc,
            'full_line': line
        })
    else:
        # Fallback if date is formatted differently or just title
        # Check if contains date
        m_date = re.search(r'(\d{4}-\d{2}-\d{2})', line)
        if m_date:
            parts = line.split(m_date.group(1))
            docx_entries.append({
                'gn': current_gn,
                'title': parts[0].replace('-', '').strip(),
                'date': m_date.group(1),
                'desc': parts[1].strip() if len(parts) > 1 else "",
                'full_line': line
            })

print(f"Total entries parsed from nw.docx: {len(docx_entries)}")
gn_counts = {}
for e in docx_entries:
    gn_counts[e['gn']] = gn_counts.get(e['gn'], 0) + 1

print(f"Total GN divisions in nw.docx: {len(gn_counts)}")
for gn, c in sorted(gn_counts.items()):
    print(f"  {gn}: {c} activities")
