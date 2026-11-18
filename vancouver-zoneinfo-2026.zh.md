# 用 Python 的 `zoneinfo` 复查温哥华 2026 年的时区规则

同一个 UTC 时刻，用两版 IANA 时区数据换算，会得到不同的温哥华时间。`2026-11-01 09:30 UTC` 在 `2025c` 里是 `01:30 UTC−08:00`，在 `2026f` 里是 `02:30 UTC−07:00`。卑诗省在 2026 年 3 月完成最后一次拨钟，11 月 1 日维持 UTC−07:00。这个例子可以用来检查预约、记录和排盘工具对历史时区规则的处理。 [卑诗省公告](https://news.gov.bc.ca/releases/2026AG0013-000209) · [IANA 变更记录](https://data.iana.org/time-zones/tzdb/NEWS)

## 在同一个 Python 进程里比较两份数据

直接调用 `ZoneInfo("America/Vancouver")` 时，Python 先查系统的 `TZPATH`，找不到相应时区才读 `tzdata` 包。安装新版 `tzdata` 后，系统时区数据库仍可能优先。下面的 [复算脚本](compare-vancouver-tzdata.py) 用 `ZipFile` 从两个 wheel 中分别读取同一个 TZif 文件，再交给 `ZoneInfo.from_file`。它接受两份本地文件，不改系统设置，也不用安装这两个版本。 [Python zoneinfo 文档](https://docs.python.org/3/library/zoneinfo.html#data-sources)

在仓库目录下运行。脚本使用 Python 3.9 或更高版本的标准库。两次下载命令分别固定一个版本。

```sh
python -m pip download --no-deps --only-binary=:all: --dest wheels tzdata==2025.3
python -m pip download --no-deps --only-binary=:all: --dest wheels tzdata==2026.6
python compare-vancouver-tzdata.py wheels/tzdata-2025.3-py2.py3-none-any.whl wheels/tzdata-2026.6-py2.py3-none-any.whl
```

这两份 wheel 内的 IANA 版本分别是 `2025c` 和 `2026f`。下表只比较当地钟表时间和 UTC 偏移。 [tzdata 2025.3](https://pypi.org/project/tzdata/2025.3/) · [tzdata 2026.6](https://pypi.org/project/tzdata/2026.6/)

| UTC 输入 | tzdata 2025.3 | tzdata 2026.6 |
| --- | --- | --- |
| 2000-01-15 20:00 | 12:00 UTC−08:00 | 12:00 UTC−08:00 |
| 2026-03-08 09:59 | 01:59 UTC−08:00 | 01:59 UTC−08:00 |
| 2026-03-08 10:00 | 03:00 UTC−07:00 | 03:00 UTC−07:00 |
| 2026-11-01 09:30 | 01:30 UTC−08:00 | 02:30 UTC−07:00 |

## 用户填的是当地时间时，用 UTC 往返检验

给一个无时区的 `datetime` 添上 `tzinfo` 后，Python 仍允许它落在被跳过的一小时内。脚本会尝试 `fold=0` 和 `fold=1`，各自换成 UTC，再转回温哥华。只保留能回到原钟表时间的结果，并按 UTC 时刻去重。这样可以区分没有结果、唯一时刻和重复时刻。 [PEP 495 的 fold 说明](https://peps.python.org/pep-0495/)

| 温哥华当地输入 | tzdata 2025.3 的有效 UTC | tzdata 2026.6 的有效 UTC |
| --- | --- | --- |
| 2026-03-08 02:30 | 无 | 无 |
| 2026-11-01 01:30 | 08:30 和 09:30 | 08:30 |

我在维护 Bazi Diff 时遇到了这个问题。网页里的虚构算例填的是第二行的**当地** `01:30`，可直接核对 UTC−07:00 和唯一偏移。文中的 `09:30 UTC` 则用于测试从 UTC 转为当地时间的反方向。 [打开同一温哥华算例](https://bazi-diff.pages.dev/chart/zh-hans/?example=vancouver-clock&utm_source=github_case&utm_medium=reference&utm_campaign=python_zoneinfo_vancouver#comparison) · [用浏览器和 Node.js 复查](vancouver-timezone-2026.zh.md)
