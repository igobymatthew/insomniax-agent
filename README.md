
* * *
    
    
    # 🎬 Insomniax Agent
    
    **Insomniax Agent** is a local, LM Studio--driven AI workflow for automated video cue-sheet editing and synchronization.  
    It generates beat-synced experimental cuts with FFmpeg, manages versioned cue-sheet data, and round-trips timelines through the [OpenTimelineIO](https://opentimeline.io/) standard for use in professional NLEs.
    
    ---
    
    ## ✨ Features
    - **Conversational editing** -- type natural-language instructions; the agent rewrites structured JSON automatically.  
    - **Local and private** -- runs entirely through LM Studio's OpenAI-compatible API.  
    - **Auto-versioning** -- every change to the cue sheet is backed up with timestamped history and reversible restores.  
    - **Beat-synced rendering** -- FFmpeg-based auto-cut script interprets an imported audio track and applies randomized edits.  
    - **Timeline interchange** -- export and import OpenTimelineIO files to or from DaVinci Resolve, Nuke Studio, or any OTIO-compatible editor.  
    - **Full round-trip** -- modify clips in your NLE, export `.otio`, and re-sync updated timings back into your cue sheet.
    
    ---
    
    ## 🧩 Repository Layout

insomniax-agent/

├─ insomniax_agent_v4.py # main conversational agent

├─ insomniax_autocut_v3.py # FFmpeg-based jump-cut renderer

├─ insomniax_to_otio_extended.py # export JSON → OTIO timeline

├─ otio_to_insomniax_sync.py # import OTIO → JSON sync utility

│

├─ insomniax.json  # current cue sheet

├─ soundtrack_mix.wav  # main audio track

├─ clip_map.json # mapping of scenes → source clips

├─ segments_v3/  # generated segments (auto)

├─ versions/ # auto-backup cue sheets

│

├─ requirements.txt

├─ .gitignore

└─ README.md
    
    
    ---
    
    ## 🚀 Quick Start
    
    1. **Clone the repository**
       ```bash
       git clone https://github.com/<yourusername>/insomniax-agent.git
       cd insomniax-agent

2. Install dependencies
    
    
    pip install -r requirements.txt

2.   

3. Ensure LM Studio is running

    - Default local endpoint: http://localhost:1234/v1

    - Load an instruction-tuned model such as Mistral-7B-Instruct or Llama-3-Instruct.

4. Run the agent
    
    
    python insomniax_agent_v4.py

4.   

5. Example conversation
    
    
    You: add black flashes to the hallway scene
    You: render video
    You: sync from Resolve timeline

  

* * *

## ⚙️ Requirements
    
    
    ffmpeg-python
    librosa
    opencv-python
    soundfile
    opentimelineio
    openai

FFmpeg must be available on your system path.

* * *

## 🧠 File Roles

| 

File

 | 

Purpose

 | 
| ---- | ----  |
| 

insomniax_agent_v4.py

 | 

Conversational controller with LM Studio integration, versioning, and OTIO sync

 | 
| 

insomniax_autocut_v3.py

 | 

Generates randomized beat-synced cuts

 | 
| 

insomniax_to_otio_extended.py

 | 

Exports cue-sheet data to OpenTimelineIO for use in NLEs

 | 
| 

otio_to_insomniax_sync.py

 | 

Imports .otio timelines back into the cue sheet for round-trip consistency

 | 

* * *

## 🧩 Example Workflow

1. Draft or edit your cue sheet via chat with the agent.

2. Generate a rendered test cut using insomniax_autocut_v3.py.

3. Export the current sequence to .otio with insomniax_to_otio_extended.py.

4. Open and refine in Resolve or another NLE.

5. Export your timeline back as .otio.

6. Type "sync from Resolve timeline" in the agent to merge updated timings.

* * *

## 🕶️ Notes

- Runs fully offline; no external API keys required.
- Works cross-platform (macOS / Windows / Linux).
- Designed for modular extension--add new tools, audio analyzers, or render styles.
* * *

© 2025 -- Insomniax Agent

An open-source experimental editing framework for AI-assisted video post-production.
    
