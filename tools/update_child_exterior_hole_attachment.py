"""Apply the user's pictured existing frame-hole attachment to concept sources."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'assemblies/child_exterior_concept'
PART = ROOT/'parts/child/exterior/printed/child_exterior_open_frame'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    placement = read(OUT/'placement.json')
    if placement['clamp_a_connection'].get('interface') == 'existing_clamp_frame_holes':
        raise SystemExit('Already applied; regenerate with build_child_exterior_concept.py.')
    history = OUT/'_work/images/history/ear_interpretation'
    history.mkdir(parents=True, exist_ok=True)
    for source in (OUT/'_work/images').glob('child_exterior_*'):
        if source.is_file():
            shutil.copy2(source, history/source.name)
    for source, name in [(OUT/'placement.json','placement_before_mount_hole_correction.json'),
                         (PART/'concept.json','concept_before_mount_hole_correction.json'),
                         (OUT/'child_exterior_concept.blend','child_exterior_before_mount_hole_correction.blend')]:
        shutil.copy2(source, OUT/'_work/intermediate'/name)
    reference = read(ROOT/'assemblies/child_clamp_suspension/placement.json')
    holes = []
    for row in reference['items']:
        if row['group'] == 'clamps':
            front = row['label'].endswith('_front')
            base_z = row['ops'][0]['translate'][2]
            for x in [-18,18]:
                for dz in [8,24]:
                    y = 85.35 if front else -85.35
                    holes.append(dict(reference_label=f"{row['label']}_frame_{x}_{dz}",
                        reference_clamp=row['label'], local_hole_mm=[-x if front else x,-85.35,dz],
                        axis_world_mm=[x,y,base_z+dz], tab_hole_world_mm=[x,89.35 if front else -89.35,base_z+dz]))
    assert len(holes) == 24
    placement['clamp_a_connection'] = dict(status='visual_only', interface='existing_clamp_frame_holes',
        axis='Y', reference_assembly='assemblies/child_clamp_suspension/placement.json',
        reference_part_doc='parts/child/exterior/printed/child_wte4_suspension_clamp/README.md',
        tab_face_y_mm=92.35, holes=holes,
        note='User image identifies the four holes on the flat frame-mounting pad, not the split-clamp ear bores. A returns split the four-hole pattern between left/right A. Both half-clamp mounting pads used; screw lengths provisional.')
    for row in placement['items']:
        if row['group'] == 'Frame A':
            row['inward_sign'] = 1 if 'left' in row['label'] else -1
            row['note'] = 'Blue A with inward returns using the pictured existing frame-mounting pad holes.'
        if row['label'] == 'clamp_cradle_integrated':
            row['note'] = 'Three linked clamps; existing four-hole mounting faces reused for A. Prior lateral extension lugs removed.'
    placement['notes'] = [n for n in placement['notes'] if 'ear' not in n and 'lugs' not in n]
    placement['notes'].append('A inward returns reuse all four pictured frame-mounting holes on each front/rear pad; two columns divided between left/right A, at three clamp levels.')
    write(OUT/'placement.json', placement)
    spec = read(PART/'concept.json')
    variants = spec['variants']
    variants['frame_a_lower'].pop('holes',None)
    for name, levels, rail in [
        ('frame_a_lower',[35,95],dict(center_mm=[0,28.8,56],size_mm=[12,26,82])),
        ('frame_a_upper',[-21],dict(center_mm=[0,28.8,-30],size_mm=[12,26,50]))]:
        variants[name].pop('mounting_rail',None)
        variants[name]['inward_tabs'] = dict(local_z_mm=levels, center_x_mm=24.825,
            hole_x_mm=118, center_y_mm=[-89.35,89.35], size_mm=[130,6,32],
            hole_offsets_z_mm=[-8,8], hole_radius_mm=1.75)
        variants[name]['inward_tabs']['center_x_mm'] = 59
    # Move the joining spine off the existing hole axes. Remove previous lateral lugs.
    spines = variants['integrated_clamps']['spines'][:4]
    for spine, x in zip(spines[:2],[-95,95]):
        spine['center_mm'] = [x,0,100]
        spine['size_mm'] = [8,26,156]
    variants['integrated_clamps']['spines'] = spines
    write(PART/'concept.json',spec)
    print('A returns aligned to the pictured 4-hole mounting faces, front/rear at all 3 levels; 24 axes.')
