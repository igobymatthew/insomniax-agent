"""
otio_to_insomniax_sync.py
Reads an OpenTimelineIO file and updates insomniax.json with new timing data.

Usage:
    python otio_to_insomniax_sync.py insomniax_timeline_extended.otio
"""

import sys
import json
from pathlib import Path

import opentimelineio as otio

CUE_PATH = Path("insomniax.json")
FPS = 24


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python otio_to_insomniax_sync.py <timeline.otio>")
        raise SystemExit(1)

    otio_file = Path(sys.argv[1])
    if not otio_file.exists():
        print(f"OTIO file not found: {otio_file}")
        raise SystemExit(1)

    timeline = otio.adapters.read_from_file(otio_file)
    data = json.loads(CUE_PATH.read_text())
    keyframes = data.get("keyframes", [])

    for i, clip in enumerate(timeline.find_clips()):
        if i >= len(keyframes):
            break
        kf = keyframes[i]
        src_range = clip.source_range
        duration = src_range.duration.to_seconds()
        start = src_range.start_time.to_seconds()

        kf["otio_start"] = round(start, 3)
        kf["otio_duration"] = round(duration, 3)
        kf["scene"] = clip.metadata.get("scene_text", kf.get("scene", ""))

        markers = []
        for m in clip.markers:
            markers.append(
                {
                    "name": m.name,
                    "color": m.color,
                    "start_sec": round(
                        m.marked_range.start_time.to_seconds(), 3
                    ),
                }
            )
        if markers:
            kf["otio_markers"] = markers

        print(
            f"Synced Scene {i+1}: "
            f"start={start:.2f}s dur={duration:.2f}s markers={len(markers)}"
        )

    CUE_PATH.write_text(json.dumps(data, indent=2))
    print(
        f"\nCue sheet updated from {otio_file.name} → {CUE_PATH.name}"
    )


if __name__ == "__main__":
    main()
