import os
import uuid
import subprocess
import logging
from datetime import datetime

HY_MOTION_DIR = "/workspace/hy-motion"
OUTPUT_ROOT = "/workspace/animations"


def generate_motion(prompt: str, skeleton: str = "human", seed: int | None = None):
    """
    Runs HY-Motion using a structured text prompt instead of a preset.
    Writes the prompt to a temporary file and passes it to inference.py.
    """

    run_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(OUTPUT_ROOT, run_id)
    os.makedirs(output_dir, exist_ok=True)

    logging.info(f"[HY-Motion] Starting run {run_id} skeleton={skeleton} seed={seed}")

    # ----------------------------------------------------------------------
    # Write prompt to a temporary file
    # ----------------------------------------------------------------------
    prompt_path = os.path.join(output_dir, "prompt.txt")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    logging.info(f"[HY-Motion] Prompt written to {prompt_path}")

    # ----------------------------------------------------------------------
    # HY-Motion command
    # ----------------------------------------------------------------------
    command = [
        "python",
        os.path.join(HY_MOTION_DIR, "inference.py"),
        "--prompt", prompt_path,
        "--skeleton", skeleton,
        "--output", output_dir
    ]

    if seed is not None:
        command += ["--seed", str(seed)]

    logging.info(f"[HY-Motion] Command: {' '.join(command)}")

    # ----------------------------------------------------------------------
    # Execute HY-Motion
    # ----------------------------------------------------------------------
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"[HY-Motion] Failed: {e}")
        return {
            "status": "error",
            "run_id": run_id,
            "error": str(e),
            "output_dir": output_dir
        }

    # ----------------------------------------------------------------------
    # Validate expected outputs
    # ----------------------------------------------------------------------
    video_path = os.path.join(output_dir, "output.mp4")
    frames_dir = os.path.join(output_dir, "frames")

    if not os.path.exists(video_path):
        logging.warning(f"[HY-Motion] Missing video output: {video_path}")

    if not os.path.exists(frames_dir):
        logging.warning(f"[HY-Motion] Missing frames directory: {frames_dir}")
    else:
        frame_files = [
            f for f in os.listdir(frames_dir)
            if f.lower().endswith((".png", ".jpg"))
        ]
        if not frame_files:
            logging.warning(f"[HY-Motion] Frames directory is empty: {frames_dir}")

    # ----------------------------------------------------------------------
    # Build result
    # ----------------------------------------------------------------------
    result = {
        "status": "success",
        "run_id": run_id,
        "skeleton": skeleton,
        "seed": seed,
        "prompt_file": prompt_path,
        "video": video_path if os.path.exists(video_path) else None,
        "frames": frames_dir if os.path.exists(frames_dir) else None,
        "output_dir": output_dir,
        "timestamp": datetime.utcnow().isoformat()
    }

    logging.info(f"[HY-Motion] Completed run {run_id}: {result}")

    return result
