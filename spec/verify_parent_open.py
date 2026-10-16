"""Run with FreeCAD console: export structural assembly and check solid collisions."""
import json,os
from pathlib import Path
import FreeCAD as A, Part
ROOT=Path(__file__).resolve().parents[1]; NAME=os.environ.get('PARENT_VERIFY_NAME','parent_open');OUT=ROOT/'assemblies'/NAME
layout=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
doc=A.newDocument('ParentOpen'); shapes=[]; omitted=[]
for it in layout['items']:
    if it['group']=='hardware':continue
    src=ROOT/it['part']/((it.get('file') or Path(it['part']).name)+'.step')
    if not src.exists():omitted.append(it['label']);continue
    s=Part.read(str(src))
    for op in reversed(it.get('ops',[])):
        if 'translate' in op:s.translate(A.Vector(*op['translate']))
        elif 'rotate' in op:
            x,y,z=op['rotate'];s=s.transformGeometry(A.Rotation(z,y,x).toMatrix())
        elif 'mirror' in op:
            m=A.Matrix();m.A11=-1;s=s.transformGeometry(m)
    assert s.isValid(),it['label']
    o=doc.addObject('PartDesign::Feature',it['label']);o.Label=it['label'];o.Shape=s
    shapes.append((it,s,o))
collisions=[]
for n,(i,s,o) in enumerate(shapes):
    for j,t,p in shapes[n+1:]:
        if 'exterior' not in (i['group'],j['group']):continue
        if not s.BoundBox.intersect(t.BoundBox):continue
        volume=s.common(t).Volume
        if volume>0.1:collisions.append(dict(a=i['label'],b=j['label'],volume_mm3=volume))
Part.export([o for i,s,o in shapes],str(OUT/(NAME+'_structure.step')))
report=dict(checked_components=len(shapes),collisions=collisions,omitted_references=omitted,hardware_checked=False)
if NAME=='parent_oneplate':
    frame=next(s for i,s,o in shapes if (i.get('file') or Path(i['part']).name)=='parent_oneplate_frame')
    bores=[]
    for x in [-60,-20]:
        for y in [-20,20]:
            probe=Part.makeCylinder(1.75,26,A.Vector(x,y,-25))
            obstruction=frame.common(probe).Volume
            assert obstruction<0.01,(x,y,obstruction)
            bores.append(dict(x=x,y=y,diameter_mm=3.5,through=True,obstruction_mm3=obstruction))
    report['camera_through_bores']=bores
(OUT/'solid_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
