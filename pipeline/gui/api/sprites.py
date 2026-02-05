# api/sprites.py
from flask import Blueprint, request, jsonify, send_file
import os
import logging

from services.comfyui import generate_sprites
from services.spritesheet import assemble_spritesheet

sprites_bp = Blueprint("sprites", __name__)


@sprites_bp.post("/generate")
def sprites_generate():
    """
    New contract (from sprites.js):

    {
      "id": "uuid",
      "motion_id": "uuid",
      "render_style": "dark fantasy gritty",
      "resolution": 512,
      "variants": 1,
      "seed": 123,
      "background": "transparent",
      "render_model": "model_id"
    }

    For now we still expect frames_dir; later this will call workflow.run().
    """
    data = request.json or {}

    # TEMP: bridge between old and new
    frames_dir = data.get("frames_dir")
    character = data.get("character", "unnamed")
    style = data.get("style")  # legacy style id

    if not frames_dir:
        return jsonify({"status": "error", "message": "frames_dir is required (temporary bridge)"}), 400

    logging.info(f"[SpriteForge] sprite generate: character={character} frames={frames_dir} style={style}")

    result = generate_sprites(frames_dir, character, style)
    return jsonify(result)


@sprites_bp.post("/assemble")
def sprites_assemble():
    """
    New contract (from sprites.js):

    {
      "frames": ["/path/to/frame1.png", "..."],
      "layout": "auto",
      "padding": 2,
      "character": "Goblin Ninja"
    }

    For now we still accept frames_dir; later we’ll resolve frames → temp dir.
    """
    data = request.json or {}
    character = data.get("character", "unnamed")
    frames_dir = data.get("frames_dir")

    if not frames_dir:
        return jsonify({"status": "error", "message": "frames_dir is required (temporary bridge)"}), 400

    logging.info(f"[SpriteForge] spritesheet assemble: character={character} frames={frames_dir}")

    result = assemble_spritesheet(frames_dir, character)
    return jsonify(result)


@sprites_bp.get("/preview/sheet")
def preview_sheet():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "Sprite sheet not found"}), 404
    return send_file(path, mimetype="image/png")
