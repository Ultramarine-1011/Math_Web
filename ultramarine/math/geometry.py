"""Planar linear maps and the catenoid/helicoid associated family."""

import numpy as np


def linear_transform(
    matrix_values: tuple[float, float, float, float], progress: float = 1.0
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    matrix = np.asarray(matrix_values, dtype=float).reshape(2, 2)
    if not np.isfinite(matrix).all() or not 0 <= progress <= 1:
        raise ValueError("Matrix must be finite and progress in [0, 1].")
    lines = []
    for index in range(-5, 6):
        lines.extend([[index, -5], [index, 5], [np.nan, np.nan]])
        lines.extend([[-5, index], [5, index], [np.nan, np.nan]])
    grid = np.array(lines).T
    current = (1 - progress) * np.eye(2) + progress * matrix
    transformed = current @ np.nan_to_num(grid)
    transformed[:, np.isnan(grid[0])] = np.nan
    return matrix, transformed, current[:, 0], current[:, 1]


def associated_surface(
    theta: float, samples: int = 56
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """theta=0 is a catenoid; theta=pi/2 is its conjugate helicoid."""
    u, v = np.meshgrid(np.linspace(-np.pi, np.pi, samples), np.linspace(-2, 2, samples))
    x = np.cos(theta) * np.cosh(v) * np.cos(u) + np.sin(theta) * np.sinh(v) * np.sin(u)
    y = np.cos(theta) * np.cosh(v) * np.sin(u) - np.sin(theta) * np.sinh(v) * np.cos(u)
    z = v * np.cos(theta) + u * np.sin(theta)
    return x, y, z
