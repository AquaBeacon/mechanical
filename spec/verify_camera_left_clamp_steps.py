"""FreeCAD: final solid validity and STEP/STL dimensional agreement."""
from pathlib import Path
import json,Mesh,Part
P=Path(__file__).resolve().parents[1]/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
checks=[]
for stem in ['camera_mount','camera_mount_twist','camera_front_clamp','camera_case_41mm']:
    s=Part.read(str(P/(stem+'.step')));m=Mesh.Mesh(str(P/(stem+'.stl')))
    delta=max(abs(getattr(s.BoundBox,k)-getattr(m.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
    error=abs(s.Volume-abs(m.Volume))/abs(m.Volume)
    checks.append(dict(stem=stem,valid=s.isValid(),solids=len(s.Solids),bounds_delta_mm=delta,relative_volume_error=error,
                       passed=s.isValid() and len(s.Solids)==1 and delta<.02 and error<.001))
result=dict(passed=all(c['passed'] for c in checks),checks=checks)
(P/'_work/analysis/clamp_clearance_20261026/step_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert result['passed'],result
print(result)
