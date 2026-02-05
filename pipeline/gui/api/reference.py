# api/reference.py
from flask import Blueprint, request, jsonify
import logging

from services.reference_descriptor import save_reference_file, describe_reference_images

bp = Blueprint("reference", __name__, url_prefix="/api/reference")


@bp.post("/upload")
def upload_reference():
    project_id = request.form.get("project_id")
    if not project_id:
        return jsonify({"status": "error", "message": "Missing project_id"}), 400

    if "file" not in request.files:
        return jsonify({"status": "error", "message": "Missing file"}), 400

    file = request.files["file"]
    meta = save_reference_file(project_id, file)

    return jsonify({
        "status": "success",
        "reference": meta
    })


@bp.post("/describe")
def describe_references():
    data = request.get_json(force=True)
    paths = data.get("paths", [])

    if not paths:
        return jsonify({"status": "error", "message": "No paths provided"}), 400

    descriptions = describe_reference_images(paths)

    return jsonify({
        "status": "success",
        "descriptions": descriptions
    })
