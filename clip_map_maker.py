"""
clip_map_maker.py
Context-aware generator for clip_map.json.

Scans:
  • insomniax.json  → extracts keywords from scene descriptions
  • footage/ folder → matches video files containing those keywords

Result:
  A minimal, relevant clip_map.json for Insomniax Agent.
"""

import json
import re
from pathlib import Path

# ────────────────────────────────────────────────
VIDEO_EXTS = {".mp4", ".mov", ".mkv"}
CUE_SHEET = Path("insomniax.json")
FOOTAGE_DIR = Path("footage")
OUT_FILE = Path("clip_map.json")

# ────────────────────────────────────────────────
def extract_scene_keywords(cue_path: Path) -> set[str]:
    """Pull words from 'scene' fields in insomniax.json."""
    if not cue_path.exists():
        print(f"⚠️ Cue sheet not found: {cue_path}")
        return set()

    data = json.loads(cue_path.read_text())
    text = " ".join(kf.get("scene", "") for kf in data.get("keyframes", []))
    # lowercase, remove punctuation, split
    words = re.findall(r"[a-zA-Z]+", text.lower())
    # filter: drop short / common words
    blacklist = {
        "the", "and", "of", "in", "to", "at", "on", "with", "for",
        "a", "an", "his", "her", "their", "he", "she", "it", "they"
    }
    return {w for w in words if len(w) > 2 and w not in blacklist}


def scan_footage(folder: Path) -> dict[str, Path]:
    """Return a mapping of lowercase token -> video path."""
    clip_map = {}
    if not folder.exists():
        print(f"⚠️ Footage folder not found: {folder}")
        return clip_map

    for f in folder.iterdir():
        if f.suffix.lower() not in VIDEO_EXTS:
            continue
        tokens = re.split(r"[_\-\s]+", f.stem.lower())
        for t in tokens:
            if len(t) > 2 and not t.isdigit():
                clip_map[t] = f
    return clip_map


def make_clip_map():
    """Generate the clip_map.json based on cue and footage matches."""
    scene_words = extract_scene_keywords(CUE_SHEET)
    print(f"🧠 Extracted {len(scene_words)} scene keywords from cue sheet")

    footage_tokens = scan_footage(FOOTAGE_DIR)
    print(f"🎞️  Found {len(footage_tokens)} candidate video tokens")

    final_map = {}
    for word in scene_words:
        matches = [v for k, v in footage_tokens.items() if word in k]
        if matches:
            final_map[word] = str(matches[0])

    # fallback
    if "default" not in final_map and footage_tokens:
        first = next(iter(footage_tokens.values()))
        final_map["default"] = str(first)

    OUT_FILE.write_text(json.dumps(final_map, indent=2))
    print(f"✅ Generated {OUT_FILE} with {len(final_map)} entries.")


if __name__ == "__main__":
    make_clip_map()