from __future__ import annotations

import json
from pathlib import Path

from ultramarine.models import NoteEntry


def load_note_entries(
    catalog_path: Path,
    notes_dir: Path,
) -> tuple[list[NoteEntry], list[str]]:
    if not catalog_path.exists():
        return [], []

    try:
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [], []
    if not isinstance(payload, list):
        return [], []

    entries: list[NoteEntry] = []
    missing_files: list[str] = []
    seen_slugs: set[str] = set()

    for item in payload:
        if not isinstance(item, dict):
            continue
        required = ("slug", "title", "summary", "file_name")
        if any(not str(item.get(field, "")).strip() for field in required):
            continue
        slug = str(item["slug"])
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        file_name = str(item["file_name"])
        if not (notes_dir / file_name).exists():
            missing_files.append(file_name)
            continue
        entries.append(
            NoteEntry(
                slug=slug,
                title=str(item["title"]),
                summary=str(item["summary"]),
                file_name=file_name,
                tags=tuple(str(tag) for tag in item.get("tags", []) if str(tag).strip()),
                featured=bool(item.get("featured", False)),
                sort_order=int(item.get("sort_order", 0)),
            )
        )

    entries.sort(key=lambda note: (note.sort_order, note.title))
    return entries, missing_files


def read_note_bytes(notes_dir: Path, note: NoteEntry) -> bytes:
    return (notes_dir / note.file_name).read_bytes()
