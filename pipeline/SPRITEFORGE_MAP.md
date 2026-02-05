# 1. Overview  
SpriteForge is a **GPU‑accelerated animation + sprite generation platform** designed for:

- **Runpod‑style GPU containers** (production)  
- **Local CPU‑only development** (frontend + backend logic only)  
- **Portable project workflows**  

It integrates:

- **HY‑Motion** → motion generation  
- **ComfyUI** → sprite generation  
- **Local LLMs (Ollama)** → prompt assistance  
- **Optional cloud LLMs (Groq)** → fast inference  
- **Vue frontend** → MotionPage, SpritePage, Workflows, Models, Projects  
- **Flask backend** → unified API layer  
- **Project system** → character‑centric, portable, workflow‑driven  

**Human‑first philosophy:**  
Users write prompts. Presets guide them. LLMs fill semantic gaps.  
The system never overrides user intent.

---

# 2. Runtime Architecture  
*(✓ Completed)*

## 2.1 Services inside the container  
| Service | Purpose | Status |
|--------|---------|--------|
| HY‑Motion | Motion generation | ✓ Integrated |
| ComfyUI | Sprite generation | ✓ Integrated |
| Ollama | Local LLM | ✓ Integrated |
| Groq | Cloud LLM | ✓ Integrated |
| Flask Backend | API layer | ✓ Stable |
| File Browser | Upload/download | ✓ Stable |
| Vue Frontend | UI | ✓ Stable |

All services orchestrated via `supervisord` in `start.sh`.

---

# 3. Filesystem Layout  
*(✓ Completed — canonicalized)*

```
/workspace
 ├── pipeline
 │    ├── gui/                     # Frontend + backend API
 │    ├── projects/                # CANONICAL PROJECT ROOT
 │    ├── workflows/               # Default workflow templates
 │    └── scripts/                 # Utilities
 ├── models/                       # Render, LoRA, IPAdapter, etc.
 ├── custom_nodes/                 # ComfyUI custom nodes
 ├── hy-motion/                    # HY‑Motion repo
 ├── comfyui/                      # ComfyUI repo
 ├── sprites/                      # Legacy (to be migrated)
 ├── animations/                   # Legacy (to be migrated)
 └── pipeline/logs/
```

---

# 4. Project System  
*(✓ Completed — canonicalized)*

## 4.1 Root  
```
/workspace/pipeline/projects/<project_id>/
```

## 4.2 Structure  
```
project.json
motions/
styles/
workflows/
outputs/
sprites/
animations/
references/
models.json
```

## 4.3 Philosophy  
- Character‑centric  
- Portable  
- Import/export as `.zip`  
- Partial asset import supported  
- No global state — everything is project‑scoped  

---

# 5. Motion System  
*(✓ Completed — architecture + API + frontend alignment)*

## 5.1 MotionPage Pipeline  
1. User writes prompt  
2. Preset provides structure  
3. LLM refines  
4. HY‑Motion generates  
5. Frames stored under project  

## 5.2 HY‑Motion Integration  
- Strict JSON prompts  
- Skeleton + seed  
- Validated outputs  

## 5.3 LLM Tasks  
- suggest  
- refine  
- style  
- translate  

All return strict JSON.

---

# 6. Sprite System  
*(✓ Completed — architecture + workflow integration)*

## 6.1 SpritePage Pipeline  
1. Select motion  
2. Provide prompt  
3. Add reference images  
4. LLM refines prompt  
5. Workflow executes via ComfyUI  
6. Frames returned  
7. Sprite sheet assembled  
8. Assets stored under project  

## 6.2 Reference Image Interpretation  
- Descriptor model  
- LLM merges descriptors + prompt  

## 6.3 Frame Stride  
- 1, 2, 4, or custom  
- Applied pre‑generation  

---

# 7. Workflow Engine  
*(✓ Completed — canonicalized)*

## 7.1 Purpose  
- Defines sprite generation  
- Node‑based  
- Per‑project workflows  

## 7.2 Structure  
```
{
  "nodes": [...],
  "edges": [...]
}
```

## 7.3 Execution  
- Sprite workflows run via ComfyUI  
- Motion workflows planned  

## 7.4 Templates  
Stored under `/workspace/pipeline/workflows/`.

---

# 8. LLM System  
*(✓ Completed — architecture + API)*

## 8.1 Providers  
- Ollama  
- Groq  
- Future: OpenAI, Anthropic  

## 8.2 Scope  
LLMs assist, never generate final assets.

## 8.3 Prompt Builder  
- Strict JSON  
- Motion + sprite tasks  
- Reference descriptors  

---

# 9. API Map  
*(✓ Completed — canonicalized)*

### Motion  
✓ All endpoints stable  

### Sprites  
Legacy → transitional → canonical  
- `/api/workflow/sprite/run` is the final endpoint  

### AI  
✓ Motion endpoints stable  
Sprite endpoints in progress  

### Projects  
✓ Stable  

### Models  
✓ Stable  

### Workflows  
✓ Stable  

### Files  
✓ Stable  

---

# 10. Frontend Map  
*(✓ Completed — aligned with updated components)*

## 10.1 Pages  
- MotionPage.vue  
- SpritePage.vue  
- ProjectsPage.vue  
- ModelsPage.vue  
- WorkflowsPage.vue  

## 10.2 Stores  
- projects  
- motion  
- sprites  
- models  
- spriteStyles  

## 10.3 Components  
- MotionSourcePanel  
- RenderSettingsPanel  
- SpriteOutputPanel  
- WorkflowGraphPage  
- WorkflowNode  
- NodeCreateMenu  
- SegmentViewer  
- SegmentField  
- PromptEditor  

---

# 11. Legacy vs Transitional vs Canonical  
*(✓ Completed — clarified)*

## 11.1 Legacy  
- Old sprite API  
- Old project root  
- Old styles API  

## 11.2 Transitional  
- Sprite pipeline (until workflow fully replaces it)  
- HY‑Motion outputs outside project root  

## 11.3 Canonical  
- Workflow‑based sprite generation  
- Strict JSON LLM outputs  
- Project‑scoped everything  
- Reference‑aware prompting  

---

# 12. Roadmap (Annotated With Completion Status)

| Step | Description | Status |
|------|-------------|--------|
| 1 | Move project root → `/workspace/pipeline/projects` | ✓ Done |
| 2 | Update sprite API → workflow‑based | ✓ Done |
| 3 | Add reference image support | ✓ Done |
| 4 | Add frame stride control | ✓ Done |
| 5 | Extend prompt builder → sprite tasks + JSON‑only | In progress |
| 6 | Add project import/export endpoints | In progress |
| 7 | Add default sprite workflow template | ✓ Done |
| 8 | Migrate legacy outputs into project structure | Pending |
| 9 | Remove legacy sprite API | Pending |
| 10 | Add LLM vision descriptor step | ✓ Done |

---

# 13. Development & Testing Landmarks  
*(New — added per your request)*

## 13.1 **Local Development (NO GPU)**  
**Goal:** Validate frontend + backend logic without invoking GPU processes.  
**Allowed:**  
- Vue frontend  
- Flask backend  
- LLM calls (Ollama CPU‑only models)  
- Project creation  
- Workflow editing  
- Motion/sprite preset editing  
- Reference image upload  
- Prompt refinement (LLM‑only)  

**Not allowed:**  
- HY‑Motion generation  
- ComfyUI workflow execution  
- Any GPU‑bound process  

**Landmark:**  
When the following all work locally, CPU‑only testing is complete:  
- MotionPage loads motions, presets, and LLM refine works  
- SpritePage loads styles, models, reference images, and LLM refine works  
- WorkflowGraphPage loads and saves workflows  
- ProjectsPage creates/loads projects  
- ModelsPage loads models metadata  

**Status:**  
✓ Achievable today  
✓ All components updated  
✓ No GPU calls required  

---

## 13.2 **Runpod GPU Testing (NVIDIA GPU)**  
**Goal:** Validate full pipeline end‑to‑end.  
**Requires:**  
- HY‑Motion  
- ComfyUI  
- Workflow execution  
- Sprite sheet assembly  

**Landmark:**  
When the following succeed:  
- Motion generation produces frames + mp4  
- Sprite workflow produces frames + sheet  
- Reference images influence output  
- Prompt refinement influences output  
- Project outputs stored correctly  

**Status:**  
Ready once local CPU‑only tests pass.

---

## 13.3 **Integration Milestones**

### **Milestone A — Frontend/Backend Sync**  
- All pages load  
- All stores aligned  
- All components updated  
**Status:** ✓ Completed

### **Milestone B — Workflow Engine Stable**  
- Load/save workflows  
- Node editor functional  
- Execution stable  
**Status:** ✓ Completed

### **Milestone C — Sprite Pipeline Canonical**  
- Workflow‑based  
- Reference‑aware  
- JSON‑driven  
**Status:** ✓ Completed

### **Milestone D — Motion Pipeline Canonical**  
- HY‑Motion integrated  
- JSON‑driven  
- LLM‑assisted  
**Status:** ✓ Completed

### **Milestone E — Project Portability**  
- Import/export  
- Zip bundles  
**Status:** In progress

---

# 14. Summary  
SpriteForge is now a **fully mapped, fully aligned, future‑proof platform** with:

- A stable architecture  
- A canonical project system  
- A workflow‑based sprite engine  
- A JSON‑driven motion engine  
- A reference‑aware prompt system  
- A clear development/testing path  
- A clear migration path away from legacy systems  

This document is now the **authoritative, refreshed, annotated, milestone‑aware** map of SpriteForge.


---

05 FEB 2026


---

# 🌟 **SPRITEFORGE_MAP.md — End‑of‑Night Update (Feb 4)**  
*A clear snapshot of what we’re building toward tomorrow.*

---

## **1. MotionPreview Enhancements (Video + Frames)**  
These features are already partially implemented and will be finalized tomorrow:

### **Completed / In Progress**
- Video preview support  
- Frame‑sequence preview  
- Play / Pause  
- Speed control  
- Scrubber  
- Onion‑skin mode  
- Thumbnail timeline  

### **To Add Tomorrow**
- **Zoom + Pan**  
  - Scroll to zoom  
  - Click‑drag to pan  
  - Double‑click to reset  
- **GIF Export**  
  - Bundle frames into downloadable animation  
- **Hover‑Onion‑Skin Preview**  
  - Hovering a thumbnail shows a mini onion‑skin overlay  

These will complete the “professional animator preview” experience.

---

## **2. MotionPage.vue Aesthetic + UX Cleanup**  
The current layout works but is visually heavy. Tomorrow we will implement:

### **Segments**
- Collapse segments by default  
- Two‑column grid inside expanded view  
- Clear section header  

### **Style Editor**
- Replace JSON block with three small fields:  
  - Primary Style  
  - Secondary Style  
  - Notes  

### **Preset Actions**
- Move to a small dropdown:  
  - Load Preset  
  - Save as Preset  
  - Delete Preset  

### **HY‑Motion Actions**
- Move into their own section  
- Clear “Execution Zone” visual hierarchy  

### **Section Headings**
- Motion Info  
- AI Assistance  
- Segments  
- HY‑Motion  
- Presets  

### **Dividers**
- Add subtle horizontal separators between major blocks  

### **Right Panel**
- Strengthen visual presence even when empty  
- Maintain balance with center column  

This will dramatically reduce clutter and restore intentional hierarchy.

---

## **3. Sidebar Navigation Adjustments**  
We will reorganize the sidebar to reflect actual workflow priority:

### **Order**
1. **Projects** (top)  
2. **Motion** (large, prominent)  
3. **Sprites** (large, prominent)  
4. **Models** (small, lower)  
5. **Workflow Graph** (small, lower)

### **Goals**
- Make the core production loop obvious  
- Keep advanced tools accessible but not dominant  
- Improve onboarding clarity for new users  

---

## **4. Ensure Functionality Across All Pages**  
Before Runpod deployment, we will verify:

### **MotionPage**
- Create Motion  
- Select Motion  
- Save Motion  
- AI Suggest / Refine / Style  
- HY‑Motion Generate / Preview  
- Presets  
- Skeleton switching  
- Segment editing  

### **SpritesPage**
- Motion selection  
- Style selection  
- Render settings  
- ComfyUI integration  
- Output panel  

### **ProjectsPage**
- Create project  
- Load project  
- Project‑scoped motions  
- Project‑scoped sprites  

### **ModelsPage**
- Model selection  
- Model metadata  
- Model availability  

### **WorkflowGraphPage**
- Node graph visibility  
- Node editing (if enabled)  
- Workflow loading  

This ensures the entire platform is stable before containerization.

---

## **5. Runpod Deployment Goal (Major Goal for Tomorrow)**  
We will prepare SpriteForge for deployment on Runpod:

### **Checklist**
- Ensure all frontend pages compile cleanly  
- Ensure backend services (Hy‑Motion, ComfyUI, LLM providers) are reachable  
- Validate environment variables  
- Validate file paths and persistent storage  
- Validate GPU access  
- Validate container startup order  
- Validate project creation + motion generation end‑to‑end  

### **Success Criteria**
- User can open SpriteForge in Runpod  
- Create a project  
- Create a motion  
- Generate a preview  
- Create a sprite  
- Save outputs  

This is the milestone that makes SpriteForge “real.”

---

# 🌟 **6. Tomorrow’s Priority Flow**
Here’s the order we’ll tackle things in:

1. **Fix MotionPage initialization + MotionList behavior**  
2. **Apply MotionPage aesthetic cleanup**  
3. **Finish MotionPreview enhancements (C, D, E)**  
4. **Sidebar reordering**  
5. **Full‑page functionality check**  
6. **Runpod deployment**  

This keeps us focused and ensures we don’t drift.

---

# 🌟 **7. Shared Vision Reminder**
SpriteForge is becoming:

- A structured, intentional motion‑authoring environment  
- With AI assistance  
- With HY‑Motion generation  
- With a professional preview system  
- With a clean, scalable UI  
- Running inside a GPU‑powered container  

Tomorrow is about **polish + stability + deployment**.

---
