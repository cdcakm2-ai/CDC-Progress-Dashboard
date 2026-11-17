import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Locate renderStatusTab
start_idx = code.find('renderStatusTab() {')
if start_idx == -1:
    print("renderStatusTab() not found")
    exit(1)

# Find closing brace of method
# Look for next method, e.g. exportActivitiesCSV
next_method_idx = code.find('exportActivitiesCSV()', start_idx)
if next_method_idx == -1:
    print("exportActivitiesCSV not found")
    exit(1)

# Find the last closing brace before exportActivitiesCSV
end_idx = code.rfind('}', start_idx, next_method_idx) + 1

new_render_status = """renderStatusTab() {
    const dataQuality = this.data.dataQualityLog || window.DATA_QUALITY_LOG || {};
    const summary = dataQuality.summary || {};

    // Update Top Counters
    const totalEl = document.getElementById("statusTotalUniqueActivities");
    if (totalEl) totalEl.textContent = `${this.data.activities.length} වැඩසටහන්`;

    const dupEl = document.getElementById("statusDuplicatesCount");
    if (dupEl) dupEl.textContent = `අනුපිටපත් ${dataQuality.confirmedDuplicates?.length || 3}ක් ඉවත් කරන ලදී`;

    const covEl = document.getElementById("statusCoverageSummary");
    if (covEl) {
      const repCount = this.data.gnDivisions.filter(g => (g.totalProjects || 0) > 0).length;
      covEl.textContent = `${repCount} / 63 වසම් (${(repCount/63*100).toFixed(1)}%)`;
    }

    // 1. Populate Confirmed Duplicates Table
    const dupTbody = document.getElementById("statusDuplicatesTableBody");
    if (dupTbody) {
      dupTbody.innerHTML = "";
      const dups = dataQuality.confirmedDuplicates || [];
      if (dups.length === 0) {
        dupTbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #10B981; padding: 1.5rem;">අනුපිටපත් වාර්තා කිසිවක් හමු නොවීය.</td></tr>`;
      } else {
        dups.forEach(d => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td style="font-weight: 700; color: #FFF;">${d.gn_name}</td>
            <td style="color: #94A3B8; font-size: 0.85rem;">${d.date}</td>
            <td style="color: #CBD5E1; font-size: 0.84rem; max-width: 250px;">${d.primary_desc}</td>
            <td style="font-size: 0.78rem; color: #38BDF8;">${d.primary_source}</td>
            <td style="font-size: 0.78rem; color: #EF4444; text-decoration: line-through;">${d.duplicate_source}</td>
            <td><span class="glass-badge green" style="font-size: 0.72rem;">ඉවත් කරන ලදී (Filtered)</span></td>
          `;
          dupTbody.appendChild(tr);
        });
      }
    }

    // 2. Populate Date Anomalies Table
    const anomTbody = document.getElementById("statusAnomaliesTableBody");
    if (anomTbody) {
      anomTbody.innerHTML = "";
      const anomalies = dataQuality.dateAnomalies || [];
      if (anomalies.length === 0) {
        anomTbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #10B981; padding: 1.5rem;">සියලු දිනයන් නිවැරදියි.</td></tr>`;
      } else {
        anomalies.forEach(a => {
          const tr = document.createElement("tr");
          const flagText = Array.isArray(a.flags) ? a.flags.join(", ") : "ලිපිකරු දෝෂයකි";
          tr.innerHTML = `
            <td style="font-weight: 700; color: #FFF;">${a.gnName}</td>
            <td style="color: #EF4444; font-weight: 600; font-size: 0.85rem;">${a.dateRaw}</td>
            <td style="color: #10B981; font-weight: 700; font-size: 0.85rem;">${a.dateParsed}</td>
            <td style="color: #CBD5E1; font-size: 0.84rem; max-width: 250px;">${a.desc}</td>
            <td style="font-size: 0.78rem; color: #94A3B8;">${a.sheet} Row ${a.row}</td>
            <td><span class="glass-badge gold" style="font-size: 0.72rem;">${flagText}</span></td>
          `;
          anomTbody.appendChild(tr);
        });
      }
    }

    // 3. Populate All 63 GN Division Submission Cards
    const reportingList = document.getElementById("statusReportingSubmissions");
    if (reportingList) {
      reportingList.innerHTML = "";
      // Sort: reported first, then pending, alphabetically by name
      const sortedDivs = [...this.data.gnDivisions].sort((a, b) => {
        if ((b.totalProjects || 0) !== (a.totalProjects || 0)) {
          return (b.totalProjects || 0) - (a.totalProjects || 0);
        }
        return a.nameSi.localeCompare(b.nameSi);
      });

      sortedDivs.forEach(g => {
        const hasData = (g.totalProjects || 0) > 0;
        const item = document.createElement("div");
        item.style.padding = "0.9rem 1rem";
        item.style.borderRadius = "10px";
        item.style.background = hasData ? "rgba(16, 185, 129, 0.04)" : "rgba(255, 255, 255, 0.02)";
        item.style.border = hasData ? "1px solid rgba(16, 185, 129, 0.2)" : "1px solid rgba(255, 255, 255, 0.06)";
        item.style.display = "flex";
        item.style.justifyContent = "space-between";
        item.style.alignItems = "center";
        item.style.gap = "0.6rem";

        if (hasData) {
          item.innerHTML = `
            <div>
              <div style="font-weight: 700; color: #FFF; display: flex; align-items: center; gap: 0.4rem;">
                <i class="bi bi-check-circle-fill text-success" style="font-size: 0.9rem;"></i>
                <span>${g.nameSi}</span>
              </div>
              <small style="color: #94A3B8; font-size: 0.74rem;">${g.sabhaNameSi}</small>
            </div>
            <div style="text-align: right;">
              <span class="glass-badge green" style="font-size: 0.72rem;">වැඩසටහන් ${g.totalProjects}ක්</span>
              <div style="font-size: 0.72rem; color: #FDE68A; margin-top: 0.2rem;">${g.lastReportDate || 'සක්‍රියයි'}</div>
            </div>
          `;
        } else {
          item.innerHTML = `
            <div>
              <div style="font-weight: 600; color: #94A3B8; display: flex; align-items: center; gap: 0.4rem;">
                <i class="bi bi-clock text-secondary" style="font-size: 0.9rem;"></i>
                <span>${g.nameSi}</span>
              </div>
              <small style="color: #64748B; font-size: 0.74rem;">${g.sabhaNameSi}</small>
            </div>
            <div style="text-align: right;">
              <span class="glass-badge gray" style="font-size: 0.72rem;">වාර්තා අපේක්ෂිතයි</span>
              <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.2rem;">දත්ත ලැබී නොමැත</div>
            </div>
          `;
        }
        reportingList.appendChild(item);
      });
    }

    // 4. Populate Audit Trail Log
    const auditTbody = document.getElementById("auditLogTableBody");
    if (auditTbody) {
      auditTbody.innerHTML = "";
      const logs = this.data.auditLog || [];
      logs.forEach(log => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td style="color: #94A3B8; font-size: 0.84rem;">${log.date}</td>
          <td style="font-weight: 600; color: #FFF;">${log.action}</td>
          <td style="color: #CBD5E1;">${log.division}</td>
          <td><span class="glass-badge green" style="font-size: 0.72rem;">${log.status}</span></td>
        `;
        auditTbody.appendChild(tr);
      });
    }

    // 5. Bind Refresh Button
    const refreshBtn = document.getElementById("btnRefreshSystemData");
    if (refreshBtn && !refreshBtn.dataset.bound) {
      refreshBtn.dataset.bound = "true";
      refreshBtn.addEventListener("click", async () => {
        refreshBtn.disabled = true;
        const origHTML = refreshBtn.innerHTML;
        refreshBtn.innerHTML = `<i class="bi bi-arrow-repeat spin"></i> සමමුහුර්ත වෙමින් පවතී...`;
        try {
          if (window.pssSheetsService) {
            await window.pssSheetsService.getDashboardData(true);
          }
          this.showToast("Google Drive දත්ත සාර්ථකව යාවත්කාලීන විය!", "success");
          setTimeout(() => {
            window.location.reload();
          }, 800);
        } catch (e) {
          this.showToast("දත්ත නැවුම් කිරීමේදී ගැටළුවක් ඇති විය.", "error");
          refreshBtn.disabled = false;
          refreshBtn.innerHTML = origHTML;
        }
      });
    }
  }"""

updated_code = code[:start_idx] + new_render_status + "\n\n  " + code[next_method_idx:]

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(updated_code)

print("Successfully updated renderStatusTab in js/app.js!")
