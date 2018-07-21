import bpy
import bpy_extras
import math
import os
import random
import mathutils
import sys
import time
from bpy_extras.view3d_utils import location_3d_to_region_2d

# this file's folder
currentDir = os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.delete(use_global=False)

print(sys.version_info)

random.seed(0.1)

def create_bead(config):
	bpy.ops.mesh.primitive_torus_add(view_align=False, 
		location=config['location'], 
		layers=layers, 
		major_radius=config['r1'], 
		minor_radius=config['r2'])
	bpy.ops.transform.resize(value=(1, 1, config['scale']), 
		constraint_axis=(False, False, True), 
		constraint_orientation='GLOBAL', 
		mirror=False, 
		proportional='DISABLED', 
		proportional_edit_falloff='SMOOTH', 
		proportional_size=1)
	bpy.ops.rigidbody.objects_add()
	bead = bpy.context.object
	bead.name = config['name']
	bead.rotation_euler = config['rotation']
	bead.data.materials.append(config['material'])
	return bead

def create_cube(config):
	bpy.ops.mesh.primitive_cube_add(radius=config['radius'], 
		view_align=False, 
		enter_editmode=False, 
		location=config['location'], 
		layers=layers)
	bpy.ops.rigidbody.objects_add()
	obj = bpy.context.object
	obj.name = config['name']
	obj.rotation_euler = config['rotation']
	obj.data.materials.append(config['material'])
	return obj

def create_sphere(config):
	bpy.ops.mesh.primitive_uv_sphere_add(size=config['size'], 
		view_align=False, 
		enter_editmode=False, 
		location=config['location'], 
		layers=layers)
	bpy.ops.rigidbody.objects_add()
	obj = bpy.context.object
	obj.name = config['name']
	obj.data.materials.append(config['material'])
	return obj

def create_cone(config):
	bpy.ops.mesh.primitive_cone_add(radius1=config['radius1'], 
		radius2=config['radius2'], 
		depth=config['radius1'], 
		view_align=False, 
		enter_editmode=False, 
		location=config['location'], 
		layers=layers)
	bpy.ops.rigidbody.objects_add()
	obj = bpy.context.object
	obj.name = config['name']
	obj.rotation_euler = config['rotation']
	obj.data.materials.append(config['material'])
	return obj


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

def add_lamp(config):
	bpy.ops.object.lamp_add(type = config['type'] if 'type' in config else 'SPOT', 
		radius=20, 
		view_align=False, 
		location=config['location'], 
		layers=layers)
	rawName = bpy.context.object.name
	if 'color' in config:
		bpy.data.lamps[rawName].node_tree.nodes["Emission"].inputs[0].default_value = config['color']
	bpy.data.lamps[rawName].node_tree.nodes['Emission'].inputs[1].default_value = config['strength']
	lamp = bpy.data.objects[rawName] 
	if 'target' in config:
		trackConstraint = lamp.constraints.new("TRACK_TO")
		trackConstraint.target = bpy.data.objects[config['target']]
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
	if 'target' in config:
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

		for frame in config['frames']:
			filename = config['folder'] + '/' + config['name'] + '-' + cameraName + '-f-' + str(frame)
			scene.frame_set(frame)
			scene.render.filepath = filename
			bpy.ops.render.render(animation=False, write_still=True)


			config2 = {
				'folder': config['folder'], 
				'name': filename,
				'cameraName': cameraName,
				'objects': config['names'],
				'frame': frame
			}

			create_info_file(config2)

def create_info_file(config):
	infoFile = open(config['name'] + '-data.txt', 'w')
	infoFile.write('# xmin, ymin, xmax, ymax\n')

	scene = bpy.context.scene
	scene.frame_set(config['frame'])
	render_scale = scene.render.resolution_percentage / 100
	render_size = (int(scene.render.resolution_x * render_scale), int(scene.render.resolution_y * render_scale))
	camera =  bpy.data.objects[config['cameraName']]

	for name in config['objects']:
		obj = bpy.data.objects[name]
		# center = obj.location
		center = obj.matrix_world.to_translation()
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
		create_bead({'location': pos, 
			'r1': r1, 'r2': 0.8*r1, 
			'rotation': rot, 
			'name': name,
			'scale': 2, 
			'material': random.choice(beadsConfig['materials'])})
	cubesConfig = config['cubes']
	for name, pos, rot in zip(cubesConfig['names'], cubesConfig['locations'], cubesConfig['rotations']):
		create_cube({'location': pos, 
			'radius': 1.5*r1,
			'rotation': rot, 
			'name': name,
			'material': random.choice(cubesConfig['materials'])})
	sphereConfig = config['spheres']
	for name, pos in zip(sphereConfig['names'], sphereConfig['locations']):
		create_sphere({'location': pos, 
			'size': 2*r1,
			'name': name,
			'material': random.choice(sphereConfig['materials'])})
	coneConfig = config['cones']
	for name, pos, rot in zip(coneConfig['names'], coneConfig['locations'], coneConfig['rotations']):
		create_cone({'location': pos, 
			'radius1': 2*r1,
			'radius2': 0,
			'name': name,
			'rotation': rot,
			'material': random.choice(coneConfig['materials'])})

	add_plane(config['plane'])
	add_verical_borders(config['borders'])

	for lampConfig in config['lamps']:
		add_lamp(lampConfig)
	for camera in config['cameras']:
		add_camera(camera)

def generateLocations(locations, n, area, d):
	""" Generate n point in the given area using locations as a seed. 
	Distance between each pair of point should be greater that d.
	area - array of two points (xmin, ymin) and (xmax, ymax)
	"""
	xmin, xmax, ymin, ymax, = area[0][0] + d, area[0][1] - d, area[1][0] + d, area[1][1] - d

	if n == 0:
		return locations
	else:
		init = (random.random()*(xmax-xmin) + xmin, random.random()*(xmax-xmin) + xmin, 1)
		while not distant(init, locations, d):
			init = (init[0], init[1], init[2] + d)
		return generateLocations(locations + [init], n - 1, area, d)

def distant(point, points, d):
	"""Return true if the distance between given point and every point in points is greater that d"""
	for p in points:
		if distanceSquare(point, p) < d**2:
			return False
	return True
	

def distanceSquare(p1, p2):
	return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2


bpy.context.scene.render.engine = 'CYCLES'


layers = tuple([True] + 19*[False])
r1 = 0.2
d = 2*r1
z = 2*r1

Qty = [{'type': 'bead', 'qty': 50}, {'type': 'cube', 'qty': 7}, {'type': 'sphere', 'qty': 15}, {'type': 'cone', 'qty': 7}]
v = [i['qty'] for i in Qty]
print(v)
stoppers = [sum(v[:i]) for i in (range(0, len(v) + 1))]
print(stoppers)
N = sum([i['qty'] for i in Qty])
T = 5
scale = 2

materials = [create_material('TexMat' + str(i), (random.random(), random.random(), random.random(), random.randrange(0, 5, 1)/5)) for i in range(1, T+1)]
locations = generateLocations([], N, [[-5, 5], [-5, 5]], 2*r1*scale)
rotations = [(math.pi * random.random(), math.pi * random.random(), 0) for i in range(0, N)]
names = {i['type']: [i['type'] + '-' + str(k) for k in range(0, i['qty'])] for i in Qty}



bpy.ops.rigidbody.world_add()

create_scene(
	{'lamps': [
		{'strength': 3000, 'target': names['bead'][1], 'location': (5, 5, 4), 'color': (0.0607904, 1, 0.153419, 1)}, 
		{'strength': 10, 'target': names['bead'][2], 'location': (-5, 5, 5), 'type': 'SUN'},
		{'strength': 500, 'target': names['bead'][2], 'location': (-5, -5, 3)},
		{'strength': 1000, 'target': names['bead'][3], 'location': (5, -5, 6)}],
	'plane': {'location': (0, 0, 0), 'color': (0.4, 0.2, 0.1, 0.9), 'size': 7},
	'borders': [{'normal': 'x', 'pos': -5, 'len': 7}, {'normal': 'x', 'pos': 5, 'len': 7}, {'normal': 'y', 'pos': -5, 'len': 7}, {'normal': 'y', 'pos': 5, 'len': 7}],
	'beads': {'names': names['bead'], 
		'locations': locations[0:stoppers[1]], 
		'rotations': rotations[0:stoppers[1]], 
		'materials': materials},
	'cubes': {'names': names['cube'], 
		'locations': locations[stoppers[1]:stoppers[2]], 
		'rotations': rotations[stoppers[1]:stoppers[2]], 
		'materials': materials},
	'spheres': {'names': names['sphere'], 
		'locations': locations[stoppers[2]:stoppers[3]], 
		'rotations': rotations[stoppers[2]:stoppers[3]], 
		'materials': materials},
	'cones': {'names': names['cone'], 
		'locations': locations[stoppers[3]:stoppers[4]], 
		'rotations': rotations[stoppers[3]:stoppers[4]], 
		'materials': materials},
	'cameras': [
		{'name': 'camera-1', 'location': (0, 0, 5), 'target': names['bead'][1], 'focal-length': 25, 'dof': 5},
		{'name': 'camera-2', 'location': (0, -5, 4), 'target': names['bead'][3]},
		{'name': 'camera-3', 'location': (5, 0, 4), 'target': names['bead'][1]},
		{'name': 'camera-4', 'location': (0, 5, 6), 'target': names['bead'][2]},
		{'name': 'camera-5', 'location': (-5, 0, 5), 'target': names['bead'][4]},
	]})

def clear_scene(scene):
	for obj in scene.objects:
		scene.objects.unlink(obj)


bpy.ops.ptcache.bake_all(bake=True)

#capture({
#	'folder': currentDir + '/output', 
#	'name': 'scene1', 
#	'res-x': 100, 
#	'res-y': 100, 
#	'res-percent': 50,
#	'cameras': ['camera-1', 'camera-2', 'camera-3', 'camera-4', 'camera-5'], 
#	'names': names['bead'],
#	'frames': [100, 240]})

clear_scene(bpy.data.scenes[0])
#for n in names:
#	print("removing all", n)
#	for name in names[n]:
#		bpy.data.scenes[0].objects.unlink(bpy.data.objects[name])
