"""Numerical trajectories and parametric curves."""

import numpy as np
from scipy.integrate import odeint


def solve_lorenz(
    sigma: float, rho: float, beta: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    def lorenz_system(state: tuple[float, float, float], _: float) -> list[float]:
        x_value, y_value, z_value = state
        return [
            sigma * (y_value - x_value),
            x_value * (rho - z_value) - y_value,
            x_value * y_value - beta * z_value,
        ]

    time = np.linspace(0, 48, 4500)
    solution = odeint(lorenz_system, (1.0, 1.0, 1.0), time)
    return time, solution[:, 0], solution[:, 1], solution[:, 2]


def compute_heart_curve(samples: int = 900) -> tuple[np.ndarray, np.ndarray]:
    t_values = np.linspace(0, 2 * np.pi, samples)
    x_value = 16 * np.sin(t_values) ** 3
    y_value = (
        13 * np.cos(t_values)
        - 5 * np.cos(2 * t_values)
        - 2 * np.cos(3 * t_values)
        - np.cos(4 * t_values)
    )
    return x_value, y_value
