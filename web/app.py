# app.py
import os
import streamlit as st

# ==========================================
# 1. 页面级全局配置 (必须是第一行代码)
# ==========================================
st.set_page_config(page_title="Ultramarine的数学宇宙", page_icon="🌌", layout="wide")

# ==========================================
# 2. 导入我们的积木模块
# ==========================================
from modules.ui_utils import load_css, render_latex_decorations
from modules.interactive import show_interactive
from modules.static_gallery import show_gallery
from modules.animations import show_animations
from modules.notes import show_notes
from modules.comments import show_comments

# ==========================================
# 3. 加载全局 UI 装饰
# ==========================================
load_css()  # 加载自定义的 CSS 外衣
render_latex_decorations()  # 在背景角落贴上微积分公式水印

# ==========================================
# 4. 侧边栏与导航控制器
# ==========================================
with st.sidebar:
    # 1. 动态获取当前 app.py 所在的绝对目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. 把目录路径和图片名字拼起来，形成绝对路径
    img_path = os.path.join(current_dir, "photo.jpg")

    # 3. 显示图片
    st.image(img_path, use_container_width=True)

    st.header("控制面板")

    # 无比清爽的单选框导航
    menu = st.radio(
        "数字导航仪",
        (
            "🏠 主页 (交互实验)",
            "🖼️ 静态画廊",
            "🎬 数学动画",
            "📚 笔记资源",
            "💬 交流广场"
        )
    )

# ==========================================
# 5. 路由系统 (根据用户选择，挂载不同的模块)
# ==========================================
if menu == "🏠 主页 (交互实验)":
    show_interactive()

elif menu == "🖼️ 静态画廊":
    show_gallery()

elif menu == "🎬 数学动画":
    show_animations()

elif menu == "📚 笔记资源":
    show_notes()

elif menu == "💬 交流广场":
    show_comments()