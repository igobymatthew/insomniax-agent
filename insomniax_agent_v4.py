"""
insomniax_agent_v4.py
Local conversational editor + timeline synchronizer for Insomniax.

Features:
  • automatic versioning
  • restoration of backups
  • OTIO re-import sync from NLE timelines
  • integration with LM Studio's OpenAI-compatible API
"""

import json
import subprocess
import pathlib
import datetime
import shutil

import openai
import opentimelineio as otio

# ── CONFIG ────────────────────────────────────────────────

# LM Studio endpoint (OpenAI-compatible)
openai.api_key = "not-needed"
openai.api_base = "http://localhost:1234/v1"

CUE_PATH = pathlib.Path("insomniax.json")
VERSIONS_DIR = pathlib.Path("versions")
VERSIONS_DIR.mkdir(exist_ok=True)

FPS = 24
DEFAULT_OTIO = pathlib.Path("insomniax_timeline_extended.otio")


# ── TOOL LOGIC ────────────────────────────────────────────

def backup_cue_sheet() -> str:
    """Copy the current cue sheet into versions/ with timestamp."""
    if not CUE_PATH.exists():
        return "No cue sheet found to back up."
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = VERSIONS_DIR / f"insomniax_{ts}.json"
    shutil.copy2(CUE_PATH, backup)
    return str(backup)


def update_cue_sheet(scene_keyword: str, field: str, new_value: str) -> str:
    """
    Find keyframes matching the scene keyword and modify a chosen field.

    scene_keyword: substring to search for in the 'scene' text
    field:         key in the keyframe dict to overwrite
    new_value:     new value as string (you can store JSON-encoded structures)
    """
    backup = backup_cue_sheet()
    if not CUE_PATH.exists():
        return f"Backed up to {backup}, but {CUE_PATH} does not exist."

    data = json.loads(CUE_PATH.read_text())
    edits = 0
    for kf in data.get("keyframes", []):
        if scene_keyword.lower() in kf.get("scene", "").lower():
            kf[field] = new_value
            edits += 1

    CUE_PATH.write_text(json.dumps(data, indent=2))
    return f"Backed up to {backup}. Updated '{field}' in {edits} keyframe(s) containing '{scene_keyword}'."


def render_video() -> str:
    """Execute the auto-cut renderer script."""
    subprocess.run(["python", "insomniax_autocut_v3.py"], check=False)
    return "Rendering launched."


def list_versions() -> str:
    """Return a simple list of available backups in versions/."""
    files = sorted(VERSIONS_DIR.glob("insomniax_*.json"))
    if not files:
        return "No backups found."
    return "\n".join(f.name for f in files)


def restore_version(timestamp: str) -> str:
    """
    Restore a previous cue sheet from a timestamped backup.

    timestamp: e.g. '2025-11-05_21-44-13'
    """
    fname = VERSIONS_DIR / f"insomniax_{timestamp}.json"
    if not fname.exists():
        return f"No version found for {timestamp}"
    backup = backup_cue_sheet()
    shutil.copy2(fname, CUE_PATH)
    return f"Restored {fname.name} → current cue sheet. (Previous live file saved as {backup})"


def sync_from_otio(otio_path: str | None = None) -> str:
    """
    Re-import a Resolve / OTIO timeline and update cue sheet timings.
    If otio_path is None, uses DEFAULT_OTIO.
    """
    path = pathlib.Path(otio_path) if otio_path else DEFAULT_OTIO
    if not path.exists():
        return f"OTIO file not found at {path}"

    backup = backup_cue_sheet()
    timeline = otio.adapters.read_from_file(path)
    if not CUE_PATH.exists():
        return f"Timeline loaded from {path.name}, but cue sheet {CUE_PATH} does not exist."

    data = json.loads(CUE_PATH.read_text())
    keyframes = data.get("keyframes", [])

    for i, clip in enumerate(timeline.find_clips()):
        if i >= len(keyframes):
            break
        kf = keyframes[i]
        src_range = clip.source_range
        dur = src_range.duration.to_seconds()
        start = src_range.start_time.to_seconds()

        # store OTIO-derived timings
        kf["otio_start"] = round(start, 3)
        kf["otio_duration"] = round(dur, 3)
        # refresh scene text from metadata if present
        kf["scene"] = clip.metadata.get("scene_text", kf.get("scene", ""))

        markers = [
            {
                "name": m.name,
                "color": m.color,
                "start_sec": round(m.marked_range.start_time.to_seconds(), 3)
            }
            for m in clip.markers
        ]
        if markers:
            kf["otio_markers"] = markers

    CUE_PATH.write_text(json.dumps(data, indent=2))
    return f"Synced {len(keyframes)} scenes from {path.name}. Backup saved as {backup}"


# ── FUNCTIONS SCHEMA FOR LLM ─────────────────────────────

FUNCTIONS = [
    {
        "name": "update_cue_sheet",
        "description": "Modify fields inside the Insomniax cue sheet (auto-backup included).",
        "parameters": {
            "type": "object",
            "properties": {
                "scene_keyword": {"type": "string"},
                "field": {"type": "string"},
                "new_value": {"type": "string"}
            },
            "required": ["scene_keyword", "field", "new_value"]
        }
    },
    {
        "name": "render_video",
        "description": "Execute the auto-cut renderer after edits are saved.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "list_versions",
        "description": "List all available versioned backups of the cue sheet.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "restore_version",
        "description": "Restore a previous cue sheet from a timestamped backup (YYYY-MM-DD_HH-MM-SS).",
        "parameters": {
            "type": "object",
            "properties": {"timestamp": {"type": "string"}},
            "required": ["timestamp"]
        }
    },
    {
        "name": "sync_from_otio",
        "description": "Re-import a Resolve/OpenTimelineIO timeline and update cue sheet timings.",
        "parameters": {
            "type": "object",
            "properties": {"otio_path": {"type": "string"}},
            "required": []
        }
    }
]


# ── AGENT LOOP ───────────────────────────────────────────


def main() -> None:
    print("Insomniax Agent v4 connected to LM Studio.\nType 'exit' to quit.\n")

    history: list[dict] = []

    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break

        if user.lower() in ("exit", "quit"):
            break

        history.append({"role": "user", "content": user})
        resp = openai.ChatCompletion.create(
            model="mistral-7b-instruct",  # adjust to whatever model LM Studio serves
            messages=history,
            functions=FUNCTIONS
        )
        msg = resp["choices"][0]["message"]

        if msg.get("function_call"):
            fn_name = msg["function_call"]["name"]
            args_raw = msg["function_call"].get("arguments") or "{}"
            try:
                args = json.loads(args_raw)
            except json.JSONDecodeError:
                args = {}
            print(f"→ calling {fn_name}({args})")
            try:
                func = globals()[fn_name]
                result = func(**args)
            except Exception as e:  # noqa: BLE001
                result = f"Error executing {fn_name}: {e}"

            history.append(msg)
            history.append({"role": "function", "name": fn_name, "content": result})
            print(f"✔ {result}\n")
        else:
            reply = msg.get("content", "") or ""
            print(f"{reply}\n")
            history.append(msg)


if __name__ == "__main__":
    main()
