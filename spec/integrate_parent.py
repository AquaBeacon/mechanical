"""Rebuild the review assembly from current P1 interior and bottom-sensor exterior.

python spec/integrate_parent.py
python spec/integrate_parent.py --check
The box is the shared datum. Purchased reference geometry is never fabricated here.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import subprocess
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scad/lib'))
from check_asm_contacts import load, matrix

OUT = ROOT / 'assemblies/parent_integrated'


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    sources = [ROOT / 'assemblies' / n / 'placement.json'
               for n in ['parent_bottom_sensors', 'parent_interior_p1']]
    exterior, interior = [json.loads(p.read_text(encoding='utf-8')) for p in sources]
    ext_box = next(i for i in exterior['items'] if i['label'] == 'box_bcas212310g')
    int_box = next(i for i in interior['items'] if i['label'] == 'box_bcas212310g')
    transform = matrix(ext_box['ops']) @ np.linalg.inv(matrix(int_box['ops']))
    # Current box frames have the same orientation. Fail explicitly if that changes.
    assert np.allclose(transform[:3, :3], np.eye(3)), 'Box rotation changed; update frame conversion'
    shift = transform[:3, 3].tolist()
    imported = {i['label'] for i in interior['items'] if i['label'] != 'box_bcas212310g'}
    items = [copy.deepcopy(i) for i in exterior['items']
             if i['group'] != 'interior' and i['label'] not in imported]
    # Derive the PWR lift from generated meshes so it cannot silently diverge from SCAD.
    plate_dir = ROOT / 'parts/parent/interior/printed'
    import trimesh
    base = trimesh.load(plate_dir / 'parent_plate/parent_plate_p1.stl', force='mesh')
    raised = trimesh.load(plate_dir / 'parent_plate_integrated/parent_plate_integrated.stl', force='mesh')
    lift = float(raised.bounds[1, 2] - base.bounds[1, 2])
    assert 0 < lift < 10, 'Unexpected PWR lift'
    for src in interior['items']:
        if src['label'] == 'box_bcas212310g':
            continue
        it = copy.deepcopy(src)
        it['ops'] = [{'translate': shift}] + it.get('ops', [])
        if it['label'] == 'plate':
            it['part'] = 'parts/parent/interior/printed/parent_plate_integrated'
            it.pop('file', None)
        if it['label'] == 'p_pwr':
            it['ops'] = [{'translate': [0, 0, lift]}] + it['ops']
        items.append(it)
    cable_part = 'parts/common/cabling/parent_td04a_cable'
    if (ROOT / cable_part / 'parent_td04a_cable.step').exists():
        items.append(dict(label='td04a_cable_d5', part=cable_part, group='cabling',
                          color='Red', ops=[], note='User cable OD5; R30 provisional; exterior route only. Not printable.'))
    assert len({i['label'] for i in items}) == len(items), 'Duplicate labels'
    for it in items:
        stem = it.get('file', Path(it['part']).name)
        for suffix in ['.stl', '.step']:
            assert (ROOT / it['part'] / (stem + suffix)).is_file(), (it['label'], suffix)
    asm = dict(name='parent_integrated', note='P1 + latest bottom-sensor exterior; prototype pending measurements. SPRESENSE placeholder contact unresolved.',
               coordinate_system=exterior.get('coordinate_system', 'Box bottom centre, Z up'),
               groups={g: True for g in sorted({i['group'] for i in items})}, items=items)
    asm['groups']['envelope'] = False
    write('placement.json', asm)
    write('sources.json', dict(sources=[dict(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources],
                              box_frame_translation=shift, pwr_lift_mm=lift,
                              status='PROTOTYPE_MEASUREMENT_PENDING'))
    # A close-up keeps the full coordinate system, including nearby external fasteners.
    meshes = {i['label']: load(ROOT, i) for i in items}
    close = copy.deepcopy(asm)
    close['name'] = 'parent_integrated_closeup'
    close['items'] = [i for i in close['items'] if meshes[i['label']].bounds[1, 2] >= -12
                      and i['group'] not in ['floats', 'ropes', 'cabling']]
    for it in close['items']:
        if it['label'] == 'box_bcas212310g':
            it['alpha'] = 0.16
    write('closeup.json', close)
    for source, target in [('placement.json', 'parent_integrated_view.scad'), ('closeup.json', 'closeup_view.scad')]:
        subprocess.run([sys.executable, str(ROOT / 'scad/lib/asm_gen.py'), str(OUT / source), str(OUT / target)], check=True)
    ints = [i for i in items if i['group'] == 'interior']
    # Check interior against ALL exterior meshes whose AABBs overlap. No nearest-distance
    # gate: a wholly enclosed part would otherwise escape penetration testing.
    np.random.seed(20260910)
    cross = []
    for a in ints:
        ma = meshes[a['label']]
        for b in items:
            if b['group'] in ['interior', 'envelope', 'floats', 'ropes'] or b['label'] == 'box_bcas212310g':
                continue
            mb = meshes[b['label']]
            if np.any(ma.bounds[0] > mb.bounds[1]) or np.any(mb.bounds[0] > ma.bounds[1]):
                continue
            hits, skipped = [], []
            for src, dst, label in [(ma, mb, b['label']), (mb, ma, a['label'])]:
                if not dst.is_watertight:
                    skipped.append(label)
                    continue
                pts, fi = trimesh.sample.sample_surface(src, 3000)
                pts -= src.face_normals[fi] * 0.1
                hits.append(int(dst.contains(pts).sum()))
            cross.append(dict(a=a['label'], b=b['label'], inside_samples=hits, nonwatertight_skipped=skipped))
    write('cross_contacts.json', dict(method='AABB candidate pairs, 3000 inset surface samples per direction, depth 0.1 mm; not a proof of no collision', pairs=cross))
    print('Integrated', len(items), 'parts; PWR lift', lift, 'mm; cross candidates', len(cross), flush=True)
    if args.check:
        command = [sys.executable, str(ROOT / 'scad/lib/check_asm_contacts.py'), str(OUT / 'placement.json'), '--root', str(ROOT), '--groups', 'interior,vessel', '--ignore-threads', '--json', str(OUT / 'interior_contacts.json')]
        with (OUT / 'interior_contacts.log').open('w', encoding='utf-8') as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        print('Interior checker exit', result.returncode, '(see log; unresolved contacts are not waived)')
        cross_failure = any(any(n >= 3 for n in p['inside_samples']) for p in cross)
        return result.returncode or int(cross_failure)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
