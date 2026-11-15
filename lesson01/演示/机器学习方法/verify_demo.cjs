/* Run with node verify_demo.cjs. Checks calculations and UI state without a browser. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const math = require('./demo.js');
const data = require('./wine-data.js');

// Validate every exported dimensional model against its saved confusion matrix.
for (let dimensions = 2; dimensions <= 13; dimensions++) {
  const confusion = Array.from({length: 3}, () => [0, 0, 0]);
  data.pca.forEach((row, i) => confusion[data.labels[i]][math.classify(row.slice(0, dimensions), data.models[dimensions])]++);
  assert.deepEqual(confusion, data.models[dimensions].confusion);
  assert.equal(confusion.reduce((sum, row, i) => sum + row[i], 0), data.models[dimensions].correct);
  const rows = math.standardize(data.raw.map(row => row.slice(0, dimensions)));
  let centers = math.initialize(rows, 3), labels = [], previous = Infinity, stable = false;
  for (let iteration = 0; iteration <= 100; iteration++) {
    const next = math.assign(rows, centers);
    const loss = math.objective(rows, next, centers);
    assert(loss <= previous + 1e-8);
    previous = loss;
    if (next.every((value, i) => value === labels[i])) { stable = true; break; }
    labels = next;
    centers = math.update(rows, labels, centers);
  }
  assert(stable);
  assert.equal(centers[0].length, dimensions);
  if (dimensions === 2) assert.equal(math.compareGroups(labels, data.labels).matched, 137);
}
assert.equal(math.squaredDistance([0, 0, 0], [0, 0, 3]), 9);

// Small DOM adapter: exercise actual event handlers and rendering, with controllable timers.
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const elements = {};
for (const match of html.matchAll(/id="([^"]+)"/g)) {
  assert(!elements[match[1]], `Duplicate id: ${match[1]}`);
  elements[match[1]] = {
    value: match[1] === 'method' ? 'kmeans' : '', listeners: {}, hidden: false, disabled: false,
    innerHTML: '', textContent: '', attributes: {}, classes: new Set(),
    addEventListener(event, callback) { this.listeners[event] = callback; },
    setAttribute(name, value) { this.attributes[name] = value; },
  };
  const el = elements[match[1]];
  el.classList = {toggle(name, enabled) { if (enabled) el.classes.add(name); else el.classes.delete(name); }};
}
const inputs = data.featureNames.map((_, i) => ({value: String(i), checked: i < 2}));
elements.features.querySelectorAll = selector => selector.includes(':checked') ? inputs.filter(input => input.checked) : inputs;
const timers = new Map();
let nextTimer = 0;
vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'demo.js'), 'utf8'), {
  window: {WINE_DATA: data},
  document: {getElementById(id) { assert(elements[id], `Missing DOM element: ${id}`); return elements[id]; }},
  setInterval(callback) { timers.set(++nextTimer, callback); return nextTimer; },
  clearInterval(id) { timers.delete(id); },
});
const click = id => { assert(!elements[id].disabled, `${id} should be enabled`); elements[id].listeners.click(); };
const change = (id, value) => { elements[id].value = String(value); elements[id].listeners.change(); };
const frame = () => [...timers.values()].forEach(callback => callback());
const assertFinitePlots = () => {
  for (const id of ['plot', 'truthPlot']) {
    assert(!/NaN|undefined|Infinity/.test(elements[id].innerHTML));
    for (const match of elements[id].innerHTML.matchAll(/<circle cx="([^"]+)" cy="([^"]+)"/g)) {
      assert(Number(match[1]) >= 72 && Number(match[1]) <= 528);
      assert(Number(match[2]) >= 46 && Number(match[2]) <= 442);
    }
  }
};
assertFinitePlots();
assert(elements.saveResult.disabled);
click('singleStep');
assert(elements.agreement.textContent.includes('当前'));
click('play'); frame(); click('pause');
assert.equal(timers.size, 0);
assert(elements.status.textContent.includes('暂停'));
click('play'); click('finish');
assert.equal(timers.size, 0);
assert(elements.agreement.textContent.includes('77.0%'));
assert(elements.play.disabled);
click('saveResult'); click('saveResult');
assert.equal((elements.savedRows.innerHTML.match(/<tr>/g) || []).length, 1);
click('reset');
assert(elements.saveResult.disabled);
assert(!elements.savedResults.hidden);
click('allFeatures');
assert(elements.plots.hidden); assert(elements.truthView.hidden);
click('finish'); click('saveResult');
assert.equal((elements.savedRows.innerHTML.match(/<tr>/g) || []).length, 2);
click('defaultFeatures');
inputs[0].checked = false; elements.features.listeners.change();
assert(elements.resultCard.hidden); assert(elements.play.disabled);
inputs[1].checked = false; elements.features.listeners.change();
assert(elements.resultCard.hidden);
// Switch methods with an incomplete attribute selection, then return.
change('method', 'svm'); assert(!elements.resultCard.hidden);
change('method', 'kmeans'); assert(elements.resultCard.hidden);
click('defaultFeatures');
inputs[0].checked = false; inputs[12].checked = true; elements.features.listeners.change();
click('finish'); assertFinitePlots();
assert(elements.plot.innerHTML.includes('脯氨酸'));
for (const mode of ['pca', 'svm']) {
  change('method', mode);
  for (let dimensions = 2; dimensions <= 13; dimensions++) {
    change('components', dimensions);
    assert.equal(elements.plots.hidden, dimensions > 2);
    assert.equal(elements.animationControls.hidden, dimensions > 2);
    assert.equal(elements.svmResults.hidden, mode !== 'svm');
    assert(!/NaN|undefined/.test(elements.variance.textContent));
    if (dimensions === 2) {
      click('play'); frame(); click('pause'); assert.equal(timers.size, 0);
      click('singleStep'); click('finish'); assertFinitePlots();
      click('reset'); click('play');
      for (let i = 0; i < 25; i++) frame();
      assert.equal(timers.size, 0); assert(elements.play.disabled);
    }
    click('saveResult');
  }
}
change('components', 2); click('play');
change('components', 13); assert.equal(timers.size, 0);
change('method', 'kmeans'); assert(!elements.plots.hidden);
click('clearSaved'); assert(elements.savedResults.hidden);
console.log('PASS: 2–13D calculations, plot bounds, playback, pause, single step, finish, reset, invalid selections, mode changes and saved comparisons.');
