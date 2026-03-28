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

    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    entries: list[NoteEntry] = []
    missing_files: list[str] = []

    for item in payload:
        file_name = item["file_name"]
        if not (notes_dir / file_name).exists():
            missing_files.append(file_name)
            continue
        entries.append(
            NoteEntry(
                slug=item["slug"],
                title=item["title"],
                summary=item["summary"],
                file_name=file_name,
                tags=tuple(item.get("tags", [])),
                featured=bool(item.get("featured", False)),
                sort_order=int(item.get("sort_order", 0)),
            )
        )

    entries.sort(key=lambda note: (note.sort_order, note.title))
    return entries, missing_files


def read_note_bytes(notes_dir: Path, note: NoteEntry) -> bytes:
    return (notes_dir / note.file_name).read_bytes()
