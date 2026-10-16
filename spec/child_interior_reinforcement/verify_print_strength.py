"""Geometric regression for paired clamps, flange elbow and penetrator clearance.

No material strength or service-life claim is made by this check.
"""
import json
import sys
from pathlib import Path
import numpy as np
import trimesh
from topopt.geom import shell_report

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scad/lib'))
from check_asm_contacts import load
from verify_child_interior import matrix

items = json.loads((ROOT / 'assemblies/child_interior/placement.json').read_text(encoding='utf-8'))['items']
meshes = {i['label']: load(ROOT, i) for i in items}
for mesh in meshes.values():
    mesh.fix_normals()
report = dict(errors=[], meshes=[], penetrators=[], cable_checks=[], comparisons=[])
printed = [i for i in items if '/printed/' in i['part']]
penetrators = [i for i in items if i['label'].startswith('penetrator_')]
for it in printed:
    m = meshes[it['label']]
    for p in penetrators:
        # An axis separation is an exact conservative lower bound, not a
        # sampled estimate of the closest points.
        other = meshes[p['label']]
        gaps = np.maximum(m.bounds[0]-other.bounds[1], other.bounds[0]-m.bounds[1])
        gap = float(max(gaps))
        entry = dict(part=it['label'], penetrator=p['label'], axis_gap_mm=gap)
        report['penetrators'].append(entry)
        if gap <= 0:
            report['errors'].append(entry)
    if 'rx_clamp_' in it['label']:
        angle = -90 if 'base' in it['label'] else 90
        local = trimesh.load(ROOT / it['part'] / (it['file']+'.stl'), force='mesh')
        local.apply_transform(matrix([{'rotate': [angle, 0, 0]}]))
        bed = (local.face_normals[:, 2] < -.999) & (local.triangles[:, :, 2].max(axis=1) < local.bounds[0, 2]+.015)
        entry = dict(part=it['label'], watertight=bool(local.is_watertight),
                     volumes=len(local.split()), extents_mm=local.extents.tolist(),
                     bed_area_mm2=float(local.area_faces[bed].sum()),
                     native_shell=shell_report(local.triangles,intersections=False))
        report['meshes'].append(entry)
        if not local.is_volume or entry['volumes'] != 1 or entry['bed_area_mm2'] < 100 or not entry['native_shell']['closed_shell']:
            report['errors'].append(entry)
    # Check all routed harnesses, which older service checks exclude.
    for cable, other in meshes.items():
        if not cable.startswith('harness_'):
            continue
        if np.any(m.bounds[0] >= other.bounds[1]) or np.any(other.bounds[0] >= m.bounds[1]):
            continue
        intersection = trimesh.boolean.intersection([m, other], engine='manifold', check_volume=False)
        volume = abs(float(intersection.volume)) if len(intersection.faces) else 0.
        entry = dict(part=it['label'], cable=cable, intersection_mm3=volume)
        report['cable_checks'].append(entry)
        if volume > .01:
            report['errors'].append(entry)
before = ROOT / 'assemblies/child_interior/_work/analysis/print_strength_20261004/before'
for name in ('child_vtray_batt_floor', 'child_vtray_batt_box', 'child_flange_brace'):
    old = trimesh.load(before / (name+'.stl'), force='mesh')
    new = trimesh.load(ROOT / 'parts/child/interior/printed' / name / (name+'.stl'), force='mesh')
    native=shell_report(new.triangles,intersections=False)
    report['comparisons'].append(dict(part=name, before_volume_mm3=float(old.volume),
                                    after_volume_mm3=float(new.volume),
                                    watertight=bool(new.is_watertight), volumes=len(new.split()),native_shell=native))
    if not new.is_volume or len(new.split()) != 1 or not native['closed_shell']:
        report['errors'].append(dict(invalid_mesh=name))
report['min_penetrator_axis_gap_mm'] = min(x['axis_gap_mm'] for x in report['penetrators'])
dest = ROOT / 'assemblies/child_interior/_work/analysis/print_strength_20261004/geometry.json'
dest.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, indent=2))
sys.exit(bool(report['errors']))
