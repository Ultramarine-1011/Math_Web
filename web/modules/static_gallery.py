# modules/static_gallery.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import plotly.graph_objects as go  # 引入高端 3D 交互绘图库


def show_gallery():
    st.markdown("这里陈列了经典的数学几何图形。你可以**使用鼠标拖动、缩放**，全方位欣赏数学的结构之美。")

    # 创建两个选项卡
    tab1, tab2 = st.tabs(["🦋 洛伦兹吸引子 (3D交互)", "❤️ 心形代数曲线 (极简美学)"])

    # ==========================================
    # 选项卡 1：洛伦兹吸引子 (使用 Plotly 渲染 WebGL 3D)
    # ==========================================
    with tab1:
        st.subheader("洛伦兹吸引子 (Lorenz Attractor)")
        # 加上一点数学公式装点门面
        st.latex(r"""
        \begin{cases} 
        \frac{dx}{dt} = \sigma(y-x) \\ 
        \frac{dy}{dt} = x(\rho-z)-y \\ 
        \frac{dz}{dt} = xy-\beta z 
        \end{cases}
        """)

        # 虽然是“静态画廊”，但我们可以给点小福利，让用户微调参数
        col1, col2, col3 = st.columns(3)
        sigma = col1.slider("参数 sigma", 5.0, 15.0, 10.0)
        rho = col2.slider("参数 rho", 10.0, 40.0, 28.0)
        beta = col3.slider("参数 beta", 1.0, 5.0, 2.667)

        # 1. 数学求解核心
        def lorenz_system(state, t):
            x, y, z = state
            return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

        t = np.linspace(0, 50, 5000)  # 生成 5000 个点，保证曲线平滑
        state0 = [1.0, 1.0, 1.0]
        solution = odeint(lorenz_system, state0, t)

        X, Y, Z = solution[:, 0], solution[:, 1], solution[:, 2]

        # 2. 使用 Plotly 构建极具现代感的 3D 图
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=X, y=Y, z=Z,
            mode='lines',
            line=dict(
                color=t,  # 颜色随时间 t 变化（产生漂亮的渐变色）
                colorscale='Plasma',  # 科技感渐变色系
                width=3  # 线条粗细
            )
        )])

        # 3. 美化 3D 空间（隐藏丑陋的网格和坐标轴背景，突出图形本身）
        fig_3d.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),  # 去掉多余白边
            paper_bgcolor='rgba(0,0,0,0)',  # 背景完全透明
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, title=''),
                yaxis=dict(showbackground=False, showticklabels=False, title=''),
                zaxis=dict(showbackground=False, showticklabels=False, title='')
            ),
            height=600  # 设定高度
        )

        # 将 Plotly 图表渲染到网页上
        st.plotly_chart(fig_3d, use_container_width=True)
        st.caption("💡 提示：按住鼠标左键拖动可以旋转三维空间，滚轮可以缩放。")

    # ==========================================
    # 选项卡 2：心形函数 (使用 Matplotlib 极简渲染)
    # ==========================================
    with tab2:
        st.subheader("心形线 (Heart Curve)")
        st.latex(r"""
        \begin{cases} 
        x = 16 \sin^3(t) \\ 
        y = 13 \cos(t) - 5 \cos(2t) - 2 \cos(3t) - \cos(4t) 
        \end{cases}
        """)

        # 1. 生成数据
        t_heart = np.linspace(0, 2 * np.pi, 1000)
        x_heart = 16 * np.sin(t_heart) ** 3
        y_heart = 13 * np.cos(t_heart) - 5 * np.cos(2 * t_heart) - 2 * np.cos(3 * t_heart) - np.cos(4 * t_heart)

        # 2. 绘图 (制造“发光”的艺术感)
        fig_heart, ax_heart = plt.subplots(figsize=(6, 6))

        # 画外边缘
        ax_heart.plot(x_heart, y_heart, color='#E74C3C', linewidth=3)
        # 填充内部，设置透明度
        ax_heart.fill(x_heart, y_heart, color='#E74C3C', alpha=0.3)

        # 3. 极简美学设置
        ax_heart.axis('equal')  # 保证心形不变形
        ax_heart.axis('off')  # 彻底隐藏坐标轴和边框，呈现艺术画作的感觉

        fig_heart.patch.set_alpha(0.0)
        ax_heart.patch.set_alpha(0.0)

        # 渲染到网页
        st.pyplot(fig_heart)
        st.caption("源自极坐标系与三角函数的极致浪漫。")