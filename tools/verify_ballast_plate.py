"""Read ballast STEP/STL exports using FreeCAD CLI and check reference geometry."""
import json
import math
from pathlib import Path

import Mesh
import Part

root = Path(__file__).resolve().parents[1]
folder = root / 'parts/common/exterior/cots/ballast_plate'
results = []
for suffix, size, hole_x in [('a', (142, 19, 4), []),
                             ('b', (163.5, 16, 3), [-61.75, -24.25, 24.25, 61.75])]:
    stem = folder / ('ballast_plate_' + suffix)
    shape = Part.Shape()
    shape.read(str(stem.with_suffix('.step')))
    mesh = Mesh.Mesh(str(stem.with_suffix('.stl')))
    expected_volume = math.prod(size) - len(hole_x)*math.pi*(5.5/2)**2*size[2]
    assert shape.isValid() and len(shape.Solids) == 1, suffix + ': invalid STEP'
    assert mesh.isSolid(), suffix + ': STL is not closed'
    for box in (shape.BoundBox, mesh.BoundBox):
        actual = (box.XMin, box.YMin, box.ZMin, box.XMax, box.YMax, box.ZMax)
        expected = (-size[0]/2, -size[1]/2, 0, size[0]/2, size[1]/2, size[2])
        assert max(abs(a-b) for a,b in zip(actual,expected)) < 0.001, (suffix, actual)
    assert abs(shape.Volume-expected_volume) < 0.01, (suffix, shape.Volume, expected_volume)
    assert abs(mesh.Volume-expected_volume)/expected_volume < 0.001, suffix + ': mesh volume'
    cylinders = [f for f in shape.Faces if isinstance(f.Surface, Part.Cylinder)]
    assert len(cylinders) == len(hole_x), suffix + ': cylinder count'
    actual_centres = sorted((f.Surface.Center.x, f.Surface.Center.y) for f in cylinders)
    for (x,y), expected_x in zip(actual_centres, hole_x):
        assert abs(x-expected_x) < 0.001 and abs(y) < 0.001, (suffix, x, y)
    for face in cylinders:
        assert abs(face.Surface.Radius-2.75) < 0.001
        assert abs(abs(face.Surface.Axis.z)-1) < 0.001
        assert abs(face.BoundBox.ZMin) < 0.001
        assert abs(face.BoundBox.ZMax-size[2]) < 0.001
    results.append(dict(variant=suffix, size_mm=size, step_volume_mm3=shape.Volume,
                        stl_volume_mm3=mesh.Volume, stl_closed=True, step_valid=True,
                        hole_centres_xy_mm=actual_centres, hole_d_mm=5.5 if hole_x else None,
                        hole_d_status='provisional' if hole_x else 'not applicable'))
out = folder / '_work/logs/geometry_validation.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(results, indent=2), encoding='utf-8')
print('[ballast] PASS: A/B STEP/STL extents, volume, closed solids and B through holes')
