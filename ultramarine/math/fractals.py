from __future__ import annotations

import numpy as np


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
    real = np.linspace(x_min, x_max, width)
    imag = np.linspace(y_min, y_max, height)
    c_values = real[None, :] + 1j * imag[:, None]
    z_values = np.zeros_like(c_values)
    escaped = np.zeros(c_values.shape, dtype=bool)
    counts = np.full(c_values.shape, max_iter, dtype=np.float64)

    for iteration in range(max_iter):
        active = ~escaped
        z_values[active] = z_values[active] ** 2 + c_values[active]
        newly_escaped = active & (np.abs(z_values) > 2)
        counts[newly_escaped] = iteration
        escaped |= newly_escaped

    return counts


def julia_escape(
    *,
    c_real: float,
    c_imag: float,
    extent: float,
    width: int,
    height: int,
    max_iter: int,
) -> np.ndarray:
    real = np.linspace(-extent, extent, width)
    imag = np.linspace(-extent, extent, height)
    z_values = real[None, :] + 1j * imag[:, None]
    c_value = complex(c_real, c_imag)
    escaped = np.zeros(z_values.shape, dtype=bool)
    counts = np.full(z_values.shape, max_iter, dtype=np.float64)

    for iteration in range(max_iter):
        active = ~escaped
        z_values[active] = z_values[active] ** 2 + c_value
        newly_escaped = active & (np.abs(z_values) > 2)
        counts[newly_escaped] = iteration
        escaped |= newly_escaped

    return counts
