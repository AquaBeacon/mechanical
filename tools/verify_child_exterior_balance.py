"""Declared ballast mass balance and sampled cable clearance for the saved concept."""
import bpy
import json
import math
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.geometry import interpolate_bezier
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
p=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
inventory=json.loads((ROOT/'parts/common/exterior/cots/ballast_inventory.json').read_text(encoding='utf-8'))
mass_by_file={r['mesh_file'][:-4]:r['mass_g'] for r in inventory['items']}
s=bpy.context.scene;s.frame_set(1)
dg=bpy.context.evaluated_depsgraph_get()
def mesh(name):
    o=s.objects[name].evaluated_get(dg);m=o.to_mesh();m.calc_loop_triangles()
    verts=[o.matrix_world@v.co*1000 for v in m.vertices]
    faces=[tuple(t.vertices) for t in m.loop_triangles]
    o.to_mesh_clear();return verts,faces
def tree(name):
    v,f=mesh(name);return BVHTree.FromPolygons(v,f)
ballast=[]
for row in p['items']:
    if row['group'] not in ['Ballast B','Ballast C']:continue
    v,f=mesh(row['label']);volume=0;moment=Vector((0,0,0))
    for face in f:
        a,b,c=[v[i] for i in face];q=a.dot(b.cross(c))/6
        volume+=q;moment+=(a+b+c)*q/4
    center=moment/volume
    mass=mass_by_file[row['file']]
    assert mass==row['mass_g']
    ballast.append(dict(label=row['label'],mass_g=mass,centroid_mm=list(center)))
total=sum(r['mass_g'] for r in ballast)
center=sum((Vector(r['centroid_mm'])*r['mass_g'] for r in ballast),Vector())/total
assert abs(center.x)<.001 and abs(center.y)<.001 and total==2240,(total,center)
assert sum(r['mass_g'] for r in ballast if r['centroid_mm'][0]<-1)==120
assert sum(r['mass_g'] for r in ballast if r['centroid_mm'][0]>1)==120
assert sum(r['mass_g'] for r in ballast if r['centroid_mm'][1]<-1)==1000
assert sum(r['mass_g'] for r in ballast if r['centroid_mm'][1]>1)==1000
guard=tree('guard_integrated');pivot=Vector(p['hinge']['pivot_world_mm'])
paths=[];clearances=[]
for route in p['cable_routes']:
    obj=s.objects[route['label']]
    points=obj.data.splines[0].bezier_points
    path=[]
    for a,b in zip(points,points[1:]):
        path += [obj.matrix_world@v*1000 for v in interpolate_bezier(a.co,a.handle_right,b.handle_left,b.co,65)]
    paths.append(path)
    closest=float('inf');at=None
    for angle in range(86):
        inverse=Matrix.Rotation(math.radians(angle),3,'X')
        for point in path:
            q=inverse@(point-pivot)+pivot
            _,_,_,distance=guard.find_nearest(q)
            clearance=distance-route['radius_mm']
            if clearance<closest:closest,at,at_point=clearance,angle,list(point)
    assert closest>0,(route['label'],closest,at)
    clearances.append(dict(label=route['label'],sampled_surface_clearance_mm=closest,angle_deg=at,point_mm=at_point))
kd=KDTree(len(paths[0]))
for i,point in enumerate(paths[0]):kd.insert(point,i)
kd.balance()
separation=min(kd.find(point)[2] for point in paths[1])-sum(r['radius_mm'] for r in p['cable_routes'])
assert separation>0,separation
collisions=[]
for route in p['cable_routes']:
    cable=tree(route['label'])
    for row in p['items']:
        if row['group'] in ['Transducer','Transducer mount']:continue # intentional cable endpoint
        if cable.overlap(tree(row['label'])):collisions.append([route['label'],row['label']])
report=dict(declared_mass_total_g=total,front_rear_c_g=1000,left_right_b_g=120,ballast_centroid_mm=list(center),items=ballast,
    centroid_assumption='Homogeneous reference ballast geometry; masses from declared inventory, never inferred from volume. Not whole-vehicle CG/CB.',
    sampled_guard_cable_clearance=clearances,sampled_cable_surface_separation_mm=separation,
    cable_static_surface_intersections=collisions,
    limitation='Centreline samples and one-degree guard poses; real cable bend radius, tolerances and deflection unverified.')
(OUT/'_work/logs/ballast_balance_and_cables.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
assert not collisions,collisions
