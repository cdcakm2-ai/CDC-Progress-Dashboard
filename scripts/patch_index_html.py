import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update version busters
html = re.sub(r'\?v=9\.0', '?v=10.0', html)

# 2. Update numbers in HTML
html = html.replace('440', '442')
html = html.replace('අනුපිටපත් 77ක්', 'අනුපිටපත් 75ක්')
html = html.replace('අනුපිටපත් (77)', 'අනුපිටපත් (75)')
html = html.replace('අනුපිටපත් 77', 'අනුපිටපත් 75')

# 3. Replace text-gold with text-primary-blue or appropriate color
html = html.replace('text-gold', 'text-blue')
html = html.replace('gold-text-gradient', 'blue-text-gradient')

# 4. Update Tab 4 GN Selection card
tab4_old = '''            <!-- GN Division Selection Ribbon & Search -->
            <div class="filter-card glass-panel" style="padding: 1.4rem; margin-bottom: 1.8rem; border: 1px solid rgba(212, 175, 55, 0.35);">
              <div style="font-size: 0.98rem; font-weight: 700; color: #FFF; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.6rem;">
                <span style="display: flex; align-items: center; gap: 0.5rem;">
                  <i class="bi bi-diagram-3-fill text-blue" style="font-size: 1.15rem;"></i> ග්‍රාම නිලධාරී වසම තෝරන්න (Drop-Down හෝ Slider මගින්):
                </span>
                <span class="glass-badge gold" style="font-size: 0.78rem;">
                  <i class="bi bi-check-circle-fill"></i> වසම් 63 ම සක්‍රීයයි
                </span>
              </div>

              <!-- Primary Drop-Down & Quick Search Selector -->
              <div style="display: grid; grid-template-columns: 1.8fr 1.2fr; gap: 1rem; align-items: center; margin-bottom: 1.2rem;">
                <div style="position: relative;">
                  <label for="activitiesGnSelectDropdown" style="display: block; font-size: 0.78rem; font-weight: 600; color: #CBD5E1; margin-bottom: 0.35rem;">
                    <i class="bi bi-chevron-down text-blue"></i> වසම් Drop-Down මෙනුව:
                  </label>
                  <select id="activitiesGnSelectDropdown" class="glass-select" style="width: 100%; font-size: 0.95rem; font-weight: 600; padding: 0.65rem 1.1rem; border: 1.5px solid rgba(212, 175, 55, 0.45); border-radius: 12px; background: rgba(15, 23, 42, 0.9); color: #FFF;">
                    <!-- Dynamically populated with all 63 GNs in order -->
                  </select>
                </div>
                <div>
                  <label for="activitiesGnSearchInput" style="display: block; font-size: 0.78rem; font-weight: 600; color: #CBD5E1; margin-bottom: 0.35rem;">
                    <i class="bi bi-search text-blue"></i> ඉක්මන් සෙවුම:
                  </label>
                  <div class="search-input-wrap" style="width: 100%;">
                    <i class="bi bi-search"></i>
                    <input type="text" id="activitiesGnSearchInput" class="glass-input" placeholder="වසමේ නම හෝ අංකයෙන් සොයන්න..." style="width: 100%; border-radius: 12px; padding: 0.65rem 1rem 0.65rem 2.6rem;" />
                  </div>
                </div>
              </div>

              <!-- Horizontal Interactive Slider with Left/Right Navigation Arrows -->
              <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                  <span style="font-size: 0.76rem; color: #94A3B8;"><i class="bi bi-sliders2 text-blue"></i> වසම් Slider පටිය (වසම් අතර මාරුවීමට ස්ලයිඩරය හෝ ඊතල භාවිතා කරන්න):</span>
                  <span style="font-size: 0.74rem; color: #64748B;">◀ ▶ ඊතල මගින් ස්ලයිඩ් කරන්න</span>
                </div>
                <div class="gn-slider-container">
                  <button id="btnSliderScrollLeft" class="slider-arrow-btn" title="පෙර වසම් ස්ලයිඩ් කරන්න" aria-label="පෙර වසම්">
                    <i class="bi bi-chevron-left"></i>
                  </button>
                  <div class="gn-slider-track" id="activitiesGnNavPills">
                    <!-- Dynamically populated with 63 GN pills with counts -->
                  </div>
                  <button id="btnSliderScrollRight" class="slider-arrow-btn" title="මීළඟ වසම් ස්ලයිඩ් කරන්න" aria-label="මීළඟ වසම්">
                    <i class="bi bi-chevron-right"></i>
                  </button>
                </div>
              </div>
            </div>'''

tab4_new = '''            <!-- GN Division Selection Ribbon & Search -->
            <div class="filter-card glass-panel" style="padding: 1.4rem; margin-bottom: 1.8rem;">
              <div style="font-size: 0.98rem; font-weight: 700; color: #243B64; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.6rem;">
                <span style="display: flex; align-items: center; gap: 0.5rem;">
                  <i class="bi bi-diagram-3-fill" style="font-size: 1.15rem; color: #3979D6;"></i> ග්‍රාම නිලධාරී වසම තෝරන්න (කලාප අනුව කාණ්ඩගත කිරීම, Slider හෝ Drop-Down මගින්):
                </span>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                  <div class="view-toggle-btns" style="display: inline-flex; background: #EEF4FC; padding: 0.25rem; border-radius: 10px; border: 1px solid #E5EAF2;">
                    <button id="btnToggleGnSliderView" class="view-toggle-btn active" style="border: none; background: #3979D6; color: #FFF; padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.8rem; font-weight: 600; cursor: pointer;">
                      <i class="bi bi-sliders"></i> Slider පටිය
                    </button>
                    <button id="btnToggleGnGroupedView" class="view-toggle-btn" style="border: none; background: transparent; color: #526078; padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.8rem; font-weight: 600; cursor: pointer;">
                      <i class="bi bi-grid-fill"></i> කාණ්ඩගත කොටු
                    </button>
                  </div>
                  <span class="glass-badge blue" style="font-size: 0.78rem;">
                    <i class="bi bi-check-circle-fill"></i> වසම් 63 ම සක්‍රීයයි
                  </span>
                </div>
              </div>

              <!-- Primary Drop-Down & Quick Search Selector -->
              <div style="display: grid; grid-template-columns: 1.8fr 1.2fr; gap: 1rem; align-items: center; margin-bottom: 1.2rem;">
                <div style="position: relative;">
                  <label for="activitiesGnSelectDropdown" style="display: block; font-size: 0.78rem; font-weight: 600; color: #526078; margin-bottom: 0.35rem;">
                    <i class="bi bi-chevron-down" style="color: #3979D6;"></i> වසම් Drop-Down මෙනුව (කලාප අනුව කාණ්ඩගත කර ඇත):
                  </label>
                  <select id="activitiesGnSelectDropdown" class="glass-select" style="width: 100%; font-size: 0.92rem; font-weight: 600; padding: 0.65rem 1.1rem;">
                    <!-- Dynamically populated with optgroups for all 8 zones -->
                  </select>
                </div>
                <div>
                  <label for="activitiesGnSearchInput" style="display: block; font-size: 0.78rem; font-weight: 600; color: #526078; margin-bottom: 0.35rem;">
                    <i class="bi bi-search" style="color: #3979D6;"></i> ඉක්මන් සෙවුම:
                  </label>
                  <div class="search-input-wrap" style="width: 100%;">
                    <i class="bi bi-search"></i>
                    <input type="text" id="activitiesGnSearchInput" class="glass-input" placeholder="වසමේ නම හෝ අංකයෙන් සොයන්න..." style="width: 100%; border-radius: 12px; padding: 0.65rem 1rem 0.65rem 2.6rem;" />
                  </div>
                </div>
              </div>

              <!-- Zone Cluster Filter Pills Bar -->
              <div style="margin-bottom: 0.8rem;">
                <div style="font-size: 0.78rem; font-weight: 600; color: #8793A6; margin-bottom: 0.4rem;">
                  <i class="bi bi-funnel-fill" style="color: #3979D6;"></i> කලාප පෙරහන (Zone Cluster තෝරන්න):
                </div>
                <div class="zone-filter-bar" id="activitiesGnZoneBar">
                  <!-- Dynamically populated zone buttons -->
                </div>
              </div>

              <!-- SLIDER VIEW (Active by default) -->
              <div id="activitiesGnSliderWrap">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                  <span style="font-size: 0.76rem; color: #526078;"><i class="bi bi-sliders2" style="color: #3979D6;"></i> වසම් Slider පටිය (වසම් අතර මාරුවීමට ස්ලයිඩරය හෝ ◀ ▶ ඊතල භාවිතා කරන්න):</span>
                  <span style="font-size: 0.74rem; color: #8793A6;">◀ ▶ ඊතල මගින් ස්ලයිඩ් කරන්න</span>
                </div>
                <div class="gn-slider-container">
                  <button id="btnSliderScrollLeft" class="slider-arrow-btn" title="පෙර වසම් ස්ලයිඩ් කරන්න" aria-label="පෙර වසම්">
                    <i class="bi bi-chevron-left"></i>
                  </button>
                  <div class="gn-slider-track" id="activitiesGnNavPills">
                    <!-- Dynamically populated with GN pills with counts -->
                  </div>
                  <button id="btnSliderScrollRight" class="slider-arrow-btn" title="මීළඟ වසම් ස්ලයිඩ් කරන්න" aria-label="මීළඟ වසම්">
                    <i class="bi bi-chevron-right"></i>
                  </button>
                </div>
              </div>

              <!-- GROUPED CARDS VIEW (Hidden by default, toggled via button) -->
              <div id="activitiesGnGroupedView" style="display: none; margin-top: 1rem;">
                <!-- Dynamically populated grouped zone cards -->
              </div>
            </div>'''

if tab4_old in html:
    html = html.replace(tab4_old, tab4_new)
    print("Replaced Tab 4 selection card successfully!")
else:
    print("Warning: tab4_old not found directly, checking partial replacement...")
    # fallback find block between "<!-- MODE 1:" and "<!-- Active Division Header Banner -->"
    pattern = r'(<!-- MODE 1: DEDICATED DIVISION-BY-DIVISION WEB ARTICLE SHOWCASE\s*-->\s*<div id="activitiesDivisionModeView">)(.*?)(<!-- Active Division Header Banner -->)'
    match = re.search(pattern, html, flags=re.DOTALL)
    if match:
        html = html[:match.start(2)] + "\n" + tab4_new + "\n            " + html[match.end(2):]
        print("Replaced Tab 4 selection card via regex successfully!")
    else:
        print("Error: Could not match Tab 4 selection block!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
