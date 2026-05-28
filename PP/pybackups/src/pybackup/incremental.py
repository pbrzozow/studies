from __future__ import annotations

import fnmatch
import hashlib
from pathlib import Path

from .models import BackupManifest, FileRecord


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def load_manifest(path: Path) -> BackupManifest:
    if path.exists():
        return BackupManifest.model_validate_json(path.read_text(encoding="utf-8"))
    return BackupManifest()


def save_manifest(manifest: BackupManifest, path: Path) -> None:
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")


def collect_changed_files(
    sources: list[Path],
    manifest: BackupManifest,
    exclude_patterns: list[str],
) -> tuple[list[Path], BackupManifest]:
    new_manifest = BackupManifest()
    changed: list[Path] = []

    def excluded(p: Path) -> bool:
        return any(fnmatch.fnmatch(p.name, pat) for pat in exclude_patterns)

    for source in sources:
        files = [source] if source.is_file() else [f for f in source.rglob("*") if f.is_file()]
        for f in files:
            if excluded(f):
                continue

            stat = f.stat()
            key = str(f.resolve())
            prev = manifest.files.get(key)

            if prev and prev.mtime == stat.st_mtime and prev.size == stat.st_size:
                new_manifest.files[key] = prev
                continue

            digest = _sha256(f)
            if prev is None or prev.sha256 != digest:
                changed.append(f)

            new_manifest.files[key] = FileRecord(size=stat.st_size, mtime=stat.st_mtime, sha256=digest)

    return changed, new_manifest
