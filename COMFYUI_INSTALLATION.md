# ComfyUI Custom Nodes Installation Guide

This guide covers installing the required ComfyUI custom nodes for enhanced sprite generation with AnimateDiff + IP-Adapter + Multi-ControlNet.

## Quick Install (Automated)

### On RunPod/Docker Container:

```bash
cd /opt/ComfyUI/custom_nodes
bash /workspace/runpod-3d-ai-template/install_comfyui_nodes.sh
```

### On Local Machine:

```bash
cd /path/to/ComfyUI/custom_nodes
export COMFYUI_DIR=/path/to/ComfyUI
bash install_comfyui_nodes.sh
```

## Manual Installation

If you prefer to install manually or the automated script fails:

### 1. Navigate to Custom Nodes Directory

```bash
cd /opt/ComfyUI/custom_nodes  # RunPod/Docker
# OR
cd /path/to/ComfyUI/custom_nodes  # Local
```

### 2. Install Each Custom Node

**Note:** These are public repositories - no authentication needed. Just press Enter if prompted for credentials.

#### AnimateDiff-Evolved (Temporal Consistency)

```bash
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
cd ComfyUI-AnimateDiff-Evolved
pip install -r requirements.txt
cd ..
```

**Purpose:** Ensures temporal consistency across animation frames, prevents flickering.

#### IP-Adapter Plus (Character Consistency)

```bash
git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git
cd ComfyUI_IPAdapter_plus
pip install -r requirements.txt
cd ..
```

**Purpose:** Maintains consistent character appearance using reference images.

#### ControlNet Aux (Preprocessors)

```bash
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
cd comfyui_controlnet_aux
pip install -r requirements.txt
cd ..
```

**Purpose:** Generates ControlNet input maps (OpenPose, Depth, Normal, Canny).

#### Advanced ControlNet (Weight Scheduling)

```bash
git clone https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet.git
cd ComfyUI-Advanced-ControlNet
pip install -r requirements.txt
cd ..
```

**Purpose:** Advanced ControlNet weight scheduling and multi-ControlNet support.

#### Rembg (Background Removal)

```bash
git clone https://github.com/mlinmg/ComfyUI-rembg.git
cd ComfyUI-rembg
pip install rembg[gpu]
cd ..
```

**Purpose:** Removes backgrounds for transparent sprites.

#### Frame Interpolation (Optional)

```bash
git clone https://github.com/Fannovel16/ComfyUI-Frame-Interpolation.git
cd ComfyUI-Frame-Interpolation
pip install -r requirements.txt
cd ..
```

**Purpose:** Generates additional frames for smoother animations.

## Required Models

After installing custom nodes, download the required AI models:

### AnimateDiff Models

Download to: `/opt/ComfyUI/models/animatediff_models/`

- **v3_sd15_mm.ckpt** (1.7 GB)
  - Download: https://huggingface.co/guoyww/animatediff/tree/main
  - Purpose: Motion model for temporal consistency

### IP-Adapter Models

Download to: `/opt/ComfyUI/models/ipadapter/`

- **ip-adapter-faceid-plusv2_sd15.bin** (340 MB)
  - Download: https://huggingface.co/h94/IP-Adapter-FaceID/tree/main
  - Purpose: Character consistency from reference images

Download to: `/opt/ComfyUI/models/clip_vision/`

- **CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors** (3.69 GB)
  - Download: https://huggingface.co/h94/IP-Adapter/tree/main/models/image_encoder
  - Purpose: Image encoding for IP-Adapter

### ControlNet Models

Download to: `/opt/ComfyUI/models/controlnet/`

- **control_v11p_sd15_openpose.pth** (1.45 GB)
  - Download: https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main
  - Purpose: Pose preservation

- **control_v11f1p_sd15_depth.pth** (1.45 GB)
  - Download: https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main
  - Purpose: Depth map guidance

- **control_v11p_sd15_normalbae.pth** (1.45 GB)
  - Download: https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main
  - Purpose: Normal map guidance

- **control_v11p_sd15_canny.pth** (1.45 GB)
  - Download: https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main
  - Purpose: Edge detection guidance

### Base Checkpoints

Download to: `/opt/ComfyUI/models/checkpoints/`

Choose based on quality preset:

- **SDXL-Turbo (Fast Prototype)**
  - `sd_xl_turbo_1.0_fp16.safetensors` (6.94 GB)
  - Download: https://huggingface.co/stabilityai/sdxl-turbo/tree/main

- **SDXL-Lightning (Balanced)**
  - `sdxl_lightning_4step.safetensors` (6.94 GB)
  - Download: https://huggingface.co/ByteDance/SDXL-Lightning/tree/main

- **SDXL 1.0 (High/Ultra Quality)**
  - `sd_xl_base_1.0.safetensors` (6.94 GB)
  - Download: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/tree/main

## Verification

### 1. Check Installed Nodes

After restarting ComfyUI, check that all nodes are loaded:

```bash
# In ComfyUI terminal/logs, look for:
# - AnimateDiff nodes loaded
# - IPAdapter nodes loaded
# - ControlNet Aux nodes loaded
# - Advanced ControlNet nodes loaded
# - Rembg nodes loaded
# - Frame Interpolation nodes loaded
```

### 2. Test Workflow

Create a simple test workflow in ComfyUI:

1. Load a checkpoint
2. Add AnimateDiff node
3. Add IP-Adapter node
4. Add ControlNet nodes (OpenPose, Depth)
5. Generate a test image

### 3. Check Models

Verify models are in correct directories:

```bash
ls /opt/ComfyUI/models/animatediff_models/
ls /opt/ComfyUI/models/ipadapter/
ls /opt/ComfyUI/models/controlnet/
ls /opt/ComfyUI/models/checkpoints/
ls /opt/ComfyUI/models/clip_vision/
```

## Troubleshooting

### Authentication Error When Cloning

**Problem:** `fatal: Authentication failed`

**Solution:** These are public repositories - you don't need authentication. If prompted for credentials, just press Enter or Ctrl+C and clone without auth:

```bash
# If it asks for username/password, press Ctrl+C
# Then clone again - it should work without prompting
git clone https://github.com/mlinmg/ComfyUI-rembg.git
```

### Missing Dependencies

**Problem:** `ModuleNotFoundError: No module named 'X'`

**Solution:** Install missing package:

```bash
cd /opt/ComfyUI
python -m pip install <package-name>
```

Common missing packages:
- `opencv-python`
- `einops`
- `kornia`
- `timm`
- `onnxruntime-gpu`

### CUDA/GPU Errors

**Problem:** `CUDA out of memory` or `No CUDA GPUs available`

**Solution:** 
- For VRAM issues: Use lower quality presets (fast/balanced instead of ultra)
- For GPU detection: Check GPU drivers and CUDA installation

### Model Not Found

**Problem:** `Model not found: X`

**Solution:** Download the model to the correct directory (see Required Models section above)

### ComfyUI Won't Start

**Problem:** ComfyUI crashes on startup after installing nodes

**Solution:**
1. Check ComfyUI logs for error messages
2. Try disabling nodes one by one to identify the problematic one
3. Reinstall ComfyUI if needed:

```bash
cd /opt
rm -rf ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
```

## Performance Tips

### VRAM Optimization

For systems with limited VRAM (< 12GB):

1. Use `--lowvram` flag when starting ComfyUI:
   ```bash
   python main.py --lowvram
   ```

2. Use smaller checkpoints:
   - SD 1.5 instead of SDXL (4GB vs 7GB VRAM)

3. Reduce batch size in workflows

4. Use quality presets wisely:
   - Fast Prototype: ~4GB VRAM
   - Balanced: ~6GB VRAM
   - High Quality: ~8GB VRAM
   - Ultra Quality: ~12GB VRAM

### Speed Optimization

1. **Use appropriate quality presets:**
   - Fast Prototype: 2-3 sec/frame
   - Balanced: 5-8 sec/frame
   - High Quality: 15-20 sec/frame
   - Ultra Quality: 30-40 sec/frame

2. **Enable xformers:**
   ```bash
   pip install xformers
   python main.py --use-xformers
   ```

3. **Use TensorRT (NVIDIA GPUs):**
   - Compile models for your GPU
   - 2-3x speedup possible

## Storage Requirements

Total storage needed for complete installation:

- Custom Nodes: ~500 MB
- AnimateDiff Models: ~2 GB
- IP-Adapter Models: ~4 GB
- ControlNet Models: ~6 GB (4 models)
- Base Checkpoint: ~7 GB (SDXL)
- **Total: ~20 GB**

Budget more if using multiple checkpoints or additional models.

## Next Steps

After installation:

1. ✅ Restart ComfyUI server
2. ✅ Verify all nodes are loaded
3. ✅ Download required models
4. ✅ Test with sample workflow
5. ✅ Run sprite generation pipeline on test project

## Support

For issues with specific custom nodes, check their GitHub repositories:

- AnimateDiff: https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved/issues
- IP-Adapter: https://github.com/cubiq/ComfyUI_IPAdapter_plus/issues
- ControlNet Aux: https://github.com/Fannovel16/comfyui_controlnet_aux/issues
- Advanced ControlNet: https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet/issues
- Rembg: https://github.com/mlinmg/ComfyUI-rembg/issues
- Frame Interpolation: https://github.com/Fannovel16/ComfyUI-Frame-Interpolation/issues

For ComfyUI general issues: https://github.com/comfyanonymous/ComfyUI/issues
