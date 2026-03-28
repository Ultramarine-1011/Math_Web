from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

import streamlit as st

from ultramarine.models import AppSettings


def _as_bool(value: str | bool | None, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_secrets() -> Mapping[str, Any]:
    try:
        if hasattr(st.secrets, "to_dict"):
            return st.secrets.to_dict()
        return dict(st.secrets)
    except Exception:
        return {}


def _resolve_path(base_dir: Path, candidate: str | None, fallback: str) -> Path:
    raw = candidate or fallback
    path = Path(raw)
    if not path.is_absolute():
        path = base_dir / path
    return path


def load_settings(
    *,
    env: Mapping[str, str] | None = None,
    secrets: Mapping[str, Any] | None = None,
    base_dir: Path | None = None,
) -> AppSettings:
    env_map = dict(os.environ if env is None else env)
    secret_map = dict(_read_secrets() if secrets is None else secrets)
    root_dir = base_dir or Path(__file__).resolve().parent.parent

    site_title = env_map.get("SITE_TITLE", "Ultramarine Mathematics Atelier")
    profile_name = env_map.get("PROFILE_NAME", "Ultramarine")
    photo_path = _resolve_path(root_dir, env_map.get("PHOTO_PATH"), "photo.jpg")
    notes_dir = _resolve_path(root_dir, env_map.get("NOTES_DIR"), "note_resources")
    notes_catalog_path = _resolve_path(
        root_dir,
        env_map.get("NOTES_CATALOG_PATH"),
        "data/notes_catalog.json",
    )
    comment_backend = env_map.get("COMMENT_BACKEND", "auto").strip().lower()
    debug = _as_bool(env_map.get("DEBUG"), default=False)

    supabase_url = env_map.get("SUPABASE_URL") or secret_map.get("SUPABASE_URL")
    supabase_key = env_map.get("SUPABASE_KEY") or secret_map.get("SUPABASE_KEY")
    supabase_comments_table = (
        env_map.get("SUPABASE_COMMENTS_TABLE")
        or secret_map.get("SUPABASE_COMMENTS_TABLE")
        or "comments"
    )

    return AppSettings(
        site_title=site_title,
        profile_name=profile_name,
        photo_path=photo_path,
        notes_dir=notes_dir,
        notes_catalog_path=notes_catalog_path,
        comment_backend=comment_backend,
        debug=debug,
        supabase_url=supabase_url,
        supabase_key=supabase_key,
        supabase_comments_table=supabase_comments_table,
    )

