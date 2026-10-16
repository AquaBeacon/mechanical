"""Check provisional open-guard hand corridors and raised ballast clearances."""
import bpy
import json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
p=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
s=bpy.context.scene
s.frame_set(p['hand_access']['check_frame'])
dg=bpy.context.evaluated_depsgraph_get()
def geometry(name):
    obj=s.objects[name].evaluated_get(dg);m=obj.to_mesh();m.calc_loop_triangles()
    v=[obj.matrix_world@a.co*1000 for a in m.vertices]
    f=[tuple(a.vertices) for a in m.loop_triangles]
    obj.to_mesh_clear()
    return v,BVHTree.FromPolygons(v,f)
names=[r['label'] for r in p['items']]
names += [o.name for group in ['Indicative cable','Cable ties','Visual fasteners'] for o in bpy.data.collections[group].objects]
meshes={name:geometry(name) for name in names}
faces=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
corridors=[]
for side,xrange in [('left',[-170,0]),('right',[0,170])]:
    ranges=[xrange,*p['hand_access']['provisional_hand_corridor_yz_mm']]
    vertices=[Vector((x,y,z)) for x in ranges[0] for y in ranges[1] for z in ranges[2]]
    probe=BVHTree.FromPolygons(vertices,faces)
    hits=[]
    for name,(v,t) in meshes.items():
        if probe.overlap(t) or any(all(ranges[i][0]<q[i]<ranges[i][1] for i in range(3)) for q in v):
            hits.append(name)
    corridors.append(dict(side=side,bounds_mm=ranges,obstructions=hits))
ballast_hits=[]
internal_clearances=[]
for row in p['items']:
    if row['group']!='Ballast C':continue
    verts=meshes[row['label']][0]
    gap=p['ballast_mount']['frame_c_center_y_mm']-5-max(abs(v.y) for v in verts)
    assert gap>0,(row['label'],'Outside purple C')
    internal_clearances.append(dict(label=row['label'],clearance_to_c_inner_plane_mm=gap))
    for other in p['items']:
        if other['label']==row['label'] or other['group']=='Ballast retainers':continue
        if meshes[row['label']][1].overlap(meshes[other['label']][1]):
            ballast_hits.append([row['label'],other['label']])
support_hits=[]
for row in p['items']:
    if row['label'] not in p['ballast_mount']['integrated_support_labels']:continue
    for other in p['items']:
        if other['group'] in ['Frame C','Ballast retainers','Ballast C','Frame A','Equipment mounts','Upward lights','Transducer mount']:continue # intended C-mounted interfaces
        if meshes[row['label']][1].overlap(meshes[other['label']][1]):
            support_hits.append([row['label'],other['label']])
report=dict(frame=s.frame_current,hand_corridors=corridors,raised_ballast_surface_intersections=ballast_hits,
    internal_ballast_clearances=internal_clearances,support_surface_intersections=support_hits,
    limitation='Provisional straight 90 x 60 mm hand envelope; no ergonomic or structural certification. Surface intersections plus mesh vertices inside corridor checked.')
(OUT/'_work/logs/hand_access.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
assert not ballast_hits,ballast_hits
assert not support_hits,support_hits
assert not any(r['obstructions'] for r in corridors),corridors
mount_axes=0
for sign,side in [(-1,'left'),(1,'right')]:
    for y,z in p['ballast_mount']['frame_mount_holes_yz_mm']:
        support='C_rear' if y<0 else 'C_front'
        for name in ['A_'+side+'_lower',support]:
            hit=meshes[name][1].ray_cast(Vector((sign*140,y,z)),Vector((-sign,0,0)),65)
            assert hit[0] is None,(name,y,z,'Support mounting hole blocked')
        mount_axes+=1
    for row in p['items']:
        if row['group']!='Ballast B' or row['ops'][0]['translate'][0]*sign<0:continue
        z=row['ops'][0]['translate'][2]
        for y in p['ballast_mount']['plate_holes_y_mm']:
            for name in ['A_'+side+'_lower',row['label']]:
                hit=meshes[name][1].ray_cast(Vector((sign*140,y,z)),Vector((-sign,0,0)),60)
                assert hit[0] is None,(name,y,z,'Plate mounting hole blocked')
            mount_axes+=1
report['verified_new_mount_axes']=mount_axes
(OUT/'_work/logs/hand_access.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS new support and existing plate hole axes:',mount_axes)
