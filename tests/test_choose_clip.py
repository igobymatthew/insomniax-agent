import sys
from pathlib import Path

import pytest

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from librosa_stub import install as install_librosa_stub

install_librosa_stub()

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from insomniax_autocut_v3 import choose_clip


def test_choose_clip_empty_clip_map_raises_value_error():
    with pytest.raises(ValueError, match="clip_map is empty"):
        choose_clip("scene", {})


def test_choose_clip_prefers_default_entry(monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.5)
    clip_map = {"default": "default.mp4", "other": "other.mp4"}

    selected = choose_clip("no match here", clip_map)

    assert selected == "default.mp4"
