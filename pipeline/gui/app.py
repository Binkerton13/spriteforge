from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import os
import logging

# Import SpriteForge service modules
from services.hymotion import generate_motion
from services.comfyui import generate_sprites
from services.spritesheet import assemble_spritesheet
from services.models import list_models, list_models_by_type
from services.styles import load_style_presets, get_style_preset
from services.workflows import list_workflows, load_workflow, save_workflow, validate_workflow
from services.model_selection import load_selection, save_selection
from services.batch import create_batch, run_batch_async, load_batch
from services.prompts import load_templates, get_template, save_template
from services.node_inspector import list_nodes, get_node_details
from services.project import save_project, load_project, list_projects, prepare_project_for_gui
from routes.health import health_bp


# --------------------------------------------------------------------------
# Create Flask App
# --------------------------------------------------------------------------
def create_app():
    app = Flask(
        __name__,
        static_folder="static",      # <-- Your built frontend lives here
        template_folder="templates"  # (unused but harmless)
    )
    app.register_blueprint(health_bp)
    CORS(app)

    # Logging setup
    log_dir = "/workspace/logs"
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, "gui_backend.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    # ----------------------------------------------------------------------
    # HEALTH ENDPOINT
    # ----------------------------------------------------------------------
    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "spriteforge-gui"})

    # ----------------------------------------------------------------------
    # FRONTEND ROUTES
    # ----------------------------------------------------------------------

    # Serve Vue frontend at root
    @app.route("/")
    def serve_frontend_root():
        return send_from_directory(app.static_folder, "index.html")

    # Optional: /ui also loads the frontend
    @app.route("/ui")
    def serve_frontend_ui():
        return send_from_directory(app.static_folder, "index.html")

    # Serve static assets (JS, CSS, images)
    @app.route("/static/<path:path>")
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

    # Catch-all for Vue Router (e.g., /sprites, /workflows, /settings)
    @app.route("/<path:path>")
    def catch_all(path):
        # If the file exists, serve it
        full_path = os.path.join(app.static_folder, path)
        if os.path.isfile(full_path):
            return send_from_directory(app.static_folder, path)

        # Otherwise return index.html for Vue Router
        return send_from_directory(app.static_folder, "index.html")

    # ----------------------------------------------------------------------
    # HY-Motion: Presets
    # ----------------------------------------------------------------------
    @app.get("/api/motion/presets")
    def motion_presets():
        presets = [
            "walk", "run", "idle", "jump",
            "attack", "stealth", "interact", "dance"
        ]
        return jsonify({"presets": presets})

    # ----------------------------------------------------------------------
    # HY-Motion: Generate Motion
    # ----------------------------------------------------------------------
    @app.post("/api/motion/generate")
    def motion_generate():
        data = request.json or {}
        preset = data.get("preset", "walk")
        seed = data.get("seed", None)

        logging.info(f"API motion request: preset={preset}, seed={seed}")
        result = generate_motion(preset, seed)
        return jsonify(result)

    # ----------------------------------------------------------------------
    # HY-Motion: Preview Animation
    # ----------------------------------------------------------------------
    @app.get("/api/preview/video")
    def preview_video():
        path = request.args.get("path")
        if not path or not os.path.exists(path):
            return jsonify({"error": "Video not found"}), 404
        return send_file(path, mimetype="video/mp4")

    @app.get("/api/preview/frames")
    def preview_frames():
        frames_dir = request.args.get("dir")
        if not frames_dir or not os.path.exists(frames_dir):
            return jsonify({"error": "Frames directory not found"}), 404

        frames = sorted([
            f for f in os.listdir(frames_dir)
            if f.lower().endswith((".png", ".jpg"))
        ])

        return jsonify({
            "frames": [os.path.join(frames_dir, f) for f in frames]
        })

    @app.get("/api/preview/frame")
    def preview_frame():
        path = request.args.get("path")
        if not path or not os.path.exists(path):
            return jsonify({"error": "Frame not found"}), 404
        return send_file(path, mimetype="image/png")

    # ----------------------------------------------------------------------
    # ComfyUI: Generate Sprite Frames
    # ----------------------------------------------------------------------
    @app.post("/api/sprites/generate")
    def sprites_generate():
        data = request.json or {}
        character = data.get("character", "unnamed")
        frames_dir = data.get("frames_dir")
        style_id = data.get("style")

        if not frames_dir:
            return jsonify({"status": "error", "message": "frames_dir is required"}), 400

        style_preset = get_style_preset(style_id) if style_id else None
        if style_id and not style_preset:
            return jsonify({"status": "error", "message": "Invalid style preset"}), 400

        model_selection = load_selection()
        style_data = {**model_selection, **(style_preset or {})}

        logging.info(
            f"API sprite request: character={character}, frames={frames_dir}, style={style_id}"
        )

        result = generate_sprites(frames_dir, character, style_data)
        return jsonify(result)

    # ----------------------------------------------------------------------
    # SpriteForge: Assemble Sprite Sheet
    # ----------------------------------------------------------------------
    @app.post("/api/sprites/assemble")
    def sprites_assemble():
        data = request.json or {}
        character = data.get("character", "unnamed")
        frames_dir = data.get("frames_dir")

        if not frames_dir:
            return jsonify({"status": "error", "message": "frames_dir is required"}), 400

        logging.info(
            f"API spritesheet request: character={character}, frames={frames_dir}"
        )

        result = assemble_spritesheet(frames_dir, character)
        return jsonify(result)

    # ----------------------------------------------------------------------
    # SpriteForge: Preview Sprite Sheet
    # ----------------------------------------------------------------------
    @app.get("/api/preview/sheet")
    def preview_sheet():
        path = request.args.get("path")
        if not path or not os.path.exists(path):
            return jsonify({"error": "Sprite sheet not found"}), 404
        return send_file(path, mimetype="image/png")

    # ----------------------------------------------------------------------
    # Model Manager API
    # ----------------------------------------------------------------------
    @app.get("/api/models")
    def models_all():
        return jsonify(list_models())

    @app.get("/api/models/<model_type>")
    def models_by_type(model_type):
        result = list_models_by_type(model_type)
        if result is None:
            return jsonify({"error": "Invalid model type"}), 400
        return jsonify({model_type: result})

    # ----------------------------------------------------------------------
    # Model Selector API
    # ----------------------------------------------------------------------
    @app.get("/api/models/active")
    def models_active():
        return jsonify(load_selection())

    @app.post("/api/models/active")
    def models_set_active():
        data = request.json or {}
        current = load_selection()

        for key in current:
            if key in data:
                current[key] = data[key]

        save_selection(current)
        return jsonify({"status": "updated", "active": current})

    # ----------------------------------------------------------------------
    # Style Manager API
    # ----------------------------------------------------------------------
    @app.get("/api/styles")
    def styles_all():
        presets_data = load_style_presets()
        presets = presets_data.get("presets", {})
        return jsonify(presets)

    @app.get("/api/styles/<style_id>")
    def styles_one(style_id):
        preset = get_style_preset(style_id)
        if not preset:
            return jsonify({"error": "Invalid style preset"}), 404
        return jsonify(preset)

    # ----------------------------------------------------------------------
    # Workflow Editor API
    # ----------------------------------------------------------------------
    @app.get("/api/workflows")
    def workflows_all():
        return jsonify({"workflows": list_workflows()})

    @app.get("/api/workflows/<name>")
    def workflows_load(name):
        data = load_workflow(name)
        if data is None:
            return jsonify({"error": "Workflow not found"}), 404
        return jsonify(data)

    @app.post("/api/workflows/<name>")
    def workflows_save(name):
        data = request.json
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON"}), 400

        save_workflow(name, data)
        return jsonify({"status": "saved"})

    @app.post("/api/workflows/validate")
    def workflows_validate():
        data = request.json
        ok, msg = validate_workflow(data)
        return jsonify({"valid": ok, "message": msg})

    # ----------------------------------------------------------------------
    # Workflow Node Inspector API
    # ----------------------------------------------------------------------
    @app.get("/api/workflows/nodes/<workflow_name>")
    def workflow_nodes(workflow_name):
        nodes = list_nodes(workflow_name)
        if nodes is None:
            return jsonify({"error": "Workflow not found"}), 404
        return jsonify({"nodes": nodes})

    @app.get("/api/workflows/node/<workflow_name>/<node_id>")
    def workflow_node_details(workflow_name, node_id):
        details = get_node_details(workflow_name, node_id)
        if details is None:
            return jsonify({"error": "Node not found"}), 404
        return jsonify(details)

    # ----------------------------------------------------------------------
    # Batch Generation API
    # ----------------------------------------------------------------------
    @app.post("/api/batch/create")
    def batch_create():
        data = request.json or {}
        motions = data.get("motions", [])
        characters = data.get("characters", [])
        styles = data.get("styles", [])

        batch = create_batch(motions, characters, styles)
        return jsonify(batch)

    @app.post("/api/batch/run/<batch_id>")
    def batch_run(batch_id):
        result = run_batch_async(batch_id)
        return jsonify({
            "status": "started",
            "batch": result
        })

    @app.get("/api/batch/status/<batch_id>")
    def batch_status(batch_id):
        result = load_batch(batch_id)
        if not result:
            return jsonify({"error": "Batch not found"}), 404
        return jsonify(result)

    # ----------------------------------------------------------------------
    # Prompt Template API
    # ----------------------------------------------------------------------
    @app.get("/api/prompts")
    def prompts_all():
        return jsonify(load_templates())

    @app.get("/api/prompts/<template_id>")
    def prompts_one(template_id):
        data = get_template(template_id)
        if not data:
            return jsonify({"error": "Template not found"}), 404
        return jsonify(data)

    @app.post("/api/prompts/<template_id>")
    def prompts_save(template_id):
        data = request.json or {}
        save_template(template_id, data)
        return jsonify({"status": "saved", "template": template_id})

    # ----------------------------------------------------------------------
    # Project Save/Load API
    # ----------------------------------------------------------------------
    @app.post("/api/project/save")
    def project_save():
        data = request.json or {}
        result = save_project(data)
        return jsonify(result)

    @app.get("/api/project/load/<project_id>")
    def project_load(project_id):
        project = load_project(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404

        return jsonify(prepare_project_for_gui(project))

    @app.get("/api/project/list")
    def project_list():
        return jsonify(list_projects())

    # ----------------------------------------------------------------------
    # File Browser API
    # ----------------------------------------------------------------------
    @app.get("/api/files/list")
    def list_files():
        root = "/workspace"
        files = []

        for dirpath, dirnames, filenames in os.walk(root):
            for f in filenames:
                full = os.path.join(dirpath, f)
                files.append(full.replace(root, ""))

        return jsonify({"files": files})

    return app


# --------------------------------------------------------------------------
# Entry Point
# --------------------------------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
