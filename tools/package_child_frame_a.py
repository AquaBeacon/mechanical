"""Place frame A's four tiles, splices and purchased fasteners from its spec.

Regenerates placement.json only. CAD generation and assembly_parts sync remain
separate operations; no raw optimiser mesh is a printable assembly item.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PART = 'parts/child/exterior/printed/child_exterior_structural_frame'
ASM = ROOT / 'assemblies/child_exterior_structure'
SCREW = 'parts/common/interior/cots/screw'


def main():
    d = json.loads((ROOT/PART/'spec/design_parameters.json').read_text(encoding='utf-8'))
    items = []
    for side, sign in [('right', 1), ('left', -1)]:
        # Proper rotations, not reflections: the plate and its outer face both
        # map to the matching side. The hole pattern is symmetric in local X.
        base = [{'translate': [sign*d['inner_face_x'], 0, 0]},
                {'rotate': [90, 0, sign*90]}]
        for variant in ['lower_minus', 'lower_plus', 'upper_minus', 'upper_plus']:
            items.append(dict(part=PART, file='child_exterior_structural_frame_'+variant,
                              label=f'Frame A {side} {variant}', group='frame_a',
                              color='SteelBlue', ops=base))
        splices = [(0, y, 0) for y in d['splice_centres_y']]
        splices += [(x, d['split_y'], 90) for x in [-158, 158]]
        for index, (x, y, angle) in enumerate(splices):
            local = [{'translate': [x, y, d['joint_seat_depth']]}, {'rotate': [0, 0, angle]}]
            items.append(dict(part=PART, file='child_exterior_structural_frame_splice',
                              label=f'Frame A {side} splice {index+1}', group='splices',
                              color='LightSlateGray', ops=base+local))
        # The nut sits completely in the inward recess; the M3x50 tip stays
        # behind the inward face. Inner nuts are inserted before the cage.
        outer_z = d['joint_seat_depth']+d['splice_seat_depth']
        nut_z = d['nut_pocket_depth']-2.4
        for index, (x, y) in enumerate(d['joint_holes_yz']):
            for suffix, z, color in [('m3x50', outer_z+.5, 'Silver'),
                                      ('washer_m3_05', outer_z, 'Silver'),
                                      ('nut_m3', nut_z, 'DimGray')]:
                items.append(dict(part=SCREW, file='screw_'+suffix,
                                  label=f'Frame A {side} joint {index+1} {suffix}',
                                  group='fasteners', color=color,
                                  ops=base+[{'translate': [x, y, z]}]))
    data = dict(name='child_exterior_structure', status='prototype_unqualified_joints', units='mm',
                note='Frame A prototype only, two sides. No clamp, frame C or complete vehicle is included. Split joint strength is unqualified.',
                coordinate_system='Vehicle X: side normal, Y: fore/aft, Z: vertical; clamp centres Z40/100/160.',
                groups=dict(frame_a=True, splices=True, fasteners=True), items=items)
    (ASM/'placement.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Placed {len(items)} items: 8 tiles, 12 splices, 48 each M3x50/washer/nut.')


if __name__ == '__main__':
    main()
