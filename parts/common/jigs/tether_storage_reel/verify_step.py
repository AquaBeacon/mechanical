"""Run with FreeCAD's freecadcmd; checks delivered solids and assembled fit."""
import json
from pathlib import Path
import FreeCAD as A
import Part

p = Path(__file__).resolve().parent
shapes = []
report = {}
for name in ('base', 'lid'):
    s = Part.Shape()
    s.read(str(p / ('tether_storage_reel_' + name + '.step')))
    report[name] = {'valid': s.isValid(), 'solids': len(s.Solids), 'volume_mm3': s.Volume}
    assert s.isValid() and len(s.Solids) == 1
    shapes.append(s)
shapes[1].rotate(A.Vector(0, 0, 0), A.Vector(1, 0, 0), 180)
shapes[1].translate(A.Vector(0, 0, 148))
report['assembled_interference_mm3'] = shapes[0].common(shapes[1]).Volume
assert report['assembled_interference_mm3'] < 0.01
(p / 'step_check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
