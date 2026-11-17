# BaZi around midnight · a reproducible Four Pillars case

A fictional birth-time range in New York shows how a midnight boundary can affect a BaZi chart. For February 4–5, 1994, from 23:40 to 00:10 local time, the year and month pillars stayed consistent in all five Bazi Diff settings. The day and hour pillars had two possible values each. At 00:10 all five settings gave Ren (Yang Water) as the Day Master.

[Run the exact example in Bazi Diff](https://bazi-diff.pages.dev/chart/?time=range&example=range&utm_source=github_case&utm_medium=reference&utm_campaign=midnight_case#compare). You can open **See the checks for 3 time windows** to reproduce the table.

[Download the 22-second video walkthrough](https://github.com/chilayt/bazi-midnight-case/releases/download/midnight-demo-v1/Bazi-Diff-Birth-Time-Demo.mp4).

[Read the work-style interpretation of this same case](https://bazi-diff.pages.dev/guides/bazi-career-reading/?utm_source=github_case&utm_medium=reference&utm_campaign=career_reading#rough-time), or [read it in Chinese](https://bazi-diff.pages.dev/guides/bazi-career-reading/zh-hans/?utm_source=github_case&utm_medium=reference&utm_campaign=career_reading#rough-time). The month stem stays fixed. A change in the Day Master changes how the two stems relate and which work prompt the tool shows.

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


### Why the solar clocks differ in this case

With both calculators set to longitude 74° west and UTC−05:00, the pinned BaZi Atlas engine applies a +4-minute longitude correction. For this example, Bazi Diff also applies an estimated equation-of-time correction of about −13 minutes 41 seconds, bringing its total shift to −9 minutes 41 seconds. The [U.S. Naval Observatory explains the distinction between mean and apparent solar time](https://aa.usno.navy.mil/faq/eqtime).

| Recorded local time on Feb 5 | BaZi Atlas mean solar time | Bazi Diff estimated apparent solar time | Atlas midnight-rule day pillar | Bazi Diff Late Zi with midnight day change |
| --- | --- | --- | --- | --- |
| 00:00 | Feb 5 00:04 | Feb 4 23:50:19 | 壬戌 | 辛酉 |
| 00:09 | Feb 5 00:13 | Feb 4 23:59:19 | 壬戌 | 辛酉 |
| 00:10 | Feb 5 00:14 | Feb 5 00:00:19 | 壬戌 | 壬戌 |

Run `node compare-bazi-atlas.mjs ../bazi-engine/engine.mjs --mean-solar` for the Atlas outputs. To inspect the Bazi Diff result, open the example above and expand the rule checks. With the **23:00** day rollover both calculators give 壬戌 at the three times in the table.

## Cross-check with Jade Almanac's public dataset

[Jade Almanac's BaZi convention audit v1.2.1](https://jadealmanac.com/bazi-calculator/conventions) includes two published CC0 clock-field probes for June 15, 1990. We ran the same clock fields through two Bazi Diff day-change settings with solar correction off and an explicit UTC+08:00 test offset. The offset is used here to isolate the rollover comparison.

| Probe | Clock fields | Bazi Diff midnight switch | Bazi Diff 23:00 switch | Published Jade Almanac result |
| --- | --- | --- | --- | --- |
| B2, control | 22:30 | 辛亥, Xin | 辛亥, Xin | 辛亥, Xin |
| B1, late Zi | 23:30 | 辛亥, Xin | 壬子, Ren | 壬子, Ren |

These rows compare day pillars from fixed clock fields. The audit's Jade Almanac observations used its no-city path. A real birth in Beijing on that date requires historical daylight-saving handling. The separate New York example above compares a date-crossing interval under five settings.

Run `node compare-jade-almanac.mjs` on Node.js 18 or later. It checks the dataset version and hashes of the deployed Bazi Diff code before printing the two rows.

## Independent civil-date check with sxtwl

[sxtwl](https://github.com/yuangu/sxtwl_cpp) 2.0.7 returns 辛酉 for February 4, 1994 and 壬戌 for February 5. At 23:40 on the local clock, midnight rollover selects February 4 for the day pillar. A 23:00 rollover selects February 5. The script calculates the civil-date pillars. Selecting which date to use is a separate BaZi convention. This check covers the day pillar only.

```sh
python -m pip install sxtwl==2.0.7
python verify-civil-day-pillars.py
```

## 中文说明

这是一个可复算的虚构案例。地点为纽约，当地时间从 1994 年 2 月 4 日 23:40 到 2 月 5 日 00:10。五种设置在整个时段给出的年柱和月柱一致，分别为甲戌和丙寅。日柱和时柱各有两种可能。到 00:10，五种设置的日主都为壬。上表和附带 JSON 记录了三个时间窗口各自的结果。

寿星天文历 sxtwl 2.0.7 独立复核了公历 2 月 4 日为辛酉、2 月 5 日为壬戌。若当地钟表是 23:40，午夜换日取前者，23:00 换日取后者。脚本可复算两个公历日期的日干支。

欢迎用自己的排盘工具复算这个虚构案例，并在[公开试用帖](https://github.com/chilayt/bazi-midnight-case/issues/1)分享所用的规则和结果。可以附上工具版本、钟表时间或太阳时口径，以及换日界线。

[不知道出生时辰怎么排八字？阅读中文指南](https://bazi-diff.pages.dev/guides/bazi-without-exact-birth-time/zh-hans/?utm_source=github_case&utm_medium=reference&utm_campaign=unknown_birth_time_zh)

### 同一张盘，为什么会有两条工作解读？

这个时段的月干都是丙。日干为辛时，月干相对日干为正官，解读会问明确的职责怎样影响你的工作。日干为壬时，这个关系变成偏财，解读会问你是否更喜欢成果可衡量的工作。[打开中文试算，查看两条解读和盘面依据](https://bazi-diff.pages.dev/chart/?time=range&example=range&reading=zh&utm_source=github_case&utm_medium=reference&utm_campaign=career_reading_zh#compare)。
