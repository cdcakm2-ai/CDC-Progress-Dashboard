const fs = require('fs');

const analyticsMethods = `
  // =========================================================================
  // TAB 6: ප්‍රගති විශ්ලේෂණය (PROGRESS ANALYSIS ENGINE)
  // =========================================================================

  initAnalyticsTab() {
    this.analyticsFilters = {
      year: "all",
      month: "all",
      gn: "all",
      sector: "all"
    };

    this.anDivFilter = "all";
    this.anDivSearchTerm = "";
    this.anCompareMode = "division"; // 'division', 'month', 'sector'

    this.populateAnalyticsFilterDropdowns();
    this.bindAnalyticsEvents();
    this.updateAnalyticsView();
  }

  populateAnalyticsFilterDropdowns() {
    // 1. Months Dropdown
    const monthSelect = document.getElementById("analyticsMonthFilter");
    const detailMonthSelect = document.getElementById("anMonthDetailSelect");
    const months = this.data.monthlyStats || [];

    if (monthSelect) {
      monthSelect.innerHTML = '<option value="all">සියලු මාස (මාස 11)</option>';
      months.forEach(m => {
        monthSelect.innerHTML += \`<option value="\${m.monthKey}">\${m.monthSi}</option>\`;
      });
    }

    if (detailMonthSelect) {
      detailMonthSelect.innerHTML = '<option value="all">සියලු මාස 11 (සමස්ත වගුව)</option>';
      months.forEach(m => {
        detailMonthSelect.innerHTML += \`<option value="\${m.monthKey}">\${m.monthSi}</option>\`;
      });
    }

    // 2. GN Divisions Dropdown (All 63)
    const gnSelect = document.getElementById("analyticsGnFilter");
    const divisions = this.data.gnDivisions || [];
    if (gnSelect) {
      gnSelect.innerHTML = '<option value="all">සියලු වසම් (වසම් 63)</option>';
      divisions.forEach(d => {
        gnSelect.innerHTML += \`<option value="\${d.nameSi}">\${d.nameSi}</option>\`;
      });
    }

    // 3. Sectors Dropdown (All 10)
    const sectorSelect = document.getElementById("analyticsSectorFilter");
    const sectors = this.data.analyticalCategories || [];
    if (sectorSelect) {
      sectorSelect.innerHTML = '<option value="all">සියලු ක්ෂේත්‍ර 10</option>';
      sectors.forEach(s => {
        sectorSelect.innerHTML += \`<option value="\${s.id}">\${s.nameSi}</option>\`;
      });
    }

    // 4. Comparison Entity Selectors
    this.populateCompareSelectors();
  }

  populateCompareSelectors() {
    const selA = document.getElementById("anCompareSelectA");
    const selB = document.getElementById("anCompareSelectB");
    const lblA = document.getElementById("anCompareLabelA");
    const lblB = document.getElementById("anCompareLabelB");
    if (!selA || !selB) return;

    selA.innerHTML = "";
    selB.innerHTML = "";

    if (this.anCompareMode === "division") {
      lblA.textContent = "පළමු වසම (Division A):";
      lblB.textContent = "දෙවන වසම (Division B):";
      const divs = this.data.gnDivisions || [];
      divs.forEach((d, idx) => {
        selA.innerHTML += \`<option value="\${d.nameSi}" \${idx === 0 ? "selected" : ""}>\${d.nameSi} (වැඩසටහන් \${d.totalProjects})</option>\`;
        selB.innerHTML += \`<option value="\${d.nameSi}" \${idx === 1 ? "selected" : ""}>\${d.nameSi} (වැඩසටහන් \${d.totalProjects})</option>\`;
      });
    } else if (this.anCompareMode === "month") {
      lblA.textContent = "පළමු මාසය (Month A):";
      lblB.textContent = "දෙවන මාසය (Month B):";
      const months = this.data.monthlyStats || [];
      months.forEach((m, idx) => {
        // default Aug vs Sep
        const isAug = m.monthKey === "2026-08";
        const isSep = m.monthKey === "2026-09";
        selA.innerHTML += \`<option value="\${m.monthKey}" \${isAug ? "selected" : ""}>\${m.monthSi} (\${m.count})</option>\`;
        selB.innerHTML += \`<option value="\${m.monthKey}" \${isSep ? "selected" : ""}>\${m.monthSi} (\${m.count})</option>\`;
      });
    } else {
      lblA.textContent = "පළමු ක්ෂේත්‍රය (Sector A):";
      lblB.textContent = "දෙවන ක්ෂේත්‍රය (Sector B):";
      const cats = this.data.analyticalCategories || [];
      cats.forEach((c, idx) => {
        selA.innerHTML += \`<option value="\${c.id}" \${idx === 0 ? "selected" : ""}>\${c.nameSi} (\${c.count})</option>\`;
        selB.innerHTML += \`<option value="\${c.id}" \${idx === 1 ? "selected" : ""}>\${c.nameSi} (\${c.count})</option>\`;
      });
    }

    this.renderAnCompareSubtab();
  }

  bindAnalyticsEvents() {
    // 1. Dynamic Filters
    const yearSelect = document.getElementById("analyticsYearFilter");
    const monthSelect = document.getElementById("analyticsMonthFilter");
    const gnSelect = document.getElementById("analyticsGnFilter");
    const sectorSelect = document.getElementById("analyticsSectorFilter");
    const resetBtn = document.getElementById("btnResetAnalyticsFilters");

    if (yearSelect) {
      yearSelect.addEventListener("change", (e) => {
        this.analyticsFilters.year = e.target.value;
        this.updateAnalyticsView();
      });
    }

    if (monthSelect) {
      monthSelect.addEventListener("change", (e) => {
        this.analyticsFilters.month = e.target.value;
        this.updateAnalyticsView();
      });
    }

    if (gnSelect) {
      gnSelect.addEventListener("change", (e) => {
        this.analyticsFilters.gn = e.target.value;
        this.updateAnalyticsView();
      });
    }

    if (sectorSelect) {
      sectorSelect.addEventListener("change", (e) => {
        this.analyticsFilters.sector = e.target.value;
        this.updateAnalyticsView();
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        this.analyticsFilters = { year: "all", month: "all", gn: "all", sector: "all" };
        if (yearSelect) yearSelect.value = "all";
        if (monthSelect) monthSelect.value = "all";
        if (gnSelect) gnSelect.value = "all";
        if (sectorSelect) sectorSelect.value = "all";
        this.anDivSearchTerm = "";
        this.anDivFilter = "all";
        const divSearchInput = document.getElementById("anDivSearchInput");
        if (divSearchInput) divSearchInput.value = "";
        document.querySelectorAll(".an-div-filter-pill").forEach(p => p.classList.toggle("active", p.getAttribute("data-filter") === "all"));
        this.updateAnalyticsView();
      });
    }

    // 2. Division Search & Quick Filters
    const divSearchInput = document.getElementById("anDivSearchInput");
    if (divSearchInput) {
      divSearchInput.addEventListener("input", (e) => {
        this.anDivSearchTerm = e.target.value.toLowerCase().trim();
        this.renderAnDivisionsSubtab();
      });
    }

    document.querySelectorAll(".an-div-filter-pill").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".an-div-filter-pill").forEach(p => p.classList.remove("active"));
        btn.classList.add("active");
        this.anDivFilter = btn.getAttribute("data-filter");
        this.renderAnDivisionsSubtab();
      });
    });

    // 3. Month Detail Select
    const detailMonthSelect = document.getElementById("anMonthDetailSelect");
    if (detailMonthSelect) {
      detailMonthSelect.addEventListener("change", (e) => {
        this.renderAnMonthlySubtab(e.target.value);
      });
    }

    // 4. Comparison Controls
    document.querySelectorAll(".an-compare-mode-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".an-compare-mode-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.anCompareMode = btn.getAttribute("data-mode");
        this.populateCompareSelectors();
      });
    });

    const selA = document.getElementById("anCompareSelectA");
    const selB = document.getElementById("anCompareSelectB");
    if (selA) selA.addEventListener("change", () => this.renderAnCompareSubtab());
    if (selB) selB.addEventListener("change", () => this.renderAnCompareSubtab());
  }

  getFilteredAnalyticsData() {
    const f = this.analyticsFilters;
    let months = [...(this.data.monthlyStats || [])];
    let divisions = [...(this.data.gnDivisions || [])];
    let categories = [...(this.data.analyticalCategories || [])];

    // Filter by year
    if (f.year !== "all") {
      const y = parseInt(f.year);
      months = months.filter(m => m.year === y);
    }

    // Filter by month
    if (f.month !== "all") {
      months = months.filter(m => m.monthKey === f.month);
    }

    // Filter by GN
    if (f.gn !== "all") {
      divisions = divisions.filter(d => d.nameSi === f.gn);
    }

    // Filter by sector
    if (f.sector !== "all") {
      categories = categories.filter(c => c.id === f.sector);
    }

    // Compute aggregate KPIs
    const totalActs = f.gn !== "all" 
      ? divisions.reduce((s, d) => s + d.totalProjects, 0)
      : (f.month !== "all" ? months.reduce((s, m) => s + m.count, 0) : 383);

    const activeDays = f.month !== "all"
      ? months.reduce((s, m) => s + m.activeDays, 0)
      : (f.gn !== "all" ? (divisions[0]?.activeDays || 10) : 173);

    const activeDivisionsCount = f.gn !== "all" ? divisions.length : 63;
    const coveragePct = f.gn !== "all" ? ((activeDivisionsCount / 63) * 100).toFixed(1) : "100%";
    const avgPerDiv = activeDivisionsCount > 0 ? (totalActs / activeDivisionsCount).toFixed(2) : 0;
    const avgPerDay = activeDays > 0 ? (totalActs / activeDays).toFixed(2) : 0;

    return {
      kpis: { totalActs, activeDays, activeDivisionsCount, coveragePct, avgPerDiv, avgPerDay },
      months,
      divisions,
      categories
    };
  }

  updateAnalyticsView() {
    const filtered = this.getFilteredAnalyticsData();
    this.renderAnCumulativeSubtab(filtered);
    this.renderAnMonthlySubtab("all", filtered);
    this.renderAnDivisionsSubtab(filtered);
    this.renderAnSectorsSubtab(filtered);
    this.renderAnTimelineSubtab();
    this.renderAnDiversitySubtab();
    this.renderAnCompareSubtab();
    this.renderAnDeepdiveSubtab(filtered);
  }

  // --- SUBTAB 1: CUMULATIVE ---
  renderAnCumulativeSubtab(filtered) {
    const k = filtered.kpis;
    const elActs = document.getElementById("anKpiTotalActs");
    const elDays = document.getElementById("anKpiActiveDays");
    const elDivs = document.getElementById("anKpiDivisions");
    const elCov = document.getElementById("anKpiCoverage");
    const elAvgDiv = document.getElementById("anKpiAvgPerDiv");
    const elAvgDay = document.getElementById("anKpiAvgPerDay");

    if (elActs) elActs.textContent = k.totalActs;
    if (elDays) elDays.textContent = k.activeDays;
    if (elDivs) elDivs.textContent = k.activeDivisionsCount;
    if (elCov) elCov.textContent = typeof k.coveragePct === "number" ? k.coveragePct + "%" : k.coveragePct;
    if (elAvgDiv) elAvgDiv.textContent = k.avgPerDiv;
    if (elAvgDay) elAvgDay.textContent = k.avgPerDay;

    if (window.pssCharts) {
      window.pssCharts.renderAnCumulativeChart(filtered.months);
    }
  }

  // --- SUBTAB 2: MONTHLY ---
  renderAnMonthlySubtab(selectedMonthKey = "all", filtered = null) {
    const tbody = document.getElementById("anMonthlyTableBody");
    const notesEl = document.getElementById("anMonthDetailNotes");
    if (!tbody) return;

    let months = this.data.monthlyStats || [];
    if (selectedMonthKey && selectedMonthKey !== "all") {
      months = months.filter(m => m.monthKey === selectedMonthKey);
      if (notesEl) notesEl.innerHTML = \`<span class="text-gold">තෝරාගත් මාසය: \${months[0]?.monthSi} (වැඩසටහන් \${months[0]?.count})</span>\`;
    } else {
      if (notesEl) notesEl.textContent = "සම්පූර්ණ මාස 11 ක සංඛ්‍යාලේඛන පහත දැක්වේ";
    }

    tbody.innerHTML = "";
    months.forEach(m => {
      const momBadge = m.momChangePct === null
        ? '<span class="badge" style="background: rgba(255,255,255,0.06); color: #94A3B8;">ආරම්භය</span>'
        : (m.momChangePct >= 0
          ? \`<span class="badge" style="background: rgba(16,185,129,0.2); color: #6EE7B7; font-weight:700;">+\${m.momChangePct}%</span>\`
          : \`<span class="badge" style="background: rgba(239,68,68,0.2); color: #F87171; font-weight:700;">\${m.momChangePct}%</span>\`);

      const isAug = m.monthKey === "2026-08";
      const isSep = m.monthKey === "2026-09";
      const rowStyle = isAug ? "background: rgba(212, 175, 55, 0.08);" : (isSep ? "background: rgba(56, 189, 248, 0.06);" : "");

      tbody.innerHTML += \`
        <tr style="\${rowStyle}">
          <td>
            <strong>\${m.monthSi}</strong>
            \${isAug ? ' <span class="glass-badge gold" style="font-size:0.68rem; padding: 0.15rem 0.4rem;">උපරිම මාසය</span>' : ''}
            \${isSep ? ' <span class="glass-badge blue" style="font-size:0.68rem; padding: 0.15rem 0.4rem;">වත්මන් මාසය</span>' : ''}
          </td>
          <td style="text-align: center; font-weight: 800; font-size: 1.05rem;" class="\${isAug ? 'gold-text-gradient' : 'text-gold'}">\${m.count}</td>
          <td style="text-align: center; color: #6EE7B7;">\${m.completed}</td>
          <td style="text-align: center; color: #60A5FA;">\${m.ongoing}</td>
          <td style="text-align: center; font-weight: 600;">\${m.activeDays}</td>
          <td style="text-align: center; font-weight: 600;">\${m.reportingDivisions}</td>
          <td style="text-align: center;">\${momBadge}</td>
          <td>\${(m.beneficiaries || 0).toLocaleString()}</td>
          <td style="color: #CBD5E1;">රු. \${((m.spentLKR || 0) / 1000000).toFixed(2)}M</td>
          <td style="font-weight: 700; color: #FDE68A;">රු. \${((m.cumulativeSpent || 0) / 1000000).toFixed(2)}M</td>
        </tr>
      \`;
    });

    if (window.pssCharts) {
      window.pssCharts.renderAnMonthlyTrendChart(this.data.monthlyStats);
    }
  }

  // --- SUBTAB 3: ALL 63 DIVISIONS ---
  renderAnDivisionsSubtab(filtered = null) {
    const tbody = document.getElementById("anDivisionsTableBody");
    if (!tbody) return;

    let divs = [...(this.data.gnDivisions || [])];

    // Search filter
    if (this.anDivSearchTerm) {
      divs = divs.filter(d => d.nameSi.toLowerCase().includes(this.anDivSearchTerm));
    }

    // Quick filter pills
    if (this.anDivFilter === "top10") {
      divs = [...divs].sort((a, b) => b.totalProjects - a.totalProjects).slice(0, 10);
    } else if (this.anDivFilter === "completed100") {
      divs = divs.filter(d => d.ongoing === 0);
    } else if (this.anDivFilter === "low") {
      divs = divs.filter(d => d.totalProjects <= 4);
    }

    // Sort by total projects descending
    divs.sort((a, b) => b.totalProjects - a.totalProjects);

    tbody.innerHTML = "";
    if (divs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="11" style="text-align: center; padding: 2rem; color: #94A3B8;">සෙවුමට ගැළපෙන ග්‍රාම නිලධාරී වසම් හමු නොවීය.</td></tr>';
      return;
    }

    divs.forEach((d, idx) => {
      const isTop3 = idx < 3;
      const rankBadge = isTop3 
        ? \`<span class="badge" style="background: rgba(212,175,55,0.25); color: #FDE68A; font-weight: 800; font-size: 0.85rem; padding: 0.25rem 0.55rem; border-radius: 999px; border: 1px solid #D4AF37;">#\${idx + 1}</span>\`
        : \`<span style="color: #94A3B8; font-weight: 600;">#\${idx + 1}</span>\`;

      const diversityStars = d.diversity >= 7
        ? \`<span class="badge" style="background: rgba(16,185,129,0.2); color: #6EE7B7; font-weight:700;">\${d.diversity}/10 (ඉහළම)</span>\`
        : (d.diversity >= 5
          ? \`<span class="badge" style="background: rgba(59,130,246,0.2); color: #93C5FD; font-weight:600;">\${d.diversity}/10</span>\`
          : \`<span class="badge" style="background: rgba(245,158,11,0.2); color: #FCD34D;">\${d.diversity}/10</span>\`);

      const statusBadge = d.ongoing === 0
        ? '<span class="glass-badge green" style="font-size:0.75rem;"><i class="bi bi-check2-circle"></i> 100% සම්පූර්ණයි</span>'
        : '<span class="glass-badge blue" style="font-size:0.75rem;"><i class="bi bi-hourglass-split"></i> ක්‍රියාත්මකයි</span>';

      tbody.innerHTML += \`
        <tr>
          <td style="text-align: center;">\${rankBadge}</td>
          <td>
            <strong style="color: #FFF; font-size: 0.95rem;">\${d.nameSi}</strong>
            <div style="font-size: 0.74rem; color: #94A3B8;">\${d.sabhaNameSi}</div>
          </td>
          <td><span class="glass-badge blue" style="font-size: 0.74rem;">\${d.keySectorSi}</span></td>
          <td style="text-align: center; font-weight: 800; font-size: 1.1rem; color: #FDE68A;">\${d.totalProjects}</td>
          <td style="text-align: center; color: #6EE7B7; font-weight: 700;">\${d.completed}</td>
          <td style="text-align: center; color: #60A5FA;">\${d.ongoing}</td>
          <td style="text-align: center;">\${diversityStars}</td>
          <td style="text-align: center; font-weight: 600;">\${d.activeDays}</td>
          <td>\${(d.beneficiaries || 0).toLocaleString()}</td>
          <td>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="font-size: 0.78rem; font-weight: 700; color: #FFF; width: 35px;">\${d.progress}%</span>
              <div class="progress-track" style="width: 60px; height: 6px;">
                <div class="progress-fill" style="width: \${d.progress}%;"></div>
              </div>
            </div>
          </td>
          <td style="text-align: center;">\${statusBadge}</td>
        </tr>
      \`;
    });

    if (window.pssCharts) {
      window.pssCharts.renderAnTopDivisionsChart(this.data.gnDivisions);
    }
  }

  // --- SUBTAB 4: 10 SECTORS ---
  renderAnSectorsSubtab(filtered = null) {
    const grid = document.getElementById("an10SectorsGrid");
    const tbody = document.getElementById("anSectorTableBody");
    const cats = this.data.analyticalCategories || [];
    if (!grid || !tbody) return;

    // Render 10 Cards
    grid.innerHTML = "";
    cats.forEach((c, idx) => {
      grid.innerHTML += \`
        <div class="glass-panel an-sector-card" style="padding: 1.1rem; --sector-color: \${c.color};">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
            <div class="kpi-icon-wrap" style="background: \${c.color}22; color: \${c.color};">
              <i class="bi \${c.icon}"></i>
            </div>
            <span class="badge" style="background: \${c.color}33; color: #FFF; font-weight: 700; font-size: 0.76rem; border: 1px solid \${c.color}66;">
              \${c.pct}%
            </span>
          </div>
          <div style="font-size: 0.86rem; font-weight: 700; color: #FFF; margin-bottom: 0.2rem; min-height: 2.2rem;">
            \${c.nameSi}
          </div>
          <div style="font-size: 1.45rem; font-weight: 800; color: \${c.color}; margin-bottom: 0.4rem;">
            \${c.count} <span style="font-size: 0.76rem; font-weight: 400; color: #94A3B8;">වැඩසටහන්</span>
          </div>
          <div style="font-size: 0.74rem; color: #CBD5E1; line-height: 1.4;">
            \${c.desc}
          </div>
        </div>
      \`;
    });

    // Render Detailed Table
    tbody.innerHTML = "";
    cats.forEach((c, idx) => {
      const priority = c.pct >= 14 ? '<span class="glass-badge gold">ඉහළ ප්‍රමුඛතාවය</span>' : (c.pct >= 9 ? '<span class="glass-badge blue">මධ්‍යස්ථ</span>' : '<span class="glass-badge green">විශේෂිත / නිවාරණ</span>');

      tbody.innerHTML += \`
        <tr>
          <td style="text-align: center; color: #94A3B8;">\${idx + 1}</td>
          <td>
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: \${c.color};"></span>
              <strong style="color: #FFF;">\${c.nameSi}</strong>
            </div>
          </td>
          <td style="text-align: center; font-weight: 800; font-size: 1.05rem; color: \${c.color};">\${c.count}</td>
          <td style="text-align: center; font-weight: 700;">\${c.pct}%</td>
          <td>\${priority}</td>
          <td style="font-size: 0.82rem; color: #CBD5E1;">\${c.desc}</td>
        </tr>
      \`;
    });

    if (window.pssCharts) {
      window.pssCharts.renderAnSectorCharts(cats);
    }
  }

  // --- SUBTAB 5: TIMELINE & WEEKDAY ANALYSIS ---
  renderAnTimelineSubtab() {
    const peakGrid = document.getElementById("anPeakDatesGrid");
    const peaks = this.data.analytics?.peakDates || [];
    if (peakGrid) {
      peakGrid.innerHTML = "";
      peaks.forEach(p => {
        peakGrid.innerHTML += \`
          <div class="glass-panel" style="padding: 1rem; border-top: 3px solid #D4AF37;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <span class="glass-badge gold" style="font-size: 0.72rem;">\${p.daySi}</span>
              <strong style="font-size: 1.35rem; color: #FDE68A;">\${p.count} <span style="font-size: 0.74rem; font-weight: 400; color: #CBD5E1;">වැඩසටහන්</span></strong>
            </div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #FFF; margin-bottom: 0.2rem;">\${p.date}</div>
            <div style="font-size: 0.76rem; color: #CBD5E1;">\${p.keyActivities}</div>
          </div>
        \`;
      });
    }

    // Render Calendar Heatmap
    const heatmapWrap = document.getElementById("anCalendarHeatmapWrap");
    const heatmapData = this.data.analytics?.heatmap || [];
    if (heatmapWrap && heatmapData.length > 0) {
      // Group by month
      const monthsMap = {};
      heatmapData.forEach(d => {
        const mKey = d.date.substring(0, 7);
        if (!monthsMap[mKey]) monthsMap[mKey] = [];
        monthsMap[mKey].push(d);
      });

      const monthNamesSi = {
        "2025-11": "2025 නොවැම්බර්",
        "2025-12": "2025 දෙසැම්බර්",
        "2026-01": "2026 ජනවාරි",
        "2026-02": "2026 පෙබරවාරි",
        "2026-03": "2026 මාර්තු",
        "2026-04": "2026 අප්‍රේල්",
        "2026-05": "2026 මැයි",
        "2026-06": "2026 ජූනි",
        "2026-07": "2026 ජූලි",
        "2026-08": "2026 අගෝස්තු",
        "2026-09": "2026 සැප්තැම්බර්"
      };

      let html = '<div class="an-heatmap-container">';
      Object.keys(monthsMap).forEach(mKey => {
        html += \`
          <div class="an-month-col">
            <div class="an-month-title">\${monthNamesSi[mKey] || mKey}</div>
            <div class="an-days-grid">
        \`;
        monthsMap[mKey].forEach(day => {
          let lvl = "level-0";
          if (day.count >= 7) lvl = "level-peak";
          else if (day.count >= 4) lvl = "level-3";
          else if (day.count >= 2) lvl = "level-2";
          else if (day.count === 1) lvl = "level-1";

          html += \`<div class="an-day-cell \${lvl}" title="\${day.date}: වැඩසටහන් \${day.count}"></div>\`;
        });
        html += \`
            </div>
          </div>
        \`;
      });
      html += '</div>';
      heatmapWrap.innerHTML = html;
    }

    if (window.pssCharts) {
      window.pssCharts.renderAnTimelineCharts();
    }
  }

  // --- SUBTAB 6: DIVERSITY ANALYSIS ---
  renderAnDiversitySubtab() {
    const topGrid = document.getElementById("anDiversityTopGrid");
    const tbody = document.getElementById("anDiversityTableBody");
    const divs = this.data.gnDivisions || [];
    if (!topGrid || !tbody) return;

    // Diversity Champions (Top 5)
    const champs = [
      { name: "හියාචාර උතුර", diversity: 9, acts: 14, desc: "වනජීවී බාධක, සෞඛ්‍ය, කෘෂි, ඩෙංගු, සුබසාධන ඇතුළු ක්ෂේත්‍ර 9ක්" },
      { name: "නුගදූව", diversity: 7, acts: 15, desc: "පෙරපාසල්, සෞඛ්‍ය, පරිසර, ජීවනෝපාය ඇතුළු ක්ෂේත්‍ර 7ක්" },
      { name: "ජඹුකැටිය", diversity: 7, acts: 12, desc: "ළමා ක්‍රීඩා, නීති දැනුවත් කිරීම්, යටිතල පහසුකම් ක්ෂේත්‍ර 7ක්" },
      { name: "බදුන්ගොඩ ජනපදය", diversity: 7, acts: 10, desc: "සමාජ සුබසාධන, සෞඛ්‍ය හා කෘෂිකාර්මික ක්ෂේත්‍ර 7ක්" },
      { name: "කදුරුගස්හේන", diversity: 7, acts: 10, desc: "කාබනික කෘෂිකර්ම, ගෙවතු වගා, පරිසර ඇතුළු ක්ෂේත්‍ර 7ක්" }
    ];

    topGrid.innerHTML = "";
    champs.forEach(c => {
      topGrid.innerHTML += \`
        <div class="glass-panel" style="padding: 1.1rem; border-top: 3px solid #D4AF37;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <strong style="color: #FFF; font-size: 1rem;">\${c.name}</strong>
            <span class="badge" style="background: rgba(212,175,55,0.25); color: #FDE68A; font-weight:800; border: 1px solid #D4AF37;">
              \${c.diversity}/10 ක්ෂේත්‍ර
            </span>
          </div>
          <div style="font-size: 0.8rem; color: #38BDF8; margin-bottom: 0.3rem;">මුළු වැඩසටහන් \${c.acts} ක් තුළ</div>
          <div style="font-size: 0.75rem; color: #CBD5E1; line-height: 1.4;">\${c.desc}</div>
        </div>
      \`;
    });

    // Diversity Tiers Table
    const tiers = [
      { name: "ඉහළම විවිධත්වය (7 - 9 ක්ෂේත්‍ර)", count: 7, pct: 11.1, examples: "හියාචාර උතුර, නුගදූව, ජඹුකැටිය, බදුන්ගොඩ ජනපදය", plan: "ආදර්ශ බහුවිධ සංවර්ධන වසම් ලෙස සම්මාන ලබාදීම හා අත්දැකීම් බෙදාගැනීම." },
      { name: "මධ්‍යස්ථ විවිධත්වය (5 - 6 ක්ෂේත්‍ර)", count: 32, pct: 50.8, examples: "අඹගහවිල, නියාගම, වලහන්දූව, පින්නදූව, බටදූව", plan: "අඩු අවධානයක් ලැබුණු සෞඛ්‍ය හා ඩෙංගු මර්දන ක්ෂේත්‍ර වෙත ව්‍යාප්ත කිරීම." },
      { name: "සාමාන්‍ය විවිධත්වය (3 - 4 ක්ෂේත්‍ර)", count: 21, pct: 33.3, examples: "ඉහළගොඩ බටහිර, අමල්ගම, ගනේගොඩ බටහිර, තල්පගොඩ", plan: "ස්වයං රැකියා හා ප්‍රජා දැනුවත් කිරීමේ නව වැඩසටහන් සැලසුම් කිරීම." },
      { name: "අවධානය අවශ්‍ය (1 - 2 ක්ෂේත්‍ර)", count: 3, pct: 4.8, examples: "දිවුලාන, තලාහිටියාව", plan: "ක්ෂේත්‍ර ප්‍රගති නිලධාරීන්ගේ සෘජු මඟපෙන්වීම යටතේ බහුවිධ වැඩසටහන් හඳුන්වා දීම." }
    ];

    tbody.innerHTML = "";
    tiers.forEach(t => {
      tbody.innerHTML += \`
        <tr>
          <td><strong style="color: #FDE68A;">\${t.name}</strong></td>
          <td style="text-align: center; font-weight: 800; font-size: 1.05rem; color: #FFF;">\${t.count}</td>
          <td style="text-align: center; font-weight: 700;">\${t.pct}%</td>
          <td style="font-size: 0.85rem; color: #CBD5E1;">\${t.examples}</td>
          <td style="font-size: 0.82rem; color: #93C5FD;">\${t.plan}</td>
        </tr>
      \`;
    });

    if (window.pssCharts) {
      window.pssCharts.renderAnDiversityChart(divs);
    }
  }

  // --- SUBTAB 7: COMPARATIVE PERFORMANCE ---
  renderAnCompareSubtab() {
    const selA = document.getElementById("anCompareSelectA");
    const selB = document.getElementById("anCompareSelectB");
    const container = document.getElementById("anCompareResultsContainer");
    if (!selA || !selB || !container) return;

    const valA = selA.value;
    const valB = selB.value;
    const mode = this.anCompareMode;

    let itemA = null;
    let itemB = null;

    if (mode === "division") {
      const divs = this.data.gnDivisions || [];
      itemA = divs.find(d => d.nameSi === valA) || divs[0];
      itemB = divs.find(d => d.nameSi === valB) || divs[1];
    } else if (mode === "month") {
      const months = this.data.monthlyStats || [];
      itemA = months.find(m => m.monthKey === valA) || months[0];
      itemB = months.find(m => m.monthKey === valB) || months[1];
    } else {
      const cats = this.data.analyticalCategories || [];
      itemA = cats.find(c => c.id === valA) || cats[0];
      itemB = cats.find(c => c.id === valB) || cats[1];
    }

    if (!itemA || !itemB) return;

    // Helper to calculate difference badge
    const diffPill = (numA, numB) => {
      if (numA === numB) return '<span class="an-diff-pill equal">සමානයි</span>';
      const pct = (((numA - numB) / (numB || 1)) * 100).toFixed(1);
      if (numA > numB) return \`<span class="an-diff-pill better"><i class="bi bi-arrow-up"></i> +\${pct}% වැඩි</span>\`;
      return \`<span class="an-diff-pill worse"><i class="bi bi-arrow-down"></i> \${pct}% අඩු</span>\`;
    };

    let metricsHtml = "";
    if (mode === "division") {
      metricsHtml = \`
        <div class="an-compare-grid">
          <!-- Entity A Card -->
          <div class="an-entity-card entity-a">
            <div>
              <span class="glass-badge gold" style="margin-bottom: 0.4rem;">පළමු වසම (A)</span>
              <h3 style="font-size: 1.3rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">\${itemA.nameSi}</h3>
              <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 1rem;">\${itemA.sabhaNameSi}</div>
            </div>
            <div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">මුළු වැඩසටහන්:</span>
                <strong style="font-size: 1.15rem; color: #FDE68A;">\${itemA.totalProjects}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">සම්පූර්ණ වූ:</span>
                <strong style="color: #6EE7B7;">\${itemA.completed}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ක්‍රියාකාරී දින:</span>
                <strong style="color: #FFF;">\${itemA.activeDays}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ක්ෂේත්‍ර විවිධත්වය:</span>
                <strong style="color: #38BDF8;">\${itemA.diversity} / 10</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ප්‍රතිලාභීන්:</span>
                <strong style="color: #FFF;">\${(itemA.beneficiaries || 0).toLocaleString()}</strong>
              </div>
            </div>
          </div>

          <!-- VS Badge & Comparison Differences -->
          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.8rem; padding: 0.5rem 0;">
            <div class="an-compare-vs-badge">VS</div>
            <div style="display: flex; flex-direction: column; gap: 0.6rem; align-items: center;">
              \${diffPill(itemA.totalProjects, itemB.totalProjects)}
              \${diffPill(itemA.diversity, itemB.diversity)}
              \${diffPill(itemA.activeDays, itemB.activeDays)}
            </div>
          </div>

          <!-- Entity B Card -->
          <div class="an-entity-card entity-b">
            <div>
              <span class="glass-badge blue" style="margin-bottom: 0.4rem;">දෙවන වසම (B)</span>
              <h3 style="font-size: 1.3rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">\${itemB.nameSi}</h3>
              <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 1rem;">\${itemB.sabhaNameSi}</div>
            </div>
            <div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">මුළු වැඩසටහන්:</span>
                <strong style="font-size: 1.15rem; color: #38BDF8;">\${itemB.totalProjects}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">සම්පූර්ණ වූ:</span>
                <strong style="color: #6EE7B7;">\${itemB.completed}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ක්‍රියාකාරී දින:</span>
                <strong style="color: #FFF;">\${itemB.activeDays}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ක්ෂේත්‍ර විවිධත්වය:</span>
                <strong style="color: #38BDF8;">\${itemB.diversity} / 10</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ප්‍රතිලාභීන්:</span>
                <strong style="color: #FFF;">\${(itemB.beneficiaries || 0).toLocaleString()}</strong>
              </div>
            </div>
          </div>
        </div>
      \`;
    } else if (mode === "month") {
      metricsHtml = \`
        <div class="an-compare-grid">
          <div class="an-entity-card entity-a">
            <div>
              <span class="glass-badge gold" style="margin-bottom: 0.4rem;">පළමු මාසය (A)</span>
              <h3 style="font-size: 1.3rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">\${itemA.monthSi}</h3>
            </div>
            <div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වැඩසටහන් ගණන:</span><strong style="color: #FDE68A; font-size: 1.15rem;">\${itemA.count}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">ක්‍රියාකාරී දින:</span><strong style="color: #FFF;">\${itemA.activeDays}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වාර්තා කළ වසම්:</span><strong style="color: #FFF;">\${itemA.reportingDivisions}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වියදම:</span><strong style="color: #CBD5E1;">රු. \${((itemA.spentLKR || 0) / 1000000).toFixed(2)}M</strong></div>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.8rem;">
            <div class="an-compare-vs-badge">VS</div>
            <div style="display: flex; flex-direction: column; gap: 0.6rem; align-items: center;">
              \${diffPill(itemA.count, itemB.count)}
              \${diffPill(itemA.activeDays, itemB.activeDays)}
            </div>
          </div>

          <div class="an-entity-card entity-b">
            <div>
              <span class="glass-badge blue" style="margin-bottom: 0.4rem;">දෙවන මාසය (B)</span>
              <h3 style="font-size: 1.3rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">\${itemB.monthSi}</h3>
            </div>
            <div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වැඩසටහන් ගණන:</span><strong style="color: #38BDF8; font-size: 1.15rem;">\${itemB.count}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">ක්‍රියාකාරී දින:</span><strong style="color: #FFF;">\${itemB.activeDays}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වාර්තා කළ වසම්:</span><strong style="color: #FFF;">\${itemB.reportingDivisions}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වියදම:</span><strong style="color: #CBD5E1;">රු. \${((itemB.spentLKR || 0) / 1000000).toFixed(2)}M</strong></div>
            </div>
          </div>
        </div>
      \`;
    } else {
      metricsHtml = \`
        <div class="an-compare-grid">
          <div class="an-entity-card entity-a">
            <div>
              <span class="glass-badge gold" style="margin-bottom: 0.4rem;">පළමු ක්ෂේත්‍රය (A)</span>
              <h3 style="font-size: 1.25rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">\${itemA.nameSi}</h3>
            </div>
            <div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වැඩසටහන්:</span><strong style="color: #FDE68A; font-size: 1.2rem;">\${itemA.count}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">සමස්ත %:</span><strong style="color: #FFF;">\${itemA.pct}%</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">විස්තරය:</span><span style="font-size: 0.76rem; color: #CBD5E1;">\${itemA.desc}</span></div>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.8rem;">
            <div class="an-compare-vs-badge">VS</div>
            \${diffPill(itemA.count, itemB.count)}
          </div>

          <div class="an-entity-card entity-b">
            <div>
              <span class="glass-badge blue" style="margin-bottom: 0.4rem;">දෙවන ක්ෂේත්‍රය (B)</span>
              <h3 style="font-size: 1.25rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">\${itemB.nameSi}</h3>
            </div>
            <div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වැඩසටහන්:</span><strong style="color: #38BDF8; font-size: 1.2rem;">\${itemB.count}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">සමස්ත %:</span><strong style="color: #FFF;">\${itemB.pct}%</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">විස්තරය:</span><span style="font-size: 0.76rem; color: #CBD5E1;">\${itemB.desc}</span></div>
            </div>
          </div>
        </div>
      \`;
    }

    container.innerHTML = metricsHtml;

    if (window.pssCharts) {
      window.pssCharts.renderAnCompareChart(itemA, itemB, mode);
    }
  }

  // --- SUBTAB 8: DEEP DIVE & INTEGRITY ---
  renderAnDeepdiveSubtab(filtered = null) {
    if (window.pssCharts) {
      window.pssCharts.renderAnDeepdiveFinChart(filtered?.divisions || this.data.gnDivisions);
    }
  }
`;

let appCode = fs.readFileSync('js/app.js', 'utf8');

// Update Tab Title for analytics
appCode = appCode.replace('analytics: "සංඛ්‍යාලේඛන හා විශ්ලේෂණ"', 'analytics: "ප්‍රගති විශ්ලේෂණය"');
appCode = appCode.replace('analytics: "sector"', 'analytics: "cumulative"');

// Add this.initAnalyticsTab() call in init()
if (!appCode.includes('this.initAnalyticsTab();')) {
  appCode = appCode.replace(
    'this.initReportsSystem();',
    'this.initReportsSystem();\n    this.initAnalyticsTab();'
  );
}

// Attach the new analytics methods right before class closing bracket
const classEndIndex = appCode.lastIndexOf('}');
if (classEndIndex !== -1) {
  const updatedCode = appCode.slice(0, classEndIndex) + '\n' + analyticsMethods + '\n}\n' + appCode.slice(classEndIndex + 1);
  fs.writeFileSync('js/app.js', updatedCode, 'utf8');
  console.log('Successfully injected analytics engine methods into js/app.js!');
} else {
  console.error('Could not find closing bracket in js/app.js!');
  process.exit(1);
}
