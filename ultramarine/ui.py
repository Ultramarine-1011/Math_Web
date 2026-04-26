from __future__ import annotations

import html
from collections.abc import Iterable

import streamlit as st


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def tag_html(tags: Iterable[str]) -> str:
    return "".join(f'<span class="tag">{escape(tag)}</span>' for tag in tags)


def render_glass_card(
    title: str,
    body: str,
    *,
    kicker: str | None = None,
    tags: Iterable[str] = (),
    class_name: str = "feature-card",
) -> None:
    kicker_html = f'<div class="card-kicker">{escape(kicker)}</div>' if kicker else ""
    tag_row = f'<div class="tag-row">{tag_html(tags)}</div>' if tags else ""
    st.markdown(
        f"""
        <div class="{class_name}">
            {kicker_html}
            <div class="feature-title">{escape(title)}</div>
            <p class="feature-summary">{escape(body)}</p>
            {tag_row}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric(label: str, value: str, detail: str | None = None) -> None:
    detail_html = f'<div class="metric-detail">{escape(detail)}</div>' if detail else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{escape(label)}</div>
            <div class="metric-value">{escape(value)}</div>
            {detail_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chart_shell(title: str, caption: str | None = None) -> None:
    caption_html = f'<p class="chart-caption">{escape(caption)}</p>' if caption else ""
    st.markdown(
        f"""
        <div class="chart-shell-title">
            <span>{escape(title)}</span>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_panel(
    title: str,
    *,
    principle: str,
    algorithm: str,
    meaning: str,
    parameters: Iterable[tuple[str, str]] = (),
) -> None:
    parameter_items = "".join(
        f"<li><strong>{escape(label)}</strong>: {escape(value)}</li>" for label, value in parameters
    )
    parameter_html = f"<ul>{parameter_items}</ul>" if parameter_items else ""
    st.markdown(
        f"""
        <div class="insight-panel">
            <div class="card-kicker">Insight Layer</div>
            <h3>{escape(title)}</h3>
            <div class="insight-grid">
                <div>
                    <span>数学原理</span>
                    <p>{escape(principle)}</p>
                </div>
                <div>
                    <span>算法逻辑</span>
                    <p>{escape(algorithm)}</p>
                </div>
                <div>
                    <span>哲学意味</span>
                    <p>{escape(meaning)}</p>
                </div>
            </div>
            {parameter_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feed_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="feed-header">
            <div>
                <div class="card-kicker">Community Feed</div>
                <h3>{escape(title)}</h3>
                <p>{escape(subtitle)}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
