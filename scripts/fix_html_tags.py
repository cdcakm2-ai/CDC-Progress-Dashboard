from html.parser import HTMLParser

class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in ['img', 'input', 'br', 'hr', 'meta', 'link']:
            self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag not in ['img', 'input', 'br', 'hr', 'meta', 'link']:
            if self.stack and self.stack[-1][0] == tag:
                self.stack.pop()
            else:
                self.errors.append((f'Mismatched </{tag}>', self.getpos(), self.stack[-3:] if self.stack else []))

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix lines 1079-1126: remove the first duplicate partial block and keep the clean filter controls
    target_part1 = '''            <!-- Table Controls & Live Search for 63 Divisions -->
            <div class="filter-card glass-panel" style="margin-bottom: 1rem; padding: 0.8rem 1.2rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.8rem;">
                <div class="search-input-wrap" style="width: 320px;">
                  <i class="bi bi-search"></i>
                  <input type="text" id="anDivSearchInput" class="glass-input" placeholder="වසමේ නමින් සොයන්න..." style="width: 100%; border-radius: 999px;" />
                </div>
                <span class="glass-badge gold" id="anDivCountBadge">වසම් 63ම ඇතුළත්ය</span>
              </div>
            </div>

            <div class="table-responsive glass-panel" style="padding: 0; overflow: hidden; margin-bottom: 1.8rem; max-height: 520px; overflow-y: auto;">
              <table class="glass-table" style="width: 100%; margin-bottom: 0;">
                <thead style="position: sticky; top: 0; z-index: 10; background: #0A192F;">
                  <tr>
                    <th style="width: 60px; text-align: center;">ශ්‍රේණිය</th>
                    <th>ග්‍රාම නිලධාරී වසම</th>
                    <th>ප්‍රමුඛ ක්ෂේත්‍රය</th>
                    <th style="text-align: center;">මුළු වැඩසටහන්</th>
                    <th style="text-align: center;">විවිධත්වය (10න්)</th>
                    <th style="text-align: center;">ක්‍රියාකාරී දින</th>
                    <th style="text-align: center;">ඡායාරූප ගණන</th>
                    <th style="text-align: center;">තත්ත්වය</th>
                  </tr>
                </thead>
                <tbody id="anDivisionsTableBody">
                  <!-- Dynamically populated for all 63 divisions -->
                </tbody>
              </table>
            </div>
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
                  <button class="btn-glass an-div-filter-pill" data-filter="top10" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-star-fill text-blue"></i> ඉහළම 10</button>
                  <button class="btn-glass an-div-filter-pill" data-filter="completed100" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-check-circle text-success"></i> 100% සම්පූර්ණ</button>
                  <button class="btn-glass an-div-filter-pill" data-filter="low" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-exclamation-circle text-warning"></i> අවධානය අවශ්‍ය</button>
                </div>
              </div>
            </div>'''

    replacement_part1 = '''            <!-- Table Controls & Live Search for 63 Divisions -->
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
                  <button class="btn-glass an-div-filter-pill" data-filter="top10" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-star-fill text-blue"></i> ඉහළම 10</button>
                  <button class="btn-glass an-div-filter-pill" data-filter="completed100" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-check-circle text-success"></i> 100% සම්පූර්ණ</button>
                  <button class="btn-glass an-div-filter-pill" data-filter="low" style="padding: 0.35rem 0.8rem; font-size: 0.8rem;"><i class="bi bi-exclamation-circle text-warning"></i> අවධානය අවශ්‍ය</button>
                </div>
              </div>
            </div>'''

    assert target_part1 in content, "target_part1 not found"
    content = content.replace(target_part1, replacement_part1)

    # 2. Fix modal bottom extra closing divs
    target_part2 = '''        <!-- Modal Bottom Actions: Print/PDF report for this activity -->
        <div style="display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 1.2rem; flex-wrap: wrap;">
          <button id="btnPrintActivityReport" class="btn-gold" style="padding: 0.55rem 1.3rem;">
            <i class="bi bi-printer"></i> මෙම වැඩසටහන් වාර්තාව මුද්‍රණය / PDF
          </button>
        </div>
        </div>
      </div>
    </div>
  </div>'''

    replacement_part2 = '''        <!-- Modal Bottom Actions: Print/PDF report for this activity -->
        <div style="display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 1.2rem; flex-wrap: wrap;">
          <button id="btnPrintActivityReport" class="btn-gold" style="padding: 0.55rem 1.3rem;">
            <i class="bi bi-printer"></i> මෙම වැඩසටහන් වාර්තාව මුද්‍රණය / PDF
          </button>
        </div>
      </div>
    </div>
  </div>'''

    assert target_part2 in content, "target_part2 not found"
    content = content.replace(target_part2, replacement_part2)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    checker = TagChecker()
    checker.feed(content)
    print("Verification after fix:")
    print("Unclosed tags:", len(checker.stack))
    print("Mismatched tags:", len(checker.errors))
    for err, pos, stack in checker.errors:
        print(f"  {err} at {pos}, stack: {[s[0] for s in stack]}")

if __name__ == '__main__':
    main()
