import bpy
import sys

fbx_path = sys.argv[sys.argv.index("--") + 1]

bpy.ops.import_scene.fbx(filepath=fbx_path)
obj = bpy.context.selected_objects[0]
mesh = obj.data

print("\n--- MESH VALIDATION REPORT ---")

# Non-manifold
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_non_manifold()
non_manifold = len([v for v in mesh.vertices if v.select])
print("Non-manifold:", non_manifold)

# Loose verts
bpy.ops.mesh.select_loose()
loose = len([v for v in mesh.vertices if v.select])
print("Loose vertices:", loose)

# Duplicate verts
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)
print("Merged duplicate vertices")

# UV overlap
uv_layer = mesh.uv_layers.active.data
overlap = any(uv.uv.x < 0 or uv.uv.x > 1 or uv.uv.y < 0 or uv.uv.y > 1 for uv in uv_layer)
print("UV outside 0-1:", overlap)

bpy.ops.object.mode_set(mode='OBJECT')
print("--- END REPORT ---\n")
