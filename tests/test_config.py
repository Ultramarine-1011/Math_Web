from __future__ import annotations

from pathlib import Path

from ultramarine.config import load_settings


def test_load_settings_defaults(tmp_path: Path) -> None:
    settings = load_settings(env={}, secrets={}, base_dir=tmp_path)

    assert settings.site_title == "Ultramarine Mathematics Atelier"
    assert settings.profile_name == "Ultramarine"
    assert settings.photo_path == tmp_path / "photo.jpg"
    assert settings.notes_dir == tmp_path / "note_resources"
    assert settings.notes_catalog_path == tmp_path / "data/notes_catalog.json"
    assert settings.comment_backend == "auto"
    assert settings.debug is False


def test_load_settings_uses_env_and_secrets(tmp_path: Path) -> None:
    env = {
        "SITE_TITLE": "Custom Site",
        "PROFILE_NAME": "Ada",
        "PHOTO_PATH": "assets/photo.jpg",
        "NOTES_DIR": "docs",
        "NOTES_CATALOG_PATH": "catalog.json",
        "COMMENT_BACKEND": "supabase",
        "DEBUG": "true",
    }
    secrets = {
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_KEY": "secret",
        "SUPABASE_COMMENTS_TABLE": "community_comments",
    }

    settings = load_settings(env=env, secrets=secrets, base_dir=tmp_path)

    assert settings.site_title == "Custom Site"
    assert settings.profile_name == "Ada"
    assert settings.photo_path == tmp_path / "assets/photo.jpg"
    assert settings.notes_dir == tmp_path / "docs"
    assert settings.notes_catalog_path == tmp_path / "catalog.json"
    assert settings.comment_backend == "supabase"
    assert settings.debug is True
    assert settings.supabase_url == "https://example.supabase.co"
    assert settings.supabase_key == "secret"
    assert settings.supabase_comments_table == "community_comments"
