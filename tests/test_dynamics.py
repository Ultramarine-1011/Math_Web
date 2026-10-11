import numpy as np

from ultramarine.math.dynamics import compute_heart_curve, solve_lorenz


def test_lorenz_trajectory_is_finite_and_starts_at_specified_state() -> None:
    time, x, y, z = solve_lorenz(10, 28, 8 / 3)
    assert np.array_equal([x[0], y[0], z[0]], [1, 1, 1])
    assert len(time) == len(x) == len(y) == len(z) == 4500
    assert np.isfinite([x, y, z]).all()


def test_heart_curve_is_closed_and_reflection_symmetric() -> None:
    x, y = compute_heart_curve()
    assert np.allclose([x[0], y[0]], [x[-1], y[-1]])
    assert np.allclose(x, -x[::-1], atol=1e-13)
    assert np.allclose(y, y[::-1], atol=1e-13)
