"""Archive the vertical study and configure the horizontal visual study (mm).

No printable CAD is changed. Existing reference meshes/proxies are reused.
Run once to migrate; subsequent runs retain the original archive.
"""
from pathlib import Path
import copy
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
ASM = ROOT / 'assemblies/child_exterior_concept'
PART = ROOT / 'parts/child/exterior/printed/child_exterior_open_frame'
HISTORY = ASM / '_work/intermediate/before_horizontal_20261007'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main():
    if not HISTORY.exists():
        HISTORY.mkdir(parents=True)
        for name in ['placement.json', 'README.md', 'child_exterior_concept.blend', 'child_exterior_concept.blend1', 'print_config.json']:
            if (ASM/name).exists():
                shutil.copy2(ASM/name, HISTORY/name)
        shutil.copytree(ASM/'parts', HISTORY/'parts')
        for name in ['concept.json', 'README.md']:
            shutil.copy2(PART/name, HISTORY/('part_'+name))
        for name in ['build_child_exterior_concept.py', 'present_child_exterior_concept.py', 'verify_child_exterior_concept.py']:
            shutil.copy2(ROOT/'tools'/name, HISTORY/name)
        old_images = ASM/'_work/images/history/before_horizontal_20261007'
        old_images.mkdir(parents=True, exist_ok=True)
        for path in (ASM/'_work/images').glob('child_exterior_*'):
            if path.is_file():
                shutil.move(str(path), old_images/path.name)
        for path in (ASM/'_work/logs').glob('*.json'):
            shutil.copy2(path, HISTORY/path.name)
    old = read(HISTORY/'placement.json')
    items = []
    # Vessel Z becomes +Y. Tube centre is [0, 0, 140], rear cap Y=-113.8.
    vessel_ops = [{'translate': [0, -100, 140]}, {'rotate': [-90, 0, 0]}]
    for source in old['items']:
        if source['group'] == 'vessel':
            row = copy.deepcopy(source)
            row['ops'] = vessel_ops + row['ops']
            row['note'] = 'Existing reference geometry: horizontal axis +Y; tube length 200 mm.'
            row['explode_mm'] = [0, 0, 100]
            items.append(row)
    # Reuse the existing connected three-level clamp halves, rotated rigidly.
    for source in read(ROOT/'assemblies/child_clamp_suspension/placement.json')['items']:
        if source['group'] not in ['clamps', 'rubber']:
            continue
        row = copy.deepcopy(source)
        row['ops'] = vessel_ops + [{'rotate': [0, 0, 90]}] + row['ops']
        row.update(print=False, material='clamp' if row['group']=='clamps' else 'rubber', explode_mm=[0,0,70])
        row['group'] = 'Horizontal cradle'
        items.append(row)
    spec = read(PART/'concept.json')
    variants = spec['variants']
    # Dimensions are visual placeholders, not manufactured or topopt geometry.
    variants.update({
        'horizontal_side': {'kind':'panel', 'size_mm':[12,440,200], 'normal_axis':'X', 'bevel_mm':3,
                            'windows':[{'center_mm':[0,0,0], 'size_mm':[40,388,148]}]},
        'horizontal_skid': {'kind':'bar', 'size_mm':[30,480,22], 'bevel_mm':5},
        'horizontal_crossbar': {'kind':'bar', 'size_mm':[288,22,16], 'bevel_mm':2},
        'horizontal_cradle_rail': {'kind':'bar', 'size_mm':[59,196,16], 'bevel_mm':2},
        'horizontal_camera_mount': {'kind':'bar', 'size_mm':[90,56,12], 'bevel_mm':2},
        'horizontal_camera_crossbar': {'kind':'bar', 'size_mm':[288,30,16], 'bevel_mm':2},
        'horizontal_sensor_arm': {'kind':'bar', 'size_mm':[60,38,12], 'bevel_mm':2},
        'horizontal_sensor_post': {'kind':'bar', 'size_mm':[16,32,55], 'bevel_mm':2},
        'horizontal_weight_tray': {'kind':'bar', 'size_mm':[288,106,10], 'bevel_mm':2},
        'horizontal_weight_stop': {'kind':'bar', 'size_mm':[16,58,18], 'bevel_mm':2},
        'horizontal_weight_band': {'kind':'composite', 'rings':[{'center_mm':[0,0,0],
                                  'outer_radius_mm':27.5, 'inner_radius_mm':24.75, 'height_mm':8}]},
        'horizontal_foam_reservation': {'kind':'bar', 'size_mm':[54,148,34], 'bevel_mm':8,
                                         'note':'Buoyancy-space reservation only; material, density and volume to be sized.'},
        'horizontal_rear_bumper': {'kind':'panel', 'size_mm':[288,12,82], 'normal_axis':'Y', 'bevel_mm':3,
                                  'windows':[{'center_mm':[0,0,0], 'size_mm':[200,40,46]}]}
    })
    spec['current_layout'] = 'horizontal_open_frame_20261007'
    write(PART/'concept.json', spec)

    def concept(label, variant, loc, group, material, explode=(0,0,0)):
        items.append(dict(label=label, part=PART.relative_to(ROOT).as_posix(), file=variant,
                          geometry='concept', group=group, material=material, print=False,
                          ops=[{'translate':loc}], explode_mm=list(explode)))

    for sign, side in [(-1,'left'),(1,'right')]:
        concept('side_'+side,'horizontal_side',[sign*150,0,125],'Open side frames','frame_a',[sign*130,0,0])
        concept('skid_'+side,'horizontal_skid',[sign*150,0,16],'Landing skids','guard',[0,0,-50])
        # Inner end X=85, coincident with reference clamp pad at 85.35.
        concept('cradle_rail_'+side,'horizontal_cradle_rail',[sign*114.5,-16,140],'Cradle interfaces','clamp')
        concept('foam_space_'+side,'horizontal_foam_reservation',[sign*111,100,225],'Buoyancy reservation','foam',[sign*70,0,80])
        concept('weight_stop_'+side,'horizontal_weight_stop',[sign*122,-90,44],'Ballast support','guard')
        for x in [sign*68,sign*98]:
            concept('weight_band_'+str(x),'horizontal_weight_band',[x,-90,59.25],'Ballast retainers','steel')
            items[-1]['ops'].append({'rotate':[0,90,0]})
    for y in [-186,186]:
        concept('lower_crossbar_'+str(y),'horizontal_crossbar',[0,y,38],'Lower frame','guard',[0,0,-40])
    concept('weight_tray','horizontal_weight_tray',[0,-90,30],'Ballast support','guard',[0,0,-40])
    concept('camera_crossbar','horizontal_camera_crossbar',[0,200,96],'Equipment mounts','guard')
    concept('camera_mount','horizontal_camera_mount',[0,229,96],'Equipment mounts','frame_a')
    concept('light_arm','horizontal_sensor_arm',[-120,-110,170],'Equipment mounts','frame_a')
    concept('transducer_arm','horizontal_sensor_arm',[120,-70,216],'Equipment mounts','frame_a')
    concept('transducer_post','horizontal_sensor_post',[150,-70,235.5],'Equipment mounts','frame_a')
    concept('rear_cable_bumper','horizontal_rear_bumper',[0,-214,140],'Rear cable protection','guard',[0,-80,0])
    for source in old['items']:
        if source['label'] == 'action_camera_front':
            row = copy.deepcopy(source)
            row.update(ops=[{'translate':[0,235,145]}], view_direction=[0,1,0], explode_mm=[0,100,0])
            items.append(row)
        elif source['label'] == 'dive_light_rear':
            row = copy.deepcopy(source)
            # The proxy's side bracket extends toward -Y and stays outside the tube.
            row.update(ops=[{'translate':[-108,-110,225]}], view_direction=[0,0,1], explode_mm=[-80,0,80])
            items.append(row)
        elif source['label'] == 'transducer_inside_c':
            row = copy.deepcopy(source)
            row.update(label='transducer_upward', ops=[{'translate':[108,-46,286]},{'rotate':[180,0,180]}],
                       acoustic_direction=[0,0,1], local_acoustic_axis=[0,0,-1], explode_mm=[80,0,80],
                       note='Same provisional TD04A mesh; acoustic face -local Z is directed +world Z as requested.')
            items.append(row)
        elif source['label'].startswith('ballast_C_'):
            row = copy.deepcopy(source)
            sign = -1 if source['label'].endswith('rear') else 1
            row.update(label='ballast_C_'+('left' if sign<0 else 'right'),
                       ops=[{'translate':[sign*38,-90,59.25]},{'rotate':[0,sign*90,0]}],
                       declared_mass_g=1000, explode_mm=[0,0,-60])
            items.append(row)
        elif source['label'].startswith('ballast_B_'):
            row = copy.deepcopy(source)
            idx = int(source['label'].split('_')[-1])-1
            row.update(ops=[{'translate':[(-1 if idx<2 else 1)*145,(-55 if idx%2==0 else 55),35]}],
                       declared_mass_g=60, explode_mm=[0,0,-40])
            # Plate long axis is local X; rotate it along the skid's Y axis.
            row['ops'].append({'rotate':[0,0,90]})
            items.append(row)

    routes = [
        dict(label='TD04A cable', material='cable_sensor',radius_mm=2.5,start='transducer_upward',end='rear_cap',
             points_mm=[[108,-72,218],[124,-115,210],[124,-162,178],[100,-168,156],[44,-158,140],[20,-142,132]],
             note='Indicative route and slack; fitting into a specific cap hole is not certified.'),
        dict(label='Tether route', material='cable_upper',radius_mm=3,start='rear_cap',end='rear_upper_exit',
             points_mm=[[-20,-142,132],[-54,-174,140],[-85,-180,175],[-125,-180,215],[-150,-210,260],[-150,-260,320]],
             note='Indicative path. Frame must carry tether load; strain relief and real bend radius are pending.')
    ]
    write(ASM/'placement.json',dict(
        name='child_exterior_concept',status='exploration_only',units='mm',
        layout='horizontal_open_frame_20261007',coordinate_system='X right; +Y forward/vessel axis; +Z upward. Tube Y=-100..100, centre Z=140.',
        dimensions_status='Provisional visual proportions; no approved fabrication interfaces.',
        reference_assembly='child_clamp_suspension',reference_photos=old['reference_photos'],
        revision='2026-10-07 horizontal vessel; transducer/light up; camera forward horizontally',
        notes=['No thrusters added: this is the existing child exterior layout study.',
               'Foam blocks represent reserved volume only; product/material/buoyancy not selected.',
               'Existing clamp cage is shown as a rigid reference; new rail attachment remains provisional.',
               'Prior hinged bottom guard is archived; rear bumper is fixed and removable, no hinge claim.'],
        items=items,cable_routes=routes,
        ballast_mount=dict(declared_total_mass_g=2240,quantity_C=2,quantity_B=4,note='Same inventory, now beneath vessel; final trim and retention pending.'),
        design_envelope_mm=dict(frame_width=330,skid_length=480,frame_top_z=225),
        reference_sources=[dict(title='BlueROV2 R4 official CAD',url='https://cad.bluerobotics.com/BLUEROV2-R4.zip',local='ref/BLUEROV2-R4.zip'),
                           dict(title='Technical Reference',url='https://bluerobotics.com/learn/technical-reference/'),
                           dict(title='Assembly guide',url='https://bluerobotics.com/learn/bluerov2-assembly/')],
        history='Previous vertical layout and source snapshots: _work/intermediate/before_horizontal_20261007; images: _work/images/history/before_horizontal_20261007'
    ))
    print('Configured horizontal visual study; archive retained:', HISTORY)


if __name__ == '__main__':
    main()
