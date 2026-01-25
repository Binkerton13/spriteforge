import os
import json
import uuid
import logging
from datetime import datetime
from typing import Optional, Dict, Any

PROJECT_ROOT = "/workspace/projects"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _atomic_write(path: str, data: dict):
    """Write JSON atomically to avoid corruption."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=4)
    os.replace(tmp, path)


def _ensure_project_dir(project_id: str) -> str:
    project_dir = os.path.join(PROJECT_ROOT, project_id)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir


# ----------------------------------------------------------------------
# Save / Load
# ----------------------------------------------------------------------
def save_project(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a project safely and return the updated metadata.
    """
    project_id = data.get("project_id") or str(uuid.uuid4())[:8]
    project_dir = _ensure_project_dir(project_id)

    data["project_id"] = project_id
    data["version"] = 1
    data["last_modified"] = datetime.utcnow().isoformat()

    if "created" not in data:
        data["created"] = data["last_modified"]

    path = os.path.join(project_dir, "project.json")

    try:
        _atomic_write(path, data)
        logging.info(f"[Project] Saved project {project_id}")
    except Exception as e:
        logging.error(f"[Project] Failed to save project {project_id}: {e}")

    return data


def load_project(project_id: str) -> Optional[Dict[str, Any]]:
    """
    Load a project by ID.
    """
    path = os.path.join(PROJECT_ROOT, project_id, "project.json")

    if not os.path.exists(path):
        logging.warning(f"[Project] Project not found: {project_id}")
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[Project] Failed to load project {project_id}: {e}")
        return None


def list_projects() -> list:
    """
    Return a list of all project IDs.
    """
    if not os.path.exists(PROJECT_ROOT):
        return []

    projects = []
    for name in os.listdir(PROJECT_ROOT):
        path = os.path.join(PROJECT_ROOT, name, "project.json")
        if os.path.exists(path):
            projects.append(name)

    projects.sort()
    return projects


# ----------------------------------------------------------------------
# GUI hydration
# ----------------------------------------------------------------------
def prepare_project_for_gui(project: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns a flattened structure the GUI can hydrate into fields.
    """
    return {
        "project_id": project.get("project_id"),
        "name": project.get("name"),
        "motion": project.get("motion", {}),
        "sprite": project.get("sprite", {}),
        "models": project.get("models", {}),
        "workflow": project.get("workflow", {}),
        "batch": project.get("batch", {}),
        "outputs": project.get("outputs", {})
    }
