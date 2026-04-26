from __future__ import annotations

from pathlib import Path

import streamlit as st

from ultramarine.content import FEATURE_CARDS, HOME_INTRO
from ultramarine.data.notes import load_note_entries
from ultramarine.models import AppSettings
from ultramarine.ui import render_metric


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
    visible_pages = max(1, len(registry))

    st.markdown(
        f"""
        <section class="hero-shell">
            <div class="hero-kicker">个人数学空间</div>
            <h1 class="hero-title">{settings.site_title}</h1>
            <p class="hero-lead">{HOME_INTRO}</p>
            <div class="meta-row">
                <div class="metric-card"><div class="metric-label">页面</div><div class="metric-value">{visible_pages}</div></div>
                <div class="metric-card"><div class="metric-label">笔记</div><div class="metric-value">{note_count}</div></div>
                <div class="metric-card"><div class="metric-label">推荐资料</div><div class="metric-value">{featured_count}</div></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        render_metric("Aesthetic", "Dark Lab", "Apple / Vercel 风格暗黑界面")
    with m2:
        render_metric("Compute", "Cached", "重型可视化计算按参数缓存")
    with m3:
        render_metric("Study", "Pure Math", "面向转入纯数学的学习路径")

    st.markdown("## 页面导览")
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
                    label=f"进入 {card.title}",
                    width="stretch",
                )

    st.markdown("## 浏览建议")
    left, right = st.columns([1.15, 0.85])
    with left:
        st.markdown(
            """
            - 如果你想先看动态内容，可以从互动实验室和数学动画开始。
            - 如果你更喜欢静态图形与整体观赏，数学画廊会更合适。
            - 如果你是来查资料，直接进入笔记资料页会更高效。
            """
        )
    with right:
        st.markdown(
            """
            <div class="note-card">
                <div class="note-title">关于这里</div>
                <p class="note-summary">
                    这里更像一间持续更新的个人数学工作室：
                    有图形、有动画、有笔记，也留了一块简洁的交流空间。
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )