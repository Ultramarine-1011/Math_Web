from __future__ import annotations

import streamlit as st

from ultramarine.config import load_settings
from ultramarine.layout import render_debug_panel, render_sidebar
from ultramarine.navigation import build_navigation
from ultramarine.theme import apply_global_styles, configure_plotly_theme


def run() -> None:
    settings = load_settings()
    st.set_page_config(
        page_title=settings.site_title,
        page_icon="∫",
        layout="wide",
    )
    configure_plotly_theme()
    apply_global_styles()

    current_page, pages = build_navigation(settings)
    st.session_state["_page_registry"] = pages
    render_sidebar(settings)
    render_debug_panel(settings)
    current_page.run()
