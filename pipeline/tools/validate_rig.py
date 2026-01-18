import bpy
import sys

fbx_path = sys.argv[sys.argv.index("--") + 1]

bpy.ops.import_scene.fbx(filepath=fbx_path)
arm = bpy.context.selected_objects[0]

print("\n--- RIG VALIDATION REPORT ---")

# Check joint orientation
bad_orient = []
for bone in arm.pose.bones:
    if abs(bone.matrix.to_euler().z) > 0.01:
        bad_orient.append(bone.name)

print("Bones with orientation issues:", bad_orient)

# Check hierarchy
if arm.data.bones[0].parent is not None:
    print("Root bone is not actually root!")

print("--- END REPORT ---\n")
