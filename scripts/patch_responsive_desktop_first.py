def patch_responsive():
    with open('css/responsive.css', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace top global block
    old_top = '''/* Strict Global Mobile Overflow Containment */
html, body {
  max-width: 100vw !important;
  width: 100% !important;
  overflow-x: hidden !important;
  position: relative !important;
  margin: 0 !important;
  padding: 0 !important;
  box-sizing: border-box !important;
}

*, *::before, *::after {
  box-sizing: border-box !important;
}

.app-layout {
  max-width: 100vw !important;
  width: 100% !important;
  overflow-x: hidden !important;
}

.app-main {
  max-width: 100% !important;
  width: 100% !important;
  min-width: 0 !important;
  overflow-x: hidden !important;
}

.tab-content-area,
.tab-view {
  max-width: 100% !important;
  width: 100% !important;
  min-width: 0 !important;
  overflow-x: hidden !important;
}'''

    new_top = '''/* Base Global Layout & Box Model */
html, body {
  width: 100%;
  min-height: 100vh;
  position: relative;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

*, *::before, *::after {
  box-sizing: border-box;
}

/* Desktop App Layout Shell (Default - Full Desktop Width) */
.app-layout {
  width: 100%;
  min-height: 100vh;
  display: flex;
  position: relative;
}

.app-main {
  margin-left: var(--sidebar-width);
  width: calc(100% - var(--sidebar-width));
  max-width: calc(100% - var(--sidebar-width));
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.tab-content-area {
  flex: 1;
  padding: 2rem 2.5rem;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.tab-view {
  width: 100%;
  max-width: 100%;
}'''

    assert old_top in content, "old_top not found in css/responsive.css"
    content = content.replace(old_top, new_top)

    # In max-width: 1280px, allow charts to stay 2-column or 1.2fr 1fr
    content = content.replace(
'''  .charts-grid {
    grid-template-columns: 1fr;
  }''',
'''  .charts-grid {
    grid-template-columns: 1.2fr 1fr;
    gap: 1.2rem;
  }'''
    )

    with open('css/responsive.css', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Updated css/responsive.css for desktop-first layout.")

if __name__ == '__main__':
    patch_responsive()
