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


def _read_dotenv(base_dir: Path) -> dict[str, str]:
    dotenv_path = base_dir / ".env"
    if not dotenv_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        clean_key = key.strip()
        clean_value = value.strip().strip('"').strip("'")
        if clean_key:
            values[clean_key] = clean_value
    return values


def load_settings(
    *,
    env: Mapping[str, str] | None = None,
    secrets: Mapping[str, Any] | None = None,
    base_dir: Path | None = None,
) -> AppSettings:
    env_map = dict(os.environ if env is None else env)
    secret_map = dict(_read_secrets() if secrets is None else secrets)
    root_dir = base_dir or Path(__file__).resolve().parent.parent
    dotenv_map = _read_dotenv(root_dir) if env is None else {}

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
    llm_api_key = (
        env_map.get("LLM_API_KEY")
        or env_map.get("OPENAI_API_KEY")
        or env_map.get("DEEPSEEK_API_KEY")
        or secret_map.get("LLM_API_KEY")
        or secret_map.get("OPENAI_API_KEY")
        or secret_map.get("DEEPSEEK_API_KEY")
        or dotenv_map.get("LLM_API_KEY")
        or dotenv_map.get("OPENAI_API_KEY")
        or dotenv_map.get("DEEPSEEK_API_KEY")
    )
    llm_base_url = (
        env_map.get("LLM_BASE_URL")
        or secret_map.get("LLM_BASE_URL")
        or dotenv_map.get("LLM_BASE_URL")
        or ("https://api.deepseek.com/v1" if dotenv_map.get("DEEPSEEK_API_KEY") else None)
        or "https://api.openai.com/v1"
    )
    llm_model = (
        env_map.get("LLM_MODEL")
        or secret_map.get("LLM_MODEL")
        or dotenv_map.get("LLM_MODEL")
        or ("deepseek-chat" if dotenv_map.get("DEEPSEEK_API_KEY") else None)
        or "gpt-4o-mini"
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
        llm_api_key=llm_api_key,
        llm_base_url=llm_base_url,
        llm_model=llm_model,
    )

