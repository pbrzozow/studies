from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from .crypto import generate_key
from .engine import run_backup, run_restore
from .models import (
    BackupJobConfig,
    CompressionConfig,
    EncryptionConfig,
    IncrementalConfig,
    RetentionConfig,
    ScheduleConfig,
    SourceConfig,
)
from .retention import list_backups

app = typer.Typer(name="pybackup", no_args_is_help=True)
console = Console()


def _config(
    name: str,
    sources: list[Path],
    destination: Path,
    exclude: list[str],
    fmt: str,
    level: int,
    encrypt: bool,
    key_file: Optional[Path],
    incremental: bool,
    manifest: Path,
    max_backups: Optional[int],
    max_age_days: Optional[int],
    cron: Optional[str] = None,
) -> BackupJobConfig:
    return BackupJobConfig(
        name=name,
        source=SourceConfig(paths=sources, exclude_patterns=exclude),
        destination=destination,
        compression=CompressionConfig(format=fmt, level=level),  # type: ignore[arg-type]
        encryption=EncryptionConfig(enabled=encrypt, key_file=key_file),
        retention=RetentionConfig(max_backups=max_backups, max_age_days=max_age_days),
        incremental=IncrementalConfig(enabled=incremental, manifest_path=manifest),
        schedule=ScheduleConfig(cron=cron) if cron else None,
    )


@app.command("run")
def cmd_run(
    sources: Annotated[list[Path], typer.Option("--source", "-s")],
    destination: Annotated[Path, typer.Option("--dest", "-d")],
    name: Annotated[str, typer.Option()] = "backup",
    exclude: Annotated[list[str], typer.Option("--exclude", "-e")] = [],
    fmt: Annotated[str, typer.Option("--format", "-f")] = "tar.gz",
    level: Annotated[int, typer.Option("--level")] = 6,
    encrypt: Annotated[bool, typer.Option("--encrypt/--no-encrypt")] = False,
    key_file: Annotated[Optional[Path], typer.Option("--key-file", "-k")] = None,
    incremental: Annotated[bool, typer.Option("--incremental/--full", "-i")] = False,
    manifest: Annotated[Path, typer.Option()] = Path(".pybackup_manifest.json"),
    max_backups: Annotated[Optional[int], typer.Option("--max-backups")] = None,
    max_age_days: Annotated[Optional[int], typer.Option("--max-age-days")] = None,
) -> None:
    """Run a backup immediately."""
    try:
        run_backup(_config(name, sources, destination, exclude, fmt, level, encrypt, key_file, incremental, manifest, max_backups, max_age_days))
    except Exception as e:
        console.print(f"[bold red]error:[/] {e}")
        raise typer.Exit(1)


@app.command("schedule")
def cmd_schedule(
    cron: Annotated[str, typer.Option("--cron", "-c")],
    sources: Annotated[list[Path], typer.Option("--source", "-s")],
    destination: Annotated[Path, typer.Option("--dest", "-d")],
    name: Annotated[str, typer.Option()] = "backup",
    exclude: Annotated[list[str], typer.Option("--exclude", "-e")] = [],
    fmt: Annotated[str, typer.Option("--format", "-f")] = "tar.gz",
    level: Annotated[int, typer.Option("--level")] = 6,
    encrypt: Annotated[bool, typer.Option("--encrypt/--no-encrypt")] = False,
    key_file: Annotated[Optional[Path], typer.Option("--key-file", "-k")] = None,
    incremental: Annotated[bool, typer.Option("--incremental/--full", "-i")] = False,
    manifest: Annotated[Path, typer.Option()] = Path(".pybackup_manifest.json"),
    max_backups: Annotated[Optional[int], typer.Option("--max-backups")] = None,
    max_age_days: Annotated[Optional[int], typer.Option("--max-age-days")] = None,
) -> None:
    """Start a blocking cron scheduler for recurring backups."""
    from .scheduler import start_scheduler
    try:
        start_scheduler(_config(name, sources, destination, exclude, fmt, level, encrypt, key_file, incremental, manifest, max_backups, max_age_days, cron))
    except Exception as e:
        console.print(f"[bold red]error:[/] {e}")
        raise typer.Exit(1)


@app.command("restore")
def cmd_restore(
    backup: Annotated[Path, typer.Argument()],
    dest: Annotated[Path, typer.Option("--dest", "-d")],
    key_file: Annotated[Optional[Path], typer.Option("--key-file", "-k")] = None,
) -> None:
    """Restore a backup archive."""
    if not backup.exists():
        console.print(f"[bold red]error:[/] not found: {backup}")
        raise typer.Exit(1)
    try:
        run_restore(backup, dest, key_file)
    except Exception as e:
        console.print(f"[bold red]error:[/] {e}")
        raise typer.Exit(1)


@app.command("keygen")
def cmd_keygen(
    output: Annotated[Path, typer.Option("--output", "-o")] = Path("backup.key"),
) -> None:
    """Generate a Fernet encryption key."""
    generate_key(output)
    console.print(f"[bold green]✓[/] {output} (chmod 600)")
    console.print("[yellow]keep this file safe — losing it means losing access to encrypted backups[/]")


@app.command("list")
def cmd_list(
    dest: Annotated[Path, typer.Argument()],
    name: Annotated[str, typer.Option()] = "backup",
) -> None:
    """List backups in a destination directory."""
    if not dest.is_dir():
        console.print(f"[bold red]error:[/] not a directory: {dest}")
        raise typer.Exit(1)

    backups = list_backups(dest, name)
    if not backups:
        console.print(f"no backups found in {dest} (name={name!r})")
        return

    t = Table(show_header=True, header_style="bold cyan")
    t.add_column("#", style="dim", justify="right")
    t.add_column("Timestamp")
    t.add_column("Filename")
    t.add_column("Size", justify="right")
    t.add_column("Enc", justify="center")

    for i, (ts, p) in enumerate(reversed(backups), 1):
        n = p.stat().st_size
        size = f"{n / (1 << 20):.2f} MB" if n >= 1 << 20 else f"{n / (1 << 10):.1f} KB"
        t.add_row(str(i), ts.strftime("%Y-%m-%d  %H:%M:%S"), p.name, size, "[green]✓[/]" if p.suffix == ".enc" else "[dim]—[/]")

    console.print(t)


def main() -> None:
    app()
