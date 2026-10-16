"""One-time documented revision of the exterior concept sources and history."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assemblies/child_exterior_concept'
PART = ROOT / 'parts/child/exterior/printed/child_exterior_open_frame'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    if any(i['label'] == 'transducer_inside_c' for i in read(OUT/'placement.json')['items']):
        raise SystemExit('Revision already applied; rebuild using build_child_exterior_concept.py.')
    # Snapshot once, before overwriting. Images stay under this assembly's _work.
    history = OUT/'_work/images/history/four_face_equipment_pair'
    history.mkdir(parents=True, exist_ok=True)
    for source in (OUT/'_work/images').glob('child_exterior_*'):
        if source.is_file() and not (history/source.name).exists():
            shutil.copy2(source, history/source.name)
    for name, source in [('placement_before_single_equipment_and_wiring.json', OUT/'placement.json'),
                         ('child_exterior_before_single_equipment_and_wiring.blend', OUT/'child_exterior_concept.blend')]:
        target = OUT/'_work/intermediate'/name
        if not target.exists():
            shutil.copy2(source, target)

    p = read(OUT/'placement.json')
    removed = {'action_camera_rear', 'camera_saddle_rear', 'dive_light_front',
               'B_bottom_front', 'B_bottom_rear', 'B_upper_rear'}
    p['items'] = [i for i in p['items'] if i['label'] not in removed]
    for i in p['items']:
        if i['label'] == 'ballast_bottom_carrier':
            i.update(label='frame_b_bottom', group='Frame B', material='frame_b', file='frame_b_bottom')
        if i['label'] == 'clamp_cradle_integrated':
            i['note'] = 'Three clamp levels joined; lateral lugs bolt to both Frame A faces.'
    def item(label, variant, group, material, loc, explode):
        return dict(label=label, part=PART.relative_to(ROOT).as_posix(), file=variant,
                    group=group, material=material, geometry='concept', print=False,
                    ops=[{'translate':loc}], explode_mm=explode)
    p['items'] += [
        dict(label='transducer_inside_c', part='parts/common/exterior/cots/td04a_transducer',
             file='td04a_transducer', group='Transducer', material='equipment', print=False,
             ops=[{'translate':[80,98,220]}, {'rotate':[180,0,0]}],
             explode_mm=[0,140,0], acoustic_direction=[0,0,1],
             note='Existing provisional TD04A silhouette, inside front C; upward face is a visual assumption.'),
        item('transducer_inner_mount', 'transducer_inner_mount', 'Transducer mount', 'steel',
             [103,103,149], [0,140,0])
    ]
    p['notes'] = [
        'User confirmed A = two opposite faces, each bolted upper/lower; C = the other two faces.',
        'Exactly one camera (front C, outward +Y), one light (rear C, upward +Z), one transducer inside front C.',
        'User confirmed bottom plate is Frame B; former three orange bars are removed.',
        'Frame A blue, B green with six lightening windows, C purple; clamp-to-A lugs have screw connections.',
        'Two shown cables only: transducer to vessel bottom, vessel bottom to upper exit; ties use window edges.',
        'All dimensions, mounting details, transducer direction and cable bend shapes are provisional visual choices.'
    ]
    p['cable_routes'] = [
        dict(label='Cable 1 | transducer to bottom', material='cable_sensor', radius_mm=2.5,
             start='transducer_inside_c', end='vessel_bottom',
             points_mm=[[80,57.5,168],[90,65,158],[113,94,145],[118,101,120],
                        [118,101,80],[118,101,20],[108,91,-30],[72,65,-52],
                        [32,22,-50],[18,6,-32],[18,6,-14]],
             ties_mm=[[118,101,140],[118,101,78],[118,101,-20]]),
        dict(label='Cable 2 | bottom to upper exit', material='cable_upper', radius_mm=2.5,
             start='vessel_bottom', end='upper_exit',
             points_mm=[[-18,-6,-14],[-18,-6,-34],[-34,-25,-60],[-76,-75,-69],
                        [-116,-101,-60],[-118,-101,-10],[-118,-101,60],
                        [-118,-101,150],[-118,-101,240],[-118,-101,285]],
             ties_mm=[[-118,-101,-40],[-118,-101,70],[-118,-101,180],[-118,-101,240]])
    ]
    p['clamp_a_connection'] = dict(status='visual_only', axis='X',
                                  screw_centers_mm=[[x,y,100] for x in [-136,136] for y in [-8,8]])
    write(OUT/'placement.json', p)
    s = read(PART/'concept.json')
    v = s['variants']
    # No uninstantiated former orange-bar design remains in the current spec.
    v.pop('frame_b', None)
    v.pop('ballast_carrier', None)
    v['frame_b_bottom'] = dict(kind='panel', size_mm=[260,190,6], bevel_mm=2,
                              normal_axis='Z', windows=[dict(center_mm=[x,y,0],size_mm=[42,46,24])
                                                       for x in [-70,0,70] for y in [-58,58]])
    v['frame_a_lower']['holes'] = [dict(center_mm=[0,y,95],radius_mm=2.2,depth_mm=30,axis='X')
                                  for y in [-8,8]]
    spines = v['integrated_clamps']['spines']
    if len(spines) == 4:
        spines += [dict(center_mm=[x,0,100],size_mm=[37,28,24]) for x in [-112,112]]
    v['transducer_inner_mount'] = dict(kind='bar',size_mm=[54,14,8],bevel_mm=1.5)
    write(PART/'concept.json', s)
    print('Revised sources; preceding model and images retained in _work.')
