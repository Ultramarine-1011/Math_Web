from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def normalize_markdown(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```markdown") and stripped.endswith("```"):
        return stripped.removeprefix("```markdown").removesuffix("```").strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        inner = stripped.removeprefix("```").removesuffix("```").strip()
        if "\n" in inner and not inner.split("\n", 1)[0].strip().startswith(("#", "-", "*", "$")):
            return inner.split("\n", 1)[1].strip()
        return inner
    return stripped


def call_chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    timeout: int = 45,
) -> str:
    endpoint = base_url.rstrip("/") + "/chat/completions"
    payload = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": 0.35,
        }
    ).encode("utf-8")
    request = Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"LLM request failed with HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    try:
        return normalize_markdown(str(result["choices"][0]["message"]["content"]))
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("LLM response did not include a message.") from exc
