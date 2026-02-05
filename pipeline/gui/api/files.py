# api/files.py
from flask import Blueprint, request, jsonify, send_file
import os
import logging

files_bp = Blueprint("files", __name__)


@files_bp.get("/preview")
def files_preview():
    """
    GET /api/files/preview?path=/absolute/path/to/file
    """
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404

    ext = os.path.splitext(path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
        return send_file(path, mimetype="image/png")

    if ext in [".mp4", ".webm"]:
        return send_file(path, mimetype="video/mp4")

    return send_file(path)


@files_bp.get("/list")
def files_list():
    """
    GET /api/files/list?path=/workspace/projects/<id>/outputs
    Returns directory contents.
    """
    root = request.args.get("path")
    if not root:
        return jsonify({"items": []})

    if not os.path.exists(root):
        return jsonify({"items": []})

    items = []
    for name in sorted(os.listdir(root)):
        full = os.path.join(root, name)
        items.append({
            "name": name,
            "path": full,
            "is_file": os.path.isfile(full),
            "is_dir": os.path.isdir(full)
        })

    return jsonify({"items": items})
