from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ultramarine.layout import render_page_intro
from ultramarine.models import AppSettings
from ultramarine.theme import PALETTE, transparent_plotly_layout


@st.cache_data(show_spinner=False)
def compute_linear_transform_frames(matrix_values: tuple[float, float, float, float]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[go.Frame]]:
    a11, a12, a21, a22 = matrix_values
    matrix = np.array([[a11, a12], [a21, a22]])
    identity = np.eye(2)

    x_lines: list[float] = []
    y_lines: list[float] = []
    for index in range(-5, 6):
        x_lines.extend([index, index, np.nan])
        y_lines.extend([-5, 5, np.nan])
        x_lines.extend([-5, 5, np.nan])
        y_lines.extend([index, index, np.nan])

    grid = np.vstack([x_lines, y_lines])
    clean_grid = np.nan_to_num(grid)
    frames: list[go.Frame] = []
    for progress in np.linspace(0, 1, 36):
        current_matrix = (1 - progress) * identity + progress * matrix
        transformed = current_matrix @ clean_grid
        transformed[np.isnan(grid)] = np.nan
        i_hat = current_matrix @ np.array([1, 0])
        j_hat = current_matrix @ np.array([0, 1])
        frames.append(
            go.Frame(
                data=[
                    go.Scatter(x=transformed[0], y=transformed[1]),
                    go.Scatter(x=[0, i_hat[0]], y=[0, i_hat[1]]),
                    go.Scatter(x=[0, j_hat[0]], y=[0, j_hat[1]]),
                ],
                traces=[0, 1, 2],
                name=f"{progress:.2f}",
            )
        )

    transformed = matrix @ clean_grid
    transformed[np.isnan(grid)] = np.nan
    return matrix, transformed, matrix @ np.array([1, 0]), matrix @ np.array([0, 1]), frames


def build_linear_transform_figure(
    transformed: np.ndarray,
    i_hat: np.ndarray,
    j_hat: np.ndarray,
    frames: list[go.Frame],
) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Scatter(
                x=transformed[0],
                y=transformed[1],
                mode="lines",
                line={"color": "rgba(15, 82, 186, 0.35)", "width": 2},
            ),
            go.Scatter(
                x=[0, i_hat[0]],
                y=[0, i_hat[1]],
                mode="lines",
                line={"color": PALETTE["coral"], "width": 5},
                name="i-hat",
            ),
            go.Scatter(
                x=[0, j_hat[0]],
                y=[0, j_hat[1]],
                mode="lines",
                line={"color": PALETTE["jade"], "width": 5},
                name="j-hat",
            ),
        ],
        frames=frames,
    )
    figure.update_layout(
        **transparent_plotly_layout(height=520),
        xaxis={"range": [-8, 8], "showgrid": False, "zeroline": True},
        yaxis={"range": [-8, 8], "showgrid": False, "zeroline": True, "scaleanchor": "x", "scaleratio": 1},
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play transform",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 45, "redraw": True}, "fromcurrent": False}],
                    }
                ],
                "x": 0.5,
                "xanchor": "center",
                "y": 1.04,
                "yanchor": "bottom",
            }
        ],
        showlegend=False,
    )
    return figure


@st.cache_data(show_spinner=False)
def compute_surface_frames() -> tuple[tuple[np.ndarray, np.ndarray, np.ndarray], list[go.Frame]]:
    u_value = np.linspace(-np.pi, np.pi, 48)
    v_value = np.linspace(-2, 2, 48)
    grid_u, grid_v = np.meshgrid(u_value, v_value)

    frames: list[go.Frame] = []
    for theta in np.linspace(0, np.pi / 2, 40):
        x_value = np.cos(theta) * np.sinh(grid_v) * np.sin(grid_u) + np.sin(theta) * np.cosh(grid_v) * np.cos(grid_u)
        y_value = -np.cos(theta) * np.sinh(grid_v) * np.cos(grid_u) + np.sin(theta) * np.cosh(grid_v) * np.sin(grid_u)
        z_value = grid_u * np.cos(theta) + grid_v * np.sin(theta)
        frames.append(go.Frame(data=[go.Surface(x=x_value, y=y_value, z=z_value)], traces=[0]))

    x_initial = np.sinh(grid_v) * np.sin(grid_u)
    y_initial = -np.sinh(grid_v) * np.cos(grid_u)
    z_initial = grid_u
    return (x_initial, y_initial, z_initial), frames


def build_surface_figure(initial_surface: tuple[np.ndarray, np.ndarray, np.ndarray], frames: list[go.Frame]) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Surface(
                x=initial_surface[0],
                y=initial_surface[1],
                z=initial_surface[2],
                colorscale="Magma",
                showscale=False,
            )
        ],
        frames=frames,
    )
    figure.update_layout(
        **transparent_plotly_layout(height=640),
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play morph",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 60, "redraw": True}, "fromcurrent": True}],
                    }
                ],
                "x": 0.5,
                "xanchor": "center",
                "y": 1.03,
                "yanchor": "bottom",
            }
        ],
        scene={
            "xaxis": {"range": [-4, 4], "visible": False},
            "yaxis": {"range": [-4, 4], "visible": False},
            "zaxis": {"range": [-4, 4], "visible": False},
            "camera": {"eye": {"x": 1.25, "y": 1.2, "z": 0.55}},
        },
    )
    return figure


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "Animations",
        "These exhibits focus on process. One demo shows how a basis transforms in the plane;"
        " the other tracks a continuous surface deformation.",
        kicker="Mathematical Motion",
    )

    tab_linear, tab_surface = st.tabs(["Linear Algebra", "Surface Morph"])

    with tab_linear:
        st.markdown("### Continuous linear transformation")
        c1, c2 = st.columns(2)
        a11 = c1.number_input("a11", -2.0, 2.0, 1.5, 0.1)
        a21 = c1.number_input("a21", -2.0, 2.0, 0.5, 0.1)
        a12 = c2.number_input("a12", -2.0, 2.0, 1.0, 0.1)
        a22 = c2.number_input("a22", -2.0, 2.0, 1.2, 0.1)

        matrix, transformed, i_hat, j_hat, frames = compute_linear_transform_frames((a11, a12, a21, a22))
        determinant = float(np.linalg.det(matrix))
        info_col, chart_col = st.columns([1.1, 1.9])
        with info_col:
            st.latex(f"\\det(A) = {determinant:.2f}")
            if determinant < 0:
                st.warning("This matrix reverses orientation.")
            elif abs(determinant) < 0.05:
                st.info("The determinant is near zero, so the plane is almost collapsed.")
            else:
                st.success(f"Area is scaled by a factor of {abs(determinant):.2f}.")
        with chart_col:
            st.plotly_chart(
                build_linear_transform_figure(transformed, i_hat, j_hat, frames),
                width="stretch",
            )

    with tab_surface:
        st.markdown("### From catenoid to helicoid")
        initial_surface, frames = compute_surface_frames()
        st.plotly_chart(
            build_surface_figure(initial_surface, frames),
            width="stretch",
        )