import bpy
from mathutils import Vector
import math

def delete_all():
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)

    for item in bpy.data.objects:
        bpy.data.objects.remove(item)

    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)

    for item in bpy.data.materials:
        bpy.data.materials.remove(item)


def add_shape(pos, marker):
    N = 30
    verts = []
    faces = []
    for n in range(0, N):
        alpha = 2*math.pi*n/N
        x, y = math.cos(alpha), math.sin(alpha)
        verts.append((x, y, 0))
        verts.append((x, y, 1))
    for n in range(0, 2*(N - 1), 2):
        faces.append((n, n + 1,  n + 3, n + 2))
    faces.append((2*(N - 1), 2*N - 1, 1,  0))
    faces.append([n for n in range(0, 2 * N, 2)])
    faces.append([n for n in range(1, 2 * N, 2)])
    beadmesh = bpy.data.meshes.new(marker)
    beadobj = bpy.data.objects.new(marker, beadmesh)
    beadobj.location = (pos[0], pos[1], pos[2])
    bpy.context.scene.objects.link(beadobj)
    beadmesh.from_pydata(verts, [], faces)
    beadmesh.update(calc_edges=True)

#delete_all()

def add_sun(location):
    bpy.ops.object.delete(use_global=False)
    bpy.ops.object.lamp_add(type='SUN', view_align=False, location=location, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

def add_camera(location):
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=location, rotation=(1.10871, 0.0132652, 1.14827), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))


add_shape((2, 0, 0), "bead1")
add_shape((0, 2, 0), "bead2")
add_shape((-2, 0, 3), "bead3")
add_shape((0, -2, 5), "bead4")
#add_sun((0, 0, 10))
add_camera((3, 3, 5))


bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


bpy.context.space_data.context = 'CONSTRAINT'
bpy.ops.object.constraint_add(type='TRACK_TO')
bpy.context.object.constraints["Track To"].target = bpy.data.objects["bead1"]

#bm = beadobj.modifiers.new("Chop", 'BOOLEAN')
for f in beadobj.faces:
    f.smooth = True


# object's location
bpy.data.objects["Torus.002"].location

# Euler's angles of the object
bpy.data.objects["Torus.002"].matrix_world.to_euler()

# object's bounding box dimensions
bpy.data.objects["Torus.002"].dimensions


bpy.ops.object.delete(use_global=False)
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.mesh.primitive_torus_add(name="bead1", view_align=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False), major_radius=1, minor_radius=0.25, abso_major_rad=1.25, abso_minor_rad=0.75)

bpy.ops.transform.resize(value=(2.90156, 2.90156, 2.90156), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.ops.transform.resize(value=(2.47123, 2.47123, 2.47123), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
bpy.context.object.name = "bead"
