#----------------------------------------------------------
# File multi_material.py
#----------------------------------------------------------
import bpy
 
def run(origin):
    # Create three materials
    red = bpy.data.materials.new('Red')
    red.diffuse_color = (1,0,0)
    blue = bpy.data.materials.new('Blue')
    blue.diffuse_color = (0,0,1)
    yellow = bpy.data.materials.new('Yellow')
    yellow.diffuse_color = (1,1,0)
 
    # Create mesh and assign materials
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments = 16,
        ring_count = 8, 
        location=origin)
    ob = bpy.context.object
    ob.name = 'MultiMatSphere'
    me = ob.data
    me.materials.append(red)
    me.materials.append(blue)
    me.materials.append(yellow)
 
    # Assign materials to faces
    for f in me.faces:
        f.material_index = f.index % 3
 
    # Set left half of sphere smooth, right half flat shading
    for f in me.faces:
        f.use_smooth = (f.center[0] < 0)
 
if __name__ == "__main__":
    run((0,0,0))