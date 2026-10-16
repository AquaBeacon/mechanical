"""Run with FreeCADCmd from the repository root."""
import json
from pathlib import Path
import FreeCAD as A
import Part

root = Path.cwd()
p = root / 'parts/child/exterior/printed/child_simple_light_mount'
base = Part.read(str(p/'child_simple_light_mount_base.step'))
cap = Part.read(str(p/'child_simple_light_mount_cap.step'))
rear = Part.read(str(root/'parts/child/exterior/printed/child_simple_rear/child_simple_rear.step'))
rows = []
def record(name, ok, value):
    rows.append(dict(check=name, passed=bool(ok), value=value))
for name,shape in [('base',base),('cap',cap)]:
    record(name+'_solid',shape.isValid() and len(shape.Solids)==1,len(shape.Solids))
record('base_cap_overlap',base.common(cap).Volume < 1e-5,base.common(cap).Volume)
record('split_gap',abs(base.distToShape(cap)[0]-1.5)<0.001,base.distToShape(cap)[0])
for name,shape in [('base',base),('cap',cap)]:
    inst=shape.copy();inst.rotate(A.Vector(),A.Vector(0,0,1),180);inst.translate(A.Vector(0,-82,100))
    overlap=inst.common(rear).Volume
    record(name+'_rear_overlap',overlap<1e-5,overlap)
    if name=='base': record('rear_contact',inst.distToShape(rear)[0]<0.001,inst.distToShape(rear)[0])
for x in [-20,20]:
    for z in [-20,20]:
        shaft=Part.makeCylinder(1.5,6,A.Vector(x,0,z),A.Vector(0,1,0))
        record('mount_M3_shaft_%s_%s'%(x,z),base.common(shaft).Volume<1e-5,base.common(shaft).Volume)
        head=Part.makeCylinder(3,3,A.Vector(x,6,z),A.Vector(0,1,0))
        record('mount_head_%s_%s'%(x,z),base.common(head).Volume<1e-5,base.common(head).Volume)
        # 3 mm diameter L-key arm inserted from the nearest side.
        arm=Part.makeCylinder(1.5,20,A.Vector(x,10,z),A.Vector(1 if x>0 else -1,0,0))
        record('L_key_%s_%s'%(x,z),base.common(arm).Volume<1e-5,base.common(arm).Volume)
        tool=Part.makeCylinder(5,12,A.Vector(-x,-74,100+z),A.Vector(0,1,0))
        record('rear_nut_tool_%s_%s'%(x,z),rear.common(tool).Volume<1e-5,rear.common(tool).Volume)
out=p/'verification/cad_checks.json';out.write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('CAD checks:',len(rows),'passed:',sum(r['passed'] for r in rows))
assert all(r['passed'] for r in rows), rows
