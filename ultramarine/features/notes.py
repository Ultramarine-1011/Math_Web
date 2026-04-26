from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

from ultramarine.data.notes import load_note_entries
from ultramarine.layout import render_page_intro
from ultramarine.models import AppSettings, NoteEntry


@st.cache_data(show_spinner=False)
def get_note_catalog(catalog_path: str, notes_dir: str) -> tuple[list[NoteEntry], list[str]]:
    return load_note_entries(Path(catalog_path), Path(notes_dir))


@st.cache_data(show_spinner=False)
def get_note_file_bytes(notes_dir: str, file_name: str) -> bytes:
    return (Path(notes_dir) / file_name).read_bytes()


@st.cache_data(show_spinner=False)
def encode_pdf(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode("utf-8")


def render(settings: AppSettings) -> None:
    render_page_intro(
        "笔记资料",
        "这里整理了我目前收集和撰写的课程笔记。你可以按标签筛选，也可以直接在线预览。",
        kicker="资料整理",
    )

    notes, missing_files = get_note_catalog(
        str(settings.notes_catalog_path),
        str(settings.notes_dir),
    )
    if missing_files:
        st.warning(f"清单中有 {len(missing_files)} 个 PDF 缺失，页面已自动跳过。")

    if not notes:
        st.info("当前还没有可展示的笔记，请先补充 `data/notes_catalog.json` 和 PDF 文件。")
        return

    all_tags = sorted({tag for note in notes for tag in note.tags})
    selected_tags = st.multiselect("按标签筛选", all_tags, key="notes_selected_tags")
    filtered_notes = [
        note for note in notes if not selected_tags or all(tag in note.tags for tag in selected_tags)
    ]

    featured_notes = [note for note in filtered_notes if note.featured]
    if featured_notes:
        st.markdown("### 推荐阅读")
        columns = st.columns(min(3, len(featured_notes)))
        for column, note in zip(columns, featured_notes[:3]):
            with column:
                st.markdown(
                    f"""
                    <div class="note-card">
                        <div class="note-title">★ {note.title}</div>
                        <p class="note-summary">{note.summary}</p>
                        <div class="tag-row">{"".join(f'<span class="tag">{tag}</span>' for tag in note.tags)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("### 浏览全部笔记")
    options = {note.slug: note for note in filtered_notes}
    selected_slug = st.selectbox(
        "选择要预览的笔记",
        list(options.keys()),
        format_func=lambda slug: options[slug].title,
    )
    selected_note = options[selected_slug]
    file_bytes = get_note_file_bytes(str(settings.notes_dir), selected_note.file_name)

    info_col, detail_col = st.columns([1.1, 1.9])
    with info_col:
        st.markdown(
            f"""
            <div class="note-card">
                <div class="note-title">{selected_note.title}</div>
                <p class="note-summary">{selected_note.summary}</p>
                <div class="tag-row">{"".join(f'<span class="tag">{tag}</span>' for tag in selected_note.tags)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            label=f"下载 {selected_note.title}",
            data=file_bytes,
            file_name=selected_note.file_name,
            mime="application/pdf",
        )

    with detail_col:
        with st.expander("在线预览", expanded=True):
            base64_pdf = encode_pdf(file_bytes)
            st.markdown(
                f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="820" type="application/pdf"></iframe>',
                unsafe_allow_html=True,
            )