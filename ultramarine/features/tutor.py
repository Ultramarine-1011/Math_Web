from __future__ import annotations

from pathlib import Path

import streamlit as st

from ultramarine.ai import call_chat_completion
from ultramarine.data.notes import load_note_entries
from ultramarine.layout import render_page_intro
from ultramarine.models import AppSettings, NoteEntry
from ultramarine.ui import render_glass_card


SYSTEM_PROMPT = """
你是 Ultramarine 数学博物馆里的 AI 数学助教。用户有 IC 工程背景，正在转入纯数学。
回答应当严谨、简洁、鼓励证明思维；遇到复杂证明时先给路线图，再给关键步骤。
如果相关主题出现在笔记清单里，请主动建议用户去笔记页查阅。
请输出标准 Markdown：标题用 ##，列表用 -，公式用 $...$ 或 $$...$$，代码块使用三反引号。
不要把整段回答包在一个 markdown 代码围栏里。
""".strip()


@st.cache_data(show_spinner=False)
def cached_notes(catalog_path: str, notes_dir: str) -> list[NoteEntry]:
    notes, _ = load_note_entries(Path(catalog_path), Path(notes_dir))
    return notes


def build_note_context(notes: list[NoteEntry]) -> str:
    lines = [
        f"- {note.title}: {note.summary} 标签={', '.join(note.tags)}"
        for note in notes[:12]
    ]
    return "\n".join(lines)


def render(settings: AppSettings) -> None:
    render_page_intro(
        "AI 数学助教",
        "把概念解释、证明提示、学习路线和本站笔记连接起来，作为进入纯数学的随身白板。",
        kicker="Study Copilot",
    )

    notes = cached_notes(str(settings.notes_catalog_path), str(settings.notes_dir))
    context = build_note_context(notes)
    st.session_state.setdefault(
        "tutor_messages",
        [
            {
                "role": "assistant",
                "content": "可以问我一个概念、证明思路或学习路线问题。我会尽量给出结构化提示。",
            }
        ],
    )

    status_col, prompt_col = st.columns([0.85, 1.35])
    with status_col:
        if settings.llm_api_key:
            render_glass_card(
                "在线模型已启用",
                f"当前模型：{settings.llm_model}。对话历史保存在本次浏览会话中。",
                kicker="LLM Ready",
                tags=("证明提示", "学习路径", "笔记导航"),
            )
        else:
            render_glass_card(
                "离线演示模式",
                "未配置 LLM_API_KEY 或 OPENAI_API_KEY，因此这里展示对话界面和推荐问题。",
                kicker="No API Key",
                tags=("安全部署", "可选功能"),
            )
        st.markdown("#### 推荐问题")
        for question in (
            "实变函数中为什么需要测度？",
            "线性代数里的对偶空间怎么直观理解？",
            "从 IC 背景转纯数学，第一学期如何安排分析与代数？",
        ):
            if st.button(question, key=f"sample_{question}"):
                st.session_state["tutor_messages"].append({"role": "user", "content": question})
                st.rerun()

    with prompt_col:
        for message in st.session_state["tutor_messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_prompt = st.chat_input("输入你的数学问题")
        if user_prompt:
            st.session_state["tutor_messages"].append({"role": "user", "content": user_prompt})
            if settings.llm_api_key:
                messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT + "\n\n本站笔记清单：\n" + context,
                    },
                    *st.session_state["tutor_messages"][-8:],
                ]
                with st.spinner("助教正在推导..."):
                    try:
                        answer = call_chat_completion(
                            base_url=settings.llm_base_url,
                            api_key=settings.llm_api_key,
                            model=settings.llm_model,
                            messages=messages,
                        )
                    except RuntimeError as exc:
                        answer = f"模型暂时不可用：{exc}"
            else:
                answer = (
                    "当前未配置模型密钥。建议先把问题拆成：定义、例子、反例、证明目标。"
                    "如果问题涉及本站笔记，可以从「笔记资料」页按标签检索。"
                )
            st.session_state["tutor_messages"].append({"role": "assistant", "content": answer})
            st.rerun()
