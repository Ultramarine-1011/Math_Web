from pathlib import Path

from ultramarine.config import load_settings
from ultramarine.features import data_lab

settings = load_settings(base_dir=Path(__file__).resolve().parents[2])
data_lab.render(settings)
