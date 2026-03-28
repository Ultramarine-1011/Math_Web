from __future__ import annotations

import os
import tempfile
from pathlib import Path

TMP_ROOT = Path(__file__).resolve().parent / ".tmp"
TMP_ROOT.mkdir(parents=True, exist_ok=True)
os.environ["TMP"] = str(TMP_ROOT)
os.environ["TEMP"] = str(TMP_ROOT)
tempfile.tempdir = str(TMP_ROOT)
