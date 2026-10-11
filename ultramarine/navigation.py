from __future__ import annotations

import streamlit as st

from ultramarine.config import AppSettings
from ultramarine.content import FEATURE_CARDS
from ultramarine.features import (
    animations,
    complex_lab,
    data_lab,
    fractals,
    gallery,
    home,
    interactive,
    notes,
)


def build_navigation(settings: AppSettings):
    renderers = {
        "interactive-lab": interactive,
        "data-lab": data_lab,
        "animations": animations,
        "gallery": gallery,
        "complex-lab": complex_lab,
        "fractals": fractals,
        "notes": notes,
    }
    pages = {
        "home": st.Page(
            lambda: home.render(settings), title="首页", icon=":material/home:", default=True
        )
    }
    for card in FEATURE_CARDS:
        renderer = renderers[card.path]
        pages[card.path] = st.Page(
            lambda renderer=renderer: renderer.render(settings),
            title=card.title,
            icon=card.icon,
            url_path=card.path,
        )
    current_page = st.navigation(
        {
            "实验": [pages["home"], pages["interactive-lab"], pages["data-lab"]],
            "数学探索": [
                pages[key] for key in ("animations", "gallery", "complex-lab", "fractals")
            ],
            "资料": [pages["notes"]],
        },
        position="top",
    )
    return current_page, pages
