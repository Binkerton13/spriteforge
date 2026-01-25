import os
import uuid
import time
import json
import logging
import requests

COMFYUI_URL = "http://127.0.0.1:8188"
WORKFLOW_DIR = "/workspace/pipeline/workflows"
SPRITE_OUTPUT_ROOT = "/workspace/sprites"


# ------------------------------------------------------------------------------
# Trigger a ComfyUI workflow
# ------------------------------------------------------------------------------
def trigger_workflow(workflow: dict, inputs: dict):
    payload = {
        "prompt": workflow,
        "extra_data": inputs
    }

    try:
        r = requests.post(f"{COMFYUI_URL}/prompt", json=payload)
        r.raise_for_status()
        data = r.json()
        return data.get("prompt_id")
    except Exception as e:
        logging.error(f"[ComfyUI] Failed to trigger workflow: {e}")
        return None


# ------------------------------------------------------------------------------
# Poll ComfyUI for results
# ------------------------------------------------------------------------------
def wait_for_result(prompt_id: str, timeout=300):
    start = time.time()

    while time.time() - start < timeout:
        try:
            r = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
            if r.status_code == 200:
                data = r.json()
                if prompt_id in data:
                    return data[prompt_id]
        except Exception:
            pass

        time.sleep(1)

    return None


# ------------------------------------------------------------------------------
# Main SpriteForge → ComfyUI integration
# ------------------------------------------------------------------------------
def generate_sprites(frames_dir: str, character_name: str, style: dict):
    """
    Runs a ComfyUI workflow that takes HY-Motion frames and generates sprites.
    Returns output directory + workflow results.
    """
    from services.model_selection import load_selection
    from services.prompts import get_template

    run_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(SPRITE_OUTPUT_ROOT, run_id)
    os.makedirs(output_dir, exist_ok=True)

    logging.info(f"[SpriteForge] Starting sprite generation run {run_id}")

    # ----------------------------------------------------------------------
    # Merge style preset + active model selection
    # ----------------------------------------------------------------------
    active_models = load_selection()
    merged = {**active_models, **(style or {})}

    # ----------------------------------------------------------------------
    # Prompt template
    # ----------------------------------------------------------------------
    template_id = merged.get("prompt_template")
    template = get_template(template_id) if template_id else None

    prompt = template.get("prompt") if template else ""
    negative_prompt = template.get("negative_prompt") if template else ""

    # ----------------------------------------------------------------------
    # Load workflow JSON
    # ----------------------------------------------------------------------
    workflow_path = os.path.join(WORKFLOW_DIR, "sprite_workflow.json")

    if not os.path.exists(workflow_path):
        return {
            "status": "error",
            "message": f"Missing workflow file: {workflow_path}"
        }

    with open(workflow_path, "r") as f:
        workflow_str = f.read()

    # ----------------------------------------------------------------------
    # Inject variables
    # ----------------------------------------------------------------------
    replacements = {
        "@frames_dir": frames_dir,
        "@character_name": character_name,
        "@output_dir": output_dir,
        "@checkpoint": merged.get("checkpoint", ""),
        "@lora": merged.get("lora", ""),
        "@vae": merged.get("vae", ""),
        "@controlnet": merged.get("controlnet", ""),
        "@ipadapter": merged.get("ipadapter", ""),
        "@sampler": merged.get("sampler", "euler"),
        "@cfg_scale": str(merged.get("cfg_scale", 1.0)),
        "@prompt": prompt,
        "@negative_prompt": negative_prompt
    }

    for key, value in replacements.items():
        workflow_str = workflow_str.replace(key, value)

    workflow = json.loads(workflow_str)

    # ----------------------------------------------------------------------
    # Prepare inputs for ComfyUI
    # ----------------------------------------------------------------------
    inputs = {
        "frames_dir": frames_dir,
        "character_name": character_name,
        "output_dir": output_dir
    }

    # ----------------------------------------------------------------------
    # Trigger workflow
    # ----------------------------------------------------------------------
    prompt_id = trigger_workflow(workflow, inputs)
    if not prompt_id:
        return {
            "status": "error",
            "message": "Failed to trigger ComfyUI workflow"
        }

    logging.info(f"[ComfyUI] Workflow triggered: prompt_id={prompt_id}")

    # ----------------------------------------------------------------------
    # Wait for results
    # ----------------------------------------------------------------------
    result = wait_for_result(prompt_id)
    if not result:
        return {
            "status": "error",
            "message": "ComfyUI workflow timed out",
            "prompt_id": prompt_id
        }

    logging.info(f"[SpriteForge] Sprite generation complete: {output_dir}")

    # ----------------------------------------------------------------------
    # Return structured result
    # ----------------------------------------------------------------------
    return {
        "status": "success",
        "run_id": run_id,
        "character": character_name,
        "frames_dir": frames_dir,
        "output_dir": output_dir,
        "prompt_id": prompt_id,
        "result": result
    }
