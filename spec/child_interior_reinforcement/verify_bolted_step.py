"""Read back all changed STEP solids; compare actual bounds and STL volume."""
import json
import os
from pathlib import Path
import Mesh
import Part

root = Path(os.environ['BODY_ROOT'])
reports = []
for part in ['child_vtray_deck/child_vtray_deck_t200', 'child_flange_brace/child_flange_brace',
             'child_vtray_batt_box/child_vtray_batt_box', 'child_vtray_batt_floor/child_vtray_batt_floor']:
    p = root / 'parts/child/interior/printed' / part
    shape = Part.read(str(p.with_suffix('.step')))
    mesh = Mesh.Mesh(str(p.with_suffix('.stl')))
    delta = max(abs(getattr(shape.BoundBox, key)-getattr(mesh.BoundBox, key))
                for key in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])
    entry = dict(part=part, valid=shape.isValid(), solids=len(shape.Solids),
                 bbox_delta_mm=delta, volume_delta_fraction=abs(shape.Volume-mesh.Volume)/abs(mesh.Volume))
    reports.append(entry)
    print(json.dumps(entry), flush=True)
    assert entry['valid'] and entry['solids'] == 1 and delta < .001 and entry['volume_delta_fraction'] < .00001
(root / 'assemblies/child_interior/_work/logs/bolted_step_check.json').write_text(json.dumps(reports, indent=2)+'\n', encoding='utf-8')
