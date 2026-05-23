from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    storage_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "storage" / "exports")
    export_ttl_seconds: int = 3600
