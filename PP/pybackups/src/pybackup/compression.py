import fnmatch
import tarfile
import zipfile
from pathlib import Path
from typing import Literal


def _excluded(path: Path, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path.name, p) for p in patterns)


def create_archive(
    sources: list[Path],
    output: Path,
    *,
    format: Literal["zip", "tar.gz", "tar.bz2"],
    level: int = 6,
    exclude_patterns: list[str] | None = None,
) -> None:
    exclude = exclude_patterns or []

    if format == "zip":
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=level) as zf:
            for src in sources:
                if src.is_file() and not _excluded(src, exclude):
                    zf.write(src, src.name)
                elif src.is_dir():
                    for f in src.rglob("*"):
                        if f.is_file() and not _excluded(f, exclude):
                            zf.write(f, f.relative_to(src.parent))
    else:
        mode = "w:gz" if format == "tar.gz" else "w:bz2"
        with tarfile.open(output, mode, compresslevel=level) as tf:
            for src in sources:
                if src.is_file() and not _excluded(src, exclude):
                    tf.add(src, arcname=src.name)
                elif src.is_dir():
                    tf.add(src, arcname=src.name, filter=lambda i: None if _excluded(Path(i.name), exclude) else i)


def create_archive_from_files(
    files: list[Path],
    source_roots: list[Path],
    output: Path,
    *,
    format: Literal["zip", "tar.gz", "tar.bz2"],
    level: int = 6,
) -> None:
    def arcname(f: Path) -> str:
        for root in source_roots:
            try:
                return str(f.relative_to(root.parent))
            except ValueError:
                pass
        return f.name

    if format == "zip":
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=level) as zf:
            for f in files:
                zf.write(f, arcname(f))
    else:
        mode = "w:gz" if format == "tar.gz" else "w:bz2"
        with tarfile.open(output, mode, compresslevel=level) as tf:
            for f in files:
                tf.add(f, arcname=arcname(f))


def extract_archive(archive: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    if archive.name.endswith(".zip"):
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(dest)
    elif ".tar" in archive.name:
        with tarfile.open(archive) as tf:
            tf.extractall(dest)
    else:
        raise ValueError(f"unknown archive format: {archive}")
