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
    assert np.max(result) <= 30


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
