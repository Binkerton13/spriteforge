import bpy
import json
import os
import sys

# ---------------- CONFIG ----------------

# Expect: blender -b --python apply_poses_export_meshes.py -- rig.fbx poses.json out_dir
argv = sys.argv
argv = argv[argv.index("--") + 1:]

FBX_PATH   = argv[0]  # e.g. "2_rig/autorig_output/character_rigged_weightsmoothed.fbx"
POSES_JSON = argv[1]  # e.g. "pipeline/deform_fix/poses.json"
OUT_DIR    = argv[2]  # e.g. "pipeline/deform_fix/snapshots"

# ----------------------------------------


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def import_fbx(path):
    bpy.ops.import_scene.fbx(filepath=path)
    armature = None
    mesh_objs = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            armature = obj
        elif obj.type == 'MESH':
            mesh_objs.append(obj)
    return armature, mesh_objs


def load_poses(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("poses", [])


def ensure_out_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def apply_pose(armature, pose_def):
    bones_data = pose_def.get("bones", {})
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    for bone_name, rot in bones_data.items():
        pb = armature.pose.bones.get(bone_name)
        if pb is None:
            continue
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = rot

    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode='OBJECT')


def export_deformed_mesh(mesh_objs, out_path):
    # Select only the mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in mesh_objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_objs[0]

    bpy.ops.export_scene.obj(
        filepath=out_path,
        use_selection=True,
        use_materials=False,
        use_normals=True,
        use_uvs=True
    )


def main():
    clear_scene()
    armature, mesh_objs = import_fbx(FBX_PATH)
    if armature is None or not mesh_objs:
        print("ERROR: Could not find armature or mesh objects in FBX.")
        return

    poses = load_poses(POSES_JSON)
    ensure_out_dir(OUT_DIR)

    print(f"Loaded {len(poses)} poses from {POSES_JSON}")

    for i, pose_def in enumerate(poses):
        pose_name = pose_def.get("name", f"pose_{i:03d}")
        print(f"Applying pose {i+1}/{len(poses)}: {pose_name}")

        apply_pose(armature, pose_def)

        safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in pose_name)
        out_path = os.path.join(OUT_DIR, f"deform_{i:03d}_{safe_name}.obj")

        export_deformed_mesh(mesh_objs, out_path)

    print("Done exporting deformed meshes.")


if __name__ == "__main__":
    main()
