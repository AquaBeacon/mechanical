"""Check load-path geometry, purchased nuts and actual insertion clearances.

Run after rendering, before exporting/syncing. Reports stay with the assembly.
This is a geometric check, not a material strength certification.
"""
import json
from pathlib import Path
import sys
import warnings
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scad/lib'))
from check_asm_contacts import load

warnings.filterwarnings('ignore', category=RuntimeWarning, module='trimesh')
items = json.loads((ROOT / 'assemblies/child_interior/placement.json').read_text(encoding='utf-8'))['items']
meshes = {i['label']: load(ROOT, i) for i in items}
report = dict(meshes=[], checks=[], errors=[])
changed = ['vtray_deck', 'vtray_batt_box', 'vtray_batt_floor', 'flange_brace']


def overlap(name, a, b):
    if np.any(a.bounds[0] >= b.bounds[1] - .001) or np.any(b.bounds[0] >= a.bounds[1] - .001):
        return
    c = trimesh.boolean.intersection([a, b], engine='manifold', check_volume=False)
    volume = float(abs(c.volume)) if c is not None and len(c.faces) else 0.
    entry = dict(pair=name, overlap_mm3=round(volume, 6))
    report['checks'].append(entry)
    if volume > .01:
        report['errors'].append(entry)


for name in changed:
    m = meshes[name]
    valid = m.is_volume and len(m.split()) == 1
    report['meshes'].append(dict(part=name, watertight=m.is_watertight,
                                  one_volume=bool(valid), bounds_mm=m.bounds.tolist(),
                                  volume_mm3=float(m.volume)))
    if not valid:
        report['errors'].append(dict(invalid_mesh=name))

hardware = [i for i in items if i['label'].startswith('bolted_nut_') or i['label'].startswith('batt_box_screw_') or i['label'] == 'batt_floor_screw']
for i in hardware:
    m = meshes[i['label']]
    for j in items:
        if j['label'] == i['label'] or '/cots/screw' in j['part'] or '/cots/hex_spacer' in j['part']:
            continue
        overlap(f"hardware/{i['label']}/{j['label']}", m, meshes[j['label']])

# Actual nut insertion sweeps from outside X. Rails are fitted afterwards.
for i in hardware:
    if not i['label'].startswith('bolted_nut_'):
        continue
    x = i['ops'][0]['translate'][0]
    for distance in np.linspace(0, 6, 13):
        nut = meshes[i['label']].copy()
        nut.apply_translation([np.sign(x) * distance, 0, 0])
        for name in changed:
            overlap(f"nut_insert/{i['label']}/{distance:.1f}/{name}", nut, meshes[name])

# Nuts remain in the bay while the service screw is removed.
for dz, dy in [(float(z), 0.) for z in np.linspace(0, -2, 9)] + [(-2., float(y)) for y in np.linspace(-.5, -45, 20)]:
    floor = meshes['vtray_batt_floor'].copy()
    floor.apply_translation([0, dy, dz])
    for i in hardware:
        if i['label'] == 'batt_floor_screw':
            continue
        overlap(f"floor/hardware/{dz:.2f}/{dy:.2f}/{i['label']}", floor, meshes[i['label']])

# Root centre is the documented 200 g / 180 mm / 5g comparison assumption.
# Confirm geometric dimensions independently of the source variables.
report['reference_load'] = dict(mass_kg=.2, lever_arm_m=.18, acceleration_g=5,
                                bending_moment_Nm=.2 * 9.81 * 5 * .18,
                                status='comparison assumption, not certified capacity')
report['fasteners'] = dict(bay_screw='M3x12', bay_quantity=4, floor_screw='M3x10 flat',
                           nut_af_mm=5.5, nut_t_mm=2.4, nuts=5,
                           flange_front_screw='M3x16', flange_front_engagement_mm=4)
target = ROOT / 'assemblies/child_interior/_work/logs/bolted_geometry_check.json'
target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('errors', report['errors'], 'intersection checks', len(report['checks']), flush=True)
sys.exit(bool(report['errors']))
