A complete, user‑friendly instruction manual.

```markdown
# SpriteForge Workflow Guide  
*A complete step‑by‑step manual for the full animation‑to‑sprite pipeline.*

---

# 1. Motion Generation (HY‑Motion)

### 1. Open the Motion Page  
Navigate to: 
    /motion

### 2. Choose a preset  
Available presets include:

- walk  
- run  
- idle  
- jump  
- attack  
- stealth  
- interact  
- dance  

### 3. Generate motion  
Click **Generate Motion**.  
HY‑Motion produces a short animation clip.

### 4. Preview  
Use:

- Video preview  
- Frame-by-frame preview  

### 5. Export frames  
Frames are saved under: 
    /workspace/animations/<motion_name>/

---

# 2. Frame Management

Each motion produces a directory of frames: 
    /workspace/animations/<motion>/frames/

You can:

- Delete frames  
- Reorder frames  
- Replace frames  
- Add interpolated frames (optional)  

---

# 3. Sprite Generation (ComfyUI)

### 1. Open the Sprite Page  
Navigate to:
    /sprites

### 2. Select a frame directory  
Use the file browser modal.

### 3. Choose a style  
Options include:

- Default  
- Custom style presets  
- IP‑Adapter identity locking  
- ControlNet pose/depth/normal  

### 4. Generate sprites  
Each frame is passed through ComfyUI using:

- AnimateDiff‑Evolved  
- IP‑Adapter Plus  
- ControlNet Aux  
- Background removal  

Output is saved under:
    /workspace/sprites/<character>/<motion>/

---

# 4. Sprite Sheet Assembly

### 1. Open the Sprite Sheet Tool  
Navigate to:
    /spritesheet

### 2. Select a sprite directory  
Choose the folder containing generated sprites.

### 3. Configure layout  
Options:

- Rows  
- Columns  
- Padding  
- Background color  

### 4. Export  
SpriteForge generates:
    /workspace/sprites/<character>/<motion>/sheet.png

---

# 5. Workflow Editor

The workflow editor allows you to:

- Inspect ComfyUI workflows  
- Modify nodes  
- Validate workflows  
- Save custom workflows  

Workflows live under:
    /workspace/pipeline/workflows/

---

# 6. Model Management

Navigate to:
    /models

You can:

- View installed models  
- Upload new models  
- Activate model selections  
- Configure LoRAs, checkpoints, VAEs, ControlNet models  

---

# 7. Project System

Projects allow you to save:

- Motion selections  
- Style presets  
- Model selections  
- Workflow choices  
- Sprite output paths  

Projects live under:
    /workspace/projects/

---

# 8. Batch Processing

Batch mode allows you to:

- Generate multiple motions  
- For multiple characters  
- With multiple styles  

Batch definitions are stored under:
    /workspace/batches/

---

# 9. File Browser

The built‑in file browser (port 8080) allows you to:

- Upload assets  
- Inspect workspace files  
- Download outputs  
- Delete unused files  

---

# 10. Logs & Debugging

Logs are stored under:
    /workspace/logs/

Includes:

- GUI backend logs  
- ComfyUI logs  
- Motion generation logs  
- Sprite generation logs  

---

# End of Guide












