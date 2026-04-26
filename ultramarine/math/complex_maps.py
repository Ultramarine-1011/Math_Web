from __future__ import annotations

import numpy as np


EPSILON = 1e-9


def complex_grid(samples: int, extent: float) -> np.ndarray:
    axis = np.linspace(-extent, extent, samples)
    real, imag = np.meshgrid(axis, axis)
    return real + 1j * imag


def apply_complex_map(z_values: np.ndarray, map_name: str, parameter: complex = 0j) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        if map_name == "square":
            mapped = z_values**2
        elif map_name == "inverse":
            mapped = 1 / np.where(np.abs(z_values) < EPSILON, np.nan + 0j, z_values)
        elif map_name == "exponential":
            mapped = np.exp(np.clip(z_values.real, -4, 4) + 1j * z_values.imag)
        elif map_name == "mobius":
            a_value = parameter
            denominator = 1 - np.conj(a_value) * z_values
            mapped = (z_values - a_value) / np.where(np.abs(denominator) < EPSILON, np.nan + 0j, denominator)
        else:
            raise ValueError(f"Unknown complex map: {map_name}")
    return np.where(np.isfinite(mapped.real) & np.isfinite(mapped.imag), mapped, np.nan + 1j * np.nan)


def apply_parametric_complex_map(
    z_values: np.ndarray,
    map_name: str,
    *,
    power: float = 2.0,
    scale: complex = 1 + 0j,
    shift: complex = 0j,
    numerator_shift: complex = 0j,
    denominator_shift: complex = 0j,
) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        if map_name == "power":
            safe_radius = np.clip(np.abs(z_values), 0, 8)
            mapped = scale * (safe_radius**power) * np.exp(1j * power * np.angle(z_values)) + shift
        elif map_name == "inverse_affine":
            denominator = z_values - denominator_shift
            mapped = scale / np.where(np.abs(denominator) < EPSILON, np.nan + 0j, denominator) + shift
        elif map_name == "exponential":
            clipped = np.clip((scale * z_values).real, -5, 5) + 1j * (scale * z_values).imag
            mapped = np.exp(clipped) + shift
        elif map_name == "mobius":
            denominator = z_values - denominator_shift
            mapped = scale * (z_values - numerator_shift) / np.where(
                np.abs(denominator) < EPSILON,
                np.nan + 0j,
                denominator,
            ) + shift
        else:
            return apply_complex_map(z_values, map_name, shift)

    finite = np.isfinite(mapped.real) & np.isfinite(mapped.imag) & (np.abs(mapped) < 1e6)
    return np.where(finite, mapped, np.nan + 1j * np.nan)


def clip_complex_values(values: np.ndarray, limit: float) -> np.ndarray:
    clipped_real = np.clip(values.real, -limit, limit)
    clipped_imag = np.clip(values.imag, -limit, limit)
    finite = np.isfinite(values.real) & np.isfinite(values.imag)
    return np.where(finite, clipped_real + 1j * clipped_imag, np.nan + 1j * np.nan)


def domain_coloring(map_name: str, samples: int, extent: float, parameter: complex = 0j) -> np.ndarray:
    z_values = complex_grid(samples, extent)
    mapped = apply_complex_map(z_values, map_name, parameter)
    angle = (np.angle(mapped) + np.pi) / (2 * np.pi)
    magnitude = np.log1p(np.abs(mapped))
    magnitude = magnitude / np.nanmax(magnitude) if np.nanmax(magnitude) > 0 else magnitude
    return np.nan_to_num(angle * 0.72 + magnitude * 0.28, nan=0.0, posinf=1.0, neginf=0.0)


def mapped_grid_lines(
    map_name: str,
    *,
    extent: float = 2.0,
    lines: int = 13,
    samples_per_line: int = 160,
    parameter: complex = 0j,
) -> list[tuple[np.ndarray, np.ndarray]]:
    axis = np.linspace(-extent, extent, samples_per_line)
    levels = np.linspace(-extent, extent, lines)
    traces: list[tuple[np.ndarray, np.ndarray]] = []

    for level in levels:
        horizontal = axis + 1j * level
        vertical = level + 1j * axis
        for line in (horizontal, vertical):
            mapped = apply_complex_map(line, map_name, parameter)
            traces.append((mapped.real, mapped.imag))
    return traces


def complex_grid_lines(
    *,
    extent: float,
    lines: int,
    samples_per_line: int,
) -> list[np.ndarray]:
    axis = np.linspace(-extent, extent, samples_per_line)
    levels = np.linspace(-extent, extent, lines)
    traces: list[np.ndarray] = []
    for level in levels:
        traces.append(axis + 1j * level)
        traces.append(level + 1j * axis)
    return traces


def build_complex_morph_lines(
    map_name: str,
    *,
    extent: float,
    lines: int,
    samples_per_line: int,
    frame_count: int,
    power: float = 2.0,
    scale: complex = 1 + 0j,
    shift: complex = 0j,
    numerator_shift: complex = 0j,
    denominator_shift: complex = 0j,
    clip_limit: float = 5.0,
) -> tuple[list[np.ndarray], list[list[np.ndarray]]]:
    source_lines = complex_grid_lines(
        extent=extent,
        lines=lines,
        samples_per_line=samples_per_line,
    )
    target_lines = [
        clip_complex_values(
            apply_parametric_complex_map(
                line,
                map_name,
                power=power,
                scale=scale,
                shift=shift,
                numerator_shift=numerator_shift,
                denominator_shift=denominator_shift,
            ),
            clip_limit,
        )
        for line in source_lines
    ]
    frames: list[list[np.ndarray]] = []
    for raw_progress in np.linspace(0, 1, frame_count):
        progress = raw_progress * raw_progress * (3 - 2 * raw_progress)
        frames.append([(1 - progress) * source + progress * target for source, target in zip(source_lines, target_lines)])
    return source_lines, frames
