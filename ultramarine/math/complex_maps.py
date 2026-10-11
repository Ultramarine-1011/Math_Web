"""Exact complex maps; display bounds are applied only by the rendering helpers."""

from __future__ import annotations

import numpy as np

EPSILON = 1e-9


def apply_complex_map(
    z_values: np.ndarray,
    map_name: str,
    *,
    power: float = 2.0,
    scale: complex = 1 + 0j,
    shift: complex = 0j,
    numerator_shift: complex = 0j,
    denominator_shift: complex = 0j,
) -> np.ndarray:
    z_values = np.asarray(z_values, dtype=complex)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        if map_name == "power":
            mapped = scale * z_values**power + shift
        elif map_name == "exponential":
            mapped = np.exp(scale * z_values) + shift
        elif map_name in {"inverse_affine", "mobius"}:
            denominator = z_values - denominator_shift
            safe = np.where(np.abs(denominator) < EPSILON, np.nan + 1j * np.nan, denominator)
            numerator = 1 if map_name == "inverse_affine" else z_values - numerator_shift
            mapped = scale * numerator / safe + shift
        else:
            raise ValueError(f"Unknown complex map: {map_name}")
    return np.where(np.isfinite(mapped), mapped, np.nan + 1j * np.nan)


def domain_coloring(map_name: str, samples: int, extent: float, **parameters) -> np.ndarray:
    """Phase in [0, 1]; zeros and poles have no defined phase and are masked."""
    axis = np.linspace(-extent, extent, samples)
    mapped = apply_complex_map(axis[None, :] + 1j * axis[:, None], map_name, **parameters)
    phase = (np.angle(mapped) + np.pi) / (2 * np.pi)
    return np.where(np.isfinite(mapped) & (np.abs(mapped) > 0), phase, np.nan)


def complex_grid_lines(*, extent: float, lines: int, samples_per_line: int) -> list[np.ndarray]:
    axis = np.linspace(-extent, extent, samples_per_line)
    levels = np.linspace(-extent, extent, lines)
    traces = []
    for level in levels:
        traces.extend([axis + 1j * level, level + 1j * axis])
    return traces


def build_complex_morph_lines(
    map_name: str,
    *,
    extent: float,
    lines: int,
    samples_per_line: int,
    frame_count: int,
    clip_limit: float = 5.0,
    **parameters,
) -> tuple[list[np.ndarray], list[list[np.ndarray]]]:
    source_lines = complex_grid_lines(extent=extent, lines=lines, samples_per_line=samples_per_line)
    target_lines = []
    for line in source_lines:
        mapped = apply_complex_map(line, map_name, **parameters)
        visible = (np.abs(mapped.real) <= clip_limit) & (np.abs(mapped.imag) <= clip_limit)
        target_lines.append(np.where(visible, mapped, np.nan + 1j * np.nan))
    frames = []
    for raw_progress in np.linspace(0, 1, frame_count):
        progress = raw_progress**2 * (3 - 2 * raw_progress)
        # Keep the complete original grid even where the target has a pole.
        frames.append(
            [
                source.copy() if progress == 0 else (1 - progress) * source + progress * target
                for source, target in zip(source_lines, target_lines)
            ]
        )
    return source_lines, frames
