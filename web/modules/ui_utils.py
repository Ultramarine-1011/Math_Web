# modules/ui_utils.py
import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* 隐藏 Streamlit 默认的右上角菜单和底部水印（让网站看起来更专业） */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 全局按钮炫酷渐变色 */
    div.stButton > button:first-child {
        background-image: linear-gradient(to right, #7792E3 0%, #6956EC 51%, #7792E3 100%);
        color: white;
        border: none;
        border-radius: 10px;
        transition: 0.5s;
        background-size: 200% auto;
    }
    div.stButton > button:hover {
        background-position: right center; 
    }

    /* 背景 LaTeX 水印装饰的绝对定位 CSS */
    .bg-latex-watermark {
        position: fixed;
        bottom: -50px;
        right: -30px;
        font-size: 100px;
        color: rgba(255, 255, 255, 0.04); /* 极低透明度，若隐若现 */
        z-index: -100; /* 藏在最底下，不影响点击 */
        pointer-events: none; /* 鼠标穿透 */
        user-select: none; /* 无法选中 */
        transform: rotate(-15deg); /* 倾斜一点更有艺术感 */
    }
    </style>
    """, unsafe_allow_html=True)

def render_latex_decorations():
    # 使用著名的欧拉公式和微积分符号作为背景水印
    watermark_html = """
    <div class="bg-latex-watermark">
        $$ \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi} $$
    </div>
    """
    st.markdown(watermark_html, unsafe_allow_html=True)