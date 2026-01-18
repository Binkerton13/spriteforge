# 3D Character Pipeline Integration

## Overview
The Exhibition 3D character processing pipeline has been successfully integrated into the runpod-3d-ai-template. This provides a complete web-based GUI for managing 3D character workflows alongside ComfyUI and File Browser.

## Three-Service Architecture

### Port Configuration
- **Port 8188**: ComfyUI (AI workflow system)
- **Port 8080**: File Browser (file management)
- **Port 7860**: Pipeline GUI (3D character pipeline)

### Services Managed by supervisord
All three services run simultaneously under supervisord:

1. **ComfyUI** (priority=10)
   - Handles AI-driven texture generation
   - Provides node-based workflow interface
   - Integrates with pipeline via ComfyUI workflows

2. **File Browser** (priority=20)
   - Browse/upload/download files in /workspace
   - Direct file editing capabilities
   - 5GB upload limit per file

3. **Pipeline GUI** (priority=30)
   - 3D model viewer with Three.js
   - Drag-and-drop file uploads
   - Project management
   - Full pipeline orchestration

## Pipeline Features

### Web GUI Capabilities
- **3D Viewer**: Real-time FBX/OBJ preview
- **File Upload**: Mesh files, UDIM tiles, references
- **Configuration**: Texture/rig/animation settings
- **Execution**: One-click pipeline start
- **Monitoring**: Real-time progress tracking

### Workflow Stages
1. **Texturing**: PBR material generation (Albedo, Normal, Roughness, Metallic, AO)
2. **Rigging**: Automated skeleton with UniRig
3. **Deformation Fix**: AI-driven mesh correction
4. **Animation**: Motion generation with HY-Motion
5. **Export**: FBX, GLTF, USD formats

## File Structure

\\\
/workspace/
 pipeline/               # Pipeline code (copied from /opt/pipeline on startup)
    api_server.py      # Flask API backend
    bootstrap.py       # Project structure creator
    project_init.py    # Multi-strategy project initialization
    one_click.py       # Master orchestrator
    web_ui/            # Web interface
       index.html
       static/
           style.css
           app.js
    tools/             # Pipeline utilities
    comfui_workflows/  # ComfyUI JSON workflows
    hy_motion_prompts/ # Animation prompts
 config/                # Configuration files
    animation_settings.json
    rig_settings.json
    texture_settings.json
 <project_name>/        # User projects (e.g., Exhibition)
     0_input/
     1_textures/
     2_rig/
     3_animation/
     4_export/
\\\

## Usage

### Building the Image
\\\ash
cd runpod-3d-ai-template
docker build -f Dockerfile.runpod -t 3d-ai-workstation:latest .
\\\

### Running Locally
\\\ash
docker run -it --gpus all \\
  -p 8188:8188 \\
  -p 8080:8080 \\
  -p 7860:7860 \\
  -v \E:\2D Programs\DockerFiles\runpod-3d-ai-template/workspace:/workspace \\
  3d-ai-workstation:latest
\\\

### Accessing Services
- ComfyUI: http://localhost:8188
- File Browser: http://localhost:8080
- Pipeline GUI: http://localhost:7860

### On RunPod
When deployed to RunPod, access services via:
- ComfyUI: https://\<pod-id\>-8188.proxy.runpod.net
- File Browser: https://\<pod-id\>-8080.proxy.runpod.net
- Pipeline GUI: https://\<pod-id\>-7860.proxy.runpod.net

## Environment Variables

\\\ash
PORT=8188                    # ComfyUI port
FILE_BROWSER_PORT=8080       # File browser port
PIPELINE_GUI_PORT=7860       # Pipeline GUI port
WORKSPACE=/workspace         # Base directory
MODEL_DOWNLOAD_ON_START=0    # Auto-download models
MODEL_URLS=""                # Comma-separated URLs
\\\

## Project Initialization

The pipeline supports multiple initialization strategies:

### 1. Interactive Mode (Default)
\\\python
python /opt/pipeline/project_init.py
# Prompts for project name
\\\

### 2. Environment Variable
\\\ash
export PROJECT_NAME=MyCharacter
python /opt/pipeline/project_init.py
\\\

### 3. Command Line
\\\ash
python /opt/pipeline/project_init.py --project MyCharacter
\\\

### 4. Web GUI
Access http://localhost:7860 and use the project selector interface.

## Files Modified/Added

### New Files
- \pipeline/api_server.py\ - Flask API with file upload
- \pipeline/project_init.py\ - Multi-strategy initialization
- \pipeline/web_ui/index.html\ - Main web interface
- \pipeline/web_ui/static/style.css\ - Dark theme styling
- \pipeline/web_ui/static/app.js\ - Frontend logic
- \pipeline/cleanup_pipeline.py\ - Remove redundant files
- \pipeline/*.md\ - Documentation files

### Modified Files
- \Dockerfile.runpod\ - Added Pipeline GUI service
- \supervisord.conf\ - Added pipeline_gui program
- \README.md\ - Added Pipeline GUI documentation
- \pipeline/bootstrap.py\ - Added --project parameter
- \pipeline/one_click.py\ - Fixed import error

## Next Steps

1. **Test Build**:
   \\\ash
   docker build -f Dockerfile.runpod -t test-pipeline .
   docker run -it --gpus all -p 8188:8188 -p 8080:8080 -p 7860:7860 test-pipeline
   \\\

2. **Deploy to RunPod**:
   - Push image to Docker Hub or GitHub Container Registry
   - Create RunPod template with 3 TCP ports exposed
   - Deploy pod and access services

3. **Workflow Testing**:
   - Upload test mesh via Pipeline GUI
   - Upload UDIM tiles
   - Start pipeline execution
   - Monitor progress in GUI
   - Download results from File Browser

## Support & Documentation

- Pipeline README: \/workspace/pipeline/README.md\
- Quick Start: \/workspace/pipeline/QUICKSTART_GUI.md\
- Deployment Guide: \/workspace/pipeline/RUNPOD_GUI_DEPLOYMENT.md\
- Web GUI Features: \/workspace/pipeline/WEB_GUI_SUMMARY.md\
- Pod Integration: \/workspace/pipeline/POD_INTEGRATION.md\

## Technical Stack

- **Backend**: Python 3.8+, Flask 2.3+, werkzeug
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Three.js r128
- **Container**: Docker, CUDA 12.1.1, PyTorch
- **Process Management**: supervisord
- **3D Processing**: Blender, UniRig, TripoSR
- **AI**: ComfyUI, HY-Motion

---

**Integration Status**:  Complete
**Last Updated**: 2026-01-17 23:50:45
**Location**: runpod-3d-ai-template/
