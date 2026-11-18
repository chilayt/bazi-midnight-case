#!/usr/bin/env python3
"""Compare America/Vancouver local-time behaviour between two downloaded tzdata wheels.

Each wheel is read directly with zipfile.ZipFile; the zone file is turned into a
standalone ZoneInfo via ZoneInfo.from_file(BytesIO(...)).  The interpreter's
time-zone settings are never changed and the system zone database is never
consulted, so the two wheels are compared in complete isolation.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE_NAME = "America/Vancouver"
ZONE_MEMBER = "tzdata/zoneinfo/America/Vancouver"
ZI_MEMBER = "tzdata/zoneinfo/tzdata.zi"

UTC_CASES = (
    "2000-01-15T20:00Z",
    "2026-03-08T09:59Z",
    "2026-03-08T10:00Z",
    "2026-11-01T09:30Z",
)
LOCAL_CASES = (
    "2026-03-08T02:30",
    "2026-11-01T01:30",
)


def read_zone(wheel_path: Path) -> tuple[ZoneInfo, str | None]:
    """Load the zone and its IANA version directly from a tzdata wheel."""
    try:
        with zipfile.ZipFile(wheel_path) as archive:
            zone_bytes = archive.read(ZONE_MEMBER)
            version = None
            if ZI_MEMBER in archive.namelist():
                first_line = archive.read(ZI_MEMBER).split(b"\n", 1)[0]
                parts = first_line.decode("ascii", "replace").split()
                if len(parts) >= 3 and parts[:2] == ["#", "version"]:
                    version = parts[2]
        return ZoneInfo.from_file(BytesIO(zone_bytes), key=ZONE_NAME), version
    except (OSError, zipfile.BadZipFile, KeyError, ValueError) as exc:
        raise ValueError(f"{wheel_path.name}: {exc}") from exc

def utc_to_local(zone: ZoneInfo, case: str) -> str:
    """Format one UTC case as local ISO time with UTC offset."""
    naive = datetime.strptime(case[:-1], "%Y-%m-%dT%H:%M")
    moment = naive.replace(tzinfo=timezone.utc)
    return moment.astimezone(zone).isoformat()


def local_to_utc(zone: ZoneInfo, case: str) -> dict:
    """Resolve one naive local case by trying fold 0 and fold 1.

    A candidate survives only when converting it to UTC and back reproduces the
    same wall clock.  Surviving candidates are de-duplicated and sorted, which
    separates skipped times (none), unique times (one) and repeated times (two).
    """
    naive = datetime.strptime(case, "%Y-%m-%dT%H:%M")
    moments = set()
    for fold in (0, 1):
        aware = naive.replace(tzinfo=zone, fold=fold)
        moment = aware.astimezone(timezone.utc)
        if moment.astimezone(zone).replace(tzinfo=None) == naive:
            moments.add(moment)
    ordered = sorted(moments)
    if not ordered:
        kind = "skipped"
    elif len(ordered) == 1:
        kind = "unique"
    else:
        kind = "repeated"
    return {
        "kind": kind,
        "utc_candidates": [m.strftime("%Y-%m-%dT%H:%M:%SZ") for m in ordered],
    }


def analyze(wheel_path: Path) -> dict:
    """Collect the zone report for a single wheel."""
    zone, version = read_zone(wheel_path)
    return {
        "wheel": wheel_path.name,
        "iana_version": version,
        "utc_to_local": {case: utc_to_local(zone, case) for case in UTC_CASES},
        "local_to_utc": {case: local_to_utc(zone, case) for case in LOCAL_CASES},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("old_wheel", type=Path, help="older tzdata wheel")
    parser.add_argument("new_wheel", type=Path, help="newer tzdata wheel")
    args = parser.parse_args(argv)
    try:
        report = {
            "old": analyze(args.old_wheel),
            "new": analyze(args.new_wheel),
        }
    except ValueError as exc:
        parser.error(str(exc))
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
