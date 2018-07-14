import bpy

bpy.context.object.rotation_euler = (0.5, 0.5, 0.5)
bpy.ops.rigidbody.world_add()
bpy.ops.rigidbody.objects_add()

plane = bpy.ops.mesh.primitive_plane_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, -10))
bpy.context.object.name = "surface"
bpy.ops.rigidbody.objects_add()
bpy.context.object.rigid_body.enabled = False

scene.frame_set(50)

#bpy.context.scene.rigidbody_world.group.objects.link(D.objects['Cube'])