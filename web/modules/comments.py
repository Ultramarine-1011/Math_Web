# modules/comments.py
import streamlit as st
import json
import os
from datetime import datetime

# 定义数据库文件存放路径
DATA_FILE = "data/comments.json"


# 初始化数据库函数
def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_FILE):
        # 如果文件不存在，创建一个空的列表
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


# 加载评论
def load_comments():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# 保存评论
def save_comments(comments):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)


def show_comments():
    st.title("💬 交流广场 (Math & Code Space)")
    st.markdown(
        "这里是我们的数字黑板。你可以用 Markdown 语法在这里分享你的灵感，甚至**直接写 LaTeX 数学公式**（用 `$$` 包裹即可）。")

    init_db()
    comments = load_comments()

    # ==========================================
    # 1. 发布动态区 (Twitter 发推风格)
    # ==========================================
    with st.container():
        st.markdown("### 📝 发布新动态")
        col_avatar, col_input = st.columns([1, 6])

        with col_avatar:
            # 使用开箱即用的 DiceBear API，根据用户名生成随机的像素化头像！
            st.image("https://api.dicebear.com/7.x/pixel-art/svg?seed=MathGenius", width=80)

        with col_input:
            user_name = st.text_input("你的昵称", "未来数学家", label_visibility="collapsed")
            new_comment = st.text_area("有什么新推演或发现？", height=100, label_visibility="collapsed")

            if st.button("🚀 发射 (Post)", use_container_width=True):
                if new_comment.strip():
                    new_entry = {
                        "id": len(comments) + 1,
                        "user": user_name,
                        "content": new_comment,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "likes": 0
                    }
                    # 将新评论插到列表最前面，最新发布的在最上面
                    comments.insert(0, new_entry)
                    save_comments(comments)
                    st.success("发布成功！")
                    st.rerun()  # 立即刷新页面以显示最新评论
                else:
                    st.warning("内容不能为空哦！写个 $E=mc^2$ 也行呀。")

    st.divider()

    # ==========================================
    # 2. 动态信息流 (Twitter Feed 风格)
    # ==========================================
    st.markdown("### 🌐 最新动态广场")

    if not comments:
        st.info("广场空空如也，快来发布第一条动态吧！")
        return

    # 遍历显示所有评论
    for c in comments:
        with st.container():
            # 为每条评论分配头像和内容区
            c_avatar, c_content = st.columns([1, 8])

            with c_avatar:
                # 传入评论者的名字作为 seed，这样同一个人每次发言头像都是固定的！
                seed = c.get('user', 'Guest')
                st.image(f"https://api.dicebear.com/7.x/identicon/svg?seed={seed}", width=60)

            with c_content:
                # 显示名字和时间 (使用 HTML 控制样式)
                st.markdown(
                    f"**{c['user']}** <span style='color:#8899A6; font-size:0.85em; margin-left:10px;'>· {c['time']}</span>",
                    unsafe_allow_html=True)

                # 显示评论正文 (支持 Markdown 和 LaTeX)
                st.markdown(c['content'])

                # 点赞按钮区
                like_col, _ = st.columns([2, 8])
                with like_col:
                    # 使用评论的唯一 ID 作为 key，防止按钮冲突
                    if st.button(f"❤️ 赞 ({c.get('likes', 0)})", key=f"like_{c['id']}"):
                        c['likes'] = c.get('likes', 0) + 1
                        save_comments(comments)
                        st.rerun()  # 点击后刷新，爱心数立即+1

        # 评论之间的分割线
        st.markdown("<hr style='margin: 10px 0px; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)