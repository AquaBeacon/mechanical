"""FreeCAD CLI: re-read the final STEP and STL, verify bounds and volume."""
from pathlib import Path
import json
import Mesh
import Part

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
checks=[]
for stem in ['camera_mount','camera_mount_twist']:
    shape=Part.read(str(P/(stem+'.step')))
    mesh=Mesh.Mesh(str(P/(stem+'.stl')))
    a,b=shape.BoundBox,mesh.BoundBox
    delta=max(abs(getattr(a,k)-getattr(b,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
    error=abs(shape.Volume-abs(mesh.Volume))/abs(mesh.Volume)
    checks.append(dict(stem=stem,valid=shape.isValid(),solids=len(shape.Solids),bounds_delta_mm=delta,
                       relative_volume_error=error,passed=shape.isValid() and len(shape.Solids)==1 and delta<.01 and error<.0001))
result=dict(passed=all(c['passed'] for c in checks),checks=checks)
(P/'_work/analysis/rear_clearance_20261024/step_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert result['passed'],result
print(result)
