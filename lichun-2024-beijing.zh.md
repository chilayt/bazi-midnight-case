# 2024 年立春，北京三个排盘时刻复算

比较同一天的三个虚构出生时刻。固定北京当地钟表时间（UTC+08:00），关闭真太阳时修正，分别按节气日期和交节时刻取年柱、月柱。

| 北京时间 | 按节气日期 | 按交节时刻 | 日柱、时柱 |
| --- | --- | --- | --- |
| 2 月 4 日 00:00 | 甲辰年、丙寅月 | 癸卯年、乙丑月 | 戊戌、壬子 |
| 2 月 4 日 16:26 | 甲辰年、丙寅月 | 癸卯年、乙丑月 | 戊戌、庚申 |
| 2 月 4 日 16:28 | 甲辰年、丙寅月 | 甲辰年、丙寅月 | 戊戌、庚申 |

[下载三个用例的 CSV](lichun-2024-beijing.csv)。

## 在浏览器复跑

1. 打开 [Bazi Diff 中文立春算例](https://bazi-diff.pages.dev/chart/zh-hans/?example=solar-term&utm_source=github_case&utm_medium=reference&utm_campaign=lichun_2024#comparison)，展开「查看英文排盘规则对照」。
2. 第 1、2 列以节气日期取年、月柱，第 3 列以交节时刻取年、月柱。要比较 16:26 与 16:28，填入对应时刻、关闭真太阳时，再排一次。
3. 用 [中文对照指南](https://bazi-diff.pages.dev/guides/why-bazi-calculators-disagree/zh-hans/?utm_source=github_case&utm_medium=reference&utm_campaign=lichun_2024#solar-term) 查看其他柱变化时应核对的设置。

## 对照来源

- [紫金山天文台 2024 年日历资料](https://pmo.cas.cn/xwdt2019/kpdt2019/202203/P020240201504888053250.pdf) 公布立春为 2 月 4 日北京时间 16:27，精确到分钟。
- [Open-Bazi 固定版本](https://github.com/Filtain/open-bazi/tree/427ff01868a10da3387345a1b0c401f7bb1db0a2) 的默认标准时间口径使用 lunar-python 1.4.9。在本机输入这三个公历时刻，四柱均与 Bazi Diff 的交节时刻列一致。两个历法实现来自同一工具库家族。
- 寿星天文历 sxtwl 2.0.7 返回约 16:26:53，lunar-python 返回 16:27:07。两者结果都落在 16:26:00 与 16:28:00 之间。这两个分钟输入适合验证换柱前后，秒级交界会受所用历表影响。
