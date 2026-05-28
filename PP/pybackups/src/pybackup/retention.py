from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path

_RE = re.compile(r"^(?P<name>.+?)_(?P<ts>\d{8}T\d{6})\.(?:tar\.gz|tar\.bz2|zip)(?:\.enc)?$")
_FMT = "%Y%m%dT%H%M%S"


def _parse_ts(path: Path) -> datetime | None:
    m = _RE.match(path.name)
    return datetime.strptime(m.group("ts"), _FMT) if m else None


def list_backups(dest: Path, name: str) -> list[tuple[datetime, Path]]:
    result = [(ts, p) for p in dest.iterdir() if p.name.startswith(name + "_") and (ts := _parse_ts(p))]
    result.sort(key=lambda x: x[0])
    return result


def apply_retention(
    dest: Path,
    name: str,
    *,
    max_backups: int | None,
    max_age_days: int | None,
) -> list[Path]:
    backups = list_backups(dest, name)
    to_delete: set[Path] = set()

    if max_backups is not None and len(backups) > max_backups:
        for _, p in backups[:len(backups) - max_backups]:
            to_delete.add(p)

    if max_age_days is not None:
        cutoff = datetime.now() - timedelta(days=max_age_days)
        to_delete.update(p for ts, p in backups if ts < cutoff)

    deleted = sorted(to_delete)
    for p in deleted:
        p.unlink(missing_ok=True)
    return deleted
