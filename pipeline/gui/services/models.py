# services/models.py
import os
import json
import logging
from typing import Dict, Any

MODEL_ROOT = "/workspace/models"
PROJECT_ROOT = "/workspace/pipeline/projects"

VALID_EXTENSIONS = (".safetensors", ".ckpt", ".pth")

MODEL_CATEGORIES = {
    "motion": "motion",
    "render": "checkpoints",
    "style": "loras",
    "ipadapter": "ipadapter",
    "loras": "loras",
}


def _safe_listdir(path: str):
    try:
        return os.listdir(path)
    except Exception as e:
        logging.error(f"[Models] Failed to list directory {path}: {e}")
        return []


def _list_files(folder: str):
    path = os.path.join(MODEL_ROOT, folder)
    os.makedirs(path, exist_ok=True)

    files = [
        f for f in _safe_listdir(path)
        if os.path.isfile(os.path.join(path, f))
        and f.lower().endswith(VALID_EXTENSIONS)
    ]
    files.sort()
    return files


def list_all_models() -> Dict[str, list]:
    result = {}
    for category, folder in MODEL_CATEGORIES.items():
        result[category] = _list_files(folder)
        logging.info(f"[Models] {category}: {len(result[category])} models in {folder}")
    return result


def _active_models_path(project_id: str) -> str:
    project_dir = os.path.join(PROJECT_ROOT, project_id)
    os.makedirs(project_dir, exist_ok=True)
    return os.path.join(project_dir, "models.json")


def load_active_models(project_id: str) -> Dict[str, Any]:
    path = _active_models_path(project_id)
    if not os.path.exists(path):
        return {
            "motion": None,
            "render": None,
            "style": None,
            "ipadapter": None,
            "loras": [],
        }

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[Models] Failed to load active models for {project_id}: {e}")
        return {
            "motion": None,
            "render": None,
            "style": None,
            "ipadapter": None,
            "loras": [],
        }


def save_active_models(project_id: str, selection: Dict[str, Any]) -> Dict[str, Any]:
    path = _active_models_path(project_id)
    tmp = path + ".tmp"

    try:
        with open(tmp, "w") as f:
            json.dump(selection, f, indent=4)
        os.replace(tmp, path)
        logging.info(f"[Models] Saved active models for project {project_id}")
    except Exception as e:
        logging.error(f"[Models] Failed to save active models for {project_id}: {e}")

    return selection
