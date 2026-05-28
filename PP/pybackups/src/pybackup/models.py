from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class FileRecord(BaseModel):
    size: int = Field(ge=0)
    mtime: float
    sha256: str


class BackupManifest(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    files: dict[str, FileRecord] = Field(default_factory=dict)


class SourceConfig(BaseModel):
    paths: list[Path] = Field(min_length=1)
    exclude_patterns: list[str] = Field(default_factory=list)

    @field_validator("paths", mode="before")
    @classmethod
    def coerce_paths(cls, v: list) -> list[Path]:
        return [Path(p) for p in v]

    @field_validator("paths")
    @classmethod
    def paths_must_exist(cls, v: list[Path]) -> list[Path]:
        for p in v:
            if not p.exists():
                raise ValueError(f"path does not exist: {p}")
        return v


class CompressionConfig(BaseModel):
    format: Literal["zip", "tar.gz", "tar.bz2"] = "tar.gz"
    level: int = Field(default=6, ge=0, le=9)


class EncryptionConfig(BaseModel):
    enabled: bool = False
    key_file: Path | None = None

    @model_validator(mode="after")
    def key_required_when_enabled(self) -> EncryptionConfig:
        if self.enabled and self.key_file is None:
            raise ValueError("--key-file is required when --encrypt is set")
        if self.enabled and self.key_file and not self.key_file.exists():
            raise ValueError(f"key file not found: {self.key_file}")
        return self


class RetentionConfig(BaseModel):
    max_backups: int | None = Field(default=None, gt=0)
    max_age_days: int | None = Field(default=None, gt=0)


class IncrementalConfig(BaseModel):
    enabled: bool = False
    manifest_path: Path = Path(".pybackup_manifest.json")


class ScheduleConfig(BaseModel):
    cron: str

    @field_validator("cron")
    @classmethod
    def valid_cron(cls, v: str) -> str:
        if len(v.strip().split()) != 5:
            raise ValueError(f"cron must have 5 fields, got: {v!r}")
        return v


class BackupJobConfig(BaseModel):
    name: str = Field(default="backup", pattern=r"^[a-zA-Z0-9_\-]+$")
    source: SourceConfig
    destination: Path
    compression: CompressionConfig = Field(default_factory=CompressionConfig)
    encryption: EncryptionConfig = Field(default_factory=EncryptionConfig)
    retention: RetentionConfig = Field(default_factory=RetentionConfig)
    incremental: IncrementalConfig = Field(default_factory=IncrementalConfig)
    schedule: ScheduleConfig | None = None

    @field_validator("destination", mode="before")
    @classmethod
    def coerce_destination(cls, v) -> Path:
        return Path(v)

    @model_validator(mode="after")
    def create_destination(self) -> BackupJobConfig:
        self.destination.mkdir(parents=True, exist_ok=True)
        return self
