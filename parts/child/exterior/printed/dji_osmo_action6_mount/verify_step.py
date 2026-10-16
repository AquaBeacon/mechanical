import json
from pathlib import Path
import Part

p = Path(__file__).resolve().parent
s = Part.Shape()
s.read(str(p / 'dji_osmo_action6_mount.step'))
r = dict(valid=s.isValid(), solids=len(s.Solids), volume_mm3=s.Volume,
         extents_mm=[s.BoundBox.XLength, s.BoundBox.YLength, s.BoundBox.ZLength])
(p / 'step_check.json').write_text(json.dumps(r, indent=2))
assert r['valid'] and r['solids'] == 1
print(r)
