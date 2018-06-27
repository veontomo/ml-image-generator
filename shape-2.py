#!bpy
"""
Name: 'material_procedural.py'
Blender: 2.69
Group: 'Materials and Textures'
Tooltip: 'Texturen procedurale'
"""

import bpy


def materialcheck(obj, materialart):
    """ Put a procedural textur on a object."""

    # used names
    matname = "mat" + materialart
    texname = "tex" + materialart

    # new material
    material = bpy.data.materials.new(matname)
    material.diffuse_color = (0, .5, 0)
    obj.data.materials.append(material)

    # new texture
    textur = bpy.data.textures.new(texname, type=materialart)

    # lits all properties and methods of a texture
    # print(dir(textur))

    # connect texture with material
    bpy.data.materials[matname].texture_slots.add()
    bpy.data.materials[matname].active_texture = textur


if __name__ == '__main__':

    # switch to object mode if edit mode is activ
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    # clear the scene
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    # all names of procedurale texturen, without IMAGE and LANDSCAPE
    materials = ['BLEND',
                 'CLOUDS',
                 'DISTORTED_NOISE',
                 'MAGIC',
                 'MARBLE',
                 'MUSGRAVE',
                 'NOISE',
                 'OCEAN',
                 'POINT_DENSITY',
                 'STUCCI',
                 'VORONOI',
                 'VOXEL_DATA',
                 'WOOD']

    x, y, z = 1, 0, 1
    for i in materials:
        # new line in the middle of the list
        if z % 7 == 0:
            y = 4
            x = 1
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0))
        obj = bpy.context.scene.objects.active

        obj.name = 'obj-%0.2d' % (z)
        obj = bpy.context.scene.objects['obj-%0.2d' % (z)]

        x += 3
        z += 1
        materialcheck(obj, i)