#!/usr/bin/env python3
"""
prepare_mesh.py
---------------
Prepare mesh for pipeline: UV unwrapping, validation, cleanup

This runs BEFORE texture generation to ensure the mesh has proper UVs.

Usage:
blender --background --python prepare_mesh.py -- <input_mesh> <output_mesh>
"""

import sys
from pathlib import Path

try:
    import bpy
except ImportError:
    print("ERROR: This script must be run through Blender")
    sys.exit(1)


def clear_scene():
    """Clear all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def import_mesh(mesh_path):
    """Import mesh file"""
    mesh_path = Path(mesh_path)
    
    if mesh_path.suffix.lower() == '.fbx':
        bpy.ops.import_scene.fbx(filepath=str(mesh_path))
    elif mesh_path.suffix.lower() == '.obj':
        bpy.ops.import_scene.obj(filepath=str(mesh_path))
    else:
        raise ValueError(f"Unsupported mesh format: {mesh_path.suffix}")
    
    # Get the imported mesh object
    mesh_obj = None
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            mesh_obj = obj
            break
    
    if not mesh_obj:
        raise ValueError("No mesh object found in imported file")
    
    print(f"Imported mesh: {mesh_path.name}")
    return mesh_obj


def create_uv_unwrapping(mesh_obj, project_path=None):
    """
    Create or apply UV unwrapping for texture mapping.
    First checks if UDIM UV layouts were uploaded, otherwise generates Smart UV Project.
    
    Args:
        mesh_obj: Blender mesh object
        project_path: Path to project directory (to check for uploaded UV layouts)
    """
    print("\n=== UV Unwrapping ===")
    
    # Check for uploaded UDIM UV layouts
    uv_layout_applied = False
    if project_path:
        uv_layout_dir = project_path / "0_input" / "uv_layouts"
        print(f"Checking for UV layouts in: {uv_layout_dir}")
        print(f"  Directory exists: {uv_layout_dir.exists()}")
        if uv_layout_dir.exists():
            uv_images = list(uv_layout_dir.glob("*.png")) + list(uv_layout_dir.glob("*.jpg"))
            print(f"  Found {len(uv_images)} image files")
            if uv_images:
                print(f"✓ Found {len(uv_images)} uploaded UV layout(s):")
                # User has uploaded UDIM UV layouts - use the existing UVs from the mesh
                if mesh_obj.data.uv_layers:
                    print(f"✓ Using existing UV map from mesh: {mesh_obj.data.uv_layers.active.name}")
                    print(f"  Uploaded UV layouts will be used for texturing:")
                    for uv_img in uv_images:
                        print(f"    - {uv_img.name}")
                    uv_layout_applied = True
                else:
                    print("⚠ UV layouts uploaded but mesh has no UV coordinates")
                    print("  Mesh must be UV unwrapped in your 3D software to match uploaded layouts")
                    print("  Falling back to automatic UV unwrapping...")
    
    if not uv_layout_applied:
        # No uploaded UV layouts or mesh has no UVs - generate automatic unwrapping
        print("No UDIM UV layouts uploaded, generating automatic UV unwrapping...")
        
        # Select the mesh and enter edit mode
        bpy.context.view_layer.objects.active = mesh_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Create UV layer if it doesn't exist
        if not mesh_obj.data.uv_layers:
            mesh_obj.data.uv_layers.new(name='UVMap')
            print("Created new UV layer: UVMap")
        else:
            print(f"Using existing UV layer: {mesh_obj.data.uv_layers.active.name}")
        
        # Smart UV Project - works well for organic models
        print("Applying Smart UV Project...")
        bpy.ops.uv.smart_project(
            angle_limit=66.0,  # Seam angle threshold
            island_margin=0.02,  # Space between UV islands (2%)
            area_weight=0.0,  # Don't weight by face area
            correct_aspect=True,
            scale_to_bounds=True
        )
        
        bpy.ops.object.mode_set(mode='OBJECT')
        print(f"✓ UV unwrapping complete: {len(mesh_obj.data.uv_layers)} UV layer(s)")
        print("  Generated UVs - textures will be auto-generated to fit")
    else:
        # Make sure we're in object mode
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    
    print(f"Final UV layers: {len(mesh_obj.data.uv_layers)}")
    return True


def validate_and_cleanup(mesh_obj):
    """Validate mesh and perform basic cleanup"""
    print("\n=== Mesh Validation & Cleanup ===")
    
    mesh = mesh_obj.data
    print(f"Mesh: {mesh_obj.name}")
    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Polygons: {len(mesh.polygons)}")
    print(f"  Edges: {len(mesh.edges)}")
    
    # Enter edit mode for cleanup
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Recalculate normals
    bpy.ops.mesh.normals_make_consistent(inside=False)
    print("✓ Recalculated normals")
    
    # Remove doubles (merge close vertices)
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    print("✓ Removed duplicate vertices")
    
    bpy.ops.object.mode_set(mode='OBJECT')
    print("=== Validation Complete ===\n")
    
    return True


def export_mesh(mesh_obj, output_path):
    """Export mesh as FBX"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Select only the mesh
    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_obj
    
    # Export as FBX
    bpy.ops.export_scene.fbx(
        filepath=str(output_path),
        use_selection=True,
        apply_scale_options='FBX_SCALE_ALL',
        object_types={'MESH'}
    )
    
    print(f"Exported prepared mesh to: {output_path}")
    return True


def main():
    """Main execution"""
    # Parse arguments (after --)
    try:
        separator_index = sys.argv.index('--')
        args = sys.argv[separator_index + 1:]
    except ValueError:
        print("ERROR: No arguments provided")
        print("Usage: blender --background --python prepare_mesh.py -- <input_mesh> <output_mesh>")
        sys.exit(1)
    
    if len(args) < 2:
        print("ERROR: Insufficient arguments")
        print("Usage: blender --background --python prepare_mesh.py -- <input_mesh> <output_mesh>")
        sys.exit(1)
    
    input_mesh = Path(args[0])
    output_mesh = Path(args[1])
    
    # Get project path
    # Input:  /workspace/TestRun/0_input/meshes/character_clean.fbx
    # Output: /workspace/TestRun/0_input/character_clean_prepared.fbx
    # Project should be: /workspace/TestRun
    
    # Go up from meshes -> 0_input -> project_root
    if input_mesh.parent.name == 'meshes':
        project_path = input_mesh.parent.parent.parent
    else:
        # Fallback: mesh directly in 0_input
        project_path = input_mesh.parent.parent
    
    print("="*80)
    print("MESH PREPARATION")
    print("="*80)
    print(f"Input:   {input_mesh}")
    print(f"Output:  {output_mesh}")
    print(f"Project: {project_path}")
    print(f"UV layout dir: {project_path / '0_input' / 'uv_layouts'}")
    print("")
    
    if not input_mesh.exists():
        print(f"ERROR: Input mesh not found: {input_mesh}")
        sys.exit(1)
    
    try:
        # Clear scene
        clear_scene()
        
        # Import mesh
        mesh_obj = import_mesh(input_mesh)
        
        # Validate and cleanup
        validate_and_cleanup(mesh_obj)
        
        # Create UV unwrapping (checks for uploaded UDIM layouts first)
        create_uv_unwrapping(mesh_obj, project_path)
        
        # Export prepared mesh
        export_mesh(mesh_obj, output_mesh)
        
        print("\n" + "="*80)
        print("MESH PREPARATION COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"\nERROR during mesh preparation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
