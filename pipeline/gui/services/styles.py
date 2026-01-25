import json
import os
import logging

STYLE_PRESET_PATH = "/workspace/pipeline/workflows/style_presets.json"

# Required fields for each style preset
REQUIRED_FIELDS = {
    "checkpoint": None,
    "lora": None,
    "vae": None,
    "controlnet": None,
    "ipadapter": None,
    "sampler": "euler",
    "cfg_scale": 1.0,
    "prompt_template": None
}


def _normalize_preset(preset: dict):
    """
    Ensures all required fields exist in a style preset.
    """
    normalized = REQUIRED_FIELDS.copy()
    normalized.update({k: v for k, v in preset.items() if k in REQUIRED_FIELDS})
    return normalized


def load_style_presets():
    """
    Loads the style preset file and returns:
    {
        "default": <default_style_id>,
        "presets": { ...normalized presets... }
    }
    """
    if not os.path.exists(STYLE_PRESET_PATH):
        logging.warning("[Styles] No style preset file found.")
        return {"default": None, "presets": {}}

    try:
        with open(STYLE_PRESET_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"[Styles] Failed to load style presets: {e}")
        return {"default": None, "presets": {}}

    presets = data.get("presets", {})
    default = data.get("default")

    # Normalize all presets
    normalized = {k: _normalize_preset(v) for k, v in presets.items()}

    logging.info(f"[Styles] Loaded {len(normalized)} style presets (default={default})")

    return {
        "default": default,
        "presets": normalized
    }


def get_style_preset(style_id: str):
    """
    Returns a single normalized style preset.
    """
    data = load_style_presets()
    presets = data.get("presets", {})

    preset = presets.get(style_id)
    if not preset:
        logging.warning(f"[Styles] Requested invalid style preset: {style_id}")
        return None

    return preset
