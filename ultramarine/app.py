from __future__ import annotations

import streamlit as st

from ultramarine.config import load_settings
from ultramarine.layout import render_debug_panel, render_sidebar
from ultramarine.navigation import build_navigation
from ultramarine.theme import apply_global_styles, configure_plotly_theme


def _initialize_session_state() -> None:
    defaults = {
        "_page_registry": {},
        "animation_speed": "balanced",
        "plot_quality": "high",
        "notes_selected_tags": [],
        "liked_comment_ids": set(),
        "last_comment_at": 0.0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def run() -> None:
    settings = load_settings()
    st.set_page_config(
        page_title=settings.site_title,
        page_icon="∫",
        layout="wide",
    )
    _initialize_session_state()
    configure_plotly_theme()
    apply_global_styles()

    current_page, pages = build_navigation(settings)
    st.session_state["_page_registry"] = pages
    render_sidebar(settings)
    render_debug_panel(settings)
    current_page.run()
