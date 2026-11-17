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

console.log('=== INSPECTING SHEET 1: FORM RESPONSES 1 ===');
const s1Text = fs.readFileSync('raw_drive_data/sheet1_form_responses_1.csv', 'utf8');
const s1 = parseCSV(s1Text);
console.log('Total rows (incl header):', s1.length);
console.log('Headers:');
s1[0].forEach((h, i) => console.log(`  Col ${i}: ${h.replace(/\n/g, ' ')}`));

console.log('\nSample Row 1:');
s1[1].slice(0, 10).forEach((val, i) => console.log(`  ${s1[0][i].replace(/\n/g, ' ')}: ${val}`));

console.log('\n=== INSPECTING SHEET 2: FORM RESPONSES 1 (Aug/Sep) ===');
const s2Text = fs.readFileSync('raw_drive_data/sheet2_form_responses_1.csv', 'utf8');
const s2 = parseCSV(s2Text);
console.log('Total rows (incl header):', s2.length);
console.log('Headers:');
s2[0].forEach((h, i) => console.log(`  Col ${i}: ${h.replace(/\n/g, ' ')}`));

console.log('\n=== INSPECTING SHEET 1: CALC_DATA ===');
const calcText = fs.readFileSync('raw_drive_data/sheet1_calc_data.csv', 'utf8');
console.log(calcText);
