from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

from ultramarine.config import AppSettings
from ultramarine.data.notes import NoteEntry, load_note_entries, read_note_bytes
from ultramarine.ui import render_glass_card, render_page_intro


@st.cache_data(show_spinner=False, ttl=60)
def get_note_catalog(catalog_path: str, notes_dir: str) -> tuple[list[NoteEntry], list[str]]:
    return load_note_entries(Path(catalog_path), Path(notes_dir))


@st.cache_data(show_spinner=False, ttl=60)
def get_note_file_bytes(notes_dir: str, file_name: str) -> bytes:
    return read_note_bytes(Path(notes_dir), file_name)


def render(settings: AppSettings) -> None:
    render_page_intro(
        "笔记资料", "按标签查阅数学课程笔记，为统计、优化与学习实验补充理论基础。", "理论资料"
    )
    notes, missing_files = get_note_catalog(
        str(settings.notes_catalog_path), str(settings.notes_dir)
    )
    if missing_files:
        st.warning(f"清单中有 {len(missing_files)} 个 PDF 缺失，页面已自动跳过。")
    if not notes:
        st.info("当前没有可展示的笔记。")
        return
    all_tags = sorted({tag for note in notes for tag in note.tags})
    selected_tags = st.multiselect("按标签筛选", all_tags, key="notes_selected_tags")
    filtered = [note for note in notes if all(tag in note.tags for tag in selected_tags)]
    if not filtered:
        st.info("没有同时匹配这些标签的笔记，请减少筛选条件。")
        return

    featured = [note for note in filtered if note.featured][:3]
    if featured:
        st.markdown("### 推荐阅读")
        for column, note in zip(st.columns(len(featured)), featured):
            with column:
                render_glass_card(note.title, note.summary, tags=note.tags, class_name="note-card")

    options = {note.slug: note for note in filtered}
    selected_slug = st.selectbox(
        "选择要预览的笔记", list(options), format_func=lambda slug: options[slug].title
    )
    note = options[selected_slug]
    try:
        file_bytes = get_note_file_bytes(str(settings.notes_dir), note.file_name)
    except (OSError, ValueError):
        st.warning("这份笔记暂时无法读取，请选择其他笔记或刷新页面。")
        return
    info, preview = st.columns([1.1, 1.9])
    with info:
        render_glass_card(note.title, note.summary, tags=note.tags, class_name="note-card")
        st.download_button(
            f"下载 {note.title}", file_bytes, file_name=note.file_name, mime="application/pdf"
        )
    with preview:
        with st.expander("在线预览", expanded=True):
            encoded = base64.b64encode(file_bytes).decode("ascii")
            st.markdown(
                f'<iframe title="PDF 笔记预览" src="data:application/pdf;base64,{encoded}" '
                'width="100%" height="820" type="application/pdf"></iframe>',
                unsafe_allow_html=True,
            )
