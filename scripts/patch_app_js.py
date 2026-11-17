import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update tabTitles
old_tab_titles = '''    // Tab titles map for breadcrumbs and header
    this.tabTitles = {
      overview: "සමස්ත ප්‍රගතිය",
      monthly: "මාසික ප්‍රගතිය",
      divisions: "වසම් අනුව ප්‍රගතිය",
      activities: "වැඩසටහන් විස්තර",
      gallery: "ඡායාරූප ගැලරිය",
      analytics: "ප්‍රගති විශ්ලේෂණය",
      reports: "වාර්තා හා බාගත කිරීම්",
      status: "දත්ත යාවත්කාලීන තත්ත්වය"
    };'''

new_tab_titles = '''    // Tab titles map for breadcrumbs and header (7 Authentic Tabs)
    this.tabTitles = {
      overview: "සමස්ත ප්‍රගතිය",
      monthly: "මාසික ප්‍රගතිය",
      divisions: "වසම් අනුව ප්‍රගතිය",
      activities: "වැඩසටහන් විස්තර",
      analytics: "ප්‍රගති විශ්ලේෂණය",
      reports: "වාර්තා හා බාගත කිරීම්",
      status: "දත්ත යාවත්කාලීන තත්ත්වය"
    };'''

assert old_tab_titles in content, "old_tab_titles not found"
content = content.replace(old_tab_titles, new_tab_titles)

# 2. Remove this.renderGalleryTab() from init()
content = content.replace("    this.renderGalleryTab();\n", "")

# 3. Update renderKPIs
old_kpis = '''  renderKPIs() {
    const sec = this.data.secretariatInfo || this.data.overview || {};

    // Total Activities
    const totalActEl = document.getElementById("kpiTotalActivities");
    if (totalActEl) totalActEl.textContent = sec.totalActivities || sec.activeProjects || (this.data.activities?.length) || 287;

    // Completed Activities
    const completedActEl = document.getElementById("kpiCompletedActivities");
    if (completedActEl) completedActEl.textContent = sec.completedProjects || sec.totalActivities || (this.data.activities?.length) || 287;

    // Reporting GN Divisions
    const reportingGnEl = document.getElementById("kpiReportingGNs");
    if (reportingGnEl) reportingGnEl.textContent = `${sec.reportingGnDivisions || 51} / ${sec.totalGNDivisions || 63}`;

    // Beneficiaries
    const beneficiariesEl = document.getElementById("kpiBeneficiaries");
    if (beneficiariesEl) beneficiariesEl.textContent = (sec.totalBeneficiaries || 0).toLocaleString();

    // Budget Spent
    const budgetSpentEl = document.getElementById("kpiBudgetSpent");
    if (budgetSpentEl) {
      const spentM = (sec.spentBudgetLKR / 1000000).toFixed(1);
      budgetSpentEl.textContent = `රු. ${spentM} M`;
    }

    // Overall Completion Rate
    const heroProgressValEl = document.getElementById("heroProgressVal");
    if (heroProgressValEl) heroProgressValEl.textContent = `${sec.overallCompletionRate}%`;

    const heroProgressFill = document.getElementById("heroProgressFill");
    if (heroProgressFill) heroProgressFill.style.width = `${sec.overallCompletionRate}%`;

    // Counts in hero box
    const hpOngoingEl = document.getElementById("hpOngoingCount");
    if (hpOngoingEl) hpOngoingEl.textContent = `${sec.ongoingProjects} වැඩසටහන්`;

    const hpCompletedEl = document.getElementById("hpCompletedCount");
    if (hpCompletedEl) hpCompletedEl.textContent = `${sec.completedProjects} වැඩසටහන්`;

    // Sidebar counts
    const sideActCount = document.getElementById("sideActivitiesBadge");
    if (sideActCount) sideActCount.textContent = sec.activeProjects;

    const sideDivCount = document.getElementById("sideDivisionsBadge");
    if (sideDivCount) sideDivCount.textContent = "63";
  }'''

new_kpis = '''  renderKPIs() {
    const sec = this.data.overview || this.data.secretariatInfo || {};

    // Total Activities (275 unique)
    const totalActEl = document.getElementById("kpiTotalActivities");
    if (totalActEl) totalActEl.textContent = sec.totalActivities || this.data.activities?.length || 275;

    // Reporting GN Divisions (53 / 63)
    const reportingGnEl = document.getElementById("kpiReportingGNs");
    if (reportingGnEl) reportingGnEl.textContent = `${sec.reportingGnDivisions || 53} / ${sec.totalGNDivisions || 63}`;

    // Active Days (113 days)
    const activeDaysEl = document.getElementById("kpiActiveDays");
    if (activeDaysEl) activeDaysEl.textContent = sec.totalActiveDays || 113;

    // Total Verified Photos (666 photos)
    const totalPhotosEl = document.getElementById("kpiTotalPhotos");
    if (totalPhotosEl) totalPhotosEl.textContent = sec.totalPhotos || 666;

    // Overall Completion Rate (100% completed monthly activities)
    const heroProgressValEl = document.getElementById("heroProgressVal");
    if (heroProgressValEl) heroProgressValEl.textContent = "100%";

    const heroProgressFill = document.getElementById("heroProgressFill");
    if (heroProgressFill) heroProgressFill.style.width = "100%";

    // Counts in hero box
    const hpReportingGn = document.getElementById("hpReportingGnCount");
    if (hpReportingGn) hpReportingGn.textContent = `${sec.reportingGnDivisions || 53} / ${sec.totalGNDivisions || 63} වසම්`;

    const hpCompletedEl = document.getElementById("hpCompletedCount");
    if (hpCompletedEl) hpCompletedEl.textContent = `${sec.totalActivities || 275} වැඩසටහන්`;

    // Sidebar counts
    const sideActCount = document.getElementById("sideActivitiesBadge");
    if (sideActCount) sideActCount.textContent = sec.totalActivities || 275;

    const sideDivCount = document.getElementById("sideDivisionsBadge");
    if (sideDivCount) sideDivCount.textContent = "63";
  }'''

assert old_kpis in content, "old_kpis not found"
content = content.replace(old_kpis, new_kpis)

# 4. Update renderMonthlyTab
old_monthly_tab = '''  renderMonthlyTab() {
    const tbody = document.getElementById("monthlyTableBody");
    if (!tbody) return;

    tbody.innerHTML = "";
    (this.data.monthlyStats || []).forEach(m => {
      const tr = document.createElement("tr");
      const targetVal = m.target || m.completed || 1;
      const completionRate = Math.round(((m.completed || 0) / targetVal) * 100);

      tr.innerHTML = `
        <td style="font-weight: 700; color: #FFF;"><i class="bi bi-calendar-event text-gold" style="margin-right: 6px;"></i>${m.monthSi}</td>
        <td style="text-align: center; font-weight: 600;">${m.target || m.completed || 0}</td>
        <td style="text-align: center; color: #10B981; font-weight: 700;">${m.completed || 0}</td>
        <td style="text-align: center; color: #38BDF8; font-weight: 700;">${m.ongoing || 0}</td>
        <td style="font-weight: 600;">${(m.beneficiaries || 0).toLocaleString()} පවුල්</td>
        <td style="font-weight: 600;">${(m.spentLKR || 0) > 0 ? 'රු. ' + (m.spentLKR || 0).toLocaleString() : '-'}</td>
        <td style="font-weight: 600; color: #FDE68A;">${(m.cumulativeSpent || 0) > 0 ? 'රු. ' + (m.cumulativeSpent || 0).toLocaleString() : '-'}</td>
        <td>
          <div class="table-progress-bar">
            <div class="table-progress-fill" style="width: ${completionRate}%; background: #10B981;"></div>
          </div>
          <span style="font-size: 0.78rem; font-weight: 700; color: #10B981;">${completionRate}%</span>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }'''

new_monthly_tab = '''  renderMonthlyTab() {
    const tbody = document.getElementById("monthlyTableBody");
    if (!tbody) return;

    tbody.innerHTML = "";
    (this.data.monthlyStats || []).forEach(m => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td style="font-weight: 700; color: #FFF;"><i class="bi bi-calendar-event text-gold" style="margin-right: 6px;"></i>${m.monthSi}</td>
        <td style="text-align: center; font-weight: 700; color: #10B981;">${m.completed || 0}</td>
        <td style="text-align: center; font-weight: 600; color: #38BDF8;">${m.activeDays || 0} දින</td>
        <td style="text-align: center; font-weight: 600; color: #FDE68A;">${m.reportingDivisions || m.reportingGns || 0}</td>
        <td style="text-align: center; font-weight: 700; color: #FFF;">${m.cumulativeActivities || m.cumulativeTotal || 0}</td>
        <td style="text-align: center;">
          <span class="glass-badge green" style="font-size: 0.74rem;"><i class="bi bi-check-circle-fill"></i> 100% සම්පූර්ණයි</span>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }'''

assert old_monthly_tab in content, "old_monthly_tab not found"
content = content.replace(old_monthly_tab, new_monthly_tab)

# 5. Update renderDivisionsTab
pattern_div_tab = re.compile(r'  renderDivisionsTab\(\) \{.*?this\.init3DTilt\(\);\s*\}', re.DOTALL)

new_div_tab = '''  renderDivisionsTab() {
    // 1. Render Table View for All 63 Divisions
    const tbody = document.getElementById("gnComparisonTableBody");
    if (tbody) {
      tbody.innerHTML = "";
      this.data.gnDivisions.forEach(gn => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>
            <div class="gn-cell-title">
              <span class="gn-cell-name" style="font-weight: 700; color: #FFF;">
                <i class="bi bi-geo-alt-fill text-gold" style="font-size: 0.85rem; margin-right: 5px;"></i>${gn.nameSi}
              </span>
            </div>
          </td>
          <td>
            <span style="font-weight: 600; font-size: 0.86rem; color: #E2E8F0;">${gn.sabhaNameSi}</span>
          </td>
          <td>
            <span class="glass-badge blue" style="font-size: 0.74rem;">${gn.keySectorSi}</span>
          </td>
          <td style="font-weight: 700; text-align: center; color: #10B981;">${gn.totalProjects}</td>
          <td style="font-weight: 600; text-align: center; color: #38BDF8;">${gn.activeDays || 0} දින</td>
          <td style="font-weight: 600; text-align: center; color: #FDE68A;"><i class="bi bi-images"></i> ${gn.totalPhotos || 0}</td>
          <td style="text-align: center;">
            <span class="glass-badge ${gn.totalProjects > 0 ? 'green' : 'blue'}" style="font-size: 0.74rem;">
              <i class="bi ${gn.totalProjects > 0 ? 'bi-check-circle-fill' : 'bi-hourglass-split'}"></i> ${gn.totalProjects > 0 ? 'වාර්තා කර ඇත' : 'පොරොත්තු'}
            </span>
          </td>
          <td style="text-align: center;">
            <button class="btn-gold btn-view-division-act" style="padding: 0.35rem 0.85rem; font-size: 0.78rem;" data-gn-name="${gn.nameSi}">
              <i class="bi bi-eye"></i> වැඩසටහන් බලන්න
            </button>
          </td>
        `;

        tr.querySelector(".btn-view-division-act").addEventListener("click", () => {
          this.openDedicatedDivisionView(gn.nameSi);
        });

        tbody.appendChild(tr);
      });
    }

    // 2. Render Cards Grid View for All 63 Divisions
    const cardsGrid = document.getElementById("divisionCardsGrid");
    if (cardsGrid) {
      cardsGrid.innerHTML = "";
      this.data.gnDivisions.forEach(gn => {
        const card = document.createElement("div");
        card.className = "division-card glass-card-3d";

        card.innerHTML = `
          <div class="div-card-top">
            <div>
              <div class="div-card-name"><i class="bi bi-geo-alt-fill text-gold"></i> ${gn.nameSi}</div>
              <div class="div-card-sabha">${gn.sabhaNameSi}</div>
            </div>
            <span class="glass-badge ${gn.totalProjects > 0 ? 'green' : 'blue'}" style="font-size: 0.74rem;">
              ${gn.totalProjects > 0 ? 'සක්‍රියයි' : 'පොරොත්තු'}
            </span>
          </div>

          <div style="margin-bottom: 0.8rem;">
            <span class="glass-badge blue" style="font-size: 0.74rem;">${gn.keySectorSi}</span>
          </div>

          <div class="div-card-metrics" style="grid-template-columns: repeat(3, 1fr);">
            <div>
              <div style="font-size: 0.72rem; color: #94A3B8;">වැඩසටහන්</div>
              <div style="font-size: 1.1rem; font-weight: 800; color: #10B981;">${gn.totalProjects} ක්</div>
            </div>
            <div>
              <div style="font-size: 0.72rem; color: #94A3B8;">සක්‍රිය දින</div>
              <div style="font-size: 1.1rem; font-weight: 800; color: #38BDF8;">${gn.activeDays || 0} දින</div>
            </div>
            <div>
              <div style="font-size: 0.72rem; color: #94A3B8;">සත්‍ය ඡායාරූප</div>
              <div style="font-size: 1.1rem; font-weight: 800; color: #FDE68A;"><i class="bi bi-images"></i> ${gn.totalPhotos || 0}</div>
            </div>
          </div>

          <div class="progress-track" style="height: 6px; margin: 0.8rem 0;">
            <div class="progress-fill shimmer-bar" style="width: ${gn.totalProjects > 0 ? 100 : 0}%; background: #10B981;"></div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 0.8rem;">
            <span style="font-size: 0.74rem; color: #94A3B8;">
              <i class="bi bi-clock-history"></i> ${gn.lastReportDate || "-"}
            </span>
            <button class="btn-gold" style="padding: 0.35rem 0.85rem; font-size: 0.76rem;">
              <i class="bi bi-arrow-right-circle"></i> වැඩසටහන් හා ඡායාරූප
            </button>
          </div>
        `;

        card.addEventListener("click", () => {
          this.openDedicatedDivisionView(gn.nameSi);
        });

        cardsGrid.appendChild(card);
      });
    }

    this.init3DTilt();
  }'''

assert pattern_div_tab.search(content), "renderDivisionsTab pattern not found"
content = pattern_div_tab.sub(new_div_tab, content)

# 6. Helper for rendering Activity Card with Direct Photo Gallery on the page
activity_card_helper = '''  // --- Activity Card Builder with Direct Photo Gallery on the Page ---
  createActivityCardElement(act) {
    const card = document.createElement("div");
    card.className = "activity-card glass-card-3d";
    card.setAttribute("data-act-id", act.id);

    const photos = act.photoObjects || (act.images || []).map((url, i) => ({
      id: `${act.id}-p${i}`,
      thumbnail: url,
      full: url,
      driveUrl: url
    }));
    const photoCount = photos.length;

    let galleryMarkup = "";
    if (photoCount === 0) {
      galleryMarkup = `
        <div class="activity-no-photos">
          <i class="bi bi-card-image" style="font-size: 1.8rem; color: #475569;"></i>
          <span style="font-size: 0.78rem; color: #64748B;">ඡායාරූප අමුණා නැත</span>
        </div>
      `;
    } else if (photoCount === 1) {
      galleryMarkup = `
        <div class="activity-card-gallery single">
          <div class="act-photo-item" data-photo-idx="0" title="විශාල කර බලන්න">
            <img src="${photos[0].thumbnail || photos[0].full}" alt="${act.titleSi}" loading="lazy" class="act-photo-img" />
            <div class="act-photo-zoom-overlay"><i class="bi bi-arrows-fullscreen"></i></div>
          </div>
        </div>
      `;
    } else if (photoCount === 2) {
      galleryMarkup = `
        <div class="activity-card-gallery two-grid">
          ${photos.map((p, idx) => `
            <div class="act-photo-item" data-photo-idx="${idx}" title="විශාල කර බලන්න">
              <img src="${p.thumbnail || p.full}" alt="${act.titleSi}" loading="lazy" class="act-photo-img" />
              <div class="act-photo-zoom-overlay"><i class="bi bi-arrows-fullscreen"></i></div>
            </div>
          `).join("")}
        </div>
      `;
    } else if (photoCount === 3) {
      galleryMarkup = `
        <div class="activity-card-gallery three-grid">
          ${photos.map((p, idx) => `
            <div class="act-photo-item" data-photo-idx="${idx}" title="විශාල කර බලන්න">
              <img src="${p.thumbnail || p.full}" alt="${act.titleSi}" loading="lazy" class="act-photo-img" />
              <div class="act-photo-zoom-overlay"><i class="bi bi-arrows-fullscreen"></i></div>
            </div>
          `).join("")}
        </div>
      `;
    } else {
      galleryMarkup = `
        <div class="activity-card-gallery four-grid">
          ${photos.slice(0, 4).map((p, idx) => `
            <div class="act-photo-item" data-photo-idx="${idx}" title="විශාල කර බලන්න">
              <img src="${p.thumbnail || p.full}" alt="${act.titleSi}" loading="lazy" class="act-photo-img" />
              ${idx === 3 && photoCount > 4 
                ? `<div class="act-photo-more-badge">+${photoCount - 4}</div>` 
                : `<div class="act-photo-zoom-overlay"><i class="bi bi-arrows-fullscreen"></i></div>`}
            </div>
          `).join("")}
        </div>
      `;
    }

    card.innerHTML = `
      <div class="activity-card-header">
        <span class="glass-badge gold" title="${act.gnNameSi}">
          <i class="bi bi-geo-alt-fill"></i> ${act.gnNameSi}
        </span>
        <span class="glass-badge green">
          <i class="bi bi-check-circle-fill"></i> සම්පූර්ණයි
        </span>
      </div>

      ${galleryMarkup}

      <div class="activity-body">
        <div class="activity-meta-row">
          <span><i class="bi bi-calendar3"></i> ${act.date}</span>
          <span>•</span>
          <span><i class="bi bi-tag-fill"></i> ${act.categoryNameSi}</span>
          <span>•</span>
          <span style="color: #FDE68A;"><i class="bi bi-images"></i> ඡායාරූප ${photoCount}</span>
        </div>

        <h3 class="activity-title">${act.titleSi}</h3>

        <div class="activity-desc-box">
          <div style="font-size: 0.76rem; color: #94A3B8; margin-bottom: 0.3rem; display: flex; align-items: center; gap: 0.3rem;">
            <i class="bi bi-file-text text-gold"></i> සිදු කළ කාර්යය / විස්තරය:
          </div>
          <p class="activity-desc" style="color: #E2E8F0; font-size: 0.88rem; line-height: 1.6; margin: 0;">${act.description || act.titleSi}</p>
        </div>

        <div class="activity-footer">
          <span class="activity-sabha" title="${act.sabhaNameSi}">
            <i class="bi bi-building"></i> ${act.sabhaNameSi}
          </span>
          <button class="btn-gold btn-open-act-modal" style="padding: 0.45rem 1rem; font-size: 0.82rem;" data-act-id="${act.id}">
            <i class="bi bi-eye"></i> සවිස්තර වාර්තාව
          </button>
        </div>
      </div>
    `;

    // Bind Lightbox click for each photo item
    const photoItems = card.querySelectorAll(".act-photo-item");
    photoItems.forEach(item => {
      item.addEventListener("click", () => {
        const photoIdx = parseInt(item.getAttribute("data-photo-idx") || "0", 10);
        // Open lightbox with all photos from this activity
        const actPhotosForLightbox = photos.map(p => ({
          url: p.full || p.thumbnail,
          titleSi: act.titleSi,
          gnDivision: act.gnNameSi,
          date: act.date,
          sabhaNameSi: act.sabhaNameSi,
          categoryNameSi: act.categoryNameSi,
          actId: act.id
        }));
        this.openLightbox(photoIdx, actPhotosForLightbox);
      });
    });

    // Bind Full Modal button
    const modalBtn = card.querySelector(".btn-open-act-modal");
    if (modalBtn) {
      modalBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        this.openModal(act);
      });
    }

    return card;
  }
'''

# 7. Update openDedicatedDivisionView
pattern_ded_view = re.compile(r'  openDedicatedDivisionView\(gnName\) \{.*?this\.init3DTilt\(\);\s*\}', re.DOTALL)

new_ded_view = '''  openDedicatedDivisionView(gnName) {
    this.selectedDedicatedDivision = gnName;
    const gnData = this.data.gnDivisions.find(g => g.nameSi === gnName);
    if (!gnData) return;

    // Show dedicated division view and hide all-divisions list view
    const dedicatedView = document.getElementById("divisionDedicatedView");
    const allDivView = document.getElementById("divisionAllListView");

    if (dedicatedView) dedicatedView.style.display = "block";
    if (allDivView) allDivView.style.display = "none";

    // Populate dedicated division banner
    document.getElementById("dedicatedDivisionName").textContent = `${gnData.nameSi} ග්‍රාම නිලධාරී වසම`;
    document.getElementById("dedicatedDivisionSabha").textContent = gnData.sabhaNameSi;
    document.getElementById("dedicatedDivisionSector").innerHTML = `<i class="bi bi-tag-fill"></i> ${gnData.keySectorSi}`;
    document.getElementById("dedicatedDivisionStatus").innerHTML = `<i class="bi bi-check-circle-fill"></i> ${gnData.totalProjects > 0 ? 'වාර්තා කර ඇත' : 'පොරොත්තු'}`;
    document.getElementById("dedicatedDivisionProgressVal").textContent = gnData.totalProjects > 0 ? "100%" : "0%";
    document.getElementById("dedicatedDivisionProgressFill").style.width = gnData.totalProjects > 0 ? "100%" : "0%";
    document.getElementById("dedicatedDivisionTotalAct").textContent = `${gnData.totalProjects} වැඩසටහන්`;
    
    const actDaysEl = document.getElementById("dedicatedDivisionActiveDays");
    if (actDaysEl) actDaysEl.textContent = `${gnData.activeDays || 0} දින`;
    
    const photosEl = document.getElementById("dedicatedDivisionPhotos");
    if (photosEl) photosEl.textContent = `${gnData.totalPhotos || 0} ඡායාරූප`;

    // Filter activities belonging ONLY to this division
    const divisionActivities = this.data.activities.filter(a => a.gnNameSi === gnName);
    const actsHeading = document.getElementById("dedicatedDivisionActivitiesHeading");
    const countBadge = document.getElementById("dedicatedDivisionActCountBadge");
    const grid = document.getElementById("dedicatedDivisionActivitiesGrid");

    if (actsHeading) {
      actsHeading.textContent = `${gnData.nameSi} වසමේ සංවර්ධන වැඩසටහන් හා ඡායාරූප`;
    }
    if (countBadge) {
      countBadge.textContent = `වැඩසටහන් ${divisionActivities.length}ක්`;
    }

    if (grid) {
      grid.innerHTML = "";

      if (divisionActivities.length === 0) {
        grid.innerHTML = `
          <div class="glass-panel" style="grid-column: 1 / -1; padding: 2.2rem; text-align: center; border-color: rgba(212, 175, 55, 0.25);">
            <div style="font-size: 2.5rem; color: #FDE68A; margin-bottom: 0.8rem;"><i class="bi bi-folder-check"></i></div>
            <h4 style="font-size: 1.25rem; font-weight: 700; color: #FFF; margin-bottom: 0.5rem;">
              ${gnData.nameSi} වසමේ සංවර්ධන කාර්යයන් ක්ෂේත්‍ර මට්ටමින් ක්‍රියාත්මක වේ
            </h4>
            <p style="color: #CBD5E1; max-width: 650px; margin: 0 auto 1.4rem; font-size: 0.92rem; line-height: 1.7;">
              ${gnData.sabhaNameSi} යටතේ වැඩසටහන් සැලසුම් කර ඇති අතර, ඉදිරි මාසික දත්ත යාවත්කාලීන කිරීමේදී සවිස්තර ඡායාරූප හා තොරතුරු පද්ධතියට ඇතුළත් කරනු ලැබේ.
            </p>
            <button class="btn-gold" onclick="window.pssApp.printDivisionReport('${gnData.nameSi}')">
              <i class="bi bi-printer"></i> මෙම වසමේ නිල ප්‍රගති වාර්තාව මුද්‍රණය කරන්න (Print / PDF)
            </button>
          </div>
        `;
      } else {
        divisionActivities.forEach(act => {
          const cardEl = this.createActivityCardElement(act);
          grid.appendChild(cardEl);
        });
      }
    }

    // Scroll to dedicated container smoothly
    dedicatedView.scrollIntoView({ behavior: "smooth", block: "start" });
    this.init3DTilt();
  }'''

assert pattern_ded_view.search(content), "openDedicatedDivisionView pattern not found"
content = pattern_ded_view.sub(new_ded_view, content)

# 8. Update renderActivitiesTab
pattern_act_tab = re.compile(r'  renderActivitiesTab\(\) \{.*?this\.init3DTilt\(\);\s*\}', re.DOTALL)

new_act_tab = '''  renderActivitiesTab() {
    const grid = document.getElementById("activitiesGrid");
    const countEl = document.getElementById("activityResultsCount");

    if (countEl) {
      countEl.textContent = `ප්‍රජා සංවර්ධන වැඩසටහන් ${this.filteredActivities.length}ක් පෙන්වනු ලැබේ (නවතම පළමුව)`;
    }

    if (!grid) return;

    if (this.filteredActivities.length === 0) {
      grid.innerHTML = `
        <div class="no-results-box">
          <i class="bi bi-search"></i>
          <h4 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.6rem; color: #FFF;">
            ගැලපෙන සංවර්ධන වැඩසටහන් හමු නොවීය
          </h4>
          <p style="color: #94A3B8; font-size: 0.92rem;">
            කරුණාකර ඔබගේ සෙවුම් පද හෝ පෙරහන් වෙනස් කර නැවත උත්සාහ කරන්න.
          </p>
        </div>
      `;
      return;
    }

    grid.innerHTML = "";
    this.filteredActivities.forEach(act => {
      const cardEl = this.createActivityCardElement(act);
      grid.appendChild(cardEl);
    });

    this.init3DTilt();
  }'''

assert pattern_act_tab.search(content), "renderActivitiesTab pattern not found"
content = pattern_act_tab.sub(new_act_tab, content)

# Insert activity_card_helper right before renderActivitiesTab
content = content.replace("  renderActivitiesTab() {", activity_card_helper + "\n  renderActivitiesTab() {")

# 9. Update openModal(activity)
pattern_modal = re.compile(r'  openModal\(activity\) \{.*?document\.body\.style\.overflow = "hidden";\s*\}', re.DOTALL)

new_modal = '''  openModal(activity) {
    this.currentModalActivity = activity;
    this.currentModalImgIndex = 0;

    const modal = document.getElementById("activityModalOverlay");
    if (!modal) return;

    this.updateModalSlide();

    // 1. වැඩසටහනේ නම
    const titleEl = document.getElementById("modalActivityTitle");
    if (titleEl) titleEl.textContent = activity.titleSi;
    const gnBadge = document.getElementById("modalGnBadge");
    if (gnBadge) gnBadge.textContent = activity.gnNameSi;
    const statusBadge = document.getElementById("modalStatusBadge");
    if (statusBadge) statusBadge.textContent = "100% සම්පූර්ණයි";
    const catBadge = document.getElementById("modalCategoryBadge");
    if (catBadge) catBadge.textContent = activity.categoryNameSi || "ප්‍රජා සංවර්ධන";
    const sabhaBadge = document.getElementById("modalSabhaBadge");
    if (sabhaBadge) sabhaBadge.textContent = activity.sabhaNameSi;

    // 2. පැවැත්වූ දිනය
    const dateVal = document.getElementById("modalDateVal");
    if (dateVal) dateVal.textContent = activity.date;

    // 3. ග්‍රාම නිලධාරී වසම
    const gnVal = document.getElementById("modalGNDivisionVal");
    if (gnVal) gnVal.textContent = activity.gnNameSi;

    // 4. ප්‍රජා සංවර්ධන සභාව
    const sabhaVal = document.getElementById("modalSabhaVal");
    if (sabhaVal) sabhaVal.textContent = activity.sabhaNameSi;

    // 5. සිදු කරන ලද කාර්යය / විස්තරය
    const actionsVal = document.getElementById("modalActionsVal");
    if (actionsVal) actionsVal.textContent = activity.description || activity.titleSi;

    // 6. සත්‍ය ක්ෂේත්‍ර ඡායාරූප ගැලරිය
    const photosContainer = document.getElementById("modalPhotosContainer");
    const photos = activity.photoObjects || (activity.images || []).map((url, i) => ({
      id: `${activity.id}-m${i}`,
      thumbnail: url,
      full: url,
      driveUrl: url
    }));

    if (photosContainer) {
      photosContainer.innerHTML = "";
      if (photos.length === 0) {
        photosContainer.innerHTML = `<span style="color: #94A3B8; font-size: 0.88rem;">ඡායාරූප අමුණා නැත.</span>`;
      } else {
        photos.forEach((p, idx) => {
          const item = document.createElement("div");
          item.className = "act-photo-item";
          item.style.height = "130px";
          item.title = "විශාල කර බලන්න";
          item.innerHTML = `
            <img src="${p.thumbnail || p.full}" alt="${activity.titleSi}" class="act-photo-img" loading="lazy" />
            <div class="act-photo-zoom-overlay"><i class="bi bi-arrows-fullscreen"></i></div>
          `;
          item.addEventListener("click", () => {
            const actPhotosForLightbox = photos.map(ph => ({
              url: ph.full || ph.thumbnail,
              titleSi: activity.titleSi,
              gnDivision: activity.gnNameSi,
              date: activity.date,
              sabhaNameSi: activity.sabhaNameSi,
              categoryNameSi: activity.categoryNameSi,
              actId: activity.id
            }));
            this.openLightbox(idx, actPhotosForLightbox);
          });
          photosContainer.appendChild(item);
        });
      }
    }

    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  }'''

assert pattern_modal.search(content), "openModal pattern not found"
content = pattern_modal.sub(new_modal, content)

# 10. Update renderAnMonthlySubtab table rows
old_an_monthly_rows = '''      tbody.innerHTML += `
        <tr style="${rowStyle}">
          <td>
            <strong>${m.monthSi}</strong>
            ${isAug ? ' <span class="glass-badge gold" style="font-size:0.68rem; padding: 0.15rem 0.4rem;">උපරිම මාසය</span>' : ''}
            ${isSep ? ' <span class="glass-badge blue" style="font-size:0.68rem; padding: 0.15rem 0.4rem;">වත්මන් මාසය</span>' : ''}
          </td>
          <td style="text-align: center; font-weight: 800; font-size: 1.05rem;" class="${isAug ? 'gold-text-gradient' : 'text-gold'}">${m.count}</td>
          <td style="text-align: center; color: #6EE7B7;">${m.completed}</td>
          <td style="text-align: center; color: #60A5FA;">${m.ongoing}</td>
          <td style="text-align: center; font-weight: 600;">${m.activeDays}</td>
          <td style="text-align: center; font-weight: 600;">${m.reportingDivisions}</td>
          <td style="text-align: center;">${momBadge}</td>
          <td>${(m.beneficiaries || 0).toLocaleString()}</td>
          <td style="color: #CBD5E1;">රු. ${((m.spentLKR || 0) / 1000000).toFixed(2)}M</td>
          <td style="font-weight: 700; color: #FDE68A;">රු. ${((m.cumulativeSpent || 0) / 1000000).toFixed(2)}M</td>
        </tr>
      `;'''

new_an_monthly_rows = '''      tbody.innerHTML += `
        <tr style="${rowStyle}">
          <td>
            <strong>${m.monthSi}</strong>
            ${isAug ? ' <span class="glass-badge gold" style="font-size:0.68rem; padding: 0.15rem 0.4rem;">උපරිම මාසය</span>' : ''}
            ${isSep ? ' <span class="glass-badge blue" style="font-size:0.68rem; padding: 0.15rem 0.4rem;">වත්මන් මාසය</span>' : ''}
          </td>
          <td style="text-align: center; font-weight: 800; font-size: 1.05rem;" class="${isAug ? 'gold-text-gradient' : 'text-gold'}">${m.count || m.completed || 0}</td>
          <td style="text-align: center; font-weight: 600; color: #38BDF8;">${m.activeDays || 0} දින</td>
          <td style="text-align: center; font-weight: 600; color: #FDE68A;">${m.reportingDivisions || m.reportingGns || 0}</td>
          <td style="text-align: center;">${momBadge}</td>
          <td style="text-align: center; font-weight: 700; color: #FFF;">${m.cumulativeActivities || m.cumulativeTotal || 0}</td>
          <td style="text-align: center;">
            <span class="glass-badge green" style="font-size: 0.72rem;"><i class="bi bi-check-circle-fill"></i> 100% සම්පූර්ණයි</span>
          </td>
        </tr>
      `;'''

assert old_an_monthly_rows in content, "old_an_monthly_rows not found"
content = content.replace(old_an_monthly_rows, new_an_monthly_rows)

# 11. Update renderAnDivisionsSubtab table rows
old_an_div_rows = '''      tbody.innerHTML += `
        <tr>
          <td style="text-align: center;">${rankBadge}</td>
          <td>
            <strong style="color: #FFF; font-size: 0.95rem;">${d.nameSi}</strong>
            <div style="font-size: 0.74rem; color: #94A3B8;">${d.sabhaNameSi}</div>
          </td>
          <td><span class="glass-badge blue" style="font-size: 0.74rem;">${d.keySectorSi}</span></td>
          <td style="text-align: center; font-weight: 800; font-size: 1.1rem; color: #FDE68A;">${d.totalProjects}</td>
          <td style="text-align: center; color: #6EE7B7; font-weight: 700;">${d.completed}</td>
          <td style="text-align: center; color: #60A5FA;">${d.ongoing}</td>
          <td style="text-align: center;">${diversityStars}</td>
          <td style="text-align: center; font-weight: 600;">${d.activeDays}</td>
          <td>${(d.beneficiaries || 0).toLocaleString()}</td>
          <td>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="font-size: 0.78rem; font-weight: 700; color: #FFF; width: 35px;">${d.progress}%</span>
              <div class="progress-track" style="width: 60px; height: 6px;">
                <div class="progress-fill" style="width: ${d.progress}%;"></div>
              </div>
            </div>
          </td>
          <td style="text-align: center;">${statusBadge}</td>
        </tr>
      `;'''

new_an_div_rows = '''      tbody.innerHTML += `
        <tr>
          <td style="text-align: center;">${rankBadge}</td>
          <td>
            <strong style="color: #FFF; font-size: 0.95rem;">${d.nameSi}</strong>
            <div style="font-size: 0.74rem; color: #94A3B8;">${d.sabhaNameSi}</div>
          </td>
          <td><span class="glass-badge blue" style="font-size: 0.74rem;">${d.keySectorSi}</span></td>
          <td style="text-align: center; font-weight: 800; font-size: 1.1rem; color: #10B981;">${d.totalProjects}</td>
          <td style="text-align: center;">${diversityStars}</td>
          <td style="text-align: center; font-weight: 600; color: #38BDF8;">${d.activeDays || 0} දින</td>
          <td style="text-align: center; font-weight: 600; color: #FDE68A;"><i class="bi bi-images"></i> ${d.totalPhotos || 0}</td>
          <td style="text-align: center;">${statusBadge}</td>
        </tr>
      `;'''

assert old_an_div_rows in content, "old_an_div_rows not found"
content = content.replace(old_an_div_rows, new_an_div_rows)

# 12. Remove "ශ්‍රී ලංකා ප්‍රජාතාන්ත්‍රික සමාජවාදී ජනරජය"
content = content.replace("ශ්‍රී ලංකා ප්‍රජාතාන්ත්‍රික සමාජවාදී ජනරජය", "අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - ප්‍රජා සංවර්ධන සභා")

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched js/app.js!")
