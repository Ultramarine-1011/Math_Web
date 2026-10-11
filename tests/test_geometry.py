import numpy as np

from ultramarine.math.geometry import associated_surface, linear_transform


def test_linear_transform_basis_and_nan_line_breaks() -> None:
    matrix, grid, i_hat, j_hat = linear_transform((1, 2, 3, 4))
    assert np.array_equal(i_hat, [1, 3])
    assert np.array_equal(j_hat, [2, 4])
    assert np.isnan(grid[:, 2::3]).all()
    assert np.array_equal(grid[:, 0], matrix @ [-5, -5])
    _, _, start_i, start_j = linear_transform((1, 2, 3, 4), 0)
    assert np.array_equal(start_i, [1, 0])
    assert np.array_equal(start_j, [0, 1])


def test_surface_endpoints_match_catenoid_and_helicoid() -> None:
    x, y, z = associated_surface(0)
    assert np.allclose(x**2 + y**2, np.cosh(z) ** 2)
    x, y, z = associated_surface(np.pi / 2)
    # The conjugate helicoid uses a 90-degree angular offset.
    assert np.allclose(x * np.cos(z) + y * np.sin(z), 0, atol=1e-14)


def test_associated_surfaces_preserve_local_metric() -> None:
    # Numerical first fundamental forms agree away from the sampled boundary.
    forms = []
    for theta in (0, np.pi / 4, np.pi / 2):
        surface = np.stack(associated_surface(theta, 150), axis=-1)
        dv, du = np.gradient(surface, 4 / 149, 2 * np.pi / 149, axis=(0, 1))
        forms.append([np.sum(du**2, axis=-1), np.sum(dv**2, axis=-1), np.sum(du * dv, axis=-1)])
    for form in forms[1:]:
        for expected, actual in zip(forms[0], form):
            assert np.allclose(expected[2:-2, 2:-2], actual[2:-2, 2:-2], atol=0.006, rtol=0.001)
