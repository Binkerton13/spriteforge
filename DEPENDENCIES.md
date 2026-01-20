# Quick Dependency Installation Guide

This guide covers installing the three required dependencies for the 3D AI pipeline on RunPod.

## Automated Installation (Recommended)

Run the installation script:

```bash
cd /workspace
chmod +x install_dependencies.sh
./install_dependencies.sh
```

This will install:
1. ✅ Pillow (for sprite generation)
2. ✅ UniRig (for auto-rigging)
3. ✅ HY-Motion (for animation generation)

⚠️ **Note**: You'll still need to manually download the AI model checkpoints (see below).

---

## Manual Installation

### 1. Install Pillow in Blender Python

```bash
# Find Blender's Python
/opt/blender/4.0/python/bin/python3.10 -m pip install --upgrade pip
/opt/blender/4.0/python/bin/python3.10 -m pip install Pillow

# Verify installation
/opt/blender/4.0/python/bin/python3.10 -c "from PIL import Image; print('Pillow installed')"
```

**Purpose**: Required by `generate_sprites_enhanced.py` for image processing, sprite sheet generation, and background removal.

---

### 2. Install UniRig

```bash
cd /workspace

# Clone repository
git clone https://github.com/VAST-AI-Research/UniRig.git unirig
cd unirig

# Edit requirements.txt to remove problematic packages
sed -i '/bpy/d' requirements.txt       # Conflicts with standalone Blender
sed -i '/flash_attn/d' requirements.txt # Optional, complex to compile

# Install dependencies
pip install -r requirements.txt
```

**Download Models** (~2-5 GB):
1. Visit: https://github.com/VAST-AI-Research/UniRig#download-models
2. Download skeleton generation and skinning weight models
3. Place in: `/workspace/unirig/models/`

**Verify Installation**:
```bash
ls /workspace/unirig/models/
# Should show model checkpoint files
```

**Without models**: Pipeline uses fallback armature (20-bone humanoid skeleton with automatic weights).

---

### 3. Install HY-Motion

```bash
cd /workspace

# Clone repository
git clone https://github.com/Tencent-Hunyuan/HY-Motion-1.0.git hy-motion
cd hy-motion

# Install dependencies
pip install -r requirements.txt
```

**Download Models** (~10-15 GB):
1. Visit: https://github.com/Tencent-Hunyuan/HY-Motion-1.0#model-download
2. Download text-to-motion model and encoders:
   - `hunyuan_motion_1.0.safetensors` (main model)
   - Motion encoder
   - Text encoder (CLIP)
3. Place in: `/workspace/hy-motion/models/`

**Verify Installation**:
```bash
ls /workspace/hy-motion/models/
# Should show model checkpoint files
```

**Without models**: Pipeline creates placeholder animations (copies rigged mesh with no animation data).

---

## Verification

Test that all dependencies are installed:

```bash
# Test Pillow
/opt/blender/4.0/python/bin/python3.10 -c "from PIL import Image; print('✓ Pillow OK')"

# Test UniRig
test -d /workspace/unirig && echo "✓ UniRig cloned" || echo "✗ UniRig missing"
test -d /workspace/unirig/models && ls /workspace/unirig/models/ || echo "⚠ UniRig models missing"

# Test HY-Motion
test -d /workspace/hy-motion && echo "✓ HY-Motion cloned" || echo "✗ HY-Motion missing"
test -d /workspace/hy-motion/models && ls /workspace/hy-motion/models/ || echo "⚠ HY-Motion models missing"
```

---

## Running the Pipeline

Once dependencies are installed:

```bash
cd /workspace/pipeline
python api_server.py
```

Access the web UI at: **http://localhost:7860**

The pipeline will automatically:
- ✅ Detect if UniRig is available (use it or fallback to basic armature)
- ✅ Detect if HY-Motion is available (use it or create placeholder)
- ✅ Use Pillow for sprite generation

---

## Fallback Behavior

If models are not downloaded, the pipeline still works with reduced functionality:

| Component | Without Models | Fallback Behavior |
|-----------|---------------|-------------------|
| **Pillow** | ❌ Pipeline fails | **REQUIRED** - No fallback |
| **UniRig** | ⚠️ Models missing | Basic 20-bone humanoid armature with automatic weights |
| **HY-Motion** | ⚠️ Models missing | Placeholder animations (rigged mesh, no motion) |

---

## Troubleshooting

### Pillow Not Found
```bash
# Error: PIL/Pillow not available
# Solution: Install in Blender's Python
/opt/blender/4.0/python/bin/python3.10 -m pip install Pillow
```

### UniRig Not Working
```bash
# Check installation
ls /workspace/unirig/
ls /workspace/unirig/models/

# If models missing, pipeline uses fallback armature (this is OK for testing)
```

### HY-Motion Not Working
```bash
# Check installation
ls /workspace/hy-motion/
ls /workspace/hy-motion/models/

# If models missing, pipeline creates placeholder animations (this is OK for testing)
```

### Permission Errors
```bash
# Fix ownership
chown -R $USER:$USER /workspace/unirig
chown -R $USER:$USER /workspace/hy-motion
```

---

## Storage Requirements

| Component | Repository | Models | Total |
|-----------|-----------|--------|-------|
| Pillow | 0 MB | 0 MB | 0 MB |
| UniRig | ~500 MB | ~2-5 GB | ~5 GB |
| HY-Motion | ~1 GB | ~10-15 GB | ~15 GB |
| **TOTAL** | | | **~20 GB** |

Ensure you have at least **25 GB** free space on `/workspace` for all dependencies.

---

## Next Steps

After installation:

1. ✅ **Test the pipeline** with a sample project
2. ✅ **Check logs** at `/workspace/<project>/pipeline/pipeline_log.txt`
3. ✅ **Download models** if you want full functionality (not required for testing)
4. ✅ **Install ComfyUI dependencies** for sprite generation (see `COMFYUI_INSTALLATION.md`)

For ComfyUI setup, click the **⚙️ ComfyUI Setup** button in the web UI to see required custom nodes and models.
