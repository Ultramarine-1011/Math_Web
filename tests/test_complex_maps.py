from __future__ import annotations

import numpy as np

from ultramarine.math.complex_maps import (
    apply_complex_map,
    build_complex_morph_lines,
    domain_coloring,
    mapped_grid_lines,
)


def test_apply_complex_map_square() -> None:
    values = np.array([1 + 1j, 2 + 0j])

    mapped = apply_complex_map(values, "square")

    assert np.allclose(mapped, np.array([0 + 2j, 4 + 0j]))


def test_domain_coloring_shape() -> None:
    coloring = domain_coloring("exponential", samples=32, extent=2.0)

    assert coloring.shape == (32, 32)
    assert np.isfinite(coloring).all()


def test_mapped_grid_lines_returns_real_imag_pairs() -> None:
    traces = mapped_grid_lines("inverse", lines=5, samples_per_line=24)

    assert len(traces) == 10
    assert all(real.shape == imag.shape for real, imag in traces)


def test_build_complex_morph_lines_handles_poles() -> None:
    source_lines, frame_lines = build_complex_morph_lines(
        "inverse_affine",
        extent=2.0,
        lines=5,
        samples_per_line=24,
        frame_count=8,
        denominator_shift=0j,
    )

    assert len(source_lines) == 10
    assert len(frame_lines) == 8
    assert all(len(frame) == len(source_lines) for frame in frame_lines)
