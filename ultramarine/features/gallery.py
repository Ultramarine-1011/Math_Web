from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ultramarine.config import AppSettings
from ultramarine.math.dynamics import compute_heart_curve, solve_lorenz
from ultramarine.theme import PALETTE, transparent_plotly_layout
from ultramarine.ui import render_chart_shell, render_glass_card, render_page_intro

cached_lorenz = st.cache_data(show_spinner=False, max_entries=32)(solve_lorenz)


def build_lorenz_figure(
    time: np.ndarray, x_value: np.ndarray, y_value: np.ndarray, z_value: np.ndarray
) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Scatter3d(
                x=x_value,
                y=y_value,
                z=z_value,
                mode="lines",
                line={"color": time, "colorscale": "Turbo", "width": 5},
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
        sigma = col1.slider("sigma", 5.0, 15.0, 10.0, key="lorenz_sigma")
        rho = col2.slider("rho", 10.0, 40.0, 28.0, key="lorenz_rho")
        beta = col3.slider("beta", 1.0, 5.0, 8 / 3, key="lorenz_beta")
        time, x_value, y_value, z_value = cached_lorenz(sigma, rho, beta)
        render_chart_shell("Lorenz Attractor")
        st.plotly_chart(
            build_lorenz_figure(time, x_value, y_value, z_value),
            width="stretch",
        )

    with tab_heart:
        render_glass_card(
            "参数曲线",
            "这条经典心形曲线保留了数学画廊中偏静态观赏的一面。",
            kicker="Parametric Curve",
            tags=("代数曲线", "参数化"),
        )
        st.latex(
            r"""
            \begin{cases}
            x = 16 \sin^3(t) \\
            y = 13 \cos(t) - 5 \cos(2t) - 2 \cos(3t) - \cos(4t)
            \end{cases}
            """
        )
        x_value, y_value = compute_heart_curve()
        render_chart_shell("Heart Curve")
        st.plotly_chart(build_heart_figure(x_value, y_value), width="stretch")
