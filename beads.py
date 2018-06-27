import bpy
import math
# object's location
# bpy.data.objects["Torus.002"].location

# Euler's angles of the object
# bpy.data.objects["Torus.002"].matrix_world.to_euler()

# object's bounding box dimensions
# bpy.data.objects["Torus.002"].dimensions


bpy.ops.object.delete(use_global=False)
location = (0, 0, 1)
locationTop = (0, 0, 10)
rotation = (math.pi/4, 0, 0)
r1 = 1
r2 = 0.8*r1
scale = 3
layers = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False) 
bpy.ops.mesh.primitive_torus_add(view_align=False, location=location, rotation=rotation, layers=layers, major_radius=r1, minor_radius=r2)

#bpy.ops.transform.resize(value=(2.90156, 2.90156, 2.90156), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.ops.transform.resize(value=(1, 1, scale), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.context.object.name = "bead"

bpy.ops.mesh.primitive_plane_add(radius=10, view_align=False, enter_editmode=False, location=location, layers=layers)
#bpy.ops.transform.resize(value=(1, 1, scale), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.context.object.name = "surface"

# Torus as a lamp: failure
bpy.context.scene.render.engine = 'CYCLES'
#bpy.ops.mesh.primitive_torus_add(layers=layers, location=locationTop, rotation=(0, 0, 0), view_align=False, major_radius=5, minor_radius=1)
# bpy.context.space_data.context = 'MATERIAL'
#bpy.ops.material.new()
#bpy.context.object.active_material.diffuse_color = (0.8, 0.8, 0.8)
#materialName = 'mat1'
#bpy.data.materials.new(materialName)
#mat = bpy.data.materials[materialName]
#mat.use_nodes = True
#nodes = mat.node_tree.nodes
#node = nodes.new("Emission")
#node.inputs[1].default_value = 30
#
#
#
bpy.ops.object.lamp_add(type='SPOT', radius=5, view_align=False, location=(0, 0, 20), layers=layers)
bpy.context.object.name = "spot lamp"

# Camera settings

bpy.data.objects['Camera'].location = (0, 0, 20)
bpy.data.objects['Camera'].rotation_euler = (0, 0, math.pi/2)

sceneKey = bpy.data.scenes.keys()[0]
bpy.data.scenes[sceneKey].render.image_settings.file_format = 'JPEG'
bpy.data.scenes[sceneKey].render.filepath = 'camera_1'
bpy.ops.render.render( write_still=True )
