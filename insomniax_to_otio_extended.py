"""
insomniax_to_otio_extended.py
Converts insomniax.json cue sheet into a rich OpenTimelineIO timeline.

Adds:
  • main video track from keyframes
  • audio track for the main soundtrack
  • beat markers from audio analysis
  • FX / jump-cut annotations as markers
"""

import json
from pathlib import Path

import librosa
import opentimelineio as otio

CUE_PATH = Path("insomniax.json")
AUDIO_PATH = Path("soundtrack_mix.wav")
OUT_PATH = Path("insomniax_timeline_extended.otio")

FPS = 24
SEGMENTS_DIR = Path("segments_v3")


def main() -> None:
    # Load cue sheet
    data = json.loads(CUE_PATH.read_text())

    # Analyze audio beats
    y, sr = librosa.load(AUDIO_PATH, sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    print(f"Detected tempo: {tempo:.2f} BPM, {len(beat_times)} beats.")

    # Create timeline + tracks
    timeline = otio.schema.Timeline("Insomniax Extended Timeline")
    video_track = otio.schema.Track(name="Video Track", kind=otio.schema.TrackKind.Video)
    audio_track = otio.schema.Track(name="Audio Track", kind=otio.schema.TrackKind.Audio)

    current_time = 0.0

    # Build video clips from keyframes
    for i, kf in enumerate(data.get("keyframes", [])):
        start = current_time
        end = start + 3.0
        current_time = end

        clip_path = SEGMENTS_DIR / f"scene_{i:02d}.mp4"
        media_ref = otio.schema.ExternalReference(
            target_url=f"file://{clip_path.resolve()}",
            available_range=otio.opentime.TimeRange(
                otio.opentime.RationalTime(0, FPS),
                otio.opentime.RationalTime((end - start) * FPS, FPS),
            ),
        )

        clip = otio.schema.Clip(
            name=f"Scene {i+1}",
            media_reference=media_ref,
            source_range=otio.opentime.TimeRange(
                otio.opentime.RationalTime(start * FPS, FPS),
                otio.opentime.RationalTime((end - start) * FPS, FPS),
            ),
        )

        # Metadata from cue sheet
        clip.metadata["scene_text"] = kf.get("scene", "")
        clip.metadata["voiceover"] = kf.get("voiceover", "")
        clip.metadata["fx"] = kf.get("fx", "")
        clip.metadata["edit_pattern"] = kf.get("edit_pattern", "")

        # FX markers
        ep = kf.get("edit_pattern", "").lower()
        if "jumpcut" in ep:
            clip.markers.append(
                otio.schema.Marker(
                    name="Jumpcut zone",
                    color="RED",
                    marked_range=otio.opentime.TimeRange(
                        otio.opentime.RationalTime(start * FPS, FPS),
                        otio.opentime.RationalTime(6, FPS),
                    ),
                )
            )
        if "black" in ep:
            clip.markers.append(
                otio.schema.Marker(
                    name="Black flash",
                    color="BLUE",
                    marked_range=otio.opentime.TimeRange(
                        otio.opentime.RationalTime((start + 1) * FPS, FPS),
                        otio.opentime.RationalTime(3, FPS),
                    ),
                )
            )

        video_track.append(clip)

    timeline.tracks.append(video_track)

    # Audio track
    audio_ref = otio.schema.ExternalReference(
        target_url=f"file://{AUDIO_PATH.resolve()}",
        available_range=otio.opentime.TimeRange(
            otio.opentime.RationalTime(0, FPS),
            otio.opentime.RationalTime(current_time * FPS, FPS),
        ),
    )
    audio_clip = otio.schema.Clip(
        name="Soundtrack Mix",
        media_reference=audio_ref,
        source_range=otio.opentime.TimeRange(
            otio.opentime.RationalTime(0, FPS),
            otio.opentime.RationalTime(current_time * FPS, FPS),
        ),
    )
    audio_track.append(audio_clip)
    timeline.tracks.append(audio_track)

    # Global beat markers
    for bt in beat_times:
        if bt > current_time:
            break
        marker = otio.schema.Marker(
            name="Beat",
            color="YELLOW",
            marked_range=otio.opentime.TimeRange(
                otio.opentime.RationalTime(bt * FPS, FPS),
                otio.opentime.RationalTime(1, FPS),
            ),
        )
        timeline.markers.append(marker)

    # Write OTIO file
    otio.adapters.write_to_file(timeline, OUT_PATH)
    print(f"Exported extended OTIO timeline → {OUT_PATH}")


if __name__ == "__main__":
    main()
