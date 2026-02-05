# services/spritesheet.py
import os
import uuid
import logging
from PIL import Image
from datetime import datetime
import json

PROJECT_ROOT = "/workspace/pipeline/projects"


def assemble_spritesheet(project_id: str, frames: list, stride: int = 1):
    """
    frames: list of absolute frame paths
    stride: 1 = every frame, 2 = every 2nd frame, etc.
    """

    frames = frames[::stride]
    if not frames:
        return {"status": "error", "message": "No frames after stride filtering"}

    run_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(PROJECT_ROOT, project_id, "sprites", run_id)
    os.makedirs(output_dir, exist_ok=True)

    logging.info(f"[SpriteForge] Assembling sheet for project {project_id} (stride={stride})")

    images = [Image.open(f).convert("RGBA") for f in frames]

    w, h = images[0].size
    sheet = Image.new("RGBA", (w * len(images), h))

    for i, img in enumerate(images):
        sheet.paste(img, (i * w, 0))

    sheet_path = os.path.join(output_dir, "sheet.png")
    sheet.save(sheet_path)

    metadata = {
        "project_id": project_id,
        "run_id": run_id,
        "frame_width": w,
        "frame_height": h,
        "num_frames": len(images),
        "frames": frames,
        "sheet_path": sheet_path,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)

    return {
        "status": "success",
        "sheet": sheet_path,
        "metadata": metadata
    }
