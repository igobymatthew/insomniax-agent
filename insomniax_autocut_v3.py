"""
insomniax_autocut_v3.py
Semi-controlled jump-cut generator for Insomniax.

- Reads a cue sheet (insomniax.json)
- Detects beats from an audio track (soundtrack_mix.wav)
- Auto-chooses the correct source clip for each scene based on clip_map.json
- Performs random keep/jump/reverse/black-flash actions per beat
"""

import json
import os
import random
import subprocess
from pathlib import Path

import librosa

# ---------------- CONFIG ----------------
CUE_SHEET = "insomniax.json"           # cue sheet JSON
CLIP_MAP = "clip_map.json"             # maps scene tags to video paths
AUDIO_TRACK = "soundtrack_mix.wav"     # main soundtrack audio file
OUT_DIR = "segments_v3"
OUT_VIDEO = "insomniax_autocut_v3.mp4"


def ffmpeg_cut(src: str, start: float, end: float, dest: str,
               reverse: bool = False, flash: bool = False) -> None:
    """Cut a segment from src between start and end seconds, apply optional FX."""
    vf = []
    if reverse:
        vf.append("reverse")
    if flash:
        vf.append("fade=out:st=0:d=0.03:alpha=1,fade=in:st=0.03:d=0.03:alpha=1")
    vfopt = ",".join(vf) if vf else "null"
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
        "-i", src,
        "-vf", vfopt,
        "-c:v", "libx264", "-preset", "ultrafast",
        "-crf", "20",
        "-an",
        dest,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def choose_clip(scene_text: str, clip_map: dict) -> str:
    """Choose an appropriate clip based on scene text, with some randomness."""
    if not clip_map:
        raise ValueError("clip_map is empty; populate clip_map.json before rendering")

    scene_text = scene_text.lower()
    for tag, path in clip_map.items():
        if tag.lower() in scene_text:
            return path

    default_entry = next(
        (clip_map[key] for key in clip_map if key.lower() == "default"),
        None,
    )

    # 20% chance of random "wrong" insert for dream-logic variety
    if random.random() < 0.2:
        pool = [
            path
            for key, path in clip_map.items()
            if key.lower() != "default" or default_entry is None
        ]
        if not pool and default_entry is not None:
            pool = [default_entry]
        return random.choice(pool)

    if default_entry is not None:
        return default_entry

    # fallback: first entry
    return next(iter(clip_map.values()))


def main() -> None:
    # Load cue sheet and clip map
    cue = json.loads(Path(CUE_SHEET).read_text())
    clip_map = json.loads(Path(CLIP_MAP).read_text())

    # Analyze beats from audio
    y, sr = librosa.load(AUDIO_TRACK, sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    print(f"BPM: {tempo:.2f}, Beats: {len(beat_times)}")

    os.makedirs(OUT_DIR, exist_ok=True)

    segments: list[str] = []

    # Each keyframe is treated as a 3-second logical block by default
    for i, kf in enumerate(cue.get("keyframes", [])):
        seg_start, seg_end = i * 3.0, i * 3.0 + 3.0
        seg_beats = [b for b in beat_times if seg_start <= b < seg_end]
        if not seg_beats:
            seg_beats = [seg_start, seg_end]

        src = choose_clip(kf.get("scene", ""), clip_map)
        print(f"[{i}] {kf.get('scene', '')[:40]}... → {os.path.basename(src)}")

        for j, bt in enumerate(seg_beats[:-1]):
            act = random.choices(
                ["keep", "jumpcut", "black", "reverse"],
                weights=[3, 4, 1, 2],
            )[0]
            start, end = bt, seg_beats[j + 1]
            name = f"{OUT_DIR}/{i:02d}_{j:03d}_{act}.mp4"

            if end <= start:
                continue

            if act == "jumpcut":
                trim = min(0.15, max(0.05, (end - start) / 4.0))
                start, end = start + trim, end - trim

            ffmpeg_cut(
                src,
                start,
                end,
                name,
                reverse=(act == "reverse"),
                flash=(act == "black"),
            )
            segments.append(name)

    # Concatenate segments
    list_path = Path(OUT_DIR) / "list.txt"
    with list_path.open("w", encoding="utf-8") as f:
        for s in segments:
            f.write(f"file '{os.path.basename(s)}'\n")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-c",
            "copy",
            OUT_VIDEO,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"Rendered auto-cut → {OUT_VIDEO}")


if __name__ == "__main__":
    main()
