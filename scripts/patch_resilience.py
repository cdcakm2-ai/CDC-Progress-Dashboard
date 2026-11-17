# Patching js/charts.js and js/app.js to be 100% crash-proof

with open('js/charts.js', 'r', encoding='utf-8') as f:
    charts_code = f.read()

# 1. In js/charts.js, guard init(data)
old_charts_init = '''  init(data) {
    this.data = data || ((typeof window !== "undefined" && window.PSS_DATA) ? window.PSS_DATA : {});
    this.renderAll();
  }'''

new_charts_init = '''  init(data) {
    this.data = data || ((typeof window !== "undefined" && window.PSS_DATA) ? window.PSS_DATA : {});
    if (typeof Chart === "undefined") {
      console.warn("Chart.js library is not available yet. Charts will initialize when ready.");
      return;
    }
    try {
      this.renderAll();
    } catch (e) {
      console.warn("Chart rendering warning:", e);
    }
  }'''

assert old_charts_init in charts_code, "old_charts_init not found"
charts_code = charts_code.replace(old_charts_init, new_charts_init)

# In renderAll, wrap each chart call in try/catch
old_render_all = '''  renderAll() {
    this.renderMonthlyChart();
    this.renderCategoryChart();
    this.renderGNRankingChart();
    this.renderAllAnalyticsCharts();
  }'''

new_render_all = '''  renderAll() {
    if (typeof Chart === "undefined") return;
    try { this.renderMonthlyChart(); } catch (e) { console.warn("Monthly chart error:", e); }
    try { this.renderCategoryChart(); } catch (e) { console.warn("Category chart error:", e); }
    try { this.renderGNRankingChart(); } catch (e) { console.warn("GN ranking chart error:", e); }
    try { this.renderAllAnalyticsCharts(); } catch (e) { console.warn("Analytics charts error:", e); }
  }'''

assert old_render_all in charts_code, "old_render_all not found"
charts_code = charts_code.replace(old_render_all, new_render_all)

with open('js/charts.js', 'w', encoding='utf-8') as f:
    f.write(charts_code)
print("js/charts.js patched successfully!")

# 2. Patching js/app.js
with open('js/app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

# Fix 1: line 1222 null-safe querySelector
old_tr_btn = '''        tr.querySelector(".btn-view-division-act").addEventListener("click", () => {
          this.openDedicatedDivisionView(gn.nameSi);
        });'''
new_tr_btn = '''        const viewBtn = tr.querySelector(".btn-view-division-act");
        if (viewBtn) {
          viewBtn.addEventListener("click", () => {
            this.openDedicatedDivisionView(gn.nameSi);
          });
        }'''
assert old_tr_btn in app_code, "old_tr_btn not found"
app_code = app_code.replace(old_tr_btn, new_tr_btn)

# Fix 2: line 3978 matchMedia safe
old_mm = '''    if (window.matchMedia("(pointer: coarse)").matches) return;'''
new_mm = '''    if (typeof window !== "undefined" && typeof window.matchMedia === "function" && window.matchMedia("(pointer: coarse)").matches) return;'''
assert old_mm in app_code, "old_mm not found"
app_code = app_code.replace(old_mm, new_mm)

# Fix 3: Re-order init() to render HTML DOM first with try/catch, then charts
old_init_calls = '''    // Initialize Charts first so all rendering methods have access
    if (window.pssCharts) {
      window.pssCharts.init(this.data);
    }
    
    // Render all dashboard sections
    this.renderKPIs();
    this.renderOverviewTab();
    this.renderMonthlyTab();
    this.renderDivisionsTab();
    this.populateFilterDropdowns();
    this.renderCategoryPills();
    this.initActivitiesDivisionShowcase();
    this.renderActivitiesTab();
    this.initReportsSystem();
    this.initAnalyticsTab();
    this.renderStatusTab();
    this.init3DTilt();
    this.initAutoDriveSyncWatcher();'''

new_init_calls = '''    // Render all dashboard DOM sections first (Ensures data is ALWAYS visible even if charts fail)
    try { this.renderKPIs(); } catch (e) { console.error("renderKPIs error:", e); }
    try { this.renderOverviewTab(); } catch (e) { console.error("renderOverviewTab error:", e); }
    try { this.renderMonthlyTab(); } catch (e) { console.error("renderMonthlyTab error:", e); }
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

    // Initialize Charts safely after DOM is ready
    if (window.pssCharts) {
      try {
        window.pssCharts.init(this.data);
      } catch (e) {
        console.warn("Chart init deferred or failed gracefully:", e);
      }
    }'''

assert old_init_calls in app_code, "old_init_calls not found"
app_code = app_code.replace(old_init_calls, new_init_calls)

# Fix 4: Robust bootloader at bottom of js/app.js
old_boot = '''// Global initialization
document.addEventListener("DOMContentLoaded", () => {
  window.pssApp = new PssApp();
  window.prajaApp = window.pssApp;
  window.pssApp.init();
});'''

new_boot = '''// Global initialization with triple-safe bootloader
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
window.addEventListener("load", bootApp);'''

assert old_boot in app_code, "old_boot not found"
app_code = app_code.replace(old_boot, new_boot)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_code)
print("js/app.js patched successfully!")
