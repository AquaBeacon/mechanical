"""Verify saved horizontal Blender scene. Manufacturing remains unverified."""
from pathlib import Path
import hashlib
import json
import math
import bpy
import bmesh
from mathutils import Matrix, Vector, Euler
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'assemblies/child_exterior_concept'
placement = json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
assert placement.get('layout') == 'horizontal_open_frame_20261007', 'Use archived verifier for vertical history'
scene = bpy.context.scene
scene.frame_set(1)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
objects = {o.get('placement_label'):o for o in scene.objects if o.get('placement_label')}
errors=[]
report=dict(status='exploration_only', checks={}, intersections=[], mesh_issues=[])


def expected_matrix(ops):
    result=Matrix.Identity(4)
    for op in ops:
        for kind,value in op.items():
            if kind=='translate':
                mat=Matrix.Translation(Vector(value)*.001)
            elif kind=='rotate':
                mat=Euler(tuple(math.radians(v) for v in value),'XYZ').to_matrix().to_4x4()
            else:
                raise ValueError(kind)
            result=result @ mat
    return result


def geometry(obj):
    evaluated=obj.evaluated_get(deps)
    mesh=evaluated.to_mesh()
    verts=[obj.matrix_world @ v.co for v in mesh.vertices]
    faces=[tuple(p.vertices) for p in mesh.polygons]
    bm=bmesh.new();bm.from_mesh(mesh)
    bad=sum(not e.is_manifold for e in bm.edges)
    bm.free();evaluated.to_mesh_clear()
    return verts,faces,bad


geometry_by_label={}
for item in placement['items']:
    label=item['label']
    if item.get('print') is not False:
        errors.append('Unexpected printable item: '+label)
    if label not in objects:
        errors.append('Missing object: '+label);continue
    obj=objects[label]
    expected=expected_matrix(item.get('ops',[]))
    # STL import keeps the mm-to-m factor in object scale; primitives bake it.
    if not item.get('geometry'):
        expected=expected @ Matrix.Diagonal(Vector([.001,.001,.001,1]))
    deviation=max(abs(obj.matrix_world[i][j]-expected[i][j]) for i in range(4) for j in range(4))
    if deviation>1e-6:
        errors.append('Placement differs: '+label)
    verts,faces,bad=geometry(obj)
    geometry_by_label[label]=(verts,faces,BVHTree.FromPolygons(verts,faces))
    if bad:
        report['mesh_issues'].append(dict(label=label,non_manifold_edges=bad))
        if item.get('geometry')=='concept':errors.append('New concept mesh is not closed: '+label)
    for field,local in [('view_direction',[0,1,0] if label=='action_camera_front' else [0,0,1]),('acoustic_direction',item.get('local_acoustic_axis',[0,0,-1]))]:
        if field in item:
            actual=(obj.matrix_world.to_3x3() @ Vector(local)).normalized()
            if (actual-Vector(item[field])).length>1e-6:errors.append('Direction differs: '+label)
            report['checks'][label+'_direction']=list(actual)
report['checks']['object_count']=len(objects)
report['checks']['placements_checked']=len(placement['items'])
axis=(objects['acrylic_tube_200'].matrix_world.to_3x3() @ Vector([1,0,0])).normalized()
report['checks']['tube_axis']=list(axis)
if (axis-Vector([0,1,0])).length>1e-6:errors.append('Vessel is not horizontal/forward')
manifest=json.loads((OUT/'_work/logs/build_manifest.json').read_text(encoding='utf-8'))
for path,digest in manifest['source_sha256'].items():
    if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:errors.append('Source changed since build: '+path)
report['checks']['source_hashes_checked']=len(manifest['source_sha256'])
vessel=[x['label'] for x in placement['items'] if x['group']=='vessel']
equipment=['action_camera_front','dive_light_rear','transducer_upward']
weights=[x['label'] for x in placement['items'] if 'declared_mass_g' in x]
foam=['foam_space_left','foam_space_right']
tested=set()
for firsts,seconds in [(vessel,equipment+weights+foam),(equipment,weights+foam),(weights,foam)]:
    for a in firsts:
        for b in seconds:
            pair=tuple(sorted((a,b)))
            if a==b or pair in tested:continue
            tested.add(pair)
            if geometry_by_label[a][2].overlap(geometry_by_label[b][2]):
                report['intersections'].append([a,b]);errors.append('Unexpected surface intersection: '+a+' / '+b)
report['checks']['surface_pairs_checked']=len(tested)
ray_checks={}
for label in ['dive_light_rear','transducer_upward']:
    top=max(v.z for v in geometry_by_label[label][0])
    x,y=objects[label].matrix_world.translation[:2]
    origin=Vector([x,y,top+.001]);hits=[]
    for target,(_,_,tree) in geometry_by_label.items():
        if target!=label and tree.ray_cast(origin,Vector([0,0,1]),2)[0] is not None:hits.append(target)
    ray_checks[label]=hits
    if hits:errors.append('Upward axis obstructed: '+label)
report['checks']['upward_axis_obstructions']=ray_checks
report['checks']['declared_ballast_g']=sum(i.get('declared_mass_g',0) for i in placement['items'])
if report['checks']['declared_ballast_g']!=2240:errors.append('Ballast inventory changed')
verts=[v for vs,_,_ in geometry_by_label.values() for v in vs]
lo=[min(v[j] for v in verts)*1000 for j in range(3)];hi=[max(v[j] for v in verts)*1000 for j in range(3)]
report['checks']['assembly_bounds_mm']=[lo,hi]
report['checks']['assembly_dimensions_mm']=[hi[j]-lo[j] for j in range(3)]
report['intentional_contacts']=['Reference clamps / liners / vessel','Cradle pads / concept support rails','Side frames / skids / crossbars / mounts','Ballast supports / retaining bands']
report['limits']=['Surface tests omit complete containment and intentional support interfaces.','No strength, pressure, full optical/acoustic cone, hydrostatic trim, cable/tool passage or manufacturing certification.']
report['errors']=errors;report['passed']=not errors
(OUT/'_work/logs/horizontal_layout_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('HORIZONTAL_LAYOUT_CHECK',json.dumps(report,ensure_ascii=True))
if errors:raise SystemExit(1)
