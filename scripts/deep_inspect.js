const fs = require('fs');

function parseCSVLine(text) {
  const result = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      if (inQuotes && text[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === ',' && !inQuotes) {
      result.push(cur);
      cur = '';
    } else {
      cur += c;
    }
  }
  result.push(cur);
  return result;
}

function parseCSV(content) {
  const lines = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < content.length; i++) {
    const c = content[i];
    if (c === '"') {
      if (inQuotes && content[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if ((c === '\r' || c === '\n') && !inQuotes) {
      if (c === '\r' && content[i + 1] === '\n') i++;
      if (cur.trim().length > 0) lines.push(parseCSVLine(cur));
      cur = '';
    } else {
      cur += c;
    }
  }
  if (cur.trim().length > 0) lines.push(parseCSVLine(cur));
  return lines;
}

function cleanGN(raw) {
  if (!raw) return '';
  // e.g. "109/ ජී ඇටඹගස්මුල්ල" -> "ඇටඹගස්මුල්ල"
  // e.g. "133/සී නාගහවත්ත" -> "නාගහවත්ත"
  let cleaned = raw.replace(/^[0-9\s\/a-zA-Z\u0D80-\u0DFF]+?\s+/, '').trim();
  if (!cleaned || cleaned.length < 3) cleaned = raw.trim();
  return cleaned;
}

function extractActivities(rows, sourceName) {
  const activities = [];
  for (let r = 1; r < rows.length; r++) {
    const row = rows[r];
    const timestamp = row[0];
    const officerName = row[1];
    const gnRaw = row[2];
    const gnClean = cleanGN(gnRaw);
    const claimedCount = parseInt(row[3]) || 0;

    // Up to 8 programs per row
    // Program 1: cols 4, 5, 6
    // Program 2: cols 8, 9, 10
    // Program 3: cols 12, 13, 14
    // Program 4: cols 16, 17, 18
    // Program 5: cols 20, 21, 22
    // Program 6: cols 24, 25, 26
    // Program 7: cols 28, 29, 30
    // Program 8: cols 32, 33, 34
    for (let p = 0; p < 8; p++) {
      const dateCol = 4 + p * 4;
      const descCol = 5 + p * 4;
      const photoCol = 6 + p * 4;

      if (dateCol < row.length) {
        const dateVal = (row[dateCol] || '').trim();
        const descVal = (row[descCol] || '').trim();
        const photoVal = (row[photoCol] || '').trim();

        if (dateVal || descVal || photoVal) {
          activities.push({
            source: sourceName,
            rowIndex: r,
            programIndex: p + 1,
            timestamp,
            officerName,
            gnRaw,
            gnClean,
            date: dateVal,
            description: descVal,
            photoUrl: photoVal
          });
        }
      }
    }
  }
  return activities;
}

const s1Rows = parseCSV(fs.readFileSync('raw_drive_data/sheet1_form_responses_1.csv', 'utf8'));
const s2Rows = parseCSV(fs.readFileSync('raw_drive_data/sheet2_form_responses_1.csv', 'utf8'));

const act1 = extractActivities(s1Rows, 'Sheet 1 (Nov-Jul)');
const act2 = extractActivities(s2Rows, 'Sheet 2 (Aug-Oct)');

console.log(`Sheet 1: ${s1Rows.length - 1} submissions -> ${act1.length} activities extracted.`);
console.log(`Sheet 2: ${s2Rows.length - 1} submissions -> ${act2.length} activities extracted.`);
console.log(`Total extracted activities across both sheets: ${act1.length + act2.length}`);

// Unique GNs
const allGNs = new Set([...act1, ...act2].map(a => a.gnClean));
console.log(`Total unique GN divisions represented: ${allGNs.size}`);
console.log('Sample GNs:', [...allGNs].slice(0, 15).join(', '));

// Count photos
const photosWithLinks = [...act1, ...act2].filter(a => a.photoUrl && a.photoUrl.includes('drive.google.com'));
console.log(`Activities with Google Drive photo links: ${photosWithLinks.length}`);

// Date format samples
const dateSamples = [...new Set([...act1, ...act2].map(a => a.date))].filter(Boolean).slice(0, 15);
console.log('Sample dates:', dateSamples.join(' | '));
