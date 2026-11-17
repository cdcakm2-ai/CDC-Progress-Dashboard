import csv
import json
import re
from collections import defaultdict
from datetime import datetime

# 1. Load both sheets
with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s1_rows = list(csv.reader(f))

with open('raw_drive_data/sheet2_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    s2_rows = list(csv.reader(f))

def clean_gn_name(g):
    s = re.sub(r'\s+', ' ', g).strip()
    s = s.replace('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල')
    s = s.replace('109 ඉහලගොඩ බටහිර', '109 ඉහළගොඩ බටහිර')
    s = s.replace('112/සී කිරින්ඳගොඩ', '112/සී කිරින්දගොඩ')
    return s

def clean_desc(d):
    s = re.sub(r'[\r\n\t]+', ' ', d)
    s = re.sub(r'\s+', ' ', s).strip()
    corrections = [
        ('සන්වර්දනය', 'සංවර්ධනය'),
        ('මර්ගය', 'මාර්ගය'),
        ('මර්ග', 'මාර්ග'),
        ('හල්ගස්මුඅල්ල', 'හල්ගස්මුල්ල'),
        ('වැඩසටහණ', 'වැඩසටහන'),
        ('පැවැත්වීඹ', 'පැවැත්වීම'),
        ('දැනුවත්කීරීම', 'දැනුවත් කිරීම'),
        ('කිරිම', 'කිරීම'),
        ('ශ්‍රමදානය්', 'ශ්‍රමදානය'),
        ('දර්මපාල', 'ධර්මපාල'),
        ('අතුරැමාර්ගයෙ', 'අතුරුමාර්ගයේ'),
        ('ඉදිකිරිම', 'ඉදිකිරීම'),
        ('ක්‍රිඩාංගනය', 'ක්‍රීඩාංගනය')
    ]
    for w, r in corrections:
        s = s.replace(w, r)
    return s

def parse_date(d_str):
    if not d_str: return "2026-08-01"
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
            elif p2 < 100:
                year = 2000 + p2
                if p1 > 12 and p0 <= 12: p0, p1 = p1, p0
                return f"{year:04d}-{p1:02d}-{p0:02d}"
        except:
            pass
    return d_str.strip()

CATEGORIES = [
    ("dengue", "ඩෙංගු මර්දන වැඩසටහන්", "#EF4444", "bi-shield-check", [
        "ඩෙංගු", "ඩෙන්ගු", "දිරාපත්", "කීට", "පරිශ්‍ර පරීක්ෂා", "දුමාර", "මදුරු"
    ]),
    ("environment", "පරිසර හා ශ්‍රමදාන", "#10B981", "bi-tree-fill", [
        "ශ්‍රමදාන", "පිරිසිදු", "කාණු", "පරිසර", "පැළ", "රුක් රෝපණ", "ගස්", "පිරිසිදුකිරීම", "ප්ලාස්ටික්", "කසල", "රුක්රෝපණ", "අත්තම", "සුසාන"
    ]),
    ("infrastructure", "යටිතල පහසුකම් සංවර්ධනය", "#3B82F6", "bi-building", [
        "මාර්ග", "මාගය", "පාර", "පාලම්", "ජල", "විදුලි", "ගොඩනැගිලි", "අලුත්වැඩියා", "කොන්ක්‍රීට්", "කොන්ක්‍රිට්", "බෝක්කු", "ගල්බැම්ම", "බැම්ම", "නල", "ළිං", "ප්‍රතිසංස්කරණ", "ප්‍රතිසංස්කරණය", "ඉදිකිරිම", "ඉදිකිරීම", "සොල්ලා", "ලයිට්", "වාරි", "අමුණ"
    ]),
    ("welfare", "සමාජ සුභසාධන වැඩසටහන්", "#EC4899", "bi-heart-pulse-fill", [
        "වැඩිහිටි", "ආධාර", "වියළි ආහාර", "වියලි", "උපකරණ", "නිවාස", "නිවස", "සුභසාධන", "විශේෂ අවශ්‍යතා", "සහනාධාර", "ආපදා", "විපතට", "ජංගම සේවය", "සත්කාර", "ප්‍රතිලාභ", "සනීපාරක්ෂක", "තමන්ගේම තැනක්"
    ]),
    ("agriculture", "කෘෂිකාර්මික හා ගෙවතු වගා", "#84CC16", "bi-flower1", [
        "ගෙවතු", "වගා", "බීජ", "පොහොර", "කෘෂි", "එළවළු", "පළතුරු", "බිම්මල්", "කොම්පෝස්ට්", "පැළ බෙදා", "පොකුරු ගම්මාන", "ධාන්‍ය", "ගම්මිරිස්", "තේ ගම්මාන", "පොල් වගාව"
    ]),
    ("health", "සෞඛ්‍ය හා වෛද්‍ය සායන", "#06B6D4", "bi-hospital-fill", [
        "සායන", "සෞඛ්‍ය", "වෛද්‍ය", "ලේ දන්දීමේ", "ලේ පරිත්‍යාග", "සුවනාරි", "දන්ත", "ඇස්", "පෝෂණ", "ඖෂධ", "සුව දිවිය"
    ]),
    ("livelihood", "ස්වයං රැකියා හා ජීවනෝපාය", "#F59E0B", "bi-briefcase-fill", [
        "ස්වයං රැකියා", "ස්වයංරැකියා", "ජීවනෝපාය", "පුහුණු", "පුහුනු", "මහන", "අත්කම්", "ආහාර නිෂ්පාදන", "ව්‍යවසායක", "ඉටිපන්දම්", "ඉටි පන්දම්", "රූපලාවන්‍ය", "රුපලාවනය", "කොණ්ඩ", "කොන්ඩ", "බාබර්", "කේක්", "මල් සැකසුම්", "විසිතුරු සතුන්", "පොල පැවැත්වීම", "සංචාරක සංගමය", "පොළ ආරම්භ", "අවුරුදු පොළ"
    ]),
    ("education", "අධ්‍යාපන, ළමා හා ක්‍රීඩා", "#8B5CF6", "bi-book-half", [
        "පෙරපාසල්", "පාසල්", "ළමා", "ළමුන්", "ක්‍රීඩා", "ක්‍රිකට්", "පොත්", "ශිෂ්‍ය", "පුස්තකාල", "දරු", "සංගීත", "චිත්‍ර", "නිපුණතා", "ශිෂ්‍යත්ව", "සිනමා", "චිත්‍රපට"
    ]),
    ("religious", "ආගමික හා සංස්කෘතික", "#D97706", "bi-stars", [
        "පෙරහැර", "බෝධි පූජා", "පිරිත්", "දාන", "දන්සල", "පන්සල්", "ආගමික", "සංස්කෘතික", "අවුරුදු", "බක්මහ", "වෙසක්", "පොසොන්", "පූජාව", "සැමරුම", "නිදහස් දින", "වෛශාක්‍ය", "පින්කම", "සෙත් පතා", "boodi puujaavak", "ඉෆ්තාර්", "DJ", "සංගීත සැදෑව"
    ]),
    ("awareness", "ප්‍රජා දැනුවත් කිරීම් හා ධාරිතා", "#6366F1", "bi-megaphone-fill", [
        "දැනුවත්", "සමිතිය", "රැස්වීම", "දේශන", "වැඩමුළු", "නීති", "මහජන", "ධාරිතා", "සාකච්ඡා", "කමිටු", "තොරතුරු දැනගැනීමේ", "ඵලදායිතා"
    ]),
]

def classify_activity(text):
    text_lower = text.lower()
    for cat_id, cat_name, color, icon, keywords in CATEGORIES:
        for kw in keywords:
            if kw in text_lower:
                return cat_id, cat_name, color, icon
    return "community", "ප්‍රජා සේවා හා සංවර්ධන", "#94A3B8", "bi-people-fill"

MONTH_NAMES = {
    "2025-11": "නොවැම්බර් 2025",
    "2025-12": "දෙසැම්බර් 2025",
    "2026-01": "ජනවාරි 2026",
    "2026-02": "පෙබරවාරි 2026",
    "2026-03": "මාර්තු 2026",
    "2026-04": "අප්‍රේල් 2026",
    "2026-05": "මැයි 2026",
    "2026-06": "ජූනි 2026",
    "2026-07": "ජූලි 2026",
    "2026-08": "අගෝස්තු 2026",
    "2026-09": "සැප්තැම්බර් 2026",
    "2026-10": "ඔක්තෝබර් 2026"
}

# Collect all 290 activities from both sheets
activities = []
act_id_num = 1

for s_name, rows in [("Sheet 1", s1_rows), ("Sheet 2", s2_rows)]:
    for r_idx, r in enumerate(rows[1:], 1):
        if len(r) < 4: continue
        gn = clean_gn_name(r[2])
        for b in range(8):
            d_col = 4 + b * 4
            desc_col = 5 + b * 4
            p_col = 6 + b * 4
            if d_col >= len(r) or desc_col >= len(r): break
            d_raw = r[d_col].strip()
            desc = clean_desc(r[desc_col])
            p_raw = r[p_col].strip() if p_col < len(r) else ""
            if not d_raw and not desc: continue

            # Photos
            f1 = re.findall(r'id=([a-zA-Z0-9_-]{15,})', p_raw)
            f2 = re.findall(r'/d/([a-zA-Z0-9_-]{15,})', p_raw)
            photo_ids = []
            for fid in f1 + f2:
                if fid not in photo_ids: photo_ids.append(fid)

            photo_objs = [{
                'id': fid,
                'thumbnail': f"https://lh3.googleusercontent.com/d/{fid}=s400",
                'full': f"https://lh3.googleusercontent.com/d/{fid}=s1200",
                'driveUrl': f"https://drive.google.com/file/d/{fid}/view?usp=sharing"
            } for fid in photo_ids]

            date_str = parse_date(d_raw)
            ym = date_str[:7]
            if ym not in MONTH_NAMES:
                ym = "2026-07"
            month_si = MONTH_NAMES.get(ym, "ජූලි 2026")

            cat_id, cat_name, cat_color, cat_icon = classify_activity(desc)

            activities.append({
                "id": f"ACT-{act_id_num:03d}",
                "titleSi": desc[:60] if len(desc) > 60 else (desc or "ප්‍රජා සංවර්ධන වැඩසටහන"),
                "gnNameSi": gn,
                "sabhaNameSi": f"{gn} ප්‍රජා සංවර්ධන සභාව",
                "date": date_str,
                "dateRaw": d_raw,
                "reportingMonth": ym,
                "monthSi": month_si,
                "category": cat_id,
                "categoryNameSi": cat_name,
                "categoryColor": cat_color,
                "categoryIcon": cat_icon,
                "description": desc or "ප්‍රජා සංවර්ධන වැඩසටහන",
                "images": [p['full'] for p in photo_objs],
                "photoObjects": photo_objs,
                "photoCount": len(photo_objs),
                "source": f"{s_name} R{r_idx} B{b+1}",
                "sheet": s_name,
                "statusLabelSi": "සම්පූර්ණයි"
            })
            act_id_num += 1

print(f"Total authentic activities extracted: {len(activities)}")

# Sort activities newest first
activities.sort(key=lambda x: x['date'], reverse=True)

# Build GN Divisions (53 reporting + 10 pending = 63)
reporting_gn_names = sorted(list(set(a['gnNameSi'] for a in activities)))
print(f"Reporting GN divisions: {len(reporting_gn_names)}")

PENDING_DIVISIONS = [
    "109 බදුන්ගොඩ",
    "112 වලහන්දූව",
    "112 යග්ගහ",
    "118 ගනේගොඩ",
    "130 හාලිවල",
    "130 කැරැන්විල ජනපදය",
    "135 මීගොඩ",
    "135 මැලෑගොඩ",
    "135 ගල්ගමුව",
    "135 දිවුලාන"
]

all_63_gn_divisions = []
for gn_name in reporting_gn_names:
    gn_acts = [a for a in activities if a['gnNameSi'] == gn_name]
    s1_cnt = sum(1 for a in gn_acts if a['sheet'] == 'Sheet 1')
    s2_cnt = sum(1 for a in gn_acts if a['sheet'] == 'Sheet 2')
    dates = sorted(list(set(a['date'] for a in gn_acts)))
    photos_count = sum(a['photoCount'] for a in gn_acts)
    cat_counts = defaultdict(int)
    for a in gn_acts:
        cat_counts[a['categoryNameSi']] += 1
    top_sector = max(cat_counts.items(), key=lambda x: x[1])[0] if cat_counts else "ප්‍රජා සේවා හා සංවර්ධන"
    diversity = len(set(a['category'] for a in gn_acts))

    all_63_gn_divisions.append({
        "nameSi": gn_name,
        "sabhaNameSi": f"{gn_name} ප්‍රජා සංවර්ධන සභාව",
        "keySectorSi": top_sector,
        "totalProjects": len(gn_acts),
        "sheet1Count": s1_cnt,
        "sheet2Count": s2_cnt,
        "completed": len(gn_acts),
        "ongoing": 0,
        "progress": 100,
        "activeDays": len(dates),
        "totalPhotos": photos_count,
        "diversity": min(diversity, 10),
        "lastReportDate": dates[-1] if dates else "2026-09-30",
        "statusBadge": "වාර්තා කර ඇත",
        "isReporting": True
    })

# Add pending divisions
for p_name in PENDING_DIVISIONS:
    all_63_gn_divisions.append({
        "nameSi": p_name,
        "sabhaNameSi": f"{p_name} ප්‍රජා සංවර්ධන සභාව",
        "keySectorSi": "සැලසුම් කෙරෙමින් පවතී",
        "totalProjects": 0,
        "sheet1Count": 0,
        "sheet2Count": 0,
        "completed": 0,
        "ongoing": 0,
        "progress": 0,
        "activeDays": 0,
        "totalPhotos": 0,
        "diversity": 0,
        "lastReportDate": "-",
        "statusBadge": "පොරොත්තු",
        "isReporting": False
    })

# Sort all 63 divisions: reporting by totalProjects desc, then pending
all_63_gn_divisions.sort(key=lambda x: (not x['isReporting'], -x['totalProjects'], x['nameSi']))

# Calculate Monthly Stats
months_ordered = [
    ("2025-11", "නොවැම්බර් 2025"),
    ("2025-12", "දෙසැම්බර් 2025"),
    ("2026-01", "ජනවාරි 2026"),
    ("2026-02", "පෙබරවාරි 2026"),
    ("2026-03", "මාර්තු 2026"),
    ("2026-04", "අප්‍රේල් 2026"),
    ("2026-05", "මැයි 2026"),
    ("2026-06", "ජූනි 2026"),
    ("2026-07", "ජූලි 2026"),
    ("2026-08", "අගෝස්තු 2026"),
    ("2026-09", "සැප්තැම්බර් 2026"),
    ("2026-10", "ඔක්තෝබර් 2026")
]

monthly_stats = []
cum_acts = 0
prev_cnt = None

for ym, m_si in months_ordered:
    m_acts = [a for a in activities if a['reportingMonth'] == ym]
    cnt = len(m_acts)
    cum_acts += cnt
    dates = set(a['date'] for a in m_acts)
    gns = set(a['gnNameSi'] for a in m_acts)
    
    mom_pct = None
    if prev_cnt is not None and prev_cnt > 0:
        mom_pct = round(((cnt - prev_cnt) / prev_cnt) * 100, 1)
    prev_cnt = cnt

    monthly_stats.append({
        "monthKey": ym,
        "monthSi": m_si,
        "count": cnt,
        "completed": cnt,
        "ongoing": 0,
        "activeDays": len(dates),
        "reportingDivisions": len(gns),
        "reportingGns": len(gns),
        "momChangePct": mom_pct,
        "cumulativeActivities": cum_acts,
        "cumulativeTotal": cum_acts,
        "cumulativeCount": cum_acts,
        "status": "100% සම්පූර්ණයි"
    })

# Categories Stats
category_stats = []
for cat_id, cat_name, color, icon, _ in CATEGORIES:
    cat_acts = [a for a in activities if a['category'] == cat_id]
    category_stats.append({
        "id": cat_id,
        "nameSi": cat_name,
        "color": color,
        "icon": icon,
        "count": len(cat_acts),
        "pct": round((len(cat_acts) / len(activities)) * 100, 1) if activities else 0
    })

# Build Photo Gallery Items (flat array of 666 photos)
photo_gallery = []
for a in activities:
    for p in a['photoObjects']:
        photo_gallery.append({
            "id": p['id'],
            "url": p['full'],
            "thumbnail": p['thumbnail'],
            "driveUrl": p['driveUrl'],
            "titleSi": a['titleSi'],
            "gnDivision": a['gnNameSi'],
            "sabhaNameSi": a['sabhaNameSi'],
            "date": a['date'],
            "monthSi": a['monthSi'],
            "category": a['category'],
            "categoryNameSi": a['categoryNameSi'],
            "actId": a['id']
        })

# Total active unique dates
unique_dates = set(a['date'] for a in activities)

# Weekday vs Weekend
weekday_counts = defaultdict(int)
for a in activities:
    try:
        dt = datetime.strptime(a['date'], '%Y-%m-%d')
        weekday_counts[dt.strftime('%A')] += 1
    except:
        pass

weekdays = sum(weekday_counts[d] for d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
weekends = sum(weekday_counts[d] for d in ['Saturday', 'Sunday'])
tot_days = weekdays + weekends or 1

# Peak dates
date_counts = defaultdict(int)
for a in activities:
    date_counts[a['date']] += 1
peak_dates = sorted([{"date": d, "count": c} for d, c in date_counts.items()], key=lambda x: x['count'], reverse=True)[:10]

# Heatmap
heatmap_data = [{"date": d, "count": c} for d, c in date_counts.items()]

overview = {
    "totalActivities": len(activities),
    "completedProjects": len(activities),
    "ongoingProjects": 0,
    "activeProjects": len(activities),
    "sheet1Activities": sum(1 for a in activities if a['sheet'] == 'Sheet 1'),
    "sheet2Activities": sum(1 for a in activities if a['sheet'] == 'Sheet 2'),
    "sheet1Responses": len(s1_rows) - 1,
    "sheet2Responses": len(s2_rows) - 1,
    "totalResponses": len(s1_rows) - 1 + len(s2_rows) - 1,
    "reportingGnDivisions": len(reporting_gn_names),
    "pendingGnDivisions": len(PENDING_DIVISIONS),
    "totalGNDivisions": 63,
    "coveragePercent": round((len(reporting_gn_names) / 63) * 100, 1),
    "totalActiveDays": len(unique_dates),
    "totalPhotos": len(photo_gallery),
    "overallCompletionRate": 100,
    "avgProgrammesPerDivision": round(len(activities) / len(reporting_gn_names), 1),
    "weekdayCount": weekdays,
    "weekendCount": weekends,
    "weekdayPct": round((weekdays / tot_days) * 100, 1),
    "weekendPct": round((weekends / tot_days) * 100, 1)
}

final_data = {
    "overview": overview,
    "categories": category_stats,
    "monthlyStats": monthly_stats,
    "gnDivisions": all_63_gn_divisions,
    "activities": activities,
    "photoGallery": photo_gallery,
    "peakDates": peak_dates,
    "heatmapData": heatmap_data,
    "weekdayAnalytics": {
        "weekdayCount": weekdays,
        "weekendCount": weekends,
        "weekdayPct": overview["weekdayPct"],
        "weekendPct": overview["weekendPct"],
        "distribution": [
            {"day": "සඳුදා", "count": weekday_counts.get("Monday", 0)},
            {"day": "අඟහරුවාදා", "count": weekday_counts.get("Tuesday", 0)},
            {"day": "බදාදා", "count": weekday_counts.get("Wednesday", 0)},
            {"day": "බ්‍රහස්පතින්දා", "count": weekday_counts.get("Thursday", 0)},
            {"day": "සිකුරාදා", "count": weekday_counts.get("Friday", 0)},
            {"day": "සෙනසුරාදා", "count": weekday_counts.get("Saturday", 0)},
            {"day": "ඉරිදා", "count": weekday_counts.get("Sunday", 0)}
        ]
    }
}

with open('raw_drive_data/canonical_v4.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("Saved raw_drive_data/canonical_v4.json successfully!")
print(f"Summary: {overview['totalActivities']} Activities, {overview['reportingGnDivisions']} Reporting GNs, {overview['totalPhotos']} Photos, {overview['totalActiveDays']} Active Days")
