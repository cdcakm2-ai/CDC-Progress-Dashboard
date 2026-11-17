const path = require('path');

global.window = global;
global.navigator = { userAgent: "Node" };
global.location = { hash: "#overview", reload: () => {} };
global.setInterval = () => {};
global.setTimeout = (fn) => fn();

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
    querySelector: () => null,
    getBoundingClientRect: () => ({ top: 0, left: 0, width: 100, height: 100 }),
    getContext: () => ({
      fillRect: () => {},
      clearRect: () => {},
      getImageData: () => {},
      putImageData: () => {},
      createImageData: () => {},
      setTransform: () => {},
      drawImage: () => {},
      save: () => {},
      fillText: () => {},
      restore: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      closePath: () => {},
      stroke: () => {},
      translate: () => {},
      scale: () => {},
      rotate: () => {},
      arc: () => {},
      fill: () => {},
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

  // Trigger all DOMContentLoaded listeners
  listeners.forEach(l => {
    if (l.evt === 'DOMContentLoaded') l.fn();
  });

  if (window.pssApp) {
    console.log("pssApp was successfully created!");
    window.pssApp.init().then(() => {
      console.log("pssApp.init() completed without errors!");
      console.log("Activities loaded:", window.pssApp.data.activities.length);
    }).catch(e => {
      console.error("ERROR in init():", e);
    });
  } else {
    console.error("pssApp was NOT created!");
  }
} catch (e) {
  console.error("CRITICAL ERROR during script execution:", e);
}
