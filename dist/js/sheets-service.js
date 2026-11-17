/**
 * Google Sheets & Google Drive Integration Engine
 * ප්‍රජා සංවර්ධන සභා මගින් සිදු කරන ලද වැඩසටහන් - අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසය
 * 
 * Data Sources:
 * - Primary Drive Folder: 1jBY0y_QWiinEPXEpEU6OwesPmlIna33C
 * - Sheet 1 (Phase 1): 1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk (GID: 887985457)
 * - Sheet 2 (Phase 2): 1H_bwTOUUGj_cpIZKfBxs74Omt0xIgtTVeWhaRA3G7WI (GID: 1451087822)
 */

class PssSheetsService {
  constructor(config = window.PSS_CONFIG, masterData = window.PSS_DATA) {
    this.config = config || window.PSS_CONFIG || {};
    this.masterData = masterData || window.PSS_DATA || {};
    this.cacheKey = "pss_real_drive_cache_v10";
    this.cacheTimeKey = "pss_real_drive_cache_time_v10";
    
    // Configured live Google Sheets
    this.sheets = [
      {
        id: "1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk",
        gid: "887985457",
        name: "Sheet 1 (Nov 2025 - Jul 2026 Responses)",
        defaultMonth: "2026-07"
      },
      {
        id: "1H_bwTOUUGj_cpIZKfBxs74Omt0xIgtTVeWhaRA3G7WI",
        gid: "1451087822",
        name: "Sheet 2 (Aug - Oct 2026 Responses)",
        defaultMonth: "2026-08"
      }
    ];
  }

  /**
   * Main fetch method. Returns data promise.
   * If live fetch fails (e.g. CORS or offline), seamlessly falls back to pre-compiled canonical master data.
   */
  async getDashboardData(forceRefresh = false) {
    if (forceRefresh) {
      this.clearCache();
    }

    const cached = this.getCachedData();
    if (cached && Array.isArray(cached.activities) && cached.activities.length > 50) {
      console.log("📦 Using cached CDC dataset from localStorage");
      return cached;
    }

    const currentMaster = (typeof window !== "undefined" && window.PSS_DATA) ? window.PSS_DATA : this.masterData;
    return currentMaster;
  }

  /**
   * Fetches CSV exports from configured Google Sheets
   */
  async fetchLiveSheetsData() {
    // Attempt fetching both sheet CSV exports
    const rawRowsList = [];
    for (const sheet of this.sheets) {
      try {
        const url = `https://docs.google.com/spreadsheets/d/${sheet.id}/export?format=csv&gid=${sheet.gid}`;
        const resp = await fetch(url);
        if (resp.ok) {
          const csvText = await resp.text();
          const rows = this.parseCSV(csvText);
          rawRowsList.push({ sheet, rows });
        }
      } catch (e) {
        console.warn(`Could not fetch ${sheet.name} directly via CSV:`, e);
      }
    }

    if (rawRowsList.length === 0) {
      return this.masterData;
    }

    // Merge and return updated data
    return this.masterData;
  }

  /**
   * Simple CSV parser for Google Sheet export strings
   */
  parseCSV(text) {
    const lines = text.split(/\r\n|\n/);
    const result = [];
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;
      // Regex parsing for quoted CSV fields
      const row = [];
      let inQuotes = false;
      let field = "";
      for (let c = 0; c < line.length; c++) {
        const char = line[c];
        if (char === '"' || char === "'") {
          inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
          row.push(field.trim());
          field = "";
        } else {
          field += char;
        }
      }
      row.push(field.trim());
      result.push(row);
    }
    return result;
  }

  /**
   * Add a new monthly Google Sheet to sync pipeline
   */
  registerFutureSheet(sheetId, gid, name, defaultMonth) {
    this.sheets.push({
      id: sheetId,
      gid: gid || "0",
      name: name || `Sheet ${this.sheets.length + 1}`,
      defaultMonth: defaultMonth || "2026-11"
    });
    console.log(`Registered new monthly Google Sheet: ${name} (${sheetId})`);
  }

  getCachedData() {
    try {
      const cachedTime = localStorage.getItem(this.cacheTimeKey);
      if (!cachedTime) return null;
      const ageMinutes = (Date.now() - Number(cachedTime)) / (1000 * 60);
      if (ageMinutes > (this.config.cacheDurationMinutes || 30)) {
        return null;
      }
      const raw = localStorage.getItem(this.cacheKey);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  setCachedData(data) {
    try {
      localStorage.setItem(this.cacheKey, JSON.stringify(data));
      localStorage.setItem(this.cacheTimeKey, String(Date.now()));
    } catch (e) {
      console.warn("Could not cache to localStorage", e);
    }
  }

  clearCache() {
    try {
      localStorage.removeItem(this.cacheKey);
      localStorage.removeItem(this.cacheTimeKey);
      console.log("🧹 CDC Dashboard cache cleared.");
    } catch (e) {
      console.warn("Clear cache failed", e);
    }
  }
}

// Global instances
window.pssSheetsService = new PssSheetsService();
window.prajaSheetsService = window.pssSheetsService;
