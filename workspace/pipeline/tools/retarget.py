"""
retarget.py
------------
Blender-based animation retargeting script for the Exhibition pipeline.

Usage:
blender -b --python retarget.py -- \
    <rig_fbx> <anim_fbx> <mapping_json> <output_fbx>
"""

import bpy
import sys
import json
from pathlib import Path


# ---------------------------------------------------------
# Utility: Clear the scene
# ---------------------------------------------------------
def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


# ---------------------------------------------------------
# Utility: Import FBX
# ---------------------------------------------------------
def import_fbx(path):
    bpy.ops.import_scene.fbx(filepath=str(path))
    return bpy.context.selected_objects


# ---------------------------------------------------------
# Utility: Export FBX
# ---------------------------------------------------------
def export_fbx(path):
    bpy.ops.export_scene.fbx(
        filepath=str(path),
        use_selection=False,
        bake_anim=True,
        add_leaf_bones=False
    )


# ---------------------------------------------------------
# Load bone mapping JSON
# ---------------------------------------------------------
def load_mapping(mapping_path):
    mapping = json.loads(Path(mapping_path).read_text())
    return mapping


# ---------------------------------------------------------
# Core Retargeting Logic
# ---------------------------------------------------------
def retarget_animation(rig_obj, anim_obj, mapping):
    """
    rig_obj: Armature with correct weights (UniRig output)
    anim_obj: Armature containing HY-Motion animation
    mapping: dict { "source_bone": "target_bone" }
    """

    bpy.context.view_layer.objects.active = rig_obj
    rig_obj.select_set(True)

    # Ensure both armatures are in pose mode
    bpy.ops.object.mode_set(mode='POSE')

    # Create a new action on the rig
    rig_action = bpy.data.actions.new("RetargetedAction")
    rig_obj.animation_data_create()
    rig_obj.animation_data.action = rig_action

    # Iterate through all bones in mapping
    for src_bone, tgt_bone in mapping.items():
        if src_bone not in anim_obj.pose.bones:
            print(f"[WARN] Source bone missing: {src_bone}")
            continue
        if tgt_bone not in rig_obj.pose.bones:
            print(f"[WARN] Target bone missing: {tgt_bone}")
            continue

        src = anim_obj.pose.bones[src_bone]
        tgt = rig_obj.pose.bones[tgt_bone]

        # Copy rotation keyframes
        for fcurve in anim_obj.animation_data.action.fcurves:
            if fcurve.data_path.endswith(f'"{src_bone}"'):

                # Create matching fcurve on rig
                new_curve = rig_action.fcurves.new(
                    data_path=f'pose.bones["{tgt_bone}"].rotation_quaternion',
                    index=fcurve.array_index
                )

                for kp in fcurve.keyframe_points:
                    new_kp = new_curve.keyframe_points.insert(
                        kp.co[0], kp.co[1]
                    )
                    new_kp.interpolation = kp.interpolation

    print("[✔] Retargeting complete.")


# ---------------------------------------------------------
# MAIN ENTRY
# ---------------------------------------------------------
def main():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]

    rig_fbx = Path(argv[0])
    anim_fbx = Path(argv[1])
    mapping_json = Path(argv[2])
    output_fbx = Path(argv[3])

    print("\n=== RETARGETING ===")
    print("Rig FBX:     ", rig_fbx)
    print("Anim FBX:    ", anim_fbx)
    print("Mapping JSON:", mapping_json)
    print("Output FBX:  ", output_fbx)

    clear_scene()

    # Import rig
    rig_objs = import_fbx(rig_fbx)
    rig_armature = next(o for o in rig_objs if o.type == 'ARMATURE')

    # Import animation
    anim_objs = import_fbx(anim_fbx)
    anim_armature = next(o for o in anim_objs if o.type == 'ARMATURE')

    # Load mapping
    mapping = load_mapping(mapping_json)

    # Retarget
    retarget_animation(rig_armature, anim_armature, mapping)

    # Export
    export_fbx(output_fbx)

    print(f"[✔] Retargeted animation saved to: {output_fbx}")


if __name__ == "__main__":
    main()
