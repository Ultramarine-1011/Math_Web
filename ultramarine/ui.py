from __future__ import annotations

import csv
import html
import io
from collections.abc import Iterable

import streamlit as st

from ultramarine.config import AppSettings
from ultramarine.content import SITE_BLURB


def download_experiment(
    name: str, columns: dict, parameters: dict, *, label: str = "下载实验 CSV（含参数）"
) -> None:
    """Include the parameters on every CSV row so exported results can be replayed."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([*parameters, *columns])
    for row in zip(*columns.values(), strict=True):
        writer.writerow([*parameters.values(), *row])
    st.download_button(
        label,
        output.getvalue().encode("utf-8-sig"),
        file_name=f"{name}.csv",
        mime="text/csv",
        key=f"download_{name}",
    )


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_sidebar(settings: AppSettings) -> None:
    with st.sidebar:
        if settings.photo_path.is_file():
            st.image(str(settings.photo_path), width="stretch")
        render_glass_card(
            settings.profile_name,
            SITE_BLURB,
            kicker="Ultramarine Lab",
            class_name="sidebar-card",
        )
        st.caption("调整参数 · 对照理论 · 记录结果")


def render_debug_panel(settings: AppSettings) -> None:
    if settings.debug:
        with st.sidebar.expander("开发自检"):
            st.write(
                {
                    "photo_exists": settings.photo_path.is_file(),
                    "notes_dir_exists": settings.notes_dir.is_dir(),
                    "notes_catalog_exists": settings.notes_catalog_path.is_file(),
                }
            )


def render_page_intro(title: str, lead: str, kicker: str | None = None) -> None:
    kicker_html = f'<div class="hero-kicker">{escape(kicker)}</div>' if kicker else ""
    st.markdown(
        f'<section>{kicker_html}<h1 class="page-title">{escape(title)}</h1>'
        f'<p class="page-lead">{escape(lead)}</p></section>',
        unsafe_allow_html=True,
    )


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
        f'<div class="{escape(class_name)}">{kicker_html}'
        f'<div class="feature-title">{escape(title)}</div>'
        f'<p class="feature-summary">{escape(body)}</p>{tag_row}</div>',
        unsafe_allow_html=True,
    )


def render_metric(label: str, value: str, detail: str | None = None) -> None:
    detail_html = f'<div class="metric-detail">{escape(detail)}</div>' if detail else ""
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{escape(label)}</div>'
        f'<div class="metric-value">{escape(value)}</div>{detail_html}</div>',
        unsafe_allow_html=True,
    )


def render_chart_shell(title: str, caption: str | None = None) -> None:
    caption_html = f'<p class="chart-caption">{escape(caption)}</p>' if caption else ""
    st.markdown(
        f'<div class="chart-shell-title"><span>{escape(title)}</span>{caption_html}</div>',
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
    sections = "".join(
        f"<div><span>{label}</span><p>{escape(text)}</p></div>"
        for label, text in (("数学原理", principle), ("算法逻辑", algorithm), ("如何理解", meaning))
    )
    st.markdown(
        '<div class="insight-panel"><div class="card-kicker">实验说明</div>'
        f'<h3>{escape(title)}</h3><div class="insight-grid">{sections}</div>'
        f"{parameter_html}</div>",
        unsafe_allow_html=True,
    )
