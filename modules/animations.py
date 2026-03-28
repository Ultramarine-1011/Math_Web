# modules/animations.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go


def show_animations():
    st.title("🎬 数学动画视界 (WebGL 引擎)")
    st.markdown("这里是动态的数学宇宙。我们通过 **前端 WebGL 引擎渲染 60FPS 动画**，完美重现 3B1B 风格的数学之美。")

    tab1, tab2 = st.tabs(["/  📐 线性代数 (2D 网格基底变换)  /", "/  🍩 微分几何 (拓扑连续形变)  /"])

    # ==========================================
    # 选项卡 1：线性代数 - 2D 实时 + 动画变换
    # ==========================================
    with tab1:
        st.subheader("矩阵即变换：实时交互与动画演示")
        st.markdown(
            "左侧是变换矩阵 $A$。**直接点击修改数值**，观察右侧空间实时响应。或**点击下方播放按钮**，欣赏从单位空间到目标空间的完整变换动画。")

        col_control, col_display = st.columns([2, 3])

        with col_control:
            st.markdown("### 目标变换矩阵 $A$")

            c1, c2 = st.columns(2)
            a11 = c1.number_input("a11", -2.0, 2.0, 1.5, 0.1, label_visibility="collapsed")
            a21 = c1.number_input("a21", -2.0, 2.0, 0.5, 0.1, label_visibility="collapsed")
            a12 = c2.number_input("a12", -2.0, 2.0, 1.0, 0.1, label_visibility="collapsed")
            a22 = c2.number_input("a22", -2.0, 2.0, 1.2, 0.1, label_visibility="collapsed")

            A = np.array([[a11, a12], [a21, a22]])
            I = np.eye(2)  # 单位矩阵

            determinant = np.linalg.det(A)
            st.latex(f"\\det(A) = {determinant:.2f}")
            if determinant < 0:
                st.warning("空间方位被翻转了！(行列式为负)")
            elif abs(determinant) < 0.05:
                st.info("空间被压缩到了一条线或一个点！(行列式接近0)")
            else:
                st.success(f"空间面积被缩放了 {abs(determinant):.2f} 倍。")

            # 【新增】播放按钮现在放在控制区，更符合逻辑
            play_button_placeholder = st.empty()

        with col_display:
            # 1. 生成 2D 基础网格
            x_lines, y_lines = [], []
            for i in range(-5, 6):
                x_lines.extend([i, i, np.nan])
                y_lines.extend([-5, 5, np.nan])
                x_lines.extend([-5, 5, np.nan])
                y_lines.extend([i, i, np.nan])
            grid_pts = np.vstack([x_lines, y_lines])
            pts_clean = np.nan_to_num(grid_pts)

            # 2. 【核心升级】预计算动画的所有帧 (从 I 到 A)
            frames_lin = []
            for t in np.linspace(0, 1, 40):  # 40 帧保证丝滑
                M = (1 - t) * I + t * A  # 线性插值

                # 应用变换
                transformed = M @ pts_clean
                transformed[np.isnan(grid_pts)] = np.nan
                vi = M @ np.array([1, 0])
                vj = M @ np.array([0, 1])

                # 创建这一帧的数据
                frames_lin.append(go.Frame(
                    data=[
                        go.Scatter(x=transformed[0], y=transformed[1]),  # 网格
                        go.Scatter(x=[0, vi[0]], y=[0, vi[1]]),  # i-hat
                        go.Scatter(x=[0, vj[0]], y=[0, vj[1]])  # j-hat
                    ],
                    traces=[0, 1, 2],  # 指定更新哪些 trace
                    name=str(t)
                ))

            # 3. 构建 Plotly 图形
            # 【重要】基础图形(data)现在是用户实时设定的最终状态 A
            # 这样保证了实时交互性，默认显示的就是目标状态
            final_transformed = A @ pts_clean
            final_transformed[np.isnan(grid_pts)] = np.nan
            final_vi = A @ np.array([1, 0])
            final_vj = A @ np.array([0, 1])

            fig_lin = go.Figure(
                data=[
                    go.Scatter(x=final_transformed[0], y=final_transformed[1], mode='lines',
                               line=dict(color='rgba(119, 146, 227, 0.5)', width=2)),
                    go.Scatter(x=[0, final_vi[0]], y=[0, final_vi[1]], mode='lines',
                               line=dict(color='#E74C3C', width=5), name='i-hat'),
                    go.Scatter(x=[0, final_vj[0]], y=[0, final_vj[1]], mode='lines',
                               line=dict(color='#2ECC71', width=5), name='j-hat')
                ],
                frames=frames_lin  # 把我们算好的动画帧塞进去
            )

            # 【重要】按钮的逻辑在这里实现
            fig_lin.update_layout(
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(
                        label="▶️ 播放变换动画",
                        method="animate",
                        args=[
                            None,  # None 表示从头播放所有帧
                            {
                                "frame": {"duration": 40, "redraw": True},  # 每帧40毫秒
                                "fromcurrent": False,  # False 表示从第0帧开始，而不是从当前状态
                                "transition": {"duration": 30, "easing": "quadratic-in-out"}  # 帧之间的平滑过渡
                            }
                        ]
                    )],
                    # 调整按钮位置和样式
                    x=0.5, xanchor="center", y=-0.1, yanchor="top"
                )],
                xaxis=dict(range=[-8, 8], showgrid=False, zeroline=True, zerolinecolor='rgba(255,255,255,0.5)'),
                yaxis=dict(range=[-8, 8], showgrid=False, zeroline=True, zerolinecolor='rgba(255,255,255,0.5)',
                           scaleanchor="x", scaleratio=1),
                height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                margin=dict(l=10, r=10, b=10, t=10)
            )

            st.plotly_chart(fig_lin, use_container_width=True)

    # ==========================================
    # 选项卡 2：拓扑形变 (原生 3D 动画丝滑版)
    # ==========================================
    with tab2:
        st.subheader("连续等距形变 (悬链曲面 🔄 螺旋曲面)")

        # 预计算曲面的参数网格
        u = np.linspace(-np.pi, np.pi, 50)
        v = np.linspace(-2, 2, 50)
        U, V = np.meshgrid(u, v)

        # 预计算动画帧
        frames_top = []
        for theta in np.linspace(0, np.pi / 2, 40):
            X = np.cos(theta) * np.sinh(V) * np.sin(U) + np.sin(theta) * np.cosh(V) * np.cos(U)
            Y = -np.cos(theta) * np.sinh(V) * np.cos(U) + np.sin(theta) * np.cosh(V) * np.sin(U)
            Z = U * np.cos(theta) + V * np.sin(theta)
            frames_top.append(go.Frame(data=[go.Surface(x=X, y=Y, z=Z)], traces=[0]))

        # 获取初始帧 (theta = 0) 作为底图
        X0 = np.sinh(V) * np.sin(U)
        Y0 = -np.sinh(V) * np.cos(U)
        Z0 = U

        fig_top = go.Figure(
            data=[go.Surface(x=X0, y=Y0, z=Z0, colorscale='Magma', showscale=False)],
            frames=frames_top
        )

        # 严格固定坐标轴范围，彻底杜绝曲面变形时的镜头抖动
        fig_top.update_layout(
            updatemenus=[dict(type="buttons", buttons=[dict(label="▶️", method="animate", args=[None, {
                "frame": {"duration": 60, "redraw": True}, "fromcurrent": True}])])],
            scene=dict(
                xaxis=dict(range=[-4, 4], visible=False),
                yaxis=dict(range=[-4, 4], visible=False),
                zaxis=dict(range=[-4, 4], visible=False),
                camera=dict(eye=dict(x=1.2, y=1.2, z=0.5))
            ),
            height=600, margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_top, use_container_width=True)