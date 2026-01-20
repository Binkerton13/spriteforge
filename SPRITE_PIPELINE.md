# 2D Sprite Pipeline for 3D Action Games

## Overview

This pipeline generates **game-ready 2D sprites** with a 3D action game aesthetic (Diablo, Path of Exile, Hades style), not RPG Maker top-down sprites. The system uses AI to enhance 3D-rendered frames, creating professional-quality sprites that mimic 3D game models.

## 🎯 Target Aesthetic

**Goal**: Photo-realistic or stylized sprites that look like 3D characters
- ✅ Isometric or 3/4 view perspective
- ✅ Smooth animations (16-30 fps)
- ✅ Multiple camera angles with depth perception
- ✅ High resolution (256x256 to 1024x1024)
- ✅ Consistent character appearance across all frames
- ✅ Baked shadows and lighting
- ❌ NOT: Simple top-down RPG Maker style
- ❌ NOT: Low-frame pixel art

## 📊 Pipeline Flow

```
Input Mesh (FBX/OBJ)
    ↓
UniRig (Auto-rig skeleton + skinning)
    ↓
HY-Motion (Generate animations from text prompts)
    ↓
Blender (Render animation frames with control maps)
    ├─ OpenPose skeleton
    ├─ Depth map
    ├─ Normal map
    ├─ Silhouette mask
    └─ Canny edges
    ↓
ComfyUI (AI-enhance frames)
    ├─ AnimateDiff (temporal consistency)
    ├─ IP-Adapter (character consistency)
    └─ Multi-ControlNet (shape preservation)
    ↓
Post-Processing
    ├─ Background removal (alpha channel)
    ├─ Shadow baking
    └─ Sprite sheet generation
    ↓
Output: Game-ready sprite sheets
```

## 🚀 Quick Start

### 1. Prepare Your Mesh

Upload a clean character mesh (FBX or OBJ):
```bash
/workspace/ProjectName/0_input/meshes/character.fbx
```

**Mesh Requirements:**
- Clean topology (no holes, overlapping faces)
- 10K-80K vertices (best results: 30K-50K)
- Humanoid proportions (for UniRig auto-rigging)
- Optional: Pre-rigged meshes also supported

### 2. (Optional) Add Reference Images

For consistent character style, upload 1-3 reference images:
```bash
/workspace/ProjectName/0_input/references/
    ├─ face_reference.png      # Facial features, hair style
    ├─ costume_reference.png   # Clothing, accessories
    └─ style_reference.png     # Overall art style
```

**Reference Image Tips:**
- Clear, well-lit photos or artwork
- Same character style you want in sprites
- Multiple angles help IP-Adapter understand 3D form

### 3. Configure Sprite Settings

Edit `pipeline/config.json`:

```json
{
  "mesh_type": "skeletal",
  "sprite_generation": {
    "enabled": true,
    "quality_preset": "balanced",
    "camera_preset": "isometric_8way",
    "character_prompt": "female warrior, long red hair, leather armor, detailed features",
    "style_tags": ["stylized realistic", "hand-painted texture"],
    "reference_images": [
      "0_input/references/face_reference.png",
      "0_input/references/costume_reference.png"
    ],
    "resolution": [512, 512],
    "fps": 16,
    "frame_sample_rate": 1
  },
  "animations": {
    "selections": [
      {"name": "idle"},
      {"name": "walk_cycle"},
      {"name": "run"},
      {"name": "attack"}
    ]
  }
}
```

### 4. Run Pipeline

```bash
cd /workspace/pipeline
python run_pipeline.py /workspace/ProjectName
```

### 5. Get Outputs

```
/workspace/ProjectName/5_sprites/
├─ idle_NE.png, idle_SE.png, ...     # Individual sprites
├─ walk_NE.png, walk_SE.png, ...
├─ sprite_sheets/
│   ├─ character_idle_8dir.png       # All directions in one sheet
│   ├─ character_walk_8dir.png
│   └─ character_atlas.png           # Master atlas
└─ metadata/
    ├─ sprite_data.json              # Frame timings, pivots
    └─ animation_config.json
```

## 🎨 Camera Presets

### Isometric 4-Way
Classic action RPG perspective (Diablo):
- **Angles**: NE, SE, SW, NW (4 directions)
- **Elevation**: 30°
- **Best for**: Fast prototyping, simple movement

### Isometric 8-Way (Recommended)
Full 8-direction movement:
- **Angles**: N, NE, E, SE, S, SW, W, NW
- **Elevation**: 30°
- **Best for**: Action games with free movement

### 3/4 View 8-Way
Slightly lower angle for more detail:
- **Angles**: 8 directions
- **Elevation**: 25°
- **Best for**: Character detail focus

### Side-Scroller 2-Way
Traditional platformer view:
- **Angles**: Left, Right
- **Elevation**: 0°
- **Best for**: 2D platformers

### Custom Angles
Define your own in `sprite_generation_enhanced.json`:
```json
"custom_preset": {
  "angles": [
    {"azimuth": 30, "elevation": 35, "label": "Custom1"},
    {"azimuth": 150, "elevation": 35, "label": "Custom2"}
  ]
}
```

## ⚙️ Quality Presets

### Fast Prototype
- **Resolution**: 256x256
- **FPS**: 12
- **Steps**: 4 (SDXL-Turbo)
- **Speed**: ~2-3 seconds per frame
- **Use**: Rapid iteration, testing

### Balanced (Recommended)
- **Resolution**: 512x512
- **FPS**: 16
- **Steps**: 8 (SDXL-Lightning)
- **Speed**: ~5-8 seconds per frame
- **Use**: Production-ready sprites

### High Quality
- **Resolution**: 512x512
- **FPS**: 24
- **Steps**: 20 (SDXL 1.0)
- **Speed**: ~15-20 seconds per frame
- **Use**: Hero characters, cinematics

### Ultra Quality
- **Resolution**: 1024x1024
- **FPS**: 30
- **Steps**: 30 (SDXL 1.0)
- **Speed**: ~30-40 seconds per frame
- **Use**: Marketing materials, closeups

## 🧠 AI Models Required

### Core Models (Essential)

**SDXL Base Models** (Choose one):
- `sdxl_base_1.0.safetensors` (High quality, slow)
- `sdxl_lightning_4step.safetensors` (Fast, good quality)
- `sdxl_turbo.safetensors` (Very fast, lower quality)

**ControlNet Models** (All SD1.5):
- `control_v11p_sd15_openpose.pth` - Pose preservation
- `control_v11f1p_sd15_depth.pth` - Shape/volume
- `control_v11p_sd15_normalbae.pth` - Surface details
- `control_v11p_sd15_canny.pth` - Edge definition (optional)

### Enhanced Models (Highly Recommended)

**AnimateDiff**:
- `v3_sd15_mm.ckpt` - Temporal consistency
- Purpose: Prevents flickering, maintains style across frames

**IP-Adapter**:
- `ip-adapter-faceid-plusv2_sd15.bin` - Facial consistency
- `ip-adapter-plus_sd15.bin` - Full body style matching
- Purpose: Maintains character appearance using reference images

### Optional Enhancements

**Background Removal**:
- `u2net.onnx` (Rembg model) - Automatic alpha channel

**Upscaling**:
- `RealESRGAN_x4plus.pth` - 4x upscaling for high-res sprites

## 📝 Character Prompt Engineering

### Basic Structure
```
{character_type}, {physical_features}, {clothing}, {style_modifiers}
```

### Example Prompts

**Female Warrior**:
```
female warrior, long flowing red hair, blue eyes, athletic build,
leather armor with gold trim, detailed facial features, 
confident pose, game sprite, stylized realistic, 
hand-painted texture, consistent lighting
```

**Male Mage**:
```
male wizard, grey beard, mystical staff, flowing blue robes with arcane symbols,
wise expression, elderly but powerful, magical aura,
game sprite, cel-shaded style, fantasy art
```

**Elf Ranger**:
```
elf ranger, blonde hair, pointed ears, green cloak, bow and quiver,
agile build, forest guardian aesthetic, nature-inspired details,
game sprite, painterly style, detailed equipment
```

### Prompt Tips

**DO Include**:
- Specific physical features (hair color, build, facial features)
- Detailed clothing/armor description
- Pose/attitude descriptors
- Style tags ("game sprite", "isometric view")
- Consistency terms ("detailed features", "professional quality")

**DON'T Include**:
- Multiple outfits (causes inconsistency)
- Conflicting styles ("realistic" + "pixel art")
- Background descriptions (handled separately)
- Vague terms ("cool", "awesome")

### Style Tags

**Stylized Realistic**:
- `stylized realistic, hand-painted texture, detailed features`
- Best for: Modern action RPGs

**Cel-Shaded**:
- `cel-shaded, clean outlines, flat colors with gradients`
- Best for: Anime-style games, Hades-like

**Painterly**:
- `painterly, brush strokes visible, artistic render`
- Best for: Fantasy RPGs, art-focused games

**Low-Poly Aesthetic**:
- `low poly aesthetic, geometric, clean shapes`
- Best for: Indie games, stylized look

## 🎮 Game Engine Integration

### Unity

```csharp
// Import sprite sheet as Texture2D
Texture2D spriteSheet = Resources.Load<Texture2D>("character_walk_8dir");

// Load metadata
SpriteMetadata metadata = JsonUtility.FromJson<SpriteMetadata>(
    Resources.Load<TextAsset>("sprite_data").text
);

// Create sprite array
Sprite[] walkSprites = new Sprite[8];
for (int i = 0; i < 8; i++) {
    walkSprites[i] = Sprite.Create(
        spriteSheet,
        metadata.frames[i].rect,
        metadata.frames[i].pivot
    );
}
```

### Godot

```gdscript
# Load sprite sheet
var sprite_sheet = load("res://sprites/character_walk_8dir.png")
var metadata = load("res://sprites/sprite_data.json").parse()

# Setup animated sprite
$AnimatedSprite.frames = SpriteFrames.new()
for anim in metadata.animations:
    $AnimatedSprite.frames.add_animation(anim.name)
    $AnimatedSprite.frames.set_animation_speed(anim.name, anim.fps)
    for frame in anim.frames:
        var atlas_texture = AtlasTexture.new()
        atlas_texture.atlas = sprite_sheet
        atlas_texture.region = frame.rect
        $AnimatedSprite.frames.add_frame(anim.name, atlas_texture)
```

### Unreal Engine

```cpp
// Load sprite texture
UTexture2D* SpriteSheet = LoadObject<UTexture2D>(
    nullptr, TEXT("/Game/Sprites/character_walk_8dir")
);

// Create paper sprite
UPaperSprite* WalkSprite = NewObject<UPaperSprite>();
WalkSprite->SetSourceTexture(SpriteSheet);
WalkSprite->SetSpriteGeometry(FSpriteGeometryCollection());
```

## 🔧 Advanced Configuration

### Multi-ControlNet Weights

Fine-tune how much each ControlNet influences the output:

```json
"controlnet_config": {
  "openpose": {
    "weight": 0.9,  // High: Strict pose adherence
    "start": 0.0,
    "end": 1.0
  },
  "depth": {
    "weight": 0.7,  // Medium-high: Preserve 3D shape
    "start": 0.0,
    "end": 0.8      // End early to allow style freedom
  },
  "normal": {
    "weight": 0.5,  // Medium: Add surface details
    "start": 0.0,
    "end": 0.6
  }
}
```

**Weight Guidelines**:
- **0.8-1.0**: Very strict control (for poses, critical shapes)
- **0.5-0.7**: Balanced control (for depth, normals)
- **0.2-0.4**: Light guidance (for edges, subtle details)

### AnimateDiff Settings

Control temporal consistency:

```json
"animatediff_config": {
  "context_length": 16,    // Process 16 frames at once
  "context_overlap": 8,    // 50% overlap for smoothness
  "motion_scale": 0.5      // 0.0=static, 1.0=very dynamic
}
```

**Motion Scale**:
- **0.3-0.5**: Subtle motion (idle, breathing)
- **0.5-0.7**: Normal motion (walk, actions)
- **0.7-1.0**: Dynamic motion (run, combat)

### IP-Adapter Strength

Control how much reference images influence style:

```json
"ip_adapter_config": {
  "weight": 0.7,    // 0.0=ignore refs, 1.0=match exactly
  "start": 0.0,
  "end": 1.0
}
```

**Weight Guidelines**:
- **0.6-0.8**: Balanced (recommended)
- **0.8-1.0**: Very consistent (may limit variety)
- **0.3-0.5**: Loose inspiration (more creative freedom)

## 📊 Performance Optimization

### Speed vs Quality Trade-offs

| Setting | Speed | Quality | Best For |
|---------|-------|---------|----------|
| SDXL-Turbo + 4 steps | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Prototyping |
| SDXL-Lightning + 8 steps | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Production |
| SDXL 1.0 + 20 steps | ⚡⚡ | ⭐⭐⭐⭐⭐ | Hero assets |
| SDXL 1.0 + 30 steps | ⚡ | ⭐⭐⭐⭐⭐ | Marketing |

### VRAM Requirements

| Configuration | VRAM | Notes |
|--------------|------|-------|
| Basic (OpenPose + Depth) | 8GB | Entry level |
| Standard (+ AnimateDiff) | 12GB | Recommended |
| Enhanced (+ IP-Adapter) | 16GB | Professional |
| Ultra (All + 1024px) | 24GB | High-end |

### Batch Processing

Generate multiple angles simultaneously:

```python
# In generate_sprites.py
batch_size = 4  # Process 4 angles at once
for batch in chunks(camera_angles, batch_size):
    render_batch(batch)
    enhance_batch(batch)
```

## 🐛 Troubleshooting

### Issue: Inconsistent Character Appearance

**Symptoms**: Character changes outfit, face, or style between frames

**Solutions**:
1. **Add reference images**: IP-Adapter needs visual consistency guide
2. **Increase IP-Adapter weight**: Try 0.8-0.9 instead of 0.7
3. **Use AnimateDiff**: Ensures temporal consistency
4. **Strengthen negative prompt**: Add "different outfit, face change"

### Issue: Flickering/Jittering

**Symptoms**: Sprite flickers or changes style frame-to-frame

**Solutions**:
1. **Enable AnimateDiff**: Critical for temporal consistency
2. **Increase context overlap**: Try 75% instead of 50%
3. **Lower motion scale**: Reduce to 0.3-0.4 for subtle animations
4. **Use consistent seed**: Same seed per animation sequence

### Issue: Lost 3D Shape

**Symptoms**: Sprite looks flat, depth information lost

**Solutions**:
1. **Increase depth ControlNet weight**: Try 0.8-0.9
2. **Add normal map ControlNet**: Preserves surface details
3. **Bake shadows**: Enable shadow baking in post-processing
4. **Check Blender render**: Verify depth map is rendering correctly

### Issue: Edges Too Soft

**Symptoms**: Blurry edges, poor sprite readability

**Solutions**:
1. **Add Canny ControlNet**: Preserves sharp edges
2. **Enable edge enhancement**: Sharpen filter in post-processing
3. **Increase resolution**: Try 512x512 or 1024x1024
4. **Use cel-shaded style**: Better defined edges

### Issue: Slow Generation

**Symptoms**: Taking too long per frame

**Solutions**:
1. **Switch to SDXL-Lightning**: 8 steps instead of 20
2. **Reduce resolution**: 256x256 for prototyping
3. **Disable optional ControlNets**: Skip Canny, Normal
4. **Lower frame sample rate**: Every 2nd frame instead of all
5. **Reduce camera angles**: 4-way instead of 8-way

## 📚 Further Reading

- [UniRig Documentation](UNIRIG_HYMOTION_INTEGRATION.md) - Rigging system
- [HY-Motion Guide](UNIRIG_HYMOTION_INTEGRATION.md#how-hy-motion-integration-works) - Animation generation
- [ComfyUI ControlNet](https://github.com/Mikubill/sd-webui-controlnet) - ControlNet usage
- [AnimateDiff](https://github.com/continue-revolution/sd-webui-animatediff) - Temporal consistency
- [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter) - Style consistency

## 🎯 Example Workflows

### Workflow 1: Fast Iteration

```json
{
  "quality_preset": "fast_prototype",
  "camera_preset": "isometric_4way",
  "resolution": [256, 256],
  "controlnet": ["openpose", "depth"],
  "skip_animatediff": true
}
```

**Result**: Quick sprites for testing gameplay

### Workflow 2: Production Quality

```json
{
  "quality_preset": "balanced",
  "camera_preset": "isometric_8way",
  "resolution": [512, 512],
  "controlnet": ["openpose", "depth", "normal"],
  "animatediff": true,
  "ip_adapter": true,
  "reference_images": ["face.png", "costume.png"]
}
```

**Result**: Professional game-ready sprites

### Workflow 3: Hero Character

```json
{
  "quality_preset": "ultra_quality",
  "camera_preset": "three_quarter_8way",
  "resolution": [1024, 1024],
  "controlnet": ["openpose", "depth", "normal", "canny"],
  "animatediff": true,
  "ip_adapter": true,
  "reference_images": ["hero_face.png", "hero_costume.png", "hero_style.png"],
  "post_processing": {
    "upscale": "RealESRGAN_x4"
  }
}
```

**Result**: Ultra high-quality sprite for main character

---

**Last Updated**: 2026-01-20  
**Pipeline Version**: 2.0  
**Focus**: 3D Action Game Sprites (Isometric/3D Perspective)
