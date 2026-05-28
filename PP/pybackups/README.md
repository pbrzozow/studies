# pybackup

A Pydantic-powered local backup tool with:

| Feature | Details |
|---|---|
| 🗜️ Compression | `zip`, `tar.gz`, `tar.bz2` with configurable level 0–9 |
| 🔒 Encryption | Fernet (AES-128-CBC + HMAC-SHA256) |
| 📈 Incremental | SHA-256 manifest — only changed files are archived |
| 🗑️ Retention | Keep last N backups and/or delete by age |
| ⏰ Scheduling | Standard 5-field cron expressions via APScheduler |

---

## Install

```bash
pip install -e .
```

Or into an isolated environment:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

---

## Commands

### `keygen` — generate an encryption key

```bash
pybackup keygen --output backup.key
```

The key file is written with `chmod 600`.
**Back this up separately — losing it means losing access to encrypted archives.**

---

### `run` — immediate backup

```bash
pybackup run \
  --source /home/alice/documents \
  --source /home/alice/photos \
  --dest   /mnt/nas/backups \
  --name   alice-home \
  --format tar.gz \
  --level  6 \
  --encrypt   --key-file backup.key \
  --incremental \
  --max-backups  10 \
  --max-age-days 30 \
  --exclude "*.pyc" \
  --exclude "__pycache__"
```

Archive filenames follow the pattern: `<name>_<YYYYmmddTHHMMSS>.tar.gz[.enc]`

---

### `schedule` — recurring backups

```bash
# Daily at 02:00
pybackup schedule \
  --cron  "0 2 * * *" \
  --source /home/alice/documents \
  --dest   /mnt/nas/backups \
  --name   nightly \
  --incremental \
  --max-backups 7
```

The process blocks (foreground). Use a service manager (systemd, supervisor) to
run it as a daemon.

---

### `list` — view existing backups

```bash
pybackup list /mnt/nas/backups --name alice-home
```

```
             Backups in /mnt/nas/backups  (name=alice-home)
 # │        Timestamp        │ Filename                                    │   Size    │ Enc
───┼─────────────────────────┼─────────────────────────────────────────────┼───────────┼─────
 1 │ 2024-03-15  02:00:01    │ alice-home_20240315T020001.tar.gz.enc       │  84.32 MB │  ✓
 2 │ 2024-03-16  02:00:00    │ alice-home_20240316T020000.tar.gz.enc       │   2.14 MB │  ✓
```

---

### `restore` — extract a backup

```bash
pybackup restore /mnt/nas/backups/alice-home_20240316T020000.tar.gz.enc \
  --dest /tmp/restored \
  --key-file backup.key
```

---

## Architecture

```
src/pybackup/
├── models.py        Pydantic models (BackupJobConfig, BackupManifest, …)
├── cli.py           Typer CLI (run / schedule / restore / keygen / list)
├── engine.py        Orchestration: ties all modules together
├── compression.py   zip / tar.gz / tar.bz2 creation and extraction
├── crypto.py        Fernet key generation, encrypt_file, decrypt_file
├── incremental.py   SHA-256 manifest + changed-file detection
├── retention.py     Prune old backups by count or age
└── scheduler.py     APScheduler cron wrapper
```

## Cron quick reference

| Expression    | Meaning               |
|---------------|-----------------------|
| `0 2 * * *`   | Daily at 02:00        |
| `0 * * * *`   | Every hour            |
| `0 2 * * 0`   | Weekly (Sun at 02:00) |
| `0 2 1 * *`   | Monthly (1st at 02:00)|
| `*/15 * * * *`| Every 15 minutes      |
