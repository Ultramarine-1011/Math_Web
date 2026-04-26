from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ultramarine.layout import render_page_intro
from ultramarine.math.fractals import julia_escape, mandelbrot_escape
from ultramarine.models import AppSettings
from ultramarine.theme import transparent_plotly_layout
from ultramarine.ui import render_chart_shell, render_glass_card, render_insight_panel


COOL_FRACTAL_SCALE = [
    [0.0, "#020617"],
    [0.18, "#0F172A"],
    [0.36, "#1D4ED8"],
    [0.58, "#06B6D4"],
    [0.78, "#A78BFA"],
    [1.0, "#F8FAFC"],
]


@st.cache_data(show_spinner=False)
def cached_mandelbrot(
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    width: int,
    height: int,
    max_iter: int,
) -> np.ndarray:
    return mandelbrot_escape(
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        width=width,
        height=height,
        max_iter=max_iter,
    )


@st.cache_data(show_spinner=False)
def cached_julia(
    c_real: float,
    c_imag: float,
    extent: float,
    width: int,
    height: int,
    max_iter: int,
) -> np.ndarray:
    return julia_escape(
        c_real=c_real,
        c_imag=c_imag,
        extent=extent,
        width=width,
        height=height,
        max_iter=max_iter,
    )


def build_escape_figure(
    data: np.ndarray,
    *,
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    height: int = 560,
    colorscale: list[list[object]] | str = COOL_FRACTAL_SCALE,
) -> go.Figure:
    x_axis = np.linspace(x_range[0], x_range[1], data.shape[1])
    y_axis = np.linspace(y_range[0], y_range[1], data.shape[0])
    figure = go.Figure(
        data=[
            go.Heatmap(
                z=data,
                x=x_axis,
                y=y_axis,
                colorscale=colorscale,
                showscale=False,
                hovertemplate="Re=%{x:.4f}<br>Im=%{y:.4f}<br>escape=%{z}<extra></extra>",
            )
        ]
    )
    layout = transparent_plotly_layout(height=height)
    layout["margin"] = {"l": 8, "r": 8, "t": 22, "b": 34}
    figure.update_layout(
        **layout,
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "title": ""},
        yaxis={
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "title": "",
            "scaleanchor": "x",
            "scaleratio": 1,
        },
    )
    return figure


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "分形天文台",
        "从 z_{n+1}=z_n^2+c 出发，观察一个二次迭代如何生成无限细节。",
        kicker="Fractal Observatory",
    )

    st.session_state.setdefault("fractal_zoom", "classic")
    controls, summary = st.columns([1.05, 1.4])
    with controls:
        zoom = st.selectbox(
            "视窗",
            ("classic", "seahorse", "elephant"),
            key="fractal_zoom",
            format_func=lambda value: {
                "classic": "全貌",
                "seahorse": "海马谷",
                "elephant": "象谷",
            }[value],
        )
        max_iter = st.slider("迭代次数", 40, 180, 96, 8, key="fractal_iter")
        resolution = st.slider("分辨率", 240, 520, 360, 40, key="fractal_resolution")
        c_real = st.slider("Julia 参数 Re(c)", -1.0, 1.0, -0.74, 0.01)
        c_imag = st.slider("Julia 参数 Im(c)", -1.0, 1.0, 0.18, 0.01)

    with summary:
        render_glass_card(
            "为什么震撼",
            "Mandelbrot 集把所有不会逃逸的参数 c 放在一起；每个点又对应一个 Julia 世界。",
            kicker="z -> z^2 + c",
            tags=("混沌", "自相似", "动力系统"),
        )
        render_insight_panel(
            "Fractal Escape Time",
            principle="Mandelbrot 集收集使 z_{n+1}=z_n^2+c 不逃逸的参数，Julia 集则固定 c 后观察初值命运。",
            algorithm="对每个像素迭代复数二次映射，记录首次越过半径 2 的迭代次数，并映射为冷色阶。",
            meaning="无限复杂并不一定需要复杂规则；边界处的细节来自稳定与逃逸之间的拉扯。",
            parameters=(
                ("视窗", zoom),
                ("迭代次数", str(max_iter)),
                ("Julia c", f"{c_real:.2f}{c_imag:+.2f}i"),
            ),
        )

    windows = {
        "classic": (-2.2, 0.9, -1.35, 1.35),
        "seahorse": (-0.92, -0.62, -0.38, -0.08),
        "elephant": (0.22, 0.42, -0.12, 0.08),
    }
    x_min, x_max, y_min, y_max = windows[zoom]
    mandelbrot = cached_mandelbrot(
        x_min,
        x_max,
        y_min,
        y_max,
        resolution,
        int(resolution * 0.78),
        max_iter,
    )
    julia = cached_julia(c_real, c_imag, 1.72, resolution, resolution, max_iter)

    left, right = st.columns([1.18, 1])
    with left:
        render_chart_shell("Mandelbrot Escape Field", "冷色逃逸时间图，坐标刻度已弱化以避免遮挡。")
        st.plotly_chart(
            build_escape_figure(
                mandelbrot,
                x_range=(x_min, x_max),
                y_range=(y_min, y_max),
            ),
            width="stretch",
            config={"displaylogo": False},
        )
    with right:
        render_chart_shell("Linked Julia Set", f"当前参数 c={c_real:.2f}{c_imag:+.2f}i")
        st.plotly_chart(
            build_escape_figure(
                julia,
                x_range=(-1.72, 1.72),
                y_range=(-1.72, 1.72),
                height=560,
            ),
            width="stretch",
            config={"displaylogo": False},
        )
