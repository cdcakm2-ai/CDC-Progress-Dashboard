import csv
import json
import re
from collections import defaultdict

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s1_rows = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2_rows = list(csv.reader(f))

def clean_gn_name(g):
    s = re.sub(r'\s+', ' ', g).strip()
    s = s.replace('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල')
    s = s.replace('ඉහලගොඩ බටහිර', 'ඉහළගොඩ බටහිර')
    return s

all_acts = []

def parse_d(d_str):
    if not d_str: return ""
    d_clean = d_str.strip().replace('.', '/').replace('-', '/').replace(' ', '')
    p = d_clean.split('/')
    if len(p) == 3:
        try:
            p0, p1, p2 = int(p[0]), int(p[1]), int(p[2])
            if p2 >= 2000:
                if p1 > 12 and p0 <= 12: p0, p1 = p1, p0
                return f"{p2:04d}-{p1:02d}-{p0:02d}"
            elif p0 >= 2000:
                return f"{p0:04d}-{p1:02d}-{p2:02d}"
        except:
            pass
    return d_str.strip()

for s_name, rows in [("Sheet 1", s1_rows), ("Sheet 2", s2_rows)]:
    for r_idx, r in enumerate(rows[1:], 1):
        if len(r) < 4: continue
        gn = clean_gn_name(r[2])
        for b in range(8):
            col_d = 4 + b * 4
            col_desc = 5 + b * 4
            col_p = 6 + b * 4
            if col_d >= len(r) or col_desc >= len(r): break
            d = r[col_d].strip()
            desc = r[col_desc].strip()
            p = r[col_p].strip() if col_p < len(r) else ""
            if not d and not desc: continue
            
            photos = []
            f1 = re.findall(r'id=([a-zA-Z0-9_-]{15,})', p)
            f2 = re.findall(r'/d/([a-zA-Z0-9_-]{15,})', p)
            for fid in f1 + f2:
                if fid not in photos: photos.append(fid)
                
            all_acts.append({
                'id': f"{s_name[:2].upper()}-R{r_idx}-B{b+1}",
                'sheet': s_name,
                'row': r_idx,
                'block': b + 1,
                'gn': gn,
                'date_raw': d,
                'date': parse_d(d),
                'desc': desc.replace('\r\n', ' ').replace('\n', ' ').strip(),
                'photos': photos
            })

by_gn = defaultdict(list)
for a in all_acts:
    by_gn[a['gn']].append(a)

# Precise duplicate checking rules
canonical_acts = []
duplicates_log = []

for gn, items in by_gn.items():
    handled = set()
    for i in range(len(items)):
        if i in handled: continue
        it_a = items[i]
        dups = []
        for j in range(i + 1, len(items)):
            if j in handled: continue
            it_b = items[j]
            
            p_a = set(it_a['photos'])
            p_b = set(it_b['photos'])
            d_a = it_a['desc'].lower()
            d_b = it_b['desc'].lower()
            
            is_dup = False
            reason = ""
            
            # Rule 1: Exact photo overlap
            if p_a and p_b and (p_a == p_b or len(p_a.intersection(p_b)) >= 1):
                is_dup = True
                reason = "එකම ඡායාරූප (Same photo links)"
            # Rule 2: Exact same description
            elif d_a == d_b:
                is_dup = True
                reason = "සර්වසම විස්තරය (Exact description)"
            # Rule 3: Specific resubmitted activities in known GNs
            elif "109/ ජී ඇටඹගස්මුල්ල" in gn:
                if "ක්‍රිකට්" in d_a and "ක්‍රිකට්" in d_b:
                    is_dup = True; reason = "ක්‍රිකට් තරගාවලිය (Resubmitted cricket match)"
                elif ("බක්මහ" in d_a or "බක් මහ" in d_a) and ("බක්මහ" in d_b or "බක් මහ" in d_b):
                    is_dup = True; reason = "බක්මහ අවුරුදු උළෙල (Resubmitted Bakmaha festival)"
                elif "පහන්" in d_a and "පහන්" in d_b:
                    is_dup = True; reason = "පහන් පූජාව (Resubmitted pahan pooja)"
                elif "පාන්" in d_a and "පාන්" in d_b and "දන්සල" in d_a and "දන්සල" in d_b:
                    is_dup = True; reason = "පාන් දන්සල (Resubmitted bread dansala)"
                elif "ඩෙංගු" in d_a and "ඩෙංගු" in d_b and it_a['date'] == it_b['date']:
                    is_dup = True; reason = "2026-06-27 ඩෙංගු මර්දන වැඩසටහන (Resubmitted dengue program)"
            elif "155/ ඊ හියාරේ ඉහළ" in gn:
                if "ශ්‍රමදාන" in d_a and "ශ්‍රමදාන" in d_b and it_a['date'] == it_b['date']:
                    is_dup = True; reason = "2026-06-26 ශ්‍රමදාන වැඩසටහන (Resubmitted shramadana)"
                elif "15/07/2026" in it_a['date_raw'] and "15/07/2026" in it_b['date_raw']:
                    is_dup = True; reason = "2026-07-15 ප්‍රජා ශක්ති කමිටු වැඩසටහන (Resubmitted committee program)"
            elif "109/බී ඉහළගොඩ දකුණ" in gn:
                if "ඉටිපන්දම්" in d_a and "ඉටිපන්දම්" in d_b:
                    is_dup = True; reason = "2026-06-25 ඉටිපන්දම් පුහුණු වැඩසටහන (Resubmitted candle training)"
            elif "152 /බී තලහිටියාව" in gn:
                if "ඩෙංගු" in d_a and "ඩෙංගු" in d_b and "25/07/2026" in it_a['date_raw'] and "25/07/2026" in it_b['date_raw']:
                    is_dup = True; reason = "2026-07-25 ඩෙංගු මර්දනය ශ්‍රමදානය (Resubmitted dengue shramadana)"
            elif "133 /ඊ තල්පෙගොඩ" in gn:
                if "ඩෙංගු" in d_a and "ඩෙංගු" in d_b and "27/06/2026" in it_a['date_raw'] and "27/06/2026" in it_b['date_raw']:
                    is_dup = True; reason = "2026-06-27 ඩෙංගු දැනුවත් කිරීම (Resubmitted dengue awareness)"
            elif "133/සී නාගහවත්ත" in gn:
                if "dj" in d_a and "dj" in d_b and "05/09/2026" in it_a['date_raw'] and "05/09/2026" in it_b['date_raw']:
                    is_dup = True; reason = "2026-09-05 DJ සංගීත සැදෑව (Sheet 1 vs Sheet 2 duplicate)"
            elif "130/ ඊ අම්බලන්වත්ත" in gn:
                if ("කොණ්ඩා" in d_a or "කොන්ඩා" in d_a) and ("කොණ්ඩා" in d_b or "කොන්ඩා" in d_b) and it_a['date'] == it_b['date']:
                    is_dup = True; reason = "2026-09-12 රූපලාවන්‍ය හා කොණ්ඩා කැපීමේ වැඩසටහන (Sheet 1 vs Sheet 2 duplicate)"
                    
            if is_dup:
                dups.append((it_b, reason))
                handled.add(j)
                
        # Best desc
        best_desc = it_a['desc']
        for dup_item, _ in dups:
            if len(dup_item['desc']) > len(best_desc):
                best_desc = dup_item['desc']
        # Merged photos
        all_p = list(dict.fromkeys(it_a['photos'] + [p for d_it, _ in dups for p in d_it['photos']]))
        
        can_item = dict(it_a)
        can_item['desc'] = best_desc
        can_item['photos'] = all_p
        can_item['dup_count'] = len(dups)
        canonical_acts.append(can_item)
        
        for d_it, r_text in dups:
            duplicates_log.append({
                'gn': gn,
                'canonical': it_a,
                'dup': d_it,
                'reason': r_text
            })

print(f"\n==========================================")
print(f"Total Raw Activity Submissions: {len(all_acts)}")
print(f"Total Filtered Duplicates: {len(duplicates_log)}")
print(f"Total Canonical Unique Activities: {len(canonical_acts)}")
print(f"==========================================")
for i, d in enumerate(duplicates_log, 1):
    c = d['canonical']
    dup = d['dup']
    print(f"{i}. GN: '{d['gn']}' | Reason: {d['reason']}")
    print(f"   Original [{c['id']}] {c['date_raw']}: {c['desc'][:50]}")
    print(f"   Duplicate [{dup['id']}] {dup['date_raw']}: {dup['desc'][:50]}")
