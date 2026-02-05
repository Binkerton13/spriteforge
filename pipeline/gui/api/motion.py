# api/motion.py
from flask import Blueprint, request, jsonify, send_file
import os
import logging

from services.hymotion import generate_motion

motion_bp = Blueprint("motion", __name__)


@motion_bp.get("/skeletons")
def motion_skeletons():
    return jsonify({
        "skeletons": [
            {
                "id": "human",
                "name": "Human (Biped)",
                "segments": ["overall", "head", "torso", "arms", "hands", "legs", "feet", "style_detail"]
            },
            {
                "id": "quadruped",
                "name": "Quadruped",
                "segments": ["overall", "head", "neck", "front_legs", "hind_legs", "tail", "style_detail"]
            },
            {
                "id": "chibi",
                "name": "Stylized Chibi",
                "segments": ["overall", "head", "torso", "arms", "legs", "exaggeration", "style_detail"]
            }
        ]
    })


@motion_bp.post("/generate")
def motion_generate():
    data = request.json or {}
    skeleton = data.get("skeleton", "human")
    prompt = data.get("prompt", "")
    seed = data.get("seed")

    logging.info(f"[HY-Motion] request skeleton={skeleton} seed={seed}")
    result = generate_motion(prompt, skeleton=skeleton, seed=seed)
    return jsonify(result)


@motion_bp.get("/preview/video")
def preview_video():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "Video not found"}), 404
    return send_file(path, mimetype="video/mp4")


@motion_bp.get("/preview/frames")
def preview_frames():
    frames_dir = request.args.get("dir")
    if not frames_dir or not os.path.exists(frames_dir):
        return jsonify({"error": "Frames directory not found"}), 404

    frames = sorted([
        f for f in os.listdir(frames_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ])

    return jsonify({
        "frames": [os.path.join(frames_dir, f) for f in frames]
    })


@motion_bp.get("/preview/frame")
def preview_frame():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "Frame not found"}), 404
    return send_file(path, mimetype="image/png")
