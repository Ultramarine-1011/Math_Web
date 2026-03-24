from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.integrate import odeint

from ultramarine.layout import render_page_intro
from ultramarine.models import AppSettings
from ultramarine.theme import PALETTE, transparent_plotly_layout


@st.cache_data(show_spinner=False)
def solve_lorenz(sigma: float, rho: float, beta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    def lorenz_system(state: tuple[float, float, float], _: float) -> list[float]:
        x_value, y_value, z_value = state
        return [
            sigma * (y_value - x_value),
            x_value * (rho - z_value) - y_value,
            x_value * y_value - beta * z_value,
        ]

    time = np.linspace(0, 48, 4500)
    solution = odeint(lorenz_system, (1.0, 1.0, 1.0), time)
    return time, solution[:, 0], solution[:, 1], solution[:, 2]


def build_lorenz_figure(time: np.ndarray, x_value: np.ndarray, y_value: np.ndarray, z_value: np.ndarray) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Scatter3d(
                x=x_value,
                y=y_value,
                z=z_value,
                mode="lines",
                line={"color": time, "colorscale": "Plasma", "width": 4},
            )
        ]
    )
    figure.update_layout(
        **transparent_plotly_layout(height=620),
        scene={
            "xaxis": {"showbackground": False, "showticklabels": False, "title": ""},
            "yaxis": {"showbackground": False, "showticklabels": False, "title": ""},
            "zaxis": {"showbackground": False, "showticklabels": False, "title": ""},
        },
    )
    return figure


@st.cache_data(show_spinner=False)
def compute_heart_curve(samples: int = 900) -> tuple[np.ndarray, np.ndarray]:
    t_values = np.linspace(0, 2 * np.pi, samples)
    x_value = 16 * np.sin(t_values) ** 3
    y_value = (
        13 * np.cos(t_values)
        - 5 * np.cos(2 * t_values)
        - 2 * np.cos(3 * t_values)
        - np.cos(4 * t_values)
    )
    return x_value, y_value


def build_heart_figure(x_value: np.ndarray, y_value: np.ndarray) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=x_value,
            y=y_value,
            mode="lines",
            fill="toself",
            line={"color": PALETTE["coral"], "width": 4},
            fillcolor="rgba(232, 108, 78, 0.18)",
        )
    )
    figure.update_layout(
        **transparent_plotly_layout(height=520),
        xaxis={"visible": False},
        yaxis={"visible": False, "scaleanchor": "x", "scaleratio": 1},
        showlegend=False,
    )
    return figure


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "数学画廊",
        "这里放的是更适合静心观看的数学图形。你可以旋转、缩放，慢慢观察结构本身的美感。",
        kicker="图形浏览",
    )

    tab_lorenz, tab_heart = st.tabs(["洛伦兹吸引子", "心形曲线"])

    with tab_lorenz:
        st.latex(
            r"""
            \begin{cases}
            \frac{dx}{dt} = \sigma (y-x) \\
            \frac{dy}{dt} = x(\rho-z)-y \\
            \frac{dz}{dt} = xy-\beta z
            \end{cases}
            """
        )
        col1, col2, col3 = st.columns(3)
        sigma = col1.slider("sigma", 5.0, 15.0, 10.0)
        rho = col2.slider("rho", 10.0, 40.0, 28.0)
        beta = col3.slider("beta", 1.0, 5.0, 2.667)
        time, x_value, y_value, z_value = solve_lorenz(sigma, rho, beta)
        st.plotly_chart(
            build_lorenz_figure(time, x_value, y_value, z_value),
            width="stretch",
        )

    with tab_heart:
        st.latex(
            r"""
            \begin{cases}
            x = 16 \sin^3(t) \\
            y = 13 \cos(t) - 5 \cos(2t) - 2 \cos(3t) - \cos(4t)
            \end{cases}
            """
        )
        x_value, y_value = compute_heart_curve()
        st.plotly_chart(build_heart_figure(x_value, y_value), width="stretch")