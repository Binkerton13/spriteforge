# services/reference_descriptor.py
import os
import logging
from typing import List, Dict

PROJECT_ROOT = "/workspace/pipeline/projects"


def _reference_dir(project_id: str) -> str:
    path = os.path.join(PROJECT_ROOT, project_id, "references")
    os.makedirs(path, exist_ok=True)
    return path


def save_reference_file(project_id: str, file_storage) -> Dict:
    """
    Save an uploaded reference image into the project references folder.
    Returns metadata including serverPath for frontend use.
    """
    ref_dir = _reference_dir(project_id)
    filename = file_storage.filename
    path = os.path.join(ref_dir, filename)

    file_storage.save(path)
    logging.info(f"[Reference] Saved reference image for {project_id}: {path}")

    return {
        "filename": filename,
        "serverPath": path,
    }


def describe_reference_images(paths: List[str]) -> List[Dict]:
    """
    Given a list of absolute image paths, return structured descriptions.
    Stub implementation for now; later you can plug in a real vision model.
    """
    descriptions = []

    for p in paths:
        # TODO: replace this with actual vision model output
        descriptions.append({
            "path": p,
            "summary": "Character reference image",
            "style": "unknown",
            "palette": [],
            "clothing": [],
            "silhouette": "unknown",
            "lighting": "unknown",
        })

    return descriptions
