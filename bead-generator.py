import bpy
import bpy_extras
import math
import os
import random
import mathutils
import sys
from threading import Thread
# this file's folder
currentDir = os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.delete(use_global=False)

print(sys.version_info)



layers = tuple([True] + 19*[False])
xmax = 4
ymax = 4
r1 = 0.2
d = 2*r1
z = 2*r1
N = 20
T = 4
random.seed(0.1)

def create_bead(location, rotation, name, mat):
	r2 = 0.8*r1
	scale = 2
	bpy.ops.mesh.primitive_torus_add(view_align=False, location=location, layers=layers, major_radius=r1, minor_radius=r2)
	bpy.ops.transform.resize(value=(1, 1, scale), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.ops.rigidbody.objects_add()
	bead = bpy.context.object
	bead.name = name
	bead.rotation_euler = rotation
	bead.data.materials.append(mat)
	return bead

def create_cube(location, rotation, name, mat):
	bpy.ops.mesh.primitive_cube_add(radius=0.2, view_align=False, enter_editmode=False, location=location, layers=layers)
	cube = bpy.context.object
	cube.name = name
	cube.rotation_euler = rotation
	cube.data.materials.append(mat)
	return cube


def add_plane(config):
	plane = bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=config['location'], layers=layers)
	bpy.context.object.name = "surface"
	size = config['size']
	bpy.ops.transform.resize(value=(size, size, size), constraint_axis=(False, False, False))
	bpy.ops.rigidbody.objects_add()
	bpy.context.object.rigid_body.enabled = False
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
	scene = bpy.data.scenes[sceneKey]
	for cameraName in config['cameras']:
		scene.camera = bpy.data.objects[cameraName]
		scene.render.image_settings.file_format = 'JPEG'
		bpy.context.scene.render.resolution_x = config['res-x']
		bpy.context.scene.render.resolution_y = config['res-y']
		bpy.context.scene.render.resolution_percentage = config['res-percent']

		frames = 50, 100, 150
		for frame in frames:
			scene.frame_set(frame)
			scene.render.filepath = config['folder'] + '/' + config['name'] + '-' + cameraName + '-f-' + str(frame)
			bpy.ops.render.render(animation=False, write_still=True)


		config2 = {'folder': config['folder'], 
			'name': config['name'] + '-' + cameraName,
			'cameraName':cameraName,
			'objects': config['names']}

		create_info_file(config2)
		#create_info_file(config['folder'], config['name'] + '-' + cameraName, cameraName, config['names'])

def add_verical_borders(config):
	print(config)
	for key in config:
		add_verical_border(key) 

def add_verical_border(config):
	pos = config['pos']
	plane = config['normal']
	if plane == 'x':
		location = (pos, 0, 1)
		rotation = (0, math.pi / 2, 0)
		scale = (1, config['len'], 1)
	if plane == 'y':
		location = (0, pos, 1)
		rotation = (math.pi / 2, 0, 0)
		scale = (config['len'], 1, 1)
	plane = bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=location)
	bpy.context.object.rotation_euler = rotation
	bpy.ops.transform.resize(value=scale, constraint_axis=(False, False, False))
	bpy.ops.rigidbody.objects_add()
	bpy.context.object.rigid_body.enabled = False
	bpy.context.object.hide_render = True


def create_scene(config):
	beadsConfig = config['beads']
	for name, pos, rot in zip(beadsConfig['names'], beadsConfig['locations'], beadsConfig['rotations']):
		m = random.randint(0, T-1)
		print(name, m, pos, rot)
		create_bead(pos, rot, name, beadsConfig['materials'][m])
	add_plane(config['plane'])
	add_verical_borders(config['borders'])
	create_cube((0, 0, 1), (0, 0, 0), "cube", beadsConfig['materials'][0])

	for lamp in config['lamps']:
		add_lamp(lamp['strength'], bpy.data.objects[lamp['target']], lamp['location'])
	for camera in config['cameras']:
		add_camera(camera)


def create_info_file(config):
	infoFile = open(config['folder'] + '/' + config['name'] + '-data.txt', 'w')
	infoFile.write('# xmin, ymin, xmax, ymax\n')

	scene = bpy.context.scene
	render_scale = scene.render.resolution_percentage / 100
	render_size = (int(scene.render.resolution_x * render_scale), int(scene.render.resolution_y * render_scale))
	camera =  bpy.data.objects[config['cameraName']]

	for name in config['objects']:
		obj = bpy.data.objects[name]
		center = obj.location
		dim = obj.dimensions
		points =  [mathutils.Vector((h, w, d)) for h in [-1, 1] for w in [-1, 1] for d in [-1, 1]]
		vertices3d =  [mathutils.Vector(center) + mathutils.Vector((p[0]*dim[0]/2, p[1]*dim[1]/2, p[2]*dim[2]/2)) for p in points]
		vertices2d = [(round(v.x * render_size[0]), 
			round(v.y * render_size[1])) for v in [bpy_extras.object_utils.world_to_camera_view(scene, camera, b) for b in vertices3d]]
		minX = min([v[0] for v in vertices2d])
		minY = min([v[1] for v in vertices2d])
		maxX = max([v[0] for v in vertices2d])
		maxY = max([v[1] for v in vertices2d])
		box2d = [minX, minY, maxX, maxY]
		infoFile.write(', '.join([str(c) for c in box2d]) + '\n')

	infoFile.close()

bpy.context.scene.render.engine = 'CYCLES'


materials = [create_material('TexMat' + str(i), (random.random(), random.random(), random.random(), random.randrange(0, 5, 1)/5)) for i in range(1, T+1)]
locations = [(random.randrange(0, xmax/d, 1)*d, random.randrange(0, ymax/d, 1)*d, random.randrange(3, 20, 1)) for i in range(0, N)]
rotations = [(math.pi * random.random(), math.pi * random.random(), 0) for i in range(0, N)]
names = ['bead' + str(i) for i in range(0, N)]

bpy.ops.rigidbody.world_add()

create_scene(
	{'lamps': [
		{'strength': 3000, 'target': names[1], 'location': (3, 3, 5)}, 
		{'strength': 500, 'target': names[2], 'location': (0, -1, 5)},
		{'strength': 1000, 'target': names[3], 'location': (-2, -2, 5)}],
	'plane': {'location': (0, 0, 0), 'color': (0.4, 0.2, 0.1, 0.9), 'size': 7},
	'borders': [{'normal': 'x', 'pos': -5, 'len': 7}, {'normal': 'x', 'pos': 5, 'len': 7}, {'normal': 'y', 'pos': -5, 'len': 7}, {'normal': 'y', 'pos': 5, 'len': 7}],
	'beads': {'names': names, 'locations': locations, 'rotations': rotations, 'materials': materials},
	'cameras': [
		{'name': 'camera-1', 'location': (0, 0, 8), 'target': names[2], 'focal-length': 20, 'dof': 15},
		{'name': 'camera-2', 'location': (1, 2, 6), 'target': names[3]}
	]})

capture({
	'folder': currentDir + '/output', 
	'name': 'scene1', 
	'res-x': 400, 
	'res-y': 400, 
	'res-percent': 100,
	'cameras': ['camera-1', 'camera-2'], 
	'names': names})