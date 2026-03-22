from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from ultramarine.data.comments import (
    JsonCommentRepository,
    create_comment_repository,
    validate_comment_input,
)
from ultramarine.models import AppSettings


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeTable:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self.rows = rows
        self._action = "select"
        self._payload: dict[str, object] | None = None
        self._filters: list[tuple[str, object]] = []
        self._limit: int | None = None

    def select(self, *_args, **_kwargs):
        self._action = "select"
        return self

    def order(self, *_args, **_kwargs):
        return self

    def limit(self, value: int):
        self._limit = value
        return self

    def eq(self, field: str, value: object):
        self._filters.append((field, value))
        return self

    def insert(self, payload: dict[str, object]):
        self._action = "insert"
        self._payload = payload
        return self

    def update(self, payload: dict[str, object]):
        self._action = "update"
        self._payload = payload
        return self

    def execute(self):
        rows = self.rows
        for field, value in self._filters:
            rows = [row for row in rows if row.get(field) == value]

        if self._action == "insert":
            next_id = str(len(self.rows) + 1)
            row = {
                "id": next_id,
                "nickname": self._payload["nickname"],
                "content": self._payload["content"],
                "created_at": "2026-03-22T00:00:00+00:00",
                "likes": self._payload.get("likes", 0),
            }
            self.rows.insert(0, row)
            return FakeResponse([row])

        if self._action == "update":
            for row in self.rows:
                if all(row.get(field) == value for field, value in self._filters):
                    row.update(self._payload or {})
                    return FakeResponse([row])
            return FakeResponse([])

        if self._limit is not None:
            rows = rows[: self._limit]
        return FakeResponse(rows)


class FakeSupabaseClient:
    def __init__(self) -> None:
        self.rows: list[dict[str, object]] = []

    def table(self, _name: str) -> FakeTable:
        return FakeTable(self.rows)


def build_settings(tmp_path: Path) -> AppSettings:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    catalog_path = data_dir / "notes_catalog.json"
    catalog_path.write_text("[]", encoding="utf-8")
    return AppSettings(
        site_title="Test",
        profile_name="Tester",
        photo_path=tmp_path / "photo.jpg",
        notes_dir=tmp_path / "note_resources",
        notes_catalog_path=catalog_path,
        comment_backend="auto",
        debug=False,
    )


def test_validate_comment_input() -> None:
    assert validate_comment_input("", "hello") == "请先填写昵称。"
    assert validate_comment_input("name", "") == "留言内容不能为空。"
    assert validate_comment_input("ok", "valid") is None


def test_json_comment_repository_round_trip(tmp_path: Path) -> None:
    repo = JsonCommentRepository(tmp_path / "comments.json")
    comment = repo.create_comment("Euler", "First post")

    listed = repo.list_comments(limit=10)
    assert listed[0].nickname == "Euler"
    assert listed[0].content == "First post"
    assert repo.increment_like(comment.id) == 1


def test_create_comment_repository_defaults_to_json(tmp_path: Path) -> None:
    settings = build_settings(tmp_path)

    handle = create_comment_repository(settings)

    assert handle.backend_label == "JSON"
    assert handle.repo.is_writable() is True


def test_create_comment_repository_uses_supabase_when_available(tmp_path: Path) -> None:
    settings = replace(
        build_settings(tmp_path),
        comment_backend="supabase",
        supabase_url="https://example.supabase.co",
        supabase_key="key",
    )
    client = FakeSupabaseClient()

    handle = create_comment_repository(
        settings,
        client_factory=lambda _url, _key: client,
    )

    created = handle.repo.create_comment("Noether", "Symmetry")
    assert handle.backend_label == "Supabase"
    assert created.nickname == "Noether"
    assert handle.repo.increment_like(created.id) == 1


def test_supabase_without_secrets_becomes_read_only(tmp_path: Path) -> None:
    settings = replace(build_settings(tmp_path), comment_backend="supabase")

    handle = create_comment_repository(settings)

    assert handle.backend_label == "Read-only"
    assert handle.repo.is_writable() is False
