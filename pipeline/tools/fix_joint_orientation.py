import bpy
import sys

fbx_path = sys.argv[sys.argv.index("--") + 1]

bpy.ops.import_scene.fbx(filepath=fbx_path)
arm = bpy.context.selected_objects[0]

print("\n--- JOINT ORIENTATION CLEANUP ---")

bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='EDIT')

edit_bones = arm.data.edit_bones

# Normalize roll
for bone in edit_bones:
    bone.roll = 0.0

# Align axes
for bone in edit_bones:
    if bone.parent:
        bone.align_roll(bone.parent.vector)

# Fix flipped axes
for bone in edit_bones:
    if bone.matrix.to_3x3().determinant() < 0:
        bone.roll += 3.14159

bpy.ops.object.mode_set(mode='OBJECT')

# Save cleaned rig
clean_path = fbx_path.replace(".fbx", "_cleaned.fbx")
bpy.ops.export_scene.fbx(filepath=clean_path)

print("Saved cleaned rig:", clean_path)
print("--- CLEANUP COMPLETE ---\n")
