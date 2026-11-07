"""FreeCADCmd readback: current bracket STEP/STL solids, bounds and volume."""
from pathlib import Path
import hashlib
import json
import Mesh
import Part

root=Path(__file__).resolve().parents[1]
folder=root/'parts/common/exterior/printed/td04a_bracket_mount'
rows=[]
for variant in ['parent_down','child_side_up']:
    stem='td04a_bracket_mount_'+variant
    stl=folder/(stem+'.stl'); step=folder/(stem+'.step')
    mesh=Mesh.Mesh(str(stl)); shape=Part.read(str(step))
    bounds=lambda b:[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
    delta=max(abs(a-b) for a,b in zip(bounds(mesh.BoundBox),bounds(shape.BoundBox)))
    volume_delta=abs(abs(mesh.Volume)-abs(shape.Volume))
    rows.append(dict(variant=variant,valid=shape.isValid(),solids=len(shape.Solids),
                     max_bbox_delta_mm=delta,volume_delta_mm3=volume_delta,
                     volume_mm3=shape.Volume,stl_sha256=hashlib.sha256(stl.read_bytes()).hexdigest(),
                     step_sha256=hashlib.sha256(step.read_bytes()).hexdigest(),
                     passed=shape.isValid() and len(shape.Solids)==1 and delta<.01 and volume_delta<.1))
result=dict(revision='cable_clearance_r6',passed=all(r['passed'] for r in rows),parts=rows)
(root/'assemblies/td04a_fixture/_work/analysis/step_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,indent=2))
if not result['passed']: raise RuntimeError('STEP readback mismatch')
