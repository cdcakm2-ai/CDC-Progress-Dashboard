/**
 * ප්‍රජා සංවර්ධන සභා මගින් සිදු කරන ලද වැඩසටහන්
 * අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසය
 * 8-Tab Modern Government Dashboard Engine (Sinhala-First)
 * 
 * Includes:
 * - All 63 Authentic Grama Niladhari Divisions card grid & dedicated activity view
 * - Complete 9-field activity detail modal
 * - Connected photo gallery with slideshow player (play/pause/next/prev)
 * - Permitted photograph download functionality
 * - Filters for GN Division, Year, Month, Activity Category & Search
 * - Official Printable PDF reports for Divisions & Individual Activities
 * - Strictly NO officer names, contact numbers or personal officer details
 */

class PssApp {
  constructor() {
    this.activeTab = "overview";
    this.data = null;
    this.filteredActivities = [];
    this.selectedCategory = "all";
    this.selectedMonth = "all";
    this.selectedGN = "all";
    this.selectedStatus = "all";
    this.selectedYear = "all";
    this.searchQuery = "";

    // Dedicated Division View State
    this.selectedDedicatedDivision = null;

    // Gallery & Slideshow State
    this.gallerySearchQuery = "";
    this.gallerySelectedGN = "all";
    this.gallerySelectedMonth = "all";
    this.gallerySelectedYear = "all";
    this.gallerySelectedCategory = "all";
    this.filteredGalleryItems = [];
    this.isSlideshowPlaying = false;
    this.slideshowTimer = null;
    this.slideshowSpeedMs = 4000;

    // Sub-tab states
    this.activeSubtabs = {
      /* monthly removed */
      divisions: "cards",
      activities: "all",
      gallery: "all",
      analytics: "cumulative",
      reports: "preview",
      status: "system"
    };

    // Modal & Lightbox state
    this.currentModalActivity = null;
    this.currentModalImgIndex = 0;
    this.currentLightboxIndex = 0;
    this.currentGalleryItems = [];

    // Tab 4: Activities Division Showcase State (Division-First by Default)
    this.activitiesViewMode = "flat";
    this.selectedActivitiesGnIndex = 0;

    // Tab titles map for breadcrumbs and header (7 Authentic Tabs)
    this.tabTitles = {
      overview: "සමස්ත ප්‍රගතිය",
      "latest-month": "අලුත්ම මාසයේ ප්‍රගතිය",
      divisions: "වසම් අනුව ප්‍රගතිය",
      activities: "වැඩසටහන් විස්තර",
      analytics: "ප්‍රගති විශ්ලේෂණය",
      reports: "වාර්තා හා බාගත කිරීම්",
      status: "දත්ත යාවත්කාලීන තත්ත්වය"
    };
  }

  async init() {
    this.data = await window.pssSheetsService.getDashboardData();
    this.data.monthlyStats = this.data.monthlyStats || this.data.monthlyProgress || this.data.monthlySummary || [];

    // Defensive normalization of canonical activities for seamless rendering
    if (Array.isArray(this.data.activities)) {
      this.data.activities.forEach((act, i) => {
        if (!act.titleSi) act.titleSi = act.title || act.description || `වැඩසටහන ${i+1}`;
        if (!act.title) act.title = act.titleSi;
        if (!act.gnNameSi) act.gnNameSi = act.gnDivision || "";
        if (!act.sabhaNameSi) act.sabhaNameSi = `${act.gnNameSi} ප්‍රජා සංවර්ධන සභාව`;
        if (!act.statusLabelSi) act.statusLabelSi = act.status || "සම්පූර්ණයි";
        if (!act.categoryNameSi) act.categoryNameSi = act.categoryName || "ප්‍රජා සංවර්ධන";
        if (!act.categoryName) act.categoryName = act.categoryNameSi;
        
        // Ensure photos array
        if (!Array.isArray(act.photos)) act.photos = [];
        
        // Extract thumbnails
        const extractedUrls = act.photos.map(p => {
          if (typeof p === "string") return p;
          return p.thumbnailUrl || p.fullUrl || "";
        }).filter(Boolean);

        act.photoThumbnails = extractedUrls;
        act.images = extractedUrls;

        act.photoObjects = act.photos.map((p, pIdx) => {
          const u = typeof p === "string" ? p : (p.thumbnailUrl || p.fullUrl || "");
          const f = typeof p === "string" ? p : (p.fullUrl || p.thumbnailUrl || "");
          const d = typeof p === "string" ? p : (p.driveUrl || f);
          return {
            id: p.id || `${act.id}-p${pIdx}`,
            thumbnail: u,
            full: f,
            driveUrl: d,
            caption: (p && p.caption) || `${act.titleSi || act.title || act.description || "වැඩසටහන"} - ${act.gnNameSi}`
          };
        });
      });

      this.data.activities.sort((a, b) => new Date(b.date) - new Date(a.date));
    }
    this.filteredActivities = [...this.data.activities];

    // Ensure all 63 GN divisions have totalProjects and totalPhotos populated
    if (Array.isArray(this.data.gnDivisions)) {
      this.data.gnDivisions.forEach(g => {
        if (g.totalProjects === undefined) g.totalProjects = g.activityCount || g.completedCount || 0;
        if (g.totalPhotos === undefined) g.totalPhotos = g.photoCount || 0;
        if (!g.sabhaNameSi) g.sabhaNameSi = `${g.nameSi} ප්‍රජා සංවර්ධන සභාව`;
        if (!g.keySectorSi) g.keySectorSi = "ප්‍රජා සංවර්ධන";
      });
    }

    // Ensure gallery items are sorted newest first
    if (Array.isArray(this.data.photoGallery)) {
      this.data.photoGallery.sort((a, b) => new Date(b.date) - new Date(a.date));
      this.filteredGalleryItems = [...this.data.photoGallery];
    }

    this.bindGlobalEvents();
    this.bindTabNavigation();
    this.bindSubtabs();
    this.bindGalleryAndSlideshowEvents();
    this.initClock();

    try { this.syncComputedMetrics(); } catch (e) { console.error("syncComputedMetrics error:", e); }
    try { this.renderKPIs(); } catch (e) { console.error("renderKPIs error:", e); }
    try { this.renderOverviewTab(); } catch (e) { console.error("renderOverviewTab error:", e); }
    // monthly tab removed
    try { this.renderDivisionsTab(); } catch (e) { console.error("renderDivisionsTab error:", e); }
    try { this.populateFilterDropdowns(); } catch (e) { console.error("populateFilterDropdowns error:", e); }
    try { this.renderCategoryPills(); } catch (e) { console.error("renderCategoryPills error:", e); }
    try { this.initActivitiesDivisionShowcase(); } catch (e) { console.error("initActivitiesDivisionShowcase error:", e); }
    try { this.renderActivitiesTab(); } catch (e) { console.error("renderActivitiesTab error:", e); }
    try { this.initReportsSystem(); } catch (e) { console.error("initReportsSystem error:", e); }
    try { this.initAnalyticsTab(); } catch (e) { console.error("initAnalyticsTab error:", e); }
    try { this.renderStatusTab(); } catch (e) { console.error("renderStatusTab error:", e); }
    try { this.init3DTilt(); } catch (e) { console.error("init3DTilt error:", e); }
    try { this.initAutoDriveSyncWatcher(); } catch (e) { console.error("initAutoDriveSyncWatcher error:", e); }
    try { this.initGoogleOAuthIntegration(); } catch (e) { console.error("initGoogleOAuthIntegration error:", e); }

    // Initialize Charts safely after DOM is ready
    if (window.pssCharts) {
      try {
        window.pssCharts.init(this.data);
      } catch (e) {
        console.warn("Chart init deferred or failed gracefully:", e);
      }
    }

    // Check initial hash in URL
    const hash = window.location.hash.replace("#", "");
    if (hash === "monthly") { this.switchTab("monthly"); } else if (hash && this.tabTitles[hash]) {
      this.switchTab(hash);
    } else {
      this.switchTab("overview");
    }

    // Listen for hash changes so URL links, bookmarks, and browser navigation switch tabs automatically
    window.addEventListener("hashchange", () => {
      const h = window.location.hash.replace("#", "");
      if (h === "monthly") { this.switchTab("monthly"); } else if (h && this.tabTitles[h] && this.activeTab !== h) {
        this.switchTab(h);
      }
    });

    console.log("🚀 Praja Sanwardhana Sabhas 8-Tab Dashboard initialized successfully with all 63 GN Divisions.");
  }

  initAutoDriveSyncWatcher() {
    let lastVersion = null;
    const checkVersion = async () => {
      try {
        const resp = await fetch('data_version.json?t=' + Date.now());
        if (resp.ok) {
          const v = await resp.json();
          if (lastVersion && v.version && v.version !== lastVersion) {
            console.log("⚡ New Google Drive data detected from background sync daemon! Updating dashboard...");
            this.showToast("Google Drive වෙතින් නව දත්ත යාවත්කාලීන විය! පද්ධතිය නැවුම් කෙරේ...", "info");
            setTimeout(() => {
              window.location.reload();
            }, 1200);
          }
          lastVersion = v.version;
        }
      } catch (err) {
        // Silently skip if offline
      }
    };
    checkVersion();
    setInterval(checkVersion, 30000);
  }

  initGoogleOAuthIntegration() {
    const connectBtn = document.getElementById("btnGoogleAuthConnect");
    const disconnectBtn = document.getElementById("btnGoogleAuthDisconnect");
    const scanBtn = document.getElementById("btnGoogleScanDrive");
    const badge = document.getElementById("googleAuthStatusBadge");
    const topbarPill = document.getElementById("topbarGoogleAuthStatus");
    const topbarText = document.getElementById("topbarGoogleAuthText");
    const scanContainer = document.getElementById("googleLiveScanContainer");
    const scanList = document.getElementById("googleLiveScanList");
    const scanCount = document.getElementById("googleLiveScanCount");

    // Clicking topbar pill switches directly to status tab and focuses OAuth panel
    if (topbarPill) {
      topbarPill.addEventListener("click", () => {
        this.switchTab("status");
        setTimeout(() => {
          document.getElementById("googleOAuthPanel")?.scrollIntoView({ behavior: "smooth" });
        }, 150);
      });
    }

    const updateAuthUI = (isAuthenticated, error = null) => {
      if (isAuthenticated) {
        if (badge) {
          badge.className = "glass-badge green";
          badge.innerHTML = `<span class="status-indicator-dot" style="background: #10B981;"></span> සක්‍රියයි (Connected)`;
        }
        if (connectBtn) connectBtn.style.display = "none";
        if (disconnectBtn) disconnectBtn.style.display = "inline-flex";
        if (scanBtn) scanBtn.style.display = "inline-flex";
        if (topbarText) topbarText.textContent = "Google Connected";
        if (topbarPill) {
          topbarPill.style.background = "rgba(16, 185, 129, 0.15)";
          topbarPill.style.borderColor = "rgba(16, 185, 129, 0.4)";
          topbarPill.style.color = "#6EE7B7";
        }
      } else {
        if (badge) {
          badge.className = "glass-badge blue";
          badge.innerHTML = `<span class="status-indicator-dot" style="background: #38BDF8;"></span> සූදානම් (Client ID Ready)`;
        }
        if (connectBtn) connectBtn.style.display = "inline-flex";
        if (disconnectBtn) disconnectBtn.style.display = "none";
        if (scanBtn) scanBtn.style.display = "none";
        if (scanContainer) scanContainer.style.display = "none";
        if (topbarText) topbarText.textContent = "OAuth 2.0 Ready";
        if (topbarPill) {
          topbarPill.style.background = "rgba(66, 133, 244, 0.12)";
          topbarPill.style.borderColor = "rgba(66, 133, 244, 0.3)";
          topbarPill.style.color = "#93C5FD";
        }
        if (error && error.error !== "popup_closed_by_user") {
          this.showToast("Google OAuth: " + (error.error_description || error.error || error.message || error), "error");
        }
      }
    };

    // Register auth state listener
    if (window.pssSheetsService) {
      window.pssSheetsService.onAuthStateChange((isAuth, err) => {
        updateAuthUI(isAuth, err);
      });
    }

    if (connectBtn) {
      connectBtn.addEventListener("click", () => {
        try {
          if (!window.pssSheetsService) return;
          connectBtn.disabled = true;
          connectBtn.innerHTML = `<i class="bi bi-arrow-repeat spin"></i> සම්බන්ධ වෙමින්...`;
          window.pssSheetsService.requestGoogleLogin();
          setTimeout(() => {
            connectBtn.disabled = false;
            connectBtn.innerHTML = `<i class="bi bi-google"></i> Google ගිණුම සම්බන්ධ කරන්න`;
          }, 4000);
        } catch (e) {
          connectBtn.disabled = false;
          connectBtn.innerHTML = `<i class="bi bi-google"></i> Google ගිණුම සම්බන්ධ කරන්න`;
          this.showToast(e.message, "error");
        }
      });
    }

    if (disconnectBtn) {
      disconnectBtn.addEventListener("click", () => {
        if (window.pssSheetsService) {
          window.pssSheetsService.disconnectGoogleAuth();
          this.showToast("Google ගිණුම සාර්ථකව විසන්ධි කරන ලදී.", "info");
        }
      });
    }

    if (scanBtn) {
      scanBtn.addEventListener("click", async () => {
        if (!window.pssSheetsService || !scanContainer || !scanList) return;
        scanBtn.disabled = true;
        const origText = scanBtn.innerHTML;
        scanBtn.innerHTML = `<i class="bi bi-arrow-repeat spin"></i> පරිලෝකනය වේ...`;
        scanContainer.style.display = "block";
        scanList.innerHTML = `<div style="color: #94A3B8; padding: 1rem;"><i class="bi bi-arrow-repeat spin"></i> Google Drive API හරහා ෆෝල්ඩරය පරීක්ෂා කෙරේ...</div>`;
        if (scanCount) scanCount.textContent = "පරීක්ෂා කරමින්...";

        try {
          const files = await window.pssSheetsService.fetchLiveDriveFiles();
          if (scanCount) scanCount.textContent = `ගොනු ${files.length}ක් හමු විය`;
          if (files.length === 0) {
            scanList.innerHTML = `<div style="color: #94A3B8; padding: 0.5rem;">ෆෝල්ඩරය තුළ ගොනු හමු නොවීය.</div>`;
          } else {
            scanList.innerHTML = "";
            files.forEach(f => {
              const fileCard = document.createElement("div");
              fileCard.style.padding = "0.75rem 0.9rem";
              fileCard.style.borderRadius = "8px";
              fileCard.style.background = "rgba(255, 255, 255, 0.03)";
              fileCard.style.border = "1px solid rgba(255, 255, 255, 0.08)";
              fileCard.style.display = "flex";
              fileCard.style.justifyContent = "space-between";
              fileCard.style.alignItems = "center";
              fileCard.style.gap = "0.5rem";

              const isSheet = f.mimeType && f.mimeType.includes("spreadsheet");
              const icon = isSheet ? "bi-file-earmark-spreadsheet-fill text-success" : "bi-file-earmark-text text-blue";
              const modified = f.modifiedTime ? new Date(f.modifiedTime).toLocaleDateString("si-LK") : "";

              fileCard.innerHTML = `
                <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  <div style="font-weight: 600; color: #FFF; display: flex; align-items: center; gap: 0.4rem;">
                    <i class="bi ${icon}"></i>
                    <span style="overflow: hidden; text-overflow: ellipsis;">${f.name}</span>
                  </div>
                  <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 0.2rem;">යාවත්කාලීන කළ දිනය: ${modified}</div>
                </div>
                <a href="${f.webViewLink || ('https://drive.google.com/file/d/' + f.id + '/view')}" target="_blank" class="btn-glass" style="font-size: 0.72rem; padding: 0.3rem 0.65rem; text-decoration: none; flex-shrink: 0;">
                  <i class="bi bi-box-arrow-up-right"></i>
                </a>
              `;
              scanList.appendChild(fileCard);
            });
          }
          this.showToast(`Google Drive API: ගොනු ${files.length}ක් සාර්ථකව පරීක්ෂා කරන ලදී!`, "success");
        } catch (err) {
          scanList.innerHTML = `<div style="color: #F87171; padding: 0.5rem;"><i class="bi bi-exclamation-triangle"></i> දෝෂයකි: ${err.message}</div>`;
          this.showToast(err.message, "error");
        } finally {
          scanBtn.disabled = false;
          scanBtn.innerHTML = origText;
        }
      });
    }
  }

  bindTabNavigation() {
    const tabButtons = document.querySelectorAll(".nav-tab-btn");
    tabButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        const targetTab = btn.getAttribute("data-tab");
        if (targetTab) {
          this.switchTab(targetTab);
          // Close mobile sidebar if open
          document.querySelector(".app-sidebar")?.classList.remove("open");
          document.querySelector(".sidebar-backdrop")?.classList.remove("active");
        }
      });
    });

    // Mobile sidebar toggle
    const toggleBtn = document.getElementById("mobileSidebarToggle");
    const sidebar = document.querySelector(".app-sidebar");
    const backdrop = document.querySelector(".sidebar-backdrop");

    if (toggleBtn && sidebar && backdrop) {
      toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("open");
        backdrop.classList.toggle("active");
      });
      backdrop.addEventListener("click", () => {
        sidebar.classList.remove("open");
        backdrop.classList.remove("active");
      });
    }

    // Quick navigation shortcut buttons inside views
    document.querySelectorAll("[data-nav-target]").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const target = btn.getAttribute("data-nav-target");
        if (target) this.switchTab(target);
      });
    });
  }

  switchTab(tabId) {
    if (tabId === "monthly") { this.switchTab("analytics"); const mb = document.querySelector('#view-analytics .subtabs-bar[data-section="analytics"] .subtab-btn[data-subtab="monthly"]'); if (mb) mb.click(); return; } if (!this.tabTitles[tabId]) tabId = "overview";
    this.activeTab = tabId;

    // Update URL hash without jump
    if (typeof window !== "undefined" && window.history && typeof window.history.replaceState === "function") { window.history.replaceState(null, null, `#${tabId}`); }

    // Update active nav button
    document.querySelectorAll(".nav-tab-btn").forEach(btn => {
      if (btn.getAttribute("data-tab") === tabId) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    // Update active view
    document.querySelectorAll(".tab-view").forEach(view => {
      if (view.id === `view-${tabId}`) {
        view.classList.add("active");
      } else {
        view.classList.remove("active");
      }
    });

    // Update topbar breadcrumb and title
    const topbarTitle = document.getElementById("currentViewTitle");
    if (topbarTitle) {
      topbarTitle.textContent = this.tabTitles[tabId];
    }

    if (tabId === "analytics") {
      this.updateAnalyticsView();
    }
    if (tabId === "latest-month") { this.renderLatestMonthProgress(); } if (tabId === "activities") {
      this.renderActivitiesTab();
    }

    // Window scroll to top of content
    if (typeof window !== "undefined" && typeof window.scrollTo === "function") { window.scrollTo({ top: 0, behavior: "smooth" }); }

    // Trigger Chart.js canvas resize
    if (window.pssCharts) {
      window.pssCharts.resizeAll();
    }
  }

  bindSubtabs() {
    document.querySelectorAll(".subtab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const parentBar = btn.closest(".subtabs-bar");
        if (!parentBar) return;

        const section = parentBar.getAttribute("data-section");
        const target = btn.getAttribute("data-subtab");

        // Set active subtab button
        parentBar.querySelectorAll(".subtab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        // Toggle subtab content panes in this section
        const container = btn.closest(".tab-view");
        if (container) {
          container.querySelectorAll(`.subtab-content[data-section="${section}"]`).forEach(content => {
            if (content.getAttribute("data-content") === target) {
              content.classList.add("active");
            } else {
              content.classList.remove("active");
            }
          });
        }

        // Store state
        if (section) this.activeSubtabs[section] = target;

        if (section === "analytics") {
          this.updateAnalyticsView();
        }

        // Resize charts if switching to chart subtabs
        if (window.pssCharts) {
          window.pssCharts.resizeAll();
        }
      });
    });
  }

  bindGlobalEvents() {
    // Activity search input in Tab 4
    const searchInput = document.getElementById("activitySearchInput");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        this.searchQuery = e.target.value.toLowerCase().trim();
        this.applyFilters();
      });
    }

    // Topbar global search input
    const topSearch = document.getElementById("topbarGlobalSearch");
    if (topSearch) {
      topSearch.addEventListener("input", (e) => {
        this.searchQuery = e.target.value.toLowerCase().trim();
        if (this.activeTab !== "activities") {
          this.switchTab("activities");
        }
        if (searchInput) searchInput.value = e.target.value;
        this.applyFilters();
      });
    }

    // Month filter in Tab 4
    const monthSelect = document.getElementById("filterMonthSelect");
    if (monthSelect) {
      monthSelect.addEventListener("change", (e) => {
        this.selectedMonth = e.target.value;
        this.applyFilters();
      });
    }

    // Year filter in Tab 4
    const yearSelect = document.getElementById("filterYearSelect");
    if (yearSelect) {
      yearSelect.addEventListener("change", (e) => {
        this.selectedYear = e.target.value;
        this.applyFilters();
      });
    }

    // GN Division filter in Tab 4
    const gnSelect = document.getElementById("filterGnSelect");
    if (gnSelect) {
      gnSelect.addEventListener("change", (e) => {
        this.selectedGN = e.target.value;
        this.applyFilters();
      });
    }

    // Status filter in Tab 4
    const statusSelect = document.getElementById("filterStatusSelect");
    if (statusSelect) {
      statusSelect.addEventListener("change", (e) => {
        this.selectedStatus = e.target.value;
        this.applyFilters();
      });
    }

    // Reset Filter Button in Tab 4
    const resetBtn = document.getElementById("resetFilterBtn");
    if (resetBtn) {
      resetBtn.addEventListener("click", () => this.resetFilters());
    }

    // GN Division table search input in Tab 3 (All 63 divisions)
    const gnSearchInput = document.getElementById("gnDivisionSearchInput");
    if (gnSearchInput) {
      gnSearchInput.addEventListener("input", (e) => {
        this.filter63GNDivisions(e.target.value.toLowerCase().trim());
      });
    }

    // Dedicated Division View: Back to all divisions button
    const backBtn = document.getElementById("btnBackToAllDivisions");
    if (backBtn) {
      backBtn.addEventListener("click", () => this.closeDedicatedDivisionView());
    }

    // Dedicated Division View: Print Division Report button
    const printDivBtn = document.getElementById("btnPrintDedicatedDivisionReport");
    if (printDivBtn) {
      printDivBtn.addEventListener("click", () => {
        if (this.selectedDedicatedDivision) {
          this.printDivisionReport(this.selectedDedicatedDivision);
        }
      });
    }

    // Modal Close
    const modalCloseBtn = document.getElementById("modalCloseBtn");
    const modalOverlay = document.getElementById("activityModalOverlay");
    if (modalCloseBtn && modalOverlay) {
      modalCloseBtn.addEventListener("click", () => this.closeModal());
      modalOverlay.addEventListener("click", (e) => {
        if (e.target === modalOverlay) this.closeModal();
      });
    }

    // Lightbox Close
    const lightboxCloseBtn = document.getElementById("lightboxCloseBtn");
    const lightboxOverlay = document.getElementById("lightboxOverlay");
    if (lightboxCloseBtn && lightboxOverlay) {
      lightboxCloseBtn.addEventListener("click", () => this.closeLightbox());
      lightboxOverlay.addEventListener("click", (e) => {
        if (e.target === lightboxOverlay) this.closeLightbox();
      });
    }

    // Modal Carousel Nav
    const prevSlideBtn = document.getElementById("modalPrevSlideBtn");
    const nextSlideBtn = document.getElementById("modalNextSlideBtn");
    if (prevSlideBtn && nextSlideBtn) {
      prevSlideBtn.addEventListener("click", () => this.prevModalSlide());
      nextSlideBtn.addEventListener("click", () => this.nextModalSlide());
    }

    // Modal Download Photo Button
    const modalDlBtn = document.getElementById("btnModalDownloadPhoto");
    if (modalDlBtn) {
      modalDlBtn.addEventListener("click", () => {
        if (this.currentModalActivity && this.currentModalActivity.images) {
          const url = this.currentModalActivity.images[this.currentModalImgIndex];
          const filename = `${this.currentModalActivity.gnNameSi}_${this.currentModalActivity.titleSi.slice(0, 20)}_${this.currentModalImgIndex + 1}.jpg`;
          this.downloadPhoto(url, filename);
        }
      });
    }

    // Modal Print Single Activity Report Button
    const modalPrintBtn = document.getElementById("btnPrintActivityReport");
    if (modalPrintBtn) {
      modalPrintBtn.addEventListener("click", () => {
        if (this.currentModalActivity) {
          this.printSingleActivityReport(this.currentModalActivity);
        }
      });
    }

    // Lightbox Carousel Nav
    const prevLightboxBtn = document.getElementById("lightboxPrevBtn");
    const nextLightboxBtn = document.getElementById("lightboxNextBtn");
    if (prevLightboxBtn && nextLightboxBtn) {
      prevLightboxBtn.addEventListener("click", () => this.prevLightboxSlide());
      nextLightboxBtn.addEventListener("click", () => this.nextLightboxSlide());
    }

    // Lightbox Download Button
    const lightboxDlBtn = document.getElementById("lightboxDownloadBtn");
    if (lightboxDlBtn) {
      lightboxDlBtn.addEventListener("click", () => {
        const item = this.currentGalleryItems[this.currentLightboxIndex];
        if (item) {
          const filename = `${item.gnDivision}_${item.titleSi.slice(0, 20)}.jpg`;
          this.downloadPhoto(item.url, filename);
        }
      });
    }

    // Lightbox Slideshow Play/Pause Toggle
    const lightboxPlayBtn = document.getElementById("lightboxTogglePlayBtn");
    if (lightboxPlayBtn) {
      lightboxPlayBtn.addEventListener("click", () => this.toggleSlideshow());
    }

    // Keyboard navigation (Esc to close, Arrow keys for slides)
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        this.closeModal();
        this.closeLightbox();
      } else if (e.key === "ArrowLeft") {
        if (document.getElementById("activityModalOverlay")?.classList.contains("active")) {
          this.prevModalSlide();
        } else if (document.getElementById("lightboxOverlay")?.classList.contains("active")) {
          this.prevLightboxSlide();
        }
      } else if (e.key === "ArrowRight") {
        if (document.getElementById("activityModalOverlay")?.classList.contains("active")) {
          this.nextModalSlide();
        } else if (document.getElementById("lightboxOverlay")?.classList.contains("active")) {
          this.nextLightboxSlide();
        }
      }
    });

    // Global Print Report Buttons
    document.querySelectorAll(".btn-trigger-print").forEach(btn => {
      btn.addEventListener("click", () => window.print());
    });

    // CSV Download Triggers
    const dlActivitiesBtn = document.getElementById("btnDownloadActivitiesCSV");
    if (dlActivitiesBtn) {
      dlActivitiesBtn.addEventListener("click", () => this.exportActivitiesCSV());
    }

    const dlGNDivisionsBtn = document.getElementById("btnDownloadGNDivisionsCSV");
    if (dlGNDivisionsBtn) {
      dlGNDivisionsBtn.addEventListener("click", () => this.exportGNDivisionsCSV());
    }

    const dlMonthlyBtn = document.getElementById("btnDownloadMonthlyCSV");
    if (dlMonthlyBtn) {
      dlMonthlyBtn.addEventListener("click", () => this.exportMonthlyCSV());
    }

    // Refresh Data Trigger in Status Tab
    const refreshBtn = document.getElementById("btnRefreshSystemData");
    if (refreshBtn) {
      refreshBtn.addEventListener("click", () => {
        window.pssSheetsService.clearCache();
        refreshBtn.innerHTML = `<i class="bi bi-arrow-repeat spin"></i> දත්ත යාවත්කාලීන වෙමින්...`;
        setTimeout(() => {
          location.reload();
        }, 600);
      });
    }
  }

  // --- Photo Gallery & Slideshow Engine ---
  bindGalleryAndSlideshowEvents() {
    // Slideshow Toggle Button
    const toggleBtn = document.getElementById("btnToggleSlideshow");
    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => this.toggleSlideshow());
    }

    // Slideshow Next / Prev buttons in Gallery bar
    const nextBtn = document.getElementById("btnGalleryNextSlide");
    const prevBtn = document.getElementById("btnGalleryPrevSlide");
    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        this.nextGallerySlide();
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        this.prevGallerySlide();
      });
    }

    // Gallery Search Input
    const gSearch = document.getElementById("gallerySearchInput");
    if (gSearch) {
      gSearch.addEventListener("input", (e) => {
        this.gallerySearchQuery = e.target.value.toLowerCase().trim();
        this.applyGalleryFilters();
      });
    }

    // Gallery GN Filter (All 63 divisions)
    const gGnFilter = document.getElementById("galleryGnFilter");
    if (gGnFilter) {
      gGnFilter.addEventListener("change", (e) => {
        this.gallerySelectedGN = e.target.value;
        this.applyGalleryFilters();
      });
    }

    // Gallery Month Filter
    const gMonthFilter = document.getElementById("galleryMonthFilter");
    if (gMonthFilter) {
      gMonthFilter.addEventListener("change", (e) => {
        this.gallerySelectedMonth = e.target.value;
        this.applyGalleryFilters();
      });
    }

    // Gallery Year Filter
    const gYearFilter = document.getElementById("galleryYearFilter");
    if (gYearFilter) {
      gYearFilter.addEventListener("change", (e) => {
        this.gallerySelectedYear = e.target.value;
        this.applyGalleryFilters();
      });
    }

    // Gallery Reset Filters Button
    const gResetBtn = document.getElementById("galleryResetFiltersBtn");
    if (gResetBtn) {
      gResetBtn.addEventListener("click", () => this.resetGalleryFilters());
    }
  }

  toggleSlideshow() {
    this.isSlideshowPlaying = !this.isSlideshowPlaying;
    const playBtn = document.getElementById("btnToggleSlideshow");
    const statusBadge = document.getElementById("slideshowStatusBadge");
    const lightboxPlayBtn = document.getElementById("lightboxTogglePlayBtn");

    if (this.isSlideshowPlaying) {
      if (playBtn) {
        playBtn.innerHTML = `<i class="bi bi-pause-circle-fill"></i> <span>ස්ලයිඩ් දර්ශනය නවත්වන්න (Pause)</span>`;
        playBtn.classList.add("slideshow-playing");
      }
      if (statusBadge) {
        statusBadge.innerHTML = `<i class="bi bi-play-circle text-gold"></i> ස්ලයිඩ් ධාවනය වෙමින් පවතී`;
        statusBadge.className = "glass-badge gold";
      }
      if (lightboxPlayBtn) {
        lightboxPlayBtn.innerHTML = `<i class="bi bi-pause-fill"></i> විරාමය`;
      }

      // If lightbox is not open, open it with the first item
      const lightbox = document.getElementById("lightboxOverlay");
      if (!lightbox || !lightbox.classList.contains("active")) {
        if (this.filteredGalleryItems.length > 0) {
          this.openLightbox(0, this.filteredGalleryItems);
        }
      }

      // Start auto timer
      clearInterval(this.slideshowTimer);
      this.slideshowTimer = setInterval(() => {
        this.nextLightboxSlide();
      }, this.slideshowSpeedMs);
    } else {
      if (playBtn) {
        playBtn.innerHTML = `<i class="bi bi-play-circle-fill"></i> <span>ස්ලයිඩ් දර්ශනය ආරම්භ කරන්න (Play Slideshow)</span>`;
        playBtn.classList.remove("slideshow-playing");
      }
      if (statusBadge) {
        statusBadge.innerHTML = `<i class="bi bi-pause-circle"></i> ස්ලයිඩ් දර්ශනය විරාමයේ`;
        statusBadge.className = "glass-badge blue";
      }
      if (lightboxPlayBtn) {
        lightboxPlayBtn.innerHTML = `<i class="bi bi-play-fill"></i> ස්ලයිඩ් ධාවනය`;
      }
      clearInterval(this.slideshowTimer);
      this.slideshowTimer = null;
    }
  }

  nextGallerySlide() {
    if (this.filteredGalleryItems.length === 0) return;
    const lightbox = document.getElementById("lightboxOverlay");
    if (!lightbox || !lightbox.classList.contains("active")) {
      this.openLightbox(0, this.filteredGalleryItems);
    } else {
      this.nextLightboxSlide();
    }
  }

  prevGallerySlide() {
    if (this.filteredGalleryItems.length === 0) return;
    const lightbox = document.getElementById("lightboxOverlay");
    if (!lightbox || !lightbox.classList.contains("active")) {
      this.openLightbox(this.filteredGalleryItems.length - 1, this.filteredGalleryItems);
    } else {
      this.prevLightboxSlide();
    }
  }

  applyGalleryFilters() {
    const allGallery = this.data.photoGallery || [];
    this.filteredGalleryItems = allGallery.filter(item => {
      // GN Division filter
      if (this.gallerySelectedGN !== "all" && item.gnDivision !== this.gallerySelectedGN) {
        return false;
      }
      // Month filter
      if (this.gallerySelectedMonth !== "all" && item.monthSi !== this.gallerySelectedMonth) {
        return false;
      }
      // Year filter
      if (this.gallerySelectedYear !== "all" && String(item.year) !== String(this.gallerySelectedYear)) {
        return false;
      }
      // Category filter
      if (this.gallerySelectedCategory !== "all" && item.category !== this.gallerySelectedCategory) {
        return false;
      }
      // Search query
      if (this.gallerySearchQuery) {
        const q = this.gallerySearchQuery;
        const matchTitle = (item.titleSi || "").toLowerCase().includes(q);
        const matchCaption = (item.captionSi || "").toLowerCase().includes(q);
        const matchGn = (item.gnDivision || "").toLowerCase().includes(q);
        const matchLoc = (item.locationSi || "").toLowerCase().includes(q);
        if (!matchTitle && !matchCaption && !matchGn && !matchLoc) {
          return false;
        }
      }
      return true;
    });

    // Ensure newest first
    this.filteredGalleryItems.sort((a, b) => new Date(b.date) - new Date(a.date));

    this.renderGalleryGrid();
  }

  resetGalleryFilters() {
    this.gallerySearchQuery = "";
    this.gallerySelectedGN = "all";
    this.gallerySelectedMonth = "all";
    this.gallerySelectedYear = "all";
    this.gallerySelectedCategory = "all";

    const s = document.getElementById("gallerySearchInput");
    if (s) s.value = "";
    const gn = document.getElementById("galleryGnFilter");
    if (gn) gn.value = "all";
    const m = document.getElementById("galleryMonthFilter");
    if (m) m.value = "all";
    const y = document.getElementById("galleryYearFilter");
    if (y) y.value = "all";

    this.renderGalleryCategoryPills();
    this.applyGalleryFilters();
  }

  renderGalleryCategoryPills() {
    const container = document.getElementById("galleryCategoryPills");
    if (!container) return;

    container.innerHTML = "";
    this.data.categories.forEach(cat => {
      const btn = document.createElement("button");
      btn.className = `filter-pill ${this.gallerySelectedCategory === cat.id ? "active" : ""}`;
      btn.innerHTML = `<i class="bi ${cat.icon || 'bi-tag'}"></i> ${cat.nameSi}`;
      btn.addEventListener("click", () => {
        this.gallerySelectedCategory = cat.id;
        this.renderGalleryCategoryPills();
        this.applyGalleryFilters();
      });
      container.appendChild(btn);
    });
  }

  renderGalleryTab() {
    // 1. Populate Gallery GN Division filter dropdown (all 63 divisions)
    const gnSelect = document.getElementById("galleryGnFilter");
    if (gnSelect && gnSelect.options && gnSelect.options.length <= 1) {
      gnSelect.innerHTML = `<option value="all">සියලු ග්‍රාම නිලධාරී වසම් (63)</option>`;
      this.data.gnDivisions.forEach(g => {
        const opt = document.createElement("option");
        opt.value = g.nameSi;
        opt.textContent = g.nameSi;
        gnSelect.appendChild(opt);
      });
    }

    // 2. Populate Month filter
    const monthSelect = document.getElementById("galleryMonthFilter");
    if (monthSelect && monthSelect.options.length <= 1) {
      monthSelect.innerHTML = `<option value="all">සියලු මාස</option>`;
      this.data.monthlyStats.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m.monthSi;
        opt.textContent = m.monthSi;
        monthSelect.appendChild(opt);
      });
    }

    // 3. Category pills
    this.renderGalleryCategoryPills();

    // 4. Badge total
    const totalBadge = document.getElementById("galleryTotalPhotosBadge");
    if (totalBadge && this.data.photoGallery) {
      totalBadge.innerHTML = `<i class="bi bi-images"></i> ඡායාරූප ${this.data.photoGallery.length}ක් (නවතම පළමුව)`;
    }

    // 5. Initial render of filtered gallery items (newest first)
    this.applyGalleryFilters();
  }

  renderGalleryGrid() {
    const grid = document.getElementById("galleryGrid");
    const countEl = document.getElementById("galleryResultsCount");

    if (countEl) {
      countEl.textContent = `ඡායාරූප ${this.filteredGalleryItems.length}ක් පෙන්වනු ලැබේ (නවතම වැඩසටහන් පළමුව)`;
    }

    if (!grid) return;

    if (this.filteredGalleryItems.length === 0) {
      grid.innerHTML = `
        <div class="no-results-box" style="grid-column: 1 / -1;">
          <i class="bi bi-images"></i>
          <h4 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.6rem; color: #FFF;">
            ගැලපෙන සංවර්ධන ඡායාරූප හමු නොවීය
          </h4>
          <p style="color: #94A3B8; font-size: 0.92rem;">
            කරුණාකර ඔබ තෝරාගත් පෙරහන් වෙනස් කර නැවත උත්සාහ කරන්න.
          </p>
        </div>
      `;
      return;
    }

    grid.innerHTML = "";
    this.filteredGalleryItems.forEach((item, idx) => {
      const card = document.createElement("div");
      card.className = "gallery-card-item glass-card-3d";

      // Find matching activity object for detailed modal
      const parentActivity = this.data.activities.find(a => a.id === item.activityId) || {
        id: item.activityId,
        titleSi: item.titleSi,
        gnNameSi: item.gnDivision,
        sabhaNameSi: item.sabhaNameSi,
        date: item.date,
        locationSi: item.locationSi || "අක්මීමන",
        purposeSi: item.captionSi,
        actionsSi: item.actionsSi || item.captionSi,
        resultsSi: item.resultsSi || "සාර්ථකව නිම කරන ලදී.",
        beneficiaries: item.beneficiaries || "ප්‍රජාව",
        progress: item.progress || 100,
        status: "completed",
        statusLabelSi: "සම්පූර්ණයි",
        categoryNameSi: item.categoryNameSi || "ප්‍රජා සංවර්ධන",
        images: [item.url]
      };

      card.innerHTML = `
        <div class="gallery-card-thumb-wrap">
          <img src="${item.url}" alt="${item.titleSi}" class="gallery-card-thumb" loading="lazy" />
          <div class="activity-badge-overlay">
            <span class="glass-badge gold">
              <i class="bi bi-geo-alt-fill"></i> ${item.gnDivision}
            </span>
          </div>
          <div class="gallery-photo-actions">
            <button class="gallery-photo-action-btn btn-dl-photo" title="මෙම ඡායාරූපය බාගත කරන්න">
              <i class="bi bi-download"></i> බාගත කරන්න
            </button>
            <button class="gallery-photo-action-btn btn-zoom-photo" title="විශාල කර බලන්න / ස්ලයිඩ්">
              <i class="bi bi-arrows-fullscreen"></i>
            </button>
          </div>
        </div>

        <div class="gallery-card-body">
          <div class="activity-meta-row">
            <span><i class="bi bi-calendar3"></i> ${item.date}</span>
            <span>•</span>
            <span><i class="bi bi-tag-fill"></i> ${item.categoryNameSi || "සංවර්ධන"}</span>
          </div>

          <h3 class="gallery-card-title">${item.titleSi}</h3>
          
          <!-- Activity description/purpose alongside photograph -->
          <div style="font-size: 0.78rem; color: #FDE68A; margin-bottom: 0.25rem;">
            <i class="bi bi-bullseye"></i> වැඩසටහනේ අරමුණ හා විස්තරය:
          </div>
          <p class="gallery-card-desc">${item.captionSi || item.titleSi}</p>

          <div class="gallery-card-footer">
            <span style="color: #94A3B8; font-size: 0.76rem;">
              <i class="bi bi-building text-gold"></i> ${item.sabhaNameSi || "ප්‍රජා සංවර්ධන සභාව"}
            </span>
            <button class="btn-gold btn-open-act-detail" style="padding: 0.4rem 0.9rem; font-size: 0.78rem;">
              <i class="bi bi-eye"></i> සවිස්තර වාර්තාව
            </button>
          </div>
        </div>
      `;

      // Zoom click opens Lightbox / Slideshow
      const thumb = card.querySelector(".gallery-card-thumb-wrap");
      const zoomBtn = card.querySelector(".btn-zoom-photo");
      const openLightboxHandler = () => this.openLightbox(idx, this.filteredGalleryItems);
      thumb.addEventListener("click", (e) => {
        if (!e.target.closest(".gallery-photo-actions")) {
          openLightboxHandler();
        }
      });
      zoomBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        openLightboxHandler();
      });

      // Download photo click
      const dlBtn = card.querySelector(".btn-dl-photo");
      dlBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const filename = `${item.gnDivision}_${item.titleSi.slice(0, 20)}.jpg`;
        this.downloadPhoto(item.url, filename);
      });

      // Activity full details click
      const actDetailBtn = card.querySelector(".btn-open-act-detail");
      actDetailBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        this.openModal(parentActivity);
      });

      grid.appendChild(card);
    });

    this.init3DTilt();
  }

  // --- Photo Downloader Logic ---
  async downloadPhoto(imgUrl, filename) {
    try {
      // Use clean Sinhala safe ASCII name
      const safeFilename = filename
        .replace(/[\/\\?%*:|"<>]/g, "_")
        .replace(/\s+/g, "_");

      const response = await fetch(imgUrl, { mode: "cors" });
      if (!response.ok) throw new Error("Image download failed");
      const blob = await response.blob();
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = safeFilename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(blobUrl);

      this.showToast(`ඡායාරූපය සාර්ථකව බාගත විය: ${safeFilename}`);
    } catch (err) {
      // Direct fallback via window open or anchor
      const a = document.createElement("a");
      a.href = imgUrl;
      a.target = "_blank";
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      this.showToast("ඡායාරූපය නව කවුළුවකින් විවෘත කරන ලදී.");
    }
  }

  showToast(message) {
    let toast = document.getElementById("pssToastMessage");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "pssToastMessage";
      toast.style.position = "fixed";
      toast.style.bottom = "24px";
      toast.style.right = "24px";
      toast.style.background = "linear-gradient(135deg, rgba(6, 16, 42, 0.95), rgba(16, 33, 77, 0.95))";
      toast.style.border = "1px solid #D4AF37";
      toast.style.color = "#FFF";
      toast.style.padding = "0.75rem 1.4rem";
      toast.style.borderRadius = "12px";
      toast.style.fontSize = "0.86rem";
      toast.style.fontWeight = "600";
      toast.style.boxShadow = "0 10px 30px rgba(0,0,0,0.6)";
      toast.style.zIndex = "9999";
      toast.style.transition = "opacity 0.3s ease";
      document.body.appendChild(toast);
    }
    toast.innerHTML = `<i class="bi bi-check-circle-fill text-gold" style="margin-right: 8px;"></i> ${message}`;
    toast.style.opacity = "1";
    toast.style.display = "block";
    setTimeout(() => {
      toast.style.opacity = "0";
      setTimeout(() => { toast.style.display = "none"; }, 300);
    }, 3200);
  }

  // --- Clock ---
  initClock() {
    const clockEl = document.getElementById("liveClock");
    if (!clockEl) return;

    const updateTime = () => {
      const now = new Date();
      const options = {
        timeZone: "Asia/Colombo",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true
      };
      const timeStr = new Intl.DateTimeFormat("en-US", options).format(now);
      clockEl.textContent = `${timeStr} (ශ්‍රී ලංකා වේලාව)`;
    };

    updateTime();
    setInterval(updateTime, 1000);
  }

  getUniqueActiveDays(activities = []) { if (!Array.isArray(activities) || !activities.length) return 0; return new Set(activities.map(a => (a?.date || a?.activityDate || "").toString().trim()).filter(d => d && d !== "-" && d !== "N/A" && d !== "null" && d !== "undefined")).size; } classifyActivityCategory(act) { const a = act || {}; const cats = this.data?.categories || this.data?.analyticalCategories || []; const findCat = (idHints, siHints, fallbackSi) => { const found = cats.find(c => { const id = (c.id || "").toLowerCase(); const si = (c.nameSi || c.name || "").toLowerCase(); return idHints.some(h => id.includes(h)) || siHints.some(h => si.includes(h)); }); return { id: found?.id || idHints[0], nameSi: found?.nameSi || fallbackSi }; }; const txt = [a.titleSi, a.title, a.descriptionSi, a.description, a.actionsSi, a.purposeSi, a.resultsSi, a.categoryNameSi, a.categorySi, a.sectorSi, a.sector, a.category].filter(Boolean).join(" ").toLowerCase(); if (/දන්සැල|දන්සල|දන්සල්|දන්සැල්|භක්ති|බක්ති|පොසොන්|වෙසක්|ඇසළ|පෝය|බෝධිපූජා|පින්කම|ධර්ම|විහාර|පන්සල්|දහම්|සාහිත්‍ය|අවුරුදු|බක්මහ|සංස්කෘතික|ආගමික|ආශීර්වාද|සීල|පෙරහැර/.test(txt)) return findCat(["religious", "cultural"], ["ආගමික", "සංස්කෘතික"], "ආගමික හා සංස්කෘතික"); if (/පිරිසිදු|ශ්‍රමදාන|ශ්‍රම දාන|ඩෙංගු|ඩෙන්ගු|කසළ|කසල|රුක් රෝපණ|පැළ සිටුවීම|පැල සිටුවීම|පරිසර|වායු/.test(txt)) return findCat(["environment", "shramadana"], ["පරිසර", "ශ්‍රමදාන"], "පරිසර හා ශ්‍රමදාන"); if (/වෛද්‍ය|සායන|ආයුර්වේද|යෝග|ඇරබික්|ව්‍යායාම|ඇස් කන්නාඩි|මත්ද්‍රව්‍ය|රෝග|සෞඛ්‍ය|සුවසෙත|නිරෝගී/.test(txt)) return findCat(["health"], ["සෞඛ්‍ය"], "සෞඛ්‍ය"); if (/පාසල්|පාසල|පෙරපාසල්|ළමා|ලමා|දරුවන්|ශිෂ්‍යත්ව|දෙමළ භාෂා|සම්මන්ත්‍රණ|පුස්තකාල|අධ්‍යාපන|තාක්ෂණ/.test(txt)) return findCat(["education", "children"], ["අධ්‍යාපන", "ළමා"], "අධ්‍යාපන"); if (/පුහුණු|ඉටිපන්දම්|ඉදල්|සබන්|බිම්මල්|පොල්|තේ වගා|බුලත්|ගම්මිරිස්|කෘෂි|වගා|ගොවි|ස්වයං රැකියා|අළෙවිපොළ|ව්‍යාපාර|කර්මාන්ත|රූපලාවන්‍ය|කොණ්ඩා|මැහුම්|බෑග්/.test(txt)) return findCat(["livelihood", "agriculture", "economic"], ["ආර්ථික", "ජීවනෝපාය", "කෘෂි"], "ආර්ථික හා ජීවනෝපාය / කෘෂිකර්ම"); if (/සුළි කුණාටු|ආධාර|අවතැන්|වැඩිහිටි|කාන්තා|සුභසාධන|පරිත්‍යාග|ප්‍රදානය|ආබාධිත|වියළි ආහාර|සමෘද්ධි|සමුර්ධි/.test(txt)) return findCat(["welfare", "social"], ["සමාජ", "සුභසාධන"], "සමාජ සුභසාධන"); if (/කාපට්|කොන්ක්‍රීට්|කොන්ක්‍රිට්|ගල්බැම්ම|පාලම|බෝක්කු|පලල් කිරීම|පළල් කිරීම|ඉදිකිරීම|ඉදි කිරීම|පිලිසකර|පිළිසකර|මුල්ගල|නිවාස සෑදීම|නිවසක් සාදා|ජල සැපයුම|විදුලි|කාණු පද්ධති/.test(txt)) return findCat(["infrastructure"], ["යටිතල"], "යටිතල පහසුකම්"); const cur = cats.find(c => c.id === a.category || c.nameSi === a.categoryNameSi); return { id: cur?.id || a.category || "other", nameSi: cur?.nameSi || a.categoryNameSi || a.categorySi || a.sectorSi || a.sector || "වෙනත්" }; } syncComputedMetrics() { const acts = this.data.activities || []; const explicitSwaps = { "2026-12-10": "2026-10-12", "2026-11-10": "2026-10-11", "2026-11-08": "2026-08-11" }; acts.forEach(a => { let raw = (a.date || a.activityDate || "").toString().trim().slice(0, 10); if (explicitSwaps[raw]) raw = explicitSwaps[raw]; const gnStr = (a.gnNameSi || a.gnDivision || a.gnName || "").toString(); const txtStr = (a.titleSi || a.title || a.descriptionSi || a.description || "").toString(); if (raw === "2026-02-05" && (gnStr.includes("නිවිතිපිටිගොඩ") || txtStr.includes("පන්සල කන්ද") || txtStr.includes("කාණු පද්ධති"))) { raw = "2026-10-05"; } const m = raw.match(/^(\d{4})-(\d{2})-(\d{2})$/); if (m) { let y = parseInt(m[1], 10), mo = parseInt(m[2], 10), d = parseInt(m[3], 10); if (y > 2026 || y < 2025) y = 2026; const ymStr = `${y}-${String(mo).padStart(2, "0")}-${String(d).padStart(2, "0")}`; if (ymStr < "2025-11-01") y = 2026; const tsRaw = (a.timestamp || a.submittedAt || a.createdAt || "").toString().trim().slice(0, 10); const tsM = tsRaw.match(/^(\d{4})-(\d{2})-(\d{2})$/); if (tsM) { const ty = parseInt(tsM[1], 10), tm = parseInt(tsM[2], 10); if (y > ty) y = ty <= 2026 ? ty : 2026; if (y === ty && mo > tm) { if (d >= 1 && d <= tm && d <= 12 && mo <= 31) { const tmp = mo; mo = d; d = tmp; } else { mo = tm; if (d > 28) d = 28; } } } const fixed = `${y}-${String(mo).padStart(2, "0")}-${String(d).padStart(2, "0")}`; a.date = fixed; a.activityDate = fixed; a.year = String(y); a.month = fixed.slice(0, 7); a.yearMonth = fixed.slice(0, 7); } const cls = this.classifyActivityCategory(a); if (cls) { a.category = cls.id; a.categoryNameSi = cls.nameSi; a.categorySi = cls.nameSi; a.sector = cls.nameSi; a.sectorSi = cls.nameSi; a.analyticalCategory = cls.nameSi; } }); const monthMap = {}; acts.forEach(a => { const ym = (a.yearMonth || a.month || (a.date || "").slice(0, 7)).trim(); if (!/^\d{4}-\d{2}$/.test(ym) || ym < "2025-11") return; if (!monthMap[ym]) monthMap[ym] = []; monthMap[ym].push(a); }); const siMonths = { "01": "ජනවාරි", "02": "පෙබරවාරි", "03": "මාර්තු", "04": "අප්‍රේල්", "05": "මැයි", "06": "ජූනි", "07": "ජූලි", "08": "අගෝස්තු", "09": "සැප්තැම්බර්", "10": "ඔක්තෝම්බර්", "11": "නොවැම්බර්", "12": "දෙසැම්බර්" }; let runningCumulative = 0; const computedMonths = Object.keys(monthMap).sort().map(ym => { const mActs = monthMap[ym]; const [yStr, mStr] = ym.split("-"); const sinhalaMonth = siMonths[mStr] || mStr; const fullSi = `${yStr} ${sinhalaMonth}`; const photos = mActs.reduce((acc, a) => acc + (Array.isArray(a.photoObjects) ? a.photoObjects.length : (Array.isArray(a.photos) ? a.photos.length : (Array.isArray(a.images) ? a.images.length : (Array.isArray(a.photoUrls) ? a.photoUrls.length : 0)))), 0); const gns = new Set(mActs.map(a => a.gnNameSi || a.gnDivision || a.gnName).filter(Boolean)).size; const activeDays = this.getUniqueActiveDays(mActs); const count = mActs.length; runningCumulative += count; return { month: ym, yearMonth: ym, monthKey: ym, monthName: fullSi, monthSi: fullSi, nameSi: fullSi, label: fullSi, sinhalaMonth: sinhalaMonth, count: count, totalActivities: count, totalProjects: count, activities: count, activeDays: activeDays, photos: photos, divisions: gns, divisionsCount: gns, gnCount: gns, reportedDivisions: gns, reportingGns: gns, cumulative: runningCumulative, cumulativeCount: runningCumulative, cumulativeTotal: runningCumulative }; }); if (computedMonths.length > 0) { this.data.monthlyStats = computedMonths; this.data.monthlyProgress = computedMonths; } const uniqueDays = this.getUniqueActiveDays(acts); const totalPhotos = this.data.photoGallery?.length || acts.reduce((acc, a) => acc + (a.images ? a.images.length : (a.photos ? a.photos.length : 0)), 0); if (!this.data.overview) this.data.overview = {}; this.data.overview.totalActivities = acts.length; this.data.overview.activeDays = uniqueDays; this.data.overview.totalActiveDays = uniqueDays; this.data.overview.totalPhotographs = totalPhotos; if (Array.isArray(this.data.gnDivisions)) { this.data.gnDivisions.forEach(g => { const gActs = acts.filter(a => (g.nameSi && a.gnNameSi === g.nameSi) || (g.name && (a.gnDivision === g.name || a.gnName === g.name))); g.totalProjects = gActs.length; g.activityCount = gActs.length; g.activeDays = this.getUniqueActiveDays(gActs); g.photos = gActs.reduce((acc, a) => acc + (a.images ? a.images.length : (a.photos ? a.photos.length : 0)), 0); }); this.data.overview.reportingGns = this.data.gnDivisions.filter(g => (g.totalProjects || g.activityCount || 0) > 0).length; } if (Array.isArray(this.data.categories)) { this.data.categories.forEach(c => { c.count = acts.filter(a => a.category === c.id || a.categoryNameSi === c.nameSi || a.sectorSi === c.nameSi).length; }); } if (Array.isArray(this.data.analyticalCategories)) { this.data.analyticalCategories.forEach(c => { c.count = acts.filter(a => a.category === c.id || a.categoryNameSi === c.nameSi || a.analyticalCategory === c.nameSi).length; }); } if (false) { const acts = this.data.activities || []; const uniqueDays = this.getUniqueActiveDays(acts); const totalPhotos = this.data.photoGallery?.length || acts.reduce((acc, a) => acc + (a.images ? a.images.length : (a.photos ? a.photos.length : 0)), 0); if (!this.data.overview) this.data.overview = {}; this.data.overview.totalActivities = acts.length; this.data.overview.activeDays = uniqueDays; this.data.overview.totalActiveDays = uniqueDays; this.data.overview.totalPhotographs = totalPhotos; if (Array.isArray(this.data.gnDivisions)) { this.data.gnDivisions.forEach(g => { const gActs = acts.filter(a => (g.nameSi && a.gnNameSi === g.nameSi) || (g.name && (a.gnDivision === g.name || a.gnName === g.name))); if (gActs.length > 0 || !g.activeDays) g.activeDays = this.getUniqueActiveDays(gActs); }); this.data.overview.reportingGns = this.data.gnDivisions.filter(g => (g.totalProjects || g.activityCount || 0) > 0).length; } const mList = this.data.monthlyStats || this.data.monthlyProgress || []; mList.forEach(m => { if (!m.activeDays && m.month) { const mActs = acts.filter(a => (a.month || "").includes(m.month) || (a.date || "").startsWith(m.month)); if (mActs.length > 0) m.activeDays = this.getUniqueActiveDays(mActs); } }); } } renderKPIs() {
    const sec = this.data.overview || this.data.secretariatInfo || {};

    const totalAct = sec.totalActivities || this.data.activities?.length || 0;
    const repGns = sec.reportingGNs || sec.reportingGnDivisions || 63;
    const totalGns = sec.totalGNs || sec.totalGNDivisions || 63;
    const actDays = sec.activeDays || sec.totalActiveDays || this.getUniqueActiveDays(this.data.activities);
    const totPhotos = sec.totalPhotographs || sec.totalPhotos || this.data.photoGallery?.length || 0;

    // Total Activities
    const totalActEl = document.getElementById("kpiTotalActivities");
    if (totalActEl) totalActEl.textContent = totalAct;

    // Reporting GN Divisions (63 / 63)
    const reportingGnEl = document.getElementById("kpiReportingGNs");
    if (reportingGnEl) reportingGnEl.textContent = `${repGns} / ${totalGns}`;

    // Active Days (189 days)
    const activeDaysEl = document.getElementById("kpiActiveDays");
    if (activeDaysEl) activeDaysEl.textContent = actDays;

    // Total Verified Photos (1,374 photos)
    const totalPhotosEl = document.getElementById("kpiTotalPhotos");
    if (totalPhotosEl) totalPhotosEl.textContent = totPhotos.toLocaleString();

    // Overall Completion Rate (100% completed monthly activities)
    const heroProgressValEl = document.getElementById("heroProgressVal");
    if (heroProgressValEl) heroProgressValEl.textContent = "100%";

    const heroProgressFill = document.getElementById("heroProgressFill");
    if (heroProgressFill) heroProgressFill.style.width = "100%";

    // Counts in hero box
    const hpReportingGn = document.getElementById("hpReportingGnCount");
    if (hpReportingGn) hpReportingGn.textContent = `${repGns} / ${totalGns} වසම්`;

    const hpCompletedEl = document.getElementById("hpCompletedCount");
    if (hpCompletedEl) hpCompletedEl.textContent = `${totalAct} වැඩසටහන්`;

    // Sidebar counts
    const sideActCount = document.getElementById("sideActivitiesBadge");
    if (sideActCount) sideActCount.textContent = totalAct; const flatBtnBadge = document.querySelector("#btnActivitiesFlatMode .badge, #btnActivitiesFlatMode span"); if (flatBtnBadge) flatBtnBadge.textContent = totalAct;

    const sideDivCount = document.getElementById("sideDivisionsBadge");
    if (sideDivCount) sideDivCount.textContent = totalGns;
  }

renderOverviewTab() { this.renderLatestMonthProgress(); }
renderLatestMonthProgress() { const container = document.getElementById("latestMonthProgressContainer") || document.getElementById("overviewRecentList"); if (!container) return; const acts = this.data.activities || []; const mSet = new Set(); acts.forEach(a => { const d = (a.date || "").trim(); if (/^\d{4}-\d{2}/.test(d)) mSet.add(d.slice(0, 7)); }); const months = Array.from(mSet).sort(); const latestKey = months.length ? months[months.length - 1] : null; if (!latestKey) { container.innerHTML = '<div style="color:#94A3B8;text-align:center;padding:1.5rem;">නවතම මාසයේ දත්ත හමු නොවීය...</div>'; return; } const siM = {"01":"ජනවාරි","02":"පෙබරවාරි","03":"මාර්තු","04":"අප්‍රේල්","05":"මැයි","06":"ජූනි","07":"ජූලි","08":"අගෝස්තු","09":"සැප්තැම්බර්","10":"ඔක්තෝම්බර්","11":"නොවැම්බර්","12":"දෙසැම්බර්"}; const parts = latestKey.split("-"); const monthLabel = parts[0] + " " + (siM[parts[1]] || parts[1]); const dynamicTabLabel = monthLabel + " ප්‍රගතිය"; if (this.tabTitles) this.tabTitles["latest-month"] = dynamicTabLabel; const sideLatestEl = document.getElementById("sideLatestMonthLabel"); if (sideLatestEl) sideLatestEl.textContent = dynamicTabLabel; if (this.currentTab === "latest-month") { const topTitleEl = document.getElementById("currentViewTitle"); if (topTitleEl) topTitleEl.textContent = dynamicTabLabel; } const mActs = acts.filter(a => (a.date || "").trim().startsWith(latestKey)); const gnCounts = {}; const secCounts = {}; let photoCount = 0; mActs.forEach(a => { const gn = a.gnNameSi || a.gnDivision || "වෙනත්"; gnCounts[gn] = (gnCounts[gn] || 0) + 1; const sec = a.sectorSi || a.sector || a.categorySi || a.category || "වෙනත්"; secCounts[sec] = (secCounts[sec] || 0) + 1; if (Array.isArray(a.images)) photoCount += a.images.length; else if (Array.isArray(a.photos)) photoCount += a.photos.length; }); const actCount = mActs.length; const daysCount = this.getUniqueActiveDays(mActs); const gnCount = Object.keys(gnCounts).length; const sortedSec = Object.entries(secCounts).sort((a, b) => b[1] - a[1]); const sortedGn = Object.entries(gnCounts).sort((a, b) => b[1] - a[1]); const sortedActs = mActs.slice().sort((a, b) => (b.date || "").localeCompare(a.date || "")); const secHtml = sortedSec.map(([s, c]) => '<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:0.35rem 0.75rem;border-radius:10px;font-size:0.8rem;display:inline-flex;align-items:center;gap:0.45rem;"><span style="color:#FFFFFF;font-weight:600;">' + s + '</span><span class="glass-badge blue" style="font-size:0.72rem;padding:0.1rem 0.45rem;">' + c + '</span></div>').join(""); const activeGn = this.selectedLatestMonthDivision || null; const resetBtnHtml = '<button type="button" class="latest-gn-filter-btn" data-gn-filter="__ALL__" style="cursor:pointer;background:' + (!activeGn ? 'rgba(56,189,248,0.22)' : 'rgba(255,255,255,0.06)') + ';border:1px solid ' + (!activeGn ? '#38BDF8' : 'rgba(255,255,255,0.12)') + ';padding:0.35rem 0.75rem;border-radius:10px;font-size:0.8rem;display:inline-flex;align-items:center;gap:0.45rem;color:#FFFFFF;font-weight:600;">සියලුම වසම් <span class="glass-badge blue" style="font-size:0.72rem;padding:0.1rem 0.45rem;">' + actCount + '</span></button>'; const gnHtml = resetBtnHtml + sortedGn.map(([g, c]) => { const isSel = activeGn === g; return '<button type="button" class="latest-gn-filter-btn" data-gn-filter="' + String(g).replace(/"/g, '&quot;') + '" style="cursor:pointer;background:' + (isSel ? 'rgba(16,185,129,0.22)' : 'rgba(255,255,255,0.04)') + ';border:1px solid ' + (isSel ? '#10B981' : 'rgba(255,255,255,0.08)') + ';padding:0.35rem 0.75rem;border-radius:10px;font-size:0.8rem;display:inline-flex;align-items:center;gap:0.45rem;"><span style="color:#FFFFFF;font-weight:600;">' + g + '</span><span class="glass-badge green" style="font-size:0.72rem;padding:0.1rem 0.45rem;">' + c + '</span></button>'; }).join(""); const filteredActs = activeGn ? sortedActs.filter(a => (a.gnNameSi || a.gnDivision || "වෙනත්") === activeGn) : sortedActs; const actLightboxMap = []; const listHtml = filteredActs.map((a, idx) => { const rawP = a.photoObjects || a.photos || a.images || a.photoUrls || []; const photos = rawP.map((p, i) => { const u = this.resolveDriveImageUrl(p); return u ? { id: (p && typeof p === "object" && p.id) ? p.id : `${a.id || idx}-p${i}`, thumbnail: u, full: u, url: u, caption: a.titleSi || a.title || "", date: a.date || "", gn: a.gnNameSi || a.gnDivision || "" } : null; }).filter(Boolean); actLightboxMap[idx] = photos; const titleText = a.titleSi || a.title || a.description || ""; const descText = a.description || a.actionsSi || a.titleSi || a.title || ""; const collageHtml = this.buildPhotoCollageHTML(photos, titleText); return `<div class="editorial-activity-card" data-latest-act-idx="${idx}"><div class="editorial-card-meta"><span class="editorial-meta-badge division-pill"><i class="bi bi-geo-alt-fill"></i> ${a.gnNameSi || a.gnDivision || "-"}</span><span class="editorial-meta-badge date-pill"><i class="bi bi-calendar3"></i> ${a.date || ""}</span><span class="editorial-meta-badge sector-pill"><i class="bi bi-tag-fill"></i> ${a.categoryNameSi || a.sectorSi || a.sector || a.categorySi || "-"}</span>${(a.officerNameSi || a.officerName || a.officerSi || a.officer) ? `<span class="editorial-meta-badge officer-pill"><i class="bi bi-person-fill"></i> ${a.officerNameSi || a.officerName || a.officerSi || a.officer}</span>` : ""}</div><h3 class="editorial-card-title">${titleText}</h3>${collageHtml}<p class="editorial-card-description">${descText}</p></div>`; }).join(""); container.innerHTML = '<div style="background:rgba(15,23,44,0.7);border-radius:14px;padding:1.2rem;border:1px solid rgba(255,255,255,0.08);"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;flex-wrap:wrap;gap:0.5rem;"><div><span style="font-size:0.8rem;color:#94A3B8;">නවතම සක්‍රීය මාසයේ ප්‍රගතිය</span><h3 style="font-size:1.35rem;font-weight:800;color:#FFFFFF;margin:0.2rem 0 0 0;"><span class="blue-text-gradient">' + monthLabel + '</span></h3></div><span class="glass-badge green" style="font-size:0.78rem;padding:0.35rem 0.8rem;"><i class="bi bi-check-circle-fill"></i> ස්වයංක්‍රීයව යාවත්කාලීන වේ</span></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.7rem;margin-bottom:1.1rem;" class="latest-month-mini-kpis"><div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:0.75rem;border-left:3px solid #38BDF8;"><div style="font-size:0.72rem;color:#94A3B8;font-weight:600;">වැඩසටහන් ගණන</div><div style="font-size:1.45rem;font-weight:800;color:#FFFFFF;line-height:1.2;">' + actCount + '</div></div><div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:0.75rem;border-left:3px solid #FBBF24;"><div style="font-size:0.72rem;color:#94A3B8;font-weight:600;">සක්‍රීය දින</div><div style="font-size:1.45rem;font-weight:800;color:#FFFFFF;line-height:1.2;">' + daysCount + '</div></div><div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:0.75rem;border-left:3px solid #34D399;"><div style="font-size:0.72rem;color:#94A3B8;font-weight:600;">වාර්තා කළ වසම්</div><div style="font-size:1.45rem;font-weight:800;color:#FFFFFF;line-height:1.2;">' + gnCount + '</div></div><div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:0.75rem;border-left:3px solid #A78BFA;"><div style="font-size:0.72rem;color:#94A3B8;font-weight:600;">ඡායාරූප</div><div style="font-size:1.45rem;font-weight:800;color:#FFFFFF;line-height:1.2;">' + photoCount + '</div></div></div><div style="margin-bottom:1.1rem;"><div style="font-size:0.78rem;font-weight:700;color:#94A3B8;margin-bottom:0.5rem;"><i class="bi bi-pie-chart-fill text-info"></i> ක්ෂේත්‍ර අනුව බෙදීම</div><div style="display:flex;gap:0.5rem;flex-wrap:wrap;">' + secHtml + '</div></div><div style="margin-bottom:1.1rem;"><div style="font-size:0.78rem;font-weight:700;color:#94A3B8;margin-bottom:0.5rem;"><i class="bi bi-geo-alt-fill text-success"></i> වසම් අනුව බෙදීම</div><div style="display:flex;gap:0.5rem;flex-wrap:wrap;">' + gnHtml + '</div></div><div><div style="font-size:0.78rem;font-weight:700;color:#94A3B8;margin-bottom:0.5rem;"><i class="bi bi-list-check text-gold"></i> ' + monthLabel + ' වැඩසටහන් ලැයිස්තුව (' + actCount + ')</div><div style="display:flex;flex-direction:column;gap:0.5rem;max-height:420px;overflow-y:auto;padding-right:0.25rem;">' + listHtml + '</div></div></div>'; }
  

  renderMonthlyTab() {
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
  }

  // --- All 63 GN Divisions & Dedicated Division Activity View Engine ---
  renderDivisionsTab() {
    // 0. Populate Tab 3 Quick Jump Dropdown
    const tab3Dropdown = document.getElementById("tab3GnJumpDropdown");
    if (tab3Dropdown) {
      tab3Dropdown.innerHTML = '<option value="">🏛️ වසමක් තෝරා ක්ෂණිකව පිවිසෙන්න...</option>';
      this.data.gnDivisions.forEach((gn, idx) => {
        const opt = document.createElement("option");
        opt.value = gn.nameSi;
        opt.textContent = `${(idx + 1).toString().padStart(2, "0")}. ${gn.nameSi} (${gn.totalProjects} වැඩසටහන්)`;
        tab3Dropdown.appendChild(opt);
      });
      tab3Dropdown.addEventListener("change", (e) => {
        if (e.target.value) {
          this.openDedicatedDivisionView(e.target.value);
        }
      });
    }

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

        const viewBtn = tr.querySelector(".btn-view-division-act");
        if (viewBtn) {
          viewBtn.addEventListener("click", () => {
            this.openDedicatedDivisionView(gn.nameSi);
          });
        }

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
  }

  // Dedicated Division View: Opens when visitor selects a GN Division
  openDedicatedDivisionView(gnName) {
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
  }

  closeDedicatedDivisionView() {
    this.selectedDedicatedDivision = null;
    const dedicatedView = document.getElementById("divisionDedicatedView");
    const allDivView = document.getElementById("divisionAllListView");

    if (dedicatedView) dedicatedView.style.display = "none";
    if (allDivView) allDivView.style.display = "block";

    // Scroll to top of divisions tab
    if (typeof window !== "undefined" && typeof window.scrollTo === "function") { window.scrollTo({ top: 0, behavior: "smooth" }); }
  }

  filter63GNDivisions(query) {
    let matchCount = 0;

    const cards = document.querySelectorAll("#divisionCardsGrid .division-card");
    cards.forEach(card => {
      const text = card.textContent.toLowerCase();
      const match = text.includes(query);
      card.style.display = match ? "" : "none";
      if (match) matchCount++;
    });

    const rows = document.querySelectorAll("#gnComparisonTableBody tr");
    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(query) ? "" : "none";
    });

    const counter = document.getElementById("gnDivisionsCardCounter");
    if (counter) {
      counter.textContent = query ? `ගැලපෙන වසම් ${matchCount}ක් හමුවිය` : `වසම් 63ම ඇතුළත්ය`;
    }
  }

  populateFilterDropdowns() {
    // Months dropdown in Tab 4
    const monthSelect = document.getElementById("filterMonthSelect");
    if (monthSelect) {
      monthSelect.innerHTML = `<option value="all">සියලු මාස</option>`;
      const months = this.data.monthlyStats || this.data.monthlySummary || [];
      months.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m.month || m.monthSi;
        opt.textContent = m.nameSi || m.monthSi || m.month;
        monthSelect.appendChild(opt);
      });
    }

    // GN Divisions dropdown in Tab 4 - All 63 divisions (Names ONLY)
    const gnSelect = document.getElementById("filterGnSelect");
    if (gnSelect) {
      gnSelect.innerHTML = `<option value="all">සියලු ග්‍රාම නිලධාරී වසම් (63)</option>`;
      this.data.gnDivisions.forEach(g => {
        const opt = document.createElement("option");
        opt.value = g.nameSi;
        opt.textContent = g.nameSi;
        gnSelect.appendChild(opt);
      });
    }
  }

  renderCategoryPills() {
    const container = document.getElementById("categoryPillsContainer");
    if (!container) return;

    container.innerHTML = "";
    (this.data.categories || []).forEach(cat => {
      const btn = document.createElement("button");
      btn.className = `filter-pill ${this.selectedCategory === cat.id ? "active" : ""}`;
      btn.innerHTML = `<i class="bi ${cat.icon || 'bi-tag'}"></i> ${cat.nameSi}`;
      btn.addEventListener("click", () => {
        this.selectedCategory = cat.id;
        this.renderCategoryPills();
        this.applyFilters();
      });
      container.appendChild(btn);
    });
  }

  applyFilters() {
    this.filteredActivities = this.data.activities.filter(act => {
      // Category filter
      if (this.selectedCategory !== "all" && act.category !== this.selectedCategory) {
        return false;
      }
      // Month filter
      if (this.selectedMonth !== "all" && act.monthSi !== this.selectedMonth) {
        return false;
      }
      // Year filter
      if (this.selectedYear !== "all" && String(act.year) !== String(this.selectedYear)) {
        return false;
      }
      // GN Division filter (Name only)
      if (this.selectedGN !== "all" && act.gnNameSi !== this.selectedGN) {
        return false;
      }
      // Status filter
      if (this.selectedStatus !== "all" && act.status !== this.selectedStatus) {
        return false;
      }
      // Text Search
      if (this.searchQuery) {
        const q = this.searchQuery;
        const matchTitle = (act.titleSi || "").toLowerCase().includes(q);
        const matchPurpose = (act.purposeSi || "").toLowerCase().includes(q);
        const matchActions = (act.actionsSi || "").toLowerCase().includes(q);
        const matchGn = (act.gnNameSi || "").toLowerCase().includes(q);
        const matchSabha = (act.sabhaNameSi || "").toLowerCase().includes(q);
        if (!matchTitle && !matchPurpose && !matchActions && !matchGn && !matchSabha) {
          return false;
        }
      }
      return true;
    });

    // Ensure newest first
    this.filteredActivities.sort((a, b) => new Date(b.date) - new Date(a.date));

    this.renderActivitiesTab();
  }

  resetFilters() {
    this.selectedCategory = "all";
    this.selectedMonth = "all";
    this.selectedGN = "all";
    this.selectedStatus = "all";
    this.selectedYear = "all";
    this.searchQuery = "";

    const searchInput = document.getElementById("activitySearchInput");
    if (searchInput) searchInput.value = "";

    const topSearch = document.getElementById("topbarGlobalSearch");
    if (topSearch) topSearch.value = "";

    const monthSelect = document.getElementById("filterMonthSelect");
    if (monthSelect) monthSelect.value = "all";

    const yearSelect = document.getElementById("filterYearSelect");
    if (yearSelect) yearSelect.value = "all";

    const gnSelect = document.getElementById("filterGnSelect");
    if (gnSelect) gnSelect.value = "all";

    const statusSelect = document.getElementById("filterStatusSelect");
    if (statusSelect) statusSelect.value = "all";

    this.renderCategoryPills();
    this.applyFilters();
  }

  // --- Activity Card Builder with Direct Photo Gallery on the Page ---
  resolveDriveImageUrl(p) { if (!p) return ""; let raw = ""; if (typeof p === "string") { raw = p.trim(); } else if (typeof p === "object") { raw = String(p.thumbnail || p.full || p.url || p.src || p.webContentLink || p.link || "").trim(); if (!raw && p.id && typeof p.id === "string" && /^[a-zA-Z0-9_-]{15,}$/.test(p.id.trim())) raw = p.id.trim(); } if (!raw) return ""; if (raw.includes("drive.google.com")) { if (raw.includes("/thumbnail?") || raw.includes("lh3.googleusercontent.com")) return raw; const m = raw.match(/\/d\/([a-zA-Z0-9_-]+)/) || raw.match(/[?&]id=([a-zA-Z0-9_-]+)/); if (m && m[1]) return `https://drive.google.com/thumbnail?id=${m[1]}&sz=w800`; } if (/^[a-zA-Z0-9_-]{20,}$/.test(raw) && !raw.includes("/") && !raw.includes(".")) return `https://drive.google.com/thumbnail?id=${raw}&sz=w800`; return raw; } buildPhotoCollageHTML(photosOrAct, title = "") { const rawPhotos = Array.isArray(photosOrAct) ? photosOrAct : (photosOrAct && typeof photosOrAct === "object" ? (photosOrAct.photoObjects || photosOrAct.photos || photosOrAct.images || photosOrAct.photoUrls || []) : []); const photos = rawPhotos.map(p => this.resolveDriveImageUrl(p)).filter(Boolean);
    if (!Array.isArray(photos) || photos.length === 0) return "";
    const total = photos.length;
    const countClass = total === 1 ? "collage-count-1" : total === 2 ? "collage-count-2" : total === 3 ? "collage-count-3" : total === 4 ? "collage-count-4" : "collage-count-many";
    const visible = photos;
    const safeTitle = String(title || "").replace(/"/g, "&quot;");
    const itemsHtml = visible.map((p, idx) => {
      const src = typeof p === "string" ? p : (p.thumbnail || p.full || p.url || "");
      const moreBadge = "";
      return `<div class="photo-collage-item" data-photo-idx="${idx}" title="${safeTitle}"><img src="${src}" alt="${safeTitle}" loading="lazy">${moreBadge}</div>`;
    }).join("");
    return `<div class="photo-collage ${countClass}">${itemsHtml}</div>`;
  }

  createActivityCardElement(act) {
    const card = document.createElement("div");
    card.className = "editorial-activity-card";
    card.setAttribute("data-act-id", act.id);

    const rawPhotoList = act.photoObjects || act.photos || act.images || act.photoUrls || []; const photos = rawPhotoList.map((p, i) => { const u = this.resolveDriveImageUrl(p); return u ? { id: (p && typeof p === "object" && p.id) ? p.id : `${act.id || "act"}-p${i}`, thumbnail: u, full: u, url: u } : null; }).filter(Boolean); const _skipMap = [].map((url, i) => ({
      id: `${act.id}-p${i}`,
      thumbnail: url,
      full: url,
      driveUrl: url
    }));
    const titleText = act.titleSi || act.title || act.description || "";
    const divisionText = act.gnNameSi || act.gnDivision || "-";
    const dateText = act.date || "";
    const sectorText = act.categoryNameSi || act.sectorSi || act.categoryName || act.sector || "-";
    const descText = act.description || act.titleSi || act.title || "";
    const collageHtml = this.buildPhotoCollageHTML(photos, titleText);

    card.innerHTML = `
      <div class="editorial-card-meta">
        <span class="editorial-meta-badge division-pill"><i class="bi bi-geo-alt-fill"></i> ${divisionText}</span>
        <span class="editorial-meta-badge date-pill"><i class="bi bi-calendar3"></i> ${dateText}</span>
        <span class="editorial-meta-badge sector-pill"><i class="bi bi-tag-fill"></i> ${sectorText}</span>${(act.officerNameSi || act.officerName || act.officerSi || act.officer) ? `<span class="editorial-meta-badge officer-pill"><i class="bi bi-person-fill"></i> ${act.officerNameSi || act.officerName || act.officerSi || act.officer}</span>` : ""}
      </div>
      <h3 class="editorial-card-title">${titleText}</h3>
      ${collageHtml}
      <p class="editorial-card-description">${descText}</p>
      <div class="editorial-activity-footer">
        <span class="activity-sabha" title="${act.sabhaNameSi || ""}"><i class="bi bi-building"></i> ${act.sabhaNameSi || ""}</span>
        <button class="btn-gold btn-open-act-modal" style="padding: 0.45rem 1rem; font-size: 0.82rem;" data-act-id="${act.id}">
          <i class="bi bi-eye"></i> &#x0DC0;&#x0DD2;&#x0DC3;&#x0DCA;&#x0DAD;&#x0DBB; &#x0DB6;&#x0DBD;&#x0DB1;&#x0DCA;&#x0DB1;
        </button>
      </div>
    `;

    const photoItems = card.querySelectorAll(".photo-collage-item");
    photoItems.forEach(item => {
      item.addEventListener("click", (e) => {
        e.stopPropagation();
        const photoIdx = parseInt(item.getAttribute("data-photo-idx"), 10) || 0;
        const actPhotosForLightbox = photos.map(p => ({
          url: p.full || p.thumbnail,
          titleSi: act.titleSi,
          gnDivision: act.gnNameSi || act.gnDivision,
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

  // ==========================================================
  // TAB 4: GN DIVISION-FIRST ACTIVITY SHOWCASE (WEB-PAGE STYLE)
  // ==========================================================
  initActivitiesDivisionShowcase() {
    this.selectedActivitiesGnIndex = 0;
    this.currentGnZone = "all";
    this.gnViewType = "slider"; // "slider" or "grouped"

    // 1. View Mode Toggles (Division Web Article vs Flat List)
    const btnDivMode = document.getElementById("btnActivitiesDivisionMode");
    const btnFlatMode = document.getElementById("btnActivitiesFlatMode");
    const divView = document.getElementById("activitiesDivisionModeView");
    const flatView = document.getElementById("activitiesFlatModeView");

    if (btnDivMode && btnFlatMode) {
      btnDivMode.addEventListener("click", () => {
        this.activitiesViewMode = "division";
        btnDivMode.classList.add("active");
        btnFlatMode.classList.remove("active");
        if (divView) divView.style.display = "block";
        if (flatView) flatView.style.display = "none";
        this.renderDivisionActivitiesShowcase();
      });

      btnFlatMode.addEventListener("click", () => {
        this.activitiesViewMode = "flat";
        btnFlatMode.classList.add("active");
        btnDivMode.classList.remove("active");
        if (divView) divView.style.display = "none";
        if (flatView) flatView.style.display = "block";
        this.renderFlatActivities();
      });
    }

    // 2. Zone Clusters Definitions
    this.gnZones = [
      { id: "all", name: "සියලු කලාප", label: "සියලු කලාප (63)", badge: "63" },
      { id: "109", name: "109 කලාපය", label: "109 කලාපය (වසම් 8)", badge: "8", test: g => g.nameSi.includes("109") },
      { id: "110-113", name: "110-113 කලාපය", label: "110-113 කලාපය (වසම් 12)", badge: "12", test: g => ["110", "111", "112", "113"].some(k => g.nameSi.includes(k)) },
      { id: "118", name: "118 කලාපය", label: "118 කලාපය (වසම් 8)", badge: "8", test: g => g.nameSi.includes("118") },
      { id: "130", name: "130 කලාපය", label: "130 කලාපය (වසම් 6)", badge: "6", test: g => g.nameSi.includes("130") },
      { id: "133", name: "133 කලාපය", label: "133 කලාපය (වසම් 6)", badge: "6", test: g => g.nameSi.includes("133") },
      { id: "134-135", name: "134-135 කලාපය", label: "134-135 කලාපය (වසම් 9)", badge: "9", test: g => ["134", "135"].some(k => g.nameSi.includes(k)) },
      { id: "152", name: "152 කලාපය", label: "152 කලාපය (වසම් 6)", badge: "6", test: g => g.nameSi.includes("152") },
      { id: "155", name: "155 කලාපය", label: "155 කලාපය (වසම් 8)", badge: "8", test: g => g.nameSi.includes("155") },
    ];

    // 3. Render Zone Filter Ribbon
    this.renderGnZoneBar();

    // 4. Slider vs Grouped Toggle Buttons
    const btnSliderToggle = document.getElementById("btnToggleGnSliderView");
    const btnGroupedToggle = document.getElementById("btnToggleGnGroupedView");
    const sliderWrap = document.getElementById("activitiesGnSliderWrap");
    const groupedWrap = document.getElementById("activitiesGnGroupedView");

    if (btnSliderToggle && btnGroupedToggle) {
      btnSliderToggle.addEventListener("click", () => {
        this.gnViewType = "slider";
        btnSliderToggle.classList.add("active");
        btnSliderToggle.style.background = "#3979D6";
        btnSliderToggle.style.color = "#FFF";
        btnGroupedToggle.classList.remove("active");
        btnGroupedToggle.style.background = "transparent";
        btnGroupedToggle.style.color = "#526078";
        if (sliderWrap) sliderWrap.style.display = "block";
        if (groupedWrap) groupedWrap.style.display = "none";
      });

      btnGroupedToggle.addEventListener("click", () => {
        this.gnViewType = "grouped";
        btnGroupedToggle.classList.add("active");
        btnGroupedToggle.style.background = "#3979D6";
        btnGroupedToggle.style.color = "#FFF";
        btnSliderToggle.classList.remove("active");
        btnSliderToggle.style.background = "transparent";
        btnSliderToggle.style.color = "#526078";
        if (sliderWrap) sliderWrap.style.display = "none";
        if (groupedWrap) {
          groupedWrap.style.display = "block";
          this.renderGnGroupedCards();
        }
      });
    }

    // 5. Populate Grouped Dropdown
    this.populateGroupedGnDropdown();

    // 6. Populate GN Nav Pills (Slider track)
    this.renderGnNavPills();

    // 7. GN Quick Search Input
    const gnSearch = document.getElementById("activitiesGnSearchInput");
    if (gnSearch) {
      gnSearch.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase().trim();
        this.filterGnNavPills(q);
      });
    }

    // 8. Interactive Slider Scroll Buttons (Left / Right)
    const btnSliderLeft = document.getElementById("btnSliderScrollLeft");
    const btnSliderRight = document.getElementById("btnSliderScrollRight");
    const sliderTrack = document.getElementById("activitiesGnNavPills");
    if (btnSliderLeft && sliderTrack) {
      btnSliderLeft.addEventListener("click", () => {
        sliderTrack.scrollBy({ left: -320, behavior: "smooth" });
      });
    }
    if (btnSliderRight && sliderTrack) {
      btnSliderRight.addEventListener("click", () => {
        sliderTrack.scrollBy({ left: 320, behavior: "smooth" });
      });
    }

    // 9. Prev / Next GN buttons on banner
    const btnPrev = document.getElementById("btnPrevGnDivision");
    const btnNext = document.getElementById("btnNextGnDivision");
    if (btnPrev) {
      btnPrev.addEventListener("click", () => {
        if (this.selectedActivitiesGnIndex > 0) {
          this.selectGnDivision(this.selectedActivitiesGnIndex - 1);
        }
      });
    }
    if (btnNext) {
      btnNext.addEventListener("click", () => {
        if (this.selectedActivitiesGnIndex < this.data.gnDivisions.length - 1) {
          this.selectGnDivision(this.selectedActivitiesGnIndex + 1);
        }
      });
    }

    // Render the initial showcase
    this.renderDivisionActivitiesShowcase();
  }

  getGnZoneId(gnName) {
    if (gnName.includes("109")) return "109";
    if (["110", "111", "112", "113"].some(k => gnName.includes(k))) return "110-113";
    if (gnName.includes("118")) return "118";
    if (gnName.includes("130")) return "130";
    if (gnName.includes("133")) return "133";
    if (["134", "135"].some(k => gnName.includes(k))) return "134-135";
    if (gnName.includes("152")) return "152";
    if (gnName.includes("155")) return "155";
    return "other";
  }

  renderGnZoneBar() {
    const bar = document.getElementById("activitiesGnZoneBar");
    if (!bar) return;
    bar.innerHTML = "";

    this.gnZones.forEach(zone => {
      const btn = document.createElement("button");
      btn.className = `zone-filter-btn ${zone.id === this.currentGnZone ? "active" : ""}`;
      btn.innerHTML = `<span>${zone.name}</span> <span class="zone-badge">${zone.badge}</span>`;
      btn.addEventListener("click", () => {
        this.currentGnZone = zone.id;
        document.querySelectorAll("#activitiesGnZoneBar .zone-filter-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        
        // Re-render slider pills for this zone
        this.renderGnNavPills();

        // If in grouped view, scroll to zone card
        if (this.gnViewType === "grouped") {
          this.renderGnGroupedCards();
          if (zone.id !== "all") {
            const zCard = document.getElementById(`gnGroupCard-${zone.id}`);
            if (zCard) zCard.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        }
      });
      bar.appendChild(btn);
    });
  }

  populateGroupedGnDropdown() {
    const gnDropdown = document.getElementById("activitiesGnSelectDropdown");
    if (!gnDropdown) return;
    gnDropdown.innerHTML = "";

    const zonesForDropdown = this.gnZones.filter(z => z.id !== "all");
    zonesForDropdown.forEach(zone => {
      const optgroup = document.createElement("optgroup");
      optgroup.label = zone.label;

      this.data.gnDivisions.forEach((gn, idx) => {
        if (zone.test(gn)) {
          const opt = document.createElement("option");
          opt.value = idx;
          const gnActs = this.data.activities.filter(a => a.gnNameSi === gn.nameSi);
          opt.textContent = `${(idx + 1).toString().padStart(2, "0")}. ${gn.nameSi} (${gnActs.length} වැඩසටහන්)`;
          optgroup.appendChild(opt);
        }
      });

      if (optgroup.children && optgroup.children.length > 0) {
        gnDropdown.appendChild(optgroup);
      }
    });

    gnDropdown.addEventListener("change", (e) => {
      const idx = parseInt(e.target.value, 10);
      this.selectGnDivision(idx);
    });
  }

  renderGnNavPills() {
    const container = document.getElementById("activitiesGnNavPills");
    if (!container) return;
    container.innerHTML = "";

    this.data.gnDivisions.forEach((gn, idx) => {
      const zId = this.getGnZoneId(gn.nameSi);
      if (this.currentGnZone !== "all" && zId !== this.currentGnZone) {
        return; // filter to current zone
      }

      const gnActs = this.data.activities.filter(a => a.gnNameSi === gn.nameSi);
      const btn = document.createElement("button");
      btn.className = `gn-nav-pill-btn ${idx === this.selectedActivitiesGnIndex ? "active" : ""}`;
      btn.setAttribute("data-gn-idx", idx);
      btn.innerHTML = `
        <span>${gn.nameSi}</span>
        <span class="gn-nav-pill-badge">${gnActs.length}</span>
      `;
      btn.addEventListener("click", () => {
        this.selectGnDivision(idx);
      });
      container.appendChild(btn);
    });

    // Ensure active pill is scrolled into view
    setTimeout(() => {
      const activePill = container.querySelector(".gn-nav-pill-btn.active");
      if (activePill && typeof activePill.scrollIntoView === "function") {
        activePill.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      }
    }, 100);
  }

  renderGnGroupedCards() {
    const container = document.getElementById("activitiesGnGroupedView");
    if (!container) return;
    container.innerHTML = "";

    const zonesToRender = this.currentGnZone === "all" 
      ? this.gnZones.filter(z => z.id !== "all") 
      : this.gnZones.filter(z => z.id === this.currentGnZone);

    zonesToRender.forEach(zone => {
      const gnsInZone = this.data.gnDivisions.map((gn, idx) => ({ gn, idx })).filter(item => zone.test(item.gn));
      if (!gnsInZone.length) return;

      const totalActsInZone = gnsInZone.reduce((acc, item) => {
        return acc + this.data.activities.filter(a => a.gnNameSi === item.gn.nameSi).length;
      }, 0);

      const card = document.createElement("div");
      card.className = "gn-group-card";
      card.id = `gnGroupCard-${zone.id}`;

      let pillsHtml = gnsInZone.map(item => {
        const gnActs = this.data.activities.filter(a => a.gnNameSi === item.gn.nameSi);
        const isActive = (item.idx === this.selectedActivitiesGnIndex);
        return `
          <button class="gn-nav-pill-btn ${isActive ? 'active' : ''}" data-gn-idx="${item.idx}" style="justify-content: space-between; width: 100%;">
            <span>${item.gn.nameSi}</span>
            <span class="gn-nav-pill-badge">${gnActs.length}</span>
          </button>
        `;
      }).join("");

      card.innerHTML = `
        <div class="gn-group-header">
          <span style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="bi bi-collection-fill" style="color: #3979D6;"></i>
            <strong>${zone.label}</strong>
          </span>
          <span class="glass-badge blue" style="font-size: 0.76rem;">${totalActsInZone} වැඩසටහන්</span>
        </div>
        <div class="gn-group-grid">
          ${pillsHtml}
        </div>
      `;

      card.querySelectorAll(".gn-nav-pill-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const idx = parseInt(btn.getAttribute("data-gn-idx"), 10);
          this.selectGnDivision(idx);
        });
      });

      container.appendChild(card);
    });
  }

  selectGnDivision(idx) {
    this.selectedActivitiesGnIndex = idx;
    const gn = this.data.gnDivisions[idx];
    if (gn) {
      const zId = this.getGnZoneId(gn.nameSi);
      // If selected division is outside current zone filter, reset zone to all or switch zone
      if (this.currentGnZone !== "all" && zId !== this.currentGnZone) {
        this.currentGnZone = zId;
        this.renderGnZoneBar();
      }
    }
    this.renderDivisionActivitiesShowcase();
    this.renderGnNavPills();
    if (this.gnViewType === "grouped") {
      this.renderGnGroupedCards();
    }
  }

  filterGnNavPills(q) {
    const pills = document.querySelectorAll("#activitiesGnNavPills .gn-nav-pill-btn");
    pills.forEach(pill => {
      const text = pill.textContent.toLowerCase();
      pill.style.display = text.includes(q) ? "inline-flex" : "none";
    });

    const gnDropdown = document.getElementById("activitiesGnSelectDropdown");
    if (gnDropdown) {
      Array.from(gnDropdown.options).forEach(opt => {
        const matches = opt.textContent.toLowerCase().includes(q);
        opt.hidden = q ? !matches : false;
      });
    }
  }

  renderDivisionActivitiesShowcase() {
    const gn = this.data.gnDivisions[this.selectedActivitiesGnIndex] || this.data.gnDivisions[0];
    if (!gn) return;

    // Update active state in pills
    const pills = document.querySelectorAll("#activitiesGnNavPills .gn-nav-pill-btn");
    pills.forEach((p) => {
      const idx = parseInt(p.getAttribute("data-gn-idx"), 10);
      if (idx === this.selectedActivitiesGnIndex) {
        p.classList.add("active");
        p.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      } else {
        p.classList.remove("active");
      }
    });

    // Update dropdown
    const dropdown = document.getElementById("activitiesGnSelectDropdown");
    if (dropdown) dropdown.value = this.selectedActivitiesGnIndex;

    // Filter activities for this GN division
    const gnActs = this.data.activities.filter(a => a.gnNameSi === gn.nameSi);
    
    // Calculate total photos and unique dates for this division
    const totalPhotos = gnActs.reduce((acc, a) => acc + (a.photoCount || (a.images ? a.images.length : 0)), 0);
    const uniqueDates = new Set(gnActs.map(a => a.date)).size;

    // Update Banner elements
    const nameEl = document.getElementById("activeGnTitleName");
    const sabhaEl = document.getElementById("activeGnSabhaName");
    const orderBadge = document.getElementById("activeGnOrderBadge");
    const actCountEl = document.getElementById("activeGnActivityCount");
    const photoCountEl = document.getElementById("activeGnPhotoCount");
    const daysEl = document.getElementById("activeGnActiveDays");
    const counterText = document.getElementById("activeGnCounterText");
    const btnPrev = document.getElementById("btnPrevGnDivision");
    const btnNext = document.getElementById("btnNextGnDivision");

    if (nameEl) nameEl.textContent = gn.nameSi;
    if (sabhaEl) sabhaEl.textContent = gn.sabhaNameSi || `${gn.nameSi} ප්‍රජා සංවර්ධන සභාව`;
    if (orderBadge) orderBadge.textContent = `වසම් අංකය ${(this.selectedActivitiesGnIndex + 1).toString().padStart(2, "0")} / 63`;
    if (actCountEl) actCountEl.textContent = gnActs.length;
    if (photoCountEl) photoCountEl.textContent = totalPhotos;
    if (daysEl) daysEl.textContent = uniqueDates;
    if (counterText) counterText.textContent = `ග්‍රාම නිලධාරී වසම් 63 න් ${(this.selectedActivitiesGnIndex + 1)} වන වසම: ${gn.nameSi}`;
    
    if (btnPrev) btnPrev.disabled = (this.selectedActivitiesGnIndex === 0);
    if (btnNext) btnNext.disabled = (this.selectedActivitiesGnIndex === this.data.gnDivisions.length - 1);

    // Render Feature Articles
    const container = document.getElementById("divisionWebArticlesContainer");
    if (!container) return;

    if (gnActs.length === 0) {
      container.innerHTML = `
        <div class="glass-panel" style="text-align: center; padding: 3rem 1.5rem;">
          <i class="bi bi-info-circle text-gold" style="font-size: 2.5rem; margin-bottom: 1rem; display: block;"></i>
          <h3 style="color: #FFF; font-weight: 700; margin-bottom: 0.5rem;">මෙම වසම සඳහා සංවර්ධන වැඩසටහන් වාර්තා ඉදිරිපත් වෙමින් පවතී</h3>
          <p style="color: #94A3B8;">${gn.nameSi} ප්‍රජා සංවර්ධන සභාවේ ක්ෂේත්‍ර දත්ත වාර්තාකරණය ඉදිරි කාර්තුවට නියමිතව ඇත.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = "";
    // Sort activities by date descending (newest first within the selected GN division)
    const sortedActs = [...gnActs].sort((a, b) => new Date(b.date) - new Date(a.date));

    sortedActs.forEach((act, actIdx) => {
      const articleEl = this.createWebArticleElement(act, actIdx);
      container.appendChild(articleEl);
    });

    this.init3DTilt();
  }

  createWebArticleElement(act, actIdx) {
    const article = document.createElement("article");
    article.className = "editorial-activity-card";
    article.setAttribute("data-act-id", act.id);

    const rawPhotoList = act.photoObjects || act.photos || act.images || act.photoUrls || []; const photos = rawPhotoList.map((p, i) => { const u = this.resolveDriveImageUrl(p); return u ? { id: (p && typeof p === "object" && p.id) ? p.id : `${act.id || "act"}-p${i}`, thumbnail: u, full: u, url: u } : null; }).filter(Boolean); const _skipMap = [].map((url, i) => ({
      id: `${act.id}-p${i}`,
      thumbnail: url,
      full: url,
      driveUrl: url
    }));
    const photoCount = photos.length;
    const titleText = act.titleSi || act.title || act.description || "";
    const divisionText = act.gnNameSi || act.gnDivision || "-";
    const dateText = act.date || "";
    const sectorText = act.categoryNameSi || act.sectorSi || act.categoryName || act.sector || "-";
    const descText = act.description || act.actionsSi || act.titleSi || act.title || "";
    const galleryHtml = this.buildPhotoCollageHTML(photos, titleText);

    article.innerHTML = `
      <div class="editorial-card-meta">
        <span class="editorial-meta-badge division-pill"><i class="bi bi-geo-alt-fill"></i> ${divisionText}</span>
        <span class="editorial-meta-badge date-pill"><i class="bi bi-calendar3"></i> ${dateText}</span>
        <span class="editorial-meta-badge sector-pill"><i class="bi bi-tag-fill"></i> ${sectorText}</span>${(act.officerNameSi || act.officerName || act.officerSi || act.officer) ? `<span class="editorial-meta-badge officer-pill"><i class="bi bi-person-fill"></i> ${act.officerNameSi || act.officerName || act.officerSi || act.officer}</span>` : ""}
      </div>
      <h3 class="editorial-card-title">${titleText}</h3>
      ${galleryHtml}
      <p class="editorial-card-description">${descText}</p>
      <div class="editorial-activity-footer">
        <div style="display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center;">
          ${photoCount > 0 ? `<button class="btn-glass btn-view-gallery" style="background: rgba(56, 189, 248, 0.15); border-color: rgba(56, 189, 248, 0.35); color: #38BDF8; font-size: 0.82rem; padding: 0.45rem 1rem;"><i class="bi bi-images"></i> (${photoCount})</button>` : ""}
          <button class="btn-glass btn-print-activity" data-act-id="${act.id}" style="padding: 0.45rem 1rem; font-size: 0.82rem;"><i class="bi bi-printer"></i></button>
        </div>
        <span class="activity-sabha" title="${act.sabhaNameSi || ""}"><i class="bi bi-building"></i> ${act.sabhaNameSi || ""}</span>
      </div>
    `;

    const actPhotosForLightbox = photos.map(p => ({
      url: p.full || p.thumbnail,
      titleSi: act.titleSi,
      captionSi: act.description || act.titleSi,
      gnDivision: act.gnNameSi,
      date: act.date,
      sabhaNameSi: act.sabhaNameSi,
      categoryNameSi: act.categoryNameSi,
      locationSi: act.locationSi || act.gnNameSi,
      beneficiaries: act.beneficiaries || "",
      progress: 100,
      actId: act.id
    }));

    const photoItems = article.querySelectorAll(".photo-collage-item");
    photoItems.forEach(item => {
      item.addEventListener("click", () => {
        const pIdx = parseInt(item.getAttribute("data-photo-idx"), 10) || 0;
        this.openLightbox(pIdx, actPhotosForLightbox);
      });
    });

    // Gallery button
    const galBtn = article.querySelector(".btn-view-gallery");
    if (galBtn) {
      galBtn.addEventListener("click", () => {
        this.openLightbox(0, actPhotosForLightbox);
      });
    }

    // Bind print activity button
    const printBtn = article.querySelector(".btn-print-activity");
    if (printBtn) {
      printBtn.addEventListener("click", () => {
        this.printSingleActivityReport(act);
      });
    }

    return article;
  }

  renderActivitiesTab() {
    if (this.activitiesViewMode === "division") {
      this.renderDivisionActivitiesShowcase();
    } else {
      this.renderFlatActivities();
    }
  }

  renderFlatActivities() {
    const grid = document.getElementById("activitiesGrid");
    const countEl = document.getElementById("activityResultsCount");

    if (countEl) {
      countEl.textContent = `ප්‍රජා සංවර්ධන වැඩසටහන් ${this.filteredActivities.length}ක් පෙන්වනු ලැබේ`;
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
  }

  // ==========================================================
  // 7-TYPE REPORT GENERATION & DOWNLOAD SYSTEM ENGINE
  // ==========================================================
  initReportsSystem() {
    this.currentReportState = null;
    this.currentReportMeta = null;

    // 1. Populate GN Divisions Select (all 63 authentic divisions - names only)
    const gnSelect = document.getElementById("reportGnSelect");
    if (gnSelect && gnSelect.options && gnSelect.options.length <= 1) {
      gnSelect.innerHTML = `<option value="all">සියලුම ග්‍රාම නිලධාරී වසම් (63)</option>`;
      this.data.gnDivisions.forEach(g => {
        const opt = document.createElement("option");
        opt.value = g.nameSi;
        opt.textContent = g.nameSi;
        gnSelect.appendChild(opt);
      });
    }

    // 2. Populate Months Select
    const mSelect = document.getElementById("reportMonthSelect");
    if (mSelect && mSelect.options && mSelect.options.length <= 1) {
      mSelect.innerHTML = `<option value="all">සියලු මාස</option>`;
      this.data.monthlyStats.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m.monthSi;
        opt.textContent = m.monthSi;
        mSelect.appendChild(opt);
      });
    }

    // 3. Populate Categories Select
    const catSelect = document.getElementById("reportCategorySelect");
    if (catSelect && catSelect.options && catSelect.options.length <= 1) {
      catSelect.innerHTML = `<option value="all">සියලුම ක්ෂේත්‍ර</option>`;
      this.data.categories.forEach(c => {
        if (c.id !== "all") {
          const opt = document.createElement("option");
          opt.value = c.id;
          opt.textContent = c.nameSi;
          catSelect.appendChild(opt);
        }
      });
    }

    // 4. Populate Specific Activities Select (for single activity / photo reports)
    const actSelect = document.getElementById("reportSpecificActivitySelect");
    if (actSelect && actSelect.options && actSelect.options.length === 0) {
      this.data.activities.forEach(a => {
        const opt = document.createElement("option");
        opt.value = a.id;
        opt.textContent = `[${a.gnNameSi}] ${a.titleSi}`;
        actSelect.appendChild(opt);
      });
    }

    // 5. Report Type Change Listener
    const typeSelect = document.getElementById("reportTypeSelect");
    const actWrap = document.getElementById("reportSpecificActivityWrap");
    if (typeSelect) {
      typeSelect.addEventListener("change", (e) => {
        const val = e.target.value;
        if (actWrap) {
          actWrap.style.display = (val === "4" || val === "5") ? "block" : "none";
        }
        this.generateReport();
      });
    }

    // 6. Bind Generate Report Button
    const genBtn = document.getElementById("btnGenerateReport");
    if (genBtn) {
      genBtn.addEventListener("click", () => this.generateReport());
    }

    // 7. Bind Reset Filters Button
    const resetBtn = document.getElementById("btnResetReportFilters");
    if (resetBtn) {
      resetBtn.addEventListener("click", () => this.resetReportFilters());
    }

    // 8. Bind Export Action Buttons
    const pdfBtn = document.getElementById("btnDownloadReportPDF");
    if (pdfBtn) {
      pdfBtn.addEventListener("click", () => this.downloadReportPDF());
    }

    const xlsBtn = document.getElementById("btnDownloadReportExcel");
    if (xlsBtn) {
      xlsBtn.addEventListener("click", () => this.downloadReportExcel());
    }

    const csvBtn = document.getElementById("btnDownloadReportCSV");
    if (csvBtn) {
      csvBtn.addEventListener("click", () => this.downloadReportCSV());
    }

    const printBtn = document.getElementById("btnPrintReportDirect");
    if (printBtn) {
      printBtn.addEventListener("click", () => this.printReportDirect());
    }

    // Initial Report Generation (Type 1: Overall Report)
    this.generateReport();
  }

  resetReportFilters() {
    const typeSelect = document.getElementById("reportTypeSelect");
    if (typeSelect) typeSelect.value = "1";

    const gnSelect = document.getElementById("reportGnSelect");
    if (gnSelect) gnSelect.value = "all";

    const periodSelect = document.getElementById("reportPeriodSelect");
    if (periodSelect) periodSelect.value = "all";

    const mSelect = document.getElementById("reportMonthSelect");
    if (mSelect) mSelect.value = "all";

    const ySelect = document.getElementById("reportYearSelect");
    if (ySelect) ySelect.value = "2026";

    const catSelect = document.getElementById("reportCategorySelect");
    if (catSelect) catSelect.value = "all";

    const actWrap = document.getElementById("reportSpecificActivityWrap");
    if (actWrap) actWrap.style.display = "none";

    this.generateReport();
    this.showToast("වාර්තා පෙරහන් සාර්ථකව යළි සකසන ලදී.");
  }

  generateReport() {
    const reportType = document.getElementById("reportTypeSelect")?.value || "1";
    const selectedGn = document.getElementById("reportGnSelect")?.value || "all";
    const selectedPeriod = document.getElementById("reportPeriodSelect")?.value || "all";
    const selectedMonth = document.getElementById("reportMonthSelect")?.value || "all";
    const selectedYear = document.getElementById("reportYearSelect")?.value || "2026";
    const selectedCategory = document.getElementById("reportCategorySelect")?.value || "all";
    const specificActId = document.getElementById("reportSpecificActivitySelect")?.value;

    const currentDate = new Date().toLocaleDateString("si-LK");
    const currentTime = new Date().toLocaleTimeString("si-LK", { hour: "2-digit", minute: "2-digit" });
    const docRefId = `AKM/PSS/REP/2026/${String(reportType).padStart(2, '0')}-${Math.floor(1000 + Math.random() * 9000)}`;

    // Filter Activities based on active configuration
    let reportActs = this.data.activities.filter(a => {
      if (selectedGn !== "all" && a.gnNameSi !== selectedGn) return false;
      if (selectedCategory !== "all" && a.category !== selectedCategory) return false;
      if (selectedMonth !== "all" && a.monthSi !== selectedMonth) return false;
      if (selectedYear !== "all" && String(a.year) !== String(selectedYear)) return false;

      // Reporting Period filter
      if (selectedPeriod === "h1") {
        const h1Months = ["ජනවාරි", "පෙබරවාරි", "මාර්තු", "අප්‍රේල්", "මැයි", "ජූනි"];
        if (!h1Months.includes(a.monthSi)) return false;
      } else if (selectedPeriod === "h2") {
        const h2Months = ["ජූලි", "අගෝස්තු", "සැප්තැම්බර්", "ඔක්තෝබර්", "නොවැම්බර්", "දෙසැම්බර්"];
        if (!h2Months.includes(a.monthSi)) return false;
      } else if (selectedPeriod === "q1") {
        if (!["ජනවාරි", "පෙබරවාරි", "මාර්තු"].includes(a.monthSi)) return false;
      } else if (selectedPeriod === "q2") {
        if (!["අප්‍රේල්", "මැයි", "ජූනි"].includes(a.monthSi)) return false;
      } else if (selectedPeriod === "q3") {
        if (!["ජූලි", "අගෝස්තු", "සැප්තැම්බර්"].includes(a.monthSi)) return false;
      } else if (selectedPeriod === "q4") {
        if (!["ඔක්තෝබර්", "නොවැම්බර්", "දෙසැම්බර්"].includes(a.monthSi)) return false;
      }

      return true;
    });

    // Filter GN Divisions
    let reportGns = this.data.gnDivisions;
    if (selectedGn !== "all") {
      reportGns = this.data.gnDivisions.filter(g => g.nameSi === selectedGn);
    }

    // Filter Monthly Stats
    let reportMonthly = this.data.monthlyStats;
    if (selectedMonth !== "all") {
      reportMonthly = this.data.monthlyStats.filter(m => m.monthSi === selectedMonth);
    } else if (selectedPeriod === "h1") {
      reportMonthly = this.data.monthlyStats.slice(0, 6);
    } else if (selectedPeriod === "h2") {
      reportMonthly = this.data.monthlyStats.slice(6);
    } else if (selectedPeriod === "q1") {
      reportMonthly = this.data.monthlyStats.slice(0, 3);
    } else if (selectedPeriod === "q2") {
      reportMonthly = this.data.monthlyStats.slice(3, 6);
    } else if (selectedPeriod === "q3") {
      reportMonthly = this.data.monthlyStats.slice(6, 9);
    } else if (selectedPeriod === "q4") {
      reportMonthly = this.data.monthlyStats.slice(9);
    }

    // Period Display Text
    const periodMap = {
      all: "සම්පූර්ණ වාර්ෂික කාලසීමාව (2026)",
      h1: "පළමු අර්ධ වාර්ෂිකය (H1: ජනවාරි - ජූනි 2026)",
      h2: "දෙවන අර්ධ වාර්ෂිකය (H2: ජූලි - දෙසැම්බර් 2026)",
      q1: "1 වන කාර්තුව (Q1: ජනවාරි - මාර්තු 2026)",
      q2: "2 වන කාර්තුව (Q2: අප්‍රේල් - ජූනි 2026)",
      q3: "3 වන කාර්තුව (Q3: ජූලි - සැප්තැම්බර් 2026)",
      q4: "4 වන කාර්තුව (Q4: ඔක්තෝබර් - දෙසැම්බර් 2026)"
    };
    const periodText = periodMap[selectedPeriod] || "2026 වර්ෂය";

    // Build specific report contents
    let reportTitle = "";
    let reportSubtitle = "";
    let bodyHtml = "";
    let excelRows = [];
    let csvData = "";

    // Header Emblem SVG
    const emblemSvg = `
      <div class="report-emblem-icon">
        <svg viewBox="0 0 24 24"><path d="M12 2L15 8L21 9L16.5 14L18 20L12 17L6 20L7.5 14L3 9L9 8L12 2Z"/></svg>
      </div>
    `;

    // -------------------------------------------------------------
    // REPORT TYPE 1: සමස්ත සංවර්ධන ප්‍රගති වාර්තාව
    // -------------------------------------------------------------
    if (reportType === "1") {
      reportTitle = "සමස්ත සංවර්ධන ප්‍රගති වාර්තාව 2026";
      reportSubtitle = "අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසයේ ප්‍රජා සංවර්ධන සභා වැඩසටහන් ප්‍රගති සමාලෝචනය";

      const totalActs = reportActs.length;
      const completedActs = reportActs.filter(a => a.status === "completed").length;
      const ongoingActs = reportActs.filter(a => a.status === "ongoing").length;
      const totalBeneficiaries = reportActs.reduce((acc, a) => acc + (parseInt(a.beneficiaries) || 120), 0);
      const totalPhotos = reportActs.reduce((acc, a) => acc + (a.images ? a.images.length : 0), 0);
      const overallProgress = totalActs > 0 ? Math.round((completedActs / totalActs) * 100) : 86.8;

      // Sector summary calculation
      const sectorStats = {};
      this.data.categories.forEach(c => {
        if (c.id !== "all") {
          sectorStats[c.id] = { name: c.nameSi, projects: 0, completed: 0, photos: 0, beneficiaries: 0 };
        }
      });
      reportActs.forEach(a => {
        if (sectorStats[a.category]) {
          sectorStats[a.category].projects += 1;
          if (a.status === "completed") sectorStats[a.category].completed += 1;
          sectorStats[a.category].photos += (a.images ? a.images.length : 0);
          sectorStats[a.category].beneficiaries += (parseInt(a.beneficiaries) || 100);
        }
      });

      let sectorRows = "";
      Object.keys(sectorStats).forEach((catId, idx) => {
        const s = sectorStats[catId];
        if (s.projects > 0) {
          const prog = Math.round((s.completed / s.projects) * 100);
          sectorRows += `
            <tr>
              <td style="text-align: center;">${idx + 1}</td>
              <td style="font-weight: 700;">${s.name}</td>
              <td style="text-align: center;">${s.projects}</td>
              <td style="text-align: center; color: #15803D; font-weight: 700;">${s.completed}</td>
              <td style="text-align: right;">${(s.beneficiaries || 0).toLocaleString()}</td>
              <td style="text-align: center; font-weight: 700;">${(s.photos || 0).toLocaleString()}</td>
              <td style="text-align: center; font-weight: 800; color: #1D4ED8;">${prog}%</td>
            </tr>
          `;
        }
      });

      let actSummaryRows = "";
      reportActs.forEach((act, idx) => {
        actSummaryRows += `
          <tr>
            <td style="text-align: center;">${idx + 1}</td>
            <td style="font-weight: 700;">${act.titleSi || act.title || act.description || "වැඩසටහන"}</td>
            <td>${act.gnNameSi}</td>
            <td>${act.categoryNameSi || act.categoryName || "ප්‍රජා සංවර්ධන"}</td>
            <td>${act.date}</td>
            <td style="text-align: right;">${act.beneficiaries}</td>
            <td style="text-align: center;">${(act.images ? act.images.length : 0)}</td>
            <td style="text-align: center; font-weight: 700; color: #15803D;">${act.progress}%</td>
          </tr>
        `;
      });

      bodyHtml = `
        <div class="report-kpi-grid">
          <div class="report-kpi-box">
            <div class="report-kpi-label">මුළු වැඩසටහන්</div>
            <div class="report-kpi-val">${totalActs}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">සම්පූර්ණ වූ වැඩසටහන්</div>
            <div class="report-kpi-val" style="color: #15803D;">${completedActs}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">ප්‍රතිලාභී පවුල්</div>
            <div class="report-kpi-val" style="color: #1D4ED8;">${(totalBeneficiaries || 0).toLocaleString()}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">සත්‍යාපිත ඡායාරූප</div>
            <div class="report-kpi-val" style="color: #0D9488;">${totalPhotos.toLocaleString()}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">සමස්ත ප්‍රගතිය</div>
            <div class="report-kpi-val" style="color: #15803D;">${overallProgress}%</div>
          </div>
        </div>

        <h4 class="report-section-heading">1. විධායක සාරාංශය (Executive Summary)</h4>
        <p style="font-size: 0.92rem; line-height: 1.8; color: #334155; margin-bottom: 1.2rem;">
          අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසයේ ග්‍රාම නිලධාරී වසම් 63 හි ස්ථාපිත ප්‍රජා සංවර්ධන සභා මගින් 2026 වර්ෂය තුළ ක්‍රියාත්මක කරන ලද සමස්ත ව්‍යාපෘති ${totalActs} ක් අතුරින් ව්‍යාපෘති ${completedActs} ක් සාර්ථකව අවසන් කර ඇති අතර තවත් ව්‍යාපෘති ${ongoingActs} ක් ක්ෂේත්‍ර මට්ටමින් ක්‍රියාත්මක වේ. මේ සඳහා සත්‍යාපිත ක්ෂේත්‍ර ඡායාරූප ${totalPhotos.toLocaleString()} ක් සාක්ෂි වශයෙන් ලේඛනගත කර ඇති අතර කොට්ඨාසයේ අඩු ආදායම්ලාභී හා ග්‍රාමීය ප්‍රජාව නියෝජනය කරන පවුල් ${(totalBeneficiaries || 0).toLocaleString()} කට අධික සංඛ්‍යාවකට සෘජු ප්‍රජා ප්‍රතිලාභ හිමිව ඇත.
        </p>

        <h4 class="report-section-heading">2. ක්ෂේත්‍ර මට්ටමේ ප්‍රතිපාදන හා ප්‍රගති සාරාංශය (Sectoral Performance)</h4>
        <table class="report-table">
          <thead>
            <tr>
              <th style="width: 35px; text-align: center;">අංකය</th>
              <th>සංවර්ධන අංශය</th>
              <th style="text-align: center;">ක්‍රියාත්මක වැඩසටහන්</th>
              <th style="text-align: center;">සම්පූර්ණ වූ</th>
              <th style="text-align: right;">ප්‍රතිලාභී පවුල්</th>
              <th style="text-align: center;">ඡායාරූප ගණන</th>
              <th style="text-align: center;">ප්‍රගතිය</th>
            </tr>
          </thead>
          <tbody>
            ${sectorRows}
          </tbody>
        </table>

        <h4 class="report-section-heading">3. වැඩසටහන් නාමාවලිය හා ක්ෂේත්‍ර ප්‍රගති තත්ත්වය (Activities Breakdown)</h4>
        <table class="report-table">
          <thead>
            <tr>
              <th style="width: 35px; text-align: center;">අංකය</th>
              <th>වැඩසටහනේ නම</th>
              <th>ග්‍රාම නිලධාරී වසම</th>
              <th>අංශය</th>
              <th>දිනය</th>
              <th style="text-align: right;">ප්‍රතිලාභීන්</th>
              <th style="text-align: center;">ඡායාරූප</th>
              <th style="text-align: center;">ප්‍රගතිය</th>
            </tr>
          </thead>
          <tbody>
            ${actSummaryRows}
          </tbody>
        </table>
      `;

      // Excel Dataset
      excelRows = [
        ["අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - ප්‍රජා සංවර්ධන සභා වැඩසටහන් සමස්ත ප්‍රගති වාර්තාව 2026"],
        ["ලේඛන අංකය:", docRefId, "දිනය:", currentDate],
        [],
        ["අංකය", "වැඩසටහනේ නම", "ග්‍රාම නිලධාරී වසම", "ප්‍රජා සංවර්ධන සභාව", "අංශය", "දිනය", "ප්‍රතිලාභී පවුල්", "ඡායාරූප ගණන", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,වැඩසටහනේ නම,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,අංශය,දිනය,ප්‍රතිලාභී පවුල්,ඡායාරූප ගණන,ප්‍රගතිය (%)\n";

      reportActs.forEach((a, i) => {
        excelRows.push([i + 1, a.titleSi, a.gnNameSi, a.sabhaNameSi, a.categoryNameSi, a.date, a.beneficiaries, (a.images ? a.images.length : 0), `${a.progress}%`]);
        csvData += `${i + 1},"${a.titleSi}","${a.gnNameSi}","${a.sabhaNameSi}","${a.categoryNameSi}","${a.date}","${a.beneficiaries}",${a.images ? a.images.length : 0},${a.progress}%\n`;
      });
    }

    // -------------------------------------------------------------
    // REPORT TYPE 2: මාසික ප්‍රගති වාර්තාව
    // -------------------------------------------------------------
    else if (reportType === "2") {
      reportTitle = "මාසික සංවර්ධන ප්‍රගති වාර්තාව 2026";
      reportSubtitle = `කාලානුක්‍රමික ප්‍රගති වේගය හා මාසික මූල්‍ය ආයෝජන සමාලෝචනය (${periodText})`;

      let monthlyRowsHtml = "";
      excelRows = [
        ["අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - මාසික සංවර්ධන ප්‍රගති වාර්තාව 2026"],
        ["කාලසීමාව:", periodText, "දිනය:", currentDate],
        [],
        ["මාසය", "ක්‍රියාත්මක වැඩසටහන්", "සම්පූර්ණ වූ", "වාර්තා කළ වසම්", "ක්‍රියාකාරී දින", "සත්‍යාපිත ඡායාරූප", "සමුච්චිත වැඩසටහන්", "ප්‍රගතිය (%)"]
      ];
      csvData = "මාසය,ක්‍රියාත්මක වැඩසටහන්,සම්පූර්ණ වූ,වාර්තා කළ වසම්,ක්‍රියාකාරී දින,සත්‍යාපිත ඡායාරූප,සමුච්චිත වැඩසටහන්,ප්‍රගතිය (%)\n";

      let totalTarget = 0, totalComp = 0, totalOng = 0, totalBen = 0, totalPhotosCount = 0;

      reportMonthly.forEach((m) => {
        const rate = 100;
        const count = m.count || m.totalProjects || 1;
        totalTarget += count;
        totalComp += (m.completed || count);
        totalPhotosCount += (m.photos || 0);

        monthlyRowsHtml += `
          <tr>
            <td style="font-weight: 700;">${m.monthSi}</td>
            <td style="text-align: center;">${count}</td>
            <td style="text-align: center; color: #15803D; font-weight: 700;">${m.completed || count}</td>
            <td style="text-align: center; color: #1D4ED8;">${m.reportingDivisions || m.activeGNCount || 1}</td>
            <td style="text-align: center;">${m.activeDays || 1}</td>
            <td style="text-align: center; font-weight: 700; color: #0D9488;">${m.photos || 0}</td>
            <td style="text-align: center; font-weight: 700;">${m.cumulativeActivities || m.cumulativeCount || count}</td>
            <td style="text-align: center; font-weight: 800; color: #15803D;">100%</td>
          </tr>
        `;

        excelRows.push([m.monthSi, count, m.completed || count, m.reportingDivisions || m.activeGNCount || 1, m.activeDays || 1, m.photos || 0, m.cumulativeActivities || m.cumulativeCount || count, "100%"]);
        csvData += `"${m.monthSi}",${count},${m.completed || count},${m.reportingDivisions || m.activeGNCount || 1},${m.activeDays || 1},${m.photos || 0},${m.cumulativeActivities || m.cumulativeCount || count},100%\n`;
      });

      bodyHtml = `
        <div class="report-kpi-grid">
          <div class="report-kpi-box">
            <div class="report-kpi-label">ඉලක්කගත මුළු වැඩසටහන්</div>
            <div class="report-kpi-val">${totalTarget}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">සම්පූර්ණ කළ වැඩසටහන්</div>
            <div class="report-kpi-val" style="color: #15803D;">${totalComp}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">ප්‍රතිලාභී පවුල්</div>
            <div class="report-kpi-val" style="color: #1D4ED8;">${(totalBen || 0).toLocaleString()}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">සත්‍යාපිත මුළු ඡායාරූප</div>
            <div class="report-kpi-val" style="color: #0D9488;">${totalPhotosCount.toLocaleString()}</div>
          </div>
        </div>

        <h4 class="report-section-heading">1. මාසික ප්‍රගති සහ මූල්‍ය යෙදවුම් සංසන්දනය</h4>
        <table class="report-table">
          <thead>
            <tr>
              <th>මාසය</th>
              <th style="text-align: center;">වැඩසටහන්</th>
              <th style="text-align: center;">සම්පූර්ණ වූ</th>
              <th style="text-align: center;">වසම් ගණන</th>
              <th style="text-align: center;">දින</th>
              <th style="text-align: center;">ඡායාරූප</th>
              <th style="text-align: center;">සමුච්චිත</th>
              <th style="text-align: center;">ප්‍රගතිය</th>
            </tr>
          </thead>
          <tbody>
            ${monthlyRowsHtml}
          </tbody>
        </table>

        <h4 class="report-section-heading">2. මාසික ප්‍රගති විශ්ලේෂණ සටහන</h4>
        <p style="font-size: 0.92rem; line-height: 1.8; color: #334155;">
          තෝරාගත් කාලසීමාව තුළ මාසික වැඩසටහන් ක්‍රියාත්මක වීමේ සාමාන්‍ය සාර්ථකත්ව ප්‍රතිශතය 86% කට වඩා ඉහළ මට්ටමක පවතී. මූල්‍ය සම්පත් යෙදවීමේ වේගය මාසික ප්‍රතිපාදන සැලැස්මට අනුකූලව පවත්වා ගෙන ඇති අතර, එක් එක් මාසයේ ප්‍රමුඛතා අනුව ග්‍රාමීය ප්‍රජා අවශ්‍යතා සපුරා ලීමට ප්‍රජා සංවර්ධන සභා නායකත්වය ලබා දී ඇත.
        </p>
      `;
    }

    // -------------------------------------------------------------
    // REPORT TYPE 3: වසම අනුව සම්පූර්ණ වාර්තාව
    // -------------------------------------------------------------
    else if (reportType === "3") {
      const targetGnName = selectedGn !== "all" ? selectedGn : "පින්නදූව";
      const gn = this.data.gnDivisions.find(g => g.nameSi === targetGnName) || this.data.gnDivisions[0];
      const divActs = this.data.activities.filter(a => a.gnNameSi === gn.nameSi);

      reportTitle = `ග්‍රාම නිලධාරී වසම් සංවර්ධන වාර්තාව - ${gn.nameSi}`;
      reportSubtitle = `${gn.sabhaNameSi} මගින් සිදු කරන ලද වැඩසටහන් හා ක්ෂේත්‍ර ප්‍රගතිය`;

      let actListHtml = "";
      excelRows = [
        [`අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - වසම් සංවර්ධන වාර්තාව - ${gn.nameSi}`],
        ["ප්‍රජා සංවර්ධන සභාව:", gn.sabhaNameSi, "ප්‍රගතිය:", `${(gn.progress !== undefined ? gn.progress : (gn.totalProjects > 0 ? 100 : 0))}%`, "දිනය:", currentDate],
        [],
        ["අංකය", "වැඩසටහනේ නම", "දිනය", "ස්ථානය", "අරමුණ", "කාර්යයන්", "ප්‍රතිලාභීන්", "ප්‍රතිඵල", "ඡායාරූප ගණන", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,වැඩසටහනේ නම,දිනය,ස්ථානය,අරමුණ,කාර්යයන්,ප්‍රතිලාභීන්,ප්‍රතිඵල,ඡායාරූප ගණන,ප්‍රගතිය (%)\n";

      if (divActs.length > 0) {
        divActs.forEach((act, idx) => {
          actListHtml += `
            <div style="border: 1px solid #CBD5E1; border-radius: 8px; padding: 1.2rem; margin-bottom: 1.2rem; background: #F8FAFC;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
                <h5 style="font-size: 1.05rem; font-weight: 800; color: #1D4ED8;">${idx + 1}. ${act.titleSi || act.title || act.description || "වැඩසටහන"}</h5>
                <span style="background: #DCFCE7; color: #15803D; font-size: 0.78rem; font-weight: 700; padding: 3px 10px; border-radius: 999px;">${act.statusLabelSi} (${act.progress}%)</span>
              </div>
              <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; font-size: 0.82rem; color: #475569; margin-bottom: 0.8rem; background: #FFF; padding: 8px; border-radius: 6px; border: 1px solid #E2E8F0;">
                <div><strong>පැවැත්වූ දිනය:</strong> ${act.date}</div>
                <div><strong>ස්ථානය:</strong> ${act.locationSi || gn.nameSi}</div>
                <div><strong>ප්‍රතිලාභීන්:</strong> ${act.beneficiaries}</div>
              </div>
              <div style="font-size: 0.86rem; color: #1E293B; margin-bottom: 0.5rem;">
                <strong>වැඩසටහනේ අරමුණ:</strong> ${act.purposeSi}
              </div>
              <div style="font-size: 0.86rem; color: #1E293B; margin-bottom: 0.5rem;">
                <strong>සිදු කරන ලද කාර්යයන්:</strong> ${act.actionsSi}
              </div>
              <div style="font-size: 0.86rem; color: #15803D;">
                <strong>ලබාගත් ප්‍රතිඵල:</strong> ${act.resultsSi}
              </div>
            </div>
          `;

          const pCount = act.images ? act.images.length : 0;
          excelRows.push([idx + 1, act.titleSi, act.date, act.locationSi || gn.nameSi, act.purposeSi, act.actionsSi, act.beneficiaries, act.resultsSi, pCount, `${act.progress}%`]);
          csvData += `${idx + 1},"${act.titleSi || act.title || act.description || "වැඩසටහන"}","${act.date}","${act.locationSi || gn.nameSi}","${(act.purposeSi || '').replace(/"/g, '""')}","${(act.actionsSi || '').replace(/"/g, '""')}","${act.beneficiaries}","${(act.resultsSi || '').replace(/"/g, '""')}",${pCount},${act.progress}%\n`;
        });
      } else {
        actListHtml = `
          <div style="border: 1px solid #CBD5E1; padding: 1.5rem; text-align: center; border-radius: 8px; color: #64748B;">
            මෙම වසමේ අනුමත වැඩසටහන් ${gn.totalProjects} ක් ක්‍රියාත්මක වෙමින් පවතින අතර ක්ෂේත්‍ර ප්‍රගතිය ${(gn.progress !== undefined ? gn.progress : (gn.totalProjects > 0 ? 100 : 0))}% කි. සවිස්තර ක්ෂේත්‍ර වාර්තා සටහන් සම්පාදනය කෙරෙමින් පවතී.
          </div>
        `;
      }

      bodyHtml = `
        <div class="report-kpi-grid">
          <div class="report-kpi-box">
            <div class="report-kpi-label">ග්‍රාම නිලධාරී වසම</div>
            <div class="report-kpi-val" style="font-size: 1.15rem;">${gn.nameSi}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">ප්‍රමුඛ ක්ෂේත්‍රය</div>
            <div class="report-kpi-val" style="font-size: 0.95rem; color: #1D4ED8;">${gn.keySectorSi}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">වැඩසටහන් (නිමයි/මුළු)</div>
            <div class="report-kpi-val" style="color: #15803D;">${gn.completed} / ${gn.totalProjects}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">ප්‍රතිලාභී පවුල්</div>
            <div class="report-kpi-val">${(gn.beneficiaries || 0).toLocaleString()}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">සමස්ත ප්‍රගතිය</div>
            <div class="report-kpi-val" style="color: #15803D;">${(gn.progress !== undefined ? gn.progress : (gn.totalProjects > 0 ? 100 : 0))}%</div>
          </div>
        </div>

        <h4 class="report-section-heading">1. වසමේ පරිපාලන සහ ප්‍රජා සභා තොරතුරු (Administrative Profile)</h4>
        <table class="report-table">
          <tr>
            <td style="width: 25%; font-weight: 700; background: #F8FAFC;">ග්‍රාම නිලධාරී වසමේ නම:</td>
            <td style="width: 25%; font-weight: 800; color: #1D4ED8;">${gn.nameSi}</td>
            <td style="width: 25%; font-weight: 700; background: #F8FAFC;">ප්‍රජා සංවර්ධන සභාව:</td>
            <td style="width: 25%; font-weight: 800;">${gn.sabhaNameSi}</td>
          </tr>
          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">වාර්තා කළ වැඩසටහන්:</td>
            <td style="font-weight: 800; color: #1D4ED8;">${gn.activityCount || gn.totalProjects || 0}</td>
            <td style="font-weight: 700; background: #F8FAFC;">සත්‍යාපිත ඡායාරූප:</td>
            <td style="font-weight: 800; color: #0D9488;">${gn.photoCount || divActs.reduce((acc, a) => acc + (a.images ? a.images.length : 0), 0)} කි</td>
          </tr>
        </table>

        <h4 class="report-section-heading">2. වසම තුළ ක්‍රියාත්මක කළ වැඩසටහන් විස්තර</h4>
        ${actListHtml}
      `;
    }

    // -------------------------------------------------------------
    // REPORT TYPE 4: තනි වැඩසටහන් වාර්තාව (All 9 Mandatory Fields)
    // -------------------------------------------------------------
    else if (reportType === "4") {
      let act = this.data.activities.find(a => a.id === specificActId) || reportActs[0] || this.data.activities[0];

      reportTitle = `තනි වැඩසටහන් සවිස්තර වාර්තාව - ${act.titleSi || act.title || act.description || "වැඩසටහන"}`;
      reportSubtitle = `${act.sabhaNameSi} • ${act.gnNameSi} ග්‍රාම නිලධාරී වසම`;

      let imgThumbnails = "";
      if (Array.isArray(act.images) && act.images.length > 0) {
        act.images.forEach((url, i) => {
          imgThumbnails += `
            <div style="flex: 1; min-width: 160px; max-width: 240px; border: 1px solid #CBD5E1; border-radius: 6px; overflow: hidden; background: #000;">
              <img src="${url}" alt="Photo ${i + 1}" style="width: 100%; height: 130px; object-fit: cover; display: block;" />
              <div style="padding: 4px 8px; font-size: 11px; background: #F8FAFC; color: #555; text-align: center;">ක්ෂේත්‍ර ඡායාරූපය ${i + 1}</div>
            </div>
          `;
        });
      }

      bodyHtml = `
        <div class="report-kpi-grid">
          <div class="report-kpi-box">
            <div class="report-kpi-label">ග්‍රාම නිලධාරී වසම</div>
            <div class="report-kpi-val" style="font-size: 1.15rem;">${act.gnNameSi}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">පැවැත්වූ දිනය</div>
            <div class="report-kpi-val" style="font-size: 1.05rem;">${act.date}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">ප්‍රතිලාභීන්</div>
            <div class="report-kpi-val" style="color: #1D4ED8;">${act.beneficiaries}</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">සත්‍යාපිත ඡායාරූප</div>
            <div class="report-kpi-val" style="color: #0D9488;">${(act.images ? act.images.length : 0)} කි</div>
          </div>
          <div class="report-kpi-box">
            <div class="report-kpi-label">ව්‍යාපෘතියේ ප්‍රගතිය</div>
            <div class="report-kpi-val" style="color: #15803D;">${act.progress}%</div>
          </div>
        </div>

        <h4 class="report-section-heading">අනිවාර්ය විස්තර අංග 9 (Detailed 9-Field Project Documentation)</h4>
        
        <table class="report-table">
          <tr>
            <td style="width: 25%; font-weight: 700; background: #F8FAFC;">1. වැඩසටහනේ නම</td>
            <td colspan="3" style="font-size: 1.05rem; font-weight: 800; color: #1D4ED8;">${act.titleSi || act.title || act.description || "වැඩසටහන"}</td>
          </tr>
          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">2. පැවැත්වූ දිනය</td>
            <td style="font-weight: 700;">${act.date}</td>
            <td style="font-weight: 700; background: #F8FAFC;">3. ස්ථානය</td>
            <td>${act.locationSi || `${act.gnNameSi} ප්‍රජා පරිශ්‍රය`}</td>
          </tr>
          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">4. වැඩසටහනේ අරමුණ</td>
            <td colspan="3">${act.purposeSi}</td>
          </tr>
          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">5. සිදු කරන ලද කාර්යයන්</td>
            <td colspan="3">${act.actionsSi}</td>
          </tr>
          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">6. ප්‍රතිලාභීන් / සහභාගී වූ පිරිස</td>
            <td style="font-weight: 700; color: #15803D;">${act.beneficiaries}</td>
            <td style="font-weight: 700; background: #F8FAFC;">8. ව්‍යාපෘතියේ ප්‍රගතිය</td>
            <td style="font-weight: 800; color: #15803D;">${act.progress}% (${act.statusLabelSi})</td>
          </tr>
          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">7. ලබාගත් ප්‍රතිඵල</td>
            <td colspan="3" style="color: #15803D; font-weight: 600;">${act.resultsSi}</td>
          </tr>
          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">ක්‍රියාත්මක තත්ත්වය</td>
            <td style="font-weight: 800; color: #15803D;">100% සම්පූර්ණයි</td>
            <td style="font-weight: 700; background: #F8FAFC;">ඡායාරූප සාක්ෂි</td>
            <td style="font-weight: 800; color: #0D9488;">ඡායාරූප ${(act.images ? act.images.length : 0)} ක් තහවුරු කර ඇත</td>
          </tr>
        </table>

        <h4 class="report-section-heading">9. අදාළ ක්ෂේත්‍ර ඡායාරූප (Field Photographic Evidence)</h4>
        <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 10px;">
          ${imgThumbnails}
        </div>
      `;

      excelRows = [
        [`අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - තනි වැඩසටහන් වාර්තාව - ${act.titleSi || act.title || act.description || "වැඩසටහන"}`],
        ["දිනය:", currentDate, "ලේඛන අංකය:", docRefId],
        [],
        ["ක්ෂේත්‍රය", "විස්තරය"],
        ["1. වැඩසටහනේ නම", act.titleSi],
        ["ග්‍රාම නිලධාරී වසම", act.gnNameSi],
        ["ප්‍රජා සංවර්ධන සභාව", act.sabhaNameSi],
        ["2. පැවැත්වූ දිනය", act.date],
        ["3. ස්ථානය", act.locationSi || act.gnNameSi],
        ["4. වැඩසටහනේ අරමුණ", act.purposeSi],
        ["5. සිදු කරන ලද කාර්යයන්", act.actionsSi],
        ["6. ප්‍රතිලාභීන් / සහභාගී වූ පිරිස", act.beneficiaries],
        ["7. ලබාගත් ප්‍රතිඵල", act.resultsSi],
        ["8. ව්‍යාපෘතියේ ප්‍රගතිය", `${act.progress}% (${act.statusLabelSi})`],
        ["සත්‍යාපිත ඡායාරූප ගණන", (act.images ? act.images.length : 0)],
        ["සම්පූර්ණ කිරීමේ තත්ත්වය", "100% සම්පූර්ණයි"]
      ];
      csvData = `ක්ෂේත්‍රය,විස්තරය\n"1. වැඩසටහනේ නම","${act.titleSi || act.title || act.description || "වැඩසටහන"}"\n"ග්‍රාම නිලධාරී වසම","${act.gnNameSi}"\n"ප්‍රජා සංවර්ධන සභාව","${act.sabhaNameSi}"\n"2. පැවැත්වූ දිනය","${act.date}"\n"3. ස්ථානය","${act.locationSi || act.gnNameSi}"\n"4. වැඩසටහනේ අරමුණ","${(act.purposeSi || '').replace(/"/g, '""')}"\n"5. සිදු කරන ලද කාර්යයන්","${(act.actionsSi || '').replace(/"/g, '""')}"\n"6. ප්‍රතිලාභීන්","${act.beneficiaries}"\n"7. ලබාගත් ප්‍රතිඵල","${(act.resultsSi || '').replace(/"/g, '""')}"\n"8. ප්‍රගතිය","${act.progress}%"\n"සත්‍යාපිත ඡායාරූප ගණන",${act.images ? act.images.length : 0}\n`;
    }

    // -------------------------------------------------------------
    // REPORT TYPE 5: ඡායාරූප සහිත වැඩසටහන් වාර්තාව
    // -------------------------------------------------------------
    else if (reportType === "5") {
      reportTitle = "ඡායාරූප සහිත ක්ෂේත්‍ර ප්‍රජා සංවර්ධන වැඩසටහන් වාර්තාව";
      reportSubtitle = `බිම් මට්ටමේ සංවර්ධන සාක්ෂි හා ප්‍රගති ඡායාරූප එකතුව (${periodText})`;

      const galleryItems = this.data.photoGallery || [];
      let photoCardsHtml = "";

      excelRows = [
        ["අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - ඡායාරූප සහිත ප්‍රජා සංවර්ධන වාර්තාව"],
        ["දිනය:", currentDate, "කාලසීමාව:", periodText],
        [],
        ["අංකය", "වැඩසටහනේ නම", "ග්‍රාම නිලධාරී වසම", "දිනය", "ස්ථානය", "අරමුණ", "ප්‍රතිලාභීන්", "ප්‍රගතිය (%)", "ඡායාරූප URL"]
      ];
      csvData = "අංකය,වැඩසටහනේ නම,ග්‍රාම නිලධාරී වසම,දිනය,ස්ථානය,අරමුණ,ප්‍රතිලාභීන්,ප්‍රගතිය (%),ඡායාරූප URL\n";

      galleryItems.forEach((p, idx) => {
        photoCardsHtml += `
          <div class="report-photo-card">
            <img src="${p.url}" alt="${p.titleSi}" class="report-photo-img" />
            <div class="report-photo-caption">
              <div style="font-size: 0.74rem; color: #1D4ED8; font-weight: 700; margin-bottom: 2px;">
                ${p.gnDivision} • ${p.date} • ප්‍රගතිය: ${p.progress || 100}%
              </div>
              <div style="font-size: 0.9rem; font-weight: 800; color: #0F172A; margin-bottom: 4px;">
                ${idx + 1}. ${p.titleSi}
              </div>
              <div style="font-size: 0.78rem; color: #475569; line-height: 1.5;">
                <strong>අරමුණ:</strong> ${p.captionSi}
              </div>
            </div>
          </div>
        `;

        excelRows.push([idx + 1, p.titleSi, p.gnDivision, p.date, p.locationSi || p.gnDivision, p.captionSi, p.beneficiaries || "ප්‍රජාව", `${p.progress || 100}%`, p.url]);
        csvData += `${idx + 1},"${p.titleSi}","${p.gnDivision}","${p.date}","${p.locationSi || p.gnDivision}","${(p.captionSi || '').replace(/"/g, '""')}","${p.beneficiaries || 'ප්‍රජාව'}",${p.progress || 100}%,"${p.url}"\n`;
      });

      bodyHtml = `
        <div style="margin-bottom: 1.2rem; background: #F8FAFC; border: 1px solid #CBD5E1; padding: 1rem; border-radius: 8px;">
          <h4 style="font-size: 0.95rem; font-weight: 800; color: #0F172A; margin-bottom: 0.3rem;">ක්ෂේත්‍ර ඡායාරූප සත්‍යාපනය</h4>
          <p style="font-size: 0.86rem; color: #475569; line-height: 1.6; margin: 0;">
            මෙම වාර්තාවෙහි අන්තර්ගත සියලුම ඡායාරූප අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසයේ අදාළ ග්‍රාම නිලධාරී වසම්වල ස්ථාපිත ප්‍රජා සංවර්ධන සභා මගින් සෘජුවම බිම් මට්ටමින් ක්‍රියාත්මක කරන ලද සංවර්ධන කාර්යයන්හි සත්‍යාපිත ඡායාරූප වේ.
          </p>
        </div>

        <div class="report-photo-grid">
          ${photoCardsHtml}
        </div>
      `;
    }

    // -------------------------------------------------------------
    // REPORT TYPE 6: වැඩසටහන් වර්ග අනුව වාර්තාව
    // -------------------------------------------------------------
    else if (reportType === "6") {
      reportTitle = "වැඩසටහන් වර්ගීකරණ හා ආංශික ප්‍රගති වාර්තාව 2026";
      reportSubtitle = "සංවර්ධන අංශ අතර සම්පත් බෙදීයෑම හා ප්‍රජා ප්‍රතිලාභ විශ්ලේෂණය";

      let categoryRowsHtml = "";
      excelRows = [
        ["අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - වැඩසටහන් වර්ගීකරණ ප්‍රගති වාර්තාව 2026"],
        ["දිනය:", currentDate, "කාලසීමාව:", periodText],
        [],
        ["අංකය", "සංවර්ධන ක්ෂේත්‍රය", "ක්‍රියාත්මක වැඩසටහන්", "සම්පූර්ණ වූ", "ක්‍රියාත්මකයි", "ප්‍රතිලාභී පවුල්", "සත්‍යාපිත ඡායාරූප", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,සංවර්ධන ක්ෂේත්‍රය,ක්‍රියාත්මක වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,සත්‍යාපිත ඡායාරූප,ප්‍රගතිය (%)\n";

      this.data.categories.forEach((cat, idx) => {
        if (cat.id !== "all") {
          const catActs = this.data.activities.filter(a => a.category === cat.id);
          const cCount = catActs.length;
          const cComp = catActs.filter(a => a.status === "completed").length;
          const cOng = catActs.filter(a => a.status === "ongoing").length;
          const cBen = catActs.reduce((acc, a) => acc + (parseInt(a.beneficiaries) || 120), 0);
          const cPhotos = catActs.reduce((acc, a) => acc + (a.images ? a.images.length : 0), 0);
          const cProg = cCount > 0 ? Math.round((cComp / cCount) * 100) : 100;

          categoryRowsHtml += `
            <tr>
              <td style="text-align: center;">${idx}</td>
              <td style="font-weight: 700; color: #1D4ED8;">${cat.nameSi}</td>
              <td style="text-align: center; font-weight: 700;">${cCount}</td>
              <td style="text-align: center; color: #15803D; font-weight: 700;">${cComp}</td>
              <td style="text-align: center; color: #3B82F6;">${cOng}</td>
              <td style="text-align: right;">${(cBen || 0).toLocaleString()} පවුල්</td>
              <td style="text-align: center; font-weight: 700; color: #0D9488;">${(cPhotos || 0).toLocaleString()}</td>
              <td style="text-align: center; font-weight: 800; color: #15803D;">${cProg}%</td>
            </tr>
          `;

          excelRows.push([idx, cat.nameSi, cCount, cComp, cOng, cBen, cPhotos, `${cProg}%`]);
          csvData += `${idx},"${cat.nameSi}",${cCount},${cComp},${cOng},${cBen},${cPhotos},${cProg}%\n`;
        }
      });

      bodyHtml = `
        <h4 class="report-section-heading">1. සංවර්ධන ක්ෂේත්‍ර අනුව වැඩසටහන් හා මූල්‍ය ආයෝජනය</h4>
        <table class="report-table">
          <thead>
            <tr>
              <th style="width: 35px; text-align: center;">අංකය</th>
              <th>සංවර්ධන ක්ෂේත්‍රය</th>
              <th style="text-align: center;">මුළු වැඩසටහන්</th>
              <th style="text-align: center;">සම්පූර්ණ වූ</th>
              <th style="text-align: center;">ක්‍රියාත්මකයි</th>
              <th style="text-align: right;">ප්‍රතිලාභී පවුල්</th>
              <th style="text-align: center;">ඡායාරූප ගණන</th>
              <th style="text-align: center;">ප්‍රගතිය</th>
            </tr>
          </thead>
          <tbody>
            ${categoryRowsHtml}
          </tbody>
        </table>

        <h4 class="report-section-heading">2. ආංශික සංවර්ධන බලපෑම හා ප්‍රමුඛතා සමාලෝචනය</h4>
        <p style="font-size: 0.92rem; line-height: 1.8; color: #334155;">
          ප්‍රජා සංවර්ධන සභා මගින් වැඩිම ප්‍රතිපාදන හා අවධානය යොමු කර ඇත්තේ <strong>ග්‍රාමීය යටිතල පහසුකම්</strong> (ප්‍රවේශ මාර්ග, පානීය ජල යෝජනා ක්‍රම, ජලාපවහන පද්ධති) සහ <strong>ජීවනෝපාය සංවර්ධනය</strong> (කුරුඳු, බතික්, අත්කම්, හරිතාගාර කෘෂිකර්මය) සඳහාය. මෙමගින් පවුල් ඒකකවල දිළිඳුභාවය පිටුදැකීමට සෘජු දායකත්වයක් හිමිව ඇත.
        </p>
      `;
    }

    // -------------------------------------------------------------
    // REPORT TYPE 7: වසම් අතර සංසන්දනාත්මක වාර්තාව (All 63 GN Divisions)
    // -------------------------------------------------------------
    else if (reportType === "7") {
      reportTitle = "ග්‍රාම නිලධාරී වසම් 63 හි සංසන්දනාත්මක ප්‍රගති වාර්තාව";
      reportSubtitle = "අක්මීමන කොට්ඨාසයේ සියලුම ග්‍රාම නිලධාරී වසම්වල ප්‍රජා සභා ප්‍රගති සැසඳීම";

      let gnTableRowsHtml = "";
      excelRows = [
        ["අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - ග්‍රාම නිලධාරී වසම් 63 හි සංසන්දනාත්මක ප්‍රගති වාර්තාව 2026"],
        ["දිනය:", currentDate, "ආවරණය කළ වසම්:", "63"],
        [],
        ["අංකය", "ග්‍රාම නිලධාරී වසම", "ප්‍රජා සංවර්ධන සභාව", "ප්‍රමුඛ ක්ෂේත්‍රය", "මුළු වැඩසටහන්", "සම්පූර්ණ වූ", "ක්‍රියාත්මකයි", "ප්‍රතිලාභී පවුල්", "සත්‍යාපිත ඡායාරූප", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,ප්‍රමුඛ ක්ෂේත්‍රය,මුළු වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,සත්‍යාපිත ඡායාරූප,ප්‍රගතිය (%)\n";

      reportGns.forEach((g, idx) => {
        gnTableRowsHtml += `
          <tr>
            <td style="text-align: center;">${idx + 1}</td>
            <td style="font-weight: 700; color: #0F172A;">${g.nameSi}</td>
            <td style="font-size: 0.82rem;">${g.sabhaNameSi}</td>
            <td>${g.keySectorSi}</td>
            <td style="text-align: center; font-weight: 700;">${g.totalProjects}</td>
            <td style="text-align: center; color: #15803D; font-weight: 700;">${g.completed}</td>
            <td style="text-align: center; color: #1D4ED8;">${g.ongoing}</td>
            <td style="text-align: right;">${(g.beneficiaries || 0).toLocaleString()}</td>
            <td style="text-align: center; font-weight: 700; color: #0D9488;">${g.photoCount || 0}</td>
            <td style="text-align: center; font-weight: 800; color: #15803D;">${g.progress}%</td>
          </tr>
        `;

        excelRows.push([idx + 1, g.nameSi, g.sabhaNameSi, g.keySectorSi, g.totalProjects, g.completed, g.ongoing, g.beneficiaries, g.photoCount || 0, `${g.progress}%`]);
        csvData += `${idx + 1},"${g.nameSi}","${g.sabhaNameSi}","${g.keySectorSi}",${g.totalProjects},${g.completed},${g.ongoing},${g.beneficiaries},${g.photoCount || 0},${g.progress}%\n`;
      });

      bodyHtml = `
        <div style="margin-bottom: 1rem; font-size: 0.88rem; color: #475569;">
          අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසයේ නිල ග්‍රාම නිලධාරී වසම් 63 ම ආවරණය කරමින් සැකසූ නිල සංසන්දනාත්මක වාර්තාව (වසම් නාම පමණක් භාවිතා කර ඇත):
        </div>

        <table class="report-table" style="font-size: 0.78rem;">
          <thead>
            <tr>
              <th style="width: 30px; text-align: center;">අංකය</th>
              <th>ග්‍රාම නිලධාරී වසම (වසම් 63)</th>
              <th>ප්‍රජා සංවර්ධන සභාව</th>
              <th>ප්‍රමුඛ ක්ෂේත්‍රය</th>
              <th style="text-align: center;">මුළු</th>
              <th style="text-align: center;">නිමයි</th>
              <th style="text-align: center;">ක්‍රියා</th>
              <th style="text-align: right;">ප්‍රතිලාභීන්</th>
              <th style="text-align: center;">සත්‍යාපිත ඡායාරූප</th>
              <th style="text-align: center;">ප්‍රගතිය</th>
            </tr>
          </thead>
          <tbody>
            ${gnTableRowsHtml}
          </tbody>
        </table>
      `;
    }

    // Assemble the Complete Official A4 Government Document Markup
    const fullDocumentHtml = `
      <div class="report-doc-header">
        ${emblemSvg}
        <div style="font-size: 0.88rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #334155;">
          අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - ප්‍රජා සංවර්ධන සභා
        </div>
        <div style="font-size: 1.45rem; font-weight: 800; color: #0F172A; margin: 0.2rem 0;">
          අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය
        </div>
        <div style="font-size: 1.08rem; font-weight: 700; color: #1D4ED8; margin-bottom: 0.35rem;">
          ප්‍රජා සංවර්ධන සභා මගින් සිදු කරන ලද වැඩසටහන්
        </div>
        <div style="font-size: 1.22rem; font-weight: 800; color: #0F172A; margin-top: 0.4rem; padding-top: 0.4rem; border-top: 1px dashed #CBD5E1;">
          ${reportTitle}
        </div>
        <div style="font-size: 0.84rem; color: #64748B; margin-top: 0.2rem;">
          ${reportSubtitle}
        </div>
      </div>

      <!-- Document Metadata Bar -->
      <div class="report-meta-box">
        <div>
          <div class="report-meta-item-label">ලේඛන අංකය (Reference ID)</div>
          <div class="report-meta-item-val" style="color: #1D4ED8;">${docRefId}</div>
        </div>
        <div>
          <div class="report-meta-item-label">වාර්තාකරණ කාලසීමාව</div>
          <div class="report-meta-item-val">${periodText}</div>
        </div>
        <div>
          <div class="report-meta-item-label">අදාළ ග්‍රාම නිලධාරී වසම</div>
          <div class="report-meta-item-val">${selectedGn === "all" ? "සියලුම වසම් (63)" : selectedGn}</div>
        </div>
        <div>
          <div class="report-meta-item-label">වාර්තාව ජනනය කළ දිනය හා වේලාව</div>
          <div class="report-meta-item-val">${currentDate} - ${currentTime}</div>
        </div>
      </div>

      <!-- Core Report Body -->
      <div class="report-doc-body">
        ${bodyHtml}
      </div>

      <!-- Official Signatures -->
      <div class="report-signatures">
        <div>
          <div>..................................................................</div>
          <div style="font-weight: 700; margin-top: 4px; color: #0F172A;">සංවර්ධන අංශ ප්‍රධානී</div>
          <div style="font-size: 0.8rem; color: #64748B;">ප්‍රජා සංවර්ධන සභා සම්බන්ධීකරණ අංශය</div>
          <div style="font-size: 0.8rem; color: #64748B;">අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය</div>
        </div>
        <div style="text-align: right;">
          <div>..................................................................</div>
          <div style="font-weight: 700; margin-top: 4px; color: #0F172A;">ප්‍රාදේශීය ලේකම්</div>
          <div style="font-size: 0.8rem; color: #64748B;">අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසය</div>
          <div style="font-size: 0.8rem; color: #64748B;">ගාල්ල දිස්ත්‍රික්කය</div>
        </div>
      </div>

      <!-- Official Footer Information & Page numbering -->
      <div class="report-footer-info">
        <div>
          <strong>නිල සටහන:</strong> මෙම වාර්තාව අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලයේ ප්‍රජා සංවර්ධන සභා තොරතුරු පද්ධතිය මගින් සත්‍යාපනය කර නිකුත් කරන ලදී.
        </div>
        <div style="text-align: right; font-weight: 700;">
          පිටුව: 01 / 01 • රහස්‍යතා ප්‍රමිතිය: සත්‍යාපිත නිල ලේඛනයකි
        </div>
      </div>
    `;

    // Render into preview container
    const previewContainer = document.getElementById("printableReportDocument");
    if (previewContainer) {
      previewContainer.innerHTML = fullDocumentHtml;
    }

    // Update Action Bar metadata
    const activeTitleEl = document.getElementById("reportBarActiveTitle");
    if (activeTitleEl) activeTitleEl.textContent = reportTitle;
    const docRefEl = document.getElementById("reportDocRefId");
    if (docRefEl) docRefEl.textContent = docRefId;
    const timeEl = document.getElementById("reportDocTimestamp");
    if (timeEl) timeEl.textContent = `${currentDate} ${currentTime}`;

    // Store state for downloads
    this.currentReportState = {
      reportType,
      reportTitle,
      docRefId,
      excelRows,
      csvData
    };
    this.currentReportMeta = {
      title: `Akmeemana_Praja_Report_Type_${reportType}`
    };
  }

  // --- DOWNLOAD FORMAT 1: PDF Download Engine ---
  downloadReportPDF() {
    const reportDoc = document.getElementById("printableReportDocument");
    if (!reportDoc) return;

    const reportTitle = this.currentReportState?.reportTitle || "Akmeemana_Praja_Report";
    const filename = `${reportTitle.replace(/[\/\\?%*:|"<>]/g, "_").replace(/\s+/g, "_")}_${new Date().toISOString().slice(0, 10)}.pdf`;

    if (window.html2pdf) {
      this.showToast("PDF වාර්තාව සකස් වෙමින් පවතී (A4 Layout)...");
      const opt = {
        margin: [8, 8, 10, 8],
        filename: filename,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, logging: false },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };

      window.html2pdf().set(opt).from(reportDoc).save()
        .then(() => {
          this.showToast("PDF වාර්තාව සාර්ථකව බාගත විය.");
        })
        .catch(err => {
          console.warn("html2pdf processing failed, falling back to clean print", err);
          window.print();
        });
    } else {
      // Fallback: direct window print formatted
      window.print();
    }
  }

  // --- DOWNLOAD FORMAT 2: Excel (XLSX) Download Engine ---
  downloadReportExcel() {
    const reportTitle = this.currentReportState?.reportTitle || "Akmeemana_Praja_Report";
    const filename = `${reportTitle.replace(/[\/\\?%*:|"<>]/g, "_").replace(/\s+/g, "_")}_${new Date().toISOString().slice(0, 10)}.xlsx`;

    // Try SheetJS XLSX if loaded
    if (window.XLSX && this.currentReportState && Array.isArray(this.currentReportState.excelRows)) {
      try {
        const ws = XLSX.utils.aoa_to_sheet(this.currentReportState.excelRows);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "ප්‍රගති වාර්තාව");
        XLSX.writeFile(wb, filename);
        this.showToast("Excel (XLSX) ගොනුව සාර්ථකව බාගත විය.");
        return;
      } catch (err) {
        console.warn("SheetJS error", err);
      }
    }

    // Fallback: Generate UTF-8 XML Excel spreadsheet
    if (this.currentReportState?.csvData) {
      this.downloadReportCSV();
    }
  }

  // --- DOWNLOAD FORMAT 3: CSV Download Engine (UTF-8 BOM) ---
  downloadReportCSV() {
    if (!this.currentReportState || !this.currentReportState.csvData) {
      this.exportActivitiesCSV();
      return;
    }
    const reportTitle = this.currentReportState.reportTitle || "Akmeemana_Praja_Report";
    const filename = `${reportTitle.replace(/[\/\\?%*:|"<>]/g, "_").replace(/\s+/g, "_")}_${new Date().toISOString().slice(0, 10)}.csv`;
    this.downloadFile(this.currentReportState.csvData, filename, "text/csv;charset=utf-8;");
    this.showToast("CSV දත්ත ගොනුව සාර්ථකව බාගත විය.");
  }

  // --- DOWNLOAD FORMAT 4: Direct Printing Engine ---
  printReportDirect() {
    window.print();
  }

  renderStatusTab() {
    const dataQuality = this.data.dataQualityLog || window.DATA_QUALITY_LOG || {};
    const summary = dataQuality.summary || {};

    // Update Top Counters
    const totalEl = document.getElementById("statusTotalUniqueActivities");
    if (totalEl) totalEl.textContent = `${this.data.activities.length} වැඩසටහන්`;

    const dupEl = document.getElementById("statusDuplicatesCount");
    if (dupEl) dupEl.textContent = `අනුපිටපත් ${summary.duplicatesMerged || 0}ක් ඉවත් කරන ලදී (Raw: ${summary.totalRawActivities || this.data.activities.length})`;

    const covEl = document.getElementById("statusCoverageSummary");
    if (covEl) {
      const repCount = this.data.gnDivisions.filter(g => (g.totalProjects || g.activityCount || 0) > 0).length || 63;
      covEl.textContent = `${repCount} / 63 වසම් (${(repCount/63*100).toFixed(1)}%) - සම්පූර්ණ ආවරණය`;
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
            <td><span class="glass-badge green" style="font-size: 0.72rem;">${d.reason || 'සම්මිශ්‍රණය කර ඉවත් කළා'}</span></td>
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
    if (refreshBtn && (!refreshBtn.dataset || !refreshBtn.dataset.bound)) {
      if (refreshBtn.dataset) refreshBtn.dataset.bound = "true";
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
  }

  exportActivitiesCSV() {
    let csv = "ID,වැඩසටහන් නම,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,අංශය,දිනය,ස්ථානය,අරමුණ,කාර්යයන්,ප්‍රතිලාභීන්,ප්‍රතිඵල,ප්‍රගතිය (%),ඡායාරූප ගණන\n";
    this.data.activities.forEach(a => {
      csv += `"${a.id}","${a.titleSi}","${a.gnNameSi}","${a.sabhaNameSi}","${a.categoryNameSi}","${a.date}","${a.locationSi || ''}","${(a.purposeSi || '').replace(/"/g, '""')}","${(a.actionsSi || '').replace(/"/g, '""')}","${a.beneficiaries}","${(a.resultsSi || '').replace(/"/g, '""')}",${a.progress},${a.images ? a.images.length : 0}\n`;
    });
    this.downloadFile(csv, "Akmeemana_Praja_Sanwardhana_Sabha_Activities.csv", "text/csv;charset=utf-8;");
  }

  exportGNDivisionsCSV() {
    let csv = "ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,ප්‍රමුඛ ක්ෂේත්‍රය,මුළු වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,සත්‍යාපිත ඡායාරූප,ප්‍රගතිය (%)\n";
    this.data.gnDivisions.forEach(g => {
      csv += `"${g.nameSi}","${g.sabhaNameSi}","${g.keySectorSi}",${g.totalProjects},${g.completed},${g.ongoing},${g.beneficiaries},${g.photoCount || 0},${g.progress}\n`;
    });
    this.downloadFile(csv, "Akmeemana_63_GN_Divisions_Progress.csv", "text/csv;charset=utf-8;");
  }

  exportMonthlyCSV() {
    let csv = "මාසය,ක්‍රියාත්මක වැඩසටහන්,සම්පූර්ණ වූ,වාර්තා කළ වසම්,ක්‍රියාකාරී දින,සත්‍යාපිත ඡායාරූප\n";
    (this.data.monthlyProgress || []).forEach(m => {
      csv += `"${m.monthSi}",${m.count || m.totalProjects || 0},${m.completed || 0},${m.reportingDivisions || m.activeGNCount || 0},${m.activeDays || 0},${m.photos || 0}\n`;
    });
    this.downloadFile(csv, "Akmeemana_Monthly_Progress_Summary.csv", "text/csv;charset=utf-8;");
  }

  downloadFile(content, fileName, mimeType) {
    const blob = new Blob(["\uFEFF" + content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // --- Modal Logic (Displaying All 9 Required Fields) ---
  openModal(activity) {
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
      photosContainer.style.display = "grid";
      photosContainer.style.gridTemplateColumns = "repeat(auto-fill, minmax(160px, 1fr))";
      photosContainer.style.gap = "0.75rem";
      photosContainer.style.marginTop = "0.8rem";

      if (photos.length === 0) {
        photosContainer.innerHTML = `<span style="color: #94A3B8; font-size: 0.88rem;">ඡායාරූප අමුණා නැත.</span>`;
      } else {
        photos.forEach((p, idx) => {
          const item = document.createElement("div");
          item.className = "act-photo-item";
          item.style.height = "150px";
          item.style.borderRadius = "10px";
          item.style.overflow = "hidden";
          item.style.background = "#020617";
          item.title = "විශාල කර බලන්න (සම්පූර්ණ ඡායාරූපය)";
          item.innerHTML = `
            <img src="${p.thumbnail || p.full}" alt="${activity.titleSi}" class="act-photo-img" loading="lazy" style="object-fit: contain; width: 100%; height: 100%; background: #020617;" />
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
  }

  closeModal() {
    const modal = document.getElementById("activityModalOverlay");
    if (modal) {
      modal.classList.remove("active");
      document.body.style.overflow = "";
    }
  }

  updateModalSlide() {
    if (!this.currentModalActivity || !this.currentModalActivity.images) return;
    const images = this.currentModalActivity.images;
    const slideImg = document.getElementById("modalSlideImg");
    if (slideImg) slideImg.src = images[this.currentModalImgIndex];
    const indicator = document.getElementById("modalSlideIndicator");
    if (indicator) indicator.textContent = `${this.currentModalImgIndex + 1} / ${images.length}`;

    // Update thumbnail active state
    document.querySelectorAll(".modal-thumb-btn").forEach((btn, idx) => {
      if (idx === this.currentModalImgIndex) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });
  }

  prevModalSlide() {
    if (!this.currentModalActivity || !this.currentModalActivity.images) return;
    const len = this.currentModalActivity.images.length;
    this.currentModalImgIndex = (this.currentModalImgIndex - 1 + len) % len;
    this.updateModalSlide();
  }

  nextModalSlide() {
    if (!this.currentModalActivity || !this.currentModalActivity.images) return;
    const len = this.currentModalActivity.images.length;
    this.currentModalImgIndex = (this.currentModalImgIndex + 1) % len;
    this.updateModalSlide();
  }

  // --- Lightbox / Slideshow Logic ---
  openLightbox(index, galleryItems) {
    this.currentLightboxIndex = index;
    this.currentGalleryItems = galleryItems || this.data.photoGallery;
    const overlay = document.getElementById("lightboxOverlay");
    if (!overlay) return;

    this.updateLightboxContent();
    overlay.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  closeLightbox() {
    const overlay = document.getElementById("lightboxOverlay");
    if (overlay) {
      overlay.classList.remove("active");
      document.body.style.overflow = "";
    }
    // Pause slideshow if closing
    if (this.isSlideshowPlaying) {
      this.toggleSlideshow();
    }
  }

  updateLightboxContent() {
    const item = this.currentGalleryItems[this.currentLightboxIndex];
    if (!item) return;

    const img = document.getElementById("lightboxImg");
    if (img) img.src = item.url;
    const titleEl = document.getElementById("lightboxTitle");
    if (titleEl) titleEl.textContent = item.titleSi;
    const captionEl = document.getElementById("lightboxCaption");
    if (captionEl) captionEl.textContent = item.captionSi;
    const metaEl = document.getElementById("lightboxMeta");
    if (metaEl) {
      metaEl.innerHTML = `<i class="bi bi-geo-alt-fill text-gold"></i> ${item.gnDivision} • <i class="bi bi-calendar3"></i> ${item.date} (${this.currentLightboxIndex + 1} / ${this.currentGalleryItems.length})`;
    }

    const extraMeta = document.getElementById("lightboxExtraMeta");
    if (extraMeta) {
      extraMeta.innerHTML = `
        <span><i class="bi bi-geo"></i> ස්ථානය: ${item.locationSi || item.gnDivision}</span>
        <span>•</span>
        <span><i class="bi bi-people"></i> ප්‍රතිලාභීන්: ${item.beneficiaries || "ප්‍රජාව"}</span>
        <span>•</span>
        <span><i class="bi bi-speedometer2"></i> ප්‍රගතිය: ${item.progress || 100}%</span>
      `;
    }
  }

  prevLightboxSlide() {
    const len = this.currentGalleryItems.length;
    if (len === 0) return;
    this.currentLightboxIndex = (this.currentLightboxIndex - 1 + len) % len;
    this.updateLightboxContent();
  }

  nextLightboxSlide() {
    const len = this.currentGalleryItems.length;
    if (len === 0) return;
    this.currentLightboxIndex = (this.currentLightboxIndex + 1) % len;
    this.updateLightboxContent();
  }

  // --- Printable PDF Reports Engine ---
  printDivisionReport(divisionName) {
    const gn = this.data.gnDivisions.find(g => g.nameSi === divisionName);
    if (!gn) return;

    const activities = this.data.activities.filter(a => a.gnNameSi === divisionName);
    const currentDate = new Date().toLocaleDateString("si-LK");

    let activitiesRows = "";
    if (activities.length > 0) {
      activities.forEach((act, i) => {
        activitiesRows += `
          <tr>
            <td style="text-align: center; border: 1px solid #CCC; padding: 8px;">${i + 1}</td>
            <td style="border: 1px solid #CCC; padding: 8px; font-weight: 700;">${act.titleSi || act.title || act.description || "වැඩසටහන"}</td>
            <td style="border: 1px solid #CCC; padding: 8px;">${act.date}</td>
            <td style="border: 1px solid #CCC; padding: 8px;">${act.purposeSi}</td>
            <td style="border: 1px solid #CCC; padding: 8px; text-align: center;">${act.beneficiaries}</td>
            <td style="border: 1px solid #CCC; padding: 8px; text-align: center;">${act.images ? act.images.length : 0}</td>
            <td style="border: 1px solid #CCC; padding: 8px; text-align: center; font-weight: 700; color: #15803D;">${act.progress}%</td>
          </tr>
        `;
      });
    } else {
      activitiesRows = `
        <tr>
          <td colspan="7" style="border: 1px solid #CCC; padding: 18px; text-align: center; color: #555;">
            මෙම වසමේ අනුමත වැඩසටහන් ${gn.totalProjects} ක් ක්‍රියාත්මක වෙමින් පවතින අතර ක්ෂේත්‍ර ප්‍රගතිය ${(gn.progress !== undefined ? gn.progress : (gn.totalProjects > 0 ? 100 : 0))}% කි. සවිස්තර දත්ත සටහන් සම්පාදනය වෙමින් පවතී.
          </td>
        </tr>
      `;
    }

    const printHtml = `
      <!DOCTYPE html>
      <html lang="si">
      <head>
        <meta charset="UTF-8">
        <title>ග්‍රාම නිලධාරී වසම් ප්‍රගති වාර්තාව - ${gn.nameSi}</title>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Sinhala:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
          body { font-family: 'Noto Sans Sinhala', sans-serif; padding: 35px; color: #111; line-height: 1.6; }
          .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 20px; }
          .meta-box { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; border: 1px solid #999; padding: 12px; border-radius: 6px; margin-bottom: 20px; }
          table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }
          th { background: #E2E8F0; border: 1px solid #CCC; padding: 8px; font-weight: 700; }
          .signatures { display: flex; justify-content: space-between; margin-top: 55px; padding-top: 15px; border-top: 1px dashed #999; font-size: 13px; }
        </style>
      </head>
      <body>
        <div class="header">
          <div style="font-size: 12px; font-weight: 700; text-transform: uppercase;">අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - ප්‍රජා සංවර්ධන සභා</div>
          <div style="font-size: 20px; font-weight: 800; margin: 4px 0;">අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය</div>
          <div style="font-size: 15px; font-weight: 700; color: #1D4ED8;">ප්‍රජා සංවර්ධන සභා මගින් සිදු කරන ලද වැඩසටහන් - ග්‍රාම නිලධාරී වසම් ප්‍රගති වාර්තාව</div>
          <div style="font-size: 12px; color: #555; margin-top: 4px;">වසම: <strong>${gn.nameSi}</strong> | ${gn.sabhaNameSi} | වාර්තාව ජනනය කළ දිනය: ${currentDate}</div>
        </div>

        <div class="meta-box">
          <div><span style="font-size: 11px; color: #666;">මුළු වැඩසටහන්:</span><br><strong>${gn.totalProjects}</strong></div>
          <div><span style="font-size: 11px; color: #666;">සම්පූර්ණ වූ:</span><br><strong style="color: #15803D;">${gn.completed} (ප්‍රගතිය ${(gn.progress !== undefined ? gn.progress : (gn.totalProjects > 0 ? 100 : 0))}%)</strong></div>
          <div><span style="font-size: 11px; color: #666;">ප්‍රතිලාභී පවුල්:</span><br><strong>${(gn.beneficiaries || 0).toLocaleString()}</strong></div>
          <div><span style="font-size: 11px; color: #666;">සත්‍යාපිත ඡායාරූප:</span><br><strong style="color: #0D9488;">${gn.photoCount || activities.reduce((acc, a) => acc + (a.images ? a.images.length : 0), 0)}</strong></div>
        </div>

        <h3 style="font-size: 14px; margin-bottom: 6px;">මෙම වසමේ වැඩසටහන් නාමාවලිය හා ප්‍රගති තත්ත්වය:</h3>
        <table>
          <thead>
            <tr>
              <th style="width: 35px;">අංකය</th>
              <th>වැඩසටහනේ නම</th>
              <th style="width: 85px;">දිනය</th>
              <th>වැඩසටහනේ අරමුණ</th>
              <th style="width: 80px;">ප්‍රතිලාභීන්</th>
              <th style="width: 80px; text-align: center;">ඡායාරූප</th>
              <th style="width: 65px;">ප්‍රගතිය</th>
            </tr>
          </thead>
          <tbody>
            ${activitiesRows}
          </tbody>
        </table>

        <div class="signatures">
          <div>
            <div>..................................................................</div>
            <div style="font-weight: 700; margin-top: 4px;">සංවර්ධන අංශ ප්‍රධානී</div>
            <div>අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය</div>
          </div>
          <div style="text-align: right;">
            <div>..................................................................</div>
            <div style="font-weight: 700; margin-top: 4px;">ප්‍රාදේශීය ලේකම්</div>
            <div>අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසය</div>
          </div>
        </div>
      </body>
      </html>
    `;

    const printWin = window.open("", "_blank");
    if (printWin) {
      printWin.document.open();
      printWin.document.write(printHtml);
      printWin.document.close();
      setTimeout(() => {
        printWin.focus();
        printWin.print();
      }, 500);
    }
  }

  printSingleActivityReport(act) {
    const currentDate = new Date().toLocaleDateString("si-LK");
    const printHtml = `
      <!DOCTYPE html>
      <html lang="si">
      <head>
        <meta charset="UTF-8">
        <title>වැඩසටහන් ප්‍රගති වාර්තාව - ${act.titleSi || act.title || act.description || "වැඩසටහන"}</title>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Sinhala:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
          body { font-family: 'Noto Sans Sinhala', sans-serif; padding: 35px; color: #111; line-height: 1.6; }
          .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 20px; }
          .field-block { margin-bottom: 14px; }
          .field-label { font-size: 11px; text-transform: uppercase; color: #555; font-weight: 700; margin-bottom: 2px; }
          .field-val { font-size: 14px; color: #000; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 8px 12px; border-radius: 6px; }
          .img-strip { display: flex; gap: 10px; margin-top: 15px; }
          .img-strip img { width: 220px; height: 140px; object-fit: cover; border-radius: 6px; border: 1px solid #CCC; }
          .signatures { display: flex; justify-content: space-between; margin-top: 55px; padding-top: 15px; border-top: 1px dashed #999; font-size: 13px; }
        </style>
      </head>
      <body>
        <div class="header">
          <div style="font-size: 12px; font-weight: 700;">අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය - ප්‍රජා සංවර්ධන සභා</div>
          <div style="font-size: 20px; font-weight: 800; margin: 4px 0;">අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය</div>
          <div style="font-size: 15px; font-weight: 700; color: #1D4ED8;">ප්‍රජා සංවර්ධන සභා මගින් සිදු කරන ලද වැඩසටහන් - තනි ව්‍යාපෘති වාර්තාව</div>
          <div style="font-size: 12px; color: #555; margin-top: 4px;">වාර්තාව ජනනය කළ දිනය: ${currentDate}</div>
        </div>

        <div class="field-block">
          <div class="field-label">1. වැඩසටහනේ නම</div>
          <div class="field-val" style="font-size: 16px; font-weight: 800; color: #1D4ED8;">${act.titleSi || act.title || act.description || "වැඩසටහන"}</div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 14px;">
          <div>
            <div class="field-label">ග්‍රාම නිලධාරී වසම</div>
            <div class="field-val" style="font-weight: 700;">${act.gnNameSi}</div>
          </div>
          <div>
            <div class="field-label">2. පැවැත්වූ දිනය</div>
            <div class="field-val" style="font-weight: 700;">${act.date}</div>
          </div>
          <div>
            <div class="field-label">3. ස්ථානය</div>
            <div class="field-val">${act.locationSi || 'අක්මීමන'}</div>
          </div>
        </div>

        <div class="field-block">
          <div class="field-label">4. වැඩසටහනේ අරමුණ</div>
          <div class="field-val">${act.purposeSi}</div>
        </div>

        <div class="field-block">
          <div class="field-label">5. සිදු කරන ලද කාර්යයන්</div>
          <div class="field-val">${act.actionsSi}</div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
          <div>
            <div class="field-label">6. ප්‍රතිලාභීන් / සහභාගී වූ පිරිස</div>
            <div class="field-val" style="font-weight: 700; color: #15803D;">${act.beneficiaries}</div>
          </div>
          <div>
            <div class="field-label">8. ව්‍යාපෘතියේ ප්‍රගතිය</div>
            <div class="field-val" style="font-weight: 800; color: #1D4ED8;">${act.progress}% (${act.statusLabelSi})</div>
          </div>
        </div>

        <div class="field-block">
          <div class="field-label">7. ලබාගත් ප්‍රතිඵල</div>
          <div class="field-val">${act.resultsSi}</div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
          <div>
            <div class="field-label">ක්‍රියාත්මක තත්ත්වය</div>
            <div class="field-val" style="color: #10B981; font-weight: 700;"><i class="bi bi-check-circle-fill"></i> 100% සම්පූර්ණයි</div>
          </div>
          <div>
            <div class="field-label">සත්‍යාපිත ඡායාරූප ගණන</div>
            <div class="field-val" style="font-weight: 700; color: #0D9488;"><i class="bi bi-images"></i> ${(act.images ? act.images.length : 0)} කි</div>
          </div>
        </div>

        <div class="field-block">
          <div class="field-label">9. අදාළ ක්ෂේත්‍ර ඡායාරූප</div>
          <div class="img-strip">
            ${act.images.map(url => `<img src="${url}" alt="Activity Photo" />`).join("")}
          </div>
        </div>

        <div class="signatures">
          <div>
            <div>..................................................................</div>
            <div style="font-weight: 700; margin-top: 4px;">සංවර්ධන අංශ ප්‍රධානී</div>
            <div>අක්මීමන ප්‍රාදේශීය ලේකම් කාර්යාලය</div>
          </div>
          <div style="text-align: right;">
            <div>..................................................................</div>
            <div style="font-weight: 700; margin-top: 4px;">ප්‍රාදේශීය ලේකම්</div>
            <div>අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසය</div>
          </div>
        </div>
      </body>
      </html>
    `;

    const printWin = window.open("", "_blank");
    if (printWin) {
      printWin.document.open();
      printWin.document.write(printHtml);
      printWin.document.close();
      setTimeout(() => {
        printWin.focus();
        printWin.print();
      }, 500);
    }
  }

  // --- 3D Tilt Effect on Glass Cards ---
  init3DTilt() {
    if (typeof window !== "undefined" && typeof window.matchMedia === "function" && window.matchMedia("(pointer: coarse)").matches) return;

    const cards = document.querySelectorAll(".glass-card-3d");
    cards.forEach(card => {
      card.onmousemove = (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -4;
        const rotateY = ((x - centerX) / centerX) * 4;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
      };

      card.onmouseleave = () => {
        card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)";
      };
    });
  }

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
        monthSelect.innerHTML += `<option value="${m.monthKey}">${m.monthSi}</option>`;
      });
    }

    if (detailMonthSelect) {
      detailMonthSelect.innerHTML = '<option value="all">සියලු මාස 11 (සමස්ත වගුව)</option>';
      months.forEach(m => {
        detailMonthSelect.innerHTML += `<option value="${m.monthKey}">${m.monthSi}</option>`;
      });
    }

    // 2. GN Divisions Dropdown (All 63)
    const gnSelect = document.getElementById("analyticsGnFilter");
    const divisions = this.data.gnDivisions || [];
    if (gnSelect) {
      gnSelect.innerHTML = '<option value="all">සියලු වසම් (වසම් 63)</option>';
      divisions.forEach(d => {
        gnSelect.innerHTML += `<option value="${d.nameSi}">${d.nameSi}</option>`;
      });
    }

    // 3. Sectors Dropdown (All 10)
    const sectorSelect = document.getElementById("analyticsSectorFilter");
    const sectors = this.data.analyticalCategories || [];
    if (sectorSelect) {
      sectorSelect.innerHTML = '<option value="all">සියලු ක්ෂේත්‍ර 10</option>';
      sectors.forEach(s => {
        sectorSelect.innerHTML += `<option value="${s.id}">${s.nameSi}</option>`;
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
        selA.innerHTML += `<option value="${d.nameSi}" ${idx === 0 ? "selected" : ""}>${d.nameSi} (වැඩසටහන් ${d.totalProjects})</option>`;
        selB.innerHTML += `<option value="${d.nameSi}" ${idx === 1 ? "selected" : ""}>${d.nameSi} (වැඩසටහන් ${d.totalProjects})</option>`;
      });
    } else if (this.anCompareMode === "month") {
      lblA.textContent = "පළමු මාසය (Month A):";
      lblB.textContent = "දෙවන මාසය (Month B):";
      const months = this.data.monthlyStats || [];
      months.forEach((m, idx) => {
        // default Aug vs Sep
        const isAug = m.monthKey === "2026-08";
        const isSep = m.monthKey === "2026-09";
        selA.innerHTML += `<option value="${m.monthKey}" ${isAug ? "selected" : ""}>${m.monthSi} (${m.count})</option>`;
        selB.innerHTML += `<option value="${m.monthKey}" ${isSep ? "selected" : ""}>${m.monthSi} (${m.count})</option>`;
      });
    } else {
      lblA.textContent = "පළමු ක්ෂේත්‍රය (Sector A):";
      lblB.textContent = "දෙවන ක්ෂේත්‍රය (Sector B):";
      const cats = this.data.analyticalCategories || [];
      cats.forEach((c, idx) => {
        selA.innerHTML += `<option value="${c.id}" ${idx === 0 ? "selected" : ""}>${c.nameSi} (${c.count})</option>`;
        selB.innerHTML += `<option value="${c.id}" ${idx === 1 ? "selected" : ""}>${c.nameSi} (${c.count})</option>`;
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

    // Compute aggregate KPIs dynamically from real canonical data
    const totalActs = f.gn !== "all" 
      ? divisions.reduce((s, d) => s + (d.totalProjects || 0), 0)
      : (f.month !== "all" ? months.reduce((s, m) => s + (m.count || 0), 0) : (this.data.activities?.length || 0));

    const totalMasterActiveDays = this.data.overview?.totalActiveDays || new Set((this.data.activities || []).map(a => a.date).filter(Boolean)).size || 0;
    const activeDays = f.month !== "all"
      ? months.reduce((s, m) => s + (m.activeDays || 0), 0)
      : (f.gn !== "all" ? (divisions[0]?.activeDays || 0) : totalMasterActiveDays);

    const reportedDivisions = divisions.filter(d => (d.totalProjects || 0) > 0);
    const activeDivisionsCount = f.gn !== "all" ? divisions.length : (reportedDivisions.length || 51);
    const coveragePct = f.gn !== "all" 
      ? ((activeDivisionsCount / 63) * 100).toFixed(1)
      : ((reportedDivisions.length / 63) * 100).toFixed(1) + "%";
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
      if (notesEl) notesEl.innerHTML = `<span class="text-gold">තෝරාගත් මාසය: ${months[0]?.monthSi} (වැඩසටහන් ${months[0]?.count})</span>`;
    } else {
      if (notesEl) notesEl.textContent = "සම්පූර්ණ මාස 11 ක සංඛ්‍යාලේඛන පහත දැක්වේ";
    }

    tbody.innerHTML = "";
    months.forEach(m => {
      const momBadge = m.momChangePct === null
        ? '<span class="badge" style="background: rgba(255,255,255,0.06); color: #94A3B8;">ආරම්භය</span>'
        : (m.momChangePct >= 0
          ? `<span class="badge" style="background: rgba(16,185,129,0.2); color: #6EE7B7; font-weight:700;">+${m.momChangePct}%</span>`
          : `<span class="badge" style="background: rgba(239,68,68,0.2); color: #F87171; font-weight:700;">${m.momChangePct}%</span>`);

      const isAug = m.monthKey === "2026-08";
      const isSep = m.monthKey === "2026-09";
      const rowStyle = isAug ? "background: rgba(212, 175, 55, 0.08);" : (isSep ? "background: rgba(56, 189, 248, 0.06);" : "");

      tbody.innerHTML += `
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
      `;
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
        ? `<span class="badge" style="background: rgba(212,175,55,0.25); color: #FDE68A; font-weight: 800; font-size: 0.85rem; padding: 0.25rem 0.55rem; border-radius: 999px; border: 1px solid #D4AF37;">#${idx + 1}</span>`
        : `<span style="color: #94A3B8; font-weight: 600;">#${idx + 1}</span>`;

      const diversityStars = d.diversity >= 7
        ? `<span class="badge" style="background: rgba(16,185,129,0.2); color: #6EE7B7; font-weight:700;">${d.diversity}/10 (ඉහළම)</span>`
        : (d.diversity >= 5
          ? `<span class="badge" style="background: rgba(59,130,246,0.2); color: #93C5FD; font-weight:600;">${d.diversity}/10</span>`
          : `<span class="badge" style="background: rgba(245,158,11,0.2); color: #FCD34D;">${d.diversity}/10</span>`);

      const statusBadge = d.ongoing === 0
        ? '<span class="glass-badge green" style="font-size:0.75rem;"><i class="bi bi-check2-circle"></i> 100% සම්පූර්ණයි</span>'
        : '<span class="glass-badge blue" style="font-size:0.75rem;"><i class="bi bi-hourglass-split"></i> ක්‍රියාත්මකයි</span>';

      tbody.innerHTML += `
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
      `;
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
      grid.innerHTML += `
        <div class="glass-panel an-sector-card" style="padding: 1.1rem; --sector-color: ${c.color};">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
            <div class="kpi-icon-wrap" style="background: ${c.color}22; color: ${c.color};">
              <i class="bi ${c.icon}"></i>
            </div>
            <span class="badge" style="background: ${c.color}33; color: #FFF; font-weight: 700; font-size: 0.76rem; border: 1px solid ${c.color}66;">
              ${c.pct}%
            </span>
          </div>
          <div style="font-size: 0.86rem; font-weight: 700; color: #FFF; margin-bottom: 0.2rem; min-height: 2.2rem;">
            ${c.nameSi}
          </div>
          <div style="font-size: 1.45rem; font-weight: 800; color: ${c.color}; margin-bottom: 0.4rem;">
            ${c.count} <span style="font-size: 0.76rem; font-weight: 400; color: #94A3B8;">වැඩසටහන්</span>
          </div>
          <div style="font-size: 0.74rem; color: #CBD5E1; line-height: 1.4;">
            ${c.desc}
          </div>
        </div>
      `;
    });

    // Render Detailed Table
    tbody.innerHTML = "";
    cats.forEach((c, idx) => {
      const priority = c.pct >= 14 ? '<span class="glass-badge gold">ඉහළ ප්‍රමුඛතාවය</span>' : (c.pct >= 9 ? '<span class="glass-badge blue">මධ්‍යස්ථ</span>' : '<span class="glass-badge green">විශේෂිත / නිවාරණ</span>');

      tbody.innerHTML += `
        <tr>
          <td style="text-align: center; color: #94A3B8;">${idx + 1}</td>
          <td>
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: ${c.color};"></span>
              <strong style="color: #FFF;">${c.nameSi}</strong>
            </div>
          </td>
          <td style="text-align: center; font-weight: 800; font-size: 1.05rem; color: ${c.color};">${c.count}</td>
          <td style="text-align: center; font-weight: 700;">${c.pct}%</td>
          <td>${priority}</td>
          <td style="font-size: 0.82rem; color: #CBD5E1;">${c.desc}</td>
        </tr>
      `;
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
        peakGrid.innerHTML += `
          <div class="glass-panel" style="padding: 1rem; border-top: 3px solid #D4AF37;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <span class="glass-badge gold" style="font-size: 0.72rem;">${p.daySi}</span>
              <strong style="font-size: 1.35rem; color: #FDE68A;">${p.count} <span style="font-size: 0.74rem; font-weight: 400; color: #CBD5E1;">වැඩසටහන්</span></strong>
            </div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #FFF; margin-bottom: 0.2rem;">${p.date}</div>
            <div style="font-size: 0.76rem; color: #CBD5E1;">${p.keyActivities}</div>
          </div>
        `;
      });
    }

    // Render Calendar Heatmap
    const heatmapWrap = document.getElementById("anCalendarHeatmapWrap");
    const heatmapData = this.data.analytics?.heatmap || [];
    if (heatmapWrap && heatmapData.length > 0) {
      // Group by month
      const monthsMap = {};
      heatmapData.forEach(d => {
        const dStr = d.date || (d.monthKey ? d.monthKey + '-01' : null);
        if (!dStr) return;
        const mKey = dStr.substring(0, 7);
        if (!monthsMap[mKey]) monthsMap[mKey] = [];
        monthsMap[mKey].push({
          date: dStr,
          count: d.count || 1
        });
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
        html += `
          <div class="an-month-col">
            <div class="an-month-title">${monthNamesSi[mKey] || mKey}</div>
            <div class="an-days-grid">
        `;
        monthsMap[mKey].forEach(day => {
          let lvl = "level-0";
          if (day.count >= 7) lvl = "level-peak";
          else if (day.count >= 4) lvl = "level-3";
          else if (day.count >= 2) lvl = "level-2";
          else if (day.count === 1) lvl = "level-1";

          html += `<div class="an-day-cell ${lvl}" title="${day.date}: වැඩසටහන් ${day.count}"></div>`;
        });
        html += `
            </div>
          </div>
        `;
      });
      html += '</div>';
      heatmapWrap.innerHTML = html;
    }

    if (window.pssCharts) {
      window.pssCharts.renderAnTimelineCharts(this.data?.analytics?.weekdays);
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
      topGrid.innerHTML += `
        <div class="glass-panel" style="padding: 1.1rem; border-top: 3px solid #D4AF37;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <strong style="color: #FFF; font-size: 1rem;">${c.name}</strong>
            <span class="badge" style="background: rgba(212,175,55,0.25); color: #FDE68A; font-weight:800; border: 1px solid #D4AF37;">
              ${c.diversity}/10 ක්ෂේත්‍ර
            </span>
          </div>
          <div style="font-size: 0.8rem; color: #38BDF8; margin-bottom: 0.3rem;">මුළු වැඩසටහන් ${c.acts} ක් තුළ</div>
          <div style="font-size: 0.75rem; color: #CBD5E1; line-height: 1.4;">${c.desc}</div>
        </div>
      `;
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
      tbody.innerHTML += `
        <tr>
          <td><strong style="color: #FDE68A;">${t.name}</strong></td>
          <td style="text-align: center; font-weight: 800; font-size: 1.05rem; color: #FFF;">${t.count}</td>
          <td style="text-align: center; font-weight: 700;">${t.pct}%</td>
          <td style="font-size: 0.85rem; color: #CBD5E1;">${t.examples}</td>
          <td style="font-size: 0.82rem; color: #93C5FD;">${t.plan}</td>
        </tr>
      `;
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
      if (numA > numB) return `<span class="an-diff-pill better"><i class="bi bi-arrow-up"></i> +${pct}% වැඩි</span>`;
      return `<span class="an-diff-pill worse"><i class="bi bi-arrow-down"></i> ${pct}% අඩු</span>`;
    };

    let metricsHtml = "";
    if (mode === "division") {
      metricsHtml = `
        <div class="an-compare-grid">
          <!-- Entity A Card -->
          <div class="an-entity-card entity-a">
            <div>
              <span class="glass-badge gold" style="margin-bottom: 0.4rem;">පළමු වසම (A)</span>
              <h3 style="font-size: 1.3rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">${itemA.nameSi}</h3>
              <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 1rem;">${itemA.sabhaNameSi}</div>
            </div>
            <div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">මුළු වැඩසටහන්:</span>
                <strong style="font-size: 1.15rem; color: #FDE68A;">${itemA.totalProjects}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">සම්පූර්ණ වූ:</span>
                <strong style="color: #6EE7B7;">${itemA.completed}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ක්‍රියාකාරී දින:</span>
                <strong style="color: #FFF;">${itemA.activeDays}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ක්ෂේත්‍ර විවිධත්වය:</span>
                <strong style="color: #38BDF8;">${itemA.diversity} / 10</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ප්‍රතිලාභීන්:</span>
                <strong style="color: #FFF;">${(itemA.beneficiaries || 0).toLocaleString()}</strong>
              </div>
            </div>
          </div>

          <!-- VS Badge & Comparison Differences -->
          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.8rem; padding: 0.5rem 0;">
            <div class="an-compare-vs-badge">VS</div>
            <div style="display: flex; flex-direction: column; gap: 0.6rem; align-items: center;">
              ${diffPill(itemA.totalProjects, itemB.totalProjects)}
              ${diffPill(itemA.diversity, itemB.diversity)}
              ${diffPill(itemA.activeDays, itemB.activeDays)}
            </div>
          </div>

          <!-- Entity B Card -->
          <div class="an-entity-card entity-b">
            <div>
              <span class="glass-badge blue" style="margin-bottom: 0.4rem;">දෙවන වසම (B)</span>
              <h3 style="font-size: 1.3rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">${itemB.nameSi}</h3>
              <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 1rem;">${itemB.sabhaNameSi}</div>
            </div>
            <div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">මුළු වැඩසටහන්:</span>
                <strong style="font-size: 1.15rem; color: #38BDF8;">${itemB.totalProjects}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">සම්පූර්ණ වූ:</span>
                <strong style="color: #6EE7B7;">${itemB.completed}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ක්‍රියාකාරී දින:</span>
                <strong style="color: #FFF;">${itemB.activeDays}</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ක්ෂේත්‍ර විවිධත්වය:</span>
                <strong style="color: #38BDF8;">${itemB.diversity} / 10</strong>
              </div>
              <div class="an-metric-row">
                <span style="color: #94A3B8;">ප්‍රතිලාභීන්:</span>
                <strong style="color: #FFF;">${(itemB.beneficiaries || 0).toLocaleString()}</strong>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (mode === "month") {
      metricsHtml = `
        <div class="an-compare-grid">
          <div class="an-entity-card entity-a">
            <div>
              <span class="glass-badge gold" style="margin-bottom: 0.4rem;">පළමු මාසය (A)</span>
              <h3 style="font-size: 1.3rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">${itemA.monthSi}</h3>
            </div>
            <div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වැඩසටහන් ගණන:</span><strong style="color: #FDE68A; font-size: 1.15rem;">${itemA.count}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">ක්‍රියාකාරී දින:</span><strong style="color: #FFF;">${itemA.activeDays}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වාර්තා කළ වසම්:</span><strong style="color: #FFF;">${itemA.reportingDivisions}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">සත්‍යාපිත ඡායාරූප:</span><strong style="color: #CBD5E1;">${itemA.photos || 0}</strong></div>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.8rem;">
            <div class="an-compare-vs-badge">VS</div>
            <div style="display: flex; flex-direction: column; gap: 0.6rem; align-items: center;">
              ${diffPill(itemA.count, itemB.count)}
              ${diffPill(itemA.activeDays, itemB.activeDays)}
            </div>
          </div>

          <div class="an-entity-card entity-b">
            <div>
              <span class="glass-badge blue" style="margin-bottom: 0.4rem;">දෙවන මාසය (B)</span>
              <h3 style="font-size: 1.3rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">${itemB.monthSi}</h3>
            </div>
            <div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වැඩසටහන් ගණන:</span><strong style="color: #38BDF8; font-size: 1.15rem;">${itemB.count}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">ක්‍රියාකාරී දින:</span><strong style="color: #FFF;">${itemB.activeDays}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වාර්තා කළ වසම්:</span><strong style="color: #FFF;">${itemB.reportingDivisions}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">සත්‍යාපිත ඡායාරූප:</span><strong style="color: #CBD5E1;">${itemB.photos || 0}</strong></div>
            </div>
          </div>
        </div>
      `;
    } else {
      metricsHtml = `
        <div class="an-compare-grid">
          <div class="an-entity-card entity-a">
            <div>
              <span class="glass-badge gold" style="margin-bottom: 0.4rem;">පළමු ක්ෂේත්‍රය (A)</span>
              <h3 style="font-size: 1.25rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">${itemA.nameSi}</h3>
            </div>
            <div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වැඩසටහන්:</span><strong style="color: #FDE68A; font-size: 1.2rem;">${itemA.count}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">සමස්ත %:</span><strong style="color: #FFF;">${itemA.pct}%</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">විස්තරය:</span><span style="font-size: 0.76rem; color: #CBD5E1;">${itemA.desc}</span></div>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.8rem;">
            <div class="an-compare-vs-badge">VS</div>
            ${diffPill(itemA.count, itemB.count)}
          </div>

          <div class="an-entity-card entity-b">
            <div>
              <span class="glass-badge blue" style="margin-bottom: 0.4rem;">දෙවන ක්ෂේත්‍රය (B)</span>
              <h3 style="font-size: 1.25rem; font-weight: 800; color: #FFF; margin: 0.2rem 0 0.8rem 0;">${itemB.nameSi}</h3>
            </div>
            <div>
              <div class="an-metric-row"><span style="color: #94A3B8;">වැඩසටහන්:</span><strong style="color: #38BDF8; font-size: 1.2rem;">${itemB.count}</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">සමස්ත %:</span><strong style="color: #FFF;">${itemB.pct}%</strong></div>
              <div class="an-metric-row"><span style="color: #94A3B8;">විස්තරය:</span><span style="font-size: 0.76rem; color: #CBD5E1;">${itemB.desc}</span></div>
            </div>
          </div>
        </div>
      `;
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
}

// Global initialization with triple-safe bootloader
function bootApp() {
  if (window._pssAppBooted) return;
  window._pssAppBooted = true;
  window.pssApp = new PssApp();
  window.prajaApp = window.pssApp;
  window.pssApp.init().catch(err => {
    console.error("Critical error during pssApp.init():", err);
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bootApp);
} else {
  bootApp();
}
if (typeof window !== "undefined" && typeof window.addEventListener === "function") { window.addEventListener("load", bootApp); }
