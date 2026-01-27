SpriteForge Frontend Component Map
Version 1.0 — UI Architecture Blueprint  
This document defines the full component hierarchy for the SpriteForge frontend (React/Vue).

🧱 1. Overview
SpriteForge’s frontend is organized into five primary domains:

Motion — motion presets, generation, preview

Sprites — sprite generation, styles, sheets

Workflows — workflow editor, nodes, validation

Models — model management, selection, upload

Projects — project save/load, metadata, assets

Each domain maps directly to backend API routes and has its own component cluster and state store.

The UI is built on a shared layout system with reusable primitives (panels, modals, tables, inspectors).

🧭 2. High‑Level Architecture Diagram
mermaid
flowchart TD

    AppLayout --> Sidebar
    AppLayout --> TopBar
    AppLayout --> Router

    Router --> MotionPage
    Router --> SpritePage
    Router --> WorkflowPage
    Router --> ModelPage
    Router --> ProjectPage

    MotionPage --> MotionPresetList
    MotionPage --> MotionSettings
    MotionPage --> MotionPreviewVideo
    MotionPage --> MotionFrameStrip

    SpritePage --> SpriteStyleSelector
    SpritePage --> SpriteModelSelector
    SpritePage --> SpriteGenerationSettings
    SpritePage --> SpriteFrameGrid
    SpritePage --> SpriteSheetAssembler

    WorkflowPage --> WorkflowList
    WorkflowPage --> WorkflowEditor
    WorkflowPage --> WorkflowNodeInspector

    ModelPage --> ModelTypeTabs
    ModelPage --> ModelList
    ModelPage --> ModelActiveSelector

    ProjectPage --> ProjectList
    ProjectPage --> ProjectMetadataEditor
    ProjectPage --> ProjectAssetList
🧱 3. Global Layout Components
Layout/
AppLayout — main shell (sidebar + header + content)

Sidebar — navigation between domains

TopBar — active model, project, status indicators

Panel — reusable container with title + actions

Modal — generic modal

Tabs — generic tab component

DataTable — reusable table

FilePicker — integrated with backend file browser

🎬 4. Motion Components
Folder: Motion/  
Backend Routes: /api/motion/*, /api/preview/*

Components
MotionPage

MotionPresetList

MotionSettings

MotionGenerateButton

MotionPreviewVideo

MotionFrameStrip

MotionToSpriteButton

State Store: motion.js
selectedPreset

seed

videoPath

framesPath

🎨 5. Sprite Components
Folder: Sprites/  
Backend Routes: /api/sprites/*, /api/styles/*, /api/models/*

Components
SpritePage

SpriteStyleSelector

SpriteModelSelector

SpriteGenerationSettings

SpriteGenerateButton

SpriteFrameGrid

SpriteSheetAssembler

SpriteSheetPreview

State Store: sprites.js
selectedStyle

selectedModel

frames

sheetPath

🧩 6. Workflow Components
Folder: Workflows/  
Backend Routes: /api/workflows/*

Components
WorkflowPage

WorkflowList

WorkflowEditor (JSON or node‑graph)

WorkflowNodeList

WorkflowNodeInspector

WorkflowValidator

WorkflowSaveButton

State Store: workflows.js
workflowList

workflowJSON

selectedNode

validationResults

🧬 7. Model Components
Folder: Models/  
Backend Routes: /api/models/*

Components
ModelPage

ModelTypeTabs

ModelList

ModelActiveSelector

ModelUploadButton

ModelCard

State Store: models.js
activeModel

modelsByType

🗂️ 8. Project Components
Folder: Projects/  
Backend Routes: /api/project/*

Components
ProjectPage

ProjectList

ProjectCreateModal

ProjectSaveButton

ProjectLoadButton

ProjectMetadataEditor

ProjectAssetList

State Store: projects.js
currentProject

metadata

assets

⚙️ 9. Batch Processing Components
Folder: Batch/  
Backend Routes: /api/batch/*

Components
BatchPage

BatchCreateForm

BatchRunButton

BatchStatusPanel

BatchResultList

State Store: batch.js
batchId

batchStatus

batchResults

📁 10. File Browser Integration
Folder: FileBrowser/  
Backend Routes: /api/files/list

Components
FileBrowserModal

FileList

FilePreview

FileUpload

FileDelete

State Store: files.js
directory

selectedFile

🔌 11. API Client Layer
Folder: api/

Each file wraps backend routes:

motion.js

sprites.js

workflows.js

models.js

projects.js

batch.js

files.js

Example:

js
export function generateMotion(preset, seed) {
  return fetch('/api/motion/generate', {
    method: 'POST',
    body: JSON.stringify({ preset, seed })
  })
}

🧠 12. State Management
React:
Zustand or Jotai recommended

Vue:
Pinia recommended

Folder: stores/

Each domain has its own store:

Code
stores/
    motion.js
    sprites.js
    workflows.js
    models.js
    projects.js
    batch.js
    files.js

📦 13. Frontend Folder Structure
Code
pipeline/gui/frontend/
    src/
        Layout/
        Motion/
        Sprites/
        Workflows/
        Models/
        Projects/
        Batch/
        FileBrowser/
        api/
        stores/
        main.js / main.jsx
        App.vue / App.jsx
    index.html
    package.json
    vite.config.js

🧩 14. Routing Map
Code
/motion        → MotionPage
/sprites       → SpritePage
/workflows     → WorkflowPage
/models        → ModelPage
/projects      → ProjectPage
/batch         → BatchPage

🧭 15. Future Extensions
Node‑graph workflow editor

Live preview panel

Asset inspector

Drag‑and‑drop sheet builder

Model tagging + metadata

Project export/import