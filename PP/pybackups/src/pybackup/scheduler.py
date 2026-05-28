from __future__ import annotations

import signal
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from rich.console import Console

from .engine import run_backup
from .models import BackupJobConfig

console = Console()


def start_scheduler(config: BackupJobConfig) -> None:
    if config.schedule is None:
        console.print("[red]no schedule configured[/]")
        sys.exit(1)

    minute, hour, day, month, dow = config.schedule.cron.split()
    scheduler = BlockingScheduler(timezone="local")
    scheduler.add_job(
        run_backup,
        trigger=CronTrigger(minute=minute, hour=hour, day=day, month=month, day_of_week=dow),
        args=[config],
        id=config.name,
        misfire_grace_time=60,
        coalesce=True,
    )

    console.print(f"[bold green]✓ Scheduler running[/] — cron: [cyan]{config.schedule.cron}[/]")
    console.print(f"  next run: [cyan]{scheduler.get_jobs()[0].next_run_time}[/]")
    console.print("[dim]Ctrl-C to stop[/]\n")

    def _stop(sig, frame):  # noqa: ANN001
        scheduler.shutdown(wait=False)
        sys.exit(0)

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
