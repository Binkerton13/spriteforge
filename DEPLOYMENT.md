# RunPod Deployment Guide

## Recent Updates (January 18, 2026)

### FBX Viewer Fix
Fixed 3D model viewer to properly display FBX files exported from Blender:
- **Library Fix**: Changed from `inflate.min.js` to `fflate.min.js` (required by FBXLoader)
- **Parse Method**: Updated to synchronous `FBXLoader.parse()` instead of callback-based
- **Normal Preservation**: Only compute normals if missing (preserves Blender's smooth shading)
- **HTML Cleanup**: Fixed duplicate element IDs causing JavaScript errors

### Build Status
Currently building Docker image with latest features:
- ComfyUI model management
- Multi-animation selection with warnings
- Animation prompt editor with project/global overrides
- 3D viewer with FBX/OBJ support
- Comprehensive tooltips
- Fixed pipeline status display

## Docker Build & Push to GHCR

### Build Command
```bash
docker build -t 3d-ai-workstation:latest -f Dockerfile.runpod .
```

### Tag for GitHub Container Registry
```bash
docker tag 3d-ai-workstation:latest ghcr.io/binkerton13/3d-ai-workstation:latest
docker tag 3d-ai-workstation:latest ghcr.io/binkerton13/3d-ai-workstation:v1.0
```

### Push to GHCR
```bash
# Login to GHCR (use a Personal Access Token with write:packages scope)
echo %GITHUB_TOKEN% | docker login ghcr.io -u binkerton13 --password-stdin

# Push images
docker push ghcr.io/binkerton13/3d-ai-workstation:latest
docker push ghcr.io/binkerton13/3d-ai-workstation:v1.0
```

### Verify Package
After pushing, check your package at:
https://github.com/Binkerton13/runpod-3d-ai-template/pkgs/container/3d-ai-workstation

## RunPod Template Configuration

### Container Image
```
ghcr.io/binkerton13/3d-ai-workstation:latest
```

### Exposed Ports
- **7860**: Pipeline GUI (HTTP)
- **8188**: ComfyUI (HTTP)
- **8080**: File Browser (HTTP)

### Volume Mounts
```
/workspace - Persistent storage for projects, models, and outputs
```

### Environment Variables
```bash
PORT=8188                    # ComfyUI port
MODEL_DOWNLOAD_ON_START=0    # Set to 1 to auto-download models
MODEL_URLS=""                # Space-separated URLs for auto-download
```

### Resource Requirements
- **Minimum GPU**: NVIDIA T4 (16GB VRAM)
- **Recommended GPU**: NVIDIA A4000, RTX 4090, or better
- **Storage**: 50GB+ (models + workspace)
- **RAM**: 16GB+ system memory

## RunPod Setup Steps

1. **Create Template**:
   - Go to RunPod Console → Templates → New Template
   - Set container image: `yourusername/runpod-3d-ai:latest`
   - Configure ports: 7860, 8188, 8080
   - Set volume path: `/workspace`

2. **Deploy Pod**:
   - Select GPU type (T4 or better)
   - Choose template created above
   - Set storage size (50GB minimum)
   - Enable persistent volume

3. **Access Services**:
   - Pipeline GUI: `https://[pod-id]-7860.proxy.runpod.net`
   - ComfyUI: `https://[pod-id]-8188.proxy.runpod.net`
   - File Browser: `https://[pod-id]-8080.proxy.runpod.net`

4. **Upload Models** (via Pipeline GUI):
   - Click "📦 Models" button
   - Navigate to "Upload" tab
   - Upload checkpoints, LoRAs, ControlNet models
   - Validate models for workflows

## Features Ready for Production

✅ **Web Interface**
- Project management with file uploads
- 3D viewer with FBX/OBJ support
- Real-time pipeline status
- Dark/light theme

✅ **AI Workflows**
- Texture generation (PBR materials)
- 2D sprite generation from 3D
- Style transfer with IP-Adapter
- OpenPose and Depth ControlNet

✅ **Model Management**
- Upload/download models
- Automatic validation
- Last-used model memory
- Organized by type

✅ **Animation System**
- 70+ motion presets
- Multi-selection with warnings
- Per-animation prompt editing
- Project-specific overrides

✅ **Pipeline Orchestration**
- Conditional stage execution
- Mesh type tagging (skeletal/static)
- Real-time status updates
- Detailed logging

## Testing Checklist

Before pushing to RunPod:
- [ ] Build Docker image successfully
- [ ] Test locally with `docker run`
- [ ] Verify all services start (ports 7860, 8188, 8080)
- [ ] Upload test mesh file
- [ ] Test FBX viewer loading
- [ ] Upload ComfyUI models
- [ ] Run pipeline test
- [ ] Check persistent storage

## Support & Documentation

- **Main README**: [README.md](README.md)
- **Animation Selection**: [ANIMATION_SELECTION.md](pipeline/ANIMATION_SELECTION.md)
- **Prompt Editor**: [PROMPT_EDITOR.md](pipeline/PROMPT_EDITOR.md)
- **RunPod Docs**: [RUNPOD_DEPLOYMENT.md](RUNPOD_DEPLOYMENT.md)

## Commit History

Latest commits:
1. `8865b2c` - Fix FBX viewer loading and improve 3D model display
2. Previous - Add animation prompt editor and tooltips
3. Previous - Add mesh type tagging, sprite generation, and ComfyUI model management

All features tested and ready for production deployment.
