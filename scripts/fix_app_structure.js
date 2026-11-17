const fs = require('fs');

let code = fs.readFileSync('js/app.js', 'utf8');

// Find the marker for the misplaced analytics methods
const marker = '// =========================================================================\n  // TAB 6: ප්‍රගති විශ්ලේෂණය (PROGRESS ANALYSIS ENGINE)';
const markerIndex = code.indexOf(marker);

if (markerIndex === -1) {
  console.error('Could not find marker!');
  process.exit(1);
}

// Slice out the analytics methods text
const analyticsCode = code.slice(markerIndex).replace(/}\s*\);\s*$/, '').trim();

// Get the original code up to line 3070 (before the class closed)
const classEndMarker = '// --- 3D Tilt Effect on Glass Cards ---';
const classEndIdx = code.indexOf(classEndMarker);
if (classEndIdx === -1) {
  console.error('Could not find classEndMarker!');
  process.exit(1);
}

// Find the closing brace of init3DTilt
const tiltFuncEnd = code.indexOf('}\n}', classEndIdx);
const insertPos = tiltFuncEnd + 1; // After the closing brace of init3DTilt, before class closing brace

const beforeClassEnd = code.slice(0, insertPos);

// Reconstruct
const finalCode = beforeClassEnd + '\n\n  ' + analyticsCode + '\n}\n\n' +
`// Global initialization
document.addEventListener("DOMContentLoaded", () => {
  window.pssApp = new PssApp();
  window.prajaApp = window.pssApp;
  window.pssApp.init();
});
`;

fs.writeFileSync('js/app.js', finalCode, 'utf8');
console.log('Successfully structured js/app.js!');
