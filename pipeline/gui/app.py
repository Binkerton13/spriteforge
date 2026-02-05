# app.py
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

from api.motion import motion_bp
from api.sprites import sprites_bp
from api.models import models_bp
from api.sprite_styles import sprite_styles_bp
from api.workflow import workflow_bp
from api.project import project_bp
from api.files import files_bp
from api.ai import ai_bp
from api.health import health_bp
from api.motion_presets import preset_bp

print("CWD =", os.getcwd()) 
print("ENV FILE EXISTS =", os.path.exists(".env"))
print("GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))
def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )
    CORS(app)

    # Health
    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "spriteforge"})

    # Frontend
    @app.route("/")
    def serve_frontend_root():
        static_folder = app.static_folder or "static"
        return send_from_directory(static_folder, "index.html")

    @app.route("/ui")
    def serve_frontend_ui():
        static_folder = app.static_folder or "static"
        return send_from_directory(static_folder, "index.html")

    @app.route("/static/<path:path>")
    def serve_static(path):
        static_folder = app.static_folder or "static"
        return send_from_directory(static_folder, path)

    # Blueprints
    app.register_blueprint(motion_bp, url_prefix="/api/motion")
    app.register_blueprint(sprites_bp, url_prefix="/api/sprites")
    app.register_blueprint(models_bp, url_prefix="/api/models")
    app.register_blueprint(sprite_styles_bp, url_prefix="/api/styles")
    app.register_blueprint(workflow_bp, url_prefix="/api/workflow")
    app.register_blueprint(project_bp, url_prefix="/api/project")
    app.register_blueprint(files_bp, url_prefix="/api/files")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(health_bp)
    app.register_blueprint(preset_bp, url_prefix="/api/motion-presets")
    # Vue router catch‑all
    @app.route("/<path:path>")
    def catch_all(path):
        static_folder = app.static_folder or "static"
        full_path = os.path.join(static_folder, path)
        if os.path.isfile(full_path):
            return send_from_directory(static_folder, path)
        return send_from_directory(static_folder, "index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
