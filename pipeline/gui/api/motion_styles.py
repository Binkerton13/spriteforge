# In api/motion.py (recommended)
from services.motion_styles import list_motion_styles
from flask import Blueprint, jsonify

@motion_bp.get("/styles")
def motion_styles():
    """
    Returns a list of built‑in motion style presets.
    """
    return jsonify({
        "styles": list_motion_styles()
    })
