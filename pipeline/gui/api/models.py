# api/models.py
from flask import Blueprint, request, jsonify
import logging

from services.models import (
    list_all_models,
    load_active_models,
    save_active_models,
)

models_bp = Blueprint("models", __name__)


@models_bp.get("/")
def models_all():
    """
    Returns all discoverable models grouped by category.
    {
      motion: [...],
      render: [...],
      style: [...],
      ipadapter: [...],
      loras: [...]
    }
    """
    data = list_all_models()
    return jsonify(data)


@models_bp.get("/active")
def models_active():
    """
    Returns the active model selection for the current project.
    Query: ?project_id=...
    """
    project_id = request.args.get("project_id")
    if not project_id:
        return jsonify({"error": "project_id is required"}), 400

    active = load_active_models(project_id)
    return jsonify(active)


@models_bp.post("/active")
def models_set_active():
    """
    Sets the active model selection for the current project.

    Body:
    {
      "project_id": "...",
      "selection": {
        "motion": "...",
        "render": "...",
        "style": "...",
        "ipadapter": "...",
        "loras": ["...", "..."]
      }
    }
    """
    data = request.json or {}
    project_id = data.get("project_id")
    selection = data.get("selection")

    if not project_id or not isinstance(selection, dict):
        return jsonify({"error": "project_id and selection are required"}), 400

    logging.info(f"[Models] Updating active models for project {project_id}")
    saved = save_active_models(project_id, selection)
    return jsonify(saved)
