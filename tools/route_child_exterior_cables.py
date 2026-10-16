"""Find fixed cable corridors around the sampled guard sweep, in millimetres."""
import bpy
import json
import math
import heapq
from pathlib import Path
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
p=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
s=bpy.context.scene;s.frame_set(1)
dg=bpy.context.evaluated_depsgraph_get()
def tree(name):
    o=s.objects[name].evaluated_get(dg);m=o.to_mesh()
    vertices=[(o.matrix_world@v.co)*1000 for v in m.vertices]
    faces=[tuple(f.vertices) for f in m.polygons]
    o.to_mesh_clear()
    return BVHTree.FromPolygons(vertices,faces)
guard=tree('guard_integrated')
fixed=[tree(r['label']) for r in p['items'] if r['group'] in ['vessel','Integrated clamp cradle','Frame A','Frame C','Fixed hinge and pin']]
pivot=Vector(p['hinge']['pivot_world_mm'])
inverse=[Matrix.Rotation(math.radians(a),3,'X') for a in range(86)]
cache={}
def clear(pt):
    key=tuple(pt)
    if key in cache:return cache[key]
    v=Vector(pt)
    for t in fixed:
        hit,n,_,dist=t.find_nearest(v)
        if dist<6 or (v-hit).dot(n)<-1e-5:
            cache[key]=False;return False
    for rot in inverse:
        q=rot@(v-pivot)+pivot
        hit,n,_,dist=guard.find_nearest(q)
        if dist<6 or (q-hit).dot(n)<-1e-5:
            cache[key]=False;return False
    cache[key]=True;return True
def solve(start,goal):
    assert clear(start),('start blocked',start)
    assert clear(goal),('goal blocked',goal)
    queue=[(0,start)]; cost={start:0}; prev={}
    directions=[(x,y,z) for x in [-5,0,5] for y in [-5,0,5] for z in [-5,0,5] if (x,y,z)!=(0,0,0)]
    while queue:
        _,cur=heapq.heappop(queue)
        if cur==goal:break
        for step in directions:
            nxt=tuple(a+b for a,b in zip(cur,step))
            x,y,z=nxt
            if not (-75<=x<=75 and -175<=y<=40 and -125<=z<=80):continue
            dist=math.dist(cur,nxt)
            new=cost[cur]+dist
            if new>=cost.get(nxt,float('inf')) or not clear(nxt):continue
            if not clear(tuple((a+b)/2 for a,b in zip(cur,nxt))):continue
            cost[nxt]=new;prev[nxt]=cur
            heapq.heappush(queue,(new+math.dist(nxt,goal),nxt))
    else:raise RuntimeError('No fixed cable corridor found')
    path=[goal]
    while path[-1]!=start:path.append(prev[path[-1]])
    path.reverse()
    print('PATH',path,flush=True)
    return path
routes=[]
for sign in [1,-1]:
    path=solve((sign*20,sign*5,-25),(sign*65,-120,20))
    routes.append(path)
(OUT/'_work/logs/cable_corridors.json').write_text(json.dumps(routes,indent=2)+'\n',encoding='utf-8')
