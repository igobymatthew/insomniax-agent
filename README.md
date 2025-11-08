# 🎬 Insomniax Agent

**Insomniax Agent** is a local, LM Studio–driven AI workflow for automated video cue-sheet editing and synchronization.  
It generates beat-synced experimental cuts with FFmpeg, manages versioned cue-sheet data, and round-trips timelines through the [OpenTimelineIO](https://opentimeline.io/) standard for use in professional NLEs.

---

## ✨ Features
- **Conversational editing** — type natural-language instructions; the agent rewrites structured JSON automatically.  
- **Local and private** — runs entirely through LM Studio’s OpenAI-compatible API.  
- **Auto-versioning** — every change to the cue sheet is backed up with timestamped history and reversible restores.  
- **Beat-synced rendering** — FFmpeg-based auto-cut script interprets an imported audio track and applies randomized edits.  
- **Timeline interchange** — export and import OpenTimelineIO files to or from DaVinci Resolve, Nuke Studio, or any OTIO-compatible editor.  
- **Full round-trip** — modify clips in your NLE, export `.otio`, and re-sync updated timings back into your cue sheet.

---

## 🧩 Repository Layout

```
insomniax-agent/
├─ insomniax_agent_v4.py            # main conversational agent
├─ insomniax_autocut_v3.py          # FFmpeg-based jump-cut renderer
├─ insomniax_to_otio_extended.py    # export JSON → OTIO timeline
├─ otio_to_insomniax_sync.py        # import OTIO → JSON sync utility
│
├─ insomniax.json                   # current cue sheet
├─ soundtrack_mix.wav               # main audio track
├─ clip_map.json                    # mapping of scenes → source clips
├─ segments_v3/                     # generated segments (auto)
├─ versions/                        # auto-backup cue sheets
│
├─ requirements.txt
├─ .gitignore
├─ .github/workflows/test.yml
└─ README.md
```

---

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/<yourusername>/insomniax-agent.git
   cd insomniax-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure LM Studio is running**
   - Default local endpoint: `http://localhost:1234/v1`
   - Load any instruction-tuned model (e.g., Mistral-7B-Instruct, Llama-3-Instruct)

4. **Run the agent**
   ```bash
   python insomniax_agent_v4.py
   ```

5. **Interact naturally**
   ```
   You: add black flashes to the hallway scene
   You: render video
   You: sync from Resolve timeline
   ```

---

## ⚙️ Requirements

```
ffmpeg-python
librosa
opencv-python
soundfile
opentimelineio
openai
tqdm
pathlib
```

*Ensure FFmpeg is installed and accessible from your system path.*

---

## 🧠 File Roles

| File | Purpose |
|------|----------|
| `insomniax_agent_v4.py` | Conversational controller with LM Studio integration, versioning, and OTIO sync |
| `insomniax_autocut_v3.py` | Generates randomized beat-synced cuts |
| `insomniax_to_otio_extended.py` | Exports cue-sheet data to OpenTimelineIO |
| `otio_to_insomniax_sync.py` | Imports OTIO timelines back into the cue sheet |

---

## 🧩 Example Workflow

1. Draft or modify your cue sheet with the agent.  
2. Render a test cut using `insomniax_autocut_v3.py`.  
3. Export the sequence to `.otio` using `insomniax_to_otio_extended.py`.  
4. Open and adjust in Resolve or any NLE.  
5. Export your timeline as `.otio`.  
6. Tell the agent:  
   ```
   You: sync from Resolve timeline
   ```
   The cue sheet updates automatically.

---

## 🧱 License

MIT License — © 2025 Matthew Ballard  
*(See `LICENSE` file in repository root.)*

---

## 🧩 Continuous Integration

GitHub Actions workflow: `.github/workflows/test.yml`

Runs:
- Python install & import tests  
- Syntax validation  
- FFmpeg availability check  

---

## 🕶️ Notes
- Runs fully offline using LM Studio’s local OpenAI-compatible API.  
- Cross-platform (macOS / Windows / Linux).  
- Modular design — extend with new tools, analyzers, or visual effects logic.

---

© 2025 *Insomniax Agent*  
An open-source experimental editing framework for AI-assisted video post-production.
