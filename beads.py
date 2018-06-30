import bpy
import math
import os

# this file's folder
currentDir = os.path.dirname(os.path.abspath(__file__))
# object's location
# bpy.data.objects["Torus.002"].location

# Euler's angles of the object
# bpy.data.objects["Torus.002"].matrix_world.to_euler()

# object's bounding box dimensions
# bpy.data.objects["Torus.002"].dimensions


bpy.ops.object.delete(use_global=False)
location = (0, 0, 1)
locationTop = (0, 0, 10)
rotation = (0, 0, 0)
r1 = 1
r2 = 0.8*r1
scale = 2
layers = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False) 
bpy.ops.mesh.primitive_torus_add(view_align=False, location=location, rotation=rotation, layers=layers, major_radius=r1, minor_radius=r2)

#bpy.ops.transform.resize(value=(2.90156, 2.90156, 2.90156), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.ops.transform.resize(value=(1, 1, scale), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.context.object.name = "bead"

bpy.context.scene.render.engine = 'CYCLES'

mat = bpy.data.materials.new('TexMat')
mat.use_nodes = True

mat.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (1, 0.9, 0.06, 0.5)
mat.node_tree.nodes["Diffuse BSDF"].inputs[1].default_value = 8
mat.node_tree.nodes["Diffuse BSDF"].label = 'yellow'

# Create procedural texture 
texture1 = bpy.data.textures.new('BumpTex', type = 'STUCCI')
texture1.noise_basis = 'BLENDER_ORIGINAL' 
texture1.noise_scale = 0.25 
texture1.noise_type = 'SOFT_NOISE' 
texture1.saturation = 1 
texture1.stucci_type = 'PLASTIC' 
texture1.turbulence = 5 


# Add texture slot for bump texture
mtex = mat.texture_slots.add()
mtex.texture = texture1
mtex.texture_coords = 'ORCO'
mtex.use_map_color_diffuse = False
mtex.use_map_normal = True 
#mtex.rgb_to_intensity = True


ob = bpy.context.object
me = ob.data
me.materials.append(mat)

bpy.ops.mesh.primitive_plane_add(radius=10, view_align=False, enter_editmode=False, location=(0,0,0), layers=layers)
#bpy.ops.transform.resize(value=(1, 1, scale), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.context.object.name = "surface"

plane = bpy.data.objects['surface']


##########
mat2 = bpy.data.materials.new('planeMat')
mat2.use_nodes = True

#mat2.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (0, 0.4, 0.4, 0.9)
#mat2.node_tree.nodes["Diffuse BSDF"].inputs[1].default_value = 6
#mat2.node_tree.nodes["Diffuse BSDF"].label = 'plane'

image = bpy.data.images.load(currentDir + '/wood.jpg')

# Create procedural texture 
texture2 = bpy.data.textures.new('wood-image', type = 'IMAGE')
texture2.image = image


#plane.material_slots[0].material.node_tree.nodes[0].image = bpy.data.images.load(currentDir + '/wood.jpg')


#bpy.ops.transform.translate(value=(0, 0, 0.786209), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True, use_accurate=False)
#bpy.ops.object.editmode_toggle()
#bpy.ops.uv.smart_project()
##bpy.context.space_data.context = 'OBJECT'
##bpy.context.space_data.context = 'MATERIAL'
#bpy.ops.image.open(filepath=currentDir+"/wood.jpg", currentDirectory=currentDir, files=[{"name":"wood.jpg", "name":"wood.jpg"}], relative_path=True, show_multiview=False)
#bpy.context.space_data.viewport_shade = 'TEXTURED'


#texture2.noise_basis_2 = 'TRI'
#texture2.wood_type = 'RINGS'
#texture2.wood_type = 'BANDNOISE'
#texture2.wood_type = 'RINGNOISE'
#texture2.wood_type = 'RINGS'
#texture2.noise_type = 'HARD_NOISE'
#texture2.wood_type = 'BANDS'
#texture2.noise_basis = 'IMPROVED_PERLIN'
#texture2.noise_basis = 'VORONOI_F2'
#texture2.noise_scale = 0.9
#texture2.nabla = 0.04
#texture2.turbulence = 9


# Add texture slot for bump texture
mtex2 = mat2.texture_slots.add()
mtex2.texture = texture2


me2 = plane.data
me2.materials.append(mat2)
##########



# Torus as a lamp: failure

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
bpy.ops.object.lamp_add(type='SPOT', radius=20, view_align=False, location=(2, 2, 10), layers=layers)
bpy.context.object.name = "spot lamp"

# Camera settings

camera = bpy.data.objects['Camera']
camera.location = (2, 2, 8)
camera.rotation_euler = (0, 0, math.pi/2)


#bpy.context.space_data.context = 'CONSTRAINT'
trackConstraint = camera.constraints.new("TRACK_TO")
trackConstraint.target = bpy.data.objects["bead"]
trackConstraint.track_axis = 'TRACK_NEGATIVE_Z'
trackConstraint.up_axis = 'UP_Y'



#bpy.context.space_data.context = 'RENDER'
bpy.context.scene.render.image_settings.color_mode = 'RGB'


sceneKey = bpy.data.scenes.keys()[0]
bpy.data.scenes[sceneKey].render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.resolution_x = 2000
bpy.context.scene.render.resolution_y = 2000
bpy.context.scene.render.resolution_percentage = 10


bpy.data.scenes[sceneKey].render.filepath = currentDir + '/camera_1'
bpy.ops.render.render( write_still=True )



# Create image texture from image
cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
cTex.image = image

# Create material
cubeMat = bpy.data.materials.new('cube')
cubeMat.use_nodes = True

# Add texture slot for color texture
mtex = cubeMat.texture_slots.add()
mtex.texture = cTex
mtex.texture_coords = 'UV'
mtex.uv_layer = 'default'


# Create new cube and give it UVs
cube = bpy.ops.mesh.primitive_cube_add(location=(3,3,0))
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.smart_project()
bpy.ops.object.mode_set(mode='OBJECT')

# Add material to current object
me = cube.data
me.materials.append(cubeMat)
 


