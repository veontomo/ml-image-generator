import bpy
import bpy_extras
import math
import os
import random
import mathutils

# this file's folder
currentDir = os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.delete(use_global=False)


rotation = (0, 0, 0)
r1 = 0.2
r2 = 0.8*r1
scale = 2
layers = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False) 

def create_bead(location, name, mat):
	bead = bpy.ops.mesh.primitive_torus_add(view_align=False, location=location, rotation=rotation, layers=layers, major_radius=r1, minor_radius=r2)
	bpy.ops.transform.resize(value=(1, 1, scale), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.context.object.name = name
	bead = bpy.context.object
	me = bead.data
	me.materials.append(mat)

	return bead

def add_plane(location):
	plane = bpy.ops.mesh.primitive_plane_add(radius=10, view_align=False, enter_editmode=False, location=location, layers=layers)
	bpy.context.object.name = "surface"
	return plane

def add_lamp(strength, trackObject, location):
	rawLamp = bpy.ops.object.lamp_add(type='SPOT', radius=20, view_align=False, location=location, layers=layers)
	rawName = bpy.context.object.name
	bpy.data.lamps[rawName].node_tree.nodes['Emission'].inputs[1].default_value = strength
	lamp = bpy.data.objects[rawName] 
	trackConstraint = lamp.constraints.new("TRACK_TO")
	trackConstraint.target = trackObject
	trackConstraint.track_axis = 'TRACK_NEGATIVE_Z'
	trackConstraint.up_axis = 'UP_Y'


def add_camera(trackObject):
	camera = bpy.data.objects['Camera']
	camera.location = (0, 0, 8)
	camera.rotation_euler = (0, 0, math.pi/2)
	trackConstraint = camera.constraints.new("TRACK_TO")
	trackConstraint.target = trackObject
	trackConstraint.track_axis = 'TRACK_NEGATIVE_Z'
	trackConstraint.up_axis = 'UP_Y'

def create_material(name, color_rgba):
	mat = bpy.data.materials.new(name)
	mat.use_nodes = True

	mat.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = color_rgba
	mat.node_tree.nodes["Diffuse BSDF"].inputs[1].default_value = 2
	mat.node_tree.nodes["Diffuse BSDF"].label = name

	# Create procedural texture 
	texture = bpy.data.textures.new('BumpTex', type = 'STUCCI')
	texture.noise_basis = 'BLENDER_ORIGINAL' 
	texture.noise_scale = 0.25 
	texture.noise_type = 'SOFT_NOISE' 
	texture.saturation = 1 
	texture.stucci_type = 'PLASTIC' 
	texture.turbulence = 5 


	# Add texture slot for bump texture
	mtex = mat.texture_slots.add()
	mtex.texture = texture
	mtex.texture_coords = 'UV'
	mtex.use_map_color_diffuse = False
	mtex.use_map_normal = True 
	#mtex.rgb_to_intensity = True
	
	return mat
def capture(name):
	bpy.context.scene.render.image_settings.color_mode = 'RGB'
	sceneKey = bpy.data.scenes.keys()[0]
	bpy.data.scenes[sceneKey].render.image_settings.file_format = 'JPEG'
	bpy.context.scene.render.resolution_x = 800
	bpy.context.scene.render.resolution_y = 800
	bpy.context.scene.render.resolution_percentage = 100
	bpy.data.scenes[sceneKey].render.filepath = currentDir + '/' + name
	bpy.ops.render.render( write_still=True )



bpy.context.scene.render.engine = 'CYCLES'
xmax = 4
ymax = 4
z = 2*r1
N = 5
T = 2
random.seed(0.5)

materials = [create_material('TexMat' + str(i), (random.random(), random.random(), random.random(), random.randrange(0, 5, 1)/5)) for i in range(1, T+1)]
d = 2*r1
locations = [(random.randrange(0, xmax/d, 1)*d, random.randrange(0, ymax/d, 1)*d, z) for i in range(0, N)]
for i, pos in enumerate(locations):
	m = random.randint(0, T-1)
	print(i, m)
	create_bead(pos, 'bead'+str(i), materials[m])
add_plane((0, 0, 0))
add_lamp(4000, bpy.data.objects['bead0'], (5, 5, 5))
add_lamp(500, bpy.data.objects['bead1'], (0, -1, 5))

add_camera(bpy.data.objects['bead0'])
capture('beads1')




scene = bpy.context.scene
render_scale = scene.render.resolution_percentage / 100
render_size = (int(scene.render.resolution_x * render_scale), int(scene.render.resolution_y * render_scale))

camera =  bpy.data.objects['Camera']
for i in range(0, N):
	obj = bpy.data.objects['bead' + str(i)]
	center = obj.location
	dim = obj.dimensions
	points =  [mathutils.Vector((h, w, d)) for h in [-1, 1] for w in [-1, 1] for d in [-1, 1]]
	box =  [mathutils.Vector(center) + mathutils.Vector((p[0]*dim[0]/2, p[1]*dim[1]/2, p[2]*dim[2]/2)) for p in points]
	for b in box:
		co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, b)
		print(obj.name + " dim-2 coords:", co_2d, "Pixel Coords:", (round(co_2d.x * render_size[0]), round(co_2d.y * render_size[1])))

