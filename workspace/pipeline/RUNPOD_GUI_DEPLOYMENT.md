# RunPod Deployment Guide - Web GUI

## Overview

This guide shows how to expose the 3D Pipeline Web GUI as a third port on RunPod, alongside ComfyUI and File Browser.

---

## 🎯 Port Configuration

| Service | Port | Purpose |
|---------|------|---------|
| ComfyUI | 8188 | AI texture/workflow generation |
| File Browser | 8080 | File management |
| **Pipeline GUI** | **7860** | Project management & 3D viewer |

---

## 📦 Dockerfile Configuration

Add the Pipeline GUI to your RunPod Dockerfile:

```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# ... existing setup ...

# Install Python dependencies for Pipeline GUI
COPY pipeline/requirements.txt /workspace/pipeline/requirements.txt
RUN pip install -r /workspace/pipeline/requirements.txt

# Install additional dependencies
RUN pip install flask werkzeug

# Copy pipeline files
COPY pipeline/ /workspace/pipeline/

# Expose ports
EXPOSE 8188  # ComfyUI
EXPOSE 8080  # File Browser  
EXPOSE 7860  # Pipeline GUI

# Startup script will handle all three services
COPY startup.sh /workspace/startup.sh
RUN chmod +x /workspace/startup.sh

CMD ["/workspace/startup.sh"]
```

---

## 🚀 Startup Script

Create `/workspace/startup.sh` to start all three services:

```bash
#!/bin/bash

echo "Starting 3D Character Pipeline Services..."

# Set environment variables
export WORKSPACE_ROOT="/workspace"
export PYTHONPATH="/workspace:${PYTHONPATH}"

# Start ComfyUI (Port 8188)
echo "[1/3] Starting ComfyUI..."
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188 &
COMFYUI_PID=$!

# Start File Browser (Port 8080)
echo "[2/3] Starting File Browser..."
filebrowser --port 8080 --address 0.0.0.0 --root /workspace &
FILEBROWSER_PID=$!

# Start Pipeline GUI (Port 7860)
echo "[3/3] Starting Pipeline GUI..."
cd /workspace
python pipeline/api_server.py --port 7860 --host 0.0.0.0 &
PIPELINE_PID=$!

# Wait for services to start
sleep 5

echo ""
echo "=========================================="
echo "✓ All services started successfully!"
echo "=========================================="
echo "ComfyUI:      http://localhost:8188"
echo "File Browser: http://localhost:8080"
echo "Pipeline GUI: http://localhost:7860"
echo "=========================================="
echo ""

# Keep container running and monitor processes
wait $COMFYUI_PID $FILEBROWSER_PID $PIPELINE_PID
```

---

## 🔧 RunPod Template Configuration

### Option 1: RunPod Web Interface

1. **Go to RunPod Templates**
2. **Create New Template**
3. **Configure Ports:**
   ```json
   {
     "ports": "8188/http,8080/http,7860/http",
     "env": [
       {
         "key": "WORKSPACE_ROOT",
         "value": "/workspace"
       }
     ]
   }
   ```

### Option 2: RunPod API

```python
import runpod

# Create pod with three exposed ports
pod = runpod.create_pod(
    name="3d-pipeline",
    image_name="your-docker-image:latest",
    gpu_type_id="NVIDIA RTX A5000",
    ports="8188/http,8080/http,7860/http",
    volume_in_gb=50,
    env={
        "WORKSPACE_ROOT": "/workspace",
        "PROJECT_NAME": "Exhibition"
    }
)

print(f"Pod ID: {pod['id']}")
print(f"ComfyUI URL: {pod['ports']['8188']['url']}")
print(f"File Browser URL: {pod['ports']['8080']['url']}")
print(f"Pipeline GUI URL: {pod['ports']['7860']['url']}")
```

### Option 3: Docker Compose (Local Testing)

```yaml
version: '3.8'

services:
  pipeline-workspace:
    image: 3d-pipeline:latest
    ports:
      - "8188:8188"  # ComfyUI
      - "8080:8080"  # File Browser
      - "7860:7860"  # Pipeline GUI
    volumes:
      - ./workspace:/workspace
    environment:
      - WORKSPACE_ROOT=/workspace
      - PROJECT_NAME=Exhibition
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Run with:
```bash
docker-compose up -d
```

---

## 🌐 Accessing the GUI

### From RunPod Dashboard:

1. **Navigate to your pod**
2. **Click "Connect"**
3. **Find exposed ports:**
   - Port 8188 → ComfyUI
   - Port 8080 → File Browser
   - **Port 7860 → Pipeline GUI** ⭐

### Direct URL Format:

```
https://<pod-id>-7860.proxy.runpod.net
```

Example:
```
https://abc123xyz-7860.proxy.runpod.net
```

---

## 🔐 Security Configuration

### Add Authentication (Recommended for production)

Modify `api_server.py`:

```python
from flask import Flask, request, jsonify, abort
from functools import wraps

# Simple token authentication
API_TOKEN = os.getenv('PIPELINE_API_TOKEN', 'your-secret-token')

def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f'Bearer {API_TOKEN}':
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

# Protect sensitive endpoints
@app.route("/api/pipeline/run", methods=["POST"])
@require_token
def run_pipeline():
    # ... existing code ...
```

Set token in RunPod:
```bash
export PIPELINE_API_TOKEN="your-secure-token-here"
```

---

## 📊 Health Checks

Add health check endpoint (already included):

```python
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "workspace": str(WORKSPACE_ROOT),
        "services": {
            "comfyui": check_comfyui(),
            "pipeline": "running"
        }
    })
```

RunPod can monitor: `http://localhost:7860/health`

---

## 🐛 Troubleshooting

### Issue: GUI not accessible

**Check if service is running:**
```bash
# SSH into pod
curl http://localhost:7860/health
```

**Check logs:**
```bash
# In startup script, add logging
python pipeline/api_server.py --port 7860 2>&1 | tee /workspace/logs/gui.log
```

### Issue: File uploads fail

**Check disk space:**
```bash
df -h /workspace
```

**Check permissions:**
```bash
chmod 777 /workspace/pipeline/web_ui/uploads
```

### Issue: 3D viewer not loading models

**Check Three.js CDN:**
- Ensure pod has internet access
- Or bundle Three.js locally

**Check file formats:**
- Supported: FBX, OBJ, glTF, GLB
- File size limit: 500MB (configurable)

---

## 🔄 Auto-Start Configuration

### Systemd Service (for persistent pods)

Create `/etc/systemd/system/pipeline-gui.service`:

```ini
[Unit]
Description=3D Pipeline Web GUI
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/workspace
ExecStart=/usr/bin/python3 /workspace/pipeline/api_server.py --port 7860 --host 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
systemctl enable pipeline-gui
systemctl start pipeline-gui
```

---

## 📈 Monitoring

### Log to File

```python
# In api_server.py main()
import logging
logging.basicConfig(
    filename='/workspace/logs/pipeline-gui.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Prometheus Metrics (Optional)

```python
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Metrics available at /metrics
```

---

## 🎨 Customization

### Change Default Port

```bash
# In startup.sh
python pipeline/api_server.py --port 9000 --host 0.0.0.0
```

Update RunPod template ports accordingly.

### Custom Branding

Edit `web_ui/index.html`:
```html
<h1>🎬 Your Studio Name - 3D Pipeline</h1>
```

Edit `web_ui/static/style.css`:
```css
:root {
    --accent-primary: #your-color;
}
```

---

## 📋 Complete Example: RunPod Deployment

### 1. Build Docker Image

```bash
docker build -t your-registry/3d-pipeline:latest .
docker push your-registry/3d-pipeline:latest
```

### 2. Create RunPod Template

```json
{
  "name": "3D Character Pipeline",
  "docker_image": "your-registry/3d-pipeline:latest",
  "ports": "8188/http,8080/http,7860/http",
  "volume_size": 50,
  "env": [
    {"key": "WORKSPACE_ROOT", "value": "/workspace"},
    {"key": "COMFYUI_URL", "value": "http://localhost:8188"}
  ],
  "start_script": "/workspace/startup.sh"
}
```

### 3. Launch Pod

```bash
runpod create pod \
  --template "3D Character Pipeline" \
  --gpu "RTX A5000" \
  --volume 50
```

### 4. Access Services

Visit RunPod dashboard and click on:
- **Port 7860** → Pipeline GUI
- **Port 8188** → ComfyUI
- **Port 8080** → File Browser

---

## 🎯 Quick Start Checklist

- [ ] Docker image includes Flask dependencies
- [ ] Startup script starts all three services
- [ ] Ports 8188, 8080, 7860 exposed in RunPod template
- [ ] Web UI files copied to `/workspace/pipeline/web_ui/`
- [ ] WORKSPACE_ROOT environment variable set
- [ ] Health check endpoint responding
- [ ] Test file upload functionality
- [ ] Test 3D model viewer with sample FBX

---

## 🔗 Related Documentation

- [api_server.py](api_server.py) - Backend API implementation
- [web_ui/index.html](web_ui/index.html) - Frontend interface
- [POD_INTEGRATION.md](POD_INTEGRATION.md) - General pod integration
- [README.md](README.md) - Pipeline overview

---

## 💡 Tips

1. **Pre-load Three.js** - Bundle it locally for faster loading
2. **Use websockets** - For real-time pipeline progress updates
3. **Enable CORS** - If GUI and API on different domains
4. **Optimize file transfers** - Use chunked uploads for large files
5. **Add rate limiting** - Prevent abuse of upload endpoint

---

## 🆘 Support

If you encounter issues:
1. Check `/workspace/logs/pipeline-gui.log`
2. Verify all three services are running: `ps aux | grep python`
3. Test health endpoint: `curl http://localhost:7860/health`
4. Check RunPod firewall settings
5. Ensure GPU drivers installed for ComfyUI

Enjoy your 3D Character Pipeline! 🎬
