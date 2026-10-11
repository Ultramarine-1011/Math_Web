import numpy as np
import pytest
from scipy.stats import t

from ultramarine.math.statistics import simulate_galton_board, simulate_mean_intervals


@pytest.mark.parametrize("balls", [1, 7, 50, 101])
def test_galton_conserves_exact_ball_count_including_partial_batches(balls: int) -> None:
    result = simulate_galton_board(balls, 42, levels=8, batch_size=50)
    assert result[-1].sum() == balls
    assert np.array_equal(result.sum(axis=1), np.minimum(np.arange(1, len(result) + 1) * 50, balls))
    assert (np.diff(result, axis=0) >= 0).all()


@pytest.mark.parametrize("probability,slot", [(0.0, 0), (1.0, 12)])
def test_galton_degenerate_probabilities(probability: float, slot: int) -> None:
    result = simulate_galton_board(123, 42, levels=12, probability=probability)
    assert result[-1, slot] == 123


def test_galton_seed_and_batch_invariance() -> None:
    one = simulate_galton_board(1234, 42, probability=0.3)
    two = simulate_galton_board(1234, 42, probability=0.3, batch_size=73)
    assert np.array_equal(one[-1], two[-1])
    assert np.array_equal(one, simulate_galton_board(1234, 42, probability=0.3))


def test_galton_matches_binomial_moments() -> None:
    bins = simulate_galton_board(100_000, 1011, levels=20, probability=0.3, batch_size=100_000)[-1]
    x = np.arange(len(bins))
    mean = x @ bins / bins.sum()
    variance = (x - mean) ** 2 @ bins / bins.sum()
    assert mean == pytest.approx(6, abs=0.03)
    assert variance == pytest.approx(4.2, abs=0.06)


def test_intervals_use_student_t_and_unbiased_sample_variance() -> None:
    n = 5
    result = simulate_mean_intervals(n, 4, 0.95, 42)
    sample = np.random.default_rng(42).standard_normal((4, n))
    expected_se = sample.std(axis=1, ddof=1) / np.sqrt(n)
    assert np.allclose(result.standard_errors, expected_se)
    assert np.allclose(result.means, sample.mean(axis=1))
    assert np.allclose(result.upper - result.means, t.ppf(0.975, n - 1) * expected_se)


def test_normal_intervals_have_nominal_coverage() -> None:
    repetitions, confidence = 6000, 0.95
    result = simulate_mean_intervals(5, repetitions, confidence, 1011, mean=3, sigma=2)
    mc_se = np.sqrt(confidence * (1 - confidence) / repetitions)
    assert abs(result.covered.mean() - confidence) < 4 * mc_se


def test_shift_scale_equivariance_and_reproducibility() -> None:
    base = simulate_mean_intervals(20, 500, 0.95, 42, "exponential")
    shifted = simulate_mean_intervals(20, 500, 0.95, 42, "exponential", mean=4, sigma=3)
    assert np.allclose(shifted.means, 4 + 3 * base.means)
    assert np.allclose(shifted.lower, 4 + 3 * base.lower)
    assert np.array_equal(shifted.covered, base.covered)
    assert np.array_equal(
        base.means, simulate_mean_intervals(20, 500, 0.95, 42, "exponential").means
    )


def test_higher_confidence_produces_nested_intervals() -> None:
    low = simulate_mean_intervals(20, 500, 0.9, 42)
    high = simulate_mean_intervals(20, 500, 0.99, 42)
    assert (high.lower <= low.lower).all()
    assert (high.upper >= low.upper).all()


@pytest.mark.parametrize(
    "kwargs", [{"sample_size": 1}, {"sigma": 0}, {"confidence": 1}, {"distribution": "unknown"}]
)
def test_invalid_interval_parameters(kwargs: dict) -> None:
    arguments = {"sample_size": 20, "repetitions": 10, "confidence": 0.95, "seed": 42} | kwargs
    with pytest.raises(ValueError):
        simulate_mean_intervals(**arguments)
