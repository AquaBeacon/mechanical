"""Validate the provisional ballast C exports with FreeCAD CLI."""
import json
import math
from pathlib import Path
import Mesh
import Part

root = Path(__file__).resolve().parents[1]
folder = root / 'parts/common/exterior/cots/ballast_c'
shape = Part.Shape()
shape.read(str(folder / 'ballast_c.step'))
mesh = Mesh.Mesh(str(folder / 'ballast_c.stl'))
assert shape.isValid() and len(shape.Solids) == 1
assert mesh.isSolid()
for box in (shape.BoundBox, mesh.BoundBox):
    actual = (box.XMin,box.YMin,box.ZMin,box.XMax,box.YMax,box.ZMax)
    expected = (-24.25,-24.25,0,24.25,24.25,76)
    assert max(abs(a-b) for a,b in zip(actual,expected)) < 0.001, actual
volume = math.pi*((48.5/2)**2*(53+8)+(36/2)**2*15)
assert abs(shape.Volume-volume)/volume < 1e-6
assert abs(mesh.Volume-volume)/volume < 0.001
surfaces = sorted((f.BoundBox.ZMin,f.BoundBox.ZMax,f.Surface.Radius)
                  for f in shape.Faces if isinstance(f.Surface,Part.Cylinder))
assert len(surfaces) == 3
for actual,expected in zip(surfaces, [(0,53,24.25),(53,68,18),(68,76,24.25)]):
    assert max(abs(a-b) for a,b in zip(actual,expected)) < 0.001, actual
inventory = json.loads((folder.parent / 'ballast_inventory.json').read_text(encoding='utf-8'))
assert [i['mass_g'] for i in inventory['items']] == [60,60,1000]
for item in inventory['items']:
    for key in ('file','mesh_file'):
        assert (root/item['part']/item[key]).is_file(), item
result = dict(step_valid=True, stl_closed=True, size_mm=[48.5,48.5,76],
              step_volume_mm3=shape.Volume, stl_volume_mm3=mesh.Volume,
              cylinder_z_ranges_and_radii_mm=surfaces, mass_g=1000,
              status='PASS for provisional geometry; head and transitions not measured')
(folder/'_work/logs/geometry_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('[ballast C] PASS: extents, volume, single closed solid, stepped cylinders, A/B/C mass/model map')
