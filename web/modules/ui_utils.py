# modules/ui_utils.py
import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* 1. 按钮透明度优化：使用 rgba (红, 绿, 蓝, 透明度) */
    /* Alpha 设为 0.2，即 20% 的透明度，看起来更高级、不刺眼 */
    button {
        background-color: rgba(119, 146, 227, 0.2) !important;
        color: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        transition: 0.3s !important;
    }
    button:hover {
        background-color: rgba(119, 146, 227, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    /* 2. 让公式水印更加优雅 */
    .latex-watermark {
        position: fixed;
        bottom: 20px;
        right: 20px;
        opacity: 0.1; /* 10% 透明度 */
        z-index: 0;
        pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)

def render_latex_decorations():
    # 改用 streamlit 原生的 st.latex()，它会自动调用 KaTeX 渲染
    # 我们用一个 div 包裹它，并赋予刚才定义好的 CSS 类名
    st.markdown('<div class="latex-watermark">', unsafe_allow_html=True)
    st.latex(r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}")
    st.markdown('</div>', unsafe_allow_html=True)