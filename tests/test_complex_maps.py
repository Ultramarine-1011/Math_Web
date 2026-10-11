import numpy as np
import pytest

from ultramarine.math.complex_maps import (
    apply_complex_map,
    build_complex_morph_lines,
    domain_coloring,
)


def test_power_and_exponential_do_not_clip_mathematical_inputs() -> None:
    values = np.array([1 + 1j, 9 + 0j])
    assert np.allclose(apply_complex_map(values, "power"), values**2)
    assert np.allclose(apply_complex_map(values, "exponential"), np.exp(values))


def test_mobius_pole_and_regular_values() -> None:
    values = np.array([1 + 0j, 2 + 0j])
    mapped = apply_complex_map(values, "mobius", denominator_shift=1, numerator_shift=-1)
    assert np.isnan(mapped[0])
    assert mapped[1] == pytest.approx(3)


def test_fractional_power_uses_principal_branch() -> None:
    assert apply_complex_map(np.array([-1 + 0j]), "power", power=0.5)[0] == pytest.approx(1j)


def test_domain_phase_masks_zero_and_pole() -> None:
    phase = domain_coloring("power", samples=33, extent=2)
    assert phase.shape == (33, 33)
    assert np.isnan(phase[16, 16])
    assert phase[16, 20] == pytest.approx(0.5)


def test_morph_preserves_initial_grid_and_hides_out_of_bounds_targets() -> None:
    source, frames = build_complex_morph_lines(
        "inverse_affine",
        extent=2,
        lines=5,
        samples_per_line=25,
        frame_count=8,
        denominator_shift=0,
        clip_limit=5,
    )
    assert len(source) == 10 and len(frames) == 8
    assert all(np.array_equal(a, b) for a, b in zip(source, frames[0]))
    finite = np.concatenate(frames[-1])
    assert np.isnan(finite).any()
    finite = finite[np.isfinite(finite)]
    assert np.max(np.abs(finite.real)) <= 5
    assert np.max(np.abs(finite.imag)) <= 5


def test_unknown_complex_map_raises() -> None:
    with pytest.raises(ValueError):
        apply_complex_map(np.array([1j]), "unknown")
