"""Load local note metadata and PDFs without exposing files outside the note directory."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class NoteEntry:
    slug: str
    title: str
    summary: str
    file_name: str
    tags: tuple[str, ...]
    featured: bool
    sort_order: int


def note_path(notes_dir: Path, file_name: str) -> Path:
    root = notes_dir.resolve()
    path = (root / file_name).resolve()
    if not path.is_relative_to(root) or path.suffix.lower() != ".pdf":
        raise ValueError("Notes must be PDFs inside the configured directory.")
    return path


def load_note_entries(catalog_path: Path, notes_dir: Path) -> tuple[list[NoteEntry], list[str]]:
    try:
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [], []
    if not isinstance(payload, list):
        return [], []

    entries, missing_files = [], []
    seen_slugs = set()
    for item in payload:
        if not isinstance(item, dict):
            continue
        required = ("slug", "title", "summary", "file_name")
        if any(
            not isinstance(item.get(field), str) or not item[field].strip() for field in required
        ):
            continue
        slug, file_name = item["slug"], item["file_name"]
        tags = item.get("tags", [])
        if slug in seen_slugs or not isinstance(tags, list):
            continue
        try:
            path = note_path(notes_dir, file_name)
            order = int(item.get("sort_order", 0))
        except (TypeError, ValueError, OverflowError):
            continue
        if not path.is_file():
            missing_files.append(file_name)
            continue
        seen_slugs.add(slug)
        entries.append(
            NoteEntry(
                slug,
                item["title"],
                item["summary"],
                file_name,
                tuple(dict.fromkeys(tag for tag in tags if isinstance(tag, str) and tag.strip())),
                item.get("featured") is True,
                order,
            )
        )
    entries.sort(key=lambda note: (note.sort_order, note.title))
    return entries, missing_files


def read_note_bytes(notes_dir: Path, file_name: str) -> bytes:
    return note_path(notes_dir, file_name).read_bytes()
