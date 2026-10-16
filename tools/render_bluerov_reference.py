"""Render the official CAD reference mesh with no changes to its geometry."""
from pathlib import Path
import bpy
import math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
scene=bpy.context.scene
for o in list(scene.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.wm.stl_import(filepath=str(OUT/'_work/intermediate/bluerov_reference/bluerov_reference.stl'),global_scale=.001)
obj=bpy.context.object
obj.rotation_euler=(math.pi/2,0,0)
bpy.context.view_layer.update()
pts=[obj.matrix_world @ Vector(c) for c in obj.bound_box]
center=sum(pts,Vector())/8
obj.location-=center
camdata=bpy.data.cameras.new('Official CAD reference')
cam=bpy.data.objects.new('Official CAD reference',camdata);scene.collection.objects.link(cam)
cam.location=(.8,.95,.65)
cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler()
camdata.type='ORTHO';camdata.ortho_scale=.72;camdata.clip_start=.001;camdata.clip_end=10
scene.camera=cam
scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='SINGLE'
scene.display.shading.single_color=(.24,.39,.49)
scene.display.shading.background_type='WORLD'
scene.world.color=(.86,.88,.90)
scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
scene.display.shading.cavity_type='BOTH'
scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/'_work/images/bluerov2_official_cad_reference.png')
bpy.ops.render.render(write_still=True)
print('REFERENCE_RENDER_COMPLETE')
