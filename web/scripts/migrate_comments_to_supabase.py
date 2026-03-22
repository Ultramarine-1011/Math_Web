from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path


def normalize_row(row: dict[str, object]) -> dict[str, object]:
    created_at = row.get("created_at") or row.get("time")
    if isinstance(created_at, str):
        try:
            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00")).isoformat()
        except ValueError:
            created_at = created_at
    return {
        "id": str(row.get("id") or ""),
        "nickname": str(row.get("nickname") or row.get("user") or "Guest"),
        "content": str(row.get("content") or ""),
        "created_at": created_at or datetime.utcnow().isoformat(),
        "likes": int(row.get("likes", 0)),
    }


def main() -> None:
    source_path = Path(os.getenv("COMMENTS_JSON_PATH", "data/comments.json"))
    if not source_path.exists():
        print(f"Skip: {source_path} does not exist.")
        return

    raw_text = source_path.read_text(encoding="utf-8").strip()
    if not raw_text:
        print("Skip: comments.json is empty.")
        return

    rows = json.loads(raw_text)
    if not rows:
        print("Skip: comments.json has no rows.")
        return

    from supabase import create_client

    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    table = os.getenv("SUPABASE_COMMENTS_TABLE", "comments")
    client = create_client(url, key)

    normalized = [normalize_row(row) for row in rows]
    client.table(table).upsert(normalized).execute()
    print(f"Migrated {len(normalized)} comments to {table}.")


if __name__ == "__main__":
    main()
