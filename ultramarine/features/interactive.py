from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import binom

from ultramarine.layout import render_page_intro
from ultramarine.models import AppSettings
from ultramarine.theme import PALETTE, animation_button_menu, transparent_plotly_layout
from ultramarine.ui import render_chart_shell, render_insight_panel


@st.cache_data(show_spinner=False)
def build_fourier_canvas_html(n_circles: int) -> str:
    return f"""
    <canvas id="fourierCanvas"
        style="width:100%; height:340px; background: radial-gradient(circle at 20% 20%, rgba(56,189,248,0.22), transparent 38%), linear-gradient(180deg, #050812 0%, #101C33 100%); border-radius: 24px;"></canvas>
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

        function draw() {{
            const width = canvas.clientWidth;
            const height = canvas.clientHeight;
            ctx.clearRect(0, 0, width, height);
            let x = width * 0.24;
            let y = height * 0.5;

            for (let i = 0; i < circleCount; i++) {{
                const n = i + 1;
                const radius = Math.min(width, height) * 0.22 * (2 / (n * Math.PI)) * (n % 2 === 0 ? -1 : 1);
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
            time += 0.028;
            requestAnimationFrame(draw);
        }}

        window.addEventListener("resize", resizeCanvas);
        draw();
    </script>
    """


@st.cache_data(show_spinner=False)
def compute_gradient_descent(
    learning_rate: float,
    start_x: float,
    start_y: float,
    steps: int = 32,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    def f(x: np.ndarray | float, y: np.ndarray | float) -> np.ndarray | float:
        return (x**2 + y**2) / 10 + np.sin(x) + np.cos(y)

    def grad(x: float, y: float) -> tuple[float, float]:
        return (x / 5 + math.cos(x), y / 5 - math.sin(y))

    grid = np.linspace(-5, 5, 55)
    mesh_x, mesh_y = np.meshgrid(grid, grid)
    mesh_z = f(mesh_x, mesh_y)

    xs = [start_x]
    ys = [start_y]
    zs = [float(f(start_x, start_y))]
    current_x = start_x
    current_y = start_y

    for _ in range(steps):
        dx, dy = grad(current_x, current_y)
        current_x = current_x - learning_rate * dx
        current_y = current_y - learning_rate * dy
        xs.append(current_x)
        ys.append(current_y)
        zs.append(float(f(current_x, current_y)))

    return mesh_x, mesh_y, mesh_z, np.array(xs), np.array(ys), np.array(zs)


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
                marker={"size": 8, "color": PALETTE["gold"], "line": {"color": "#FFFFFF", "width": 1}},
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


@st.cache_data(show_spinner=False)
def simulate_galton_board(
    num_balls: int,
    seed: int,
    levels: int = 20,
    batch_size: int = 50,
) -> tuple[np.ndarray, list[go.Frame]]:
    rng = np.random.default_rng(seed)
    bins = np.zeros(levels + 1)
    frames: list[go.Frame] = []

    for step in range(max(1, num_balls // batch_size)):
        drops = rng.integers(0, 2, size=(batch_size, levels))
        final_positions = np.sum(drops, axis=1)
        for position in final_positions:
            bins[position] += 1

        theory_x = np.arange(0, levels + 1)
        theory_y = binom.pmf(theory_x, levels, 0.5) * float(np.sum(bins))
        frames.append(
            go.Frame(
                data=[
                    go.Bar(x=theory_x, y=bins.copy(), marker_color=PALETTE["jade"], opacity=0.88),
                    go.Scatter(
                        x=theory_x,
                        y=theory_y,
                        mode="lines",
                        line={"color": PALETTE["coral"], "width": 3, "dash": "dash"},
                    ),
                ],
                name=str(step),
            )
        )

    return bins, frames


def build_galton_figure(num_balls: int, seed: int) -> go.Figure:
    bins, frames = simulate_galton_board(num_balls, seed)
    if not frames:
        frames = [go.Frame(data=[go.Bar(x=list(range(21)), y=bins)])]

    figure = go.Figure(data=frames[0].data, frames=frames)
    figure.update_layout(
        **transparent_plotly_layout(height=420),
        xaxis={"title": "落入槽位", "showgrid": False},
        yaxis={"title": "小球数量", "gridcolor": "rgba(22, 33, 51, 0.08)"},
        updatemenus=animation_button_menu("播放模拟过程", y=1.07, duration=95),
        showlegend=False,
    )
    return figure


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "互动实验室",
        "这里收纳了几组可直接操作的数学实验。你可以一边调整参数，一边观察图形和过程如何变化。",
        kicker="互动数学",
    )

    tab_fourier, tab_descent, tab_galton = st.tabs(
        ["傅里叶级数", "梯度下降", "伽尔顿板"]
    )

    with tab_fourier:
        st.latex(r"f(x)=\sum_{n=1}^N \frac{2(-1)^{n+1}}{n\pi}\sin(nx)")
        n_circles = st.slider("展开项数", 3, 60, 12, key="fourier_terms")
        render_insight_panel(
            "Fourier Epicycles",
            principle="把周期函数投影到一组正交三角基上，项数越多，高频细节越丰富，截断误差越小。",
            algorithm="Canvas 每帧叠加 N 个旋转圆轮，圆心沿前一个圆的端点移动，最后端点写入右侧轨迹。",
            meaning="复杂波形不是一次性出现，而是由许多简单圆周运动协作生成；结构来自分解。",
            parameters=(("展开项数", f"{n_circles} 项"),),
        )
        render_chart_shell("Fourier Epicycles")
        components.html(build_fourier_canvas_html(n_circles), height=360)
        st.caption("通过圆轮叠加，逐步逼近目标波形。")

    with tab_descent:
        col_lr, col_x, col_y = st.columns(3)
        learning_rate = col_lr.slider("学习率", 0.01, 0.3, 0.08, key="descent_learning_rate")
        start_x = col_x.slider("起点 x", -4.0, 4.0, -3.2, 0.1, key="descent_start_x")
        start_y = col_y.slider("起点 y", -4.0, 4.0, 3.0, 0.1, key="descent_start_y")
        radius = math.hypot(start_x, start_y)
        region_hint = "平坦区" if radius < 1.4 else "外缘高坡区" if radius > 4.2 else "弯曲过渡区"
        render_insight_panel(
            "Gradient Descent Trajectory",
            principle="沿负梯度方向更新参数，局部下降最快，但全局结果会受非凸地形和起点影响。",
            algorithm="每步计算 ∇f=(x/5+cos x, y/5-sin y)，再执行 (x,y) ← (x,y)-η∇f。",
            meaning="优化不是寻找绝对真理的直线，而是在局部信息里持续修正方向。",
            parameters=(
                ("学习率 η", f"{learning_rate:.2f}"),
                ("自由起点", f"({start_x:.1f}, {start_y:.1f})"),
                ("当前位置语义", region_hint),
            ),
        )
        mesh_x, mesh_y, mesh_z, path_x, path_y, path_z = compute_gradient_descent(
            learning_rate,
            start_x,
            start_y,
        )
        render_chart_shell("Gradient Descent Trajectory")
        st.plotly_chart(
            build_gradient_descent_figure(mesh_x, mesh_y, mesh_z, path_x, path_y, path_z),
            width="stretch",
        )

    with tab_galton:
        if "galton_seed" not in st.session_state:
            st.session_state["galton_seed"] = 42
        controls = st.columns([1.4, 0.8])
        num_balls = controls[0].slider("小球数量", 100, 5000, 1000, step=100, key="galton_balls")
        if controls[1].button("重新采样"):
            st.session_state["galton_seed"] += 1
        render_insight_panel(
            "Galton Board Distribution",
            principle="每颗小球经历独立的左右选择，最终槽位服从二项分布，数量变大后逼近正态钟形。",
            algorithm="用随机数批量模拟每层左右分支，累积槽位频数，并同步画出理论二项分布曲线。",
            meaning="个体轨迹不可预测，但大量重复会显出稳定秩序。",
            parameters=(("小球数量", f"{num_balls}"), ("随机种子", str(st.session_state["galton_seed"]))),
        )
        render_chart_shell("Galton Board Distribution")
        st.plotly_chart(
            build_galton_figure(num_balls, int(st.session_state["galton_seed"])),
            width="stretch",
        )
        st.caption("虚线表示相同参数下的理论二项分布曲线。")