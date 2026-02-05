# api/project.py
from flask import Blueprint, request, jsonify
import logging

from services.project import (
    save_project,
    load_project,
    list_projects,
    prepare_project_for_gui,
    ensure_project_scaffold,
)

project_bp = Blueprint("project", __name__)


@project_bp.post("/save")
def project_save():
    """
    Body:
    {
      "project_id": "...",   # optional
      "name": "...",
      "motion": {...},
      "sprite": {...},
      "models": {...},
      "workflow": {...}
    }
    """
    data = request.json or {}

    saved = save_project(data)
    ensure_project_scaffold(saved["project_id"])

    return jsonify(saved)


@project_bp.get("/load/<project_id>")
def project_load(project_id):
    project = load_project(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    hydrated = prepare_project_for_gui(project)
    return jsonify(hydrated)


@project_bp.get("/list")
def project_list():
    return jsonify(list_projects())
