"""One placement transform shared by candidate verification and publication."""
from copy import deepcopy
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'


def candidate_placement(original, interface, geometry):
    placement = deepcopy(original)
    d = interface['clamp']
    gap = d['split_gap']
    bolt_length = 10*math.ceil((2*d['ear_t']+gap+2+2.4+3)/10)
    bolt_variant = f'screw_m3x{bolt_length}'
    if not (ROOT/'parts/common/interior/cots/screw'/(bolt_variant+'.stl')).exists():
        raise RuntimeError('Build purchased bolt variant first: '+bolt_variant)
    old_items = placement['items']
    placement['items'] = []
    for front, angle in [(False,0),(True,180)]:
        placement['items'].append(dict(label='cage_front' if front else 'cage_rear',
            part=PART.relative_to(ROOT).as_posix(), file='child_wte4_suspension_clamp_cage',
            group='clamps', color='SteelBlue' if front else 'SeaGreen',
            ops=[dict(rotate=[0,0,angle])],
            note='Native optimised three-band cage; lifting eye on four-hole mounting-face side. Exploration only.'))
    for item in old_items:
        if item.get('group') == 'clamps':
            continue
        if item.get('group') == 'hardware':
            for op in item.get('ops', []):
                if 'translate' in op:
                    p = op['translate']
                    if abs(p[0]) > 70:
                        p[0] = d['bolt_x'] if p[0] > 0 else -d['bolt_x']
                        face = abs(geometry.get('clamp_washer_seat_y',-d['ear_t']-gap/2))
                        offset = 0 if 'washer_' in item['label'] else 1
                        p[1] = (1 if p[1] > 0 else -1)*(face+offset)
                        if item['label'].endswith('_bolt'):
                            item['file'] = bolt_variant
        placement['items'].append(item)
    placement['status'] = 'exploration_only'
    return placement, bolt_length
