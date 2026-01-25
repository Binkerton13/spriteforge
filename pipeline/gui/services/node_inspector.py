import json
import os
import logging

WORKFLOW_DIR = "/workspace/pipeline/workflows"


def load_workflow_json(name: str):
    """Safely load a workflow JSON file."""
    path = os.path.join(WORKFLOW_DIR, os.path.basename(name))

    if not os.path.exists(path):
        logging.warning(f"[NodeInspector] Workflow not found: {name}")
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[NodeInspector] Failed to load workflow {name}: {e}")
        return None


def list_nodes(workflow_name: str):
    """Return a list of nodes with id + type."""
    data = load_workflow_json(workflow_name)
    if not data:
        return None

    nodes = data.get("nodes", [])
    if not isinstance(nodes, list):
        logging.error("[NodeInspector] Invalid workflow: 'nodes' must be a list")
        return None

    result = []
    for node in nodes:
        nid = str(node.get("id"))
        ntype = node.get("type") or node.get("class_type")
        result.append({"id": nid, "type": ntype})

    return result


def get_node_details(workflow_name: str, node_id: str):
    """Return full details for a specific node."""
    data = load_workflow_json(workflow_name)
    if not data:
        return None

    nodes = data.get("nodes", [])
    if not isinstance(nodes, list):
        logging.error("[NodeInspector] Invalid workflow: 'nodes' must be a list")
        return None

    # Normalize node_id to string for comparison
    node_id = str(node_id)

    # Find node
    node = None
    for n in nodes:
        if str(n.get("id")) == node_id:
            node = n
            break

    if not node:
        logging.warning(f"[NodeInspector] Node not found: {node_id}")
        return None

    connections = data.get("connections", [])
    incoming = []
    outgoing = []

    for conn in connections:
        # Support variable-length connection tuples
        if len(conn) < 4:
            continue

        src, src_out, dst, dst_in = conn[:4]

        if str(dst) == node_id:
            incoming.append({
                "from": str(src),
                "output": src_out,
                "input": dst_in
            })

        if str(src) == node_id:
            outgoing.append({
                "to": str(dst),
                "output": src_out,
                "input": dst_in
            })

    return {
        "id": node_id,
        "type": node.get("type") or node.get("class_type"),
        "inputs": node.get("inputs", {}),
        "outputs": node.get("outputs", {}),
        "incoming": incoming,
        "outgoing": outgoing
    }
