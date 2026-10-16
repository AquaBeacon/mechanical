"""Mesh, hardware, staged tools and discrete removal checks for side twist."""
from pathlib import Path
import hashlib,json,itertools
import numpy as np
import trimesh
from prepare_child_horizontal_plate_frame import ROOT,OUT,load_world,matrix,overlap,save,printed_baseline
from build_child_horizontal_accessories import TAG,PART,QR,hardware

def main():
    p=json.loads((OUT/'placement.json').read_text(encoding='utf-8'));world=load_world(p);lookup={r['label']:(r,m) for r,m in world}
    new=[(r,m) for r,m in world if r.get('owner')==TAG]
    printed=[(r,m) for r,m in new if r['print']]; failures=[];rows=[]
    # Ensure repeated accessory rebuilds preserve all foreign rows and choices.
    from copy import deepcopy
    from build_child_horizontal_accessories import install
    regenerated=deepcopy(p)
    install(regenerated,json.loads((PART/'_work/analysis/geometry/interface.json').read_text()))
    if regenerated!=p:failures.append(dict(kind='placement_regeneration_not_idempotent'))
    def record(kind,label,volume,**extra):
        data=dict(kind=kind,label=label,volume_mm3=float(volume),**extra);rows.append(data)
        if volume>.1:failures.append(data)
    for r,m in printed:
        if not m.is_volume or len(m.split())!=1 or np.count_nonzero(m.area_faces<1e-12):
            failures.append(dict(kind='invalid_mesh',label=r['label']))
    # All newly installed meshes versus all pre-existing meshes, and all pairs
    # in the new hardware/printable set. Rubber contact is represented compressed.
    for r,m in new:
        for b,bm in world:
            if b.get('owner')==TAG:continue
            v=overlap(m,bm)
            if v>1e-5:record('existing_interference',r['label']+' / '+b['label'],v)
    for (r,m),(b,bm) in itertools.combinations(new,2):
        v=overlap(m,bm)
        if v>1e-5:record('new_interference',r['label']+' / '+b['label'],v)
    # Verify full cylindrical gauge against unchanged holder bore. This is a
    # reference-holder fit test, not a model of the light head/buttons.
    base=lookup['side_light_holder_cap'][0]
    gauge=trimesh.creation.cylinder(radius=16.49,height=81,sections=96)
    gauge.apply_translation([0,40.5,0]);gauge.apply_transform(matrix(base['ops']))
    for r,m in world:
        if not r['print'] and r['group']=='fasteners':continue
        record('reference_bore_gauge',r['label'],overlap(gauge,m))
    settings=p['side_twist_mount'];station=settings['stations'][settings['light_station']]
    face=matrix([{'translate':station['origin_mm']},{'rotate':station['rotation_deg']}])
    interface=json.loads((PART/'_work/analysis/geometry/interface.json').read_text())
    dock=face@matrix([{'translate':interface[6:8]+[interface[5]]},{'rotate':[0,0,interface[8]]}]);q=hardware()
    # Derive the optical axis from the actual holder placement, then follow the
    # same bayonet motion used for insertion. Positive Z is the locked direction.
    locked_axis=matrix(base['ops'])[:3,2]
    entry_motion=dock@matrix([{'rotate':[0,0,-q['turn_deg']]}])@np.linalg.inv(dock)
    closing_motion=dock@matrix([{'rotate':[0,0,q['turn_deg']]}])@np.linalg.inv(dock)
    entry_axis=entry_motion[:3,:3]@locked_axis
    closed_axis=closing_motion[:3,:3]@entry_axis
    knob_row,knob_mesh=lookup['side_light_twist_knob']
    knob_pose=matrix(knob_row['ops']);knob_axis=knob_pose[:3,2]
    knob_source=trimesh.load(ROOT/knob_row['part']/(knob_row['file']+'.stl'),force='mesh')
    knob_height=float(knob_source.bounds[1,2]-knob_source.bounds[0,2])
    knob_centre=(knob_pose@np.array([0,0,float(knob_source.bounds[:,2].mean()),1]))[:3]
    orientation=dict(locked_light_axis_xyz=locked_axis.tolist(),insertion_light_axis_xyz=entry_axis.tolist(),
        after_closing_axis_xyz=closed_axis.tolist(),closing_rotation_deg=q['turn_deg'],knob_axis_xyz=knob_axis.tolist(),
        knob_centre_xyz_mm=knob_centre.tolist(),light_centre_xyz_mm=settings['light_centre_xyz_mm'])
    if (not np.allclose(locked_axis,[0,0,1],atol=1e-9) or not np.allclose(closed_axis,[0,0,1],atol=1e-9)
            or not np.allclose(knob_axis,[0,1,0],atol=1e-9)
            or abs(knob_centre[2]-settings['light_centre_xyz_mm'][2])>1e-6
            or knob_centre[1]<=settings['light_centre_xyz_mm'][1] or not p['groups'].get('accessories')):
        failures.append(dict(kind='locked_orientation_or_visibility',**orientation))
    # A full turn of the fluted knob, plus 3 mm radial finger allowance. This
    # small clearance gauge is not a model of a complete hand or glove.
    knob_radius=float(np.linalg.norm(knob_source.vertices[:,:2],axis=1).max())
    turn_clearance=[]
    for allowance in (0,3):
        sweep=trimesh.creation.cylinder(radius=knob_radius+allowance,height=knob_height,sections=96)
        sweep.apply_translation([0,0,float(knob_source.bounds[:,2].mean())]);sweep.apply_transform(knob_pose)
        blocked=[dict(part=r['label'],volume_mm3=overlap(sweep,m)) for r,m in world
            if r['label'] not in ('side_light_twist_knob','side_light_lock_bolt','side_light_lock_washer')]
        blocked=[r for r in blocked if r['volume_mm3']>.1]
        turn_clearance.append(dict(radial_allowance_mm=allowance,blocked=blocked))
        if blocked:failures.append(dict(kind='knob_rotation_clearance',radial_allowance_mm=allowance,blocked=blocked))
    # Check that finishing the lower foot did not change the C cam, post, lug
    # or lock-bore region. Compare against the unchanged trial meshes locally.
    contact_checks=[]
    for kind,label,limits in [('female','side_light_frame_receiver',[4.1,18.1]),
                              ('male','side_light_light_twist',[10.4,18.4])]:
        original=trimesh.load(ROOT/QR/('quick_release_prototypes_twist_'+kind+'.stl'),force='mesh')
        if kind=='male':original.apply_transform(matrix([{'translate':[0,0,q['pad_t']+q['ring_h']+
            q['twist_plate_t']+q['twist_lock_gap']]},{'rotate':[180,0,0]}]))
        region=trimesh.creation.box([44,44,limits[1]-limits[0]]);region.apply_translation([0,0,sum(limits)/2])
        original.apply_transform(dock);region.apply_transform(dock)
        a=trimesh.boolean.intersection([original,region],engine='manifold',check_volume=False)
        b=trimesh.boolean.intersection([lookup[label][1],region],engine='manifold',check_volume=False)
        v=abs(float(a.volume))+abs(float(b.volume))-2*overlap(a,b)
        contact_checks.append(dict(kind=kind,symmetric_difference_mm3=max(0,v),normal_limits_mm=limits))
        if v>.1:failures.append(dict(kind='C_contact_geometry_changed',**contact_checks[-1]))
    moving_names={'side_light_light_twist','side_light_holder_cap','side_light_rubber_pads'}
    moving_names|={r['label'] for r,m in new if r['label'].startswith('side_light_clamp_')}
    # Reserve the whole central side area plus the outside approach to the grip.
    # Only accessories are checked against the broad region, since the original
    # side rails deliberately remain around their 90 x 34 mm finger opening.
    hand=[]
    for side,sign in (('right',1),('left',-1)):
        keep=trimesh.creation.box(extents=[150,90,170]);keep.apply_translation([sign*(122+75),0,125])
        for r,m in new:record('central_side_hand_approach',side+' / '+r['label'],overlap(keep,m))
        hand.append(dict(side=side,bounds_mm=keep.bounds.tolist()))
    for reservation in p.get('access_reservations',[]):
        if reservation.get('shape')=='cylinder':
            keep=trimesh.creation.cylinder(radius=reservation['diameter_mm']/2,height=reservation['length_mm'],sections=64)
            keep.apply_transform(matrix([{'translate':reservation['centre_mm']},{'rotate':reservation['rotation_deg']}]))
            for r,m in new:record('existing_cable_reservation',r['label'],overlap(keep,m))
        elif 'bounds_mm' in reservation:
            bounds=np.array(reservation['bounds_mm']);keep=trimesh.creation.box(extents=bounds[1]-bounds[0]);keep.apply_translation(bounds.mean(axis=0))
            for r,m in new:record('existing_access_reservation',r['label'],overlap(keep,m))
    outward=max(m.bounds[1,0] for r,m in printed)-122
    if outward>60:failures.append(dict(kind='outward_projection',value_mm=outward,limit_mm=60))
    if interface[5]!=0 or p['protection'].get('side_extensions_mount')!='inside':
        failures.append(dict(kind='flat_receiver_requires_inner_extensions'))
    moving=[(r,m) for r,m in new if r['label'] in moving_names]
    fixed=[(r,m) for r,m in world if r['label'] not in moving_names and r['label'] not in
           ('side_light_twist_knob','side_light_lock_bolt','side_light_lock_washer')]
    # Withdraw the whole knob/hex bolt/loose washer straight along the QR +X.
    for travel in (0,2,5,10,20,30,40,45):
        shift=dock[:3,0]*travel
        for label in ('side_light_twist_knob','side_light_lock_bolt','side_light_lock_washer'):
            m=lookup[label][1].copy();m.apply_translation(shift)
            for r,bm in world:
                if r['label'] in ('side_light_twist_knob','side_light_lock_bolt','side_light_lock_washer'):continue
                record('lock_withdrawal',label+' / '+r['label'],overlap(m,bm),travel_mm=travel)
    # The cam draws in 0.6 mm over 60 degrees; relax first, then rotate back.
    # Padded surfaces permit compression but do not permit plastic interference.
    for angle in range(0,-61,-5):
        lift=q['twist_cam_lift']*(-angle/q['turn_deg'])
        motion=dock@matrix([{'translate':[0,0,lift]},{'rotate':[0,0,angle]}])@np.linalg.inv(dock)
        for r,m in moving:
            moved=m.copy();moved.apply_transform(motion)
            for b,bm in fixed:
                record('release_rotation',r['label']+' / '+b['label'],overlap(moved,bm),angle_deg=angle,lift_mm=lift)
    for travel in (0,1,2,5,10,20,40):
        motion=dock@matrix([{'translate':[0,0,q['twist_cam_lift']+travel]},
                           {'rotate':[0,0,-q['turn_deg']]}])@np.linalg.inv(dock)
        for r,m in moving:
            moved=m.copy();moved.apply_transform(motion)
            for b,bm in fixed:record('release_lift',r['label']+' / '+b['label'],overlap(moved,bm),travel_mm=travel)
    # Tighten the two frame screws before attaching the integral light unit.
    # The four external clamp heads are accessible with a straight driver.
    tools=[]
    for j in p['fastener_joints']:
        if j.get('owner')!=TAG:continue
        label=j['label'];position=np.array(j['seat_mm']);rotation=matrix([{'rotate':j['axis_rotation_deg']}])
        length=35
        tool=trimesh.creation.cylinder(radius=4,height=length,sections=32)
        tool.apply_translation([0,0,length/2+2.05]);tool.apply_transform(rotation);tool.apply_translation(position)
        if label.startswith('side_light_frame_'):
            stage=[(r,m) for r,m in world if r['label'] not in moving_names]
        else:stage=[(r,m) for r,m in world if r['print']]
        blocked=[dict(part=r['label'],volume_mm3=overlap(tool,m)) for r,m in stage if r['print']]
        blocked=[b for b in blocked if b['volume_mm3']>.1]
        tools.append(dict(label=label,tool_diameter_mm=8,reach_mm=length,blocked=blocked))
        if blocked:failures.append(dict(kind='tool_access',**tools[-1]))
    # Store actual counts, input hashes and only nonzero clashes; routine zero
    # records are summarized so the result remains readable.
    inputs={OUT/'placement.json',Path(__file__).resolve(),PART/'child_horizontal_twist_mount.scad',
            ROOT/'scad/lib/child_horizontal_twist_interface.scad',ROOT/QR/'quick_release_prototypes.scad'}
    inputs|={ROOT/r['part']/(r['file']+'.stl') for r,m in world}
    result=dict(result='FAIL' if failures else 'PASS',printable_parts=[dict(label=r['label'],bounds_mm=m.bounds.tolist(),
        volume_mm3=float(m.volume),watertight=bool(m.is_volume)) for r,m in printed],
        checked_pairs=len(rows),placement_regeneration_idempotent=regenerated==p,nonzero_intersections=[r for r in rows if r['volume_mm3']>1e-5],
        tool_access=tools,hand_approach_regions=hand,locked_orientation=orientation,knob_full_turn_clearance=turn_clearance,
        C_contact_geometry=contact_checks,outward_projection_mm=outward,previous_outward_projection_mm=59.5,initial_outward_projection_mm=123.5,release_rotation_step_deg=5,lock_withdrawal_mm=45,normal_lift_mm=40,
        printed_stock_sha256=printed_baseline(),failures=failures,
        input_sha256={str(f.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(inputs)},
        limitations=['Discrete rigid motion, not strength, adhesion, friction or operator-force validation',
                     '33 x 81 gauge represents the confirmed reference holder, not the full light or its head',
                     'No camera/TD04A device fixture or cable/connector model is installed'])
    save(OUT/'_work/analysis/side_twist_mount/validation.json',result)
    print(json.dumps(dict(result=result['result'],parts=len(printed),checks=len(rows),failures=failures[:40]),ensure_ascii=False))
    if failures:raise RuntimeError('Accessory verification failed')

if __name__=='__main__':main()
