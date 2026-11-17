const path = require('path');

global.window = global;
global.document = {
  readyState: "complete",
  addEventListener: () => {},
  getElementById: (id) => ({
    innerHTML: "",
    innerText: "",
    addEventListener: () => {},
    appendChild: () => {},
    style: {},
    classList: { add: () => {}, remove: () => {}, contains: () => false },
    setAttribute: () => {},
    getAttribute: () => null,
    querySelectorAll: () => []
  }),
  querySelector: () => null,
  querySelectorAll: () => [],
  createElement: () => ({
    innerHTML: "",
    innerText: "",
    addEventListener: () => {},
    appendChild: () => {},
    style: {},
    classList: { add: () => {}, remove: () => {} },
    setAttribute: () => {},
    getAttribute: () => null
  })
};
global.localStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

try {
  require('../js/data.js');
  console.log("data.js loaded. PSS_DATA activities:", (window.PSS_DATA?.activities || []).length);
  require('../js/sheets-service.js');
  console.log("sheets-service.js loaded.");
  require('../js/charts.js');
  console.log("charts.js loaded.");
  require('../js/app.js');
  console.log("app.js loaded.");
} catch (e) {
  console.error("CRITICAL ERROR during script load:", e);
}
