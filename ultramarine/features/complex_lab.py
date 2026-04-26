from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ultramarine.layout import render_page_intro
from ultramarine.math.complex_maps import build_complex_morph_lines
from ultramarine.models import AppSettings
from ultramarine.theme import PALETTE, animation_button_menu, transparent_plotly_layout
from ultramarine.ui import render_chart_shell, render_insight_panel


MAP_OPTIONS = {
    "power": "f(z)=s z^n + b",
    "inverse_affine": "f(z)=s/(z-p)+b",
    "exponential": "f(z)=exp(s z)+b",
    "mobius": "f(z)=s(z-a)/(z-p)+b",
}


@st.cache_data(show_spinner=False)
def cached_morph_lines(
    map_name: str,
    extent: float,
    lines: int,
    samples_per_line: int,
    frame_count: int,
    power: float,
    scale_real: float,
    scale_imag: float,
    shift_real: float,
    shift_imag: float,
    numerator_real: float,
    numerator_imag: float,
    pole_real: float,
    pole_imag: float,
) -> tuple[list[np.ndarray], list[list[np.ndarray]]]:
    return build_complex_morph_lines(
        map_name,
        extent=extent,
        lines=lines,
        samples_per_line=samples_per_line,
        frame_count=frame_count,
        power=power,
        scale=complex(scale_real, scale_imag),
        shift=complex(shift_real, shift_imag),
        numerator_shift=complex(numerator_real, numerator_imag),
        denominator_shift=complex(pole_real, pole_imag),
    )


def build_complex_animation_figure(
    source_lines: list[np.ndarray],
    frame_lines: list[list[np.ndarray]],
    extent: float,
) -> go.Figure:
    traces = []
    for index, line in enumerate(source_lines):
        is_axis = index in {len(source_lines) // 2 - 1, len(source_lines) // 2}
        traces.append(
            go.Scatter(
                x=line.real,
                y=line.imag,
                mode="lines",
                line={
                    "color": "rgba(251, 191, 36, 0.82)" if is_axis else "rgba(191, 233, 255, 0.38)",
                    "width": 2.2 if is_axis else 1.15,
                },
                hoverinfo="skip",
                showlegend=False,
            )
        )
    unit_circle = np.exp(1j * np.linspace(0, 2 * np.pi, 220))
    traces.append(
        go.Scatter(
            x=unit_circle.real,
            y=unit_circle.imag,
            mode="lines",
            line={"color": "rgba(52, 211, 153, 0.72)", "width": 2},
            hoverinfo="skip",
            showlegend=False,
        )
    )

    frames = [
        go.Frame(
            data=[
                go.Scatter(
                    x=line.real,
                    y=line.imag,
                    mode="lines",
                    line=traces[index].line,
                    hoverinfo="skip",
                    showlegend=False,
                )
                for index, line in enumerate(lines)
            ],
            traces=list(range(len(source_lines))),
            name=str(frame_index),
        )
        for frame_index, lines in enumerate(frame_lines)
    ]

    figure = go.Figure(data=traces, frames=frames)
    figure.update_layout(
        **transparent_plotly_layout(height=640),
        updatemenus=animation_button_menu("播放映射", y=1.05, duration=45),
        xaxis={
            "range": [-extent * 1.85, extent * 1.85],
            "showgrid": False,
            "zeroline": True,
            "zerolinecolor": "rgba(255,255,255,0.18)",
        },
        yaxis={
            "range": [-extent * 1.85, extent * 1.85],
            "showgrid": False,
            "zeroline": True,
            "zerolinecolor": "rgba(255,255,255,0.18)",
            "scaleanchor": "x",
            "scaleratio": 1,
        },
    )
    return figure


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "复变映射实验室",
        "把复函数看作平面到平面的变形：相位、模长、极点和共形结构会同时显形。",
        kicker="Complex Analysis",
    )

    st.session_state.setdefault("complex_map_name", "power")
    controls, visual = st.columns([0.82, 1.72])
    with controls:
        map_name = st.selectbox(
            "选择映射",
            list(MAP_OPTIONS.keys()),
            key="complex_map_name",
            format_func=lambda value: MAP_OPTIONS[value],
        )
        extent = st.slider("原始网格范围", 1.0, 6.0, 2.4, 0.2, key="complex_extent")
        lines = st.slider("网格线数量", 7, 29, 15, 2, key="complex_lines")
        frame_count = st.slider("动画帧数", 24, 96, 54, 6, key="complex_frames")
        power = st.slider("幂指数 n", 0.5, 5.0, 2.0, 0.1, key="complex_power")
        scale_real = st.slider("缩放 Re(s)", -3.0, 3.0, 1.0, 0.1, key="complex_scale_real")
        scale_imag = st.slider("缩放 Im(s)", -3.0, 3.0, 0.0, 0.1, key="complex_scale_imag")
        shift_real = st.slider("平移 Re(b)", -4.0, 4.0, 0.0, 0.1, key="complex_shift_real")
        shift_imag = st.slider("平移 Im(b)", -4.0, 4.0, 0.0, 0.1, key="complex_shift_imag")
        numerator_real = st.slider("零点/分子 Re(a)", -4.0, 4.0, 0.4, 0.1, key="complex_num_real")
        numerator_imag = st.slider("零点/分子 Im(a)", -4.0, 4.0, 0.2, 0.1, key="complex_num_imag")
        pole_real = st.slider("极点 Re(p)", -4.0, 4.0, -0.5, 0.1, key="complex_pole_real")
        pole_imag = st.slider("极点 Im(p)", -4.0, 4.0, 0.0, 0.1, key="complex_pole_imag")
        render_insight_panel(
            "Complex Mapping Animation",
            principle="全纯函数在非奇点附近近似为旋转加缩放，因此小网格会保持近似正交。",
            algorithm="先生成复平面网格，再计算 f(z)，用 smoothstep 在 z 与 f(z) 之间插值生成动画帧。",
            meaning="复变函数不是把点搬家，而是在每个局部给平面制定一套旋转、伸缩和折叠规则。",
            parameters=(
                ("映射", MAP_OPTIONS[map_name]),
                ("范围", f"[-{extent:.1f}, {extent:.1f}]"),
                ("缩放 s", f"{scale_real:.1f}{scale_imag:+.1f}i"),
                ("平移 b", f"{shift_real:.1f}{shift_imag:+.1f}i"),
            ),
        )

    with visual:
        source_lines, frame_lines = cached_morph_lines(
            map_name,
            extent,
            lines,
            160,
            frame_count,
            power,
            scale_real,
            scale_imag,
            shift_real,
            shift_imag,
            numerator_real,
            numerator_imag,
            pole_real,
            pole_imag,
        )
        render_chart_shell("3B1B-style Complex Morph")
        st.plotly_chart(
            build_complex_animation_figure(source_lines, frame_lines, extent),
            width="stretch",
            config={"displaylogo": False},
        )

    if map_name == "exponential":
        st.info("指数映射把竖直方向的平移折叠成周期相位，缩放参数会改变周期和径向增长速度。")
    elif map_name == "inverse_affine":
        st.info("反演型映射会把极点附近快速拉向远方，极点位置 p 决定图形最剧烈的撕裂点。")
    elif map_name == "mobius":
        st.info("Mobius 型映射把广义圆映成广义圆，是复分析里最重要的全局变换之一。")
    else:
        st.info("幂映射会把角度乘以 n。n 越大，原点附近的相位绕行越密集。")
