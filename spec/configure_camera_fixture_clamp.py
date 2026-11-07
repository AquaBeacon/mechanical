"""Update only camera fixture placements for the axial clamp revision.

Run after the matching camera CAD has been rebuilt and reviewed. This script does
not build CAD, synchronize print packages, or claim fastener validation.
"""
from pathlib import Path
import json
import sys
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from prepare_child_horizontal_plate_frame import matrix

SCREW = 'parts/common/interior/cots/screw'
TAG = 'camera_twist_accessory'
OLD = ('twist_knob', 'lock_bolt', 'lock_nut', 'lock_washer', 'rubber_pads')


def row_index(p):
    rows = {r['label']: r for r in p['items']}
    if len(rows) != len(p['items']):
        raise ValueError('Duplicate item labels')
    return rows


def clamp(p, prefix, base, removal):
    p.setdefault('fastener_joints', [])
    p['items'] = [r for r in p['items'] if not r['label'].startswith(prefix + 'axial_')]
    p['fastener_joints'] = [r for r in p['fastener_joints'] if not r['label'].startswith(prefix + 'axial_')]
    for i, y in enumerate((-52, 52)):
        label = prefix + f'axial_{i}'
        common = dict(part=SCREW, group='fasteners', color='Silver', print=False,
                      owner=TAG)
        # screw source's shank extends -Z from its head seat; washer spans 0..0.5.
        for suffix, file, z, rot in [('screw', 'camera_m3x30_hex', 31.5, []),
                                     ('nut', 'screw_nut_m3', 2.4, [{'rotate':[0,0,30]}])]:
            item = dict(label=label+'_'+suffix, file=file,
                        ops=base+[{'translate':[0,y,z]}]+rot, **common)
            if suffix == 'screw': item['part']='parts/child/exterior/printed/dji_osmo_action6_mount_m3'
            if suffix != 'nut': item['removal_group'] = removal
            p['items'].append(item)
        p['items'].append(dict(label=label+'_spacer',
            part='parts/child/exterior/printed/dji_osmo_action6_mount_m3',
            file='camera_hand_spacer',ops=base+[{'translate':[0,y,8]}],
            group='accessories',color='Orange',print=True,owner=TAG,removal_group=removal))
        p['items'].append(dict(label=label+'_knob',
            part='parts/child/exterior/printed/dji_osmo_action6_mount_m3',
            file='camera_hand_knob',ops=base+[{'translate':[0,y,30.5]}],
            group='accessories',color='SeaGreen',print=True,owner=TAG,removal_group=removal))
        p['items'].append(dict(label=label+'_knob_cap',
            part='parts/child/exterior/printed/dji_osmo_action6_mount_m3',
            file='camera_hand_knob_cap',ops=base+[{'translate':[0,y,33.5]}],
            group='accessories',color='SeaGreen',print=True,owner=TAG,removal_group=removal))
        seat = matrix(base+[{'translate':[0,y,31.5]}])
        nut = matrix(base+[{'translate':[0,y,2.4]}])
        angles = np.degrees(trimesh.transformations.euler_from_matrix(seat)).tolist()
        p['fastener_joints'].append(dict(label=label, seat_mm=seat[:3,3].tolist(),
            axis_rotation_deg=angles, length_mm=30, nut_start_mm=nut[:3,3].tolist(),
            nut_rotation_deg=angles, nominal_diameter_mm=3, exposed_nut=False, owner=TAG))


def update_parent(p):
    rows = row_index(p)
    base = rows['camera_qr_female']['ops']
    p['items'] = [r for r in p['items'] if r['label'] not in ({'camera_qr_'+s for s in OLD} | {'camera_qr_knob'})]
    clamp(p, 'camera_qr_', base, 'camera')
    p['camera_twist_mount'].update(revision=3, interface='camera axial clamp',
        removal='Unscrew each knob until free, raise to about 3.8 mm, remove the U spacer, slide the screw outward, then rotate.',
        clamp_screws='M3x30 hex, two; printed 1 mm compression floor and snap cap; M3 nuts', validation='pending')


def update_child(p):
    rows = row_index(p)
    receiver = rows['side_camera_frame_receiver']['ops']
    assert receiver == [{'translate':[-122.0,60,130.0]},{'rotate':[90,0,-90]}]
    for r in p['items']:
        if r.get('removal_group') == 'child_camera':
            ops = r['ops']
            if len(ops) >= 3 and ops[2] in ({'translate':[-35,0,0]}, {'translate':[-45,0,0]}):
                ops[2] = {'translate':[-53,0,0]}
            elif len(ops) >= 3 and ops[2] == {'translate':[-53,0,0]}:
                pass
            elif r['label'] not in {'side_camera_rubber_pads'} and not r['label'].startswith('side_camera_axial_'):
                raise ValueError('Unexpected moving camera pose: '+r['label'])
    p['items'] = [r for r in p['items'] if r['label'] not in {'side_camera_'+s for s in OLD}]
    for z in (100,176):
        stem=f'guard_join_-1_98_{z}'
        rows = row_index(p)
        screw, washer = rows[stem+'_screw'], rows[stem+'_washer']
        x = screw['ops'][0]['translate'][0]
        if x == -122.5:
            assert washer['ops'][0]['translate'][0] == x and screw['file'] == 'screw_m3x25'
            screw['ops'][0]['translate'][0] = washer['ops'][0]['translate'][0] = -126.5
            screw['file'] = 'screw_m3x30'
        else:
            assert x == -126.5 and washer['ops'][0]['translate'][0] == x and screw['file'] == 'screw_m3x30'
        joint=next(j for j in p['fastener_joints'] if j['label']==stem)
        joint['seat_mm'][0]=-126.5
        joint['length_mm']=30
    # Original placement left 0.1 mm assembly slack. Seat both existing
    # frame nuts against the pocket reaction face without changing frame geometry.
    rows=row_index(p)
    for i in range(2):
        nut=rows[f'side_camera_frame_{i}_nut']
        z=nut['ops'][2]['translate'][2]
        if abs(z-(-11.6)) < 1e-8: nut['ops'][2]['translate'][2]=-11.5
        else: assert abs(z-(-11.5)) < 1e-8
        joint=next(j for j in p['fastener_joints'] if j['label']==f'side_camera_frame_{i}')
        x=joint['nut_start_mm'][0]
        if abs(x-(-110.4)) < 1e-8: joint['nut_start_mm'][0]=-110.5
        else: assert abs(x-(-110.5)) < 1e-8
    base=receiver+[{'translate':[-53,0,0]},{'rotate':[0,0,90]}]
    clamp(p, 'side_camera_', base, 'child_camera')
    meta=p['camera_twist_mount']
    meta.update(revision=3, dock_offset_uvn_mm=[-53,0,0],
        dock_origin_mm=(matrix(base)@np.array([0,0,0,1]))[:3].tolist(),
        interface='camera axial clamp',
        removal='Unscrew each knob until free, raise to about 3.8 mm, remove the U spacer, slide the screw outward, then rotate.',
        clamp_screws='M3x30 hex, two; printed 1 mm compression floor and snap cap; M3 nuts', validation='pending')
    stock=set(p['print_progress']['source_mesh_sha256'])
    remaining=[r for r in p['items'] if r.get('print',False) and r['part']+'/'+r['file']+'.stl' not in stock]
    p['print_progress']['remaining_instances']=len(remaining)
    p['print_progress']['base_remaining_instances']=sum(r.get('owner')!='side_twist_accessory' for r in remaining)


def main():
    paths=[ROOT/'assemblies'/n/'placement.json' for n in ('parent_exterior','child_horizontal_plate_frame')]
    data=[json.loads(p.read_text(encoding='utf-8')) for p in paths]
    update_parent(data[0]); update_child(data[1])
    for p, value in zip(paths,data):
        p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Placements updated; rebuild views, synchronize packages and verify fasteners separately.')

if __name__ == '__main__':
    main()
