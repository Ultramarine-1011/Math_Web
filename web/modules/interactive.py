# modules/interactive.py
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
import time  # 我们需要 time 来控制循环
from scipy.stats import binom


def show_interactive():
    st.title("🏠 主页：实时交互实验室")
    st.markdown(
        "这里是数学与代码完美交融的地方。基于 **WebGL** 和 **HTML5 Canvas** 的底层渲染，体验原生 60FPS 的丝滑演算。")

    tab1, tab2, tab3 = st.tabs(
        ["/  🌀 傅里叶级数 (高阶锯齿波)  /", "/  🏔️ 2D 梯度下降 (WebGL 丝滑版)  /", "/  🎱 高尔顿板 (50槽扩容版)  /"])

    # ==========================================
    # 选项卡 1：傅里叶级数 (这部分不变)
    # ==========================================
    with tab1:
        st.subheader("傅里叶级数：用圆画出一切 (锯齿波版)")
        st.markdown(
            r"挑战复杂的**锯齿波 (Sawtooth Wave)**。它包含了**所有整数次谐波** ($n=1,2,3...$)，你可以看到极其密集的“本轮”系统。")
        n_circles = st.slider("选择展开的项数 (圆的个数 N)", 1, 100, 10, key="fourier_n")

        html_code = f"""
        <canvas id="fourierCanvas" width="800" height="300" style="background-color: #0E1117; border-radius: 10px;"></canvas>
        <script>
            const canvas = document.getElementById('fourierCanvas');
            const ctx = canvas.getContext('2d');
            let time = 0; let wave =[];
            const n_circles = {n_circles}; 

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                let x = 200; let y = 150;
                for (let i = 0; i < n_circles; i++) {{
                    let prevx = x; let prevy = y;
                    let n = i + 1; 
                    let radius = 70 * (2 / (n * Math.PI)) * (n % 2 === 0 ? -1 : 1);
                    x += radius * Math.cos(n * time); y += radius * Math.sin(n * time);
                    ctx.beginPath(); ctx.arc(prevx, prevy, Math.abs(radius), 0, 2 * Math.PI); ctx.strokeStyle = "rgba(119, 146, 227, 0.3)"; ctx.lineWidth = 1; ctx.stroke();
                    ctx.beginPath(); ctx.moveTo(prevx, prevy); ctx.lineTo(x, y); ctx.strokeStyle = "rgba(255, 255, 255, 0.7)"; ctx.stroke();
                }}
                wave.unshift(y);
                ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(400, wave[0]); ctx.strokeStyle = "rgba(231, 76, 60, 0.5)"; ctx.setLineDash([5, 5]); ctx.stroke(); ctx.setLineDash([]);
                ctx.beginPath();
                for (let i = 0; i < wave.length; i++) {{ ctx.lineTo(i + 400, wave[i]); }}
                ctx.strokeStyle = "#41E08E"; ctx.lineWidth = 2; ctx.stroke();
                if (wave.length > 500) wave.pop();
                time += 0.03; requestAnimationFrame(draw); 
            }}
            draw();
        </script>
        """
        components.html(html_code, height=320)

        # ==========================================
        # 选项卡 2：2D 梯度下降 (Plotly 原生动画，彻底告别闪烁)
        # ==========================================
        with tab2:
            st.subheader("高维空间寻优：2D 梯度下降")
            col1, col2 = st.columns(2)
            lr = col1.slider("学习率 (Alpha)", 0.01, 0.3, 0.08, key="lr2d")
            start_pt = col2.selectbox("初始降落点", ["山顶区域 (-4, -4)", "半山腰 (3, 4)", "悬崖边 (0, -4)"])

            if "山顶" in start_pt:
                x0, y0 = -4.0, -4.0
            elif "半山腰" in start_pt:
                x0, y0 = 3.0, 4.0
            else:
                x0, y0 = 0.0, -4.0

            def f(x, y):
                return (x ** 2 + y ** 2) / 10 + np.sin(x) + np.cos(y)

            def df_dx(x, y):
                return x / 5 + np.cos(x)

            def df_dy(x, y):
                return y / 5 - np.sin(y)

            X_grid = np.linspace(-5, 5, 50)
            Y_grid = np.linspace(-5, 5, 50)
            X_mesh, Y_mesh = np.meshgrid(X_grid, Y_grid)
            Z_mesh = f(X_mesh, Y_mesh)

            # 提前算好 30 步的全部轨迹
            traj_x, traj_y, traj_z = [x0], [y0], [f(x0, y0)]
            curr_x, curr_y = x0, y0
            for _ in range(30):
                curr_x = curr_x - lr * df_dx(curr_x, curr_y)
                curr_y = curr_y - lr * df_dy(curr_x, curr_y)
                traj_x.append(curr_x)
                traj_y.append(curr_y)
                traj_z.append(f(curr_x, curr_y))

            # 构建 Plotly 原生动画帧 (Frames)
            frames = []
            for i in range(len(traj_x)):
                frames.append(go.Frame(
                    data=[
                        go.Scatter3d(x=traj_x[:i + 1], y=traj_y[:i + 1], z=traj_z[:i + 1]),  # 更新红线
                        go.Scatter3d(x=[traj_x[i]], y=[traj_y[i]], z=[traj_z[i]])  # 更新金球
                    ],
                    traces=[1, 2],  # 指定只更新数据中的第 1、2 个轨迹 (不重绘画布曲面，提升性能)
                    name=str(i)
                ))

            # 构建基础图形
            fig = go.Figure(
                data=[
                    go.Surface(x=X_mesh, y=Y_mesh, z=Z_mesh, colorscale='Viridis', opacity=0.6, showscale=False),
                    # Trace 0
                    go.Scatter3d(x=[traj_x[0]], y=[traj_y[0]], z=[traj_z[0]], mode='lines',
                                 line=dict(color='red', width=5)),  # Trace 1
                    go.Scatter3d(x=[traj_x[0]], y=[traj_y[0]], z=[traj_z[0]], mode='markers',
                                 marker=dict(size=8, color='gold'))  # Trace 2
                ],
                frames=frames
            )

            # 添加 WebGL 原生播放按钮，并严格固定 3D 坐标轴范围，防止抖动
            fig.update_layout(
                updatemenus=[dict(type="buttons", buttons=[dict(label="▶️", method="animate", args=[None, {
                    "frame": {"duration": 100, "redraw": True}, "fromcurrent": True}])])],
                scene=dict(
                    xaxis=dict(range=[-5, 5], visible=False),
                    yaxis=dict(range=[-5, 5], visible=False),
                    zaxis=dict(range=[-2, 8], visible=False),  # 严格固定 Z 轴
                    camera=dict(eye=dict(x=1.5, y=1.5, z=0.5))
                ),
                margin=dict(l=0, r=0, b=0, t=0), height=500, paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

        # ==========================================
        # 选项卡 3：高尔顿板 (统计学模拟)
        # ==========================================
    with tab3:
        st.subheader("秩序诞生于混沌：高尔顿板模拟")
        st.markdown(
            "无数个随机掉落的小球，每次向左向右的概率均为 50%。不可预知的个体命运，最终竟然汇聚成完美的**正态分布 (Normal Distribution)**。")

        num_balls = st.slider("释放小球总数", 100, 5000, 1000, step=100)
        num_levels = 20  # 20层钉子，产生 21 个柱子

        if st.button("▶️ 释放小球"):
            bar_spot = st.empty()
            # 记录 21 个槽位的球数
            bins = np.zeros(num_levels + 1)

            # 为了网页流畅，我们分批掉落（每次掉 50 个），而不是一个一个掉
            batch_size = 50
            for _ in range(num_balls // batch_size):
                # 矩阵化随机模拟：50个球，每个球走 20 层，向右为1，向左为0
                # 求和就是最后落入的槽位索引！极其优雅的数学实现。
                drops = np.random.randint(0, 2, size=(batch_size, num_levels))
                final_positions = np.sum(drops, axis=1)

                # 将这批球的最终位置加入统计槽中
                for pos in final_positions:
                    bins[pos] += 1

                # 用 Plotly 画出动态柱状图
                fig_bar = go.Figure(data=[go.Bar(
                    x=list(range(num_levels + 1)), y=bins,
                    marker_color='#41E08E', opacity=0.8
                )])

                # 叠加上理论的二项分布曲线 (近似正态)
                from scipy.stats import binom
                x_theory = np.arange(0, num_levels + 1)
                y_theory = binom.pmf(x_theory, num_levels, 0.5) * sum(bins)  # 理论概率 * 样本总数

                fig_bar.add_trace(go.Scatter(
                    x=x_theory, y=y_theory, mode='lines',
                    line=dict(color='white', width=3, dash='dash'),
                    name="理论正态曲线"
                ))

                fig_bar.update_layout(
                    xaxis=dict(title="落入的槽位 (0-20)", showgrid=False),
                    yaxis=dict(title="小球数量", showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                    margin=dict(l=0, r=0, b=0, t=30), height=400,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )

                bar_spot.plotly_chart(fig_bar, use_container_width=True)
                time.sleep(0.05)

            st.success("所有小球落下，中心极限定理诚不欺我！")