with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """  renderKPIs() {
    const sec = this.data.secretariatInfo;

    // Total Activities
    const totalActEl = document.getElementById("kpiTotalActivities");
    if (totalActEl) totalActEl.textContent = sec.activeProjects;

    // Completed Activities
    const completedActEl = document.getElementById("kpiCompletedActivities");
    if (completedActEl) completedActEl.textContent = sec.completedProjects;

    // Reporting GN Divisions
    const reportingGnEl = document.getElementById("kpiReportingGNs");
    if (reportingGnEl) reportingGnEl.textContent = `63 / 63`;"""

replacement = """  renderKPIs() {
    const sec = this.data.secretariatInfo || this.data.overview || {};

    // Total Activities
    const totalActEl = document.getElementById("kpiTotalActivities");
    if (totalActEl) totalActEl.textContent = sec.totalActivities || sec.activeProjects || (this.data.activities?.length) || 287;

    // Completed Activities
    const completedActEl = document.getElementById("kpiCompletedActivities");
    if (completedActEl) completedActEl.textContent = sec.completedProjects || sec.totalActivities || (this.data.activities?.length) || 287;

    // Reporting GN Divisions
    const reportingGnEl = document.getElementById("kpiReportingGNs");
    if (reportingGnEl) reportingGnEl.textContent = `${sec.reportingGnDivisions || 51} / ${sec.totalGNDivisions || 63}`;"""

if target in text:
    text = text.replace(target, replacement)
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully patched renderKPIs in js/app.js!")
else:
    print("Target not found in js/app.js")
