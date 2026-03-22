from pathlib import Path

import streamlit as st

from ultramarine.config import load_settings
from ultramarine.features import home

settings = load_settings(base_dir=Path(__file__).resolve().parents[2])
st.session_state["_page_registry"] = {}
home.render(settings)
