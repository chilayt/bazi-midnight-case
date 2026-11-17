# 紫微斗数夫妻宫在不同出生时辰下怎么变

用同一个虚构日期比较四组时辰，查看夫妻宫所在的地支和主星。结果来自 iztro 2.6.5。地支与星名是排盘规则的输出，盘面比较不评估两人的关系结果。

采用公历、出生地钟表时辰、晚子时按当日、启用闰月修正、女。四条记录均为虚构输入。

| 公历日期 | 当地钟表时间 | iztro timeIndex | 农历日 | 夫妻宫地支 | 主星 |
| --- | --- | ---: | --- | --- | --- |
| 1990-06-15 | 01:00–02:59 | 1 | 五月廿三 | 卯 | 太阳、天梁 |
| 1990-06-15 | 11:00–12:59 | 6 | 五月廿三 | 戌 | 破军 |
| 1990-06-15 | 23:00–23:59 | 12 | 五月廿三 | 辰 | 武曲 |
| 1990-06-16 | 00:00–00:59 | 0 | 五月廿四 | 辰 | 天同 |

只改变同一天的时辰，丑时与午时的宫位、主星都不同。跨过午夜的两条记录地支同为辰，主星有变化。比对两个工具时，先记下公历或农历输入、时辰和所用的换日规则，再核对宫位和主星。

## 在网页上复算

[直接跑午时算例](https://bazi-diff.pages.dev/tools/ziwei/?example=demo&utm_source=github_case&utm_medium=reference&utm_campaign=ziwei_palace_case#ziwei-result)。在结果中展开 **从夫妻宫看关系**，也可以在十二宫列表里找到同一个宫位。也可以[直接跑丑时算例](https://bazi-diff.pages.dev/tools/ziwei/?example=early&utm_source=github_case&utm_medium=reference&utm_campaign=ziwei_palace_case#ziwei-result)。剩下两组可在[空白排盘](https://bazi-diff.pages.dev/tools/ziwei/?utm_source=github_case&utm_medium=reference&utm_campaign=ziwei_palace_case)中按表输入。

## 用 Node.js 复算

在空目录安装指定版本，保存下方代码为 `check.cjs`，运行 `node check.cjs`。

```sh
npm install --save-exact iztro@2.6.5
```

```js
const { astro, version } = require("iztro");
console.log(version);

const inputs = [
  ["1990-06-15", 1],
  ["1990-06-15", 6],
  ["1990-06-15", 12],
  ["1990-06-16", 0],
];

for (const [dateStr, timeIndex] of inputs) {
  const chart = astro.withOptions({
    type: "solar",
    dateStr,
    timeIndex,
    gender: "female",
    fixLeap: true,
    language: "zh-CN",
    config: { dayDivide: "current" },
  });
  const palace = chart.palace("夫妻");
  const stars = palace.majorStars.map(star => star.name).join("、") || "无主星";
  console.log(dateStr, timeIndex, chart.lunarDate, palace.earthlyBranch, stars);
}
```

[iztro 快速开始](https://docs.iztro.com/quick-start) · [十二宫资料](https://docs.iztro.com/posts/palace) · [v2.6.5 发行版](https://github.com/SylarLong/iztro/releases/tag/v2.6.5)
