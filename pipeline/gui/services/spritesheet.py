import os
import uuid
import logging
from PIL import Image, UnidentifiedImageError
from datetime import datetime
import json

SPRITE_OUTPUT_ROOT = "/workspace/sprites"


def assemble_spritesheet(frames_dir: str, character_name: str):
    """
    Takes a directory of frames and assembles them into a sprite sheet.
    Returns paths to the sheet and metadata.
    """

    # ----------------------------------------------------------------------
    # Validate input directory
    # ----------------------------------------------------------------------
    if not os.path.exists(frames_dir):
        return {
            "status": "error",
            "message": f"Frames directory does not exist: {frames_dir}",
            "frames_dir": frames_dir
        }

    run_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(SPRITE_OUTPUT_ROOT, run_id)
    os.makedirs(output_dir, exist_ok=True)

    logging.info(f"[SpriteForge] Assembling sprite sheet for {character_name} from {frames_dir}")

    # ----------------------------------------------------------------------
    # Collect frames
    # ----------------------------------------------------------------------
    frame_files = sorted([
        os.path.join(frames_dir, f)
        for f in os.listdir(frames_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    if not frame_files:
        return {
            "status": "error",
            "message": "No frames found in directory",
            "frames_dir": frames_dir
        }

    # Warn about JPEG frames
    if any(f.lower().endswith(".jpg") or f.lower().endswith(".jpeg") for f in frame_files):
        logging.warning("[SpriteForge] JPEG frames detected — transparency may be lost.")

    # ----------------------------------------------------------------------
    # Load images safely
    # ----------------------------------------------------------------------
    images = []
    for f in frame_files:
        try:
            img = Image.open(f).convert("RGBA")
            images.append(img)
        except UnidentifiedImageError:
            logging.error(f"[SpriteForge] Corrupted or unreadable frame: {f}")
            return {
                "status": "error",
                "message": f"Corrupted or unreadable frame: {f}",
                "frames_dir": frames_dir
            }

    # ----------------------------------------------------------------------
    # Validate consistent dimensions
    # ----------------------------------------------------------------------
    frame_width, frame_height = images[0].size
    for img in images:
        if img.size != (frame_width, frame_height):
            logging.error("[SpriteForge] Inconsistent frame sizes detected.")
            return {
                "status": "error",
                "message": "Frames have inconsistent dimensions",
                "frames_dir": frames_dir
            }

    num_frames = len(images)
    logging.info(f"[SpriteForge] {num_frames} frames loaded ({frame_width}x{frame_height})")

    # ----------------------------------------------------------------------
    # Create sheet (single row for now)
    # ----------------------------------------------------------------------
    sheet_width = frame_width * num_frames
    sheet_height = frame_height

    sheet = Image.new("RGBA", (sheet_width, sheet_height))

    for i, img in enumerate(images):
        sheet.paste(img, (i * frame_width, 0))

    # ----------------------------------------------------------------------
    # Save sheet
    # ----------------------------------------------------------------------
    sheet_path = os.path.join(output_dir, f"{character_name}_sheet.png")
    sheet.save(sheet_path)

    # ----------------------------------------------------------------------
    # Metadata
    # ----------------------------------------------------------------------
    metadata = {
        "character": character_name,
        "run_id": run_id,
        "frame_width": frame_width,
        "frame_height": frame_height,
        "num_frames": num_frames,
        "frames_dir": frames_dir,
        "sheet_path": sheet_path,
        "timestamp": datetime.utcnow().isoformat()
    }

    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

    logging.info(f"[SpriteForge] Sprite sheet created: {sheet_path}")

    return {
        "status": "success",
        "run_id": run_id,
        "sheet": sheet_path,
        "metadata": metadata,
        "metadata_path": metadata_path,
        "output_dir": output_dir
    }
