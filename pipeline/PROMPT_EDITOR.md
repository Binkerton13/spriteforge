# Animation Prompt Editor & Tooltips

## Overview
Enhanced the animation system with per-animation prompt editing capabilities and comprehensive tooltips throughout the interface for better user guidance.

## Features Added

### 1. **Animation Prompt Editor**

#### Access
- Click "✏️ Edit Prompts" button next to "Clear All" in animation selection
- Only available when animations are selected
- Opens modal with all selected animations

#### Functionality
**Per-Animation Editing:**
- Edit all fields for each selected animation:
  - Motion (textarea, 3 rows)
  - Style (textarea, 2 rows)
  - Constraints (textarea, 2 rows)
  - Camera (text input)
  - Output (text input)

**Reset Feature:**
- 🔄 Reset button for each animation
- Reverts to original library defaults
- Immediate visual feedback

**Save Options:**
1. **💾 Save for Project**:
   - Stores in `{project}/pipeline/animation_overrides.json`
   - Project-specific customizations
   - Doesn't affect other projects
   - Merged with library defaults on load

2. **🌐 Save as Defaults**:
   - Updates `pipeline/hy_motion_prompts/prompt_library.json`
   - Global changes affecting all projects
   - Requires confirmation dialog
   - Updates library in memory immediately

#### Persistence
**Project Overrides:**
```json
{
  "locomotion:walk_cycle": {
    "motion": "Custom walk description...",
    "style": "Modified style...",
    "constraints": "Updated constraints...",
    "camera": "Locked, low angle.",
    "output": "60 frames, 30fps."
  }
}
```

**Loading Behavior:**
1. Project loaded → Load `animation_overrides.json`
2. Animation selected → Merge overrides with library
3. getSelectedAnimations() → Returns merged data
4. Override takes precedence over library defaults

### 2. **Comprehensive Tooltips**

#### Coverage
**Mesh Settings:**
- Mesh Type selector: "Determines which pipeline stages will run"
- Skeletal option: "Full pipeline with rigging and animation"
- Static option: "Texturing only"

**Texture Generation:**
- Positive Prompt: "Describe the desired texture appearance and details"
- Negative Prompt: "Specify what to avoid in the texture"
- Seed: "Random seed for reproducible results"

**Rigging:**
- Preset: "Choose bone structure preset for auto-rigging"
- Scale: "Uniform scale factor for the rig"
- Orientation: "World space orientation for the character"

**Animation:**
- Edit Prompts: "Edit prompts for selected animations"
- Clear All: "Deselect all animations"
- Mode selector: Explains library vs custom modes

**Sprite Generation:**
- Enable checkbox: "Generate 2D sprites from 3D animation frames"
- Frame Interval: "How often to capture frames from the animation"
- Camera Angles: "Hold Ctrl/Cmd to select multiple angles"
- Character Prompt: "Describe the character's appearance for sprite generation"
- Negative Prompt: "What to avoid in sprite appearance"
- Resolution: "Output resolution for each sprite"
- Sprite Sheet: "Combine all frames into a single sprite sheet"

#### Implementation
```html
<!-- Example tooltip usage -->
<label for="texturePrompt" title="Describe the desired texture appearance">
    Positive Prompt
</label>

<input type="number" 
       id="rigScale" 
       title="1.0 = original size">
```

### 3. **API Endpoints**

#### Get Animation Overrides
```
GET /api/projects/<project_name>/animation_overrides

Response:
{
  "status": "success",
  "overrides": {
    "locomotion:walk_cycle": {...},
    "idle:idle_breathing": {...}
  }
}
```

#### Save Animation Overrides
```
PUT /api/projects/<project_name>/animation_overrides

Body:
{
  "overrides": {
    "locomotion:walk_cycle": {
      "motion": "...",
      "style": "...",
      ...
    }
  }
}

Response:
{
  "status": "success",
  "message": "Saved 2 animation overrides",
  "total_overrides": 5
}
```

#### Update Global Library
```
PUT /api/animation_library/update

Body:
{
  "updates": {
    "locomotion:walk_cycle": {
      "motion": "...",
      "style": "..."
    }
  }
}

Response:
{
  "status": "success",
  "message": "Updated 1 animations in library"
}
```

## User Workflows

### Workflow 1: Customize Animations for Project
1. Select project
2. Choose animations from library (e.g., walk_cycle, run_cycle)
3. Click "✏️ Edit Prompts"
4. Modify prompts for specific project needs
5. Click "💾 Save for Project"
6. Prompts saved in project folder only

### Workflow 2: Update Library Defaults
1. Select animations
2. Click "✏️ Edit Prompts"
3. Edit prompts to improve defaults
4. Click "🌐 Save as Defaults"
5. Confirm global update
6. All future projects use new defaults

### Workflow 3: Reset to Defaults
1. Open prompt editor
2. See customized prompts
3. Click 🔄 on any animation
4. Prompts revert to library original
5. Save changes

## Technical Details

### JavaScript Functions

**loadAnimationOverrides()**
- Called when project loads
- Fetches project-specific overrides
- Stores in `projectAnimationOverrides` object

**getSelectedAnimations()**
- Returns array of selected animations
- Merges library defaults with project overrides
- Override fields take precedence

**openPromptEditor()**
- Gets selected animations
- Creates editor UI for each
- Populates with current values (merged)

**savePromptOverrides(scope)**
- Collects edited values
- Saves to project file or global library
- Updates local state

**resetPromptToDefault(index)**
- Reverts single animation to library original
- Updates form fields
- Visual feedback

### File Structure
```
workspace/
├── projects/
│   └── MyProject/
│       └── pipeline/
│           ├── config.json
│           └── animation_overrides.json    # NEW: Project overrides
│
└── pipeline/
    └── hy_motion_prompts/
        └── prompt_library.json             # Global library
```

### Override Merging Logic
```javascript
// Base prompt from library
const basePrompt = promptLibrary[category][name];

// Apply project override if exists
let prompt = { ...basePrompt };
if (projectAnimationOverrides[key]) {
    prompt = { ...prompt, ...projectAnimationOverrides[key] };
}
```

## Benefits

1. **Flexibility**: Customize animations per project without affecting library
2. **Experimentation**: Try different prompts without fear of breaking defaults
3. **Sharing**: Update library for team-wide improvements
4. **Clarity**: Tooltips guide users through all options
5. **Efficiency**: Batch edit multiple animations at once
6. **Reversibility**: Reset to defaults anytime

## UI/UX Improvements

**Visual Hierarchy:**
- Clear separation between project and global saves
- Color-coded save buttons (secondary vs primary)
- Individual animation cards with headers

**Accessibility:**
- Title attributes for screen readers
- Descriptive button labels
- Clear action confirmations

**Responsive Design:**
- Scrollable editor content (max 500px)
- Grid layout for compact fields
- Mobile-friendly tooltips

## Future Enhancements

- [ ] Bulk reset all overrides
- [ ] Export/import override presets
- [ ] Compare override vs library side-by-side
- [ ] Highlight which fields are overridden
- [ ] Version history for library updates
- [ ] Undo/redo for prompt editing
- [ ] Template system for common customizations
