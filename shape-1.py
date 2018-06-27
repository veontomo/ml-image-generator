import bpy


def delete_all():
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)

    for item in bpy.data.objects:
        bpy.data.objects.remove(item)

    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)

    for item in bpy.data.materials:
        bpy.data.materials.remove(item)

def add_cone():
    bpy.ops.mesh.primitive_cone_add()

def add_donut():
    for x in range(1, 2):
        bpy.ops.mesh.primitive_torus_add(location=[5*x, 0, 0], minor_radius=1.0, major_radius=1.0, rotation=[x, 0., 0.])

if __name__ == "__main__":
    delete_all()
    add_donut()
    new_mat = bpy.data.materials.new("WOOD")
    new_mat.diffuse_color = (0.73077, 0.0659535, 0.8)
    mesh = bpy.context.object.data
    mesh.materials.append(new_mat)

