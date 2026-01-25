import os
import json
import logging

WORKFLOW_DIR = "pipeline/workflows"
MODEL_DIR = "/workspace/models"
PRESET_PATH = os.path.join(WORKFLOW_DIR, "style_presets.json")
TEMPLATE_PATH = os.path.join(WORKFLOW_DIR, "prompt_templates.json")
MANIFEST_PATH = os.path.join(WORKFLOW_DIR, "workflow_manifest.json")
ACTIVE_MODELS_PATH = os.path.join(WORKFLOW_DIR, "active_models.json")


# ----------------------------------------------------------------------
# Utility helpers
# ----------------------------------------------------------------------
def _load_json(path, errors, file_label=None):
    """Load JSON safely and append errors if malformed."""
    label = file_label or os.path.basename(path)

    if not os.path.exists(path):
        errors.append({"file": label, "message": "File not found"})
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        errors.append({"file": label, "message": f"Invalid JSON: {e}"})
        return None


def _file_exists(path):
    return os.path.exists(path) and os.path.isfile(path)


# ----------------------------------------------------------------------
# Workflow validation
# ----------------------------------------------------------------------
def validate_workflow(path, errors):
    data = _load_json(path, errors, file_label=os.path.basename(path))
    if not data:
        return

    # Required top-level fields
    if "nodes" not in data:
        errors.append({"file": path, "message": "Missing 'nodes' field"})
        return
    if "connections" not in data:
        errors.append({"file": path, "message": "Missing 'connections' field"})
        return

    nodes = data["nodes"]
    if not isinstance(nodes, list):
        errors.append({"file": path, "message": "'nodes' must be a list"})
        return

    # Validate node structure
    node_ids = set()
    for node in nodes:
        nid = node.get("id")
        if nid is None:
            errors.append({"file": path, "message": "Node missing 'id'"})
            continue

        node_ids.add(str(nid))

        if "type" not in node:
            errors.append({"file": path, "message": f"Node {nid} missing 'type'"})

        if "inputs" not in node:
            errors.append({"file": path, "message": f"Node {nid} missing 'inputs'"})

        if "outputs" not in node:
            errors.append({"file": path, "message": f"Node {nid} missing 'outputs'"})

    # Validate connections
    for conn in data["connections"]:
        if len(conn) < 4:
            errors.append({"file": path, "message": f"Invalid connection format: {conn}"})
            continue

        src, src_out, dst, dst_in = conn[:4]

        if str(src) not in node_ids:
            errors.append({"file": path, "message": f"Connection references missing source node {src}"})

        if str(dst) not in node_ids:
            errors.append({"file": path, "message": f"Connection references missing destination node {dst}"})


# ----------------------------------------------------------------------
# Style preset validation
# ----------------------------------------------------------------------
def validate_style_presets(errors):
    data = _load_json(PRESET_PATH, errors, "style_presets.json")
    if not data:
        return

    presets = data.get("presets", {})
    if not isinstance(presets, dict):
        errors.append({"file": "style_presets.json", "message": "'presets' must be a dict"})
        return

    for preset_id, preset in presets.items():
        # Model path
        model_path = preset.get("model")
        if model_path:
            full_path = os.path.join(MODEL_DIR, model_path)
            if not _file_exists(full_path):
                errors.append({
                    "file": "style_presets.json",
                    "message": f"Preset '{preset_id}' references missing model: {full_path}"
                })

        # LoRA paths
        loras = preset.get("loras", [])
        for lora in loras:
            full_path = os.path.join(MODEL_DIR, lora)
            if not _file_exists(full_path):
                errors.append({
                    "file": "style_presets.json",
                    "message": f"Preset '{preset_id}' references missing LoRA: {full_path}"
                })

        # Prompt template reference
        template_id = preset.get("template")
        if template_id:
            templates = _load_json(TEMPLATE_PATH, errors, "prompt_templates.json")
            if templates and template_id not in templates.get("templates", {}):
                errors.append({
                    "file": "style_presets.json",
                    "message": f"Preset '{preset_id}' references missing template '{template_id}'"
                })


# ----------------------------------------------------------------------
# Prompt template validation
# ----------------------------------------------------------------------
def validate_prompt_templates(errors):
    data = _load_json(TEMPLATE_PATH, errors, "prompt_templates.json")
    if not data:
        return

    templates = data.get("templates", {})
    if not isinstance(templates, dict):
        errors.append({"file": "prompt_templates.json", "message": "'templates' must be a dict"})
        return

    for tid, tpl in templates.items():
        if "prompt" not in tpl:
            errors.append({"file": "prompt_templates.json", "message": f"Template '{tid}' missing 'prompt'"})
        if "negative_prompt" not in tpl:
            errors.append({"file": "prompt_templates.json", "message": f"Template '{tid}' missing 'negative_prompt'"})


# ----------------------------------------------------------------------
# Workflow manifest validation
# ----------------------------------------------------------------------
def validate_manifest(errors):
    data = _load_json(MANIFEST_PATH, errors, "workflow_manifest.json")
    if not data:
        return

    workflows = data.get("workflows", [])
    if not isinstance(workflows, list):
        errors.append({"file": "workflow_manifest.json", "message": "'workflows' must be a list"})
        return

    for entry in workflows:
        path = entry.get("file")
        if not path:
            errors.append({"file": "workflow_manifest.json", "message": "Workflow entry missing 'file'"})
            continue

        full_path = os.path.join(WORKFLOW_DIR, path)
        validate_workflow(full_path, errors)


# ----------------------------------------------------------------------
# Active models validation
# ----------------------------------------------------------------------
def validate_active_models(errors):
    if not os.path.exists(ACTIVE_MODELS_PATH):
        return  # optional file

    data = _load_json(ACTIVE_MODELS_PATH, errors, "active_models.json")
    if not data:
        return

    models = data.get("models", [])
    for model in models:
        path = model.get("path")
        if path:
            full_path = os.path.join(MODEL_DIR, path)
            if not _file_exists(full_path):
                errors.append({
                    "file": "active_models.json",
                    "message": f"Missing model file: {full_path}"
                })


# ----------------------------------------------------------------------
# Master validator
# ----------------------------------------------------------------------
def validate_all():
    errors = []

    # Validate core workflow files
    validate_manifest(errors)
    validate_style_presets(errors)
    validate_prompt_templates(errors)
    validate_active_models(errors)

    return {
        "status": "ok" if not errors else "error",
        "errors": errors
    }
