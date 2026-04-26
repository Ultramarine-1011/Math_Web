from __future__ import annotations

from ultramarine.ai import normalize_markdown


def test_normalize_markdown_removes_markdown_fence() -> None:
    content = """```markdown
## 标题

- 条目
```"""

    assert normalize_markdown(content) == "## 标题\n\n- 条目"


def test_normalize_markdown_keeps_regular_markdown() -> None:
    assert normalize_markdown("## 标题\n\n正文") == "## 标题\n\n正文"
