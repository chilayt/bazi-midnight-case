"""Reproduce the midnight example's civil-date pillars with sxtwl 2.0.7."""

from datetime import date, timedelta
from importlib.metadata import version

import sxtwl


STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"


def day_pillar(civil_date):
    day = sxtwl.fromSolar(civil_date.year, civil_date.month, civil_date.day)
    gan_zhi = day.getDayGZ()
    return STEMS[gan_zhi.tg] + BRANCHES[gan_zhi.dz]


if __name__ == "__main__":
    if version("sxtwl") != "2.0.7":
        raise SystemExit("Install the recorded version: python -m pip install sxtwl==2.0.7")
    civil_date = date(1994, 2, 4)
    next_date = civil_date + timedelta(days=1)
    actual = (day_pillar(civil_date), day_pillar(next_date))
    if actual != ("辛酉", "壬戌"):
        raise SystemExit(f"Unexpected day pillars: {actual}")
    print(f"{civil_date} {actual[0]}")
    print(f"{next_date} {actual[1]}")
