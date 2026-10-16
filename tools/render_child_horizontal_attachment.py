"""Render the existing cage and its three right-side adapters in isolation.

Uses the saved, verified CAD presentation; hides objects for inspection only.
No mesh, placement or saved assembly is altered.
"""
from pathlib import Path
import hashlib
import json
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_horizontal'
blend=OUT/'child_exterior_horizontal.blend'
bpy.ops.wm.open_mainfile(filepath=str(blend))
scene=bpy.context.scene
placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
visible=[]
for item in placement['items']:
    name=item['label'];obj=bpy.data.objects.get(name)
    if obj is None:raise RuntimeError('Missing assembly object '+name)
    show=item['group'] in ['vessel','clamps','rubber'] or name.startswith('right_clamp_')
    obj.hide_render=not show
    if show:visible.append(name)
for obj in scene.objects:
    if obj.type=='CURVE':obj.hide_render=True
camera=bpy.data.objects['07 | Cradle and lower ballast']
camera.location=Vector((470,-360,320))*.001
direction=Vector((50,0,140))*.001-camera.location
camera.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
camera.data.ortho_scale=.33
scene.camera=camera
scene.render.threads_mode='FIXED';scene.render.threads=8
scene.cycles.samples=32
scene.render.resolution_x=1500;scene.render.resolution_y=1100
scene.render.filepath=str(OUT/'_work/images/clamp_links_isolated.png')
bpy.ops.render.render(write_still=True)
report=dict(source_blend_sha256=hashlib.sha256(blend.read_bytes()).hexdigest(),
            visible_labels=visible,note='Objects hidden for inspection; geometry and assembly file unchanged.')
(OUT/'_work/logs/clamp_links_render.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
