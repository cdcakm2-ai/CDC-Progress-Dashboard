with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Patch async init() normalization
old_init_block = '''  async init() {
    this.data = await window.pssSheetsService.getDashboardData();

    // Ensure activities are sorted newest first
    if (Array.isArray(this.data.activities)) {
      this.data.activities.sort((a, b) => new Date(b.date) - new Date(a.date));
    }
    this.filteredActivities = [...this.data.activities];'''

new_init_block = '''  async init() {
    this.data = await window.pssSheetsService.getDashboardData();

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
            caption: (p && p.caption) || `${act.titleSi} - ${act.gnNameSi}`
          };
        });
      });

      this.data.activities.sort((a, b) => new Date(b.date) - new Date(a.date));
    }
    this.filteredActivities = [...this.data.activities];'''

text = text.replace(old_init_block, new_init_block)

# 2. Patch line 1028 in renderOverviewTab()
old_recent_img = '''<img src="${act.images[0]}" alt="${act.titleSi}" style="width: 48px; height: 48px; border-radius: 10px; object-fit: cover;" />'''
new_recent_img = '''<img src="${(act.images && act.images[0]) || (act.photos && act.photos[0] && (act.photos[0].thumbnailUrl || act.photos[0].fullUrl)) || 'https://images.unsplash.com/photo-1544717305-2782549b5136?w=100'}" alt="${act.titleSi}" style="width: 48px; height: 48px; border-radius: 10px; object-fit: cover; background: #F3F6FC;" />'''

text = text.replace(old_recent_img, new_recent_img)

# 3. Patch createWebArticleElement
old_web_article = '''    const photos = act.photoObjects || (act.images || []).map((url, i) => ({
      id: `${act.id}-p${i}`,
      thumbnail: url,
      full: url,
      driveUrl: url,
      caption: `${act.titleSi} - ${act.gnNameSi}`
    }));
    const photoCount = photos.length;

    // Photos Gallery Grid (Uncropped full presentation)
    let galleryHtml = "";
    if (photoCount > 0) {
      galleryHtml = `
        <div class="activity-article-gallery-box">
          <div class="activity-article-gallery-title">
            <span><i class="bi bi-camera-fill text-gold"></i> à·ƒà¶­à·Šâ€ à¶»à·šà¶­à·Šâ€ à¶» à¶¡à· à¶ºà· à¶»à·–à¶´ (${photoCount})</span>
            <span style="font-size: 0.76rem; color: #94A3B8;">à·€à·’à· à· à¶½ à¶šà·’à¶»à·“à¶¸à¶§ à¶šà·Šà¶½à·’à¶šà·Š à¶šà¶»à¶±à·Šà¶±</span>
          </div>
          <div class="activity-article-gallery-grid">
            ${photos.map((p, pIdx) => `
              <div class="activity-article-photo-item" data-photo-idx="${pIdx}" title="${p.caption || act.titleSi}">
                <img src="${p.thumbnail || p.full}" alt="${act.titleSi}" class="activity-article-photo-img" loading="lazy" />
                <div class="activity-article-photo-overlay">
                  <i class="bi bi-arrows-fullscreen"></i>
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    } else {
      galleryHtml = `
        <div class="activity-article-gallery-box" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 180px; text-align: center;">
          <i class="bi bi-images" style="font-size: 2rem; color: #475569; margin-bottom: 0.5rem;"></i>
          <span style="font-size: 0.85rem; color: #64748B;">à¶¸à·™à¶¸ à·€à· à¶©à·ƒà¶§à·„à¶± à·ƒà¶³à·„à·  à¶¡à· à¶ºà· à¶»à·–à¶´ à¶…à¶¸à·”à¶«à·  à¶±à· à¶­</span>
        </div>
      `;
    }'''

new_web_article = '''    const photos = (act.photoObjects && act.photoObjects.length > 0)
      ? act.photoObjects
      : (act.photos || []).map((p, i) => ({
          id: p.id || `${act.id}-p${i}`,
          thumbnail: p.thumbnailUrl || p.fullUrl || (typeof p === 'string' ? p : ''),
          full: p.fullUrl || p.thumbnailUrl || (typeof p === 'string' ? p : ''),
          driveUrl: p.driveUrl || (p.fullUrl || ''),
          caption: p.caption || `${act.titleSi || act.title} - ${act.gnNameSi}`
        }));
    const photoCount = photos.length;

    // Photos Gallery Grid (Uncropped full presentation)
    let galleryHtml = "";
    if (photoCount > 0) {
      galleryHtml = `
        <div class="activity-article-gallery-box" style="background: #F8FAFD; border: 1px solid #E5EAF2; border-radius: 16px; padding: 1.2rem;">
          <div class="activity-article-gallery-title" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; border-bottom: 1px solid #E5EAF2; padding-bottom: 0.5rem;">
            <span style="color: #243B64; font-weight: 700; font-size: 0.95rem;"><i class="bi bi-camera-fill" style="color: #3979D6;"></i> සත්‍ය ක්ෂේත්‍ර ඡායාරූප (${photoCount})</span>
            <span style="font-size: 0.76rem; color: #8793A6;">විශාල කිරීමට ක්ලික් කරන්න</span>
          </div>
          <div class="activity-article-gallery-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 0.8rem;">
            ${photos.map((p, pIdx) => `
              <div class="activity-article-photo-item" data-photo-idx="${pIdx}" title="${p.caption || act.titleSi || act.title}" style="border-radius: 12px; overflow: hidden; border: 1px solid #E5EAF2; height: 160px; background: #FFF; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                <img src="${p.thumbnail || p.full}" alt="${act.titleSi || act.title}" class="activity-article-photo-img" loading="lazy" style="width: 100%; height: 100%; object-fit: contain !important; background: #F3F6FC;" />
              </div>
            `).join("")}
          </div>
        </div>
      `;
    } else {
      galleryHtml = `
        <div class="activity-article-gallery-box" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 180px; text-align: center; background: #F8FAFD; border: 1px dashed #E5EAF2; border-radius: 16px; padding: 1rem;">
          <i class="bi bi-images" style="font-size: 2rem; color: #8793A6; margin-bottom: 0.5rem;"></i>
          <span style="font-size: 0.85rem; color: #8793A6;">මෙම වැඩසටහන සඳහා ඡායාරූප අමුණා නැත</span>
        </div>
      `;
    }'''

text = text.replace(old_web_article, new_web_article)

# Fix categoryNameSi and title in article header
text = text.replace('${act.categoryNameSi}', '${act.categoryNameSi || act.categoryName || "ප්‍රජා සංවර්ධන"}')
text = text.replace('${act.titleSi}', '${act.titleSi || act.title || act.description || "වැඩසටහන"}')

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated js/app.js with defensive activity normalization and photo mapping!")
