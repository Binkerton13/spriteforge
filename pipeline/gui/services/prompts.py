import json
import os
import logging

TEMPLATE_PATH = "/workspace/pipeline/workflows/prompt_templates.json"

# Required fields for each prompt template
REQUIRED_FIELDS = {
    "prompt": "",
    "negative_prompt": ""
}


def _normalize_template(t: dict):
    """
    Ensures all required fields exist in a template.
    """
    normalized = REQUIRED_FIELDS.copy()
    normalized.update({k: v for k, v in t.items() if k in REQUIRED_FIELDS})
    return normalized


def load_templates():
    """
    Loads all prompt templates and returns a dict:
    {
        "template_id": { "prompt": "...", "negative_prompt": "..." }
    }
    """
    if not os.path.exists(TEMPLATE_PATH):
        logging.warning("[Prompts] No template file found.")
        return {}

    try:
        with open(TEMPLATE_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"[Prompts] Failed to load template file: {e}")
        return {}

    templates = data.get("templates", {})

    # Normalize all templates
    normalized = {k: _normalize_template(v) for k, v in templates.items()}

    logging.info(f"[Prompts] Loaded {len(normalized)} templates")
    return normalized


def get_template(template_id: str):
    """
    Returns a single normalized template.
    """
    templates = load_templates()
    template = templates.get(template_id)

    if not template:
        logging.warning(f"[Prompts] Requested invalid template: {template_id}")
        return None

    return template


def save_template(template_id: str, data: dict):
    """
    Saves or updates a template.
    Ensures schema normalization and safe file handling.
    """
    # Load existing file or create new structure
    if os.path.exists(TEMPLATE_PATH):
        try:
            with open(TEMPLATE_PATH, "r") as f:
                full = json.load(f)
        except Exception as e:
            logging.error(f"[Prompts] Failed to read template file: {e}")
            full = {"templates": {}}
    else:
        full = {"templates": {}}

    # Normalize and save
    full["templates"][template_id] = _normalize_template(data)

    try:
        with open(TEMPLATE_PATH, "w") as f:
            json.dump(full, f, indent=4)
        logging.info(f"[Prompts] Saved template '{template_id}'")
        return True
    except Exception as e:
        logging.error(f"[Prompts] Failed to save template '{template_id}': {e}")
        return False
