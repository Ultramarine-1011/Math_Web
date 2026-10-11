import numpy as np
import pytest

from ultramarine.math.optimization import gradient, gradient_descent, objective
from ultramarine.math.regression import fit_regression, generate_regression_data


@pytest.mark.parametrize("point", [[0, 0], [-3.2, 3], [4, -4]])
def test_analytic_gradient_matches_finite_difference(point: list) -> None:
    point = np.array(point, dtype=float)
    step = 1e-6
    numeric = [
        (objective(*(point + step * axis)) - objective(*(point - step * axis))) / (2 * step)
        for axis in np.eye(2)
    ]
    assert np.allclose(gradient(point), numeric, atol=1e-8)


@pytest.mark.parametrize("rate", [0.01, 0.15, 1.5])
def test_gradient_descent_decreases_objective(rate: float) -> None:
    path, losses = gradient_descent(rate, -3.2, 3, 100)
    assert path.shape == (101, 2)
    assert np.array_equal(path[0], [-3.2, 3])
    assert (np.diff(losses) <= 1e-12).all()


def test_gradient_descent_zero_steps_and_invalid_rate() -> None:
    assert len(gradient_descent(0.1, 0, 0, 0)[0]) == 1
    with pytest.raises(ValueError):
        gradient_descent(0, 0, 0)


def test_regression_recovers_noiseless_parameters() -> None:
    x, y, _, _ = generate_regression_data(120, 0, 42)
    result = fit_regression(x, y, steps=200)
    assert np.allclose(result.optimum, [1, 2], atol=1e-12)
    assert np.allclose(result.weights[-1], result.optimum, atol=1e-9)


@pytest.mark.parametrize("penalty", [0.0, 0.5, 3.0])
def test_ridge_matches_normal_equations_and_gd_converges(penalty: float) -> None:
    x, y, _, _ = generate_regression_data(120, 0.8, 42)
    design = np.column_stack([np.ones_like(x), x])
    expected = np.linalg.solve(design.T @ design + len(x) * np.diag([0, penalty]), design.T @ y)
    fit = fit_regression(x, y, penalty, steps=400)
    assert np.allclose(fit.optimum, expected, atol=1e-12)
    assert np.allclose(fit.weights[-1], expected, atol=1e-9)
    assert (np.diff(fit.losses) <= 1e-12).all()
    objective = np.mean((design @ fit.optimum - y) ** 2) + penalty * fit.optimum[1] ** 2
    assert fit.losses[-1] == pytest.approx(objective)


def test_ridge_does_not_penalize_intercept() -> None:
    x = np.linspace(-2, 2, 20)
    fit = fit_regression(x, 5 + 2 * x, penalty=3, steps=400)
    assert fit.optimum[0] == pytest.approx(5)
    assert 0 < fit.optimum[1] < 2


def test_singular_design_has_finite_minimum_norm_solution() -> None:
    x, y = np.zeros(10), np.full(10, 3.0)
    fit = fit_regression(x, y, steps=100)
    assert np.allclose(fit.optimum, [3, 0])
    assert np.allclose(fit.weights[-1], fit.optimum)


def test_unstable_learning_rate_stops_at_loss_limit() -> None:
    x, y, _, _ = generate_regression_data(120, 0.8, 42)
    fit = fit_regression(x, y, rate_fraction=1.2, steps=300)
    assert len(fit.losses) < 301
    assert fit.losses[-1] > 1e12
    assert np.isfinite(fit.weights).all()


def test_data_split_is_reproducible_and_complete() -> None:
    data = generate_regression_data(120, 0.8, 42)
    assert [len(part) for part in data] == [90, 90, 30, 30]
    assert all(np.array_equal(a, b) for a, b in zip(data, generate_regression_data(120, 0.8, 42)))
    assert not np.array_equal(data[0], generate_regression_data(120, 0.8, 43)[0])


@pytest.mark.parametrize("kwargs", [{"penalty": -1}, {"rate_fraction": 0}, {"steps": -1}])
def test_invalid_regression_parameters(kwargs: dict) -> None:
    with pytest.raises(ValueError):
        fit_regression(np.array([1, 2]), np.array([1, 2]), **kwargs)
