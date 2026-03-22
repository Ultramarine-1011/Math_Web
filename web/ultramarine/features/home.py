from __future__ import annotations

from pathlib import Path

import streamlit as st

from ultramarine.content import FEATURE_CARDS, HOME_INTRO
from ultramarine.data.notes import load_note_entries
from ultramarine.models import AppSettings


@st.cache_data(show_spinner=False)
def _load_note_stats(catalog_path: str, notes_dir: str) -> tuple[int, int]:
    notes, _ = load_note_entries(Path(catalog_path), Path(notes_dir))
    featured = sum(1 for note in notes if note.featured)
    return len(notes), featured


def render(settings: AppSettings) -> None:
    note_count, featured_count = _load_note_stats(
        str(settings.notes_catalog_path),
        str(settings.notes_dir),
    )
    registry = st.session_state.get("_page_registry", {})

    st.markdown(
        f"""
        <section class="hero-shell">
            <div class="hero-kicker">Public Mathematics Studio</div>
            <h1 class="hero-title">{settings.site_title}</h1>
            <p class="hero-lead">{HOME_INTRO}</p>
            <div class="meta-row">
                <div class="metric-card">
                    <div class="metric-label">Pages</div>
                    <div class="metric-value">6</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Notes</div>
                    <div class="metric-value">{note_count}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Featured Notes</div>
                    <div class="metric-value">{featured_count}</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    st.markdown("## Site Map")
    columns = st.columns(2)
    for index, card in enumerate(FEATURE_CARDS):
        with columns[index % 2]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-title">{card.icon} {card.title}</div>
                    <p class="feature-summary">{card.summary}</p>
                    <p class="muted" style="margin-top:0.5rem;">{card.detail}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            page = registry.get(card.path)
            if page is not None:
                st.page_link(
                    page,
                    label=f"Open {card.title}",
                    width="stretch",
                )

    st.markdown("## What Changed")
    left, right = st.columns([1.15, 0.85])
    with left:
        st.markdown(
            """
            - The home page handles branding and navigation instead of business logic.
            - Every page exposes one `render(settings)` entry point.
            - Computation, note metadata, and comment storage now live outside the UI layer.
            """
        )
    with right:
        st.markdown(
            """
            <div class="note-card">
                <div class="note-title">Deployment Notes</div>
                <p class="note-summary">
                    This version is organized for Streamlit Cloud. Add Supabase secrets and
                    the community page will switch to cloud-backed writes automatically.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )