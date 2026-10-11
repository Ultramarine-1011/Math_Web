"""Escape times counted from 1; max_iter+1 denotes no observed escape."""

from __future__ import annotations

import numpy as np


def _escape(z: np.ndarray, c: np.ndarray | complex, max_iter: int, radius: float) -> np.ndarray:
    if max_iter < 1:
        raise ValueError("Iteration budget must be positive.")
    counts = np.full(z.shape, max_iter + 1, dtype=np.int32)
    active = np.ones(z.shape, dtype=bool)
    # Julia initial values already outside the escape radius have escape time 0.
    outside = np.abs(z) > radius
    counts[outside] = 0
    active[outside] = False
    for iteration in range(1, max_iter + 1):
        if not active.any():
            break
        z[active] = z[active] ** 2 + (c[active] if isinstance(c, np.ndarray) else c)
        escaped = active & (np.abs(z) > radius)
        counts[escaped] = iteration
        active[escaped] = False
    return counts


def mandelbrot_escape(
    *,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    width: int,
    height: int,
    max_iter: int,
) -> np.ndarray:
    c = np.linspace(x_min, x_max, width)[None, :] + 1j * np.linspace(y_min, y_max, height)[:, None]
    return _escape(np.zeros_like(c), c, max_iter, 2.0)


def julia_escape(
    *,
    c_real: float,
    c_imag: float,
    extent: float,
    width: int,
    height: int,
    max_iter: int,
) -> np.ndarray:
    z = (
        np.linspace(-extent, extent, width)[None, :]
        + 1j * np.linspace(-extent, extent, height)[:, None]
    )
    c = complex(c_real, c_imag)
    radius = max(2.0, (1 + np.sqrt(1 + 4 * abs(c))) / 2)
    return _escape(z, c, max_iter, radius)
