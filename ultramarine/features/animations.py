from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ultramarine.config import AppSettings
from ultramarine.math.geometry import associated_surface, linear_transform
from ultramarine.theme import PALETTE, animation_button_menu, transparent_plotly_layout
from ultramarine.ui import render_chart_shell, render_insight_panel, render_page_intro


@st.cache_data(show_spinner=False, max_entries=16)
def compute_linear_transform_frames(
    matrix_values: tuple[float, float, float, float],
) -> tuple[np.ndarray, list[go.Frame]]:
    frames = []
    for index, progress in enumerate(np.linspace(0, 1, 36)):
        _, grid, i_hat, j_hat = linear_transform(matrix_values, progress)
        frames.append(
            go.Frame(
                data=[
                    go.Scatter(x=grid[0], y=grid[1]),
                    go.Scatter(x=[0, i_hat[0]], y=[0, i_hat[1]]),
                    go.Scatter(x=[0, j_hat[0]], y=[0, j_hat[1]]),
                ],
                traces=[0, 1, 2],
                name=str(index),
            )
        )
    return np.array(matrix_values).reshape(2, 2), frames


def build_linear_transform_figure(
    frames: list[go.Frame],
) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Scatter(
                x=frames[0].data[0].x,
                y=frames[0].data[0].y,
                mode="lines",
                line={"color": "rgba(125, 211, 252, 0.34)", "width": 2},
            ),
            go.Scatter(
                x=[0, 1],
                y=[0, 0],
                mode="lines",
                line={"color": PALETTE["coral"], "width": 7},
                name="i-hat",
            ),
            go.Scatter(
                x=[0, 0],
                y=[0, 1],
                mode="lines",
                line={"color": PALETTE["jade"], "width": 7},
                name="j-hat",
            ),
        ],
        frames=frames,
    )
    figure.update_layout(
        **transparent_plotly_layout(height=520),
        xaxis={
            "range": [-8, 8],
            "showgrid": False,
            "zeroline": True,
            "zerolinecolor": "rgba(255,255,255,0.22)",
        },
        yaxis={
            "range": [-8, 8],
            "showgrid": False,
            "zeroline": True,
            "zerolinecolor": "rgba(255,255,255,0.22)",
            "scaleanchor": "x",
            "scaleratio": 1,
        },
        updatemenus=animation_button_menu("播放变换", y=1.05, duration=45),
        showlegend=False,
    )
    return figure


@st.cache_data(show_spinner=False, max_entries=16)
def compute_surface_frames() -> tuple[tuple[np.ndarray, np.ndarray, np.ndarray], list[go.Frame]]:
    frames = []
    for index, raw_progress in enumerate(np.linspace(0, 1, 60)):
        progress = raw_progress**2 * (3 - 2 * raw_progress)
        x, y, z = associated_surface(progress * np.pi / 2)
        frames.append(go.Frame(data=[go.Surface(x=x, y=y, z=z)], traces=[0], name=str(index)))
    return associated_surface(0), frames


def build_surface_figure(
    initial_surface: tuple[np.ndarray, np.ndarray, np.ndarray], frames: list[go.Frame]
) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Surface(
                x=initial_surface[0],
                y=initial_surface[1],
                z=initial_surface[2],
                colorscale="Magma",
                lighting={"ambient": 0.38, "diffuse": 0.88, "specular": 0.7, "roughness": 0.26},
                showscale=False,
            )
        ],
        frames=frames,
    )
    figure.update_layout(
        **transparent_plotly_layout(height=640),
        updatemenus=animation_button_menu("播放形变", y=1.04, duration=38),
        scene={
            "xaxis": {"range": [-4, 4], "visible": False},
            "yaxis": {"range": [-4, 4], "visible": False},
            "zaxis": {"range": [-4, 4], "visible": False},
            "camera": {"eye": {"x": 1.42, "y": 1.18, "z": 0.72}},
        },
    )
    return figure


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "数学动画",
        "这一页更强调过程本身。与其只看结果，不如把变化完整看一遍。",
        kicker="变化过程",
    )

    tab_linear, tab_surface = st.tabs(["线性代数", "曲面形变"])

    with tab_linear:
        st.markdown("### 连续线性变换")
        c1, c2 = st.columns(2)
        a11 = c1.number_input("a11", -2.0, 2.0, 1.5, 0.1, key="linear_a11")
        a21 = c1.number_input("a21", -2.0, 2.0, 0.5, 0.1, key="linear_a21")
        a12 = c2.number_input("a12", -2.0, 2.0, 1.0, 0.1, key="linear_a12")
        a22 = c2.number_input("a22", -2.0, 2.0, 1.2, 0.1, key="linear_a22")

        matrix, frames = compute_linear_transform_frames((a11, a12, a21, a22))
        determinant = float(np.linalg.det(matrix))
        info_col, chart_col = st.columns([1.1, 1.9])
        with info_col:
            st.latex(f"\\det(A) = {determinant:.2f}")
            if determinant < 0:
                st.warning("这个矩阵会翻转空间方向。")
            elif abs(determinant) < 0.05:
                st.info("行列式接近零，空间被压缩得非常明显。")
            else:
                st.success(f"面积被缩放为原来的 {abs(determinant):.2f} 倍。")
            render_insight_panel(
                "Linear Transformation",
                principle="矩阵把基向量移动到新位置，整个平面的网格由基向量线性组合决定。",
                algorithm="在单位矩阵和目标矩阵之间插值，逐帧重算网格点和两个基向量。",
                meaning="线性代数的抽象不是符号游戏，而是空间规则的可视化。",
                parameters=(
                    ("det(A)", f"{determinant:.2f}"),
                    ("面积缩放", f"{abs(determinant):.2f} 倍"),
                ),
            )
        with chart_col:
            render_chart_shell("Animated Linear Transformation")
            st.plotly_chart(
                build_linear_transform_figure(frames),
                width="stretch",
            )

    with tab_surface:
        st.markdown("### 从悬链曲面到螺旋曲面")
        initial_surface, frames = compute_surface_frames()
        render_insight_panel(
            "Catenoid to Helicoid",
            principle="悬链曲面与螺旋曲面是一对共轭极小曲面，可以通过连续参数族相互形变。",
            algorithm="使用 smoothstep 参数曲线插值，生成 60 帧曲面，减少起止瞬间的速度突变。",
            meaning="局部参数曲面的第一基本形式保持不变；这不等同于全局拓扑等价。",
            parameters=(("帧数", str(len(frames))), ("采样", "56 x 56")),
        )
        render_chart_shell("Catenoid to Helicoid")
        st.plotly_chart(
            build_surface_figure(initial_surface, frames),
            width="stretch",
        )
