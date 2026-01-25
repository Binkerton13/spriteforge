# SpriteForge  
### AI‑Driven 2D Animation & Sprite Generation Pipeline  
**HY‑Motion → Frames → ComfyUI → Sprites**

SpriteForge is a modular, production‑ready pipeline for generating game‑ready 2D sprites using AI‑driven motion generation and image synthesis.  
It replaces traditional 3D rigging workflows with a clean, modern stack built around:

- **HY‑Motion** for motion generation  
- **ComfyUI** for image generation  
- **Custom nodes** for identity locking, temporal consistency, and background removal  
- **A unified SpriteForge GUI** for orchestration  

---

## Features

### Animation & Motion
- HY‑Motion 1.0 integration  
- Motion presets (walk, run, stealth, interact, etc.)  
- Frame extraction and management  
- Optional frame interpolation for smoother motion  

### Image & Sprite Generation
- ComfyUI baked into the container  
- AnimateDiff‑Evolved for temporal consistency  
- IP‑Adapter Plus for character identity locking  
- ControlNet Aux for pose/depth/normal preprocessing  
- Background removal (rembg + essentials)  
- Sprite sheet assembly (coming soon)  

### Unified GUI (Port 5000)
- Animation generation  
- Frame preview  
- Sprite generation  
- Model management (checkpoints, LoRAs, IP‑Adapters, VAEs)  
- Settings & logs  

### Developer‑Friendly
- Clean Dockerfile  
- Idempotent installers  
- Persistent workspace  
- Modular folder structure  
- Easy to extend  

---

## Architecture Overview

HY‑Motion → Frames → ComfyUI → SpriteForge GUI → SpritesHY‑Motion → Frames → ComfyUI → SpriteForge GUI → Sprites

### Services & Ports
| Service | Port | Description |
|--------|------|-------------|
| ComfyUI | 8188 | Image generation engine |
| File Browser | 8080 | Workspace file explorer |
| SpriteForge GUI | 5000 | Unified control panel |
| Frontend Dev (optional) | 3000 | React/Vue dev server |

---

## Folder Structure

/workspace
/pipeline
start.sh
install_dependencies.sh
supervisord.conf
/gui
app.py
/routes
/templates
/static
/services
/models
/scripts
install_custom_nodes.sh
/env_patches
sitecustomize.py

/custom_nodes
/models
/checkpoints
/loras
/vae
/controlnet
/unet

/animations
/sprites
/logs

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/<yourname>/SpriteForge.git
cd SpriteForge

### 2. Build the container

docker build -t spriteforge .

### 3. Run the container

docker run --gpus all -p 8188:8188 -p 8080:8080 -p 5000:5000 -v ./workspace:/workspace spriteforge

Usage
SpriteForge GUI (recommended)
Open your browser : http://localhost:5000

From here you can:

Generate animations

Extract frames

Generate sprites

Manage models

View logs

ComfyUI : http://localhost:8188

File Browser : http://localhost:8080

Models
SpriteForge expects models in:

/workspace/models/checkpoints
/workspace/models/loras
/workspace/models/vae
/workspace/models/controlnet
/workspace/models/unet

Recommended Models
AnimateDiff: v3_sd15_mm.ckpt

IP‑Adapter: ip-adapter-faceid-plusv2_sd15.bin

ControlNet: openpose, depth, normalbae, canny

Checkpoints: SDXL‑Turbo, SDXL‑Lightning, SDXL 1.0

Development
GUI Backend
Located in : /workspace/pipeline/gui/app.py

Runs automatically via supervisord.

Custom Nodes
Installed via: /workspace/pipeline/scripts/install_custom_nodes.sh

HY‑Motion
Located in: /workspace/hy-motion

Roadmap
Sprite sheet assembler

Batch animation presets

Character identity library

Style presets

Web‑based model downloader

Full React/Vue frontend

License
MIT License (or your preferred license)

Contributing
Pull requests are welcome.
Please open an issue first to discuss major changes.

Credits
HY‑Motion by Tencent Hunyuan

ComfyUI by comfyanonymous

Custom nodes by their respective authors

SpriteForge architecture by Morgen

---