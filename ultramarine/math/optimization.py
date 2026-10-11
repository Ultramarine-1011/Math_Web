"""Deterministic optimization kernels, independent of the UI."""

from __future__ import annotations

import numpy as np


def objective(x: np.ndarray | float, y: np.ndarray | float) -> np.ndarray | float:
    return (x**2 + y**2) / 10 + np.sin(x) + np.cos(y)


def gradient(point: np.ndarray) -> np.ndarray:
    x, y = point
    return np.array([x / 5 + np.cos(x), y / 5 - np.sin(y)])


def gradient_descent(
    learning_rate: float, start_x: float, start_y: float, steps: int = 80
) -> tuple[np.ndarray, np.ndarray]:
    if not np.isfinite([learning_rate, start_x, start_y]).all() or learning_rate <= 0:
        raise ValueError("Learning rate must be positive and all inputs finite.")
    if steps < 0:
        raise ValueError("Steps must be nonnegative.")
    path = np.empty((steps + 1, 2))
    path[0] = [start_x, start_y]
    for index in range(steps):
        path[index + 1] = path[index] - learning_rate * gradient(path[index])
    return path, np.asarray(objective(path[:, 0], path[:, 1]))
