from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

SMOKE_SCRIPTS = [
    "tests/smoke_apps/home_app.py",
    "tests/smoke_apps/interactive_app.py",
    "tests/smoke_apps/gallery_app.py",
    "tests/smoke_apps/animations_app.py",
    "tests/smoke_apps/notes_app.py",
    "tests/smoke_apps/community_app.py",
    "app.py",
]


@pytest.mark.parametrize("script_path", SMOKE_SCRIPTS)
def test_streamlit_pages_smoke(script_path: str) -> None:
    app = AppTest.from_file(Path(script_path), default_timeout=5)
    app.run(timeout=8)
    assert len(app.exception) == 0
