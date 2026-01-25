import os
import json
import logging

WORKFLOW_DIR = "/workspace/pipeline/workflows"

# Files that should NOT appear in the workflow list
EXCLUDED_FILES = {
    "style_presets.json",
    "prompt_templates.json",
    "active_models.json",
    "workflow_manifest.json"
}


def _safe_json_load(path):
    """Safely load JSON with error handling."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[Workflows] Failed to load JSON {path}: {e}")
        return None


def _sanitize_name(name: str):
    """Prevent directory traversal."""
    return os.path.basename(name)


def list_workflows():
    """Return only valid workflow JSON files."""
    try:
        files = os.listdir(WORKFLOW_DIR)
    except Exception as e:
        logging.error(f"[Workflows] Failed to list workflow directory: {e}")
        return []

    workflows = [
        f for f in files
        if f.endswith(".json")
        and f not in EXCLUDED_FILES
        and not f.startswith("project_")
    ]

    workflows.sort()
    logging.info(f"[Workflows] Found {len(workflows)} workflows")
    return workflows


def load_workflow(name: str):
    """Load a workflow JSON file safely."""
    name = _sanitize_name(name)
    path = os.path.join(WORKFLOW_DIR, name)

    if not os.path.exists(path):
        logging.warning(f"[Workflows] Workflow not found: {name}")
        return None

    data = _safe_json_load(path)
    if data is None:
        return None

    logging.info(f"[Workflows] Loaded workflow: {name}")
    return data


def save_workflow(name: str, data: dict):
    """Save a workflow JSON file safely."""
    name = _sanitize_name(name)
    path = os.path.join(WORKFLOW_DIR, name)

    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"[Workflows] Saved workflow: {name}")
        return True
    except Exception as e:
        logging.error(f"[Workflows] Failed to save workflow {name}: {e}")
        return False


def validate_workflow(data: dict):
    """
    Validate workflow structure.
    Must contain:
      - nodes: list
      - connections: list
    Each node must contain:
      - id
      - type
      - inputs
      - outputs
    """
    if not isinstance(data, dict):
        return False, "Workflow must be a JSON object"

    if "nodes" not in data:
        return False, "Missing 'nodes' field"
    if "connections" not in data:
        return False, "Missing 'connections' field"

    nodes = data["nodes"]
    if not isinstance(nodes, list):
        return False, "'nodes' must be a list"

    for node in nodes:
        if "id" not in node:
            return False, "Node missing 'id'"
        if "type" not in node:
            return False, f"Node {node.get('id')} missing 'type'"
        if "inputs" not in node:
            return False, f"Node {node.get('id')} missing 'inputs'"
        if "outputs" not in node:
            return False, f"Node {node.get('id')} missing 'outputs'"

    logging.info("[Workflows] Workflow validated successfully")
    return True, "Workflow is valid"
