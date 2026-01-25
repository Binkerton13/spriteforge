import os
import logging

MODEL_ROOT = "/workspace/models"

# ComfyUI-standard model folders
MODEL_TYPES = {
    "checkpoints": "checkpoints",
    "loras": "loras",
    "vae": "vae",
    "controlnet": "controlnet",
    "ipadapter": "ipadapter",
    "clip": "clip",
    "embeddings": "embeddings",
    "upscale": "upscale_models"
}

VALID_EXTENSIONS = (".safetensors", ".ckpt", ".pth")


def _safe_listdir(path):
    """Safely list files in a directory."""
    try:
        return os.listdir(path)
    except Exception as e:
        logging.error(f"[ModelManager] Failed to list directory {path}: {e}")
        return []


def list_models():
    """
    Returns a dictionary of all model types and their files.
    """
    result = {}

    for key, folder in MODEL_TYPES.items():
        path = os.path.join(MODEL_ROOT, folder)
        os.makedirs(path, exist_ok=True)

        files = [
            f for f in _safe_listdir(path)
            if os.path.isfile(os.path.join(path, f))
            and f.lower().endswith(VALID_EXTENSIONS)
        ]

        files.sort()
        result[key] = files

        logging.info(f"[ModelManager] {key}: {len(files)} models found in {path}")

    return result


def list_models_by_type(model_type: str):
    """
    Returns a list of models for a specific type.
    """
    if model_type not in MODEL_TYPES:
        logging.warning(f"[ModelManager] Invalid model type requested: {model_type}")
        return None

    folder = MODEL_TYPES[model_type]
    path = os.path.join(MODEL_ROOT, folder)
    os.makedirs(path, exist_ok=True)

    files = [
        f for f in _safe_listdir(path)
        if os.path.isfile(os.path.join(path, f))
        and f.lower().endswith(VALID_EXTENSIONS)
    ]

    files.sort()

    logging.info(f"[ModelManager] Listed {len(files)} models for type: {model_type} in {path}")
    return files
