import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import vm from 'node:vm';

const deployment = 'https://0d92bc72.bazi-diff.pages.dev';
const source = 'https://jadealmanac.com/bazi-calculator/conventions.json';

async function fetchText(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
  return response.text();
}

const [lunarCode, engineCode, datasetText] = await Promise.all([
  fetchText(`${deployment}/lunar.js`),
  fetchText(`${deployment}/engine.js`),
  fetchText(source),
]);
for (const [code, sha256] of [
  [lunarCode, 'c59cf28934ad45a79e30149042a973fa9461419372ebdc835dcca296fd6aa306'],
  [engineCode, '491c089f0b4f111291257627df5d5d895661b578035b9ad7c261934bb7e4e376'],
]) {
  assert.equal(createHash('sha256').update(code).digest('hex'), sha256);
}
const dataset = JSON.parse(datasetText);
assert.equal(dataset.version, '1.2.1');
const ctx = vm.createContext({});
vm.runInContext(lunarCode, ctx, { filename: 'lunar.js' });
vm.runInContext(engineCode, ctx, { filename: 'engine.js' });
const engine = vm.runInContext('BaziDiff', ctx);

for (const id of ['B2', 'B1']) {
  const probe = dataset.probes.find(row => row.id === id);
  const [year, month, day] = probe.date.split('-').map(Number);
  const [hour, minute] = probe.time.split(':').map(Number);
  // Isolate day rollover with the original bare clock fields. The city
  // satisfies the calculator input. Solar adjustment is off and +08:00
  // is an explicit test offset, independently of historical civil time.
  const { methods } = engine.compare({
    year, month, day, hour, minute, city: probe.place, utcOffsetMinutes: 480,
  }, false);
  const jade = dataset.implementations.find(row => row.id === 'jadealmanac');
  const jadeDay = jade.observations.find(row => row.probe_id === id).pillars_zh.split(' ')[2];
  const [midnight, earlyZi] = methods.map(chart => chart[2]);
  assert.equal(earlyZi, jadeDay);
  assert.equal(midnight, '辛亥');
  console.log(JSON.stringify({ id, date: probe.date, clock: probe.time, midnight, earlyZi, jadeDay }));
}
