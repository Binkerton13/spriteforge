# api/workflow.py
from flask import Blueprint, request, jsonify
from services.workflow import run_workflow
from services.project import ensure_project_scaffold
import logging

workflow_bp = Blueprint("workflow", __name__, url_prefix="/api/workflow")


@workflow_bp.post("/<workflow_type>/run")
def run(workflow_type):
    data = request.get_json(force=True)

    project_id = data.get("project_id")
    if not project_id:
        return jsonify({"status": "error", "message": "Missing project_id"}), 400

    ensure_project_scaffold(project_id)

    logging.info(f"[WorkflowAPI] Running workflow '{workflow_type}' for project {project_id}")

    result = run_workflow(project_id, workflow_type, data)

    return jsonify(result)
