import bpy
import json
import sys
import os
import math

# ------------------------------------------------------------
# blender -b --python generate_drivers.py -- corrected.fbx poses.json output.fbx
# ------------------------------------------------------------

argv = sys.argv
argv = argv[argv.index("--") + 1:]

FBX_PATH     = argv[0]   # rig with corrective shape keys
POSES_JSON   = argv[1]   # same poses.json used for sampling
OUTPUT_FBX   = argv[2]   # final rig with drivers
ANGLE_MAX    = math.radians(1.57)  # 90 degrees falloff
# ------------------------------------------------------------


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def import_fbx(path):
    bpy.ops.import_scene.fbx(filepath=path)
    arm = None
    mesh = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            arm = obj
        if obj.type == 'MESH':
            mesh = obj
    return arm, mesh


def load_poses(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("poses", [])


def get_shape_key(mesh, name):
    if mesh.data.shape_keys is None:
        return None
    for sk in mesh.data.shape_keys.key_blocks:
        if sk.name == name:
            return sk
    return None


def add_driver(shape_key, bone_name, axis, max_angle):
    drv = shape_key.driver_add("value").driver
    drv.type = 'SCRIPTED'

    var = drv.variables.new()
    var.name = "rot"
    var.type = 'TRANSFORMS'

    tgt = var.targets[0]
    tgt.id = bpy.context.scene.objects[bone_name.split("/")[0]] if "/" in bone_name else None

    # If bone is in armature
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
            tgt.id = obj
            tgt.bone_target = bone_name
            break

    tgt.transform_type = f"ROT_{axis.upper()}"
    tgt.transform_space = 'LOCAL_SPACE'

    drv.expression = f"max(min(rot/{max_angle}, 1.0), 0.0)"


def main():
    clear_scene()

    arm, mesh = import_fbx(FBX_PATH)
    if arm is None or mesh is None:
        print("ERROR: Could not find armature or mesh in FBX.")
        return

    poses = load_poses(POSES_JSON)
    print(f"Loaded {len(poses)} poses.")

    for pose in poses:
        pose_name = pose.get("name")
        bones = pose.get("bones", {})

        shape_key = get_shape_key(mesh, pose_name)
        if shape_key is None:
            print(f"Skipping pose '{pose_name}' — no matching shape key.")
            continue

        print(f"Creating drivers for shape key: {pose_name}")

        for bone_name, rot in bones.items():
            # Determine dominant axis
            x, y, z = rot
            axis = max(range(3), key=lambda i: abs(rot[i]))
            axis_letter = ["X", "Y", "Z"][axis]

            add_driver(shape_key, bone_name, axis_letter, ANGLE_MAX)

    print("Exporting final rig with drivers:", OUTPUT_FBX)
    bpy.ops.export_scene.fbx(filepath=OUTPUT_FBX)

    print("Driver generation complete.")


if __name__ == "__main__":
    main()
