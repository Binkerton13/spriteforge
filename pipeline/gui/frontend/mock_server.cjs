// ---------------------------------------------------------------------------
// SpriteForge Rich Mock Backend (Fantasy Theme)
// CommonJS Version (JS1)
// Location: pipeline/gui/frontend/mock_server.cjs
// ---------------------------------------------------------------------------

const express = require("express")
const cors = require("cors")
const { createProxyMiddleware } = require("http-proxy-middleware")

// ---------------------------------------------------------------------------
// CONFIG
// ---------------------------------------------------------------------------

// Mock server port
const PORT = 5001

// Real backend (only used if running; otherwise ignored)
const REAL_BACKEND = "http://localhost:5000"

// Workspace root (Linux-style, matches production)
const WORKSPACE_ROOT = "/workspace"

// Auto-detect backend availability
let backendOnline = false

async function checkBackend() {
  try {
    const res = await fetch(`${REAL_BACKEND}/api/health`)
    backendOnline = res.ok
  } catch {
    backendOnline = false
  }
}

// Check every 2 seconds
setInterval(checkBackend, 2000)
checkBackend()

// ---------------------------------------------------------------------------
// EXPRESS SETUP
// ---------------------------------------------------------------------------

const app = express()
app.use(cors())
app.use(express.json())

// ---------------------------------------------------------------------------
// EPHEMERAL IN-MEMORY MOCK DATA
// (Resets every time the mock server restarts)
// ---------------------------------------------------------------------------

const mockData = {
  motion: {
    skeletons: [
      {
        id: "human",
        name: "Human (Biped)",
        segments: ["overall", "head", "torso", "arms", "hands", "legs", "feet", "style"]
      },
      {
        id: "quadruped",
        name: "Quadruped",
        segments: ["overall", "head", "neck", "front_legs", "hind_legs", "tail", "style"]
      },
      {
        id: "chibi",
        name: "Stylized Chibi",
        segments: ["overall", "head", "torso", "arms", "legs", "exaggeration", "style"]
      }
    ],

    presets: {
      "sneaking-walk": {
        id: "sneaking-walk",
        name: "Sneaking Walk",
        skeleton: "human",
        motion: {
          overall: "Sneaking walk with cautious pacing.",
          head: "Slightly forward, scanning left to right.",
          torso: "Hunched, shoulders raised, elbows tucked.",
          arms: "Arms flexed at the elbow, subtle sway.",
          hands: "Relaxed but ready.",
          legs: "Gentle stepping motion, knees slightly bent.",
          feet: "Soft, deliberate foot placement.",
          style: "Stealthy, tense, controlled."
        },
        metadata: {
          seed: 12345,
          created: "2026-01-28T23:00:00Z",
          version: 1
        }
      }
    }
  },

  models: {
    checkpoints: [
      "dragonfire_v9.safetensors",
      "ember_knight_v3.ckpt",
      "arcane_beast_v2.safetensors"
    ],
    loras: [
      "chibi_magic_v2.safetensors",
      "noodle_samurai_v1.safetensors"
    ],
    vae: [
      "noodle_sauce.vae"
    ],
    controlnet: [
      "goblin_pose_v1.ckpt"
    ],
    ipadapter: [
      "arcane_face_v1.safetensors"
    ],
    animatediff: [
      "storybook_motion_v1.ckpt"
    ],
    active: {
      checkpoints: "dragonfire_v9.safetensors",
      loras: "chibi_magic_v2.safetensors",
      vae: "noodle_sauce.vae",
      controlnet: "goblin_pose_v1.ckpt",
      ipadapter: "arcane_face_v1.safetensors",
      animatediff: "storybook_motion_v1.ckpt"
    }
  },

  styles: {
    presets: {
      "celestial-chibi": {
        name: "Celestial Chibi",
        description: "Cute, glowing, star‑touched chibi style",
        color: "#ffd6ff"
      },
      "noir-goblin": {
        name: "Noir Goblin",
        description: "Shadowy, gritty goblin detective aesthetic",
        color: "#333333"
      },
      "arcane-ink": {
        name: "Arcane Ink",
        description: "Mystical line‑art infused with magical glyphs",
        color: "#4b0082"
      },
      "pixel-dungeon": {
        name: "Pixel Dungeon",
        description: "Retro 16‑bit dungeon crawler look",
        color: "#00aaff"
      },
      "storybook-watercolor": {
        name: "Storybook Watercolor",
        description: "Soft, painterly children’s book style",
        color: "#ffcc99"
      }
    }
  },

  workflows: {
    list: [
      "arcane_spriteflow.json",
      "goblin_motion_lab.json"
    ],
    data: {
      "arcane_spriteflow.json": {
        name: "Arcane Spriteflow",
        nodes: [
          { id: "1", type: "Input", label: "Character Frames" },
          { id: "2", type: "Style", label: "Apply Arcane Ink" },
          { id: "3", type: "Output", label: "Final Sprite Sheet" }
        ]
      },
      "goblin_motion_lab.json": {
        name: "Goblin Motion Lab",
        nodes: [
          { id: "1", type: "Motion", label: "Goblin Sneak" },
          { id: "2", type: "Refine", label: "Smooth Animation" }
        ]
      }
    }
  },

  prompts: {
    templates: {
      "arcane-wizard": {
        title: "Arcane Wizard",
        text: "A mystical wizard surrounded by swirling runes."
      },
      "goblin-rogue": {
        title: "Goblin Rogue",
        text: "A sneaky goblin thief lurking in the shadows."
      }
    }
  },

  projects: {
    list: [
      "wizard_dance_loop",
      "goblin_sneak_cycle",
      "dragon_hatch_idle"
    ],
    data: {
      "wizard_dance_loop": {
        name: "wizard_dance_loop",
        character: "Wizard",
        style: "arcane-ink",
        frames: 12
      },
      "goblin_sneak_cycle": {
        name: "goblin_sneak_cycle",
        character: "Goblin",
        style: "noir-goblin",
        frames: 8
      },
      "dragon_hatch_idle": {
        name: "dragon_hatch_idle",
        character: "Dragon",
        style: "storybook-watercolor",
        frames: 6
      }
    }
  },

  batches: {},

  // Fake file tree under /workspace
  files: {
    "/workspace": [
      { name: "models", path: "/workspace/models", is_dir: true },
      { name: "sprites", path: "/workspace/sprites", is_dir: true },
      { name: "projects", path: "/workspace/projects", is_dir: true }
    ],
    "/workspace/models": [
      { name: "checkpoints", path: "/workspace/models/checkpoints", is_dir: true },
      { name: "loras", path: "/workspace/models/loras", is_dir: true },
      { name: "vae", path: "/workspace/models/vae", is_dir: true }
    ],
    "/workspace/models/checkpoints": [
      { name: "dragonfire_v9.safetensors", path: "/workspace/models/checkpoints/dragonfire_v9.safetensors", is_file: true },
      { name: "ember_knight_v3.ckpt", path: "/workspace/models/checkpoints/ember_knight_v3.ckpt", is_file: true }
    ],
    "/workspace/sprites": [
      { name: "goblin_sneak", path: "/workspace/sprites/goblin_sneak", is_dir: true }
    ],
    "/workspace/sprites/goblin_sneak": [
      { name: "frame_0001.png", path: "/workspace/sprites/goblin_sneak/frame_0001.png", is_file: true },
      { name: "frame_0002.png", path: "/workspace/sprites/goblin_sneak/frame_0002.png", is_file: true }
    ]
  }
}

// ---------------------------------------------------------------------------
// SECTION 2 — Helpers + Mock Generators
// ---------------------------------------------------------------------------

// Random ID generator (fantasy‑flavored)
function makeId(prefix = "id") {
  const n = Math.floor(Math.random() * 99999)
  return `${prefix}_${n.toString().padStart(5, "0")}`
}

// Timestamp helper
function now() {
  return new Date().toISOString()
}

// Fake frame generator for animations
function generateFakeFrames(count = 8, basePath = "/workspace/sprites/goblin_sneak") {
  const frames = []
  for (let i = 1; i <= count; i++) {
    const num = i.toString().padStart(4, "0")
    frames.push(`${basePath}/frame_${num}.png`)
  }
  return frames
}

// Fake video preview path
function fakeVideo(character = "goblin") {
  return `/workspace/animations/${character}_preview.mp4`
}

// Fake sprite sheet path
function fakeSpriteSheet(character = "goblin") {
  return `/workspace/spritesheets/${character}_sheet.png`
}

// Fake batch progress generator
function generateBatchStatus(batchId) {
  const batch = mockData.batches[batchId]
  if (!batch) return null

  // Simulate progress
  const elapsed = Date.now() - batch.startTime
  const pct = Math.min(100, Math.floor(elapsed / 120))

  batch.progress = pct
  batch.updated = now()

  if (pct >= 100) {
    batch.status = "completed"
    batch.result = {
      sheet: fakeSpriteSheet(batch.character),
      frames: generateFakeFrames(8, `/workspace/sprites/${batch.character}`)
    }
  }

  return batch
}

// Fake workflow validation
function validateWorkflowMock(data) {
  if (!data || !Array.isArray(data.nodes)) {
    return { valid: false, message: "Invalid workflow format" }
  }
  if (data.nodes.length === 0) {
    return { valid: false, message: "Workflow must contain at least one node" }
  }
  return { valid: true, message: "Workflow is valid" }
}

// Fake file preview resolver
function fakePreviewFor(path) {
  const ext = path.toLowerCase()

  if (ext.endsWith(".png") || ext.endsWith(".jpg") || ext.endsWith(".jpeg")) {
    return { type: "image", mimetype: "image/png", path }
  }

  if (ext.endsWith(".mp4") || ext.endsWith(".webm")) {
    return { type: "video", mimetype: "video/mp4", path }
  }

  return { type: "raw", mimetype: "application/octet-stream", path }
}

// Fake project preparation (matches backend structure)
function prepareProjectForGUI(project) {
  return {
    name: project.name,
    character: project.character,
    style: project.style,
    frames: project.frames,
    lastModified: now(),
    workspacePath: `/workspace/projects/${project.name}`
  }
}

// ---------------------------------------------------------------------------
// SECTION 3 — Motion Routes (Structured Prompt System)
// ---------------------------------------------------------------------------

// GET /api/motion/skeletons
app.get("/api/motion/skeletons", (req, res) => {
  return res.json({
    skeletons: mockData.motion.skeletons
  })
})

// GET /api/motion/presets
app.get("/api/motion/presets", (req, res) => {
  const list = Object.values(mockData.motion.presets)
  return res.json({ presets: list })
})

// POST /api/motion/presets/save
app.post("/api/motion/presets/save", (req, res) => {
  const preset = req.body.preset
  if (!preset || !preset.id) {
    return res.status(400).json({ error: "Preset must include an id" })
  }

  mockData.motion.presets[preset.id] = preset

  return res.json({
    status: "ok",
    preset
  })
})

// DELETE /api/motion/presets/:id
app.delete("/api/motion/presets/:id", (req, res) => {
  const id = req.params.id
  delete mockData.motion.presets[id]
  return res.json({ status: "deleted" })
})

// POST /api/motion/generate
app.post("/api/motion/generate", (req, res) => {
  const { skeleton, prompt, seed } = req.body

  // Fake frames
  const frames = Array.from({ length: 12 }).map((_, i) => {
    const n = String(i + 1).padStart(3, "0")
    return `/mock/motion/${skeleton}/frame_${n}.png`
  })

  // Fake preview
  const preview = `/mock/motion/${skeleton}/preview.gif`

  const motionData = {
    duration: 1.0,
    fps: 12,
    skeleton,
    seed
  }

  return res.json({
    frames,
    preview,
    motionData,
    seed
  })
})

// ---------------------------------------------------------------------------
// SECTION 4 — Models Routes
// ---------------------------------------------------------------------------

// GET /api/models
app.get("/api/models", (req, res) => {
  return res.json({
    checkpoints: mockData.models.checkpoints,
    loras: mockData.models.loras,
    vae: mockData.models.vae,
    controlnet: mockData.models.controlnet,
    ipadapter: mockData.models.ipadapter,
    animatediff: mockData.models.animatediff
  })
})

// GET /api/models/:type
app.get("/api/models/:type", (req, res) => {
  const type = req.params.type

  if (!mockData.models[type]) {
    return res.status(400).json({ error: `Invalid model type '${type}'` })
  }

  return res.json({
    [type]: mockData.models[type]
  })
})

// GET /api/models/active
app.get("/api/models/active", (req, res) => {
  return res.json(mockData.models.active)
})

// POST /api/models/active
app.post("/api/models/active", (req, res) => {
  const data = req.body || {}

  // New format: { type: "...", model: "..." }
  if (data.type && data.model) {
    if (!mockData.models[data.type]) {
      return res.status(400).json({ error: `Invalid model type '${data.type}'` })
    }

    mockData.models.active[data.type] = data.model

    return res.json({
      status: "updated",
      active: mockData.models.active
    })
  }

  // Backward compatibility: { checkpoints: "foo.safetensors" }
  let updated = false
  for (const key of Object.keys(mockData.models.active)) {
    if (data[key]) {
      mockData.models.active[key] = data[key]
      updated = true
    }
  }

  if (!updated) {
    return res.status(400).json({ error: "Invalid payload" })
  }

  return res.json({
    status: "updated",
    active: mockData.models.active
  })
})

// POST /api/models/upload
app.post("/api/models/upload", (req, res) => {
  // Since this is a mock server, we don't handle real file uploads.
  // We simulate success and add the file to the model list.

  const modelType = req.body?.type || "checkpoints"
  const filename = req.body?.filename || makeId("uploaded") + ".safetensors"

  if (!mockData.models[modelType]) {
    return res.status(400).json({ error: `Invalid model type '${modelType}'` })
  }

  mockData.models[modelType].push(filename)

  return res.json({
    status: "ok",
    filename,
    type: modelType,
    path: `${WORKSPACE_ROOT}/models/${modelType}/${filename}`,
    note: "Mock upload — no real file saved"
  })
})

// ---------------------------------------------------------------------------
// SECTION 5 — Styles Routes
// ---------------------------------------------------------------------------

// GET /api/styles
app.get("/api/styles", (req, res) => {
  const presets = mockData.styles.presets

  // Convert object → array for GUI convenience
  const list = Object.keys(presets).map(id => ({
    id,
    name: presets[id].name,
    description: presets[id].description,
    color: presets[id].color
  }))

  return res.json({ styles: list })
})

// GET /api/styles/:id
app.get("/api/styles/:id", (req, res) => {
  const id = req.params.id
  const preset = mockData.styles.presets[id]

  if (!preset) {
    return res.status(404).json({
      error: `Style preset '${id}' not found`
    })
  }

  return res.json({
    id,
    ...preset
  })
})

// ---------------------------------------------------------------------------
// SECTION 6 — Files Routes
// ---------------------------------------------------------------------------

// GET /api/files/list
// Returns the contents of a directory inside /workspace
app.get("/api/files/list", (req, res) => {
  const dir = req.query.dir || "/workspace"

  const listing = mockData.files[dir]
  if (!listing) {
    return res.status(404).json({
      error: `Directory not found: ${dir}`
    })
  }

  return res.json({
    dir,
    items: listing
  })
})

// GET /api/files/preview
// Returns metadata about a file (image/video/raw)
app.get("/api/files/preview", (req, res) => {
  const path = req.query.path
  if (!path) {
    return res.status(400).json({ error: "Missing 'path' query parameter" })
  }

  const preview = fakePreviewFor(path)

  return res.json({
    status: "ok",
    preview,
    note: "Mock preview — no real file on disk"
  })
})

// ---------------------------------------------------------------------------
// SECTION 7 — Workflows Routes
// ---------------------------------------------------------------------------

// GET /api/workflows
// Returns a list of available workflow files
app.get("/api/workflows", (req, res) => {
  return res.json({
    workflows: mockData.workflows.list
  })
})

// GET /api/workflows/:name
// Returns the JSON content of a workflow
app.get("/api/workflows/:name", (req, res) => {
  const name = req.params.name
  const data = mockData.workflows.data[name]

  if (!data) {
    return res.status(404).json({
      error: `Workflow '${name}' not found`
    })
  }

  return res.json({
    name,
    ...data
  })
})

// POST /api/workflows/validate
// Validates workflow structure (mocked)
app.post("/api/workflows/validate", (req, res) => {
  const workflow = req.body
  const result = validateWorkflowMock(workflow)

  return res.json(result)
})

// ---------------------------------------------------------------------------
// SECTION 8 — Sprites Routes
// ---------------------------------------------------------------------------

// GET /api/sprites/list
// Lists sprite folders under /workspace/sprites
app.get("/api/sprites/list", (req, res) => {
  const root = "/workspace/sprites"
  const listing = mockData.files[root] || []

  const folders = listing.filter(item => item.is_dir)

  return res.json({
    sprites: folders.map(f => ({
      name: f.name,
      path: f.path
    }))
  })
})

// POST /api/sprites/generate
// Generates a fake sprite sequence
app.post("/api/sprites/generate", (req, res) => {
  const data = req.body || {}
  const character = data.character || "goblin"
  const preset = data.motion || "goblin_sneak"

  const dir = `/workspace/sprites/${preset}`
  const frames = generateFakeFrames(8, dir)

  const result = {
    status: "ok",
    character,
    preset,
    frames_dir: dir,
    frames,
    sheet: fakeSpriteSheet(character),
    created: now()
  }

  return res.json(result)
})

// GET /api/sprites/preview
// Returns metadata about a sprite frame or sheet
app.get("/api/sprites/preview", (req, res) => {
  const path = req.query.path
  if (!path) {
    return res.status(400).json({ error: "Missing 'path' query parameter" })
  }

  const preview = fakePreviewFor(path)

  return res.json({
    status: "ok",
    preview,
    note: "Mock sprite preview — no real file on disk"
  })
})

// POST /api/sprites/assemble
app.post("/api/sprites/assemble", (req, res) => {
  const data = req.body || {}
  const character = data.character || "goblin"

  const sheet = fakeSpriteSheet(character)

  return res.json({
    status: "ok",
    sheet,
    preview: fakePreviewFor(sheet),
    note: "Mock sprite sheet assembly — no real image generated"
  })
})


// ---------------------------------------------------------------------------
// SECTION 9 — Batch Routes
// ---------------------------------------------------------------------------

// POST /api/batch/create
// Creates a new fake batch job
app.post("/api/batch/create", (req, res) => {
  const data = req.body || {}

  const batchId = makeId("batch")
  const character = data.character || "goblin"
  const preset = data.motion || "goblin_sneak"

  mockData.batches[batchId] = {
    id: batchId,
    status: "created",
    character,
    preset,
    progress: 0,
    created: now(),
    updated: now(),
    startTime: Date.now(),
    result: null
  }

  return res.json({
    status: "ok",
    batch_id: batchId
  })
})

// POST /api/batch/run/:id
// Starts a fake batch job
app.post("/api/batch/run/:id", (req, res) => {
  const id = req.params.id
  const batch = mockData.batches[id]

  if (!batch) {
    return res.status(404).json({ error: `Batch '${id}' not found` })
  }

  batch.status = "running"
  batch.updated = now()
  batch.startTime = Date.now()

  return res.json({
    status: "started",
    batch_id: id
  })
})

// GET /api/batch/status/:id
// Returns simulated progress
app.get("/api/batch/status/:id", (req, res) => {
  const id = req.params.id
  const batch = mockData.batches[id]

  if (!batch) {
    return res.status(404).json({ error: `Batch '${id}' not found` })
  }

  const updated = generateBatchStatus(id)

  return res.json({
    id,
    status: updated.status,
    progress: updated.progress,
    character: updated.character,
    preset: updated.preset,
    result: updated.result || null,
    updated: updated.updated
  })
})

// ---------------------------------------------------------------------------
// SECTION 10 — Prompts Routes
// ---------------------------------------------------------------------------

// GET /api/prompts
// Returns a list of all prompt templates
app.get("/api/prompts", (req, res) => {
  const templates = mockData.prompts.templates

  const list = Object.keys(templates).map(id => ({
    id,
    title: templates[id].title
  }))

  return res.json({
    prompts: list
  })
})

// GET /api/prompts/:id
// Returns a specific prompt template
app.get("/api/prompts/:id", (req, res) => {
  const id = req.params.id
  const template = mockData.prompts.templates[id]

  if (!template) {
    return res.status(404).json({
      error: `Prompt template '${id}' not found`
    })
  }

  return res.json({
    id,
    ...template
  })
})

// POST /api/prompts/:id
// Saves or updates a prompt template
app.post("/api/prompts/:id", (req, res) => {
  const id = req.params.id
  const data = req.body || {}

  if (!data.title || !data.text) {
    return res.status(400).json({
      error: "Prompt template must include 'title' and 'text'"
    })
  }

  mockData.prompts.templates[id] = {
    title: data.title,
    text: data.text
  }

  return res.json({
    status: "saved",
    id,
    template: mockData.prompts.templates[id]
  })
})

// ---------------------------------------------------------------------------
// SECTION 11 — Project Routes
// ---------------------------------------------------------------------------

// GET /api/project/list
// Returns a list of all project names
app.get("/api/project/list", (req, res) => {
  return res.json({
    projects: mockData.projects.list
  })
})

// GET /api/project/load/:id
// Loads a specific project
app.get("/api/project/load/:id", (req, res) => {
  const id = req.params.id
  const project = mockData.projects.data[id]

  if (!project) {
    return res.status(404).json({
      error: `Project '${id}' not found`
    })
  }

  return res.json({
    status: "ok",
    project: prepareProjectForGUI(project)
  })
})

// POST /api/project/save
// Saves or updates a project
app.post("/api/project/save", (req, res) => {
  const data = req.body || {}

  if (!data.name) {
    return res.status(400).json({
      error: "Project must include a 'name'"
    })
  }

  // Create or update project
  mockData.projects.data[data.name] = {
    name: data.name,
    character: data.character || "Unknown",
    style: data.style || "arcane-ink",
    frames: data.frames || 1
  }

  // Add to list if new
  if (!mockData.projects.list.includes(data.name)) {
    mockData.projects.list.push(data.name)
  }

  return res.json({
    status: "saved",
    project: prepareProjectForGUI(mockData.projects.data[data.name])
  })
})

// ---------------------------------------------------------------------------
// SECTION 12 — Preview Routes
// ---------------------------------------------------------------------------

// GET /api/preview/sheet
// Returns metadata for a sprite sheet preview
app.get("/api/preview/sheet", (req, res) => {
  const character = req.query.character || "goblin"
  const sheet = fakeSpriteSheet(character)

  return res.json({
    status: "ok",
    sheet,
    preview: fakePreviewFor(sheet),
    note: "Mock sprite sheet preview — no real file on disk"
  })
})

// GET /api/preview/image
// Returns metadata for any image path
app.get("/api/preview/image", (req, res) => {
  const path = req.query.path
  if (!path) {
    return res.status(400).json({
      error: "Missing 'path' query parameter"
    })
  }

  const preview = fakePreviewFor(path)

  return res.json({
    status: "ok",
    preview,
    note: "Mock image preview — no real file on disk"
  })
})

// GET /api/preview/frames
app.get("/api/preview/frames", (req, res) => {
  const frames = generateFakeFrames(8, "/workspace/sprites/mock")

  return res.json({
    status: "ok",
    frames
  })
})


// ---------------------------------------------------------------------------
// SECTION 13 — Health Route
// ---------------------------------------------------------------------------

app.get("/api/health", (req, res) => {
  return res.json({
    status: "ok",
    service: "mock-backend",
    backendOnline
  })
})

// ---------------------------------------------------------------------------
// SECTION 14 — Server Bootstrap
// ---------------------------------------------------------------------------

// If the real backend is online, proxy unknown routes to it.
// Otherwise, mock server handles everything.
app.use(
  "/api",
  createProxyMiddleware({
    target: REAL_BACKEND,
    changeOrigin: true,
    logLevel: "silent",
    router: () => (backendOnline ? REAL_BACKEND : null),
    onProxyReq: (proxyReq, req, res) => {
      if (!backendOnline) {
        // Cancel proxying — mock server handles the route
        proxyReq.destroy()
      }
    }
  })
)

// ---------------------------------------------------------------------------
// SECTION 15 — AI Assistance (Mock)
// ---------------------------------------------------------------------------

app.post("/api/ai/motion/suggest", (req, res) => {
  const { skeleton } = req.body

  const suggestions = {
    overall: "A smooth, flowing motion with balanced weight shifts.",
    head: "Gentle tracking of the environment.",
    torso: "Relaxed posture with subtle sway.",
    arms: "Natural swing matching the gait.",
    hands: "Loose and expressive.",
    legs: "Confident stepping rhythm.",
    feet: "Soft heel-to-toe transitions.",
    style: "Graceful, fluid, harmonious."
  }

  return res.json({ fields: suggestions })
})

app.post("/api/ai/motion/refine", (req, res) => {
  const { fields } = req.body
  const refined = {}

  for (const key in fields) {
    refined[key] = fields[key]
      ? fields[key] + " (refined for clarity and detail)"
      : ""
  }

  return res.json({ fields: refined })
})

app.post("/api/ai/motion/style", (req, res) => {
  const { style } = req.body
  return res.json({
    style: style + " — enhanced with richer descriptive detail"
  })
})

app.post("/api/ai/motion/translate", (req, res) => {
  const { targetSkeleton, fields } = req.body

  const translated = {}
  for (const key in fields) {
    translated[key] = `[${targetSkeleton}] ${fields[key]}`
  }

  return res.json({ fields: translated })
})

// Catch-all for unknown routes (mock fallback)
app.use((req, res) => {
  return res.status(404).json({
    error: "Mock backend: route not found",
    route: req.originalUrl
  })
})

// Start server
app.listen(PORT, () => {
  console.log("-------------------------------------------------------")
  console.log(" SpriteForge Mock Backend (Fantasy Edition)")
  console.log("-------------------------------------------------------")
  console.log(` Mock server running on http://localhost:${PORT}`)
  console.log(` Workspace root: ${WORKSPACE_ROOT}`)
  console.log(" Backend auto-detect:", REAL_BACKEND)
  console.log("-------------------------------------------------------")
})
// End of mock_server.cjs