from __future__ import annotations

import streamlit as st

from ultramarine.config import AppSettings
from ultramarine.content import FEATURE_CARDS, HOME_INTRO, SITE_BLURB
from ultramarine.data.notes import load_note_entries
from ultramarine.ui import escape, render_glass_card, render_metric


def render(settings: AppSettings) -> None:
    notes, _ = load_note_entries(settings.notes_catalog_path, settings.notes_dir)
    registry = st.session_state.get("_page_registry", {})
    st.markdown(
        f'<section class="hero-shell"><div class="hero-kicker">{SITE_BLURB}</div>'
        f'<h1 class="hero-title">{escape(settings.site_title)}</h1>'
        f'<p class="hero-lead">{HOME_INTRO}</p></section>',
        unsafe_allow_html=True,
    )
    for column, label, value, detail in zip(
        st.columns(3),
        ("探索空间", "理论资料", "实验方法"),
        (str(len(FEATURE_CARDS) + 1), f"{len(notes)} 份笔记", "可复现"),
        ("数学、统计与机器学习", "保留原有 PDF 与课程标签", "记录参数、种子与数值结果"),
    ):
        with column:
            render_metric(label, value, detail)

    st.markdown("## 选择一个实验入口")
    columns = st.columns(2)
    for index, card in enumerate(FEATURE_CARDS):
        with columns[index % 2]:
            render_glass_card(card.title, card.summary + card.detail)
            if card.path in registry:
                st.page_link(
                    registry[card.path], label=f"进入 {card.title}", icon=card.icon, width="stretch"
                )

    st.markdown("## 从原理出发")
    st.markdown(
        "- **概率与推断**：先用伽尔顿板对照二项分布，再观察置信区间的长期覆盖率。\n"
        "- **优化与学习**：先观察非凸函数的梯度下降，再用回归实验比较迭代解、解析解与测试误差。\n"
        "- **结构与几何**：从线性变换到复变映射、分形与数学画廊，结合笔记理解公式。"
    )
