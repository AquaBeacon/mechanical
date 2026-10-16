"""Refresh STL from the already rebuilt analytic STEP after every generated SCAD.

All generated SCAD files are source-tracked by the packager. Refreshing only the
first STL before later SCAD files are written leaves a misleading stale timestamp.
This performs a real remesh and validates it, rather than changing timestamps.
"""
from parent_access_common import mesh_volume
import FreeCAD as A,Part,MeshPart
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];checks=[]
# All SCAD outputs precede every STL refresh, including the battery in the
# same source folder, because packaging tracks that entire folder's CAD.
floor_path=R/'parts/parent/interior/printed/parent_hand_service/floor_plate.step'
floor_shape=Part.read(str(floor_path))
floor_mesh=MeshPart.meshFromShape(Shape=floor_shape,LinearDeflection=.025,AngularDeflection=.10,Relative=False)
points,faces=floor_mesh.Topology
text='// Generated from the rebuilt analytic STEP. Parameters: spec/build_parent_hand_service.py.\npolyhedron(points='+json.dumps([[p.x,p.y,p.z] for p in points])+',faces='+json.dumps([list(face) for face in faces])+',convexity=10);\n'
floor_path.with_suffix('.scad').write_text(text,encoding='utf-8')
for folder in ['parent_hand_service','ann_mb1_internal_rack','gnss_universal_carrier','parent_lipo_retainer']:
    p=R/'parts/parent/interior/printed'/folder
    skip=json.loads((p/'manufacturing.json').read_text()).get('non_print_files',[])
    for f in sorted(p.glob('*.step')):
        if f.stem in skip:continue
        s=Part.read(str(f));assert s.isValid() and len(s.Solids)==1,f
        m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.025,AngularDeflection=.10,Relative=False)
        assert m.isSolid(),f
        b=s.optimalBoundingBox(False,False)
        delta=max(abs(getattr(b,k)-getattr(m.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
        diff=abs(s.Volume-mesh_volume(m))/s.Volume
        assert delta<.05 and diff<.02,(f,delta,diff)
        m.write(str(f.with_suffix('.stl')))
        checks.append({'part':f.relative_to(R).as_posix(),'closed_stl':True,'solids':1,'bbox_difference_mm':delta,'relative_volume_difference':diff})
(R/'assemblies/parent_hand_service/remesh_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('PASS: validated and remeshed',len(checks),'printable STEP sources',flush=True)
