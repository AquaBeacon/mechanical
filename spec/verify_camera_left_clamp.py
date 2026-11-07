"""Check 41 mm clamp contact, nut retention, tools and both assemblies."""
from pathlib import Path
import json,sys,hashlib,itertools
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'spec'))
from prepare_child_horizontal_plate_frame import load_world,matrix
from verify_parent_exterior_qr import intersection,probe
P=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
OUT=P/'_work/analysis/clamp_clearance_20261026'

def box(lo,hi):
    lo,hi=np.array(lo),np.array(hi);m=trimesh.creation.box(hi-lo);m.apply_translation((lo+hi)/2);return m

def main():
    checks=[]
    def check(name,passed,**data):checks.append(dict(name=name,passed=bool(passed),**data))
    meshes={s:trimesh.load(P/(s+'.stl'),force='mesh') for s in ['camera_mount_twist','camera_front_clamp','camera_case_41mm']}
    mount,jaw,case=(meshes[n] for n in meshes)
    for n,m in meshes.items():check('closed_'+n,m.is_volume and len(m.split())==1,bounds=m.bounds.tolist())
    baseline=trimesh.load(OUT/'history'/P.relative_to(ROOT)/'camera_mount_twist.stl',force='mesh')
    # Original unnotched jaw is the shape reference, shifted toward front-view right.
    original=P/'_work/analysis/clamp_right20_20261026/history'/P.relative_to(ROOT)/'camera_front_clamp.stl'
    old_jaw=trimesh.load(original,force='mesh');old_jaw.apply_translation([-12,0,0])
    delta=abs(old_jaw.volume)+abs(jaw.volume)-2*intersection(old_jaw,jaw)
    check('right_12mm_no_notch',abs(delta)<.1,symmetric_difference_mm3=float(delta))
    fingers=trimesh.boolean.intersection([mount,box([-16,-8,8.01],[16,8,31.1])],engine='manifold')
    gap=float(jaw.bounds[0,0]-fingers.bounds[1,0])
    check('separate_from_M5_fixture',gap>=2.84,projected_x_gap_mm=gap)
    for label,lo,hi in [('C_interface',[-30,-65,10],[30,-31.51,70]),('M5_fingers',[-16,-8,8.01],[16,8,31.1])]:
        region=box(lo,hi)
        a=trimesh.boolean.intersection([mount,region],engine='manifold',check_volume=False)
        b=trimesh.boolean.intersection([baseline,region],engine='manifold',check_volume=False)
        delta=max(0,abs(a.volume)+abs(b.volume)-2*intersection(a,b))
        check('unchanged_'+label,delta<.05,symmetric_difference_mm3=float(delta))
    for name,a,b in [('case_mount',case,mount),('case_front',case,jaw),('jaw_mount',jaw,mount)]:
        v=intersection(a,b);check(name,v<.03,mm3=v)
    v=intersection(mount,box([22.5,-23.4,40.5],[47.5,-20.49,68]))
    check('projecting_rear_pad_removed',v<.01,mm3=v)
    for side in [-1,1]:
        v=intersection(mount,box([side*32-6,-23.44,8.001],[side*32+6,-3.45,36.501]))
        check('rear_keepout_'+str(side),v<.01,mm3=v)
        region=box([side*32-6,0,8.01],[side*32+6,8,36.5])
        v=intersection(mount,region)
        check('old_bottom_support_removed_'+str(side),v<.01,mm3=v)
        v=intersection(mount,probe([side*25,0,24],[side*60,0,24],12))
        check('M5_driver_'+str(side),v<.01,mm3=v)
    for name,m,y in [('rear',mount,-23.45),('front',jaw,17.55)]:
        pts=([[x,y,z] for x in [25,32] for z in [43,50,60,65]]+[[12,y,65]] if name=='rear' else [[x,y,z] for x in [12,20,28,33] for z in [43,50,60,65]])
        d=trimesh.proximity.closest_point(m,pts)[1]
        check(name+'_contact',max(d)<.01,max_distance_mm=float(max(d)))
    for angle in [-.5,.5]:
        c=case.copy();c.apply_transform(matrix([{'translate':[0,0,24]},{'rotate':[angle,0,0]},{'translate':[0,0,-24]}]))
        v=intersection(c,mount)+intersection(c,jaw)
        check('geometric_rotation_stop_'+str(angle),v>.1,interference_mm3=v)
    screw_dir=ROOT/'parts/common/interior/cots/screw'
    for x in [16.5,29.5]:
        washer=trimesh.load(screw_dir/'screw_washer_m4_08.stl',force='mesh')
        washer.apply_translation([x,11.5,4]);pushed=washer.copy();pushed.apply_translation([0,0,.1])
        v=intersection(pushed,mount)
        check(f'recessed_head_reaction_{x}',v>.5,washer_seat_z=4.8,head_bottom_z=0,roof_web_mm=3.2,mm3=v)
        nut=trimesh.load(screw_dir/'screw_nut_m4.stl',force='mesh')
        nut.apply_transform(matrix([{'translate':[x,11.5,10.6]},{'rotate':[0,0,30]}]))
        v=intersection(nut,mount)+intersection(nut,jaw);check(f'nut_fit_{x}',v<.01,mm3=v)
        pulled=nut.copy();pulled.apply_translation([0,0,-.2]);v=intersection(pulled,jaw)
        check(f'nut_axial_roof_{x}',v>.5,pull_direction='-Z',seat_z=10.6,mm3=v)
        swept=nut.copy();swept.apply_transform(matrix([{'translate':[x,11.5,0]},{'rotate':[0,0,15]},{'translate':[-x,-11.5,0]}]));v=intersection(swept,jaw)
        check(f'nut_antirotation_{x}',v>.1,mm3=v)
        insertion=trimesh.creation.cylinder(radius=7/(2*np.cos(np.pi/6)),height=15.399,sections=6)
        insertion.apply_transform(matrix([{'translate':[x,11.5,18.3005]},{'rotate':[0,0,30]}]))
        check(f'nut_insertion_from_above_{x}',intersection(insertion,jaw)<.01)
        check(f'bolt_stack_{x}',4+16>13.8 and 4+16<36.5,seat_z=4,nut_range=[10.6,13.8],tip_z=20,engagement_mm=3.2)
        for travel in [0,1.5,3]:
            moving=jaw.copy();moving.apply_translation([0,travel,0])
            check(f'jaw_adjustment_{x}_{travel}',intersection(moving,mount)<.01)
    collisions=[];tool_hits=[];motion_hits=[]
    for name,prefix in [('parent_exterior','camera_'),('child_horizontal_plate_frame','side_camera_')]:
        p=json.loads((ROOT/'assemblies'/name/'placement.json').read_text(encoding='utf-8'))
        for row in p['items']:row.setdefault('file',Path(row['part']).name)
        world=load_world(p)
        selected={prefix+'mount',prefix+'case_reference',prefix+'front_clamp'}|{r['label'] for r,m in world if r.get('revision_owner')=='left_clamp_20261025'}
        for (a,am),(b,bm) in itertools.combinations(world,2):
            if a['label'] not in selected and b['label'] not in selected:continue
            v=intersection(am,bm)
            if v>.04:collisions.append(dict(assembly=name,a=a['label'],b=b['label'],mm3=v))
        pose=matrix(next(r for r,m in world if r['label']==prefix+'mount')['ops'])
        lookup={r['label']:(r,m) for r,m in world}
        group='camera' if name=='parent_exterior' else 'child_camera'
        moving=[(r,m) for r,m in world if r.get('removal_group')==group]
        if name=='parent_exterior':
            dock=matrix(lookup['camera_qr_female'][0]['ops'])
            locks={'camera_qr_lock_bolt','camera_qr_lock_washer','camera_qr_knob'}
        else:
            station=p['side_twist_mount']['stations']['left_front']
            dock=matrix([{'translate':station['origin_mm']},{'rotate':station['rotation_deg']},
                         {'translate':[-35,0,0]},{'rotate':[0,0,90]}])
            locks={'side_camera_lock_bolt','side_camera_lock_washer','side_camera_twist_knob'}
        fixed=[(r,m) for r,m in world if r.get('removal_group')!=group and r['label'] not in locks]
        for angle,travel in [(a,.6*a/60) for a in range(0,61,5)]+[(60,.6+t) for t in [5,10,20,40,80]]:
            transform=dock@matrix([{'translate':[0,0,travel]},{'rotate':[0,0,-angle]}])@np.linalg.inv(dock)
            for r,m in moving:
                swept=m.copy();swept.apply_transform(transform)
                for b,bm in fixed:
                    v=intersection(swept,bm)
                    if v>.1:motion_hits.append(dict(assembly=name,angle=angle,travel=travel,a=r['label'],b=b['label'],mm3=v))
        for travel in [0,5,10,20,30,45]:
            for label in locks:
                swept=lookup[label][1].copy();swept.apply_translation(dock[:3,0]*travel)
                for b,bm in world:
                    if b['label'] in locks:continue
                    v=intersection(swept,bm)
                    if v>.1:motion_hits.append(dict(assembly=name,lock_travel=travel,a=label,b=b['label'],mm3=v))
        for x in [16.5,29.5]:
            tool=probe([x,11.5,-80],[x,11.5,-.01],4);tool.apply_transform(pose)
            for r,m in world:
                v=intersection(tool,m)
                if v>.04:tool_hits.append(dict(assembly=name,tool_x=x,part=r['label'],mm3=v))
    check('assembly_collisions',not collisions,collisions=collisions)
    check('clamp_screw_tools',not tool_hits,hits=tool_hits)
    check('C_release_and_lock_paths',not motion_hits,hits=motion_hits)
    front=max(mount.bounds[1,1],jaw.bounds[1,1])
    check('compact_front_extent',front<29.51,front_y_mm=float(front),previous_front_y_mm=45.4914,
          reduction_mm=float(45.4914-front))
    result=dict(passed=all(c['passed'] for c in checks),checks=checks,
        hashes={n:hashlib.sha256((P/(n+'.stl')).read_bytes()).hexdigest() for n in meshes},
        limits=['Case thickness 41 mm measured; width 95 mm, height and axis offset provisional.',
                'Rotation stop is a rigid geometry test, not a physical holding-load certification.',
                'M4 sliding-foot retention uses bolt preload/friction; wet slip, creep and strength require testing.'])
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'geometry_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
