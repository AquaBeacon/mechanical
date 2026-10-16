"""FreeCAD: export the remaining bolted parts, rejecting invalid/mismatched STEP.

The bay may use zero-tolerance coplanar retriangulation in _work/intermediate.
The authoritative source STL is always the dimensional and volume reference.
Input/output paths are supplied through the established BODY_ROOT variable.
"""
import json
import os
import hashlib
from pathlib import Path
import Mesh
import Part

root = Path(os.environ['BODY_ROOT'])
for relative in ['parts/child/interior/printed/child_vtray_deck/child_vtray_deck_t200',
                 'parts/child/interior/printed/child_flange_brace/child_flange_brace',
                 'parts/child/interior/printed/child_vtray_batt_box/child_vtray_batt_box',
                 'parts/child/interior/printed/child_vtray_batt_floor/child_vtray_batt_floor',
                 'parts/common/interior/cots/screw/screw_m3x16']:
    p = root / relative
    reference = Mesh.Mesh(str(p.with_suffix('.stl')))
    compact = p.parent / '_work/intermediate/bolted-step-mesh.stl'
    if compact.exists():
        audit = json.loads((p.parent / '_work/analysis/bolted_mount/step_compact.json').read_text(encoding='utf-8'))
        assert audit['source_sha256'] == hashlib.sha256(p.with_suffix('.stl').read_bytes()).hexdigest(), 'Compact mesh is stale'
        assert audit['output_sha256'] == hashlib.sha256(compact.read_bytes()).hexdigest(), 'Compact mesh changed'
    mesh = Mesh.Mesh(str(compact if compact.exists() else p.with_suffix('.stl')))
    # Very short chamfer edges must not be merged by a 0.001 mm sewing tolerance.
    shape = Part.Shape()
    shape.makeShapeFromMesh(mesh.Topology, 1e-7)
    assert len(shape.Shells) == 1, relative
    solid = Part.makeSolid(shape.Shells[0])
    b, r = solid.BoundBox, reference.BoundBox
    bounds_error = max(abs(getattr(b, v) - getattr(r, v)) for v in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])
    report = dict(valid=solid.isValid(), solids=len(solid.Solids), volume_mm3=solid.Volume,
                  stl_volume_mm3=reference.Volume,
                  relative_volume_difference=abs(solid.Volume-reference.Volume)/abs(reference.Volume),
                  bbox_difference_mm=bounds_error, representation='faceted STEP from verified SCAD mesh')
    print(p.name, json.dumps(report), flush=True)
    assert report['valid'] and report['solids'] == 1
    assert bounds_error < .001 and report['relative_volume_difference'] < .00001
    solid.exportStep(str(p.with_suffix('.step')))
    p.with_suffix('.check.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
