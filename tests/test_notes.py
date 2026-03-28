from __future__ import annotations

import json
from pathlib import Path

from ultramarine.data.notes import load_note_entries


def test_load_note_entries_skips_missing_files(tmp_path: Path) -> None:
    notes_dir = tmp_path / "note_resources"
    notes_dir.mkdir()
    (notes_dir / "existing.pdf").write_bytes(b"pdf")

    catalog_path = tmp_path / "notes_catalog.json"
    catalog_path.write_text(
        json.dumps(
            [
                {
                    "slug": "existing",
                    "title": "Existing",
                    "summary": "Exists",
                    "file_name": "existing.pdf",
                    "tags": ["analysis"],
                    "featured": True,
                    "sort_order": 2,
                },
                {
                    "slug": "missing",
                    "title": "Missing",
                    "summary": "Missing",
                    "file_name": "missing.pdf",
                    "tags": ["topology"],
                    "featured": False,
                    "sort_order": 1,
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    notes, missing_files = load_note_entries(catalog_path, notes_dir)

    assert [note.slug for note in notes] == ["existing"]
    assert missing_files == ["missing.pdf"]
