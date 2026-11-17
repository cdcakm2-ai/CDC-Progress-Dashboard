const path = require('path');

global.window = global;
global.window.matchMedia = () => ({ matches: false });
global.navigator = { userAgent: "Node" };
global.location = { hash: "#overview", reload: () => {} };
global.setInterval = () => {};
global.setTimeout = (fn) => fn();

global.Chart = class MockChart {
  constructor(canvas, config) {
    this.canvas = canvas;
    this.config = config;
  }
  destroy() {}
  resize() {}
  update() {}
};

const mockElement = () => {
  const el = {
    innerHTML: "",
    innerText: "",
    value: "",
    addEventListener: () => {},
    appendChild: () => {},
    style: {},
    classList: { add: () => {}, remove: () => {}, contains: () => false },
    setAttribute: () => {},
    getAttribute: () => null,
    querySelectorAll: () => [],
    querySelector: () => mockElement(),
    getBoundingClientRect: () => ({ top: 0, left: 0, width: 100, height: 100 }),
    getContext: () => ({
      fillRect: () => {},
      clearRect: () => {},
      measureText: () => ({ width: 0 })
    })
  };
  return el;
};

const listeners = [];
global.document = {
  readyState: "interactive",
  addEventListener: (evt, fn) => {
    listeners.push({ evt, fn });
  },
  getElementById: (id) => mockElement(),
  querySelector: () => mockElement(),
  querySelectorAll: () => [mockElement()],
  createElement: () => mockElement(),
  body: mockElement()
};

global.localStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

try {
  require('../js/data.js');
  require('../js/sheets-service.js');
  require('../js/charts.js');
  require('../js/app.js');

  listeners.forEach(l => {
    if (l.evt === 'DOMContentLoaded') l.fn();
  });

  if (window.pssApp) {
    console.log("pssApp created.");
    window.pssApp.init().then(() => {
      console.log("SUCCESS! All 12 methods in init() ran without any errors!");
      console.log("Activities loaded:", window.pssApp.data.activities.length);
      console.log("GN Divisions loaded:", window.pssApp.data.gnDivisions.length);
      console.log("Filtered activities:", window.pssApp.filteredActivities.length);
    }).catch(e => {
      console.error("ERROR in init():", e);
    });
  }
} catch (e) {
  console.error("CRITICAL ERROR during script execution:", e);
}
