<div align="center">
  <h1 style="font-family: 'Segoe UI', Arial, sans-serif; font-weight: 700; letter-spacing: 1px;">SpriteForge</h1>
  <h2 style="font-family: 'Fira Sans', 'Segoe UI', Arial, sans-serif; font-weight: 400; color: #4a90e2;">AI‑Driven 2D Animation & Sprite Generation Pipeline</h2>
  <strong style="font-family: 'Fira Mono', monospace; font-size: 1.1em;">HY‑Motion → Frames → ComfyUI → Sprites</strong>
</div>

SpriteForge is a modular, production‑ready pipeline for generating game‑ready 2D sprites using AI‑driven motion generation and image synthesis.

It is designed for:

- Game developers and technical artists automating 2D sprite creation  
- Researchers exploring AI‑based animation workflows  
- Teams seeking a modern, containerized, extensible pipeline for 2D asset production  

SpriteForge replaces traditional 3D rigging workflows with a clean, modern stack built around:

- **HY‑Motion** for motion generation  
- **ComfyUI** for image generation  
- **Custom nodes** for identity locking, temporal consistency, and background removal  
- **A unified SpriteForge GUI** for orchestration  

---

# 🚀 Features

## Animation & Motion
	- HY‑Motion 1.0 integration  
	- Motion presets (walk, run, stealth, interact, etc.)  
	- Frame extraction & management  
	- Optional frame interpolation  

## Image & Sprite Generation
	- ComfyUI baked into the container  
	- AnimateDiff‑Evolved for temporal consistency  
	- IP‑Adapter Plus for identity locking  
	- ControlNet Aux for pose/depth/normal preprocessing  
	- Background removal (rembg + essentials)  
	- Sprite sheet assembly  

## Unified GUI (Port 5000)
	- Motion generation  
	- Frame preview  
	- Sprite generation  
	- Model management (checkpoints, LoRAs, IP‑Adapters, VAEs)  
	- Workflow editor  
	- Settings & logs  

## Developer‑Friendly
	- Clean Dockerfile  
	- Idempotent installers  
	- Persistent workspace  
	- Modular folder structure  
	- Easy to extend  

---

# 🏗 Architecture Overview

HY‑Motion → Frames → ComfyUI → SpriteForge GUI → Sprites

## Services & Ports

	| Service | Port | Description |
	|--------|------|-------------|
	| ComfyUI | 8188 | Image generation engine |
	| File Browser | 8080 | Workspace file explorer |
	| SpriteForge GUI | 5000 | Unified control panel |
	| Frontend Dev (optional) | 3000 | Vue dev server |

---

# 📁 Folder Structure

	/workspace
	/models
	/custom_nodes
	/animations
	/sprites
	/logs

	/pipeline
	/gui
	app.py
	/static
	/templates
	/services
	/routes
	/frontend (Vue source)
	/workflows
	/scripts
	/env_patches
	project.json
	VERSION

	start.sh
	supervisord.conf
	Dockerfile
	requirements.txt

---

# 🛠 Installation

## 1. Clone the repository
	```bash
	git clone https://github.com/<yourname>/SpriteForge.git
	cd SpriteForge

2. Build the container

	docker build -t spriteforge .

3. Run the container

	docker run --gpus all \
	-p 8188:8188 -p 8080:8080 -p 5000:5000 \
	-v ./workspace:/workspace \
	spriteforge

🎨 Usage
SpriteForge GUI (recommended)

	Open: http://localhost:5000

	Use the GUI to:

	Generate animations

	Extract frames

	Generate sprites

	Assemble sprite sheets

	Manage models

	Inspect workflows

	View logs

ComfyUI

	http://localhost:8188

File Browser

	http://localhost:8080

📦 Models
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

🧩 Development
	GUI Backend
		/workspace/pipeline/gui/app.py  
		Runs automatically via supervisord.

		Custom Nodes
		Installed via:
		/workspace/pipeline/scripts/install_custom_nodes.sh

		HY‑Motion
		Located at:
		/workspace/hy-motion

🗺 Roadmap
	Sprite sheet assembler (enhanced)

	Batch animation presets

	Character identity library

	Style presets

	Web‑based model downloader

	Full Vue frontend expansion

🤝 Contributing
	Pull requests welcome.
	Open an issue to discuss major changes.

📝 License
	MIT License (or your preferred license)

🙏 Credits
	HY‑Motion by Tencent Hunyuan

	ComfyUI by comfyanonymous

	Custom nodes by their respective authors

	SpriteForge architecture by Morgen