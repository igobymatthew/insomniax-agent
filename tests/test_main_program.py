import json
import sys
import types
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from librosa_stub import install as install_librosa_stub

install_librosa_stub()

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import insomniax_autocut_v3 as autocut


def test_main_runs_program(tmp_path, monkeypatch):
    cue_path = tmp_path / "insomniax.json"
    cue_path.write_text(
        json.dumps(
            {
                "keyframes": [
                    {"scene": "First scene"},
                    {"scene": "Second scene"},
                ]
            }
        ),
        encoding="utf-8",
    )

    clip_path = tmp_path / "clip.mp4"
    clip_path.write_text("clip", encoding="utf-8")
    clip_map_path = tmp_path / "clip_map.json"
    clip_map_path.write_text(
        json.dumps({"default": str(clip_path)}),
        encoding="utf-8",
    )

    audio_path = tmp_path / "audio.wav"
    audio_path.write_text("audio", encoding="utf-8")

    monkeypatch.setattr(autocut, "CUE_SHEET", str(cue_path))
    monkeypatch.setattr(autocut, "CLIP_MAP", str(clip_map_path))
    monkeypatch.setattr(autocut, "AUDIO_TRACK", str(audio_path))

    out_dir = tmp_path / "segments"
    out_video = tmp_path / "output.mp4"
    monkeypatch.setattr(autocut, "OUT_DIR", str(out_dir))
    monkeypatch.setattr(autocut, "OUT_VIDEO", str(out_video))

    librosa = sys.modules["librosa"]
    librosa.beat.beat_track = lambda *args, **kwargs: (120.0, [0, 1, 2, 3, 4, 5])
    librosa.frames_to_time = lambda beats, sr=None: [float(b) for b in beats]

    monkeypatch.setattr(autocut.random, "random", lambda: 1.0)
    monkeypatch.setattr(autocut.random, "choices", lambda population, weights: [population[0]])

    ffmpeg_calls = []

    def fake_ffmpeg_cut(src, start, end, dest, reverse=False, flash=False):
        ffmpeg_calls.append((src, start, end, dest, reverse, flash))
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        Path(dest).write_text("segment", encoding="utf-8")

    monkeypatch.setattr(autocut, "ffmpeg_cut", fake_ffmpeg_cut)

    run_calls = []

    def fake_run(cmd, stdout=None, stderr=None):
        run_calls.append(list(cmd))
        if cmd and cmd[0] == "ffmpeg" and "concat" in cmd:
            out_video.write_text("video", encoding="utf-8")
        return types.SimpleNamespace(returncode=0)

    monkeypatch.setattr(autocut.subprocess, "run", fake_run)

    autocut.main()

    assert ffmpeg_calls, "Expected ffmpeg_cut to be invoked at least once"

    list_path = out_dir / "list.txt"
    assert list_path.exists(), "Expected concat list file to be created"
    assert "file" in list_path.read_text(encoding="utf-8")

    assert run_calls, "Expected subprocess.run to be invoked"
    assert out_video.exists(), "Expected output video placeholder to be created"
