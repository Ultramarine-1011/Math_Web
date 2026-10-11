"""Linear and ridge regression with an unpenalized intercept."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def generate_regression_data(
    sample_size: int, noise: float, seed: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if sample_size < 4 or noise < 0 or not np.isfinite(noise):
        raise ValueError("At least four samples and nonnegative finite noise are required.")
    rng = np.random.default_rng(seed)
    x = rng.uniform(-2, 2, sample_size)
    y = 1 + 2 * x + rng.normal(0, noise, sample_size)
    split = int(sample_size * 0.75)
    return x[:split], y[:split], x[split:], y[split:]


@dataclass(frozen=True)
class RegressionFit:
    weights: np.ndarray
    losses: np.ndarray
    optimum: np.ndarray
    stability_limit: float


def fit_regression(
    x: np.ndarray,
    y: np.ndarray,
    penalty: float = 0.0,
    rate_fraction: float = 0.8,
    steps: int = 100,
) -> RegressionFit:
    """GD on MSE + penalty*slope²; rate_fraction multiplies the 2/L bound.

    Iteration stops if loss exceeds 1e12 to bound deliberately unstable experiments.
    The reference solution uses augmented least squares, including singular designs.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or not x.size:
        raise ValueError("x and y must be nonempty vectors of equal length.")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Observations must be finite.")
    if penalty < 0 or rate_fraction <= 0 or not np.isfinite([penalty, rate_fraction]).all():
        raise ValueError("Penalty must be nonnegative and rate fraction positive.")
    if steps < 0:
        raise ValueError("Steps must be nonnegative.")
    design = np.column_stack([np.ones_like(x), x])
    regularizer = np.diag([0.0, penalty])
    hessian = 2 * (design.T @ design / x.size + regularizer)
    limit = 2 / np.linalg.eigvalsh(hessian)[-1]
    augmented = np.vstack([design, [0, np.sqrt(x.size * penalty)]])
    optimum = np.linalg.lstsq(augmented, np.append(y, 0.0), rcond=None)[0]
    weights = [np.zeros(2)]
    losses = [float(np.mean(y**2))]
    for _ in range(steps):
        current = weights[-1]
        grad = 2 * (design.T @ (design @ current - y) / x.size + regularizer @ current)
        updated = current - rate_fraction * limit * grad
        loss = float(np.mean((design @ updated - y) ** 2) + penalty * updated[1] ** 2)
        weights.append(updated)
        losses.append(loss)
        if loss > 1e12:
            break
    return RegressionFit(np.array(weights), np.array(losses), optimum, float(limit))
