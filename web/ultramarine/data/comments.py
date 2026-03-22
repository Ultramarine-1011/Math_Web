from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Protocol

from ultramarine.models import AppSettings, Comment

COMMENT_COOLDOWN_SECONDS = 15
MAX_NICKNAME_LENGTH = 24
MAX_CONTENT_LENGTH = 400


class CommentRepository(Protocol):
    def list_comments(self, limit: int) -> list[Comment]:
        ...

    def create_comment(self, nickname: str, content: str) -> Comment:
        ...

    def increment_like(self, comment_id: str) -> int:
        ...

    def is_writable(self) -> bool:
        ...


@dataclass(frozen=True, slots=True)
class CommentRepositoryHandle:
    repo: CommentRepository
    backend_label: str
    status_message: str | None = None


def validate_comment_input(nickname: str, content: str) -> str | None:
    clean_name = nickname.strip()
    clean_content = content.strip()

    if not clean_name:
        return "请先填写昵称。"
    if len(clean_name) > MAX_NICKNAME_LENGTH:
        return f"昵称请控制在 {MAX_NICKNAME_LENGTH} 个字符以内。"
    if not clean_content:
        return "留言内容不能为空。"
    if len(clean_content) > MAX_CONTENT_LENGTH:
        return f"留言请控制在 {MAX_CONTENT_LENGTH} 个字符以内。"
    return None


def get_local_comment_path(settings: AppSettings) -> Path:
    return settings.notes_catalog_path.parent / "comments.json"


def _row_to_comment(row: dict[str, Any]) -> Comment:
    return Comment(
        id=str(row["id"]),
        nickname=str(row["nickname"]),
        content=str(row["content"]),
        created_at=str(row["created_at"]),
        likes=int(row.get("likes", 0)),
    )


class JsonCommentRepository:
    def __init__(self, path: Path, *, writable: bool = True) -> None:
        self.path = path
        self._writable = writable
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict[str, Any]]:
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                return payload
        except json.JSONDecodeError:
            pass
        return []

    def _save(self, rows: list[dict[str, Any]]) -> None:
        if not self._writable:
            raise PermissionError("Repository is read-only.")
        self.path.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def list_comments(self, limit: int) -> list[Comment]:
        rows = sorted(
            self._load(),
            key=lambda item: str(item.get("created_at", "")),
            reverse=True,
        )
        return [_row_to_comment(row) for row in rows[:limit]]

    def create_comment(self, nickname: str, content: str) -> Comment:
        comment = Comment(
            id=str(uuid.uuid4()),
            nickname=nickname.strip(),
            content=content.strip(),
            created_at=datetime.now(timezone.utc).isoformat(),
            likes=0,
        )
        rows = self._load()
        rows.insert(
            0,
            {
                "id": comment.id,
                "nickname": comment.nickname,
                "content": comment.content,
                "created_at": comment.created_at,
                "likes": comment.likes,
            },
        )
        self._save(rows)
        return comment

    def increment_like(self, comment_id: str) -> int:
        rows = self._load()
        for row in rows:
            if str(row.get("id")) == comment_id:
                row["likes"] = int(row.get("likes", 0)) + 1
                self._save(rows)
                return int(row["likes"])
        raise KeyError(comment_id)

    def is_writable(self) -> bool:
        return self._writable


class SupabaseCommentRepository:
    def __init__(
        self,
        *,
        url: str,
        key: str,
        table: str,
        client_factory: Callable[[str, str], Any] | None = None,
    ) -> None:
        self.table = table
        self._client_factory = client_factory
        self._client = self._create_client(url, key)

    def _create_client(self, url: str, key: str) -> Any:
        if self._client_factory is not None:
            return self._client_factory(url, key)

        from supabase import create_client

        return create_client(url, key)

    def list_comments(self, limit: int) -> list[Comment]:
        response = (
            self._client.table(self.table)
            .select("id, nickname, content, created_at, likes")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return [_row_to_comment(row) for row in response.data or []]

    def create_comment(self, nickname: str, content: str) -> Comment:
        payload = {
            "nickname": nickname.strip(),
            "content": content.strip(),
            "likes": 0,
        }
        response = self._client.table(self.table).insert(payload).execute()
        if not response.data:
            raise RuntimeError("Supabase insert returned no data.")
        return _row_to_comment(response.data[0])

    def increment_like(self, comment_id: str) -> int:
        select_response = (
            self._client.table(self.table)
            .select("likes")
            .eq("id", comment_id)
            .limit(1)
            .execute()
        )
        if not select_response.data:
            raise KeyError(comment_id)
        likes = int(select_response.data[0].get("likes", 0)) + 1
        (
            self._client.table(self.table)
            .update({"likes": likes})
            .eq("id", comment_id)
            .execute()
        )
        return likes

    def is_writable(self) -> bool:
        return True


def create_comment_repository(
    settings: AppSettings,
    *,
    client_factory: Callable[[str, str], Any] | None = None,
) -> CommentRepositoryHandle:
    local_path = get_local_comment_path(settings)
    local_repo = JsonCommentRepository(local_path, writable=True)

    if settings.comment_backend == "json":
        return CommentRepositoryHandle(
            repo=local_repo,
            backend_label="JSON",
            status_message="当前使用本地 JSON 文件作为留言存储，适合本地开发和轻量演示。",
        )

    if settings.comment_backend == "supabase":
        if not (settings.supabase_url and settings.supabase_key):
            return CommentRepositoryHandle(
                repo=JsonCommentRepository(local_path, writable=False),
                backend_label="Read-only",
                status_message="缺少 Supabase 凭证，留言广场已降级为只读模式。",
            )
        try:
            repo = SupabaseCommentRepository(
                url=settings.supabase_url,
                key=settings.supabase_key,
                table=settings.supabase_comments_table,
                client_factory=client_factory,
            )
            return CommentRepositoryHandle(
                repo=repo,
                backend_label="Supabase",
                status_message="留言正在使用 Supabase 云端数据库，可安全用于公开部署。",
            )
        except Exception:
            return CommentRepositoryHandle(
                repo=JsonCommentRepository(local_path, writable=False),
                backend_label="Read-only",
                status_message="Supabase 初始化失败，留言广场已切换为只读模式。",
            )

    if settings.supabase_url and settings.supabase_key:
        try:
            repo = SupabaseCommentRepository(
                url=settings.supabase_url,
                key=settings.supabase_key,
                table=settings.supabase_comments_table,
                client_factory=client_factory,
            )
            return CommentRepositoryHandle(
                repo=repo,
                backend_label="Supabase",
                status_message="检测到 Supabase 凭证，留言自动切换到云端存储。",
            )
        except Exception:
            return CommentRepositoryHandle(
                repo=JsonCommentRepository(local_path, writable=False),
                backend_label="Read-only",
                status_message="云端留言不可用，当前仅展示已有内容。",
            )

    return CommentRepositoryHandle(
        repo=local_repo,
        backend_label="JSON",
        status_message="未配置云端留言，将自动使用本地 JSON 仓储。",
    )
