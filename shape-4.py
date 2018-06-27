import bpy
import math

bpy.ops.object.empty_add(type='CUBE', view_align=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

cam = bpy.data.objects['Camera']

origin = bpy.data.objects['Empty']

def radians(grad):
	return 2*math.pi*grad/360

step_count = 32

for step in range(0, step_count):
    origin.rotation_euler[2] = radians(step * (360.0 / step_count))

    bpy.data.scenes["Scene"].render.filepath = 'renedered/shot_%d.jpg' % step
    bpy.ops.render.render( write_still=True )