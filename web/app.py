# app.py - 你的个人数学宇宙的总入口

import streamlit as st
import os

# ==========================================
# 1. 页面级全局配置 (必须是第一行执行的配置)
# ==========================================
st.set_page_config(page_title="Ultramarine的数学宇宙", page_icon="🌌", layout="wide")

# ==========================================
# 2. 【核心逻辑】定义唯一的项目根目录 (Single Source of Truth)
# 这是解决云端“找不到文件”错误的终极方案
# 无论代码被放在服务器的哪个角落，它都能准确找到自己所在的目录
# ==========================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# 3. 导入我们的模块 (积木块)
# ==========================================
from modules.ui_utils import load_css, render_latex_decorations
from modules.interactive import show_interactive
from modules.static_gallery import show_gallery
from modules.animations import show_animations
from modules.notes import show_notes
from modules.comments import show_comments

# ==========================================
# 4. 加载全局 UI 装饰
# ==========================================
load_css()  # 加载自定义的 CSS 外衣
render_latex_decorations()  # 在背景角落贴上微积分公式水印

# ==========================================
# 5. 侧边栏与导航控制器
# ==========================================
with st.sidebar:
    # 绝对路径引用图片，确保云端永远不会报错
    photo_path = os.path.join(PROJECT_ROOT, "photo.jpg")
    # 如果图片不存在（比如还没上传），提供一个兜底方案
    if os.path.exists(photo_path):
        st.image(photo_path, caption="Congkai Liu (Ultramarine)",  width="stretch")
    else:
        st.image("https://api.dicebear.com/7.x/shapes/svg?seed=Ultramarine", caption="Congkai Liu",
                 width="stretch")

    st.title("控制中枢")

    # 导航栏
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
# 6. 路由系统 (根据选择，精准调度对应的模块)
# ==========================================

if menu == "🏠 主页 (交互实验)":
    # 交互实验模块，不需要文件系统 IO，不需要传根目录
    show_interactive()

elif menu == "🖼️ 静态画廊":
    # 画廊模块
    show_gallery()

elif menu == "🎬 数学动画":
    # 动画模块
    show_animations()

elif menu == "📚 笔记资源":
    # 传入“尚方宝剑”：项目根目录
    show_notes(PROJECT_ROOT)

elif menu == "💬 交流广场":
    # 传入“尚方宝剑”：项目根目录，以便它找到 data/comments.json
    show_comments(PROJECT_ROOT)