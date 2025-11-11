import sys
import types


def install() -> None:
    """Install a lightweight stub for the optional librosa dependency."""
    if "librosa" in sys.modules:
        return

    stub = types.ModuleType("librosa")
    stub.load = lambda *args, **kwargs: ([], 0)
    stub.beat = types.SimpleNamespace(
        beat_track=lambda *args, **kwargs: (0, []),
    )
    stub.frames_to_time = lambda *args, **kwargs: []
    sys.modules["librosa"] = stub
