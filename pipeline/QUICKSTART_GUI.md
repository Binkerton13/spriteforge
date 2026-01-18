# 🚀 Quick Start Guide - Web GUI

## Get Your Pipeline GUI Running in 3 Minutes!

---

## 📋 Prerequisites

- Python 3.8+
- pip

---

## ⚡ Installation

### 1. Install Dependencies

```bash
cd pipeline
pip install flask werkzeug
```

### 2. Start the Server

```bash
python api_server.py --port 7860
```

### 3. Open Your Browser

```
http://localhost:7860
```

---

## 🎯 First Steps in the GUI

### 1. **Create Your First Project**
   - Click **"+ New Project"** button
   - Enter project name (e.g., "MyCharacter")
   - Click **"Create"**

### 2. **Upload Your Character Mesh**
   - Drag and drop your FBX or OBJ file into the left panel
   - OR click **"Browse"** button
   - Watch it appear in the 3D viewer!

### 3. **Upload UDIM Tiles (Optional)**
   - Drag PNG texture files to the UDIM Tiles section
   - Multiple files supported

### 4. **Configure Settings**
   - **Right Panel:**
     - Edit texture prompts
     - Adjust rig settings
     - Set animation prompts
     - Choose export formats

### 5. **Save & Run**
   - Click **"💾 Save Config"** to save settings
   - Click **"▶️ Run Pipeline"** to start processing

---

## 🎨 3D Viewer Controls

| Action | Method |
|--------|--------|
| **Rotate** | Left-click + drag |
| **Pan** | Right-click + drag |
| **Zoom** | Scroll wheel |
| **Reset** | Click "↻ Reset View" |
| **Wireframe** | Click "⬚ Wireframe" |
| **Grid** | Click "⊞ Grid" |

---

## 🌐 Accessing from Other Devices

### On Local Network:

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   ```

2. Start server with host flag:
   ```bash
   python api_server.py --port 7860 --host 0.0.0.0
   ```

3. Access from another device:
   ```
   http://YOUR_IP:7860
   ```
   Example: `http://192.168.1.100:7860`

---

## 🐳 Running with Docker (Optional)

```bash
# Build image
docker build -t 3d-pipeline-gui .

# Run container
docker run -p 7860:7860 -v ./workspace:/workspace 3d-pipeline-gui

# Access
http://localhost:7860
```

---

## 🔧 Configuration Options

### Change Port:
```bash
python api_server.py --port 8000
```

### Set Workspace Path:
```bash
python api_server.py --workspace "/path/to/your/workspace"
```

### Run in Background:
```bash
# Windows (PowerShell)
Start-Process python -ArgumentList "api_server.py --port 7860" -WindowStyle Hidden

# Linux/Mac
nohup python api_server.py --port 7860 &
```

---

## 🚀 All Three Services Together

Start ComfyUI, File Browser, AND Pipeline GUI:

```bash
# Make executable (Linux/Mac)
chmod +x start_services.sh

# Run
./start_services.sh
```

**Access:**
- ComfyUI: http://localhost:8188
- File Browser: http://localhost:8080  
- **Pipeline GUI: http://localhost:7860** ⭐

---

## 🎬 Example Workflow

1. **Start GUI:** `python api_server.py --port 7860`
2. **Create Project:** Click "+ New Project" → Enter "FantasyWarrior"
3. **Upload Mesh:** Drag `warrior.fbx` to "Character Mesh" area
4. **View in 3D:** Model loads automatically in center viewer
5. **Upload UVs:** Drag `uv_1001.png`, `uv_1002.png` to "UDIM Tiles"
6. **Set Prompts:**
   - Positive: "realistic skin texture, fantasy armor"
   - Negative: "distortion, artifacts"
7. **Configure Rig:**
   - Preset: "Humanoid Game"
   - Scale: 1.0
8. **Save:** Click "💾 Save Config"
9. **Run:** Click "▶️ Run Pipeline"
10. **Monitor:** Watch pipeline progress in modal

---

## 📱 Browser Compatibility

| Browser | Status |
|---------|--------|
| Chrome 90+ | ✅ Full support |
| Firefox 88+ | ✅ Full support |
| Edge 90+ | ✅ Full support |
| Safari 14+ | ✅ Full support |
| Mobile Safari | ⚠️ Limited (no file upload) |
| Chrome Mobile | ⚠️ Limited (no file upload) |

**Note:** Requires WebGL support for 3D viewer

---

## 🐛 Troubleshooting

### Issue: Port already in use
```bash
# Find and kill process using port
# Windows
netstat -ano | findstr :7860
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:7860 | xargs kill -9
```

### Issue: Can't upload files
- Check folder permissions
- Verify `pipeline/web_ui/uploads/` exists
- Check file size (max 500MB by default)

### Issue: 3D viewer not loading
- Ensure internet connection (for Three.js CDN)
- Check browser console for errors (F12)
- Try different browser

### Issue: "Module not found" error
```bash
pip install flask werkzeug
```

---

## 💡 Tips & Tricks

1. **Multiple Projects:** Switch between projects using dropdown
2. **Quick Upload:** Drag files directly from file explorer
3. **Model Inspection:** Use wireframe mode to see topology
4. **Copy Settings:** Export config JSON, edit, re-import
5. **Keyboard:** Tab through form fields for quick editing

---

## 📞 Need Help?

- Check `/health` endpoint: http://localhost:7860/health
- View logs in terminal
- Check browser console (F12)
- See full documentation: [WEB_GUI_SUMMARY.md](WEB_GUI_SUMMARY.md)

---

## 🎉 You're Ready!

Your 3D Character Pipeline web interface is now running. Start creating amazing characters! 🎨

**Next:** [Deploy to RunPod](RUNPOD_GUI_DEPLOYMENT.md) for remote access with GPU acceleration.
