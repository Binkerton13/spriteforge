# 3D Character Pipeline  
A modular, production‑grade 3D character pipeline for UDIM texturing, auto‑rigging, AI deformation correction, HY‑Motion animation, retargeting, and final export packaging.

This repository provides a **fully automated, end‑to‑end character processing pipeline** designed for Runpod, Blender, ComfyUI, UniRig, and HY‑Motion.

**✨ Multi-Project Support:** Each project can have a custom name specified by the user on initialization.

---

## 🌐 Overview

This pipeline transforms a clean character mesh into a fully animated, retargeted, textured, and export‑ready asset.

It includes:

- **UDIM texture generation** via ComfyUI  
- **PBR map generation**  
- **Auto‑rigging** via UniRig  
- **Rig cleanup** (orientation, weights, validation)  
- **AI deformation correction**  
- **HY‑Motion animation generation**  
- **Animation retargeting**  
- **Final export packaging**  
- **A single orchestrator (`one_click.py`)**  

---

## 📁 Folder Structure

<ProjectName>/
│
├── 0_input/                 # Raw meshes, UVs, references
├── 1_textures/              # UDIM + PBR outputs
├── 2_rig/                   # Auto-rigging + cleanup
├── 3_animation/             # HY-Motion + retargeting
├── 4_export/                # Final packaged output (FBX, glTF, USD)
├── config/                  # Project-specific settings
│
└── pipeline/
    ├── tools/               # Blender + Python tools
    ├── comfyui_workflows/   # Texture + deform workflows
    ├── hy_motion_prompts/   # Prompt builder + library
    ├── bootstrap.py         # Folder creator
    ├── project_init.py      # Project initialization
    ├── api_server.py        # REST API for pod integration
    ├── config.json          # Pipeline configuration
    └── one_click.py         # Master orchestrator

---

## 🚀 Quick Start

### Option A: Web GUI (Recommended) 🎨

**Start the web interface:**
```bash
python pipeline/api_server.py --port 7860
```

Then open your browser to: `http://localhost:7860`

**Features:**
- 🎨 **3D Model Viewer** - Preview FBX/OBJ files with Three.js
- 📂 **Drag & Drop Upload** - Easy file management
- ⚙️ **Visual Configuration** - Edit prompts and settings in a GUI
- 📊 **Real-time Pipeline Status** - Monitor progress
- 🎬 **Project Management** - Create and switch between projects

### Option B: Command Line

**1. Initialize Your Project**

**Interactive Mode (Recommended):**
```bash
python pipeline/project_init.py --interactive
```

**With Project Name:**
```bash
python pipeline/project_init.py --project MyCharacter
```

**For Pod Environment:**
```bash
export PROJECT_NAME="MyCharacter"
python pipeline/project_init.py --from-env
```

### 2. Add Your Input Files
Place your clean FBX and UV tiles into:
```
<ProjectName>/0_input/meshes/character_clean.fbx
<ProjectName>/0_input/uv_layouts/*.png
```

### 3. Configure the Pipeline  
Edit:
```
<ProjectName>/pipeline/config.json
```

### 4. Run the Full Pipeline  
```bash
cd <ProjectName>
python pipeline/one_click.py
```

### 5. Optional: Run Cleanup

Remove redundant files and empty folders:
```bash
python pipeline/cleanup_pipeline.py
```

---

# High‑Level Pipeline Diagram

```mermaid
flowchart TD
    A0[0_input<br/>clean_fbx + UVs] --> A1[Mesh Validation<br/>validate_mesh.py]

    A1 --> B1[UDIM Texture Generation<br/>texture_workflow.json]
    B1 --> B2[PBR Map Generation<br/>pbr_*.json]
    B2 --> B3[UDIM Packaging<br/>package_udim_material]

    B3 --> C1[Auto-Rigging<br/>unirig.py]
    C1 --> C2[Rig Validation<br/>validate_rig.py]
    C2 --> C3[Joint Orientation Fix<br/>fix_joint_orientation.py]
    C3 --> C4[Weight Smoothing<br/>smooth_weights.py]

    C4 --> D1[Pose Sampling<br/>sample_deform_poses.py]
    D1 --> D2[AI Deform Fix<br/>deform_fix_workflow.json]
    D2 --> D3[Apply Corrections<br/>apply_deform_corrections.py]

    D3 --> E1[HY-Motion Animation<br/>hy_motion.py]
    E1 --> F1[Retarget Animation<br/>retarget.py]
    F1 --> G1[Final Export Package<br/>export_package.py]

# Subsystem Diagrams

## UDIM Texture Generation

flowchart TD
    A[UV Tiles<br/>0_input/uv_layouts] --> B[texture_workflow.json]
    B --> C[ComfyUI Texture Generation]
    C --> D[Albedo Maps<br/>1_textures/albedo]

    D --> E[PBR Workflows<br/>pbr_normal.json<br/>pbr_roughness.json<br/>pbr_metallic.json<br/>pbr_ao.json]
    E --> F[ComfyUI PBR Generation]
    F --> G[PBR Maps<br/>1_textures/{normal,roughness,metallic,ao}]

    G --> H[UDIM Packaging<br/>package_udim_material]
    H --> I[UDIM Material Set<br/>1_textures/udim_material]

## Rigging (UniRig + Cleanup)

flowchart TD
    A[clean_fbx] --> B[unirig.py]
    B --> C[character_rigged.fbx]

    C --> D[validate_rig.py]
    D --> E[fix_joint_orientation.py]
    E --> F[smooth_weights.py]

    F --> G[rig_output_smoothed.fbx]

## AI Deformation Correction

flowchart TD
    A[rig_output_smoothed.fbx] --> B[sample_deform_poses.py]
    B --> C[Pose Meshes]

    C --> D[deform_fix_workflow.json]
    D --> E[ComfyUI AI Correction]

    E --> F[Corrected Maps]
    F --> G[apply_deform_corrections.py]
    G --> H[corrected_fbx]

## HY‑Motion Animation

flowchart TD
    A[motion.txt] --> B[hy_motion.py]
    B --> C[HunyuanMotionPipeline]
    C --> D[raw_animation.fbx]

## Retargeting

flowchart TD
    A[rigged_fbx_cleaned] --> C[retarget.py]
    B[raw_animation.fbx] --> C
    D[bone_mapping.json] --> C

    C --> E[animation_retargeted.fbx]

## Final Export Packaging

flowchart TD
    A[animation_retargeted.fbx] --> D[export_package.py]
    B[rigged_fbx_cleaned] --> D
    C[UDIM Material Set] --> D

    D --> E[4_export/<project_name>/]

Tools & Scripts
    Blender Tools
        validate_mesh.py

        validate_rig.py

        fix_joint_orientation.py

        smooth_weights.py

        sample_deform_poses.py

        apply_deform_corrections.py

        retarget.py

    Python Tools
        hy_motion.py

        export_package.py

        bootstrap.py

    ComfyUI Workflows
        texture_workflow.json

        pbr_normal.json

        pbr_roughness.json

        pbr_metallic.json

        pbr_ao.json

        deform_fix_workflow.json

Configuration
    All pipeline settings live in:

    pipeline/config.json

        This includes:

        UDIM tiles

        PBR outputs

        UniRig settings

        HY‑Motion paths

        Deform‑fix workflow

        Retargeting mapping

        Export settings

## 🔧 Running Individual Stages

### Validate Mesh
```bash
blender -b --python pipeline/tools/validate_mesh.py -- <fbx>
```

### Generate UDIM Textures
```bash
python3 pipeline/one_click.py  # runs full pipeline
```

### HY‑Motion Only
```bash
python3 pipeline/tools/hy_motion.py --prompt motion.txt --output anim.fbx
```

### Retarget Only
```bash
blender -b --python pipeline/tools/retarget.py -- rig.fbx anim.fbx mapping.json output.fbx
```

---

## 🚢 Pod Integration

For RunPod or similar container environments, see [POD_INTEGRATION.md](POD_INTEGRATION.md) for:
- Environment variable configuration
- API-based project creation
- Pre-pod and post-pod initialization strategies
- 3D-AI-Workstation integration patterns

**Quick Pod Setup:**
```bash
# Set project name as environment variable
export PROJECT_NAME="MyCharacter"

# Initialize on pod startup
python pipeline/project_init.py --from-env
```

**API Server for Pod Management:**
```bash
# Start API server
python pipeline/api_server.py --port 8080

# Create project via API
curl -X POST http://pod-ip:8080/api/projects/create \
  -H "Content-Type: application/json" \
  -d '{"project_name": "MyCharacter"}'
```

---

## 📝 Project Management Commands

### Create New Project
```bash
python pipeline/project_init.py --project MyNewCharacter
```

### Rename Existing Project
```bash
python pipeline/project_init.py --rename Exhibition MyCharacter
```

### List Projects (requires API server)
```bash
curl http://localhost:8080/api/projects
```

### Clean Up Redundant Files
```bash
python pipeline/cleanup_pipeline.py
```

---

## 📚 Additional Documentation

- [🌐 RUNPOD_GUI_DEPLOYMENT.md](RUNPOD_GUI_DEPLOYMENT.md) - **Deploy Web GUI on RunPod (Port 7860)**
- [🚀 POD_INTEGRATION.md](POD_INTEGRATION.md) - Pod integration strategies and patterns
- [⚙️ pipeline/config.json](config.json) - Configuration reference
- [🔧 Individual tool documentation](tools/) - in `pipeline/tools/`

---

## 🗑️ Cleanup & Maintenance

The pipeline includes a cleanup script to remove:
- Empty configuration files
- Redundant documentation
- Unused UI components
- Empty script folders

```bash
python pipeline/cleanup_pipeline.py
```

---

## 📋 License

MIT License

## 🙏 Credits

- **HY‑Motion** by Tencent Hunyuan
- **UniRig** - Auto-rigging system
- **Blender Foundation** - 3D creation suite
- **ComfyUI** - AI workflow system
- **Pipeline** by Morgen