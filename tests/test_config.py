from pathlib import Path

import pytest

from ultramarine.config import load_settings


def test_load_settings_defaults(tmp_path: Path) -> None:
    settings = load_settings(env={}, base_dir=tmp_path)
    assert settings.site_title == "Ultramarine Lab"
    assert settings.profile_name == "Ultramarine"
    assert settings.photo_path == tmp_path / "photo.jpg"
    assert settings.notes_dir == tmp_path / "note_resources"
    assert settings.notes_catalog_path == tmp_path / "data/notes_catalog.json"
    assert settings.debug is False


def test_environment_overrides_and_absolute_paths(tmp_path: Path) -> None:
    settings = load_settings(
        env={
            "SITE_TITLE": "Custom Lab",
            "PROFILE_NAME": "Ada",
            "PHOTO_PATH": "assets/photo.jpg",
            "NOTES_DIR": str(tmp_path / "pdfs"),
            "NOTES_CATALOG_PATH": "catalog.json",
            "DEBUG": "true",
        },
        base_dir=tmp_path,
    )
    assert settings.site_title == "Custom Lab"
    assert settings.profile_name == "Ada"
    assert settings.photo_path == tmp_path / "assets/photo.jpg"
    assert settings.notes_dir == tmp_path / "pdfs"
    assert settings.notes_catalog_path == tmp_path / "catalog.json"
    assert settings.debug is True


@pytest.mark.parametrize("value", ["1", "true", " ON ", "yes"])
def test_debug_values(value: str) -> None:
    assert load_settings(env={"DEBUG": value}).debug
