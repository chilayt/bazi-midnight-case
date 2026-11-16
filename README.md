# BaZi around midnight · a reproducible Four Pillars case

A fictional birth-time range in New York shows how a midnight boundary can affect a BaZi chart. For February 4–5, 1994, from 23:40 to 00:10 local time, the year and month pillars stayed consistent in all five Bazi Diff settings. The day and hour pillars had two possible values each. At 00:10 all five settings gave Ren (Yang Water) as the Day Master.

[Run the exact example in Bazi Diff](https://bazi-diff.pages.dev/chart/?time=range&example=range&utm_source=github_case&utm_medium=reference&utm_campaign=midnight_case#compare). You can open **See the checks for 3 time windows** to reproduce the table.

[Download the 22-second video walkthrough](https://github.com/chilayt/bazi-midnight-case/releases/download/midnight-demo-v1/Bazi-Diff-Birth-Time-Demo.mp4).

## Inputs and expected outputs

- Birth city and clock: New York, local civil time (UTC−05:00).
- Interval: 1994-02-04 23:40 through 1994-02-05 00:10, inclusive, at one-minute resolution.
- Stable pillars: 甲戌 (Yang Wood Dog) for the year and 丙寅 (Yang Fire Tiger) for the month.
- The Day Master is the Heavenly Stem of the day pillar.

| Local time | Xin (辛, Yin Metal) | Ren (壬, Yang Water) |
| --- | --- | --- |
| Feb 4, 23:40–23:59 | Almanac midnight; Late Zi with midnight day change | Early Zi; Exact solar terms; True solar time |
| Feb 5, 00:00–00:09 | Late Zi with midnight day change | Almanac midnight; Early Zi; Exact solar terms; True solar time |
| Feb 5, 00:10 | — | All five settings above |

The setting names are the labels Bazi Diff displays. Other tools may package their rules differently. Agreement is specific to the input interval and settings checked. The example is fictional and contains no personal birth data. See the [rule comparison guide](https://bazi-diff.pages.dev/guides/why-bazi-calculators-disagree/) for the related clock and day-change conventions.

If you maintain a BaZi tool, can you reproduce this input and share the rule labels, software version, clock basis and day-change convention you used? Which setting would you document first to make differences easier to explain? [Share your observations in the open trial](https://github.com/chilayt/bazi-midnight-case/issues/1) using just the fictional inputs.

## Cross-check with BaZi Atlas

[BaZi Atlas](https://github.com/bazi-atlas/bazi-engine/tree/d494d532cf2f71eb716571956b10255021c24b33) was run with New York local clock fields, an explicit UTC−05:00 offset and solar-time adjustment off. This uses the engine's two documented day-switch settings.

| Local clock | BaZi Atlas 23:00 switch (sect 1) | BaZi Atlas midnight switch (sect 2) |
| --- | --- | --- |
| Feb 4, 23:40–23:59 | 壬戌, Ren | 辛酉, Xin |
| Feb 5, 00:00–00:10 | 壬戌, Ren | 壬戌, Ren |

Those two switches agree from 00:00 in BaZi Atlas. The five-setting Bazi Diff example above includes a setting that still gives Xin through 00:09. The tools share a lunar-javascript dependency. The comparison shows how the selected settings affect this case.

Clone the linked engine, check out `d494d532cf2f71eb716571956b10255021c24b33`, and run `npm ci --ignore-scripts` in that checkout. From this case repository, run the script with the path to the engine entry point:

```sh
node compare-bazi-atlas.mjs ../bazi-engine/engine.mjs
```

The script prints one JSON row per local minute. Each row includes the four pillars and Day Master for both settings.


## 中文说明

这是一个可复算的虚构案例。地点为纽约，当地时间从 1994 年 2 月 4 日 23:40 到 2 月 5 日 00:10。五种设置在整个时段给出的年柱和月柱一致，分别为甲戌和丙寅。日柱和时柱各有两种可能。到 00:10，五种设置的日主都为壬。上表和附带 JSON 记录了三个时间窗口各自的结果。

欢迎用自己的排盘工具复算这个虚构案例，并在[公开试用帖](https://github.com/chilayt/bazi-midnight-case/issues/1)分享所用的规则和结果。可以附上工具版本、钟表时间或太阳时口径，以及换日界线。

[不知道出生时辰怎么排八字？阅读中文指南](https://bazi-diff.pages.dev/guides/bazi-without-exact-birth-time/zh-hans/?utm_source=github_case&utm_medium=reference&utm_campaign=unknown_birth_time_zh)
