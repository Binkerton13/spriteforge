# runpod-3d-ai-template
A full 3D + AI production environment for Runpod, including Hy-Motion, UniRig, Blender (headless), ComfyUI, and TripoSR.

## Features

### Services
- **ComfyUI**: Runs on port `8188` (configurable via `PORT` environment variable)
- **File Browser**: Runs on port `8080` with full upload and editing capabilities

### File Browser
Access the file browser at `http://<your-runpod-url>:8080/` to:
- 📁 Browse the entire `/workspace` directory
- ⬆️ Upload files (up to 5GB each)
- 📝 Create and edit text files directly in the browser
- 📂 Create new folders
- ⬇️ Download files
- 🗑️ Delete files and folders
- Drag-and-drop file uploads

The file browser provides a modern, dark-themed interface optimized for managing AI model files, scripts, and outputs.

### AI Tools Included
- **ComfyUI**: Node-based stable diffusion UI
- **UniRig**: Advanced 3D rigging
- **TripoSR**: 3D reconstruction
- **Hy-Motion**: Motion generation
- **Blender**: Headless 3D rendering and animation

## Usage

### Building
```bash
# Full build with all tools
docker build -t runpod-3d-ai -f Dockerfile .

# Runtime-only build (smaller)
docker build -t runpod-3d-ai-runtime -f Dockerfile.runpod .
```

### Running Locally
```bash
docker run -it --gpus all \
  -p 8188:8188 \
  -p 8080:8080 \
  -v $(pwd)/workspace:/workspace \
  runpod-3d-ai
```

Access:
- ComfyUI: http://localhost:8188
- File Browser: http://localhost:8080

### Environment Variables
- `PORT`: ComfyUI port (default: 8188)
- `WORKSPACE`: Base directory for file browser (default: /workspace)
- `FILE_BROWSER_PORT`: File browser port (default: 8080)
- `MODEL_DOWNLOAD_ON_START`: Set to `1` to download models on startup
- `MODEL_URLS`: Comma-separated list of model URLs to download

## Runpod Deployment

When deploying to Runpod:
1. The container will automatically start both ComfyUI and the File Browser
2. Map port 8080 in your Runpod template settings to access the file browser
3. Use the file browser to upload models, scripts, and manage your workspace
4. All changes are persisted in the `/workspace` volume
