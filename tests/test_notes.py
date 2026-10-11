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


def test_load_note_entries_handles_invalid_catalog(tmp_path: Path) -> None:
    catalog_path = tmp_path / "notes_catalog.json"
    catalog_path.write_text("{bad json", encoding="utf-8")

    notes, missing_files = load_note_entries(catalog_path, tmp_path)

    assert notes == []
    assert missing_files == []


def test_catalog_skips_malformed_entries_and_deduplicates(tmp_path: Path) -> None:
    (tmp_path / "ok.pdf").write_bytes(b"pdf")
    valid = {
        "slug": "ok",
        "title": "OK",
        "summary": "Summary",
        "file_name": "ok.pdf",
        "tags": ["analysis"],
    }
    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            [
                None,
                valid | {"slug": None},
                valid | {"sort_order": "invalid"},
                valid | {"tags": None},
                valid,
                valid,
            ]
        )
    )
    notes, _ = load_note_entries(catalog, tmp_path)
    assert len(notes) == 1
    assert notes[0].tags == ("analysis",)


def test_catalog_rejects_traversal_and_non_pdf_files(tmp_path: Path) -> None:
    import pytest

    from ultramarine.data.notes import read_note_bytes

    root = tmp_path / "notes"
    root.mkdir()
    (tmp_path / "outside.pdf").write_bytes(b"private")
    (root / "not_pdf.txt").write_text("private")
    (root / "linked.pdf").symlink_to(tmp_path / "outside.pdf")
    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            [
                {"slug": name, "title": name, "summary": "summary", "file_name": name}
                for name in ["../outside.pdf", "not_pdf.txt", "linked.pdf"]
            ]
        )
    )
    assert load_note_entries(catalog, root)[0] == []
    with pytest.raises(ValueError):
        read_note_bytes(root, "../outside.pdf")


def test_real_catalog_keeps_all_ten_pdfs() -> None:
    root = Path(__file__).resolve().parents[1]
    notes, missing = load_note_entries(root / "data/notes_catalog.json", root / "note_resources")
    assert len(notes) == 10
    assert missing == []
