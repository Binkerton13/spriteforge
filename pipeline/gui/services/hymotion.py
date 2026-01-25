import os
import uuid
import subprocess
import logging
from datetime import datetime

HY_MOTION_DIR = "/workspace/hy-motion"
OUTPUT_ROOT = "/workspace/animations"


def generate_motion(preset: str, seed: int | None = None):
    """
    Runs HY-Motion with the given preset and optional seed.
    Returns a dictionary with output paths and metadata.
    """

    run_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(OUTPUT_ROOT, run_id)
    os.makedirs(output_dir, exist_ok=True)

    logging.info(f"[HY-Motion] Starting run {run_id} preset={preset} seed={seed}")

    # ----------------------------------------------------------------------
    # HY-Motion command
    # ----------------------------------------------------------------------
    command = [
        "python",
        os.path.join(HY_MOTION_DIR, "inference.py"),
        "--preset", preset,            # placeholder
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
        # Check if frames directory is empty
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
        "preset": preset,
        "seed": seed,
        "video": video_path if os.path.exists(video_path) else None,
        "frames": frames_dir if os.path.exists(frames_dir) else None,
        "output_dir": output_dir,
        "timestamp": datetime.utcnow().isoformat()
    }

    logging.info(f"[HY-Motion] Completed run {run_id}: {result}")

    return result
