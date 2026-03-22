from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import binom

from ultramarine.layout import render_page_intro
from ultramarine.models import AppSettings
from ultramarine.theme import PALETTE, transparent_plotly_layout


@st.cache_data(show_spinner=False)
def build_fourier_canvas_html(n_circles: int) -> str:
    return f"""
    <canvas id="fourierCanvas" width="900" height="320"
        style="width:100%; background: linear-gradient(180deg, #162133 0%, #1D2E4D 100%); border-radius: 24px;"></canvas>
    <script>
        const canvas = document.getElementById("fourierCanvas");
        const ctx = canvas.getContext("2d");
        let time = 0;
        const trail = [];
        const circleCount = {n_circles};

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let x = 220;
            let y = 160;

            for (let i = 0; i < circleCount; i++) {{
                const n = i + 1;
                const radius = 74 * (2 / (n * Math.PI)) * (n % 2 === 0 ? -1 : 1);
                const prevX = x;
                const prevY = y;
                x += radius * Math.cos(n * time);
                y += radius * Math.sin(n * time);

                ctx.beginPath();
                ctx.arc(prevX, prevY, Math.abs(radius), 0, Math.PI * 2);
                ctx.strokeStyle = "rgba(214, 225, 255, 0.22)";
                ctx.lineWidth = 1;
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(prevX, prevY);
                ctx.lineTo(x, y);
                ctx.strokeStyle = "rgba(255, 255, 255, 0.78)";
                ctx.lineWidth = 1.4;
                ctx.stroke();
            }}

            trail.unshift(y);
            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.lineTo(430, trail[0]);
            ctx.strokeStyle = "rgba(232, 108, 78, 0.75)";
            ctx.setLineDash([5, 5]);
            ctx.stroke();
            ctx.setLineDash([]);

            ctx.beginPath();
            for (let i = 0; i < trail.length; i++) {{
                ctx.lineTo(i + 430, trail[i]);
            }}
            ctx.strokeStyle = "#D2A44C";
            ctx.lineWidth = 2.4;
            ctx.stroke();

            if (trail.length > 420) trail.pop();
            time += 0.028;
            requestAnimationFrame(draw);
        }}

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
            go.Surface(x=mesh_x, y=mesh_y, z=mesh_z, colorscale="Tealgrn", opacity=0.7, showscale=False),
            go.Scatter3d(
                x=[path_x[0]],
                y=[path_y[0]],
                z=[path_z[0]],
                mode="lines",
                line={"color": PALETTE["coral"], "width": 5},
            ),
            go.Scatter3d(
                x=[path_x[0]],
                y=[path_y[0]],
                z=[path_z[0]],
                mode="markers",
                marker={"size": 8, "color": PALETTE["gold"]},
            ),
        ],
        frames=frames,
    )
    figure.update_layout(
        **transparent_plotly_layout(height=520),
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play descent",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}],
                    }
                ],
                "x": 0.5,
                "xanchor": "center",
                "y": 1.03,
                "yanchor": "bottom",
            }
        ],
        scene={
            "xaxis": {"range": [-5, 5], "visible": False},
            "yaxis": {"range": [-5, 5], "visible": False},
            "zaxis": {"range": [-2, 8], "visible": False},
            "camera": {"eye": {"x": 1.55, "y": 1.45, "z": 0.52}},
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
        xaxis={"title": "Slot", "showgrid": False},
        yaxis={"title": "Ball count", "gridcolor": "rgba(22, 33, 51, 0.08)"},
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play simulation",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 110, "redraw": True}, "fromcurrent": False}],
                    }
                ],
                "x": 0.5,
                "xanchor": "center",
                "y": 1.06,
                "yanchor": "bottom",
            }
        ],
        showlegend=False,
    )
    return figure


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "Interactive Lab",
        "This page keeps the original mathematical demos but refactors them into independent"
        " compute-and-render units. That makes the page much easier to test and extend.",
        kicker="Interactive Mathematics",
    )

    tab_fourier, tab_descent, tab_galton = st.tabs(
        ["Fourier Canvas", "Gradient Descent", "Galton Board"]
    )

    with tab_fourier:
        st.latex(r"f(x)=\sum_{n=1}^N \frac{2(-1)^{n+1}}{n\pi}\sin(nx)")
        n_circles = st.slider("Series terms", 3, 60, 12)
        components.html(build_fourier_canvas_html(n_circles), height=340)
        st.caption("The Fourier demo still uses native Canvas, but the HTML generator is now isolated.")

    with tab_descent:
        col_lr, col_start = st.columns(2)
        learning_rate = col_lr.slider("Learning rate", 0.01, 0.3, 0.08)
        start_key = col_start.selectbox(
            "Starting point",
            ("ridge", "plateau", "cliff"),
            format_func=lambda value: {
                "ridge": "Ridge (-4, -4)",
                "plateau": "Plateau (3, 4)",
                "cliff": "Cliff (0, -4)",
            }[value],
        )
        starts = {"ridge": (-4.0, -4.0), "plateau": (3.0, 4.0), "cliff": (0.0, -4.0)}
        mesh_x, mesh_y, mesh_z, path_x, path_y, path_z = compute_gradient_descent(
            learning_rate,
            starts[start_key][0],
            starts[start_key][1],
        )
        st.plotly_chart(
            build_gradient_descent_figure(mesh_x, mesh_y, mesh_z, path_x, path_y, path_z),
            width="stretch",
        )

    with tab_galton:
        if "galton_seed" not in st.session_state:
            st.session_state["galton_seed"] = 42
        controls = st.columns([1.4, 0.8])
        num_balls = controls[0].slider("Number of balls", 100, 5000, 1000, step=100)
        if controls[1].button("Resample"):
            st.session_state["galton_seed"] += 1
        st.plotly_chart(
            build_galton_figure(num_balls, int(st.session_state["galton_seed"])),
            width="stretch",
        )
        st.caption("The dashed line shows the theoretical binomial curve for the same parameters.")