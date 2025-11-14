import json
import sys
from pathlib import Path

import pytest

# Ensure repository root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import insomniax_agent_v4 as agent


@pytest.fixture()
def fixed_timestamp(monkeypatch):
    class _FixedNow:
        def strftime(self, fmt: str) -> str:  # noqa: ARG002 - signature required for compatibility
            return "2025-01-02_03-04-05"

    class _FixedDatetime:
        @staticmethod
        def now():
            return _FixedNow()

    monkeypatch.setattr(agent.datetime, "datetime", _FixedDatetime)


def test_update_cue_sheet_creates_version_backup(tmp_path, monkeypatch, fixed_timestamp):
    cue_path = tmp_path / "insomniax.json"
    original_data = {
        "keyframes": [
            {"scene": "First scene", "note": "draft"},
            {"scene": "Another scene", "note": "unchanged"},
        ]
    }
    cue_path.write_text(json.dumps(original_data), encoding="utf-8")

    versions_dir = tmp_path / "versions"
    versions_dir.mkdir()

    monkeypatch.setattr(agent, "CUE_PATH", cue_path)
    monkeypatch.setattr(agent, "VERSIONS_DIR", versions_dir)

    result = agent.update_cue_sheet("First", "note", "final")

    backup_path = versions_dir / "insomniax_2025-01-02_03-04-05.json"
    assert backup_path.exists(), "Expected a timestamped backup to be created"

    backup_contents = json.loads(backup_path.read_text(encoding="utf-8"))
    assert backup_contents == original_data, "Backup should preserve the original cue sheet"

    updated = json.loads(cue_path.read_text(encoding="utf-8"))
    assert updated["keyframes"][0]["note"] == "final"
    assert updated["keyframes"][1]["note"] == "unchanged"

    expected_fragment = "Updated 'note' in 1 keyframe(s) containing 'First'."
    assert expected_fragment in result
