import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

WORKFLOW_DIR = "/workspace/pipeline/workflows"


def _load_json(path: str) -> Optional[Dict[str, Any]]:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _atomic_write(path: str, data: Dict[str, Any]) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    os.replace(tmp, path)


def repair_workflow(path: str) -> Dict[str, Any]:
    """
    Attempt to auto-repair a ComfyUI workflow JSON.
    Returns the repaired data (not yet written).
    Raises FileNotFoundError if the file does not exist.
    """
    data = _load_json(path)
    if data is None:
        raise FileNotFoundError(path)

    repairs: List[str] = []

    # --- Ensure nodes + connections exist ---
    raw_nodes = data.get("nodes", [])
    connections = data.get("connections", [])

    # Handle dict-style nodes -> list-style nodes
    if isinstance(raw_nodes, dict):
        repairs.append("Converted dict-style 'nodes' to list-style 'nodes'")
        nodes: List[Dict[str, Any]] = []
        for nid_str, node in raw_nodes.items():
            try:
                nid = int(nid_str)
            except ValueError:
                # Fallback: assign later
                nid = None
            node = dict(node)  # shallow copy
            if nid is not None:
                node["id"] = nid
            nodes.append(node)
        data["nodes"] = nodes
    elif isinstance(raw_nodes, list):
        nodes = raw_nodes
    else:
        repairs.append("Replaced invalid 'nodes' with empty list")
        nodes = []
        data["nodes"] = nodes

    # Ensure connections is a list
    if not isinstance(connections, list):
        repairs.append("Replaced invalid 'connections' with empty list")
        connections = []
        data["connections"] = connections

    # --- Normalize nodes ---
    node_ids: List[int] = []

    # First pass: collect existing numeric IDs
    for node in nodes:
        nid = node.get("id")
        if isinstance(nid, int):
            node_ids.append(nid)

    # Helper to get next ID
    def next_id() -> int:
        return (max(node_ids) + 1) if node_ids else 1

    for node in nodes:
        nid = node.get("id")
        if not isinstance(nid, int):
            nid = next_id()
            node["id"] = nid
            node_ids.append(nid)
            repairs.append(f"Assigned new id {nid} to node missing or invalid 'id'")

        # Normalize class_type -> type
        if "type" not in node and "class_type" in node:
            node["type"] = node.pop("class_type")
            repairs.append(f"Node {nid} converted 'class_type' → 'type'")

        if "type" not in node:
            node["type"] = "UnknownNode"
            repairs.append(f"Node {nid} missing 'type', set to 'UnknownNode'")

        if not isinstance(node.get("inputs"), dict):
            node["inputs"] = {}
            repairs.append(f"Node {nid} missing or invalid 'inputs', set to {{}}")

        if not isinstance(node.get("outputs"), dict):
            node["outputs"] = {}
            repairs.append(f"Node {nid} missing or invalid 'outputs', set to {{}}")

    # Sort nodes by ID for stable diffs
    nodes.sort(key=lambda n: n["id"])
    data["nodes"] = nodes
    node_id_set = set(node_ids)

    # --- Normalize connections ---
    valid_connections: List[List[Any]] = []
    for conn in connections:
        if not isinstance(conn, (list, tuple)) or len(conn) < 4:
            repairs.append(f"Removed invalid connection (len<4 or not list): {conn}")
            continue

        src, src_out, dst, dst_in = conn[:4]

        # Coerce src/dst to int
        try:
            src_int = int(src)
            dst_int = int(dst)
        except (TypeError, ValueError):
            repairs.append(f"Removed connection {conn} (non-numeric node IDs)")
            continue

        if src_int not in node_id_set:
            repairs.append(f"Removed connection {conn} (missing source node {src_int})")
            continue
        if dst_int not in node_id_set:
            repairs.append(f"Removed connection {conn} (missing destination node {dst_int})")
            continue

        valid_connections.append([src_int, src_out, dst_int, dst_in])

    if len(valid_connections) != len(connections):
        data["connections"] = valid_connections
        repairs.append("Pruned invalid connections")

    # TODO: inject required variables here if desired
    # e.g., ensure @frames_dir, @output_dir, @prompt, etc.

    # Attach repair metadata
    data["_repairs"] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "actions": repairs,
        "source": os.path.basename(path),
    }

    return data


def repair_workflow_file(name: str) -> Dict[str, Any]:
    """
    Convenience wrapper: repair a workflow by name in WORKFLOW_DIR
    and write it back atomically. Returns the repaired data.
    """
    path = os.path.join(WORKFLOW_DIR, name)
    repaired = repair_workflow(path)
    _atomic_write(path, repaired)
    return repaired
