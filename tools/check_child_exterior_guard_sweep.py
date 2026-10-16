"""Sample world-space mesh intersections throughout the concept opening sweep."""
import bpy
import json
import math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
p=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
scene=bpy.context.scene
scene.frame_set(1)
moving=p['hinge']['moving_labels']
fixed=[r['label'] for r in p['items'] if r['label'] not in moving]
fixed += [o.name for o in bpy.data.collections['Indicative cable'].objects]
fixed += [o.name for group in ['Visual fasteners','Cable ties']
          for o in bpy.data.collections[group].objects]
dg=bpy.context.evaluated_depsgraph_get()
def mesh(name):
    o=scene.objects[name].evaluated_get(dg)
    m=o.to_mesh()
    vertices=[o.matrix_world @ v.co for v in m.vertices]
    faces=[tuple(f.vertices) for f in m.polygons]
    o.to_mesh_clear()
    bounds=[tuple(min(v[i] for v in vertices) for i in range(3)),
            tuple(max(v[i] for v in vertices) for i in range(3))]
    return BVHTree.FromPolygons(vertices,faces),bounds
static={n:mesh(n) for n in fixed}
pivot=scene.objects['Cable guard hinge pivot']
report=[]
angles=list(range(86))
for angle in angles:
    pivot.rotation_euler=Vector(p['hinge']['axis_world'])*math.radians(-angle)
    bpy.context.view_layer.update()
    hits=[]
    for name in moving:
        tree,bounds=mesh(name)
        for other,(target,box) in static.items():
            if any(bounds[1][i]<box[0][i] or box[1][i]<bounds[0][i] for i in range(3)):
                continue
            overlap=tree.overlap(target)
            if overlap:
                hits.append([name,other,len(overlap)])
    report.append(dict(angle_deg=angle,intersections=hits))
    print(angle,hits,flush=True)
(OUT/'_work/logs/guard_sweep.json').write_text(json.dumps({
    'method':'World-space evaluated triangle surface intersections; sampled angles, not a continuous clearance proof',
    'samples':report},indent=2)+'\n',encoding='utf-8')
scene.frame_set(1)
