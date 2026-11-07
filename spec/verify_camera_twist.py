"""Check actual integral camera mesh, all child hardware and removal/tool paths."""
from pathlib import Path
import hashlib, itertools, json, sys
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from prepare_child_horizontal_plate_frame import matrix, save, load_world, printed_baseline
from verify_parent_exterior_qr import intersection, probe

def main():
    folder=ROOT/'assemblies/child_horizontal_plate_frame'
    placement=folder/'placement.json';p=json.loads(placement.read_text(encoding='utf-8'))
    world=load_world(p);lookup={r['label']:(r,m) for r,m in world}
    new=[(r,m) for r,m in world if r.get('owner')=='camera_twist_accessory']
    failures=[];checks=[]
    native_checks=[]
    def check(kind,label,a,b,threshold=.04):
        v=intersection(a,b)
        if v>threshold:failures.append(dict(kind=kind,label=label,volume_mm3=v))
        return v
    part=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
    original=trimesh.load(part/'camera_mount.stl',force='mesh')
    integral=trimesh.load(part/'camera_mount_twist.stl',force='mesh')
    lost=trimesh.boolean.difference([original,integral],engine='manifold',check_volume=False)
    lost_volume=0. if lost is None else abs(float(lost.volume))
    native_checks.append(dict(feature='current_camera_geometry_retained',lost_mm3=lost_volume))
    if lost_volume>.05:failures.append(dict(kind='camera_geometry_removed',volume_mm3=lost_volume))
    native_checks.append(dict(feature='compact_no_front_stop',bounds_mm=integral.bounds.tolist()))
    if not (abs(integral.extents[0]-88)<.01 and abs(integral.bounds[1,1]-9)<.01):
        failures.append(dict(kind='front_stop_or_unused_floor_remaining',bounds_mm=integral.bounds.tolist()))
    for label,ends,diameter in [('M5_axis',[[-60,0,24],[60,0,24]],5),
                              ('left_D12_driver',[[-50,0,24],[-25,0,24]],12),
                              ('right_D12_driver',[[25,0,24],[50,0,24]],12)]:
        v=check('camera_fastener_access',label,integral,probe(*ends,diameter),.01)
        native_checks.append(dict(feature=label,diameter_mm=diameter,blocked_mm3=v))
    for r,m in new:
        if r.get('print'):
            checks.append(dict(label=r['label'],watertight=bool(m.is_volume),components=len(m.split()),
                bounds_mm=m.bounds.tolist(),volume_mm3=float(m.volume)))
            if not m.is_volume or len(m.split())!=1:failures.append(dict(kind='invalid_mesh',label=r['label']))
        for b,bm in world:
            if b.get('owner')=='camera_twist_accessory':continue
            check('existing_interference',r['label']+' / '+b['label'],m,bm)
    for (r,m),(b,bm) in itertools.combinations(new,2):
        check('new_interference',r['label']+' / '+b['label'],m,bm)
    station=p['side_twist_mount']['stations'][p['camera_twist_mount']['station']]
    face=matrix([{'translate':station['origin_mm']},{'rotate':station['rotation_deg']}])
    dock=face@matrix([{'translate':p['camera_twist_mount']['dock_offset_uvn_mm']},
                      {'rotate':[0,0,p['camera_twist_mount']['dock_rotation_deg']]}])
    camera_pose=matrix(lookup['side_camera_mount'][0]['ops'])
    orientation=dict(camera_up_xyz=camera_pose[:3,2].tolist(),camera_front_xyz=camera_pose[:3,1].tolist(),
                     camera_right_xyz=camera_pose[:3,0].tolist(),lock_withdrawal_axis_xyz=dock[:3,0].tolist())
    if not (np.allclose(camera_pose[:3,2],[0,0,1]) and np.allclose(camera_pose[:3,1],[-1,0,0])
            and np.allclose(dock[:3,0],[0,0,1])):
        failures.append(dict(kind='camera_not_upright_or_lock_direction',**orientation))
    removable={r['label'] for r,m in new if r.get('removal_group')=='child_camera'}
    locks={'side_camera_'+k for k in ('twist_knob','lock_bolt','lock_washer')}
    fixed=[(r,m) for r,m in world if r['label'] not in removable|locks]
    sweep=[]
    for angle in range(0,61,5):
        movement=dock@matrix([{'translate':[0,0,.6*angle/60]},{'rotate':[0,0,-angle]}])@np.linalg.inv(dock)
        for name in removable:
            m=lookup[name][1].copy();m.apply_transform(movement)
            for b,bm in fixed:
                v=check('release_rotation',f'{angle} deg: {name} / {b["label"]}',m,bm,.1)
                if v>.1:sweep.append([angle,name,b['label'],v])
    for travel in [5,10,20,40,80]:
        movement=dock@matrix([{'translate':[0,0,.6+travel]},{'rotate':[0,0,-60]}])@np.linalg.inv(dock)
        for name in removable:
            m=lookup[name][1].copy();m.apply_transform(movement)
            for b,bm in fixed:check('release_pull',f'{travel} mm: {name} / {b["label"]}',m,bm,.1)
    for travel in [0,5,10,20,30,45]:
        for name in locks:
            m=lookup[name][1].copy();m.apply_translation(dock[:3,0]*travel)
            for b,bm in world:
                if b['label'] in locks:continue
                check('lock_withdrawal',f'{travel} mm: {name} / {b["label"]}',m,bm)
    knob=lookup['side_camera_twist_knob'][0];km=matrix(knob['ops'])
    src=trimesh.load(ROOT/knob['part']/(knob['file']+'.stl'),force='mesh')
    for allowance in [0,3]:
        clearance=trimesh.creation.cylinder(radius=np.linalg.norm(src.vertices[:,:2],axis=1).max()+allowance,
            height=src.extents[2],sections=96)
        clearance.apply_translation([0,0,src.bounds[:,2].mean()]);clearance.apply_transform(km)
        for b,bm in world:
            if b['label'] in locks:continue
            check('knob_turn_clearance',f'radial +{allowance}: '+b['label'],clearance,bm)
    # Frame bolts are installed before the camera. The other frame hardware,
    # case and receiver remain in the tool/nut approach inspection.
    tools=[]
    for i in range(2):
        bolt=lookup[f'side_camera_frame_{i}_screw'][0];pose=matrix(bolt['ops'])
        tool=probe([0,0,.01],[0,0,70],3);tool.apply_transform(pose)
        host_bolt=lookup[bolt['label']][1]
        # Opposite nut seat/tip positions measured from the real fastener mesh.
        local=host_bolt.copy();local.apply_transform(np.linalg.inv(face))
        nut=lookup[f'side_camera_frame_{i}_nut'][1].copy();nut.apply_transform(np.linalg.inv(face))
        protrusion=float(nut.bounds[0,2]-local.bounds[0,2])
        tools.append(dict(label=bolt['label'],tip_n_mm=float(local.bounds[0,2]),
                          nut_inner_n_mm=float(nut.bounds[0,2]),protrusion_mm=protrusion))
        if protrusion<1.4:failures.append(dict(kind='insufficient_thread_protrusion',label=bolt['label'],protrusion_mm=protrusion))
        for b,bm in world:
            if b['label'] in removable|locks or b['label']==bolt['label']:continue
            check('frame_bolt_driver_before_camera',bolt['label']+' / '+b['label'],tool,bm)
    for side,sign in [('left',-1),('right',1)]:
        hand=trimesh.creation.box([150,90,170]);hand.apply_translation([sign*(122+75),0,125])
        for r,m in new:check('central_hand_approach',side+' / '+r['label'],hand,m)
    for reservation in p.get('access_reservations',[]):
        if reservation.get('shape')=='cylinder':
            keep=trimesh.creation.cylinder(radius=reservation['diameter_mm']/2,height=reservation['length_mm'],sections=64)
            keep.apply_transform(matrix([{'translate':reservation['centre_mm']},{'rotate':reservation['rotation_deg']}]))
        elif 'bounds_mm' in reservation:
            bounds=np.array(reservation['bounds_mm']);keep=trimesh.creation.box(bounds[1]-bounds[0]);keep.apply_translation(bounds.mean(axis=0))
        else:continue
        for r,m in new:check('cable_reservation',reservation.get('name','reservation')+' / '+r['label'],keep,m)
    printed_baseline()
    result=dict(passed=not failures,placement_sha256=hashlib.sha256(placement.read_bytes()).hexdigest(),
        printed_meshes=checks,native_camera_checks=native_checks,orientation=orientation,fastener_tips=tools,failures=failures,
        motion=dict(rotation_degrees=list(range(0,61,5)),pull_mm=[5,10,20,40,80],lock_withdrawal_mm=[0,5,10,20,30,45],
            knob_radial_allowance_mm=[0,3]),
        limits=['Provisional existing case envelope; real lens field of view, cable bending and hand/glove fit unverified.',
                'Discrete rigid-body geometry checks; strength, physical fit, friction, creep and fatigue unverified.'])
    save(folder/'_work/analysis/camera_twist_20261021/geometry_checks.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
