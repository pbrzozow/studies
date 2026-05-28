from __future__ import annotations

import tempfile
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from .compression import create_archive, create_archive_from_files, extract_archive
from .crypto import decrypt_file, encrypt_file, load_fernet
from .incremental import collect_changed_files, load_manifest, save_manifest
from .models import BackupJobConfig
from .retention import apply_retention

console = Console()


def _fmt_size(n: int) -> str:
    if n >= 1 << 20:
        return f"{n / (1 << 20):.2f} MB"
    if n >= 1 << 10:
        return f"{n / (1 << 10):.1f} KB"
    return f"{n} B"


def run_backup(config: BackupJobConfig) -> Path | None:
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    archive_name = f"{config.name}_{ts}.{config.compression.format}"
    sources = config.source.paths
    exclude = config.source.exclude_patterns

    if config.incremental.enabled:
        console.print("[bold cyan]Incremental[/] — scanning for changes…")
        manifest = load_manifest(config.incremental.manifest_path)
        changed, new_manifest = collect_changed_files(sources, manifest, exclude)
        if not changed:
            console.print("[green]✓ No changes — skipping.[/]")
            return None
        console.print(f"  [cyan]{len(changed)}[/] file(s) changed")
    else:
        changed = []
        new_manifest = None

    with tempfile.TemporaryDirectory() as _tmp:
        tmp = Path(_tmp)
        archive_path = tmp / archive_name

        with Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn(), TimeElapsedColumn(), console=console, transient=True) as p:
            task = p.add_task(f"[cyan]Compressing → {archive_name}", total=None)
            if changed:
                create_archive_from_files(changed, sources, archive_path, format=config.compression.format, level=config.compression.level)
            else:
                create_archive(sources, archive_path, format=config.compression.format, level=config.compression.level, exclude_patterns=exclude)
            p.update(task, description="[green]Done ✓")

        console.print(f"[bold]Archive[/]: {archive_name} ({_fmt_size(archive_path.stat().st_size)})")

        final = archive_path
        if config.encryption.enabled:
            enc_path = tmp / (archive_name + ".enc")
            with Progress(SpinnerColumn(), TextColumn("{task.description}"), transient=True, console=console) as p:
                task = p.add_task("[cyan]Encrypting…", total=None)
                encrypt_file(archive_path, enc_path, load_fernet(config.encryption.key_file))  # type: ignore[arg-type]
                p.update(task, description="[green]Done ✓")
            final = enc_path

        output = config.destination / final.name
        output.write_bytes(final.read_bytes())

    console.print(f"[bold green]✓ Saved[/]: {output} ({_fmt_size(output.stat().st_size)})")

    if config.incremental.enabled and new_manifest is not None:
        save_manifest(new_manifest, config.incremental.manifest_path)

    ret = config.retention
    if ret.max_backups or ret.max_age_days:
        deleted = apply_retention(config.destination, config.name, max_backups=ret.max_backups, max_age_days=ret.max_age_days)
        if deleted:
            console.print(f"[yellow]Retention:[/] removed {len(deleted)} old backup(s)")

    return output


def run_restore(backup_path: Path, dest: Path, key_file: Path | None = None) -> None:
    with tempfile.TemporaryDirectory() as _tmp:
        tmp = Path(_tmp)
        archive = backup_path

        if backup_path.suffix == ".enc":
            if key_file is None:
                raise ValueError("encrypted backup requires --key-file")
            archive = tmp / backup_path.stem
            console.print("[cyan]Decrypting…[/]")
            decrypt_file(backup_path, archive, load_fernet(key_file))

        console.print(f"[cyan]Extracting →[/] {dest}")
        extract_archive(archive, dest)

    console.print(f"[bold green]✓ Restore complete[/]: {dest}")
