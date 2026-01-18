#!/usr/bin/env python3
"""
project_init.py
---------------
Project initialization module for 3D-AI-Workstation integration.

This module provides multiple strategies for creating projects with user-specified
names, designed to work with both local systems and pod-based environments.

Usage Patterns:

1. Local/Workstation (Interactive):
   python project_init.py --interactive
   
2. With Project Name (CLI):
   python project_init.py --project MyCharacter --workspace /path/to/workspace
   
3. From Environment Variable (Pod):
   export PROJECT_NAME="MyCharacter"
   python project_init.py
   
4. Pod Post-Initialization:
   # Pod starts with default structure
   # User sends project name via API/command
   python project_init.py --rename Exhibition MyCharacter
"""

import argparse
import json
import os
import re
import shutil
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------
# Project Name Validation
# ---------------------------------------------------------
def validate_project_name(name: str) -> tuple[bool, str]:
    """
    Validate project name follows naming conventions.
    
    Returns:
        (is_valid, error_message)
    """
    if not name:
        return False, "Project name cannot be empty"
    
    if len(name) < 2:
        return False, "Project name must be at least 2 characters"
    
    if len(name) > 64:
        return False, "Project name must be 64 characters or less"
    
    # Allow alphanumeric, underscores, hyphens
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        return False, "Project name can only contain letters, numbers, underscores, and hyphens"
    
    # Must start with letter or number
    if not name[0].isalnum():
        return False, "Project name must start with a letter or number"
    
    return True, ""


# ---------------------------------------------------------
# Project Structure Creation
# ---------------------------------------------------------
def ensure_dir(path: Path) -> None:
    """Create directory if it doesn't exist"""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"[✔] Created: {path}")


def create_project_structure(workspace_root: Path, project_name: str) -> Path:
    """
    Create full project structure with specified name.
    
    Args:
        workspace_root: Base workspace directory
        project_name: User-specified project name
    
    Returns:
        Path to created project directory
    """
    print(f"\n=== CREATING PROJECT: {project_name} ===\n")
    
    project_root = workspace_root / project_name
    
    # Create main folders
    folders = [
        "0_input/meshes",
        "0_input/uv_layouts",
        "0_input/references",
        "1_textures/albedo",
        "1_textures/normal",
        "1_textures/roughness",
        "1_textures/metallic",
        "1_textures/ao",
        "1_textures/udim_material",
        "2_rig/scripts",
        "2_rig/config",
        "2_rig/autorig_output",
        "2_rig/rigui",
        "3_animation/deform_fix",
        "3_animation/hy_motion/single_output",
        "3_animation/hy_motion/batch_output",
        "3_animation/hy_motion/scripts",
        "3_animation/retargeted",
        "4_export/fbx",
        "4_export/gltf",
        "4_export/usd",
        "config",
        "pipeline/tools",
        "pipeline/comfyui_workflows",
        "pipeline/hy_motion_prompts",
    ]
    
    for folder in folders:
        ensure_dir(project_root / folder)
    
    print(f"\n[✔] Project structure created at: {project_root}\n")
    
    return project_root


def create_project_config(project_root: Path, project_name: str) -> None:
    """
    Create project-specific configuration file.
    
    Args:
        project_root: Root directory of the project
        project_name: Project name for configuration
    """
    config = {
        "project_name": project_name,
        "clean_fbx": "0_input/meshes/character_clean.fbx",
        "comfyui_url": "http://127.0.0.1:8188",
        "texture_workflow": "pipeline/comfyui_workflows/texture_workflow.json",
        "udim_tiles": {
            "1001": {
                "uv": "0_input/uv_layouts/character_uv_1001.png",
                "prompt": "skin texture, realistic pores",
                "negative": "distortion, artifacts",
                "seed": 12345,
                "output": "1_textures/albedo/albedo_1001.png"
            }
        },
        "pbr_outputs": {
            "1001": {
                "normal": "1_textures/normal/normal_1001.png",
                "roughness": "1_textures/roughness/roughness_1001.png",
                "metallic": "1_textures/metallic/metallic_1001.png",
                "ao": "1_textures/ao/ao_1001.png"
            }
        },
        "udim_output_root": "1_textures/udim_material",
        "unirig": {
            "executable": "2_rig/rigui/unirig.py",
            "input_mesh": "0_input/meshes/character_clean.fbx",
            "output_rig": "2_rig/autorig_output/character_rigged.fbx",
            "preset": "2_rig/config/humanoid_standard.json",
            "scale": 1.0,
            "root_bone": "Hips",
            "orientation": "Y_UP"
        },
        "rig_output": {
            "fbx": "2_rig/autorig_output/character_rigged.fbx"
        },
        "rig_output_clean": "2_rig/autorig_output/character_rigged_cleaned.fbx",
        "rig_output_smoothed": "2_rig/autorig_output/character_rigged_weightsmoothed.fbx",
        "deform_fix_workflow": "pipeline/comfyui_workflows/deform_fix_workflow.json",
        "deform_fix": {
            "pose_list": "3_animation/deform_fix/poses.json",
            "corrected_fbx": "3_animation/deform_fix/character_corrected.fbx"
        },
        "hy_motion_prompt": "3_animation/hy_motion/single_output/motion.txt",
        "hy_motion_raw_anim": "3_animation/hy_motion/raw_animation.fbx",
        "bone_mapping": "2_rig/config/bone_mapping.json",
        "retargeted_anim": "3_animation/retargeted/animation_retargeted.fbx"
    }
    
    config_path = project_root / "pipeline/config.json"
    config_path.write_text(json.dumps(config, indent=2))
    print(f"[✔] Created config: {config_path}")


# ---------------------------------------------------------
# Project Initialization Strategies
# ---------------------------------------------------------
def init_project_interactive(workspace_root: Path) -> Optional[Path]:
    """
    Interactive project creation (for workstation use).
    
    Prompts user for project name and creates structure.
    """
    print("\n=== 3D CHARACTER PIPELINE - PROJECT SETUP ===\n")
    
    while True:
        project_name = input("Enter project name: ").strip()
        
        is_valid, error = validate_project_name(project_name)
        if not is_valid:
            print(f"[✗] Invalid project name: {error}")
            continue
        
        project_path = workspace_root / project_name
        if project_path.exists():
            overwrite = input(f"[?] Project '{project_name}' already exists. Continue? (y/n): ")
            if overwrite.lower() != 'y':
                continue
        
        break
    
    # Create project
    project_root = create_project_structure(workspace_root, project_name)
    create_project_config(project_root, project_name)
    
    return project_root


def init_project_from_env(workspace_root: Path) -> Optional[Path]:
    """
    Create project from environment variable (for pod use).
    
    Reads PROJECT_NAME from environment and creates structure.
    Suitable for pod startup scripts.
    """
    project_name = os.getenv("PROJECT_NAME")
    
    if not project_name:
        print("[✗] Error: PROJECT_NAME environment variable not set")
        return None
    
    is_valid, error = validate_project_name(project_name)
    if not is_valid:
        print(f"[✗] Invalid PROJECT_NAME: {error}")
        return None
    
    print(f"[✔] Using PROJECT_NAME from environment: {project_name}")
    
    project_root = create_project_structure(workspace_root, project_name)
    create_project_config(project_root, project_name)
    
    return project_root


def init_project_with_name(workspace_root: Path, project_name: str) -> Optional[Path]:
    """
    Create project with specified name (for CLI/API use).
    
    Args:
        workspace_root: Base workspace directory
        project_name: Project name to create
    
    Returns:
        Path to created project or None if validation failed
    """
    is_valid, error = validate_project_name(project_name)
    if not is_valid:
        print(f"[✗] Invalid project name: {error}")
        return None
    
    project_root = create_project_structure(workspace_root, project_name)
    create_project_config(project_root, project_name)
    
    return project_root


def rename_existing_project(workspace_root: Path, old_name: str, new_name: str) -> Optional[Path]:
    """
    Rename existing project (for post-initialization in pod).
    
    Useful when pod creates default structure, then user specifies name.
    
    Args:
        workspace_root: Base workspace directory
        old_name: Current project name
        new_name: New project name
    
    Returns:
        Path to renamed project or None if failed
    """
    is_valid, error = validate_project_name(new_name)
    if not is_valid:
        print(f"[✗] Invalid new project name: {error}")
        return None
    
    old_path = workspace_root / old_name
    new_path = workspace_root / new_name
    
    if not old_path.exists():
        print(f"[✗] Project '{old_name}' does not exist")
        return None
    
    if new_path.exists():
        print(f"[✗] Project '{new_name}' already exists")
        return None
    
    print(f"[↻] Renaming project '{old_name}' → '{new_name}'...")
    
    # Rename directory
    shutil.move(str(old_path), str(new_path))
    
    # Update config file with new project name
    config_path = new_path / "pipeline/config.json"
    if config_path.exists():
        config = json.loads(config_path.read_text())
        config["project_name"] = new_name
        config_path.write_text(json.dumps(config, indent=2))
    
    print(f"[✔] Project renamed successfully: {new_path}")
    
    return new_path


# ---------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Initialize 3D character pipeline project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (prompt for name)
  python project_init.py --interactive
  
  # Create with specific name
  python project_init.py --project MyCharacter
  
  # Use environment variable
  export PROJECT_NAME="MyCharacter"
  python project_init.py --from-env
  
  # Rename existing project
  python project_init.py --rename Exhibition MyCharacter
        """
    )
    
    parser.add_argument(
        "--workspace",
        "-w",
        type=Path,
        default=Path.cwd(),
        help="Workspace root directory (default: current directory)"
    )
    
    parser.add_argument(
        "--project",
        "-p",
        help="Project name to create"
    )
    
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive mode: prompt for project name"
    )
    
    parser.add_argument(
        "--from-env",
        action="store_true",
        help="Read project name from PROJECT_NAME environment variable"
    )
    
    parser.add_argument(
        "--rename",
        nargs=2,
        metavar=("OLD_NAME", "NEW_NAME"),
        help="Rename existing project"
    )
    
    args = parser.parse_args()
    
    workspace_root = args.workspace.resolve()
    workspace_root.mkdir(parents=True, exist_ok=True)
    
    # Determine which initialization strategy to use
    project_root = None
    
    if args.rename:
        old_name, new_name = args.rename
        project_root = rename_existing_project(workspace_root, old_name, new_name)
    elif args.interactive:
        project_root = init_project_interactive(workspace_root)
    elif args.from_env:
        project_root = init_project_from_env(workspace_root)
    elif args.project:
        project_root = init_project_with_name(workspace_root, args.project)
    else:
        # Default: try environment variable, fall back to interactive
        project_name = os.getenv("PROJECT_NAME")
        if project_name:
            print("[i] Found PROJECT_NAME in environment")
            project_root = init_project_from_env(workspace_root)
        else:
            project_root = init_project_interactive(workspace_root)
    
    if project_root:
        print(f"\n[✔✔✔] SUCCESS! Project ready at: {project_root}\n")
        return 0
    else:
        print("\n[✗✗✗] Project initialization failed\n")
        return 1


if __name__ == "__main__":
    exit(main())
