"""FreeCAD CLI: read reference analytic cylinders, never modify vendor CAD."""
import json
import os
from pathlib import Path
import Part

root = Path(os.environ['ASM_ROOT'])
part = root / 'parts/child/exterior/printed/child_wte4_suspension_clamp'
shape = Part.read(str(part / 'ref/WTE4_CLAMP_BR-102710-004/BR-102678-004_RevC.STEP'))
rows = []
for face in shape.Faces:
    surface = face.Surface
    if isinstance(surface, Part.Cylinder):
        rows.append(dict(radius_mm=surface.Radius, centre_mm=list(surface.Center),
                         axis=list(surface.Axis), area_mm2=face.Area))
rows.sort(key=lambda row: row['area_mm2'], reverse=True)
out = dict(reference='BR-102678-004_RevC.STEP', cylinders=rows,
           note='Analytic surface radii; groove radii and bore radii must be distinguished using face area/position.')
(part / '_work/analysis/topology_petg/reference_cylinders.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
print(json.dumps(rows[:12], indent=2))
