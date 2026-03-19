# modules/comments.py
import streamlit as st
import json
import os
from datetime import datetime


# 获取数据库文件路径的统一方法
def get_db_path(project_root):
    return os.path.join(project_root, "data", "comments.json")


# 初始化数据库
def init_db(project_root):
    data_dir = os.path.join(project_root, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    db_file = get_db_path(project_root)
    if not os.path.exists(db_file):
        with open(db_file, "w", encoding="utf-8") as f:
            json.dump([], f)


# 加载评论
def load_comments(project_root):
    db_file = get_db_path(project_root)
    try:
        with open(db_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# 保存评论
def save_comments(project_root, comments):
    db_file = get_db_path(project_root)
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)


def show_comments(project_root):
    st.title("💬 交流广场")
    st.markdown("这里是我们的数学学术讨论区。支持 Markdown 和 **LaTeX 公式渲染**。")

    # 确保数据库存在
    init_db(project_root)
    comments = load_comments(project_root)

    # ==========================================
    # 1. 发布动态区
    # ==========================================
    with st.container():
        st.markdown("### 📝 发布新动态")
        col_avatar, col_input = st.columns([1, 6])

        with col_avatar:
            # 默认头像
            st.image("https://api.dicebear.com/7.x/pixel-art/svg?seed=MathGenius", width=80)

        with col_input:
            user_name = st.text_input("你的昵称", "未来数学家", label_visibility="collapsed")
            new_comment = st.text_area("分享你的数学感悟...", height=100, label_visibility="collapsed")

            if st.button("🚀 发射 (Post)", use_container_width=True):
                if new_comment.strip():
                    new_entry = {
                        "id": datetime.now().timestamp(),  # 使用时间戳作为唯一 ID
                        "user": user_name,
                        "content": new_comment,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "likes": 0
                    }
                    comments.insert(0, new_entry)
                    save_comments(project_root, comments)
                    st.rerun()  # 立即刷新
                else:
                    st.warning("内容不能为空哦！")

    st.divider()

    # ==========================================
    # 2. 动态信息流
    # ==========================================
    st.markdown("### 🌐 最新动态")

    if not comments:
        st.info("广场空空如也，快来发布第一条动态吧！")
        return

    for c in comments:
        with st.container():
            c_avatar, c_content = st.columns([1, 8])

            with c_avatar:
                # 每个用户名字对应一个固定的头像
                seed = c.get('user', 'Guest')
                st.image(f"https://api.dicebear.com/7.x/identicon/svg?seed={seed}", width=60)

            with c_content:
                st.markdown(
                    f"**{c['user']}** <span style='color:#8899A6; font-size:0.85em; margin-left:10px;'>· {c['time']}</span>",
                    unsafe_allow_html=True)
                st.markdown(c['content'])

                # 点赞逻辑
                like_col, _ = st.columns([2, 8])
                with like_col:
                    if st.button(f"❤️ 赞 ({c.get('likes', 0)})", key=f"like_{c['id']}"):
                        c['likes'] = c.get('likes', 0) + 1
                        save_comments(project_root, comments)
                        st.rerun()
        st.markdown("<hr style='margin: 10px 0px; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)