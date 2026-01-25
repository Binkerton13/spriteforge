import json
import os
import logging

SELECTION_PATH = "/workspace/pipeline/workflows/active_models.json"

# Full schema for model selection + style-compatible fields
DEFAULT_SELECTION = {
    "checkpoint": None,
    "lora": None,
    "vae": None,
    "controlnet": None,
    "ipadapter": None,
    "clip": None,
    "embeddings": None,
    "upscale": None,

    # Style-compatible fields
    "sampler": "euler",
    "cfg_scale": 1.0,
    "prompt_template": None
}


def _normalize_selection(data: dict):
    """
    Ensures all required keys exist and fills missing ones with defaults.
    """
    normalized = DEFAULT_SELECTION.copy()
    normalized.update({k: v for k, v in data.items() if k in DEFAULT_SELECTION})
    return normalized


def load_selection():
    """
    Loads the active model selection, normalizes it, and returns it.
    """
    if not os.path.exists(SELECTION_PATH):
        logging.info("[ModelSelection] No selection file found, using defaults.")
        return DEFAULT_SELECTION.copy()

    try:
        with open(SELECTION_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"[ModelSelection] Failed to load selection file: {e}")
        return DEFAULT_SELECTION.copy()

    normalized = _normalize_selection(data)
    logging.info(f"[ModelSelection] Loaded selection: {normalized}")
    return normalized


def save_selection(data: dict):
    """
    Saves the active model selection after normalizing it.
    """
    normalized = _normalize_selection(data)

    try:
        with open(SELECTION_PATH, "w") as f:
            json.dump(normalized, f, indent=4)
        logging.info(f"[ModelSelection] Saved selection: {normalized}")
        return True
    except Exception as e:
        logging.error(f"[ModelSelection] Failed to save selection: {e}")
        return False
