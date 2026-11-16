import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const enginePath = process.argv[2];
if (!enginePath) {
  console.error("Usage: node compare-bazi-atlas.mjs /path/to/bazi-engine/engine.mjs");
  process.exit(1);
}

const { computeBazi } = await import(pathToFileURL(resolve(enginePath)).href);
const startLocal = Date.UTC(1994, 1, 4, 23, 40);

for (let minuteOffset = 0; minuteOffset <= 30; minuteOffset++) {
  // Use UTC methods to enumerate local clock labels without the host time zone.
  const clock = new Date(startLocal + minuteOffset * 60_000);
  const input = {
    year: clock.getUTCFullYear(),
    month: clock.getUTCMonth() + 1,
    day: clock.getUTCDate(),
    hour: clock.getUTCHours(),
    minute: clock.getUTCMinutes(),
    tzOffsetHours: -5,
    longitude: null,
  };

  const settings = [1, 2].map((sect) => {
    const { pillars, meta } = computeBazi({ ...input, sect });
    return {
      sect,
      pillars: [pillars.year, pillars.month, pillars.day, pillars.time].map((pillar) => pillar.ganzhi),
      dayMaster: meta.dayMaster,
    };
  });
  console.log(JSON.stringify({ local: clock.toISOString().slice(0, 16), settings }));
}
