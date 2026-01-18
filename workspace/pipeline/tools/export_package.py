"""
export_package.py
-----------------
Final packaging script for the Exhibition pipeline.

This script collects:
- The final retargeted animation (FBX)
- The rigged mesh (FBX)
- The UDIM material package
- Metadata (project.json)

Usage:
python3 export_package.py --input <retargeted_fbx> --project <project_name>
"""

import argparse
import json
import shutil
from pathlib import Path


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def copy_if_exists(src: Path, dst: Path):
    if src.exists():
        shutil.copy2(src, dst)
        print(f"[✔] Copied: {src.name}")
    else:
        print(f"[WARN] Missing file: {src}")


def build_metadata(project_name: str, output_dir: Path):
    metadata = {
        "project": project_name,
        "description": "Final packaged output from the Exhibition pipeline.",
        "contents": {
            "rig": "rig.fbx",
            "animation": "animation.fbx",
            "materials": "materials/",
        }
    }

    (output_dir / "project.json").write_text(json.dumps(metadata, indent=4))
    print("[✔] Metadata written: project.json")


def package_export(retargeted_fbx: str, project_name: str):
    retargeted_fbx = Path(retargeted_fbx)

    # Root export folder
    export_root = Path("4_export") / project_name
    ensure_dir(export_root)

    print(f"\n=== PACKAGING EXPORT: {project_name} ===")
    print("Output directory:", export_root)

    # ---------------------------------------------------------
    # 1. Copy retargeted animation
    # ---------------------------------------------------------
    anim_dst = export_root / "animation.fbx"
    copy_if_exists(retargeted_fbx, anim_dst)

    # ---------------------------------------------------------
    # 2. Copy rig (if available)
    # ---------------------------------------------------------
    rig_src = Path("2_rig/autorig_output/character_rigged_cleaned.fbx")
    rig_dst = export_root / "rig.fbx"
    copy_if_exists(rig_src, rig_dst)

    # ---------------------------------------------------------
    # 3. Copy UDIM material package
    # ---------------------------------------------------------
    udim_root = Path("1_textures/udim_material")
    udim_dst = export_root / "materials"

    if udim_root.exists():
        shutil.copytree(udim_root, udim_dst, dirs_exist_ok=True)
        print("[✔] UDIM materials copied.")
    else:
        print("[WARN] UDIM material folder not found:", udim_root)

    # ---------------------------------------------------------
    # 4. Write metadata
    # ---------------------------------------------------------
    build_metadata(project_name, export_root)

    print(f"\n[✔] Export package complete: {export_root}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Retargeted animation FBX")
    parser.add_argument("--project", required=True, help="Project name for export folder")

    args = parser.parse_args()
    package_export(args.input, args.project)


if __name__ == "__main__":
    main()
