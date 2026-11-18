# 农历闰月生日怎么核对紫微排盘

[English](#english)

用一个虚构生日核对两步。先确定农历换算后的公历日期，再复算紫微命盘。这个算例把**农历 2017 年闰六月三十**换成**公历 2017 年 8 月 21 日**。当年的普通六月只有 29 天，闰六月有 30 天。香港天文台日历里，7 月 22 日是前一个六月的二十九，次日开始第二个六月，8 月 21 日是这个月的三十。 [香港天文台 2017 年公农历对照](https://www.hko.gov.hk/en/gts/time/calendar/text/files/T2017e.txt)

1. 打开八字页的农历换算。输入 `2017`、`6`、`30`，勾选「闰月」，确认换算结果为 `2017-08-21`。 [打开农历换算](https://bazi-diff.pages.dev/chart/zh-hans/?utm_source=github_case&utm_medium=reference&utm_campaign=ziwei_leap_month_zh#lunar-birthday)
2. 打开紫微排盘，填入公历 `2017-08-21`。这个虚构算例选择午时 `11:00–12:59` 和女命。 [打开中文紫微排盘](https://bazi-diff.pages.dev/tools/ziwei/?utm_source=github_case&utm_medium=reference&utm_campaign=ziwei_leap_month_zh#ziwei-form)
3. 在 Bazi Diff 的排盘设置下，命盘摘要会显示二〇一七年闰六月三十，十二宫中命宫在寅，官禄宫在午，有天同、太阴。可以用下面的代码核对。

旧版 `iztro` 直接从这组农历数据排盘会先按普通六月检查天数，得到只有 29 天的错误。上游在 `lunar-lite` 合并了先选择闰月再校验的修正。本文的复算路径先确定公历日期，再用站点现有紫微计算设置排盘。 [上游问题](https://github.com/SylarLong/iztro/issues/320) · [已合并修复](https://github.com/SylarLong/lunar-lite/pull/1)

## English

The fictional Chinese lunar date **day 30 of the leap sixth month in 2017** converts to **August 21, 2017**. The regular sixth month has 29 days and the leap sixth month has 30. The calendar records day 29 on July 22, another sixth month starting July 23, and day 30 on August 21. [Hong Kong Observatory calendar](https://www.hko.gov.hk/en/gts/time/calendar/text/files/T2017e.txt)

1. Open the lunar birthday converter. Enter `2017`, `6`, and `30`, select **Leap month**, and check that the result is `2017-08-21`. [Open the BaZi date converter](https://bazi-diff.pages.dev/chart/?utm_source=github_case&utm_medium=reference&utm_campaign=ziwei_leap_month_en#lunar-birthday)
2. Use `2017-08-21` in the Zi Wei chart. For the fictional trial, select the Horse hour `11:00–12:59` and the female setting. [Open the English Zi Wei chart](https://bazi-diff.pages.dev/tools/ziwei/en/?utm_source=github_case&utm_medium=reference&utm_campaign=ziwei_leap_month_en#ziwei-form)
3. With the settings used by Bazi Diff, the result has twelve palaces. The Life Palace sits at Yin and the Career Palace at Wu with Tian Tong and Tai Yin.

## Node.js 复算

Save the released [calendar script](https://bazi-diff.pages.dev/lunar.js) as `lunar.js` and the released [iztro bundle](https://bazi-diff.pages.dev/tools/ziwei/iztro-v2.6.5.min.js) as `iztro-v2.6.5.min.js`. Save the snippet alongside them and run it with Node.js.

```js
const assert = require('node:assert/strict');
const { Lunar, LunarYear } = require('./lunar.js');
globalThis.self = globalThis;
const { astro } = require('./iztro-v2.6.5.min.js');

const year = LunarYear.fromYear(2017);
assert.equal(year.getMonth(6).getDayCount(), 29);
assert.equal(year.getMonth(-6).getDayCount(), 30);

const date = Lunar.fromYmd(2017, -6, 30).getSolar().toYmd();
assert.equal(date, '2017-08-21');

const chart = astro.withOptions({
  type: 'solar', dateStr: date, timeIndex: 6, gender: 'female',
  fixLeap: true, config: { dayDivide: 'current' },
});
assert.equal(chart.palaces.length, 12);
assert.equal(chart.palaces.find(p => p.name === '命宫').earthlyBranch, '寅');
const career = chart.palaces.find(p => p.name === '官禄');
assert.equal(career.earthlyBranch, '午');
assert.deepEqual(career.majorStars.map(star => star.name), ['天同', '太阴']);
console.log(date, career.earthlyBranch, career.majorStars.map(star => star.name));
```
