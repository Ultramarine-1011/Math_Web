"""Seeded binomial simulation and repeated mean confidence intervals."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import t


def simulate_galton_board(
    num_balls: int,
    seed: int,
    levels: int = 20,
    probability: float = 0.5,
    batch_size: int = 50,
) -> np.ndarray:
    """Return cumulative bin counts, including the last partial batch."""
    if num_balls < 1 or levels < 1 or batch_size < 1:
        raise ValueError("Ball count, levels and batch size must be positive.")
    if not 0 <= probability <= 1:
        raise ValueError("Probability must lie in [0, 1].")
    positions = np.random.default_rng(seed).binomial(levels, probability, size=num_balls)
    counts = np.zeros(levels + 1, dtype=np.int64)
    batches = []
    for start in range(0, num_balls, batch_size):
        counts += np.bincount(positions[start : start + batch_size], minlength=levels + 1)
        batches.append(counts.copy())
    return np.array(batches)


@dataclass(frozen=True)
class ConfidenceSimulation:
    means: np.ndarray
    standard_errors: np.ndarray
    lower: np.ndarray
    upper: np.ndarray
    covered: np.ndarray


def simulate_mean_intervals(
    sample_size: int,
    repetitions: int,
    confidence: float,
    seed: int,
    distribution: str = "normal",
    mean: float = 0.0,
    sigma: float = 1.0,
) -> ConfidenceSimulation:
    """Two-sided Student t intervals; exact for iid normal samples only."""
    if sample_size < 2 or repetitions < 1:
        raise ValueError("At least two observations and one repetition are required.")
    if not 0 < confidence < 1 or sigma <= 0 or not np.isfinite([mean, sigma]).all():
        raise ValueError("Invalid confidence level or population parameters.")
    rng = np.random.default_rng(seed)
    shape = (repetitions, sample_size)
    if distribution == "normal":
        standardized = rng.standard_normal(shape)
    elif distribution == "exponential":
        standardized = rng.exponential(size=shape) - 1
    else:
        raise ValueError(f"Unknown distribution: {distribution}")
    samples = mean + sigma * standardized
    means = samples.mean(axis=1)
    errors = samples.std(axis=1, ddof=1) / np.sqrt(sample_size)
    margin = t.ppf((1 + confidence) / 2, df=sample_size - 1) * errors
    lower, upper = means - margin, means + margin
    return ConfidenceSimulation(means, errors, lower, upper, (lower <= mean) & (mean <= upper))
