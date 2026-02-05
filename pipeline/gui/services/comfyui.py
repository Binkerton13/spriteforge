# services/comfyui.py
import os
import uuid
import time
import json
import logging
import requests

COMFYUI_URL = "http://127.0.0.1:8188"


def trigger_workflow(workflow: dict, inputs: dict):
    payload = {
        "prompt": workflow,
        "extra_data": inputs
    }

    try:
        r = requests.post(f"{COMFYUI_URL}/prompt", json=payload)
        r.raise_for_status()
        return r.json().get("prompt_id")
    except Exception as e:
        logging.error(f"[ComfyUI] Failed to trigger workflow: {e}")
        return None


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


def generate_sprites(workflow: dict, inputs: dict):
    """
    Runs a ComfyUI workflow with runtime inputs:
      - motion frames
      - refined prompt
      - reference images
      - stride
      - settings
    """

    project_id = inputs.get("project_id")
    run_id = str(uuid.uuid4())[:8]

    logging.info(f"[SpriteForge] Starting sprite workflow run {run_id} for project {project_id}")

    inputs["run_id"] = run_id

    prompt_id = trigger_workflow(workflow, inputs)
    if not prompt_id:
        return {"status": "error", "message": "Failed to trigger ComfyUI workflow"}

    result = wait_for_result(prompt_id)
    if not result:
        return {
            "status": "error",
            "message": "ComfyUI workflow timed out",
            "prompt_id": prompt_id
        }

    logging.info(f"[SpriteForge] Sprite workflow complete: run_id={run_id}")

    return {
        "status": "success",
        "run_id": run_id,
        "prompt_id": prompt_id,
        "result": result
    }
