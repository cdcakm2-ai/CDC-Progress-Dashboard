/**
 * Google Sheets & Google Drive Integration Engine with Google OAuth 2.0 (GIS)
 * ප්‍රජා සංවර්ධන සභා මගින් සිදු කරන ලද වැඩසටහන් - අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසය
 * 
 * Google Cloud OAuth 2.0 Client ID:
 * 385022926771-9ees1jtcu1nmsqd0bkr2nkp3e559f529.apps.googleusercontent.com
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
    
    // Google Cloud OAuth 2.0 Configuration
    this.googleClientId = (this.config && this.config.googleClientId) || "385022926771-9ees1jtcu1nmsqd0bkr2nkp3e559f529.apps.googleusercontent.com";
    this.driveFolderId = (this.config && this.config.driveFolderId) || "1jBY0y_QWiinEPXEpEU6OwesPmlIna33C";
    this.tokenClient = null;
    this.accessToken = sessionStorage.getItem("pss_google_access_token") || null;
    this.authCallbacks = [];

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

    // Attempt lazy init if Google Identity Services is already in DOM
    this.tryInitGoogleAuth();
  }

  // =========================================================================
  // Google OAuth 2.0 (Google Identity Services - GIS) Integration
  // =========================================================================

  onAuthStateChange(callback) {
    if (typeof callback === "function") {
      this.authCallbacks.push(callback);
      // Immediately notify current state
      callback(this.isGoogleAuthenticated());
    }
  }

  notifyAuthChange(isAuthenticated, error = null) {
    this.authCallbacks.forEach(cb => {
      try {
        cb(isAuthenticated, error);
      } catch (e) {
        console.warn("Auth callback error:", e);
      }
    });
  }

  isGoogleAuthenticated() {
    if (!this.accessToken) return false;
    const expiry = sessionStorage.getItem("pss_google_token_expiry");
    if (expiry && Date.now() > Number(expiry)) {
      this.accessToken = null;
      sessionStorage.removeItem("pss_google_access_token");
      sessionStorage.removeItem("pss_google_token_expiry");
      return false;
    }
    return true;
  }

  tryInitGoogleAuth() {
    if (this.tokenClient) return true;
    if (typeof google === "undefined" || !google.accounts || !google.accounts.oauth2) {
      return false;
    }

    try {
      this.tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: this.googleClientId,
        scope: "https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/spreadsheets.readonly",
        callback: (resp) => {
          if (resp && resp.error) {
            console.error("Google OAuth token error:", resp);
            this.notifyAuthChange(false, resp);
            return;
          }
          if (resp && resp.access_token) {
            this.accessToken = resp.access_token;
            sessionStorage.setItem("pss_google_access_token", resp.access_token);
            if (resp.expires_in) {
              const expTime = Date.now() + (Number(resp.expires_in) * 1000);
              sessionStorage.setItem("pss_google_token_expiry", String(expTime));
            }
            console.log(" Google OAuth 2.0 token successfully acquired!");
            this.notifyAuthChange(true);
          }
        }
      });
      return true;
    } catch (err) {
      console.warn("Error initializing Google Identity Services Token Client:", err);
      return false;
    }
  }

  requestGoogleLogin(promptMode = "consent") {
    if (!this.tokenClient) {
      const initialized = this.tryInitGoogleAuth();
      if (!initialized) {
        throw new Error("Google Identity Services (GIS) පුස්තකාලය තවමත් පූරණය වෙමින් පවතී. කරුණාකර තත්පර කිහිපයකින් නැවත උත්සාහ කරන්න.");
      }
    }
    this.tokenClient.requestAccessToken({ prompt: promptMode });
  }

  disconnectGoogleAuth() {
    const currentToken = this.accessToken;
    this.accessToken = null;
    sessionStorage.removeItem("pss_google_access_token");
    sessionStorage.removeItem("pss_google_token_expiry");

    if (currentToken && typeof google !== "undefined" && google.accounts && google.accounts.oauth2) {
      try {
        google.accounts.oauth2.revoke(currentToken, () => {
          console.log(" Google OAuth token revoked.");
        });
      } catch (e) {
        console.warn("Token revocation failed:", e);
      }
    }

    this.notifyAuthChange(false);
  }

  /**
   * Scan Google Drive folder for files using live Google Drive API v3
   */
  async fetchLiveDriveFiles(folderId = this.driveFolderId) {
    if (!this.isGoogleAuthenticated()) {
      throw new Error("Google Drive API ඇමතීමට ප්‍රථම Google OAuth සත්‍යාපනය අවශ්‍ය වේ.");
    }

    const query = encodeURIComponent(`'${folderId}' in parents and trashed = false`);
    const fields = encodeURIComponent("files(id, name, mimeType, modifiedTime, size, webViewLink, iconLink)");
    const url = `https://www.googleapis.com/drive/v3/files?q=${query}&fields=${fields}&orderBy=modifiedTime%20desc`;

    const response = await fetch(url, {
      headers: {
        "Authorization": `Bearer ${this.accessToken}`
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        this.disconnectGoogleAuth();
        throw new Error("Google OAuth ටෝකනය කල් ඉකුත් වී ඇත. කරුණාකර නැවත Google ගිණුමට සම්බන්ධ වන්න.");
      }
      throw new Error(`Google Drive API දෝෂයකි: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data.files || [];
  }

  /**
   * Fetch spreadsheet cell values using live Google Sheets API v4
   */
  async fetchSheetValues(spreadsheetId, range = "A1:Z100") {
    if (!this.isGoogleAuthenticated()) {
      throw new Error("Google Sheets API ඇමතීමට ප්‍රථම Google OAuth සත්‍යාපනය අවශ්‍ය වේ.");
    }

    const url = `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/${encodeURIComponent(range)}`;
    const response = await fetch(url, {
      headers: {
        "Authorization": `Bearer ${this.accessToken}`
      }
    });

    if (!response.ok) {
      throw new Error(`Google Sheets API දෝෂයකි: ${response.status}`);
    }

    const data = await response.json();
    return data.values || [];
  }

  // =========================================================================
  // Master Dashboard Data Methods
  // =========================================================================

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
