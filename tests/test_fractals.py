from __future__ import annotations

import numpy as np

from ultramarine.features.fractals import COOL_FRACTAL_SCALE, build_escape_figure
from ultramarine.math.fractals import julia_escape, mandelbrot_escape


def test_mandelbrot_escape_shape_and_bounds() -> None:
    result = mandelbrot_escape(
        x_min=-2.0,
        x_max=0.8,
        y_min=-1.2,
        y_max=1.2,
        width=40,
        height=24,
        max_iter=30,
    )

    assert result.shape == (24, 40)
    assert np.min(result) >= 0
    assert np.max(result) <= 31


def test_julia_escape_shape_and_bounds() -> None:
    result = julia_escape(
        c_real=-0.74,
        c_imag=0.18,
        extent=1.7,
        width=36,
        height=36,
        max_iter=28,
    )

    assert result.shape == (36, 36)
    assert np.isfinite(result).all()


def test_build_escape_figure_uses_cool_colorscale() -> None:
    data = np.arange(16, dtype=float).reshape(4, 4)

    figure = build_escape_figure(
        data,
        x_range=(-1.0, 1.0),
        y_range=(-1.0, 1.0),
        height=320,
    )

    assert figure.data[0].colorscale == tuple(tuple(item) for item in COOL_FRACTAL_SCALE)
    assert figure.layout.height == 320


def test_mandelbrot_known_escape_times_and_non_escape_sentinel() -> None:
    def point(real):
        return mandelbrot_escape(
            x_min=real, x_max=real, y_min=0, y_max=0, width=1, height=1, max_iter=10
        )[0, 0]

    assert point(3) == 1
    assert point(1) == 3
    assert point(0) == point(-1) == point(-2) == 11


def test_julia_uses_safe_radius_for_large_parameters() -> None:
    # z=-3 is fixed under z²-12; a universal radius 2 incorrectly labels it as escaped.
    result = julia_escape(c_real=-12, c_imag=0, extent=3, width=1, height=3, max_iter=10)
    assert result[1, 0] == 11
