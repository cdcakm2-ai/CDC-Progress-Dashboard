with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_tab4_block = '''            <!-- GN Division Selection Ribbon & Search -->
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
            </div>
'''

start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if '<!-- GN Division Selection Ribbon & Search -->' in line:
        start_idx = i
    if start_idx is not None and '<!-- Active Division Header Banner -->' in line:
        end_idx = i
        break

if start_idx is not None and end_idx is not None:
    lines[start_idx:end_idx] = [new_tab4_block + '\n']
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Replaced lines {start_idx+1} to {end_idx} with new_tab4_block successfully!")
else:
    print(f"Could not find indices: start={start_idx}, end={end_idx}")
