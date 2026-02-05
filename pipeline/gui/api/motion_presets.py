# api/motion_presets.py
from flask import Blueprint, request, jsonify
import os, json

preset_bp = Blueprint("motion_presets", __name__, url_prefix="/api/motion-presets")

PRESET_PATH = "/workspace/presets/motion.json"


def load_presets():
    if not os.path.exists(PRESET_PATH):
        return []
    try:
        with open(PRESET_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_presets(data):
    os.makedirs(os.path.dirname(PRESET_PATH), exist_ok=True)
    with open(PRESET_PATH, "w") as f:
        json.dump(data, f, indent=2)


@preset_bp.get("/")
def list_presets():
    return jsonify({"presets": load_presets()})


@preset_bp.post("/")
def save_all():
    data = request.get_json(force=True)
    presets = data.get("presets", [])
    save_presets(presets)
    return jsonify({"status": "ok"})


@preset_bp.post("/add")
def add_preset():
    data = request.get_json(force=True)
    presets = load_presets()
    presets.append(data)
    save_presets(presets)
    return jsonify({"status": "ok"})


@preset_bp.post("/delete")
def delete_preset():
    data = request.get_json(force=True)
    name = data.get("name")
    presets = load_presets()
    presets = [p for p in presets if p.get("name") != name]
    save_presets(presets)
    return jsonify({"status": "ok"})
