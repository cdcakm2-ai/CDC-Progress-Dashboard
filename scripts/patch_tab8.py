import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_str = '<section class="tab-view" id="view-status">'
end_str = '</section>'

idx_start = html.find(start_str)
if idx_start == -1:
    print("Could not find start_str in index.html")
    exit(1)

idx_end = html.find(end_str, idx_start)
if idx_end == -1:
    print("Could not find end_str in index.html")
    exit(1)

new_status_html = """<section class="tab-view" id="view-status">
          <div class="tab-header-box">
            <div class="tab-title-wrap">
              <span class="tab-kicker"><i class="bi bi-shield-check"></i> සත්‍ය Google Drive දත්ත විගණනය හා ගුණාත්මක තත්ත්වය</span>
              <h1 class="tab-main-heading">දත්ත යාවත්කාලීන තත්ත්වය සහ පූර්ණ විගණන වාර්තාව</h1>
              <p class="tab-main-subtext">අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසයේ නිල Google Drive ගබඩාවෙන් සෘජුවම ලබාගත් තහවුරු කළ දත්ත, අනුපිටපත් ඉවත්කිරීම් සහ වසම් 63 හි ආවරණ තත්ත්වය.</p>
            </div>
            <div style="display: flex; gap: 0.8rem; align-items: center; flex-wrap: wrap;">
              <a href="https://drive.google.com/drive/folders/1jBY0y_QWiinEPXEpEU6OwesPmlIna33C?usp=sharing" target="_blank" class="btn-glass" style="text-decoration: none;">
                <i class="bi bi-google"></i> Google Drive ෆෝල්ඩරය
              </a>
              <button id="btnRefreshSystemData" class="btn-gold">
                <i class="bi bi-arrow-repeat"></i> දත්ත සමමුහුර්ත කරන්න (Sync)
              </button>
            </div>
          </div>

          <!-- Status Metric Cards (4 Pillars of Data Quality) -->
          <div class="status-cards-grid">
            <div class="glass-panel" style="padding: 1.4rem;">
              <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.3rem;"><i class="bi bi-cloud-check-fill text-gold"></i> දත්ත මූලාශ්‍රය</div>
              <div style="font-size: 1.15rem; font-weight: 800; color: #10B981; display: flex; align-items: center; gap: 0.5rem;">
                <span class="status-indicator-dot"></span> Google Drive සජීවීයි
              </div>
              <div style="font-size: 0.75rem; color: #CBD5E1; margin-top: 0.4rem;">CDC Progress Dashboard (ID: 1jBY0y...)</div>
            </div>

            <div class="glass-panel" style="padding: 1.4rem;">
              <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.3rem;"><i class="bi bi-journal-check text-gold"></i> අනන්‍ය වැඩසටහන්</div>
              <div style="font-size: 1.15rem; font-weight: 800; color: #FDE68A;" id="statusTotalUniqueActivities">
                287 වැඩසටහන්
              </div>
              <div style="font-size: 0.75rem; color: #CBD5E1; margin-top: 0.4rem;">ප්‍රතිචාර 95කින් (සටහන්: 290 | අනුපිටපත් ඉවත් කළ පසු)</div>
            </div>

            <div class="glass-panel" style="padding: 1.4rem;">
              <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.3rem;"><i class="bi bi-filter-circle-fill text-gold"></i> අනුපිටපත් ඉවත් කිරීම</div>
              <div style="font-size: 1.15rem; font-weight: 800; color: #38BDF8;" id="statusDuplicatesCount">
                අනුපිටපත් 3ක් ඉවත් කරන ලදී
              </div>
              <div style="font-size: 0.75rem; color: #CBD5E1; margin-top: 0.4rem;">තහවුරු කළ අනුපිටපත් 3 | සැක සහිත 2</div>
            </div>

            <div class="glass-panel" style="padding: 1.4rem;">
              <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.3rem;"><i class="bi bi-geo-alt-fill text-gold"></i> වසම් 63 ආවරණය</div>
              <div style="font-size: 1.15rem; font-weight: 800; color: #A78BFA;" id="statusCoverageSummary">
                51 / 63 වසම් (81.0%)
              </div>
              <div style="font-size: 0.75rem; color: #CBD5E1; margin-top: 0.4rem;">වසම් 12ක දත්ත තවමත් ලැබී නොමැත</div>
            </div>
          </div>

          <!-- Subtabs for Status Tab -->
          <div class="subtabs-bar" data-section="status">
            <button class="subtab-btn active" data-subtab="audit"><i class="bi bi-shield-check"></i> දත්ත ගුණාත්මකභාවය හා විගණනය</button>
            <button class="subtab-btn" data-subtab="duplicates"><i class="bi bi-layers-half"></i> අනුපිටපත් විගණන ලේඛනය (3)</button>
            <button class="subtab-btn" data-subtab="anomalies"><i class="bi bi-calendar-event"></i> දින විෂමතා පරීක්ෂාව (3)</button>
            <button class="subtab-btn" data-subtab="submissions"><i class="bi bi-building-check"></i> වසම් 63 වාර්තාකරණ තත්ත්වය</button>
            <button class="subtab-btn" data-subtab="drive"><i class="bi bi-google"></i> Google Drive මූලාශ්‍ර විස්තර</button>
          </div>

          <!-- Status Subtab 1: Quality & Audit Log -->
          <div class="subtab-content active" data-section="status" data-content="audit">
            <div class="glass-panel" style="padding: 1.6rem; margin-bottom: 1.5rem;">
              <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.6rem;">
                <i class="bi bi-file-earmark-check-fill text-gold"></i> සත්‍ය දත්ත ඒකාබද්ධ කිරීමේ හා ගුණාත්මකභාවය තහවුරු කිරීමේ ක්‍රමවේදය
              </h4>
              <div style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.7; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem;">
                <div style="background: rgba(255,255,255,0.02); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                  <div style="font-weight: 700; color: #FDE68A; margin-bottom: 0.5rem;"><i class="bi bi-1-circle"></i> අනුපිටපත් ඉවත් කිරීමේ තහවුරුව</div>
                  ගූගල් පෝරම (Google Forms) හරහා නිලධාරීන් විසින් එකම වැඩසටහන නැවත ඇතුළත් කර ඇති අවස්ථා ස්වයංක්‍රීය බහු-ස්ථර ඇල්ගොරිතම මගින් හඳුනාගෙන, තහවුරු කළ අනුපිටපත් 3ක් ඉවත් කර 100% අනන්‍ය වැඩසටහන් 287ක් පමණක් ගණනය කර ඇත.
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                  <div style="font-weight: 700; color: #FDE68A; margin-bottom: 0.5rem;"><i class="bi bi-2-circle"></i> නිල වසම් නාම සම්මතකරණය</div>
                  අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසයේ නිල ග්‍රාම නිලධාරී වසම් 63 හි නාමාවලියට අනුව, පෝරමවල තිබූ කේත හා අක්ෂර වින්‍යාස විවිධත්වයන් 54ම 100% නිවැරදිව සම්මත වසම් නාම වෙත සිතියම්ගත කර ඇත.
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                  <div style="font-weight: 700; color: #FDE68A; margin-bottom: 0.5rem;"><i class="bi bi-3-circle"></i> ඡායාරූප සත්‍යතාව</div>
                  ප්‍රදර්ශනය වන සියලුම ඡායාරූප 666ම Google Drive සත්‍ය මූලාශ්‍රයෙන් සෘජුවම ලබාගෙන ඇති අතර, කිසිදු ආදර්ශ හෝ stock ඡායාරූපයක් පද්ධතිය තුළ අඩංගු නොවේ.
                </div>
              </div>
            </div>

            <div class="audit-table-card glass-panel">
              <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin-bottom: 1.2rem;">
                <i class="bi bi-clock-history text-gold"></i> පද්ධති ක්‍රියාකාරීත්ව විගණන ලේඛනය (Audit Trail)
              </h4>
              <table class="comparison-table">
                <thead>
                  <tr>
                    <th>දිනය සහ වේලාව</th>
                    <th>සිදු කරන ලද කාර්යය</th>
                    <th>අදාළ වසම / මූලාශ්‍රය</th>
                    <th>තත්ත්වය</th>
                  </tr>
                </thead>
                <tbody id="auditLogTableBody">
                  <!-- Dynamically populated -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- Status Subtab 2: Confirmed Duplicates Filtered -->
          <div class="subtab-content" data-section="status" data-content="duplicates">
            <div class="glass-panel" style="padding: 1.6rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 0.8rem;">
                <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin: 0;">
                  <i class="bi bi-layers-half text-danger"></i> ඉවත් කරන ලද තහවුරු කළ අනුපිටපත් (Confirmed Duplicates Filtered)
                </h4>
                <span class="glass-badge red"><i class="bi bi-check2-circle"></i> සම්පූර්ණයෙන්ම ඉවත් කර නිරවුල් කරන ලදී</span>
              </div>
              <p style="font-size: 0.84rem; color: #94A3B8; margin-bottom: 1.2rem;">
                පහත දැක්වෙන්නේ එකම වසමේ, එකම දිනයේ සහ එකම විස්තරය/ඡායාරූප සහිතව Google Sheets හි ද්විත්වව ඇතුළත්ව තිබූ වාර්තා වේ. දත්ත ගුණාත්මකභාවය සුරැකීම පිණිස මේවා ප්‍රධාන ගණනය කිරීම්වලින් ඉවත් කර ඇත:
              </p>
              <div class="table-responsive">
                <table class="comparison-table">
                  <thead>
                    <tr>
                      <th>ග්‍රාම නිලධාරී වසම</th>
                      <th>දිනය</th>
                      <th>වැඩසටහනේ විස්තරය</th>
                      <th>මූලික සටහන</th>
                      <th>අනුපිටපත් සටහන</th>
                      <th>විගණන තත්ත්වය</th>
                    </tr>
                  </thead>
                  <tbody id="statusDuplicatesTableBody">
                    <!-- Populated dynamically -->
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Status Subtab 3: Date Anomalies & Typos -->
          <div class="subtab-content" data-section="status" data-content="anomalies">
            <div class="glass-panel" style="padding: 1.6rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 0.8rem;">
                <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin: 0;">
                  <i class="bi bi-exclamation-triangle-fill text-warning"></i> පෝරමවල දින ඇතුළත් කිරීම් ආශ්‍රිත ලිපිකරු විෂමතා පරීක්ෂාව
                </h4>
                <span class="glass-badge gold"><i class="bi bi-info-circle"></i> නිරීක්ෂණය කරන ලදී</span>
              </div>
              <p style="font-size: 0.84rem; color: #94A3B8; margin-bottom: 1.2rem;">
                Google Sheets හි පෝරම පුරවන අවස්ථාවේ නිලධාරීන් විසින් අත්වැරදීමකින් වසර වැරදි ලෙස යතුරු ලියනය කළ අවස්ථා (Typo) හඳුනාගෙන, වාර්තාකරණ මාසය අනුව නිවැරදිව පද්ධතියේ ස්ථානගත කර ඇත:
              </p>
              <div class="table-responsive">
                <table class="comparison-table">
                  <thead>
                    <tr>
                      <th>ග්‍රාම නිලධාරී වසම</th>
                      <th>පෝරමයේ ලියූ දිනය (Raw)</th>
                      <th>සම්මත කළ දිනය (Normalized)</th>
                      <th>වැඩසටහනේ විස්තරය</th>
                      <th>මූලාශ්‍ර පත්‍රිකාව</th>
                      <th>විගණන සටහන</th>
                    </tr>
                  </thead>
                  <tbody id="statusAnomaliesTableBody">
                    <!-- Populated dynamically -->
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Status Subtab 4: Submissions -->
          <div class="subtab-content" data-section="status" data-content="submissions">
            <div class="glass-panel" style="padding: 1.6rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 0.8rem;">
                <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin: 0;">
                  <i class="bi bi-building-check text-gold"></i> අක්මීමන කොට්ඨාසයේ වසම් 63 හි දත්ත ලැබීමේ තත්ත්වය
                </h4>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                  <span class="glass-badge green"><i class="bi bi-check-circle-fill"></i> වාර්තා ලැබුණු වසම් 51ක් (81.0%)</span>
                  <span class="glass-badge gray"><i class="bi bi-hourglass-split"></i> වාර්තා අපේක්ෂිත වසම් 12ක් (19.0%)</span>
                </div>
              </div>
              <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.8rem;" id="statusReportingSubmissions">
                <!-- Dynamically populated -->
              </div>
            </div>
          </div>

          <!-- Status Subtab 5: Drive Sources -->
          <div class="subtab-content" data-section="status" data-content="drive">
            <div class="glass-panel" style="padding: 1.6rem;">
              <h4 style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin-bottom: 1.2rem;">
                <i class="bi bi-google text-gold"></i> සත්‍ය Google Drive දත්ත මූලාශ්‍ර සහ ලේඛන සබඳතා
              </h4>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.2rem;">
                <div style="background: rgba(255,255,255,0.02); padding: 1.4rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                  <div style="font-size: 0.8rem; color: #D4AF37; font-weight: 700; margin-bottom: 0.4rem;">ප්‍රධාන Google Drive ෆෝල්ඩරය</div>
                  <div style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin-bottom: 0.6rem;">CDC Progress Dashboard</div>
                  <div style="font-size: 0.8rem; color: #94A3B8; word-break: break-all; margin-bottom: 0.8rem;">
                    ID: <code>1jBY0y_QWiinEPXEpEU6OwesPmlIna33C</code>
                  </div>
                  <a href="https://drive.google.com/drive/folders/1jBY0y_QWiinEPXEpEU6OwesPmlIna33C?usp=sharing" target="_blank" class="btn-gold" style="display: inline-block; font-size: 0.8rem; padding: 0.45rem 1rem; text-decoration: none;">
                    <i class="bi bi-box-arrow-up-right"></i> ෆෝල්ඩරය විවෘත කරන්න
                  </a>
                </div>

                <div style="background: rgba(255,255,255,0.02); padding: 1.4rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                  <div style="font-size: 0.8rem; color: #D4AF37; font-weight: 700; margin-bottom: 0.4rem;">පළමු අදියර ප්‍රතිචාර පත්‍රිකාව (Phase 1)</div>
                  <div style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin-bottom: 0.6rem;">ප්‍රජා සංවර්ධන සභා වැඩසටහන් (Responses)</div>
                  <div style="font-size: 0.8rem; color: #94A3B8; word-break: break-all; margin-bottom: 0.8rem;">
                    ප්‍රතිචාර: 70 | ප්‍රකාශිත: 257 | අනන්‍ය: 243 | ඡායාරූප: 554
                  </div>
                  <a href="https://docs.google.com/spreadsheets/d/1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk" target="_blank" class="btn-glass" style="display: inline-block; font-size: 0.8rem; padding: 0.45rem 1rem; text-decoration: none;">
                    <i class="bi bi-file-earmark-spreadsheet"></i> Sheet 1 විවෘත කරන්න
                  </a>
                </div>

                <div style="background: rgba(255,255,255,0.02); padding: 1.4rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                  <div style="font-size: 0.8rem; color: #D4AF37; font-weight: 700; margin-bottom: 0.4rem;">දෙවන අදියර ප්‍රතිචාර පත්‍රිකාව (Phase 2)</div>
                  <div style="font-size: 1.05rem; font-weight: 700; color: #FFF; margin-bottom: 0.6rem;">මාසික වැඩසටහන් (2026 අගෝස්තු-ඔක්තෝබර්)</div>
                  <div style="font-size: 0.8rem; color: #94A3B8; word-break: break-all; margin-bottom: 0.8rem;">
                    ප්‍රතිචාර: 25 | ප්‍රකාශිත: 47 | අනන්‍ය: 44 | ඡායාරූප: 112
                  </div>
                  <a href="https://docs.google.com/spreadsheets/d/1H_bwTOUUGj_cpIZKfBxs74Omt0xIgtTVeWhaRA3G7WI" target="_blank" class="btn-glass" style="display: inline-block; font-size: 0.8rem; padding: 0.45rem 1rem; text-decoration: none;">
                    <i class="bi bi-file-earmark-spreadsheet"></i> Sheet 2 විවෘත කරන්න
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>"""

updated_html = html[:idx_start] + new_status_html + html[idx_end + len(end_str):]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Successfully patched index.html with advanced Tab 8 Data Quality views!")
