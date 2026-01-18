import bpy
import sys
import os
import math

# ------------------------------------------------------------
# blender -b --python freeze_rig.py -- rig_smoothed.fbx output_frozen.fbx
# ------------------------------------------------------------

argv = sys.argv
argv = argv[argv.index("--") + 1:]

INPUT_FBX  = argv[0]
OUTPUT_FBX = argv[1]


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


def apply_object_transforms(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def freeze_armature(arm):
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in arm.data.edit_bones:
        # Normalize bone roll
        bone.roll = 0.0

        # Orthogonalize bone matrix
        m = bone.matrix.to_3x3().normalized()
        bone.matrix = m.to_4x4()

    bpy.ops.object.mode_set(mode='OBJECT')


def freeze_pose(arm):
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')

    for pb in arm.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0.0, 0.0, 0.0)

    bpy.ops.object.mode_set(mode='OBJECT')


def main():
    clear_scene()

    arm, mesh = import_fbx(INPUT_FBX)
    if arm is None or mesh is None:
        print("ERROR: Could not find armature or mesh.")
        return

    # Apply transforms on mesh and armature
    apply_object_transforms(mesh)
    apply_object_transforms(arm)

    # Freeze pose and bone matrices
    freeze_pose(arm)
    freeze_armature(arm)

    # Export final frozen rig
    bpy.ops.export_scene.fbx(
        filepath=OUTPUT_FBX,
        apply_scale_options='FBX_SCALE_ALL',
        add_leaf_bones=False,
        bake_space_transform=True
    )

    print("Rig frozen and exported:", OUTPUT_FBX)


if __name__ == "__main__":
    main()
