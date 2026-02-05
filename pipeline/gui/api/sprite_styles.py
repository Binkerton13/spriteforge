# api/sprite_styles.py
from flask import Blueprint, request, jsonify
from services.sprite_styles import (
    list_sprite_styles,
    load_sprite_style,
    save_sprite_style,
    delete_sprite_style
)

sprite_styles_bp = Blueprint("sprite_styles", __name__)

# ---------------------------------------------------------
# LIST STYLES
# ---------------------------------------------------------
@sprite_styles_bp.get("/list/<project_id>")
def api_list_sprite_styles(project_id):
    styles = list_sprite_styles(project_id)
    return jsonify({"styles": styles})


# ---------------------------------------------------------
# LOAD SINGLE STYLE
# ---------------------------------------------------------
@sprite_styles_bp.get("/load/<project_id>/<style_id>")
def api_load_sprite_style(project_id, style_id):
    style = load_sprite_style(project_id, style_id)
    if not style:
        return jsonify({"error": "Style not found"}), 404
    return jsonify({"style": style})


# ---------------------------------------------------------
# SAVE / UPDATE STYLE
# ---------------------------------------------------------
@sprite_styles_bp.post("/save/<project_id>")
def api_save_sprite_style(project_id):
    data = request.json or {}
    style = save_sprite_style(project_id, data)
    return jsonify({"style": style})


# ---------------------------------------------------------
# DELETE STYLE
# ---------------------------------------------------------
@sprite_styles_bp.delete("/delete/<project_id>/<style_id>")
def api_delete_sprite_style(project_id, style_id):
    ok = delete_sprite_style(project_id, style_id)
    if not ok:
        return jsonify({"error": "Style not found"}), 404
    return jsonify({"deleted": style_id})
