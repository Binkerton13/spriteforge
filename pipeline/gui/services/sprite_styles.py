# services/sprite_styles.py
import os
import json
import uuid
import logging
from typing import Dict, Any, Optional

PROJECT_ROOT = "/workspace/pipeline/projects"


def _styles_dir(project_id: str) -> str:
    base = os.path.join(PROJECT_ROOT, project_id, "styles")
    os.makedirs(base, exist_ok=True)
    return base


def list_sprite_styles(project_id: str):
    base = _styles_dir(project_id)
    styles = []

    for fname in os.listdir(base):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(base, fname), "r") as f:
                    styles.append(json.load(f))
            except Exception as e:
                logging.error(f"[Styles] Failed to load {fname}: {e}")

    return styles


def load_sprite_style(project_id: str, style_id: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(_styles_dir(project_id), f"{style_id}.json")
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[Styles] Failed to load style {style_id}: {e}")
        return None


def save_sprite_style(project_id: str, style: Dict[str, Any]) -> Dict[str, Any]:
    style_id = style.get("id") or str(uuid.uuid4())[:8]
    style["id"] = style_id

    path = os.path.join(_styles_dir(project_id), f"{style_id}.json")
    tmp = path + ".tmp"

    try:
        with open(tmp, "w") as f:
            json.dump(style, f, indent=4)
        os.replace(tmp, path)
        logging.info(f"[Styles] Saved style {style_id} for project {project_id}")
    except Exception as e:
        logging.error(f"[Styles] Failed to save style {style_id}: {e}")

    return style


def delete_sprite_style(project_id: str, style_id: str) -> bool:
    path = os.path.join(_styles_dir(project_id), f"{style_id}.json")
    if not os.path.exists(path):
        return False

    try:
        os.remove(path)
        return True
    except Exception as e:
        logging.error(f"[Styles] Failed to delete style {style_id}: {e}")
        return False
