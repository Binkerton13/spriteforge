import bpy, sys, json

fbx_path = sys.argv[sys.argv.index("--") + 1]
poses_path = sys.argv[sys.argv.index("--") + 2]

bpy.ops.import_scene.fbx(filepath=fbx_path)
arm = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE'][0]

poses = json.load(open(poses_path))

for i, pose in enumerate(poses):
    for bone_name, rot in pose["bones"].items():
        bone = arm.pose.bones.get(bone_name)
        if bone:
            bone.rotation_mode = 'XYZ'
            bone.rotation_euler = rot  # [x, y, z] in radians

    bpy.context.view_layer.update()

    # Export deformed mesh snapshot
    out_path = f"pipeline/deform_fix/snapshots/deform_pose_{i:03d}.obj"
    bpy.ops.export_scene.obj(filepath=out_path, use_selection=False)
