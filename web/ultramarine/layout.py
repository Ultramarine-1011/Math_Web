from __future__ import annotations

from typing import Iterable

import streamlit as st

from ultramarine.content import SITE_BLURB
from ultramarine.models import AppSettings


def render_sidebar(settings: AppSettings) -> None:
    with st.sidebar:
        if settings.photo_path.exists():
            st.image(str(settings.photo_path), width="stretch")
        else:
            st.markdown(
                '<div class="sidebar-card"><h3 style="margin-top:0;">Ultramarine</h3>'
                '<p class="muted" style="margin-bottom:0;">Local portrait not found. Text-only fallback is active.</p></div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="sidebar-card" style="margin-top: 1rem;">
                <div class="metric-label">Mathematics Atelier</div>
                <div class="metric-value" style="font-size:1.35rem;">{settings.profile_name}</div>
                <p class="muted" style="margin:0.55rem 0 0;">{SITE_BLURB}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "Navigation now uses native multipage routing. Experiments, notes, animations, and community pages all sit on the same shell."
        )


def render_page_intro(title: str, lead: str, kicker: str | None = None) -> None:
    kicker_html = f'<div class="hero-kicker">{kicker}</div>' if kicker else ""
    st.markdown(
        f"""
        <section>
            {kicker_html}
            <h1 class="page-title">{title}</h1>
            <p class="page-lead">{lead}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(items: Iterable[tuple[str, str]]) -> None:
    item_list = list(items)
    columns = st.columns(len(item_list))
    for column, (label, value) in zip(columns, item_list):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_debug_panel(settings: AppSettings, backend_label: str | None = None) -> None:
    if not settings.debug:
        return
    with st.sidebar.expander("Debug self-check", expanded=False):
        st.write(
            {
                "photo_exists": settings.photo_path.exists(),
                "notes_dir_exists": settings.notes_dir.exists(),
                "notes_catalog_exists": settings.notes_catalog_path.exists(),
                "comment_backend": settings.comment_backend,
                "resolved_backend": backend_label or "pending",
                "supabase_configured": bool(settings.supabase_url and settings.supabase_key),
            }
        )