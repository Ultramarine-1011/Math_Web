"""Public site configuration; no credentials or external services are needed."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AppSettings:
    site_title: str
    profile_name: str
    photo_path: Path
    notes_dir: Path
    notes_catalog_path: Path
    debug: bool = False


def load_settings(
    *, env: Mapping[str, str] | None = None, base_dir: Path | None = None
) -> AppSettings:
    values = os.environ if env is None else env
    root = base_dir or Path(__file__).resolve().parent.parent

    def path(key: str, default: str) -> Path:
        candidate = Path(values.get(key) or default).expanduser()
        return candidate if candidate.is_absolute() else root / candidate

    return AppSettings(
        site_title=values.get("SITE_TITLE", "Ultramarine Lab"),
        profile_name=values.get("PROFILE_NAME", "Ultramarine"),
        photo_path=path("PHOTO_PATH", "photo.jpg"),
        notes_dir=path("NOTES_DIR", "note_resources"),
        notes_catalog_path=path("NOTES_CATALOG_PATH", "data/notes_catalog.json"),
        debug=values.get("DEBUG", "").strip().lower() in {"1", "true", "yes", "on"},
    )
