"""Install one shared integral camera/C male on parent and child exteriors.

Only camera-owned rows are changed. Existing printed child stock is immutable.
Canonical placements remain authoritative; snapshots retain the previous state.
"""
from pathlib import Path
from copy import deepcopy
import argparse, hashlib, json, os, shutil, subprocess, sys
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from prepare_child_horizontal_plate_frame import matrix, save, printed_baseline, call, OSC
from clean_stl_degenerates import clean
CAM='parts/child/exterior/printed/dji_osmo_action6_mount_m3'
RECEIVER='parts/child/exterior/printed/child_horizontal_twist_mount'
QR='parts/common/jigs/quick_release_prototypes'
TAG='camera_twist_accessory'
STEM='child_horizontal_twist_mount_camera_receiver'
CAMERA_DOCK_ANGLE_DEG=90 # -90 deg from portrait: clockwise from outside left

def snapshot(assembly):
    dest=assembly/'_work/analysis/camera_twist_20261021/history'
    if (dest/'snapshot.json').exists():return
    files=['README.md','placement.json','print_config.json']
    files += [p.relative_to(assembly).as_posix() for p in (assembly/'parts').glob('*') if p.is_file()]
    records=[]
    for relative in files:
        src=assembly/relative
        if not src.exists():continue
        dst=dest/relative;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
        records.append(dict(file=relative,sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
    save(dest/'snapshot.json',records)

def build_receiver():
    # Left front U=-Y; negative U moves the dock toward the front, away from
    # the central hand approach. Keep the original two frame mounting axes.
    folder=ROOT/RECEIVER
    variants=folder/'variants.txt';text=variants.read_text(encoding='utf-8')
    line=f'camera_receiver part="frame_receiver" receiver_u=-35 dock_rotation={CAMERA_DOCK_ANGLE_DEG}'
    variants.write_text('\n'.join(l for l in text.splitlines() if not l.startswith('camera_receiver ')).rstrip()+'\n'+line+'\n',encoding='utf-8')
    call([OSC,'--export-format','asciistl','-D','part="frame_receiver"','-D','receiver_u=-35','-D',f'dock_rotation={CAMERA_DOCK_ANGLE_DEG}',
          '-o',folder/(STEM+'.stl'),folder/'child_horizontal_twist_mount.scad'],
         folder/'_work/logs/camera_receiver.log')
    clean(folder/(STEM+'.stl'),folder/'_work/analysis/camera_receiver/edge_flip.json',binary=False)
    m=trimesh.load(folder/(STEM+'.stl'),force='mesh')
    assert m.is_volume and len(m.split())==1
    meta=json.loads((folder/'manufacturing.json').read_text(encoding='utf-8'))
    meta['print_rotations_deg'][STEM]=[0,0,0]
    meta['layer_heights_mm'][STEM]=.1
    meta['support_modes'][STEM]='auto'
    if STEM not in meta['degenerate_edge_flip_files']:meta['degenerate_edge_flip_files'].append(STEM)
    save(folder/'manufacturing.json',meta)

def install_parent(p):
    p['items']=[r for r in p['items'] if r['label'] not in ('camera_qr_male','locating_camera_stop')
                and not r['label'].startswith(('qr_male_','locating_camera_'))]
    camera=next(r for r in p['items'] if r['label']=='camera_mount')
    camera.update(file='camera_mount_twist',note='Compact camera cradle: outer O-triangle-O front stop and floor extension removed; integral stock C male.')
    p['camera_twist_mount']=dict(revision=2,source=CAM+'/camera_mount_twist.scad',
        female='camera_qr_female',male='camera_mount',parent_camera_pose_retained=True,
        front_rotation_stop_removed=True,
        removed_hardware='four M3x14 socket screws and four M3 nuts; detached front adjuster and its bridge/adjusting fasteners')

def install_child(p):
    p['items']=[r for r in p['items'] if r.get('owner')!=TAG]
    p['fastener_joints']=[r for r in p['fastener_joints'] if r.get('owner')!=TAG]
    station=p['side_twist_mount']['stations']['left_front']
    station['status']='camera_installed'
    face=[{'translate':station['origin_mm']},{'rotate':station['rotation_deg']}]
    dock=face+[{'translate':[-35,0,0]},{'rotate':[0,0,CAMERA_DOCK_ANGLE_DEG]}]
    template={r['label']:r for r in p['items']}
    def row(label,part,file,ops,printed=False,color='Silver',moving=False):
        r=dict(label='side_camera_'+label,part=part,file=file,ops=ops,
               group='accessories' if printed or moving else 'fasteners',color=color,
               print=printed,owner=TAG)
        if moving:r['removal_group']='child_camera'
        p['items'].append(r);return r
    row('frame_receiver',RECEIVER,STEM,face,True,'SteelBlue')
    # Reuse the already validated metal/washer/knob stack in the same dock axes.
    for label in ['twist_knob','lock_bolt','lock_nut','lock_washer','rubber_pads']:
        r=deepcopy(template['side_light_'+label]);r['label']='side_camera_'+label
        r['ops']=dock+r['ops'][3:];r['owner']=TAG
        if label=='rubber_pads':r['removal_group']='child_camera'
        p['items'].append(r)
    for i in range(2):
        for kind in ['screw','head_washer','nut']:
            r=deepcopy(template[f'side_light_frame_{i}_{kind}'])
            r['label']=r['label'].replace('side_light_','side_camera_');r['ops']=face+r['ops'][2:];r['owner']=TAG
            p['items'].append(r)
        joint=deepcopy(next(r for r in p['fastener_joints'] if r['label']==f'side_light_frame_{i}'))
        joint.update(label=f'side_camera_frame_{i}',owner=TAG)
        # Transform the recorded world seats/axes with the actual left/right poses.
        right=matrix(template['side_light_frame_receiver']['ops'])
        left=matrix(face);mapping=left@np.linalg.inv(right)
        for k in ('seat_mm','nut_start_mm'):
            joint[k]=(mapping@np.r_[joint[k],1])[:3].tolist()
        for k in ('axis_rotation_deg','nut_rotation_deg'):
            rot=mapping@matrix([{'rotate':joint[k]}])
            joint[k]=np.degrees(trimesh.transformations.euler_from_matrix(rot)).tolist()
        p['fastener_joints'].append(joint)
    # Read the q->camera matrix from the generated source's defining dimensions.
    import re
    source=(ROOT/CAM/'camera_mount.scad').read_text(encoding='utf-8')
    scalar=lambda n:float(re.search(rf'\b{n}\s*=\s*([0-9.]+)\s*;',source).group(1))
    back=-scalar('case_d')/2-scalar('rear_gap')-scalar('plate_t')
    wrapper=(ROOT/CAM/'camera_mount_twist.scad').read_text(encoding='utf-8')
    adapter_t=float(re.search(r'\badapter_thickness\s*=\s*([0-9.]+)',wrapper).group(1))
    from build_child_horizontal_accessories import generate_interface
    q=generate_interface();locked=sum(q[k] for k in ('pad_t','ring_h','twist_plate_t','twist_lock_gap'))
    a=np.array([[0,-1,0,0],[0,0,-1,back-adapter_t],[1,0,0,scalar('mount_center_z')],[0,0,0,1]],float)
    local=matrix([{'translate':[0,0,locked]},{'rotate':[180,0,0]}])@np.linalg.inv(a)
    native=[{'translate':local[:3,3].tolist()},
            {'rotate':np.degrees(trimesh.transformations.euler_from_matrix(local)).tolist()}]
    row('mount',CAM,'camera_mount_twist',dock+native,True,'Orange',True)
    # The case proxy is already the established provisional case envelope.
    parent=json.loads((ROOT/'assemblies/parent_exterior/placement.json').read_text(encoding='utf-8'))
    case=deepcopy(next(r for r in parent['items'] if r['label']=='camera_case_reference'))
    parent_cam=next(r for r in parent['items'] if r['label']=='camera_mount')
    relative=np.linalg.inv(matrix(parent_cam['ops']))@matrix(case['ops'])
    extra=[{'translate':relative[:3,3].tolist()},
           {'rotate':np.degrees(trimesh.transformations.euler_from_matrix(relative)).tolist()}]
    row('case_reference',case['part'],case['file'],dock+native+extra,False,'DimGray',True)
    p['camera_twist_mount']=dict(revision=2,station='left_front',dock_offset_uvn_mm=[-35,0,0],
        dock_origin_mm=(matrix(dock)@np.array([0,0,0,1]))[:3].tolist(),dock_rotation_deg=CAMERA_DOCK_ANGLE_DEG,
        camera_orientation='upright landscape; rotated clockwise 90 deg from outside-left portrait view',
        interface='CHILD-HORIZONTAL-TWIST-C-R4',mount_screws='M3x18 socket, two; 0.5 mm head washers; existing inside nut pockets',
        removal='withdraw vertical lock assembly +Z 45 mm; rotate -60 deg about dock N, then outward 80 mm',
        camera_case_dimensions='existing provisional envelope; physical camera field of view and cable unverified')
    stock=set(p['print_progress']['source_mesh_sha256'])
    remaining=[r for r in p['items'] if r.get('print',False) and r['part']+'/'+r['file']+'.stl' not in stock]
    p['print_progress']['remaining_instances']=len(remaining)
    p['print_progress']['base_remaining_instances']=sum(r.get('owner')!='side_twist_accessory' for r in remaining)

def main():
    raise SystemExit('Legacy camera twist installer is retired; use configure_camera_fixture_clamp.py and build the updated sources.')
    # OpenSCAD 2021 cannot canonicalize the legacy Body_Models junction cwd.
    os.chdir(ROOT)
    parser=argparse.ArgumentParser();parser.add_argument('--placement-only',action='store_true');args=parser.parse_args()
    for name in ['parent_exterior','child_horizontal_plate_frame']:snapshot(ROOT/'assemblies'/name)
    if not args.placement_only:build_receiver()
    meta=json.loads((ROOT/CAM/'manufacturing.json').read_text(encoding='utf-8'))
    meta['print_rotations_deg']['camera_mount_twist']=[0,0,0]
    save(ROOT/CAM/'manufacturing.json',meta)
    for name,install in [('parent_exterior',install_parent),('child_horizontal_plate_frame',install_child)]:
        folder=ROOT/'assemblies'/name;p=json.loads((folder/'placement.json').read_text(encoding='utf-8'))
        install(p);save(folder/'placement.json',p)
        call([sys.executable,ROOT/'scad/lib/asm_gen.py',folder/'placement.json',folder/(name+'_view.scad')],
             folder/'_work/logs/camera_twist_view_generation.log')
    printed_baseline()
    print('Installed integral C camera on parent and left-front child; child printed stock unchanged.')

if __name__=='__main__':main()
