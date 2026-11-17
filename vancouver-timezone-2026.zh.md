# 如何测试浏览器是否还在给温哥华拨回冬令时

2026 年 11 月 1 日，温哥华不再把钟拨回一小时。但在一台带旧时区数据的 Node.js 上，把当天的 `09:30 UTC` 转为温哥华时间，仍然会得到 `01:30 UTC−08:00`。按当地现行规则，那一刻应该是 `02:30 UTC−07:00`。预约、日程和历史记录工具只要依赖本机时区数据，都可能遇到这类版本差异。

## 用四个 UTC 时刻检查运行环境

下面的脚本可以在浏览器控制台或 Node.js 中运行。输入统一用带 `Z` 的 UTC 时刻，输出显式指定 `America/Vancouver`，因此测试不依赖设备当前时区。

```js
const formatter = new Intl.DateTimeFormat("en-GB", {
  timeZone: "America/Vancouver",
  hour: "2-digit",
  minute: "2-digit",
  timeZoneName: "longOffset",
});

for (const instant of [
  "2000-01-15T20:00:00Z",
  "2026-03-08T09:59:00Z",
  "2026-03-08T10:00:00Z",
  "2026-11-01T09:30:00Z",
]) {
  console.log(instant, formatter.format(new Date(instant)));
}
```

| UTC 输入 | 预期温哥华时间 | Node.js v25.2.1 / tzdb 2025b 实测 |
| --- | --- | --- |
| 2000-01-15 20:00 | 12:00 UTC−08:00 | 12:00 UTC−08:00 |
| 2026-03-08 09:59 | 01:59 UTC−08:00 | 01:59 UTC−08:00 |
| 2026-03-08 10:00 | 03:00 UTC−07:00 | 03:00 UTC−07:00 |
| 2026-11-01 09:30 | 02:30 UTC−07:00 | 01:30 UTC−08:00 |

前 3 行验证历史冬令时和春季跳时仍正常。最后一行才会区分运行时是否应用了这次变更。Node.js 可用 `process.versions.tz` 查看打包的时区数据版本。在提供浏览器端工具时，直接测试固定时刻的输出也能核对实际行为。

卑诗省公布 3 月 8 日为最后一次拨钟，11 月 1 日延续 UTC−07:00。IANA 在 2026b 中记录了此次变更。法律生效时间和 IANA 为兼容 CLDR、ICU 而采用的建模日期有区别。测试上表用的是可观察的当地钟表时间和 UTC 偏移。 [卑诗省公告](https://archive.news.gov.bc.ca/releases/news_releases_2024-2028/2026AG0013-000209.htm) · [IANA tzdb 变更记录](https://data.iana.org/time-zones/tzdb/NEWS)

## 在填写当地时间的工具里复查

转换的反方向也值得测。输入温哥华当地 `2026-11-01 01:30`，旧规则会把它视作重复时刻，给出两个可能的 UTC 偏移。现行规则只对应 `08:30 UTC`，此时偏移是 UTC−07:00。3 月 8 日当地 `02:30` 则在向前拨钟时被跳过。

Bazi Diff 用出生地的当地钟表时间排盘。在正式站选择 **Vancouver**，输入虚构日期 **2026-11-01 01:30**，可以看到 UTC−07:00，也不会出现选择重复时刻的提示。把输入改成 **2000-01-15 12:00**，页面仍显示当时的 UTC−08:00。日常维护时，在固定输入上分别验证「一对一」「重复」和「跳过」三种情形，比只核对今天的偏移更容易发现回归。 [用排盘表单复查](https://bazi-diff.pages.dev/chart/?utm_source=github_case&utm_medium=reference&utm_campaign=vancouver_timezone#compare)
