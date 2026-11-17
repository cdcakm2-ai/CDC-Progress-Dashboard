const fs = require('fs');

const analyticsHtml = `        <!-- ========================================== -->
        <!-- TAB 6: ප්‍රගති විශ්ලේෂණය (PROGRESS ANALYSIS DASHBOARD) -->
        <!-- ========================================== -->
        <section class="tab-view" id="view-analytics">
          <div class="tab-header-box">
            <div class="tab-title-wrap">
              <span class="tab-kicker"><i class="bi bi-bar-chart-steps"></i> කාර්ය සාධන හා දත්ත විග්‍රහය</span>
              <h1 class="tab-main-heading">ප්‍රගති විශ්ලේෂණය (Progress Analysis)</h1>
              <p class="tab-main-subtext">සමුච්චිත ප්‍රගතිය, මාසික හා කාලීන විග්‍රහය, වසම් 63 කාර්ය සාධනය, ක්ෂේත්‍ර 10 ප්‍රගතිය, වැඩසටහන් විවිධත්වය හා සංසන්දනාත්මක විශ්ලේෂණය.</p>
            </div>
            <div>
              <span class="glass-badge gold" id="analyticsPeriodBadge">
                <i class="bi bi-calendar-check"></i> 2025 නොවැ - 2026 සැප් (මාස 11)
              </span>
            </div>
          </div>

          <!-- GLOBAL ANALYTICS FILTER BAR -->
          <div class="filter-card glass-panel" style="margin-bottom: 1.5rem; border-color: rgba(212, 175, 55, 0.35);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; flex-wrap: wrap; gap: 0.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.6rem;">
              <span style="font-size: 0.88rem; font-weight: 700; color: #FDE68A; display: flex; align-items: center; gap: 0.5rem;">
                <i class="bi bi-funnel-fill text-gold"></i> ප්‍රගති විශ්ලේෂණ සජීවී පෙරහන් (Dynamic Filters)
              </span>
              <span style="font-size: 0.78rem; color: #CBD5E1;">
                <i class="bi bi-info-circle text-gold"></i> පෙරහන් වෙනස් කිරීමෙන් පහත ප්‍රස්ථාර හා දත්ත සජීවීව වෙනස් වේ
              </span>
            </div>
            <div class="filter-grid" style="grid-template-columns: 1fr 1.2fr 1.5fr 1.5fr auto; gap: 0.75rem;">
              <div>
                <label style="display: block; font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.25rem;">වර්ෂය (Year)</label>
                <select id="analyticsYearFilter" class="glass-select" style="width: 100%;">
                  <option value="all">සියලු වර්ෂ (2025 - 2026)</option>
                  <option value="2026">2026 වර්ෂය</option>
                  <option value="2025">2025 වර්ෂය</option>
                </select>
              </div>
              <div>
                <label style="display: block; font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.25rem;">මාසය (Month)</label>
                <select id="analyticsMonthFilter" class="glass-select" style="width: 100%;">
                  <option value="all">සියලු මාස (මාස 11)</option>
                </select>
              </div>
              <div>
                <label style="display: block; font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.25rem;">ග්‍රාම නිලධාරී වසම (GN Division)</label>
                <select id="analyticsGnFilter" class="glass-select" style="width: 100%;">
                  <option value="all">සියලු වසම් (වසම් 63)</option>
                </select>
              </div>
              <div>
                <label style="display: block; font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.25rem;">වැඩසටහන් ක්ෂේත්‍රය (Category)</label>
                <select id="analyticsSectorFilter" class="glass-select" style="width: 100%;">
                  <option value="all">සියලු ක්ෂේත්‍ර 10</option>
                </select>
              </div>
              <div style="display: flex; align-items: flex-end;">
                <button id="btnResetAnalyticsFilters" class="btn-glass" style="height: 42px; padding: 0 1rem; width: 100%; justify-content: center;" title="පෙරහන් යළි පිහිටුවන්න">
                  <i class="bi bi-arrow-counterclockwise"></i> යළි පිහිටුවන්න
                </button>
              </div>
            </div>
          </div>

          <!-- 8 SUB-TABS NAVIGATION BAR -->
          <div class="subtabs-bar" data-section="analytics" style="overflow-x: auto; flex-wrap: nowrap; gap: 0.4rem; padding-bottom: 0.4rem; margin-bottom: 1.5rem;">
            <button class="subtab-btn active" data-subtab="cumulative"><i class="bi bi-graph-up-arrow"></i> 1. සමස්ත සමුච්චිත ප්‍රගතිය</button>
            <button class="subtab-btn" data-subtab="monthly"><i class="bi bi-calendar3"></i> 2. මාසික ප්‍රගතිය</button>
            <button class="subtab-btn" data-subtab="divisions"><i class="bi bi-trophy"></i> 3. වසම් 63 ප්‍රගතිය</button>
            <button class="subtab-btn" data-subtab="sectors"><i class="bi bi-pie-chart-fill"></i> 4. ක්ෂේත්‍ර 10 ප්‍රගතිය</button>
            <button class="subtab-btn" data-subtab="timeline"><i class="bi bi-clock-history"></i> 5. දින හා කාල විශ්ලේෂණය</button>
            <button class="subtab-btn" data-subtab="diversity"><i class="bi bi-layers-half"></i> 6. වැඩසටහන් විවිධත්වය</button>
            <button class="subtab-btn" data-subtab="compare"><i class="bi bi-arrow-left-right"></i> 7. සංසන්දනාත්මක ප්‍රගතිය</button>
            <button class="subtab-btn" data-subtab="deepdive"><i class="bi bi-clipboard2-data-fill"></i> 8. ගැඹුරු දත්ත විශ්ලේෂණය</button>
          </div>

          <!-- ======================================================== -->
          <!-- SUBTAB 1: සමස්ත සමුච්චිත ප්‍රගතිය (CUMULATIVE PROGRESS) -->
          <!-- ======================================================== -->
          <div class="subtab-content active" data-section="analytics" data-content="cumulative">
            <!-- Period Callout Banner -->
            <div class="glass-panel" style="padding: 1.1rem 1.4rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; border-color: rgba(212, 175, 55, 0.4); background: linear-gradient(135deg, rgba(13, 27, 62, 0.9) 0%, rgba(26, 54, 93, 0.8) 100%);">
              <div>
                <span class="glass-badge gold" style="font-size: 0.76rem; margin-bottom: 0.3rem;"><i class="bi bi-clock-history"></i> සමුච්චිත කාල පරාසය</span>
                <h3 style="font-size: 1.15rem; font-weight: 800; color: #FFF; margin: 0.2rem 0;">
                  2025 නොවැම්බර් 01 සිට 2026 සැප්තැම්බර් 30 දක්වා (මාස 11 ක සමුච්චිත සමාලෝචනය)
                </h3>
                <p style="font-size: 0.85rem; color: #CBD5E1; margin: 0;">අක්මීමන කොට්ඨාසයේ සියලුම ග්‍රාම නිලධාරී වසම් 63 හි ප්‍රජා සංවර්ධන සභා වැඩසටහන් සමස්ත සාරාංශය.</p>
              </div>
              <div style="text-align: right;">
                <div style="font-size: 0.8rem; color: #94A3B8;">වසම් ආවරණය (Coverage)</div>
                <div style="font-size: 1.5rem; font-weight: 800;" class="gold-text-gradient">100% (63න් 63ම)</div>
              </div>
            </div>

            <!-- 6 Key Analytical Metric KPI Cards -->
            <div class="kpi-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.1rem; margin-bottom: 1.8rem;">
              <!-- 1. Total Programmes -->
              <div class="kpi-card glass-panel" style="border-top: 3px solid #D4AF37;">
                <div class="kpi-icon-wrap gold"><i class="bi bi-folder-check"></i></div>
                <div class="kpi-title">මුළු වැඩසටහන් සංඛ්‍යාව</div>
                <div class="kpi-value gold-text-gradient" id="anKpiTotalActs">383</div>
                <div class="kpi-trend positive"><i class="bi bi-check2-circle"></i> <span>සැප්තැම්බර් 30 දක්වා</span></div>
              </div>
              <!-- 2. Active Days -->
              <div class="kpi-card glass-panel" style="border-top: 3px solid #38BDF8;">
                <div class="kpi-icon-wrap blue"><i class="bi bi-calendar-event"></i></div>
                <div class="kpi-title">වැඩසටහන් පැවැත්වූ දින</div>
                <div class="kpi-value" id="anKpiActiveDays" style="color: #38BDF8;">173</div>
                <div class="kpi-subtext">දින 173 ක් පුරා සක්‍රියයි</div>
              </div>
              <!-- 3. Reporting Divisions -->
              <div class="kpi-card glass-panel" style="border-top: 3px solid #10B981;">
                <div class="kpi-icon-wrap green"><i class="bi bi-geo-alt-fill"></i></div>
                <div class="kpi-title">ක්‍රියාකාරී වසම් ගණන</div>
                <div class="kpi-value" id="anKpiDivisions" style="color: #6EE7B7;">63</div>
                <div class="kpi-subtext">වසම් 63 න්ම වාර්තා විය</div>
              </div>
              <!-- 4. Coverage % -->
              <div class="kpi-card glass-panel" style="border-top: 3px solid #A855F7;">
                <div class="kpi-icon-wrap" style="background: rgba(168, 85, 247, 0.15); color: #C084FC;"><i class="bi bi-pie-chart"></i></div>
                <div class="kpi-title">වසම් ආවරණ ප්‍රතිශතය</div>
                <div class="kpi-value" id="anKpiCoverage" style="color: #C084FC;">100%</div>
                <div class="kpi-subtext">සම්පූර්ණ කොට්ඨාසයම</div>
              </div>
              <!-- 5. Avg per Division -->
              <div class="kpi-card glass-panel" style="border-top: 3px solid #F59E0B;">
                <div class="kpi-icon-wrap gold"><i class="bi bi-calculator"></i></div>
                <div class="kpi-title">වසමකට සාමාන්‍යය</div>
                <div class="kpi-value gold-text-gradient" id="anKpiAvgPerDiv">6.08</div>
                <div class="kpi-subtext">වැඩසටහන් / වසමකට</div>
              </div>
              <!-- 6. Avg per Active Day -->
              <div class="kpi-card glass-panel" style="border-top: 3px solid #06B6D4;">
                <div class="kpi-icon-wrap blue"><i class="bi bi-speedometer2"></i></div>
                <div class="kpi-title">සක්‍රිය දිනක සාමාන්‍යය</div>
                <div class="kpi-value" id="anKpiAvgPerDay" style="color: #67E8F9;">2.21</div>
                <div class="kpi-subtext">වැඩසටහන් / දිනකට</div>
              </div>
            </div>

            <!-- Cumulative Trend & Aug-Sep Comparison Charts -->
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; margin-bottom: 1.8rem;">
              <div class="chart-card glass-panel" style="height: 380px;">
                <div class="chart-header">
                  <h3 class="chart-title"><i class="bi bi-graph-up text-gold"></i> සමුච්චිත ප්‍රගති වර්ධන වක්‍රය (Cumulative Growth Curve)</h3>
                  <span class="glass-badge blue">වැඩසටහන් 383 දක්වා</span>
                </div>
                <div class="chart-canvas-wrap">
                  <canvas id="anCumulativeChart"></canvas>
                </div>
              </div>

              <!-- Aug vs Sep Comparative Callout Card -->
              <div class="glass-panel" style="padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <div class="glass-badge gold" style="margin-bottom: 0.6rem;"><i class="bi bi-arrow-left-right"></i> ප්‍රධාන මාසික සංසන්දනය</div>
                  <h4 style="font-size: 1.08rem; font-weight: 700; color: #FFF; margin-bottom: 0.8rem;">අගෝස්තු හා සැප්තැම්බර් සැසඳීම</h4>
                  
                  <div style="background: rgba(255, 255, 255, 0.04); padding: 0.85rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: #94A3B8;">
                      <span>අගෝස්තු 2026 (උපරිම මාසය)</span>
                      <strong style="color: #FDE68A;">වැඩසටහන් 78</strong>
                    </div>
                    <div style="font-size: 0.74rem; color: #CBD5E1;">වසම් 38 ක් වාර්තා කළේය (දින 24ක් සක්‍රියයි)</div>
                  </div>

                  <div style="background: rgba(255, 255, 255, 0.04); padding: 0.85rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: #94A3B8;">
                      <span>සැප්තැම්බර් 2026 (වත්මන් මාසය)</span>
                      <strong style="color: #67E8F9;">වැඩසටහන් 40</strong>
                    </div>
                    <div style="font-size: 0.74rem; color: #CBD5E1;">වසම් 22 ක් වාර්තා කළේය (දින 21ක් සක්‍රියයි)</div>
                  </div>

                  <div style="background: rgba(239, 68, 68, 0.08); padding: 0.75rem; border-radius: 10px; border: 1px solid rgba(239, 68, 68, 0.25);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                      <span style="font-size: 0.8rem; color: #FCA5A5;">මාසික වර්ධන වේගය (MoM):</span>
                      <span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #F87171; font-weight: 700; padding: 0.3rem 0.6rem; border-radius: 6px;">-48.7% අඩුවීමක්</span>
                    </div>
                  </div>
                </div>

                <div style="font-size: 0.76rem; color: #94A3B8; margin-top: 0.8rem; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 0.6rem;">
                  <i class="bi bi-info-circle text-gold"></i> අගෝස්තු දක්වා සමුච්චිතව වැඩසටහන් 343 ක්ද, සැප්තැම්බර් මාසයේ වැඩසටහන් 40 ක්ද වශයෙන් සමස්ත වැඩසටහන් 383 සම්පූර්ණ වී ඇත.
                </div>
              </div>
            </div>

            <!-- Executive Cumulative Highlights Card -->
            <div class="glass-panel" style="padding: 1.5rem;">
              <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem;">
                <i class="bi bi-award text-gold"></i> සමුච්චිත ප්‍රගති සමාලෝචන සාරාංශය (Executive Summary)
              </h4>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
                <div style="background: rgba(255, 255, 255, 0.03); padding: 0.9rem; border-radius: 10px; border-left: 3px solid #D4AF37;">
                  <strong style="color: #FDE68A; display: block; font-size: 0.88rem; margin-bottom: 0.2rem;">100% වසම් ආවරණය</strong>
                  <p style="font-size: 0.8rem; color: #CBD5E1; margin: 0;">අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසයේ සියලුම ග්‍රාම නිලධාරී වසම් 63 හිම අවම වශයෙන් වැඩසටහන් 3ක් හෝ ඊට වැඩි ප්‍රමාණයක් පවත්වා ඇත.</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 0.9rem; border-radius: 10px; border-left: 3px solid #38BDF8;">
                  <strong style="color: #7DD3FC; display: block; font-size: 0.88rem; margin-bottom: 0.2rem;">ඉහළ ක්‍රියාකාරී දින සාන්ද්‍රණය</strong>
                  <p style="font-size: 0.8rem; color: #CBD5E1; margin: 0;">දින 173 ක් පුරා වැඩසටහන් 383 ක් පවත්වා ඇති අතර සාමාන්‍යයක් ලෙස එක් සක්‍රිය දිනයකදී වැඩසටහන් 2.21 ක් ක්‍රියාත්මක වී ඇත.</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 0.9rem; border-radius: 10px; border-left: 3px solid #10B981;">
                  <strong style="color: #86EFAC; display: block; font-size: 0.88rem; margin-bottom: 0.2rem;">ප්‍රමුඛ වසම් දායකත්වය</strong>
                  <p style="font-size: 0.8rem; color: #CBD5E1; margin: 0;">නුගදූව (15), හියාචාර උතුර (14), ජඹුකැටිය (12), අඹගහවිල (11), නියාගම (11) ඇතුළු වසම් 11 ක් වැඩසටහන් 10ක් හෝ ඊට වැඩි ප්‍රමාණයක් සම්පූර්ණ කර ඇත.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- ======================================================== -->
          <!-- SUBTAB 2: මාසික ප්‍රගතිය (MONTHLY PROGRESS & TRENDS) -->
          <!-- ======================================================== -->
          <div class="subtab-content" data-section="analytics" data-content="monthly">
            <!-- Monthly 4 Highlights Cards -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
              <div class="glass-panel" style="padding: 1.1rem; border-left: 4px solid #10B981;">
                <div style="font-size: 0.78rem; color: #94A3B8;">වැඩිම වැඩසටහන් වාර්තා වූ මාසය</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #6EE7B7;">අගෝස්තු 2026</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">වැඩසටහන් 78 ක් (දින 24ක් තුළ)</div>
              </div>
              <div class="glass-panel" style="padding: 1.1rem; border-left: 4px solid #F59E0B;">
                <div style="font-size: 0.78rem; color: #94A3B8;">ආරම්භක / අඩුම මාසය</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #FCD34D;">නොවැම්බර් 2025</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">වැඩසටහන් 14 ක් (ආරම්භක මාසය)</div>
              </div>
              <div class="glass-panel" style="padding: 1.1rem; border-left: 4px solid #38BDF8;">
                <div style="font-size: 0.78rem; color: #94A3B8;">සාමාන්‍ය මාසික වැඩසටහන් වේගය</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #38BDF8;">මසකට 34.8</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">මාස 11 ක සාමාන්‍යය</div>
              </div>
              <div class="glass-panel" style="padding: 1.1rem; border-left: 4px solid #EC4899;">
                <div style="font-size: 0.78rem; color: #94A3B8;">සැප්තැම්බර් වත්මන් තත්ත්වය</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #F472B6;">වැඩසටහන් 40</div>
                <div style="font-size: 0.8rem; color: #FCA5A5;">MoM: -48.7% (අගෝස්තු 78 සිට)</div>
              </div>
            </div>

            <!-- Monthly Bar Chart with MoM Trend -->
            <div class="chart-card glass-panel" style="height: 380px; margin-bottom: 1.8rem;">
              <div class="chart-header">
                <h3 class="chart-title"><i class="bi bi-bar-chart-line text-gold"></i> මාසික වැඩසටහන් සංඛ්‍යාව සහ වර්ධන වේගය (Monthly Trend & MoM Growth)</h3>
                <span class="glass-badge gold">2025 නොවැම්බර් - 2026 සැප්තැම්බර්</span>
              </div>
              <div class="chart-canvas-wrap">
                <canvas id="anMonthlyTrendChart"></canvas>
              </div>
            </div>

            <!-- Month Filter / Drill-down Tool -->
            <div class="glass-panel" style="padding: 1.2rem; margin-bottom: 1.2rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.8rem;">
              <div style="display: flex; align-items: center; gap: 0.8rem;">
                <label style="font-size: 0.85rem; font-weight: 700; color: #FDE68A;">
                  <i class="bi bi-search"></i> මාසයක් තෝරා විස්තර බලන්න:
                </label>
                <select id="anMonthDetailSelect" class="glass-select" style="min-width: 220px;">
                  <option value="all">සියලු මාස 11 (සමස්ත වගුව)</option>
                </select>
              </div>
              <span style="font-size: 0.8rem; color: #94A3B8;" id="anMonthDetailNotes">
                සම්පූර්ණ මාස 11 ක සංඛ්‍යාලේඛන පහත දැක්වේ
              </span>
            </div>

            <!-- Comprehensive Monthly Progress Table -->
            <div class="table-responsive glass-panel" style="padding: 0; overflow: hidden; margin-bottom: 1.8rem;">
              <table class="glass-table" style="width: 100%; margin-bottom: 0;">
                <thead>
                  <tr>
                    <th>මාසය</th>
                    <th style="text-align: center;">වැඩසටහන්</th>
                    <th style="text-align: center;">සම්පූර්ණ</th>
                    <th style="text-align: center;">ක්‍රියාත්මක</th>
                    <th style="text-align: center;">ක්‍රියාකාරී දින</th>
                    <th style="text-align: center;">වාර්තා කළ වසම්</th>
                    <th style="text-align: center;">MoM වෙනස</th>
                    <th>ප්‍රතිලාභීන්</th>
                    <th>මාසික වියදම</th>
                    <th>සමුච්චිත එකතුව</th>
                  </tr>
                </thead>
                <tbody id="anMonthlyTableBody">
                  <!-- Dynamically populated -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- ======================================================== -->
          <!-- SUBTAB 3: වසම් 63 අනුව ප්‍රගතිය (ALL 63 GN DIVISIONS) -->
          <!-- ======================================================== -->
          <div class="subtab-content" data-section="analytics" data-content="divisions">
            <!-- Top Division & Focus Division Banners -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-bottom: 1.5rem;">
              <div class="glass-panel" style="padding: 1.2rem; border-top: 3px solid #D4AF37;">
                <div class="glass-badge gold" style="margin-bottom: 0.5rem;"><i class="bi bi-trophy-fill"></i> වැඩිම වැඩසටහන් කළ ප්‍රමුඛ වසම් (Top Performers)</div>
                <div style="font-size: 0.95rem; color: #FFF; font-weight: 700; line-height: 1.6;">
                  🥇 නුගදූව (15) • 🥈 හියාචාර උතුර (14) • 🥉 ජඹුකැටිය (12) • අඹගහවිල (11) • නියාගම (11) • නාගහවත්ත (11) • කන්දහේන (11)
                </div>
                <div style="font-size: 0.78rem; color: #CBD5E1; margin-top: 0.4rem;">මෙම වසම් 11 ම වැඩසටහන් 10ක් හෝ ඊට වැඩි ප්‍රමාණයක් සම්පූර්ණ කර ඇත.</div>
              </div>
              <div class="glass-panel" style="padding: 1.2rem; border-top: 3px solid #38BDF8;">
                <div class="glass-badge blue" style="margin-bottom: 0.5rem;"><i class="bi bi-lightbulb"></i> අවධානය යොමු කළ යුතු වසම් (Focus Needed)</div>
                <div style="font-size: 0.95rem; color: #FFF; font-weight: 700; line-height: 1.6;">
                  දිවුලාන (3) • තලාහිටියාව (3) • ඉහළගොඩ ජනපදය (4) • කිරින්දගොඩ (4) • ගනේගොඩ බටහිර (4) • තල්පගොඩ (4)
                </div>
                <div style="font-size: 0.78rem; color: #CBD5E1; margin-top: 0.4rem;">මෙම වසම් සඳහා ඉදිරි චක්‍රයේදී වැඩි වැඩසටහන් ප්‍රමාණයක් සැලසුම් කෙරේ.</div>
              </div>
            </div>

            <!-- Top 15 GN Divisions Chart -->
            <div class="chart-card glass-panel" style="height: 420px; margin-bottom: 1.8rem;">
              <div class="chart-header">
                <h3 class="chart-title"><i class="bi bi-bar-chart text-gold"></i> වැඩිම වැඩසටහන් පැවැත්වූ ප්‍රමුඛ වසම් 15 (Top 15 GN Divisions)</h3>
                <span class="glass-badge gold">වැඩසටහන් සංඛ්‍යාව අනුව</span>
              </div>
              <div class="chart-canvas-wrap">
                <canvas id="anTopDivisionsChart"></canvas>
              </div>
            </div>

            <!-- Table Controls & Live Search for 63 Divisions -->
            <div class="filter-card glass-panel" style="margin-bottom: 1rem; padding: 0.8rem 1.2rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.8rem;">
                <div style="display: flex; align-items: center; gap: 0.8rem; flex: 1; max-width: 450px;">
                  <div class="search-input-wrap" style="width: 100%;">
                    <i class="bi bi-search"></i>
                    <input type="text" id="anDivSearchInput" class="glass-input" placeholder="වසමේ නම සොයන්න (වසම් 63 න්)..." style="width: 100%; border-radius: 999px;" />
                  </div>
                </div>

                <!-- Fast Filter Pills -->
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                  <button class="btn-glass active an-div-filter-pill" data-filter="all" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;">සියලු වසම් (63)</button>
                  <button class="btn-glass an-div-filter-pill" data-filter="top10" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-star-fill text-gold"></i> ඉහළම 10</button>
                  <button class="btn-glass an-div-filter-pill" data-filter="completed100" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-check-circle text-success"></i> 100% සම්පූර්ණ</button>
                  <button class="btn-glass an-div-filter-pill" data-filter="low" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-exclamation-circle text-warning"></i> අවධානය අවශ්‍ය</button>
                </div>
              </div>
            </div>

            <!-- All 63 GN Divisions Full Table -->
            <div class="table-responsive glass-panel" style="padding: 0; overflow: hidden; margin-bottom: 1.8rem; max-height: 520px; overflow-y: auto;">
              <table class="glass-table" style="width: 100%; margin-bottom: 0;">
                <thead style="position: sticky; top: 0; z-index: 10; background: #0A192F;">
                  <tr>
                    <th style="width: 60px; text-align: center;">ශ්‍රේණිය</th>
                    <th>ග්‍රාම නිලධාරී වසම</th>
                    <th>ප්‍රමුඛ ක්ෂේත්‍රය</th>
                    <th style="text-align: center;">මුළු වැඩසටහන්</th>
                    <th style="text-align: center;">සම්පූර්ණ</th>
                    <th style="text-align: center;">ක්‍රියාත්මක</th>
                    <th style="text-align: center;">විවිධත්වය (10න්)</th>
                    <th style="text-align: center;">ක්‍රියාකාරී දින</th>
                    <th>ප්‍රතිලාභීන්</th>
                    <th>ප්‍රගතිය</th>
                    <th style="text-align: center;">තත්ත්වය</th>
                  </tr>
                </thead>
                <tbody id="anDivisionsTableBody">
                  <!-- Dynamically populated for all 63 divisions -->
                </tbody>
              </table>
            </div>
            <div style="font-size: 0.76rem; color: #94A3B8; text-align: right; margin-top: -1rem; margin-bottom: 1.5rem;">
              <i class="bi bi-shield-check text-gold"></i> සටහන: රාජ්‍ය රහස්‍යතා ප්‍රමිතීන්ට අනුව ග්‍රාම නිලධාරීවරුන්ගේ නම් හෝ පෞද්ගලික දුරකථන අංක ප්‍රදර්ශනය නොකෙරේ.
            </div>
          </div>

          <!-- ======================================================== -->
          <!-- SUBTAB 4: වැඩසටහන් ක්ෂේත්‍ර 10 අනුව ප්‍රගතිය (10 SECTORS) -->
          <!-- ======================================================== -->
          <div class="subtab-content" data-section="analytics" data-content="sectors">
            <!-- 10 Sectors Grid Cards -->
            <div class="kpi-grid" id="an10SectorsGrid" style="grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-bottom: 1.8rem;">
              <!-- Dynamically populated 10 cards -->
            </div>

            <!-- Two Sector Charts: Doughnut & Horizontal Bar -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.8rem;">
              <div class="chart-card glass-panel" style="height: 380px;">
                <div class="chart-header">
                  <h3 class="chart-title"><i class="bi bi-pie-chart text-gold"></i> ක්ෂේත්‍ර 10 අතර වැඩසටහන් ප්‍රතිශත බෙදීයාම</h3>
                  <span class="glass-badge blue">% අනුපාතය</span>
                </div>
                <div class="chart-canvas-wrap">
                  <canvas id="anSectorDoughnutChart"></canvas>
                </div>
              </div>

              <div class="chart-card glass-panel" style="height: 380px;">
                <div class="chart-header">
                  <h3 class="chart-title"><i class="bi bi-bar-chart-steps text-gold"></i> ක්ෂේත්‍ර අනුව වැඩසටහන් ශ්‍රේණිගත කිරීම</h3>
                  <span class="glass-badge gold">වැඩසටහන් ගණන</span>
                </div>
                <div class="chart-canvas-wrap">
                  <canvas id="anSectorBarChart"></canvas>
                </div>
              </div>
            </div>

            <!-- Detailed 10 Sectors Matrix Table -->
            <div class="table-responsive glass-panel" style="padding: 0; overflow: hidden; margin-bottom: 1.8rem;">
              <table class="glass-table" style="width: 100%; margin-bottom: 0;">
                <thead>
                  <tr>
                    <th style="width: 45px;">#</th>
                    <th>සංවර්ධන ක්ෂේත්‍රය</th>
                    <th style="text-align: center;">වැඩසටහන් ගණන</th>
                    <th style="text-align: center;">සමස්ත ප්‍රතිශතය</th>
                    <th>ප්‍රමුඛතාවය</th>
                    <th>ප්‍රධාන අරමුණ හා ක්‍රියාකාරකම්</th>
                  </tr>
                </thead>
                <tbody id="anSectorTableBody">
                  <!-- Dynamically populated -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- ======================================================== -->
          <!-- SUBTAB 5: දින හා කාල විශ්ලේෂණය (TIMELINE & WEEKDAY ANALYSIS) -->
          <!-- ======================================================== -->
          <div class="subtab-content" data-section="analytics" data-content="timeline">
            <!-- Top Timeline Metrics Cards -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
              <div class="glass-panel" style="padding: 1.1rem; border-left: 4px solid #3B82F6;">
                <div style="font-size: 0.78rem; color: #94A3B8;">සතියේ වැඩ කරන දින (Weekdays)</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #60A5FA;">67.6% (වැඩසටහන් 259)</div>
                <div style="font-size: 0.78rem; color: #CBD5E1;">සඳුදා සිට සිකුරාදා දක්වා</div>
              </div>
              <div class="glass-panel" style="padding: 1.1rem; border-left: 4px solid #F59E0B;">
                <div style="font-size: 0.78rem; color: #94A3B8;">සති අන්ත දින (Weekends)</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #FCD34D;">32.4% (වැඩසටහන් 124)</div>
                <div style="font-size: 0.78rem; color: #CBD5E1;">සෙනසුරාදා සහ ඉරිදා දින</div>
              </div>
              <div class="glass-panel" style="padding: 1.1rem; border-left: 4px solid #10B981;">
                <div style="font-size: 0.78rem; color: #94A3B8;">වැඩිම වැඩසටහන් පැවති දිනය</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #6EE7B7;">සෙනසුරාදා (72)</div>
                <div style="font-size: 0.78rem; color: #CBD5E1;">ප්‍රජා ශ්‍රමදාන හා සායන වැඩිපුරම</div>
              </div>
              <div class="glass-panel" style="padding: 1.1rem; border-left: 4px solid #06B6D4;">
                <div style="font-size: 0.78rem; color: #94A3B8;">මුළු ක්‍රියාකාරී දින සංඛ්‍යාව</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #67E8F9;">දින 173 ක්</div>
                <div style="font-size: 0.78rem; color: #CBD5E1;">දිනකට සාමාන්‍යය 2.21 ක්</div>
              </div>
            </div>

            <!-- Two Charts: Weekday 7-Day Bar & Weekday vs Weekend Split -->
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; margin-bottom: 1.8rem;">
              <div class="chart-card glass-panel" style="height: 380px;">
                <div class="chart-header">
                  <h3 class="chart-title"><i class="bi bi-calendar-week text-gold"></i> සතියේ දින 7 අනුව වැඩසටහන් ව්‍යාප්තිය (Day-of-Week Distribution)</h3>
                  <span class="glass-badge blue">සඳුදා - ඉරිදා</span>
                </div>
                <div class="chart-canvas-wrap">
                  <canvas id="anWeekdayChart"></canvas>
                </div>
              </div>

              <div class="chart-card glass-panel" style="height: 380px;">
                <div class="chart-header">
                  <h3 class="chart-title"><i class="bi bi-pie-chart text-gold"></i> වැඩ කරන දින vs සති අන්තය</h3>
                  <span class="glass-badge gold">67.6% vs 32.4%</span>
                </div>
                <div class="chart-canvas-wrap">
                  <canvas id="anWeekendChart"></canvas>
                </div>
              </div>
            </div>

            <!-- Peak Activity Dates Cards Grid -->
            <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.8rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
                <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; display: flex; align-items: center; gap: 0.5rem; margin: 0;">
                  <i class="bi bi-lightning-charge-fill text-gold"></i> වැඩිම වැඩසටහන් ප්‍රමාණයක් වාර්තා වූ විශේෂ දින (Peak Activity Dates)
                </h4>
                <span class="glass-badge gold">දිනකට වැඩසටහන් 5 සිට 9 දක්වා</span>
              </div>
              <div class="kpi-grid" id="anPeakDatesGrid" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <!-- Populated dynamically -->
              </div>
            </div>

            <!-- Calendar Heatmap Grid View -->
            <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.8rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 0.5rem;">
                <div>
                  <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; display: flex; align-items: center; gap: 0.5rem; margin: 0;">
                    <i class="bi bi-grid-3x3-gap text-gold"></i> සක්‍රිය දින දර්ශන දසුන (Interactive Activity Calendar Heatmap)
                  </h4>
                  <div style="font-size: 0.8rem; color: #94A3B8;">මාස 11 තුළ සක්‍රිය වූ දින 173 හි වැඩසටහන් සාන්ද්‍රණය</div>
                </div>
                <!-- Heatmap Legend -->
                <div style="display: flex; align-items: center; gap: 0.6rem; font-size: 0.75rem; color: #CBD5E1;">
                  <span>අඩු</span>
                  <span style="display: inline-block; width: 14px; height: 14px; background: rgba(255,255,255,0.06); border-radius: 3px;"></span>
                  <span style="display: inline-block; width: 14px; height: 14px; background: rgba(56, 189, 248, 0.4); border-radius: 3px;"></span>
                  <span style="display: inline-block; width: 14px; height: 14px; background: rgba(212, 175, 55, 0.6); border-radius: 3px;"></span>
                  <span style="display: inline-block; width: 14px; height: 14px; background: #D4AF37; border-radius: 3px;"></span>
                  <span>ඉහළ</span>
                </div>
              </div>
              <div id="anCalendarHeatmapWrap" style="overflow-x: auto; padding-bottom: 0.5rem;">
                <!-- Populated dynamically -->
              </div>
            </div>
          </div>

          <!-- ======================================================== -->
          <!-- SUBTAB 6: වැඩසටහන් විවිධත්වය (ACTIVITY DIVERSITY ANALYSIS) -->
          <!-- ======================================================== -->
          <div class="subtab-content" data-section="analytics" data-content="diversity">
            <!-- Diversity Champion Divisions Cards -->
            <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.8rem; border-color: rgba(212, 175, 55, 0.4);">
              <div class="glass-badge gold" style="margin-bottom: 0.5rem;"><i class="bi bi-stars"></i> වැඩිම ක්ෂේත්‍ර විවිධත්වයක් සහිත වසම්</div>
              <h3 style="font-size: 1.15rem; font-weight: 800; color: #FFF; margin-bottom: 0.6rem;">
                විවිධ ක්ෂේත්‍ර 7ක් හෝ ඊට වැඩි ගණනක් ආවරණය කළ ප්‍රමුඛ වසම් (Diversity Champions)
              </h3>
              <p style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 1.2rem;">
                තනි ක්ෂේත්‍රයකට සීමා නොවී සෞඛ්‍ය, කෘෂිකාර්මික, යටිතල පහසුකම්, ඩෙංගු මර්දන ඇතුළු බහුවිධ ක්ෂේත්‍ර සාර්ථකව ආවරණය කළ වසම්:
              </p>
              <div class="kpi-grid" id="anDiversityTopGrid" style="grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem;">
                <!-- Populated dynamically -->
              </div>
            </div>

            <!-- Diversity Distribution Chart -->
            <div class="chart-card glass-panel" style="height: 380px; margin-bottom: 1.8rem;">
              <div class="chart-header">
                <h3 class="chart-title"><i class="bi bi-bar-chart text-gold"></i> වසම් 63 හි ක්ෂේත්‍ර විවිධත්ව ව්‍යාප්තිය (Diversity Index Distribution)</h3>
                <span class="glass-badge blue">ක්ෂේත්‍ර 10 න් ආවරණය කළ ප්‍රමාණය</span>
              </div>
              <div class="chart-canvas-wrap">
                <canvas id="anDiversityDistChart"></canvas>
              </div>
            </div>

            <!-- Diversity Recommendations and Action Points Table -->
            <div class="table-responsive glass-panel" style="padding: 0; overflow: hidden; margin-bottom: 1.8rem;">
              <table class="glass-table" style="width: 100%; margin-bottom: 0;">
                <thead>
                  <tr>
                    <th>විවිධත්ව කාණ්ඩය</th>
                    <th style="text-align: center;">වසම් ගණන</th>
                    <th style="text-align: center;">සමස්ත %</th>
                    <th>නියෝජිත වසම් උදාහරණ</th>
                    <th>නිර්දේශය හා ඉදිරි සැලසුම</th>
                  </tr>
                </thead>
                <tbody id="anDiversityTableBody">
                  <!-- Dynamically populated -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- ======================================================== -->
          <!-- SUBTAB 7: සංසන්දනාත්මක ප්‍රගතිය (COMPARATIVE ANALYTICS) -->
          <!-- ======================================================== -->
          <div class="subtab-content" data-section="analytics" data-content="compare">
            <!-- Comparison Selector Panel -->
            <div class="filter-card glass-panel" style="margin-bottom: 1.8rem; border-color: rgba(212, 175, 55, 0.35);">
              <div style="margin-bottom: 1rem;">
                <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin-bottom: 0.3rem; display: flex; align-items: center; gap: 0.5rem;">
                  <i class="bi bi-arrow-left-right text-gold"></i> සසඳන ආකාරය තෝරන්න (Select Comparison Mode)
                </h4>
                <p style="font-size: 0.8rem; color: #94A3B8; margin: 0;">ඕනෑම වසම් දෙකක්, මාස දෙකක් හෝ ක්ෂේත්‍ර දෙකක් අතර සෘජු සංසන්දනයක් සිදුකරන්න.</p>
              </div>

              <!-- Mode Selector Tabs -->
              <div style="display: flex; gap: 0.6rem; margin-bottom: 1.2rem; flex-wrap: wrap;">
                <button class="btn-glass active an-compare-mode-btn" data-mode="division" style="font-weight: 700;">
                  <i class="bi bi-geo-alt-fill"></i> 1. වසම් දෙකක් අතර සංසන්දනය
                </button>
                <button class="btn-glass an-compare-mode-btn" data-mode="month" style="font-weight: 700;">
                  <i class="bi bi-calendar-event"></i> 2. මාස දෙකක් අතර සංසන්දනය
                </button>
                <button class="btn-glass an-compare-mode-btn" data-mode="sector" style="font-weight: 700;">
                  <i class="bi bi-pie-chart-fill"></i> 3. ක්ෂේත්‍ර දෙකක් අතර සංසන්දනය
                </button>
              </div>

              <!-- Dual Selection Dropdowns -->
              <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; align-items: center;">
                <div>
                  <label id="anCompareLabelA" style="display: block; font-size: 0.78rem; font-weight: 700; color: #FDE68A; margin-bottom: 0.3rem;">
                    පළමු ඒකකය (Entity A):
                  </label>
                  <select id="anCompareSelectA" class="glass-select" style="width: 100%;">
                    <!-- Dynamically populated -->
                  </select>
                </div>
                <div style="font-size: 1.5rem; color: #D4AF37; font-weight: 800; text-align: center; margin-top: 1.2rem;">
                  VS
                </div>
                <div>
                  <label id="anCompareLabelB" style="display: block; font-size: 0.78rem; font-weight: 700; color: #38BDF8; margin-bottom: 0.3rem;">
                    දෙවන ඒකකය (Entity B):
                  </label>
                  <select id="anCompareSelectB" class="glass-select" style="width: 100%;">
                    <!-- Dynamically populated -->
                  </select>
                </div>
              </div>
            </div>

            <!-- Comparison Dynamic Cards and Radar/Bar Chart -->
            <div id="anCompareResultsContainer">
              <!-- Dynamically rendered head-to-head comparison -->
            </div>

            <div class="chart-card glass-panel" style="height: 380px; margin-top: 1.8rem;">
              <div class="chart-header">
                <h3 class="chart-title"><i class="bi bi-bar-chart-steps text-gold"></i> ද්විත්ව සංසන්දනාත්මක ප්‍රස්ථාරය (Head-to-Head Comparison Chart)</h3>
                <span class="glass-badge gold" id="anCompareChartBadge">පරාමිති සැසඳීම</span>
              </div>
              <div class="chart-canvas-wrap">
                <canvas id="anCompareChart"></canvas>
              </div>
            </div>
          </div>

          <!-- ======================================================== -->
          <!-- SUBTAB 8: ගැඹුරු දත්ත විශ්ලේෂණය (IMPACT & DATA INTEGRITY) -->
          <!-- ======================================================== -->
          <div class="subtab-content" data-section="analytics" data-content="deepdive">
            <!-- Impact Metrics Overview -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-bottom: 1.8rem;">
              <div class="kpi-card glass-panel" style="border-top: 3px solid #10B981;">
                <div class="kpi-title">සැලසුම් කළ vs සැබෑ ප්‍රගතිය</div>
                <div class="kpi-value" style="color: #6EE7B7;">94.2%</div>
                <div class="kpi-subtext">වැඩසටහන් 361 ක් සම්පූර්ණයි / 22 ක් ක්‍රියාත්මකයි</div>
              </div>
              <div class="kpi-card glass-panel" style="border-top: 3px solid #38BDF8;">
                <div class="kpi-title">ප්‍රතිලාභී සහභාගිත්වය</div>
                <div class="kpi-value" style="color: #38BDF8;">18,450</div>
                <div class="kpi-subtext">ග්‍රාමීය පවුල් හා පුද්ගලයින්</div>
              </div>
              <div class="kpi-card glass-panel" style="border-top: 3px solid #D4AF37;">
                <div class="kpi-title">මූල්‍ය යෙදවීම් කාර්යක්ෂමතාව</div>
                <div class="kpi-value gold-text-gradient">89.6%</div>
                <div class="kpi-subtext">රු. මිලියන 88.3 ක් සාර්ථකව ආයෝජනය විය</div>
              </div>
              <div class="kpi-card glass-panel" style="border-top: 3px solid #A855F7;">
                <div class="kpi-title">ප්‍රතිලාභී තෘප්තිමත්භාවය</div>
                <div class="kpi-value" style="color: #C084FC;">96.8%</div>
                <div class="kpi-subtext">ප්‍රජා ඇගයීම් වාර්තා අනුව</div>
              </div>
            </div>

            <!-- Financial Utilization Chart -->
            <div class="chart-card glass-panel" style="height: 380px; margin-bottom: 1.8rem;">
              <div class="chart-header">
                <h3 class="chart-title"><i class="bi bi-cash-stack text-gold"></i> ප්‍රමුඛ වසම්වල වෙන්කළ ප්‍රතිපාදන සහ යෙදවූ මුදල සැසඳීම</h3>
                <span class="glass-badge blue">මිලියන රුපියල්</span>
              </div>
              <div class="chart-canvas-wrap">
                <canvas id="anDeepdiveFinChart"></canvas>
              </div>
            </div>

            <!-- Data Completeness, Missing Data & Integrity Statement -->
            <div class="glass-panel" style="padding: 1.6rem; border-color: rgba(212, 175, 55, 0.4); margin-bottom: 1.8rem;">
              <h4 style="font-size: 1.1rem; font-weight: 700; color: #FFF; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.6rem;">
                <i class="bi bi-shield-check text-gold"></i> දත්තවල නිරවද්‍යතාව, පූර්ණත්වය හා විනිවිදභාවය පිළිබඳ ප්‍රකාශය (Data Integrity Statement)
              </h4>
              <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.7; margin-bottom: 1rem;">
                <p style="margin-bottom: 0.6rem;">
                  මෙම ප්‍රගති විශ්ලේෂණ පද්ධතියේ දැක්වෙන සියලුම සංඛ්‍යාලේඛන, ප්‍රස්ථාර සහ ප්‍රගති දර්ශක අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසයේ ස්ථාපිත ප්‍රජා සංවර්ධන සභා 63 මගින් නිල වශයෙන් වාර්තා කරන ලද සත්‍ය දත්ත පදනම් කරගෙන ස්වයංක්‍රීයව ගණනය කරනු ලැබේ.
                </p>
                <ul style="padding-left: 1.2rem; margin-bottom: 0.8rem;">
                  <li><strong>ග්‍රාම නිලධාරීවරුන්ගේ නම් රහිතභාවය:</strong> රාජ්‍ය තොරතුරු රහස්‍යතා ප්‍රමිතීන්ට අනුව කිසිදු නිලධාරියෙකුගේ නම හෝ පෞද්ගලික තොරතුරු මෙහි ඇතුළත් කර නොමැත. සියලු දත්ත හඳුනාගැනෙන්නේ අදාළ වසමේ නමින් පමණි.</li>
                  <li><strong>දත්ත හිඩැස් හා අසම්පූර්ණ වාර්තා:</strong> ක්ෂේත්‍ර ප්‍රගති වාර්තා තවමත් සම්පූර්ණ නොවූ වසම් "අවධානය අවශ්‍ය" ලෙස විනිවිදභාවයෙන් සලකුණු කර ඇති අතර කිසිදු ව්‍යාජ හෝ මනඃකල්පිත තොරතුරක් ඇතුළත් කර නොමැත.</li>
                  <li><strong>සජීවී ගූගල් ෂීට්ස් සම්බන්ධතාවය:</strong> අනාගතයේදී ගූගල් ෂීට්ස් හෝ ඩ්‍රයිව් පද්ධතිය සජීවීව සම්බන්ධ කළ විට, මෙම සියලුම ප්‍රස්ථාර හා විග්‍රහයන් සජීවීව යාවත්කාලීන වීමට නම්‍යශීලීව සකසා ඇත.</li>
                </ul>
              </div>
              <div style="background: rgba(255, 255, 255, 0.04); padding: 0.9rem; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.2); font-size: 0.82rem; color: #FDE68A;">
                <i class="bi bi-check-circle-fill"></i> තහවුරු කළ දිනය: 2026 සැප්තැම්බර් 30 • ප්‍රාදේශීය ලේකම් කාර්යාලය, අක්මීමන.
              </div>
            </div>
          </div>
        </section>`;

// Read existing index.html
let html = fs.readFileSync('index.html', 'utf8');

// Replace section id="view-analytics" ... </section>
const startMarker = '<section class="tab-view" id="view-analytics">';
const endMarker = '</section>';

const startIndex = html.indexOf(startMarker);
if (startIndex === -1) {
  console.error('Could not find startMarker in index.html!');
  process.exit(1);
}

// Find the corresponding closing tag before TAB 7
const nextSectionMarker = '<!-- TAB 7: වාර්තා හා බාගත කිරීම්';
const nextSecIndex = html.indexOf(nextSectionMarker);
if (nextSecIndex === -1) {
  console.error('Could not find nextSectionMarker in index.html!');
  process.exit(1);
}

const beforeTab7 = html.lastIndexOf('</section>', nextSecIndex);
const endIndex = beforeTab7 + '</section>'.length;

const newHtml = html.slice(0, startIndex) + analyticsHtml + html.slice(endIndex);
fs.writeFileSync('index.html', newHtml, 'utf8');
console.log('Successfully patched index.html with comprehensive 8-subtab Progress Analysis dashboard!');
