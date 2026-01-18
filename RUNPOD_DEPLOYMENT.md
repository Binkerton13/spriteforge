# RunPod Deployment Guide

## Image Location
**GHCR Image**: `ghcr.io/binkerton13/3d-ai-workstation:latest`

## Quick Deploy on RunPod

### Step 1: Make Image Public on GitHub
1. Go to https://github.com/Binkerton13?tab=packages
2. Find `3d-ai-workstation` package
3. Click **Package settings**
4. Scroll to **Danger Zone** → **Change visibility**
5. Set to **Public** (allows RunPod to pull without authentication)

### Step 2: Create RunPod Template

1. **Login to RunPod**: https://www.runpod.io/console/pods
2. **Navigate to Templates**: Click "Templates" in left sidebar
3. **Create New Template**: Click "+ New Template"

**Template Settings**:
```
Template Name: 3D AI Workstation
Container Image: ghcr.io/binkerton13/3d-ai-workstation:latest
Container Disk: 50 GB (minimum, increase if storing large models)

Expose HTTP Ports:
  - 8188 (ComfyUI)
  - 8080 (File Browser)
  - 7860 (Pipeline GUI)

Expose TCP Ports: (leave empty)

Environment Variables:
  PORT=8188
  FILE_BROWSER_PORT=8080
  PIPELINE_GUI_PORT=7860
  MODEL_DOWNLOAD_ON_START=0
  MODEL_URLS=

Docker Command: (leave empty - uses CMD from Dockerfile)

Volume Mount Path: /workspace
```

### Step 3: Deploy Pod

1. **Select GPU**: Click "Deploy" on your template
2. **Choose GPU**: RTX 4090 recommended (24GB VRAM for large models)
3. **Select Storage**: 
   - Container Disk: 50GB minimum
   - Volume: 100GB+ recommended (for models/outputs)
4. **Deploy**: Click "Deploy On-Demand" or "Deploy Spot"

### Step 4: Access Services

Once pod is running, RunPod will provide URLs:

**Connect Button** → Shows three ports:
- **8188** → ComfyUI: `https://<pod-id>-8188.proxy.runpod.net`
- **8080** → File Browser: `https://<pod-id>-8080.proxy.runpod.net`
- **7860** → Pipeline GUI: `https://<pod-id>-7860.proxy.runpod.net`

## Using the 3D Pipeline

### Initial Setup (First Time)

1. **Access Pipeline GUI**: Open port 7860 URL
2. **Create Project**: 
   - Click "New Project" 
   - Enter project name (e.g., "MyCharacter")
   - Project structure created automatically

### Upload Assets

**Via Pipeline GUI (Port 7860)**:
- Drag and drop FBX/OBJ mesh files
- Upload UDIM texture tiles (1001, 1002, etc.)
- Add reference images

**Via File Browser (Port 8080)**:
- Upload to `/workspace/<project>/0_input/meshes/`
- Upload UDIM tiles to appropriate folders
- Direct file management

### Configure Pipeline

**In Pipeline GUI**:
- **Texture Settings**: PBR material types (Albedo, Normal, Roughness, Metallic, AO)
- **Rig Settings**: Skeleton type, joint count
- **Animation Settings**: Motion type, duration, HY-Motion prompts

### Run Pipeline

1. **Start Execution**: Click "Start Pipeline" button
2. **Monitor Progress**: Watch logs in GUI
3. **Check ComfyUI**: Switch to port 8188 to see AI texture generation
4. **Download Results**: Use File Browser (8080) to get outputs from `/workspace/<project>/4_export/`

## Environment Variables

### Port Configuration
```bash
PORT=8188                  # ComfyUI port
FILE_BROWSER_PORT=8080     # File browser port  
PIPELINE_GUI_PORT=7860     # Pipeline GUI port
```

### Model Management
```bash
MODEL_DOWNLOAD_ON_START=1  # Auto-download models on startup
MODEL_URLS=https://example.com/model1.safetensors,https://example.com/model2.safetensors
```

## Storage Structure

```
/workspace/
├── pipeline/              # Pipeline code (copied from /opt/pipeline)
├── config/                # Configuration files
├── <project_name>/        # Your project (e.g., "Exhibition")
│   ├── 0_input/
│   │   ├── meshes/       # FBX/OBJ files
│   │   ├── references/   # Reference images
│   │   └── uv_layouts/   # UV maps
│   ├── 1_textures/       # Generated PBR textures
│   ├── 2_rig/            # Rigged characters
│   ├── 3_animation/      # Animated sequences
│   └── 4_export/         # Final outputs (FBX, GLTF, USD)
└── models/               # AI models
    ├── checkpoints/
    ├── loras/
    ├── 3d/
    └── textures/
```

## Troubleshooting

### Services Not Starting
- **Check Logs**: Use RunPod terminal to view `supervisord.log`
- **Port Issues**: Ensure all 3 ports (8188, 8080, 7860) are exposed in template

### Out of Memory
- **Increase GPU**: Switch to higher VRAM GPU (A40, A100)
- **Reduce Batch Size**: Adjust settings in Pipeline GUI

### Pipeline GUI 404 Error
- **Wait for Startup**: Services take 30-60 seconds to initialize
- **Check Port**: Ensure accessing port 7860, not 8188 or 8080

### File Upload Fails
- **Size Limit**: Large files (>5GB) may timeout, use File Browser instead
- **Permissions**: Check `/workspace` volume is mounted and writable

## Cost Optimization

### Spot Instances
- **70% cheaper** than on-demand
- Good for batch processing
- May be interrupted (save work frequently)

### Storage
- Use **Network Volume** for persistent storage across pods
- Minimize **Container Disk** size (only OS/apps, not data)

### Auto-Stop
- Set pod to auto-stop after idle time
- Download results regularly

## Next Steps

1. ✅ **Image Published**: `ghcr.io/binkerton13/3d-ai-workstation:latest`
2. ⏳ **Create Template**: Follow Step 2 above
3. ⏳ **Deploy Pod**: Follow Step 3 above
4. ⏳ **Test Pipeline**: Upload test mesh and run full workflow
5. ⏳ **Monitor Performance**: Check GPU utilization, memory usage

---

**Support**: Check `/workspace/pipeline/README.md` for pipeline documentation
**GUI Features**: See `/workspace/pipeline/WEB_GUI_SUMMARY.md`
**Quick Start**: See `/workspace/pipeline/QUICKSTART_GUI.md`
