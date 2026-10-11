from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import binom

from ultramarine.config import AppSettings
from ultramarine.math.optimization import gradient, gradient_descent, objective
from ultramarine.math.statistics import simulate_galton_board
from ultramarine.theme import PALETTE, animation_button_menu, transparent_plotly_layout
from ultramarine.ui import download_experiment, render_insight_panel, render_page_intro


@st.cache_data(show_spinner=False, max_entries=32)
def build_fourier_canvas_html(n_circles: int) -> str:
    return f"""
    <button id="toggle" type="button" style="margin-bottom:8px">播放 / 暂停</button>
    <canvas id="fourierCanvas" role="img" aria-label="傅里叶圆轮与锯齿波轨迹"
        style="width:100%; height:340px; background: #101C33; border-radius: 24px;"></canvas>
    <script>
        const canvas = document.getElementById("fourierCanvas");
        const ctx = canvas.getContext("2d");
        const dpr = window.devicePixelRatio || 1;
        function resizeCanvas() {{
            const rect = canvas.getBoundingClientRect();
            canvas.width = rect.width * dpr;
            canvas.height = rect.height * dpr;
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        }}
        resizeCanvas();
        let time = 0;
        const trail = [];
        const circleCount = {n_circles};

        let running = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        document.getElementById("toggle").addEventListener("click", () => {{
            running = !running;
        }});
        let previous = 0;
        function draw(timestamp = 0) {{
            const delta = Math.min(50, timestamp - previous);
            previous = timestamp;
            requestAnimationFrame(draw);
            if ((!running || document.hidden) && trail.length) return;
            const width = canvas.clientWidth;
            const height = canvas.clientHeight;
            ctx.clearRect(0, 0, width, height);
            let x = width * 0.24;
            let y = height * 0.5;

            for (let i = 0; i < circleCount; i++) {{
                const n = i + 1;
                const radius = Math.min(width, height) * 0.22 *
                    (2 / (n * Math.PI)) * (n % 2 === 0 ? -1 : 1);
                const prevX = x;
                const prevY = y;
                x += radius * Math.cos(n * time);
                y += radius * Math.sin(n * time);

                ctx.beginPath();
                ctx.arc(prevX, prevY, Math.abs(radius), 0, Math.PI * 2);
                ctx.strokeStyle = "rgba(191, 233, 255, 0.22)";
                ctx.lineWidth = 1;
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(prevX, prevY);
                ctx.lineTo(x, y);
                ctx.strokeStyle = "rgba(255, 255, 255, 0.82)";
                ctx.lineWidth = 1.4;
                ctx.stroke();
            }}

            trail.unshift(y);
            const waveStart = width * 0.48;
            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.lineTo(waveStart, trail[0]);
            ctx.strokeStyle = "rgba(251, 113, 133, 0.82)";
            ctx.setLineDash([5, 5]);
            ctx.stroke();
            ctx.setLineDash([]);

            ctx.beginPath();
            for (let i = 0; i < trail.length; i++) {{
                ctx.lineTo(i + waveStart, trail[i]);
            }}
            ctx.shadowColor = "rgba(251, 191, 36, 0.62)";
            ctx.shadowBlur = 14;
            ctx.strokeStyle = "#FBBF24";
            ctx.lineWidth = 2.4;
            ctx.stroke();
            ctx.shadowBlur = 0;

            if (trail.length > width * 0.48) trail.pop();
            time += 0.00168 * delta;
        }}

        window.addEventListener("resize", resizeCanvas);
        draw();
    </script>
    """


def build_gradient_descent_figure(
    mesh_x: np.ndarray,
    mesh_y: np.ndarray,
    mesh_z: np.ndarray,
    path_x: np.ndarray,
    path_y: np.ndarray,
    path_z: np.ndarray,
) -> go.Figure:
    frames = [
        go.Frame(
            data=[
                go.Scatter3d(x=path_x[: index + 1], y=path_y[: index + 1], z=path_z[: index + 1]),
                go.Scatter3d(x=[path_x[index]], y=[path_y[index]], z=[path_z[index]]),
            ],
            traces=[1, 2],
            name=str(index),
        )
        for index in range(len(path_x))
    ]

    figure = go.Figure(
        data=[
            go.Surface(
                x=mesh_x,
                y=mesh_y,
                z=mesh_z,
                colorscale="Viridis",
                opacity=0.82,
                showscale=False,
                lighting={"ambient": 0.42, "diffuse": 0.82, "specular": 0.65, "roughness": 0.32},
            ),
            go.Scatter3d(
                x=[path_x[0]],
                y=[path_y[0]],
                z=[path_z[0]],
                mode="lines",
                line={"color": PALETTE["coral"], "width": 7},
            ),
            go.Scatter3d(
                x=[path_x[0]],
                y=[path_y[0]],
                z=[path_z[0]],
                mode="markers",
                marker={
                    "size": 8,
                    "color": PALETTE["gold"],
                    "line": {"color": "#FFFFFF", "width": 1},
                },
            ),
        ],
        frames=frames,
    )
    figure.update_layout(
        **transparent_plotly_layout(height=520),
        updatemenus=animation_button_menu("播放下降过程", y=1.04, duration=90),
        scene={
            "xaxis": {"range": [-5, 5], "visible": False},
            "yaxis": {"range": [-5, 5], "visible": False},
            "zaxis": {"range": [-2, 8], "visible": False},
            "camera": {"eye": {"x": 1.65, "y": 1.35, "z": 0.72}},
        },
    )
    return figure


cached_descent = st.cache_data(show_spinner=False, max_entries=32)(gradient_descent)
cached_galton = st.cache_data(show_spinner=False, max_entries=32)(simulate_galton_board)


def build_galton_figure(counts: np.ndarray, levels: int, probability: float) -> go.Figure:
    slots = np.arange(levels + 1)
    pmf = binom.pmf(slots, levels, probability)
    frames = [
        go.Frame(
            data=[
                go.Bar(x=slots, y=bins, name="模拟频数", marker_color=PALETTE["jade"]),
                go.Scatter(
                    x=slots,
                    y=pmf * bins.sum(),
                    name="理论二项分布",
                    mode="lines+markers",
                    line={"color": PALETTE["coral"], "dash": "dash"},
                ),
            ],
            name=str(index),
        )
        for index, bins in enumerate(counts)
    ]
    figure = go.Figure(data=frames[-1].data, frames=frames)
    figure.update_layout(
        **transparent_plotly_layout(height=440),
        xaxis_title="向右次数 / 槽位",
        yaxis_title="小球数量",
        updatemenus=animation_button_menu("播放累积过程", duration=90),
        yaxis_range=[0, max(float(counts[-1].max()), float((pmf * counts[-1].sum()).max())) * 1.15],
    )
    return figure


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "数学与优化",
        "从周期分解到数值优化与概率模拟，调整参数并对照理论结果。",
        "Mathematics & Optimization",
    )
    tab_fourier, tab_descent, tab_galton = st.tabs(["傅里叶级数", "梯度下降", "伽尔顿板"])
    with tab_fourier:
        st.latex(r"f_N(x)=\sum_{n=1}^N \frac{2(-1)^{n+1}}{n\pi}\sin(nx)")
        n_circles = st.slider("展开项数", 3, 60, 12, key="fourier_terms")
        render_insight_panel(
            "傅里叶圆轮",
            principle="这组系数对应周期 2π 的锯齿波：在 (-π,π) 内 f(x)=x/π。",
            algorithm="旋转圆轮的纵坐标叠加为部分和，右侧记录端点轨迹。",
            meaning="连续点处部分和趋近锯齿波；跳跃处收敛到左右极限均值，附近保留 Gibbs 过冲。",
            parameters=(("项数", str(n_circles)),),
        )
        components.html(build_fourier_canvas_html(n_circles), height=395)
        st.caption("使用播放 / 暂停控制运动；系统偏好减少动态效果时默认暂停。")

    with tab_descent:
        st.latex(r"f(x,y)=(x^2+y^2)/10+\sin x+\cos y")
        c1, c2, c3, c4 = st.columns(4)
        rate = c1.slider("学习率", 0.01, 1.5, 0.15, 0.01, key="descent_learning_rate")
        start_x = c2.slider("起点 x", -4.0, 4.0, -3.2, 0.1, key="descent_start_x")
        start_y = c3.slider("起点 y", -4.0, 4.0, 3.0, 0.1, key="descent_start_y")
        steps = c4.slider("迭代步数", 20, 200, 80, 10, key="descent_steps")
        path, losses = cached_descent(rate, start_x, start_y, steps)
        mesh_x, mesh_y = np.meshgrid(np.linspace(-5, 5, 55), np.linspace(-5, 5, 55))
        render_insight_panel(
            "非凸优化",
            principle="梯度为 (x/5+cos x, y/5-sin y)，Hessian 的谱范数不超过 L=1.2。",
            algorithm="每步沿负梯度更新；0<η<2/L≈1.667 时可保证函数值下降。",
            meaning="梯度趋近零仅表示接近驻点；不同起点可能落入不同局部极小值。",
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("初始目标值", f"{losses[0]:.4f}")
        c2.metric("最终目标值", f"{losses[-1]:.4f}")
        c3.metric("最终梯度范数", f"{np.linalg.norm(gradient(path[-1])):.5f}")
        st.plotly_chart(
            build_gradient_descent_figure(
                mesh_x,
                mesh_y,
                objective(mesh_x, mesh_y),
                path[:, 0],
                path[:, 1],
                losses,
            ),
            width="stretch",
        )
        loss_chart = go.Figure(go.Scatter(y=losses, mode="lines", name="目标值"))
        loss_chart.update_layout(
            **transparent_plotly_layout(280), xaxis_title="迭代", yaxis_title="f(x,y)"
        )
        st.plotly_chart(loss_chart, width="stretch")
        download_experiment(
            "gradient_descent",
            {
                "iteration": np.arange(len(path)),
                "x": path[:, 0],
                "y": path[:, 1],
                "loss": losses,
            },
            {"learning_rate": rate, "start_x": start_x, "start_y": start_y, "steps": steps},
        )

    with tab_galton:
        c1, c2, c3, c4 = st.columns(4)
        balls = c1.slider("小球数量", 100, 5000, 1000, 100, key="galton_balls")
        levels = c2.slider("层数", 2, 40, 20, key="galton_levels")
        probability = c3.slider("向右概率 p", 0.0, 1.0, 0.5, 0.05, key="galton_probability")
        seed = int(c4.number_input("随机种子", 0, 2**32 - 1, 42, key="galton_seed"))
        counts = cached_galton(balls, seed, levels, probability)
        bins, slots = counts[-1], np.arange(levels + 1)
        empirical_mean = float(slots @ bins / balls)
        empirical_var = float((slots - empirical_mean) ** 2 @ bins / balls)
        st.latex(r"K\sim\mathrm{Binomial}(m,p),\quad E[K]=mp,\quad \mathrm{Var}(K)=mp(1-p)")
        st.caption(
            "每颗小球的各层选择相互独立。固定种子与参数即可重现；二项分布仅在适当条件下近似正态。"
        )
        st.plotly_chart(build_galton_figure(counts, levels, probability), width="stretch")
        st.table(
            {
                "统计量": ["均值", "方差（频数 / N）", "小球总数"],
                "模拟": [empirical_mean, empirical_var, float(bins.sum())],
                "理论": [
                    levels * probability,
                    levels * probability * (1 - probability),
                    float(balls),
                ],
            }
        )
        download_experiment(
            "galton_board",
            {
                "slot": slots,
                "count": bins,
                "expected_count": binom.pmf(slots, levels, probability) * balls,
            },
            {"seed": seed, "balls": balls, "levels": levels, "probability": probability},
        )
