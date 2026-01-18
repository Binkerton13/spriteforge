import bpy
import sys

fbx_path = sys.argv[sys.argv.index("--") + 1]

bpy.ops.import_scene.fbx(filepath=fbx_path)
obj = bpy.context.selected_objects[0]
arm = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE'][0]

bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

print("\n--- SKIN WEIGHT SMOOTHING ---")

# Laplacian smoothing
bpy.ops.object.vertex_group_smooth(
    group_select_mode='ALL',
    factor=0.5,
    repeat=4
)

# Normalize all weights
bpy.ops.object.vertex_group_normalize_all()

# Volume-preserving smoothing
bpy.ops.object.vertex_group_smooth(
    group_select_mode='ALL',
    factor=0.25,
    repeat=2
)

bpy.ops.object.mode_set(mode='OBJECT')

clean_path = fbx_path.replace(".fbx", "_weightsmoothed.fbx")
bpy.ops.export_scene.fbx(filepath=clean_path)

print("Saved smoothed rig:", clean_path)
print("--- SMOOTHING COMPLETE ---\n")
