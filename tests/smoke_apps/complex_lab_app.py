from pathlib import Path

from ultramarine.config import load_settings
from ultramarine.features import complex_lab

settings = load_settings(base_dir=Path(__file__).resolve().parents[2])
complex_lab.render(settings)
