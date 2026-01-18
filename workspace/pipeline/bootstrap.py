"""
bootstrap.py
------------
Creates the full project pipeline folder structure with user-specified project name.

This script is:
- Idempotent (safe to run multiple times)
- Non-destructive (never overwrites existing files)
- Copilot-friendly (clean, explicit, modular)
- Project-aware (accepts custom project name)

Usage:
    # Create structure in current directory with default name
    python bootstrap.py
    
    # Create structure with custom project name
    python bootstrap.py --project MyCharacter
    
    # Create structure in specific location
    python bootstrap.py --root /path/to/workspace --project MyCharacter
"""

import argparse
from pathlib import Path


# ---------------------------------------------------------
# Utility: Create a directory if missing
# ---------------------------------------------------------
def ensure(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"[✔] Created: {path}")
    else:
        print(f"[=] Exists:  {path}")


# ---------------------------------------------------------
# Main folder creation logic
# ---------------------------------------------------------
def create_structure(root: Path, project_name: str = "Exhibition"):
    """
    Creates the full pipeline folder structure for a 3D character project.
    
    Args:
        root: Base directory where project will be created
        project_name: Name of the project (user-specified or default)
    
    Returns:
        Path to the created project directory
    """
    print(f"\n=== BOOTSTRAPPING {project_name.upper()} PIPELINE ===\n")
    print(f"Project root: {root}")
    print(f"Project name: {project_name}\n")

    # 0_input
    ensure(root / "0_input/meshes")
    ensure(root / "0_input/uv_layouts")
    ensure(root / "0_input/references")

    # 1_textures
    ensure(root / "1_textures")
    ensure(root / "1_textures/udim_material")

    # 2_rig
    ensure(root / "2_rig/scripts")
    ensure(root / "2_rig/config")
    ensure(root / "2_rig/autorig_output")
    ensure(root / "2_rig/rigui")

    # 3_animation
    ensure(root / "3_animation/deform_fix")
    ensure(root / "3_animation/hy_motion")
    ensure(root / "3_animation/hy_motion/single_output")
    ensure(root / "3_animation/hy_motion/batch_output")
    ensure(root / "3_animation/hy_motion/scripts")
    ensure(root / "3_animation/hy_motion/ui")
    ensure(root / "3_animation/retargeted")

    # 4_export
    ensure(root / "4_export")
    ensure(root / "4_export/fbx")
    ensure(root / "4_export/gltf")
    ensure(root / "4_export/usd")
    
    # config (project-level settings)
    ensure(root / "config")

    # pipeline
    ensure(root / "pipeline/tools")
    ensure(root / "pipeline/comfyui_workflows")
    ensure(root / "pipeline/hy_motion_prompts")

    print(f"\n[✔] Bootstrap complete for project: {project_name}\n")
    
    return root


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap 3D character pipeline structure"
    )
    parser.add_argument(
        "--project",
        "-p",
        default="Exhibition",
        help="Project name (default: Exhibition)"
    )
    parser.add_argument(
        "--root",
        "-r",
        type=Path,
        default=None,
        help="Root directory (default: parent of current script)"
    )
    
    args = parser.parse_args()
    
    # Determine root directory
    if args.root:
        root = args.root.resolve()
    else:
        # Default: parent directory of this script
        root = Path(__file__).resolve().parents[1]
    
    # Ensure root exists
    root.mkdir(parents=True, exist_ok=True)
    
    # Create project structure
    project_root = create_structure(root, args.project)
    
    print(f"[✔] Project '{args.project}' ready at: {project_root}")


if __name__ == "__main__":
    main()
