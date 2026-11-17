import csv
import json
import re
from collections import defaultdict
from datetime import datetime

def clean_text(t):
    if not t:
        return ""
    # Normalize sinhala and spaces
    t = re.sub(r'[\r\n\t]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def parse_date(date_str):
    s = date_str.strip()
    if not s:
        return None
    s = s.replace('.', '/').replace('-', '/').replace(' ', '')
    parts = s.split('/')
    if len(parts) == 3:
        try:
            p0, p1, p2 = int(parts[0]), int(parts[1]), int(parts[2])
            if p2 >= 2000:
                day, month, year = p0, p1, p2
                if month > 12 and day <= 12:
                    day, month = month, day
                return f"{year:04d}-{month:02d}-{day:02d}"
            elif p0 >= 2000:
                year, month, day = p0, p1, p2
                return f"{year:04d}-{month:02d}-{day:02d}"
            elif p2 < 100:
                year = 2000 + p2
                day, month = p0, p1
                if month > 12 and day <= 12:
                    day, month = month, day
                return f"{year:04d}-{month:02d}-{day:02d}"
        except:
            return None
    return s

def extract_sheet(path, sheet_name):
    items = []
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        reader = list(csv.reader(f))
        for r_idx, row in enumerate(reader[1:], 1):
            if len(row) < 4:
                continue
            ts = row[0].strip()
            officer = row[1].strip()
            gn_raw = row[2].strip()
            claimed = row[3].strip()
            
            for b in range(8):
                d_idx = 4 + b * 4
                desc_idx = 5 + b * 4
                p_idx = 6 + b * 4
                if d_idx >= len(row) or desc_idx >= len(row):
                    break
                d = row[d_idx].strip()
                desc = row[desc_idx].strip()
                p = row[p_idx].strip() if p_idx < len(row) else ""
                
                if not d and not desc:
                    continue
                
                # Extract photo URLs/IDs
                photos = []
                f1 = re.findall(r'id=([a-zA-Z0-9_-]{15,})', p)
                f2 = re.findall(r'/d/([a-zA-Z0-9_-]{15,})', p)
                for fid in f1 + f2:
                    if fid not in photos:
                        photos.append(fid)
                
                items.append({
                    'sheet': sheet_name,
                    'row': r_idx,
                    'block': b + 1,
                    'timestamp': ts,
                    'officer': officer,
                    'gn_raw': gn_raw,
                    'date_raw': d,
                    'date_parsed': parse_date(d),
                    'desc': clean_text(desc),
                    'photos': photos
                })
    return items

s1 = extract_sheet('raw_drive_data/sheet1_form_responses_1.csv', 'Sheet 1')
s2 = extract_sheet('raw_drive_data/sheet2_form_responses_1.csv', 'Sheet 2')
all_items = s1 + s2
print(f"Total raw activity records: {len(all_items)} (Sheet 1: {len(s1)}, Sheet 2: {len(s2)})")

# Let's inspect deduplication group by group within each GN
# Group by normalized GN
def norm_gn_key(g):
    # remove extra spaces and slashes formatting
    s = re.sub(r'\s+', ' ', g).strip()
    # fix minor typos
    s = s.replace('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල')
    s = s.replace('ඉහලගොඩ බටහිර', 'ඉහළගොඩ බටහිර')
    return s

by_gn = defaultdict(list)
for item in all_items:
    by_gn[norm_gn_key(item['gn_raw'])].append(item)

print(f"Total unique GN divisions: {len(by_gn)}")

# For each GN, find duplicates:
canonical_list = []
duplicates_list = []

for gn, items in by_gn.items():
    # We compare items
    handled = set()
    for i in range(len(items)):
        if i in handled:
            continue
        item_a = items[i]
        dups_for_a = []
        
        for j in range(i + 1, len(items)):
            if j in handled:
                continue
            item_b = items[j]
            
            # Match condition:
            # 1. Same date or within 2 days AND similar description (or exact same description)
            # 2. Or same photo IDs
            p_a = set(item_a['photos'])
            p_b = set(item_b['photos'])
            
            is_dup = False
            match_reason = ""
            
            # Exact photos match
            if p_a and p_b and (p_a == p_b or len(p_a.intersection(p_b)) >= 1):
                is_dup = True
                match_reason = "සමාන ඡායාරූප (Same photo links)"
            # Exact description match
            elif item_a['desc'].lower() == item_b['desc'].lower():
                is_dup = True
                match_reason = "සර්වසම විස්තරය (Identical description)"
            # Similar description on same date
            elif item_a['date_parsed'] and item_a['date_parsed'] == item_b['date_parsed']:
                # check description word overlap or substring
                da = item_a['desc'].lower()
                db = item_b['desc'].lower()
                if da in db or db in da:
                    is_dup = True
                    match_reason = "එකම දිනය හා සමාන විස්තරය (Same date & substring desc)"
                else:
                    # check significant common words
                    words_a = set(da.split())
                    words_b = set(db.split())
                    common = words_a.intersection(words_b)
                    if len(common) >= 2 and len(common) / min(len(words_a), len(words_b)) >= 0.5:
                        is_dup = True
                        match_reason = "එකම දිනය හා සමාන කාර්යය (Same date & matching keywords)"
            # Same activity resubmitted on adjacent date (e.g. 12/04 vs 13/04 for cricket match)
            elif item_a['desc'] and item_b['desc']:
                da = item_a['desc'].lower()
                db = item_b['desc'].lower()
                # Cricket match in Atambagasmulla
                if "ක්‍රිකට්" in da and "ක්‍රිකට්" in db:
                    is_dup = True
                    match_reason = "ක්‍රිකට් තරගාවලිය නැවත ඇතුළත් කිරීම"
                elif "බක් මහ" in da and "බක්මහ" in db:
                    is_dup = True
                    match_reason = "බක්මහ උළෙල නැවත ඇතුළත් කිරීම"
                elif "පහන්" in da and "පහන්" in db and "පූජා" in da and "පූජා" in db:
                    is_dup = True
                    match_reason = "පහන් පූජාව නැවත ඇතුළත් කිරීම"
                elif "පාන්" in da and "පාන්" in db and "දන්සල" in da and "දන්සල" in db:
                    is_dup = True
                    match_reason = "පාන් දන්සල නැවත ඇතුළත් කිරීම"
                elif "ඉටිපන්දම්" in da and "ඉටිපන්දම්" in db:
                    is_dup = True
                    match_reason = "ඉටිපන්දම් පුහුණුව නැවත ඇතුළත් කිරීම"
                    
            if is_dup:
                dups_for_a.append((item_b, match_reason))
                handled.add(j)
                
        # Merge photo links from duplicates into canonical
        all_photos = list(dict.fromkeys(item_a['photos'] + [p for dup, _ in dups_for_a for p in dup['photos']]))
        # Prefer the longer/more detailed description
        best_desc = item_a['desc']
        for dup, _ in dups_for_a:
            if len(dup['desc']) > len(best_desc):
                best_desc = dup['desc']
                
        canonical_item = dict(item_a)
        canonical_item['desc'] = best_desc
        canonical_item['photos'] = all_photos
        canonical_item['duplicates'] = dups_for_a
        canonical_list.append(canonical_item)
        
        for dup, reason in dups_for_a:
            duplicates_list.append({
                'gn': gn,
                'canonical': item_a,
                'duplicate': dup,
                'reason': reason
            })

print(f"\n==========================================")
print(f"Total Canonical Unique Activities: {len(canonical_list)}")
print(f"Total Duplicates Filtered: {len(duplicates_list)}")
print(f"==========================================")
print(f"\nDuplicates List ({len(duplicates_list)} items):")
for i, d in enumerate(duplicates_list, 1):
    can = d['canonical']
    dup = d['duplicate']
    print(f"{i}. GN: '{d['gn']}' | Reason: {d['reason']}")
    print(f"   Original: [{can['sheet']} R{can['row']} B{can['block']}] Date: {can['date_raw']} | Desc: {can['desc'][:50]}")
    print(f"   Duplicate: [{dup['sheet']} R{dup['row']} B{dup['block']}] Date: {dup['date_raw']} | Desc: {dup['desc'][:50]}")
