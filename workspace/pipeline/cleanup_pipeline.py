#!/usr/bin/env python3
"""
cleanup_pipeline.py
-------------------
Removes redundant and empty files/folders from the Exhibition pipeline.

This script:
- Removes empty configuration files
- Removes empty/redundant script folders
- Removes duplicate documentation
- Removes unused UI components
- Reports what was deleted

Usage:
    python pipeline/cleanup_pipeline.py
"""

import shutil
from pathlib import Path


def remove_if_empty(path: Path) -> bool:
    """Remove file if it exists and is empty"""
    if path.exists():
        if path.is_file() and path.stat().st_size == 0:
            path.unlink()
            print(f"[✔] Removed empty file: {path}")
            return True
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()
            print(f"[✔] Removed empty directory: {path}")
            return True
    return False


def remove_path(path: Path, description: str = "") -> bool:
    """Remove file or directory if it exists"""
    if path.exists():
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)
        print(f"[✔] Removed {description}: {path}")
        return True
    else:
        print(f"[=] Already gone: {path}")
        return False


def cleanup_pipeline(root: Path):
    """Remove all redundant files and folders"""
    
    print("\n=== CLEANING UP PIPELINE ===\n")
    
    removed_count = 0
    
    # 1. Empty configuration files
    print("\n[1] Removing empty configuration files...")
    removed_count += remove_if_empty(root / "config/animation_settings.json")
    removed_count += remove_if_empty(root / "config/rig_settings.json")
    removed_count += remove_if_empty(root / "config/texture_settings.json")
    
    # 2. Empty/redundant script folders
    print("\n[2] Removing empty script folders...")
    removed_count += remove_path(
        root / "scripts/run_texture_pipeline.py",
        "empty script"
    )
    removed_count += remove_path(
        root / "scripts/run_rig_pipeline.py",
        "empty script"
    )
    removed_count += remove_path(
        root / "scripts/run_animation_pipeline.py",
        "empty script"
    )
    removed_count += remove_if_empty(root / "scripts/utils")
    removed_count += remove_if_empty(root / "scripts")
    
    # 3. Redundant documentation
    print("\n[3] Removing duplicate documentation...")
    removed_count += remove_path(
        root / "pipeline/DEPENDENCY_MAP.md",
        "duplicate documentation"
    )
    removed_count += remove_path(
        root / "pipeline/dependency_map.json",
        "unused JSON dependency map"
    )
    
    # 4. Redundant rig folders
    print("\n[4] Removing redundant rig folders...")
    removed_count += remove_if_empty(root / "2_rig/scripts")
    
    # 5. Standalone UI (not integrated with main pipeline)
    print("\n[5] Removing standalone UI components...")
    removed_count += remove_path(
        root / "3_animation/hy_motion/ui",
        "standalone UI folder"
    )
    removed_count += remove_path(
        root / "3_animation/hy_motion/scripts/ui_server.py",
        "standalone UI server"
    )
    
    # 6. Check for unused tools (ask before removing)
    print("\n[6] Checking for potentially unused tools...")
    potentially_unused = [
        root / "pipeline/tools/generate_drivers.py",
        root / "pipeline/tools/apply_poses_export_meshes.py"
    ]
    
    for tool_path in potentially_unused:
        if tool_path.exists():
            print(f"[?] Found potentially unused tool: {tool_path}")
            print(f"    (Not auto-removing - verify manually)")
    
    print(f"\n[✔] Cleanup complete. Removed {removed_count} items.\n")


def main():
    # Get project root (parent of pipeline folder)
    root = Path(__file__).resolve().parents[1]
    print(f"Project root: {root}")
    
    cleanup_pipeline(root)


if __name__ == "__main__":
    main()
