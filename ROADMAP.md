# 🗺️ Insomniax Agent — Project Roadmap

This document outlines the short-term goals, architecture, and long-term evolution of the **Insomniax Agent** system and its key submodule, **Clip Map Maker**.

---

## 🎯 Core Vision

**Insomniax Agent** is a local, modular post-production automation framework.  
It combines conversational control, structured cue-sheet logic, and audio/video synchronization to bridge human creativity with machine precision — all running offline via LM Studio.

---

## 🧩 Phase 1 — Current System (v4.0)

**Status:** ✅ Stable and Functional

**Core Modules**
| Module | Purpose |
|---------|----------|
| `insomniax_agent_v4.py` | Conversational control, JSON editing, versioning, OTIO sync |
| `insomniax_autocut_v3.py` | Beat-synced automatic video cut generator |
| `insomniax_to_otio_extended.py` | Exports structured OTIO timelines for NLEs |
| `otio_to_insomniax_sync.py` | Imports `.otio` timelines and updates cue sheets |
| `clip_map_maker.py` | Generates contextual clip mapping from footage and cue sheets |

**Capabilities**
- Full LM Studio integration via OpenAI-compatible endpoint.  
- Local operation (no cloud dependencies).  
- Automatic versioning and rollback of cue sheets.  
- FFmpeg-based procedural auto-editing pipeline.  
- Round-trip timeline synchronization via OTIO.  
- Semantic cue mapping between text and footage.

---

## 🧠 Phase 2 — Planned Enhancements (v5.0)

**Focus:** Automation, Context Awareness, and UX Refinement

| Feature | Description | Status |
|----------|--------------|--------|
| **Interactive Editing** | Extend conversational control to direct clip_map and auto-cut settings dynamically. | ⏳ Planned |
| **Audio-Driven Cut Logic** | Analyze frequency bands or dynamic range to determine visual cut density. | ⏳ Planned |
| **Scene Dependency Awareness** | Cross-link similar scenes (e.g. “mirror reflection” and “bathroom”) for consistent tone. | ⏳ Planned |
| **Adaptive Rendering** | Adjust render parameters (contrast, grade, effect layers) based on cue metadata. | ⏳ Planned |
| **Timeline Summarizer** | Command: “summarize current timeline” → prints scene sequence, durations, and key motifs. | ⏳ Planned |
| **Incremental Sync** | OTIO sync only updates changed keyframes for faster iteration. | ⏳ Planned |

---

## 🧩 Clip Map Maker Submodule (Integrated)

**File:** `clip_map_maker.py`  
**Purpose:** Automatically link words from scene descriptions to relevant source footage.

### Current Capabilities (v1.0)
- Scans `insomniax.json` → extracts keywords from `"scene"` fields.  
- Scans `footage/` → matches filenames containing those words.  
- Generates a clean `clip_map.json` with minimal user effort.  
- Adds a fallback `"default"` entry automatically.  
- Prints summary of matches and keyword coverage.

### Planned Extensions (v1.5+)
| Feature | Description |
|----------|-------------|
| **Interactive CLI Review** | Prompt user to approve or skip each mapping. |
| **Preview Support** | Play a few seconds of each clip before confirming. |
| **Semantic Matching** | Use small language model embeddings for fuzzy keyword matching. |
| **Coverage Report** | Print percentage of cue-sheet keywords successfully mapped. |
| **Auto-Rebuild Trigger** | Detect changes in footage or cue sheet → rebuild automatically. |

---

## 🧮 Phase 3 — AI-Assisted Editing (v6.0)

**Goal:** Integrate machine reasoning for context-aware editing and cue refinement.

| Addition | Description |
|-----------|-------------|
| **LLM “Cut Logic” Evaluation** | Let the agent reason about pacing, rhythm, or tone consistency between scenes. |
| **Automatic FX Assignment** | Suggest appropriate filters or overlays based on lighting and mood cues. |
| **Generative Fallbacks** | Use diffusion-generated frames for missing or damaged clips. |
| **Metadata Harmonization** | Maintain consistent color palettes and aspect ratios across sequences. |

---

## 🧱 Phase 4 — Expanded Ecosystem (v7.0)

| Extension | Function |
|------------|-----------|
| **Web Control Panel (FastAPI + HTMX)** | Local browser dashboard for reviewing cue sheets and renders. |
| **Agent API Mode** | Serve endpoints for remote control or batch processing. |
| **Multi-Project Manager** | Handle multiple Insomniax projects simultaneously with shared media pools. |
| **Integration with DiffusionStudio** | Optional generative feed to supply raw footage for auto-cut pipelines. |

---

## 🧩 Technical Considerations

- **Language:** Python 3.11+  
- **Libraries:** `ffmpeg-python`, `librosa`, `opencv-python`, `soundfile`, `opentimelineio`, `openai`  
- **Storage:** JSON-based configuration, OTIO interchange  
- **Execution:** All scripts run locally; no network dependencies beyond LM Studio endpoint  
- **Platform:** macOS, Windows, Linux  

---

## 🧭 Long-Term Vision (v8.0+)

> “From scene text to full render — one continuous loop.”

- Natural-language → cue sheet → timeline → render → revision → sync  
- Fully self-contained offline AI editing suite  
- Modular architecture for community extensions  
- Optional web layer for visual browsing of clips and cue mappings  

---

## 🪜 Next Actions

- [ ] Add `interactive_review()` mode to `clip_map_maker.py`  
- [ ] Implement “summarize current timeline” in `insomniax_agent_v4.py`  
- [ ] Integrate audio spectrum analysis into auto-cut logic  
- [ ] Add optional semantic match module using `sentence-transformers`  
- [ ] Document project-level configuration (`project.json` template)  
- [ ] Create showcase repo media example with 5 sample clips  

---

## 🧾 Version Table

| Version | Focus | Status |
|----------|--------|---------|
| **v4.0** | Current: functional LM Studio agent + OTIO sync | ✅ |
| **v5.0** | UX + incremental sync improvements | ⏳ Planned |
| **v6.0** | AI-assisted reasoning for editing logic | ⏳ Planned |
| **v7.0** | Web dashboard + multi-project support | ⏳ Planned |
| **v8.0** | End-to-end automation loop | 🧩 Vision |

---

© 2025 *Insomniax Agent*  
*Local AI-Assisted Editing Framework*
