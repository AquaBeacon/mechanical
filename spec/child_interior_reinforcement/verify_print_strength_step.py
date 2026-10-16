"""FreeCAD CLI: read back changed printable STEP solids against source STL."""
import json
import os
from pathlib import Path
import Mesh
import Part

root = Path(os.environ['BODY_ROOT'])
report = []
names = ['child_vtray_deck/child_vtray_deck_t200',
         'child_vtray_batt_floor/child_vtray_batt_floor',
         'child_vtray_batt_box/child_vtray_batt_box',
         'child_flange_brace/child_flange_brace',
         'child_rx_edge_clamp/child_rx_edge_clamp_base_pair',
         'child_rx_edge_clamp/child_rx_edge_clamp_cap_pair']
for name in names:
    stem = root / 'parts/child/interior/printed' / name
    shape = Part.read(str(stem.with_suffix('.step')))
    mesh = Mesh.Mesh(str(stem.with_suffix('.stl')))
    delta = max(abs(getattr(shape.BoundBox, a)-getattr(mesh.BoundBox, a))
                for a in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
    error = abs(shape.Volume-abs(mesh.Volume))/abs(mesh.Volume)
    entry = dict(part=name, valid=shape.isValid(), solids=len(shape.Solids),
                 bounds_error_mm=delta, relative_volume_error=error)
    report.append(entry)
for variant in ('xh6_rx','xh4_temp','bat','led'):
    stem=root/'parts/common/cabling/child_harness'/('child_harness_'+variant)
    shape=Part.read(str(stem.with_suffix('.step')))
    mesh=Mesh.Mesh(str(stem.with_suffix('.stl')))
    delta=max(abs(getattr(shape.BoundBox,a)-getattr(mesh.BoundBox,a))
              for a in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
    report.append(dict(part='child_harness_'+variant,valid=shape.isValid(),
                       solids=len(shape.Solids),expected_solids=2 if variant=='bat' else 1,
                       bounds_error_mm=delta,
                       relative_volume_error=abs(shape.Volume-abs(mesh.Volume))/abs(mesh.Volume)))
dest = root / 'assemblies/child_interior/_work/analysis/print_strength_20261004/step.json'
dest.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, indent=2), flush=True)
assert all(x['valid'] and x['solids']==x.get('expected_solids',1) and x['bounds_error_mm']<.01 and
           x['relative_volume_error']<.0025 for x in report)
