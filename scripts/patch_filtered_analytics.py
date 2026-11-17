with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    // Compute aggregate KPIs
    const totalActs = f.gn !== "all" 
      ? divisions.reduce((s, d) => s + d.totalProjects, 0)
      : (f.month !== "all" ? months.reduce((s, m) => s + m.count, 0) : 383);

    const activeDays = f.month !== "all"
      ? months.reduce((s, m) => s + m.activeDays, 0)
      : (f.gn !== "all" ? (divisions[0]?.activeDays || 10) : 173);

    const activeDivisionsCount = f.gn !== "all" ? divisions.length : 63;
    const coveragePct = f.gn !== "all" ? ((activeDivisionsCount / 63) * 100).toFixed(1) : "100%";
    const avgPerDiv = activeDivisionsCount > 0 ? (totalActs / activeDivisionsCount).toFixed(2) : 0;
    const avgPerDay = activeDays > 0 ? (totalActs / activeDays).toFixed(2) : 0;"""

replacement = """    // Compute aggregate KPIs dynamically from real canonical data
    const totalActs = f.gn !== "all" 
      ? divisions.reduce((s, d) => s + (d.totalProjects || 0), 0)
      : (f.month !== "all" ? months.reduce((s, m) => s + (m.count || 0), 0) : (this.data.activities?.length || 287));

    const totalMasterActiveDays = this.data.overview?.totalActiveDays || new Set((this.data.activities || []).map(a => a.date).filter(Boolean)).size || 115;
    const activeDays = f.month !== "all"
      ? months.reduce((s, m) => s + (m.activeDays || 0), 0)
      : (f.gn !== "all" ? (divisions[0]?.activeDays || 0) : totalMasterActiveDays);

    const reportedDivisions = divisions.filter(d => (d.totalProjects || 0) > 0);
    const activeDivisionsCount = f.gn !== "all" ? divisions.length : (reportedDivisions.length || 51);
    const coveragePct = f.gn !== "all" 
      ? ((activeDivisionsCount / 63) * 100).toFixed(1)
      : ((reportedDivisions.length / 63) * 100).toFixed(1) + "%";
    const avgPerDiv = activeDivisionsCount > 0 ? (totalActs / activeDivisionsCount).toFixed(2) : 0;
    const avgPerDay = activeDays > 0 ? (totalActs / activeDays).toFixed(2) : 0;"""

if target in code:
    code = code.replace(target, replacement)
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully patched getFilteredAnalyticsData in js/app.js!")
else:
    print("Could not find exact target string in js/app.js")
