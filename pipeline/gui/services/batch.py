import os
import uuid
import json
import logging
import threading
from datetime import datetime

from services.hymotion import generate_motion
from services.comfyui import generate_sprites
from services.spritesheet import assemble_spritesheet
from services.styles import get_style_preset
from services.worker_pool import WorkerPool

POOL = WorkerPool(num_workers=3)
BATCH_ROOT = "/workspace/batches"

# Per-batch locks to prevent concurrent writes
_BATCH_LOCKS = {}


def get_batch_lock(batch_id: str):
    """Return a per-batch lock, creating it if needed."""
    if batch_id not in _BATCH_LOCKS:
        _BATCH_LOCKS[batch_id] = threading.Lock()
    return _BATCH_LOCKS[batch_id]


# ----------------------------------------------------------------------
# Batch creation
# ----------------------------------------------------------------------
def create_batch(motions, characters, styles):
    batch_id = str(uuid.uuid4())[:8]
    batch_dir = os.path.join(BATCH_ROOT, batch_id)
    os.makedirs(batch_dir, exist_ok=True)

    jobs = []
    job_index = 1

    for motion in motions:
        for character in characters:
            for style in styles:
                jobs.append({
                    "id": f"job_{job_index:03d}",
                    "motion": motion,
                    "character": character,
                    "style": style,
                    "status": "pending",
                    "result": None,
                    "error": None
                })
                job_index += 1

    batch_meta = {
        "batch_id": batch_id,
        "created": datetime.utcnow().isoformat(),
        "jobs": jobs,
        "completed": 0,
        "failed": 0
    }

    save_batch(batch_id, batch_meta)
    logging.info(f"[Batch] Created batch {batch_id} with {len(jobs)} jobs")
    return batch_meta


# ----------------------------------------------------------------------
# Batch file helpers
# ----------------------------------------------------------------------
def load_batch(batch_id: str):
    path = os.path.join(BATCH_ROOT, batch_id, "batch.json")
    if not os.path.exists(path):
        logging.warning(f"[Batch] Batch not found: {batch_id}")
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[Batch] Failed to load batch {batch_id}: {e}")
        return None


def save_batch(batch_id: str, meta: dict):
    """Thread-safe write of batch metadata."""
    batch_dir = os.path.join(BATCH_ROOT, batch_id)
    os.makedirs(batch_dir, exist_ok=True)
    path = os.path.join(batch_dir, "batch.json")

    lock = get_batch_lock(batch_id)
    with lock:
        try:
            with open(path, "w") as f:
                json.dump(meta, f, indent=4)
        except Exception as e:
            logging.error(f"[Batch] Failed to save batch {batch_id}: {e}")


# ----------------------------------------------------------------------
# Synchronous batch execution
# ----------------------------------------------------------------------
def run_batch(batch_id: str):
    meta = load_batch(batch_id)
    if not meta:
        return None

    for job in meta["jobs"]:
        if job["status"] != "pending":
            continue

        run_job(batch_id, job)
        save_batch(batch_id, meta)

    return meta


# ----------------------------------------------------------------------
# Asynchronous batch execution
# ----------------------------------------------------------------------
def run_batch_async(batch_id: str):
    meta = load_batch(batch_id)
    if not meta:
        return None

    for job in meta["jobs"]:
        if job["status"] == "pending":
            POOL.submit(run_job, batch_id, job)

    return meta


# ----------------------------------------------------------------------
# Job execution
# ----------------------------------------------------------------------
def run_job(batch_id: str, job: dict):
    logging.info(f"[Batch] Starting job {job['id']} in batch {batch_id}")

    job["status"] = "running"
    job["error"] = None

    # Reload meta inside job to keep counts accurate
    meta = load_batch(batch_id)
    if not meta:
        logging.error(f"[Batch] Meta missing for batch {batch_id}")
        job["status"] = "failed"
        job["error"] = "Batch metadata missing"
        return

    # --------------------------------------------------------------
    # 1. Motion
    # --------------------------------------------------------------
    motion_result = generate_motion(job["motion"], None)
    if not motion_result or motion_result.get("status") != "success":
        job["status"] = "failed"
        job["error"] = "HY-Motion failed"
        _update_counts(meta, job)
        save_batch(batch_id, meta)
        return

    frames_dir = motion_result.get("frames")
    if not frames_dir or not os.path.exists(frames_dir):
        job["status"] = "failed"
        job["error"] = "No frames produced by HY-Motion"
        _update_counts(meta, job)
        save_batch(batch_id, meta)
        return

    # --------------------------------------------------------------
    # 2. Style
    # --------------------------------------------------------------
    style_data = get_style_preset(job["style"])
    if not style_data:
        job["status"] = "failed"
        job["error"] = f"Invalid style preset: {job['style']}"
        _update_counts(meta, job)
        save_batch(batch_id, meta)
        return

    # --------------------------------------------------------------
    # 3. Sprite frames
    # --------------------------------------------------------------
    sprite_result = generate_sprites(frames_dir, job["character"], style_data)
    if not sprite_result or sprite_result.get("status") != "success":
        job["status"] = "failed"
        job["error"] = "Sprite generation failed"
        _update_counts(meta, job)
        save_batch(batch_id, meta)
        return

    # --------------------------------------------------------------
    # 4. Sprite sheet
    # --------------------------------------------------------------
    sheet_result = assemble_spritesheet(
        sprite_result["output_dir"],
        job["character"]
    )
    if not sheet_result or sheet_result.get("status") != "success":
        job["status"] = "failed"
        job["error"] = "Sprite sheet assembly failed"
        _update_counts(meta, job)
        save_batch(batch_id, meta)
        return

    # --------------------------------------------------------------
    # Success
    # --------------------------------------------------------------
    job["status"] = "done"
    job["result"] = {
        "motion": motion_result,
        "sprites": sprite_result,
        "sheet": sheet_result
    }

    logging.info(f"[Batch] Job {job['id']} in batch {batch_id} completed successfully")

    _update_counts(meta, job)
    save_batch(batch_id, meta)


def _update_counts(meta: dict, job: dict):
    """Update completed/failed counters based on job status."""
    if "completed" not in meta:
        meta["completed"] = 0
    if "failed" not in meta:
        meta["failed"] = 0

    if job["status"] == "done":
        meta["completed"] += 1
    elif job["status"] == "failed":
        meta["failed"] += 1
