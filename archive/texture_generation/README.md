# Texture Generation - ARCHIVED

**Status**: Deprecated and moved to archive (2026-01-20)

## Why Archived?

The texture generation system was removed from the main pipeline because:

1. **Not needed for 2D sprite workflow**: AI-enhanced sprites don't require pre-generated 3D textures
2. **Complex dependencies**: Required custom ComfyUI nodes not in base installation
3. **Performance overhead**: UDIM multi-tile generation was slow
4. **Pipeline focus shift**: New focus is on game-ready 2D sprites, not 3D mesh texturing

## What Was Archived?

- `generate_textures.py` - UDIM texture generation tool
- `texture_workflow.json` - ComfyUI diffuse/albedo workflow
- `pbr_*.json` - PBR map generation workflows (normal, roughness, metallic, AO)

## New Pipeline

The new sprite-focused pipeline is:

```
Input Mesh (FBX/OBJ)
    ↓
UniRig (Auto-rig skeleton)
    ↓
HY-Motion (Generate animations)
    ↓
Blender (Render animation frames with control maps)
    ↓
ComfyUI (AI-enhance frames → game-ready sprites)
    ↓
Output: 2D sprite sheets for 3D action games
```

See [SPRITE_PIPELINE.md](../../SPRITE_PIPELINE.md) for current documentation.

## If You Need 3D Textures

This code still works! To use:

1. Copy files back to `pipeline/tools/` and `pipeline/comfui_workflows/`
2. Install required ComfyUI custom nodes (see archived workflow comments)
3. Run standalone: `python generate_textures.py <project_path> <config_path>`

## Technical Details

### UDIM Multi-Tile System
- Scanned `0_input/uv_layouts/` for uploaded UV layout images
- Extracted tile numbers via regex: `r'(\d{4})'`
- Generated textures for all detected tiles (1001-100N)

### ComfyUI Workflows
- `texture_workflow.json`: SDXL-based diffuse texture generation
- `pbr_normal.json`: Normal map generation (requires NormalMap node)
- `pbr_roughness.json`: Roughness map (requires ImageToGray node)
- `pbr_metallic.json`: Metallic map (requires ConstantColor node)
- `pbr_ao.json`: Ambient occlusion map (requires custom AO node)

### Configuration
```json
{
  "texture_generation": {
    "prompt": "skin texture, realistic pores",
    "negative_prompt": "blurry, low quality",
    "seed": 13,
    "resolution": [1024, 1024],
    "udim_tiles": {
      "1001": { "prompt": "...", "type": "diffuse" }
    }
  }
}
```

---

**Archived on**: 2026-01-20  
**Last working commit**: 7100ba1  
**Reason**: Pipeline refocus on 2D sprite generation for 3D action games
