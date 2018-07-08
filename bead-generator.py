import bpy
import bpy_extras
import math
import os
import random
import mathutils
import sys

# this file's folder
currentDir = os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.delete(use_global=False)

print(sys.version_info)



rotation = (0, 0, 0)
r1 = 0.2
r2 = 0.8*r1
d = 2*r1
scale = 2
layers = tuple([True] + 19*[False])

def create_bead(location, rotation, name, mat):
	bead = bpy.ops.mesh.primitive_torus_add(view_align=False, location=location, layers=layers, major_radius=r1, minor_radius=r2)
	bpy.ops.transform.resize(value=(1, 1, scale), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.context.object.name = name
	bead = bpy.context.object
	bead.rotation_euler = rotation
	bead.data.materials.append(mat)

	return bead

def add_plane(config):
	plane = bpy.ops.mesh.primitive_plane_add(radius=10, view_align=False, enter_editmode=False, location=config['location'], layers=layers)
	bpy.context.object.name = "surface"
	mat = bpy.data.materials.new('surface-wood')
	mat.use_nodes = True
	mat.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = config['color']
	mat.node_tree.nodes["Diffuse BSDF"].inputs[1].default_value = 2
	
	# Create procedural texture 
	texture = bpy.data.textures.new('BumpTex', type = 'IMAGE')
	texture.image = bpy.data.images.load(currentDir + '/wood.jpg')

	# Add texture slot for bump texture
	mtex = mat.texture_slots.add()
	mtex.texture = texture
	mtex.texture_coords = 'UV'
	mtex.use_map_color_diffuse = False
	mtex.use_map_normal = True 
	bpy.data.objects['surface'].data.materials.append(mat)

	return plane

def add_lamp(strength, trackObject, location):
	bpy.ops.object.lamp_add(type='SPOT', radius=20, view_align=False, location=location, layers=layers)
	rawName = bpy.context.object.name
	bpy.data.lamps[rawName].node_tree.nodes['Emission'].inputs[1].default_value = strength
	lamp = bpy.data.objects[rawName] 
	trackConstraint = lamp.constraints.new("TRACK_TO")
	trackConstraint.target = trackObject
	trackConstraint.track_axis = 'TRACK_NEGATIVE_Z'
	trackConstraint.up_axis = 'UP_Y'


def add_camera(config):
	bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=config['location'], layers=layers)
	camera = bpy.context.object
	camera.name = config['name']
	if 'focal-length' in config:
		camera.data.lens =  config['focal-length']
		camera.data.lens_unit = 'MILLIMETERS'
	if 'dof' in config:
		camera.data.dof_distance = config['dof']

	camera.rotation_euler = (0, 0, math.pi/2)
	trackConstraint = camera.constraints.new("TRACK_TO")
	trackConstraint.target = bpy.data.objects[config['target']]
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

def create_materialWOOD(name, color_rgba):
	mat = bpy.data.materials.new(name)
	mat.use_nodes = True

	mat.node_tree.nodes["Glossy BSDF"].inputs[0].default_value = color_rgba
	mat.node_tree.nodes["Glossy BSDF"].inputs[1].default_value = 2
	mat.node_tree.nodes["Glossy BSDF"].label = name

	# Create procedural texture 
	texture = bpy.data.textures.new('BumpTex', type = 'WOOD')


	# Add texture slot for bump texture
	mtex = mat.texture_slots.add()
	mtex.texture = texture
	mtex.texture_coords = 'UV'
	mtex.use_map_color_diffuse = False
	mtex.use_map_normal = True 
	#mtex.rgb_to_intensity = True
	
	return mat

def capture(config):
	bpy.context.scene.render.image_settings.color_mode = 'RGB'
	sceneKey = bpy.data.scenes.keys()[0]
	for cameraName in config['cameras']:
		bpy.data.scenes[sceneKey].camera = bpy.data.objects[cameraName]
		bpy.data.scenes[sceneKey].render.image_settings.file_format = 'JPEG'
		bpy.context.scene.render.resolution_x = config['res-x']
		bpy.context.scene.render.resolution_y = config['res-y']
		bpy.context.scene.render.resolution_percentage = config['res-percent']
		bpy.data.scenes[sceneKey].render.filepath = config['folder'] + '/' + config['name'] + '-' + cameraName
		bpy.ops.render.render( write_still=True )
		create_info_file(config['folder'], config['name'] + '-' + cameraName)




def create_scene(config):
	for name, pos, rot in zip(names, locations, rotations):
		m = random.randint(0, T-1)
		print(name, m, pos, rot)
		create_bead(pos, rot, name, materials[m])
	add_plane(config['plane'])

	for lamp in config['lamps']:
		add_lamp(lamp['strength'], bpy.data.objects[lamp['target']], lamp['location'])
	for camera in config['cameras']:
		add_camera(camera)


def create_info_file(workingDir, fileName):
	infoFile = open(workingDir + '/' + fileName + '-data.txt', 'w')
	infoFile.write('# xmin, ymin, xmax, ymax\n')

	scene = bpy.context.scene
	render_scale = scene.render.resolution_percentage / 100
	render_size = (int(scene.render.resolution_x * render_scale), int(scene.render.resolution_y * render_scale))
	camera =  bpy.data.objects['camera-1']


	for name in names:
		obj = bpy.data.objects[name]
		center = obj.location
		dim = obj.dimensions
		points =  [mathutils.Vector((h, w, d)) for h in [-1, 1] for w in [-1, 1] for d in [-1, 1]]
		vertices3d =  [mathutils.Vector(center) + mathutils.Vector((p[0]*dim[0]/2, p[1]*dim[1]/2, p[2]*dim[2]/2)) for p in points]
		vertices2d = [(round(v.x * render_size[0]), round(v.y * render_size[1])) for v in [bpy_extras.object_utils.world_to_camera_view(scene, camera, b) for b in vertices3d]]
		print(vertices2d)
		minX = min([v[0] for v in vertices2d])
		minY = min([v[1] for v in vertices2d])
		maxX = max([v[0] for v in vertices2d])
		maxY = max([v[1] for v in vertices2d])
		box2d = [minX, minY, maxX, maxY]
		infoFile.write(', '.join([str(c) for c in box2d]) + '\n')

	infoFile.close()

bpy.context.scene.render.engine = 'CYCLES'
xmax = 4
ymax = 4
z = 2*r1
N = 15
T = 5
random.seed(0.1)

materials = [create_material('TexMat' + str(i), (random.random(), random.random(), random.random(), random.randrange(0, 5, 1)/5)) for i in range(1, T+1)]
locations = [(random.randrange(0, xmax/d, 1)*d, random.randrange(0, ymax/d, 1)*d, z) for i in range(0, N)]
rotations = [(math.pi * random.random(), math.pi * random.random(), 0) for i in range(0, N)]
names = ['bead' + str(i) for i in range(0, N)]
create_scene(
	{'lamps': [
		{'strength': 3000, 'target': names[1], 'location': (2, 2, 5)}, 
		{'strength': 500, 'target': names[2], 'location': (0, -1, 5)},
		{'strength': 1000, 'target': names[3], 'location': (-2, -2, 5)}],
	'plane': {'location': (0, 0, 0), 'color': (0.3, 0.1, 0.4, 0.9)},
	'cameras': [
		{'name': 'camera-1', 'location': (0, 0, 8), 'target': names[2], 'focal-length': 20, 'dof': 15},
		{'name': 'camera-2', 'location': (1, 2, 6), 'target': names[3], 'focal-length': 40, 'dof': 5}
	]})
capture({'folder': currentDir + '/output', 'name': 'scene1', 'res-x': 400, 'res-y': 400, 'res-percent': 100,
	'cameras': ['camera-1', 'camera-2']})