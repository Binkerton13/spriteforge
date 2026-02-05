API Routes Map
Flask Blueprints and Routes
/api/ai (ai_bp)
POST /motion/suggest → ai_suggest()
Calls: ai_motion_suggest(data)
POST /motion/refine → ai_refine()
Calls: ai_motion_refine(data)
POST /motion/style → ai_style()
Calls: ai_motion_style(data)
POST /motion/translate → ai_translate()
Calls: ai_motion_translate(data)
/api/motion (motion_bp)
GET /skeletons → motion_skeletons()
Returns hardcoded skeletons list
POST /generate → motion_generate()
Calls: generate_motion(prompt, skeleton, seed)
GET /preview/video → preview_video()
Returns video file
GET /preview/frames → preview_frames()
Returns list of frame image paths
GET /preview/frame → preview_frame()
Returns single frame image
/api/sprites (sprites_bp)
POST /generate → sprites_generate()
Calls: generate_sprites(frames_dir, character, style)
POST /assemble → sprites_assemble()
Calls: assemble_spritesheet(frames_dir, character)
GET /preview/sheet → preview_sheet()
Returns sprite sheet image
/api/models (models_bp)
GET / → models_all()
Calls: list_all_models()
GET /active → models_active()
Calls: load_active_models(project_id)
POST /active → models_set_active()
Calls: save_active_models(project_id, selection)
/api/styles (styles_bp)
GET /sprite → styles_list()
Calls: list_sprite_styles(project_id)
GET /sprite/<style_id> → styles_one(style_id)
Calls: load_sprite_style(project_id, style_id)
POST /sprite/save → styles_save()
Calls: save_sprite_style(project_id, style)
DELETE /sprite/<style_id> → styles_delete(style_id)
Calls: delete_sprite_style(project_id, style_id)
/api/workflow (workflow_bp)
GET /<workflow_type> → workflow_load(workflow_type)
Calls: load_workflow(project_id, workflow_type)
POST /<workflow_type>/save → workflow_save(workflow_type)
Calls: validate_workflow_graph(graph), save_workflow(project_id, workflow_type, graph)
POST /<workflow_type>/run → workflow_run(workflow_type)
Calls: run_workflow(project_id, workflow_type, inputs)
/api/project (project_bp)
POST /save → project_save()
Calls: save_project(data), ensure_project_scaffold(project_id)
GET /load/<project_id> → project_load(project_id)
Calls: load_project(project_id), prepare_project_for_gui(project)
GET /list → project_list()
Calls: list_projects()
/api/files (files_bp)
GET /preview → files_preview()
Returns file (image/video/other)
GET /list → files_list()
Returns directory contents
Legacy/Direct Flask Routes in app.py
GET /health → health()
Returns service status
GET / → serve_frontend_root()
Serves index.html
GET /ui → serve_frontend_ui()
Serves index.html
GET /static/path:path → serve_static(path)
Serves static files
GET /path:path → catch_all(path)
Vue router catch-all, serves static or index.html
Service Modules Map
comfyui.py
trigger_workflow(workflow, inputs) — Triggers a ComfyUI workflow
wait_for_result(prompt_id, timeout) — Polls for workflow result
generate_sprites(workflow, runtime_inputs) — Runs a ComfyUI workflow for sprites
spritesheet.py
assemble_spritesheet(frames_dir, character_name) — Assembles frames into a sprite sheet
hymotion.py
generate_motion(prompt, skeleton, seed) — Runs HY-Motion with a prompt and skeleton
models.py
list_all_models() — Lists all models by category
load_active_models(project_id) — Loads active models for a project
save_active_models(project_id, selection) — Saves active model selection
sprite_styles.py
list_sprite_styles(project_id) — Lists all sprite styles for a project
load_sprite_style(project_id, style_id) — Loads a specific sprite style
save_sprite_style(project_id, style) — Saves a sprite style
delete_sprite_style(project_id, style_id) — Deletes a sprite style
project.py
save_project(data) — Saves project data
load_project(project_id) — Loads a project
list_projects() — Lists all projects
prepare_project_for_gui(project) — Prepares project data for frontend
ensure_project_scaffold(project_id) — Ensures project directory structure
Likely Legacy / Safe to Remove
Direct routes in app.py (other than /health and static serving) are mostly for frontend SPA support, not API, and are not legacy but not part of the API.
Old style/model/workflow systems:
If you see any routes or service functions not referenced in the frontend (Vue/JS) or not used in blueprints, mark as legacy.
Any duplicate style/model management functions outside the /api/styles or /api/models endpoints may be legacy.
No evidence of legacy/unused endpoints in the current API map.
If you find functions in services/ not imported or called by any API or blueprint, they are likely safe to remove.
Note:

All API endpoints are grouped under /api/* via blueprints.
Service modules are cleanly separated and called by their respective API handlers.
No legacy Flask routes for business logic remain in app.py; all logic is routed through blueprints.
For a full legacy audit, cross-reference with frontend API usage and check for unused service functions.