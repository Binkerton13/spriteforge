# services/workflow.py
import os
import json
import logging
from typing import Optional, Dict, Any

from services.comfyui import generate_sprites

PROJECT_ROOT = "/workspace/pipeline/projects"


def _workflow_path(project_id: str, workflow_type: str) -> str:
    project_dir = os.path.join(PROJECT_ROOT, project_id)
    workflows_dir = os.path.join(project_dir, "workflows")
    os.makedirs(workflows_dir, exist_ok=True)
    return os.path.join(workflows_dir, f"{workflow_type}.json")


def _safe_json_load(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[Workflow] Failed to load JSON {path}: {e}")
        return None


def _atomic_write(path: str, data: Dict[str, Any]):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=4)
    os.replace(tmp, path)


def load_workflow(project_id: str, workflow_type: str) -> Optional[Dict[str, Any]]:
    path = _workflow_path(project_id, workflow_type)
    if not os.path.exists(path):
        logging.warning(f"[Workflow] Not found: {path}")
        return None
    return _safe_json_load(path)


def save_workflow(project_id: str, workflow_type: str, graph: Dict[str, Any]) -> bool:
    path = _workflow_path(project_id, workflow_type)
    try:
        _atomic_write(path, graph)
        logging.info(f"[Workflow] Saved {workflow_type} for project {project_id}")
        return True
    except Exception as e:
        logging.error(f"[Workflow] Failed to save {workflow_type} for {project_id}: {e}")
        return False


def validate_workflow_graph(graph: Dict[str, Any]):
    if not isinstance(graph, dict):
        return False, "Workflow graph must be an object"

    nodes = graph.get("nodes")
    links = graph.get("links")

    if not isinstance(nodes, dict):
        return False, "Workflow graph must contain 'nodes' as an object"
    if not isinstance(links, list):
        return False, "Workflow graph must contain 'links' as a list"

    return True, "ok"


def run_workflow(project_id: str, workflow_type: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    graph = load_workflow(project_id, workflow_type)
    if graph is None:
        return {"status": "error", "message": "Workflow not found"}

    if workflow_type == "sprite":
        return generate_sprites(graph, inputs)

    return {
        "status": "error",
        "message": f"Workflow type '{workflow_type}' is not runnable yet"
    }
