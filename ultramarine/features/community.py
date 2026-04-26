from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from ultramarine.data.comments import (
    COMMENT_COOLDOWN_SECONDS,
    CommentRepositoryHandle,
    create_comment_repository,
    validate_comment_input,
)
from ultramarine.layout import render_page_intro
from ultramarine.models import AppSettings
from ultramarine.ui import escape, render_feed_header


@st.cache_resource(show_spinner=False)
def get_repository_handle(settings: AppSettings) -> CommentRepositoryHandle:
    return create_comment_repository(settings)


def _friendly_timestamp(value: str) -> str:
    try:
        instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return instant.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return value


def _render_status(handle: CommentRepositoryHandle) -> None:
    if not handle.status_message:
        return
    if handle.repo.is_writable():
        st.success(handle.status_message)
    elif handle.backend_label == "Read-only":
        st.warning(handle.status_message)
    else:
        st.info(handle.status_message)


def render(settings: AppSettings) -> None:
    render_page_intro(
        "交流广场",
        "如果你愿意，可以在这里留下一句想法、问题或阅读感受。",
        kicker="轻量交流",
    )
    handle = get_repository_handle(settings)
    repo = handle.repo
    _render_status(handle)

    st.session_state.setdefault("liked_comment_ids", set())
    st.session_state.setdefault("last_comment_at", 0.0)

    with st.form("community-post-form", clear_on_submit=True):
        nickname = st.text_input("昵称", value=settings.profile_name)
        content = st.text_area("留言内容", height=130, placeholder="分享你最近在思考的数学问题、证明思路或阅读感想。")
        submitted = st.form_submit_button("发布留言", disabled=not repo.is_writable())

    if submitted:
        error = validate_comment_input(nickname, content)
        now = datetime.now(timezone.utc).timestamp()
        if error:
            st.warning(error)
        elif now - float(st.session_state["last_comment_at"]) < COMMENT_COOLDOWN_SECONDS:
            st.warning(f"为了避免刷屏，请等待 {COMMENT_COOLDOWN_SECONDS} 秒后再发送下一条。")
        else:
            repo.create_comment(nickname, content)
            st.session_state["last_comment_at"] = now
            st.success("留言已发布。")
            st.rerun()

    comments = repo.list_comments(limit=50)
    if not comments:
        st.info("留言广场还很安静，欢迎成为第一位留下笔记的人。")
        return

    render_feed_header("最新留言", "支持 Markdown 与代码块，适合留下问题、证明草稿或阅读札记。")
    liked_ids = st.session_state["liked_comment_ids"]
    for comment in comments:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="comment-card" style="box-shadow:none;">
                    <div class="feature-title">● {escape(comment.nickname)}</div>
                    <p class="comment-meta">{escape(_friendly_timestamp(comment.created_at))}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(comment.content)
            if st.button(
                f"赞同 {comment.likes}",
                key=f"like_button_{comment.id}",
                disabled=(not repo.is_writable()) or (comment.id in liked_ids),
            ):
                repo.increment_like(comment.id)
                liked_ids.add(comment.id)
                st.rerun()