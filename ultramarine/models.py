from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AppSettings:
    site_title: str
    profile_name: str
    photo_path: Path
    notes_dir: Path
    notes_catalog_path: Path
    comment_backend: str
    debug: bool
    supabase_url: str | None = None
    supabase_key: str | None = None
    supabase_comments_table: str = "comments"


@dataclass(frozen=True, slots=True)
class NoteEntry:
    slug: str
    title: str
    summary: str
    file_name: str
    tags: tuple[str, ...]
    featured: bool
    sort_order: int

    @property
    def stem(self) -> str:
        return Path(self.file_name).stem


@dataclass(frozen=True, slots=True)
class Comment:
    id: str
    nickname: str
    content: str
    created_at: str
    likes: int

