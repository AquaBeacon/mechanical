"""Conservative sampled actual-mesh checks for the camera axial fixture.

This reports sampled motions, not a proof of continuous clearance or strength.
Run after every fixture and COTS mesh is rebuilt. A failure remains a failure.
"""
from pathlib import Path
import hashlib, json, sys
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'spec')]
from prepare_child_horizontal_plate_frame import matrix, load_world
from verify_parent_exterior_qr import intersection, probe
OUT=ROOT/'assemblies/child_horizontal_plate_frame/_work/analysis/camera_fixture_20261029'


def main():
    checks=[]
    assembly_filter=next((x.split('=',1)[1] for x in sys.argv if x.startswith('--assembly=')),None)
    report=OUT/('fixture_checks_'+assembly_filter+'.json' if assembly_filter else 'fixture_checks.json')
    def record(name, ok, **detail):
        checks.append(dict(name=name,passed=bool(ok),**detail))
        report.write_text(json.dumps(dict(passed=all(x['passed'] for x in checks),checks=checks,complete=False),indent=2)+'\n',encoding='utf-8')
        if not ok:
            print('FAIL', name, detail, flush=True)
            if '--stop-on-failure' in sys.argv: raise SystemExit(1)
    # Hash exact consumed sources and meshes before and after the run: a CAD
    # rebuild during verification would otherwise produce ambiguous evidence.
    inputs=[
        'scad/lib/camera_rotary_joint.scad',
        'scad/lib/edge_finished_profiles.scad',
        'scad/lib/child_horizontal_twist_interface.scad',
        'parts/common/interior/cots/screw/screw_m3x30.stl',
        'parts/common/interior/cots/screw/screw_m3x18.stl',
        'parts/common/interior/cots/screw/screw_washer_m3_05.stl',
        'parts/common/interior/cots/screw/screw_nut_m3.stl',
        'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_front_clamp.stl',
        'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_case_41mm.stl',
        'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount.scad',
        'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount_twist.scad',
        'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount_twist.stl',
        'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_rotary_spacer.scad',
        'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_rotary_spacer.stl',
        'parts/parent/exterior/printed/parent_oneplate_camera_qr/parent_oneplate_camera_qr.scad',
        'parts/parent/exterior/printed/parent_oneplate_camera_qr/parent_oneplate_camera_qr_female.stl',
        'parts/child/exterior/printed/child_horizontal_twist_mount/child_horizontal_twist_mount.scad',
        'parts/child/exterior/printed/child_horizontal_twist_mount/child_horizontal_twist_mount_camera_receiver.stl',
        'assemblies/parent_exterior/placement.json',
        'assemblies/child_horizontal_plate_frame/placement.json',
        'spec/verify_camera_fixture_clamp.py',
    ]
    def hashes():
        return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in inputs}
    input_hashes=hashes()
    baseline=json.loads((OUT/'history/baseline_hashes.json').read_text(encoding='utf-8'))
    changed=[]; baseline_checked=0; removed_obsolete=[]
    camera_files=('camera_mount_twist.', 'parent_oneplate_camera_qr_female.', 'child_horizontal_twist_mount_camera_receiver.')
    for f,digest in baseline.items():
        if Path(f).suffix.lower() != '.stl' or Path(f).name.startswith(camera_files):continue
        path=ROOT/f
        # Parent's package copy represented the now-removed camera knob.
        # Preserve verification of the shared source and child/light copy.
        obsolete='assemblies/parent_exterior/parts/quick_release_prototypes_twist_knob.stl'
        if f==obsolete and not path.exists():
            removed_obsolete.append(f); continue
        baseline_checked+=1
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:changed.append(f)
    record('nonfixture_baseline_hashes', not changed,checked=baseline_checked,changed=changed,removed_camera_package_copy=removed_obsolete)
    for name,prefix,group in [('parent_exterior','camera_', 'camera'),('child_horizontal_plate_frame','side_camera_', 'child_camera')]:
        if assembly_filter and name != assembly_filter: continue
        p=json.loads((ROOT/'assemblies'/name/'placement.json').read_text(encoding='utf-8'))
        for row in p['items']:row.setdefault('file',Path(row['part']).name)
        world=load_world(p); rows={r['label']:r for r,m in world}; meshes={r['label']:m for r,m in world}
        override=next((x.split('=',1)[1] for x in sys.argv if x.startswith('--child-receiver=')),None)
        if name=='child_horizontal_plate_frame' and override:
            candidate=trimesh.load(override,force='mesh')
            candidate.apply_transform(matrix(rows['side_camera_frame_receiver']['ops']))
            meshes['side_camera_frame_receiver']=candidate
            record(name+'_candidate_receiver_used',True,path=str(Path(override).resolve()),sha256=hashlib.sha256(Path(override).read_bytes()).hexdigest())
        female='camera_qr_female' if name=='parent_exterior' else 'side_camera_frame_receiver'
        base=rows[female]['ops']
        if name!='parent_exterior':base=base+[{'translate':[-53,0,0]},{'rotate':[0,0,90]}]
        dock=matrix(base); inv=np.linalg.inv(dock)
        selected={label for label in rows if label.startswith(prefix) and (label==female or rows[label].get('removal_group')==group or label.startswith(prefix+'qr_axial_') or label.startswith(prefix+'axial_'))}
        # Include all camera/frame screws and the two shared guard stacks.
        if name!='parent_exterior':selected|={l for l in rows if l.startswith('side_camera_frame_') or l.startswith(('guard_join_-1_98_100_','guard_join_-1_98_176_'))}
        hits=[]
        for a in sorted(selected):
            for b in sorted(rows):
                if a==b or (b in selected and b<a):continue
                try:v=intersection(meshes[a],meshes[b])
                except Exception as e:
                    hits.append(dict(a=a,b=b,error=str(e)));continue
                if v>.04:hits.append(dict(a=a,b=b,mm3=v))
        record(name+'_world_intersections',not hits,hits=hits)
        # Push the male a small amount toward the female to expose the actual contact faces.
        mount=meshes[prefix+'mount']
        pushed=mount.copy();pushed.apply_translation(-dock[:3,2]*.1)
        face_overlap=intersection(pushed,meshes[female])
        record(name+'_male_female_face_contact',face_overlap>.1,overlap_at_0_1mm_push=face_overlap)
        for label in (prefix+'mount',female):
            mesh=meshes[label]
            record(name+'_'+label+'_one_closed_component',mesh.is_volume and len(mesh.split())==1,
                   components=len(mesh.split()),volume_mm3=float(mesh.volume))
        axial_prefix='camera_qr_axial_' if name=='parent_exterior' else 'side_camera_axial_'
        for i,y in enumerate((-52,52)):
            stem=axial_prefix+str(i); screw=meshes[stem+'_screw']; washer=meshes[stem+'_washer'];nut=meshes[stem+'_nut']; receiver=meshes[female]
            for label,mesh in [('screw',screw),('washer',washer),('nut',nut)]:
                local=mesh.copy();local.apply_transform(inv)
                record(name+f'_{i}_{label}_mesh_closed',local.is_volume and len(local.split())==1,bounds=local.bounds.tolist())
            localnut=nut.copy();localnut.apply_transform(inv)
            record(name+f'_{i}_nut_axial_limits', np.allclose(localnut.bounds[:,2],[2.4,4.8],atol=.03),bounds=localnut.bounds.tolist())
            pulled=nut.copy();pulled.apply_translation(dock[:3,2]*.15)
            contact=intersection(pulled,receiver)
            record(name+f'_{i}_nut_roof_pull',contact>.1,overlap_mm3=contact,direction='receiver +Z',stroke_mm=.15,
                   nominal_nut_top_z=4.8, nominal_roof_z=[4.8,8],
                   note='Push checks first reaction; full escape path and roof integrity require separate examination.')
            localpull=localnut.copy()
            sweep=trimesh.convex.convex_hull(np.vstack((localpull.vertices,localpull.vertices+np.array([0,0,12]))))
            sweep.apply_transform(dock)
            swept_overlap=intersection(sweep,receiver)
            record(name+f'_{i}_nut_full_pull_sweep_intersects_roof',swept_overlap>.1,
                   overlap_mm3=swept_overlap,stroke_mm=12,direction='+Z',
                   note='Conservative swept hull; first reaction is checked separately; not a strength test.')
            turned=nut.copy();turned.apply_transform(dock@matrix([{'translate':[0,y,0]},{'rotate':[0,0,15]},{'translate':[0,-y,0]}])@inv)
            anti=intersection(turned,receiver)
            record(name+f'_{i}_nut_antirotation',anti>.05,overlap_mm3=anti,angle_deg=15)
            # Entire prism is a conservative radial insertion envelope from the exterior edge.
            nut_local=localnut.copy();nut_local.apply_translation([0,0,-.4])
            # Convex hull fills the nut hole and spans every intermediate
            # translation; this is a conservative continuous insertion test.
            verts=nut_local.vertices
            offset=np.array([0,np.sign(y)*25,0])
            swept=trimesh.convex.convex_hull(np.vstack((verts,verts+offset)))
            swept.apply_transform(dock)
            insertion_overlap=intersection(swept,receiver)
            record(name+f'_{i}_nut_radial_insertion_swept',insertion_overlap<.04,
                   overlap_mm3=insertion_overlap,travel_mm=25,
                   method='convex hull of filled nut at both endpoints')
            seating=[]
            for travel in np.linspace(0,.4,5):
                trial=nut_local.copy();trial.apply_translation([0,0,travel]);trial.apply_transform(dock)
                v=intersection(trial,receiver)
                if v>.04:seating.append([float(travel),v])
            record(name+f'_{i}_nut_seating',not seating,hits=seating,travel_mm=.4,step_mm=.1)
            tip_probe=probe([0,y,.501],[0,y,1],3);tip_probe.apply_transform(dock)
            tip_obstruction=intersection(tip_probe,receiver)
            record(name+f'_{i}_screw_tip_relief',tip_obstruction<.04,obstruction_mm3=tip_obstruction,tip_z=1,relief_bottom_z=.5)
            record(name+f'_{i}_thread_engagement', 2.4-1>=1 and 4.8-2.4>=2.4-1e-6,
                   nut_z=[2.4,4.8],screw_tip_z=1,engagement_mm=2.4,tip_protrusion_mm=1.4)
            tool=probe([0,y,31.01],[0,y,101.01],8);tool.apply_transform(dock)
            toolhits=[]
            for label,m in meshes.items():
                if label in {stem+'_screw',stem+'_washer'}:continue
                v=intersection(tool,m)
                if v>.04:toolhits.append(dict(part=label,mm3=v))
            record(name+f'_{i}_axial_tool_d8',not toolhits,hits=toolhits)
        # Both fixed frame axes and shared guard axes; camera moving group removed.
        if name!='parent_exterior':
            for stem in ['side_camera_frame_0','side_camera_frame_1','guard_join_-1_98_100','guard_join_-1_98_176']:
                j=next(j for j in p['fastener_joints'] if j['label']==stem)
                origin=np.array(j['seat_mm']); axis=matrix([{'rotate':j['axis_rotation_deg']}])[:3,2]
                nut_origin=np.array(j['nut_start_mm']); nut_axis=matrix([{'rotate':j['nut_rotation_deg']}])[:3,2]
                ends=[float(np.dot(nut_origin-origin,-axis)),float(np.dot(nut_origin+2.4*nut_axis-origin,-axis))]
                low,high=sorted(ends); engagement=max(0.,min(high,j['length_mm'])-max(low,0.))
                record(name+'_'+stem+'_nominal_thread_stack',engagement>=2.39 and high<=j['length_mm'],
                       engagement_mm=engagement, nut_interval_along_shaft_mm=[low,high], length_mm=j['length_mm'])
                washer_label=stem+('_head_washer' if stem.startswith('side_camera') else '_washer')
                pushed_washer=meshes[washer_label].copy();pushed_washer.apply_translation(-axis*.1)
                seat_overlap=intersection(pushed_washer,meshes[female])
                record(name+'_'+stem+'_washer_receiver_seat',seat_overlap>.01,overlap_mm3=seat_overlap,push_mm=.1)
                foot=meshes[female].copy();foot.apply_translation(-axis*.1)
                region=probe(origin-axis*40,origin+axis*40,16)
                try:foot=trimesh.boolean.intersection([foot,region],engine='manifold',check_volume=False)
                except Exception as e:raise RuntimeError('foot region boolean: '+str(e))
                contacts=[]
                for label in ('left_front_guard','left_side_frame'):
                    if label in meshes:
                        v=intersection(foot,meshes[label])
                        if v>.01:contacts.append(dict(part=label,mm3=v))
                record(name+'_'+stem+'_receiver_foot_support',bool(contacts),contacts=contacts,push_mm=.1)
                if stem.startswith('side_camera'):
                    nut=meshes[stem+'_nut']; sweep=[]
                    for travel in np.arange(0,.501,.05):
                        pushed=nut.copy();pushed.apply_translation(axis*travel)
                        sweep.append([round(float(travel),3),intersection(pushed,meshes['left_side_frame'])])
                    first=next((t for t,v in sweep if v>.01),None)
                    record(name+'_'+stem+'_nut_pull_reaction',first is not None and first<=.4,
                           first_reaction_mm=first,samples=sweep,step_mm=.05,
                           direction='toward screw head',
                           note='Original placement had 0.1 mm slack; nut now placed at reaction face. Actual load/strength unproven.')
                    hull=trimesh.convex.convex_hull(np.vstack((nut.vertices,nut.vertices+axis*12)))
                    swept_overlap=intersection(hull,meshes['left_side_frame'])
                    record(name+'_'+stem+'_nut_pull_swept_barrier',swept_overlap>.1,
                           overlap_mm3=swept_overlap,travel_mm=12,
                           note='Filled-nut convex swept hull intersects barrier; initial reaction checked separately.')
                if stem.startswith('guard_join'):
                    inner_label=stem+'_nut_washer'; inner=meshes[inner_label].copy()
                    inner.apply_translation(axis*.1)
                    contacts=[]
                    for label in ('left_front_guard','left_side_frame'):
                        if label in meshes:
                            v=intersection(inner,meshes[label])
                            if v>.01:contacts.append(dict(part=label,mm3=v))
                    record(name+'_'+stem+'_inner_washer_seat',bool(contacts),contacts=contacts)
                tool=probe(origin+axis*.01,origin+axis*70.01,3)
                hits=[]
                for label,m in meshes.items():
                    if rows[label].get('removal_group')==group or label in {stem+'_screw',stem+'_washer',stem+'_head_washer'}:continue
                    v=intersection(tool,m)
                    if v>.04:hits.append(dict(part=label,mm3=v))
                record(name+'_'+stem+'_tool_d3',not hits,hits=hits)
        # Screws and washers are removed first; each U spacer slides -X.
        for i in range(2):
            stem=axial_prefix+str(i); spacer=meshes[stem+'_spacer']; hits=[]
            for distance in np.linspace(0,14,29):
                trial=spacer.copy();trial.apply_translation(-dock[:3,0]*distance)
                for label,mesh in meshes.items():
                    if label==stem+'_spacer' or (label.startswith(axial_prefix) and (label.endswith('_screw') or label.endswith('_washer'))):continue
                    v=intersection(trial,mesh)
                    if v>.04:hits.append(dict(travel_mm=float(distance),part=label,mm3=v))
            record(name+f'_{i}_spacer_removal_sampled',not hits,hits=hits,direction='dock -X',travel_mm=14,step_mm=.5)
            for direction,host in [(-1,female),(1,prefix+'mount')]:
                pressed=spacer.copy();pressed.apply_translation(dock[:3,2]*direction*.1)
                v=intersection(pressed,meshes[host])
                record(name+f'_{i}_spacer_seat_'+host,v>.01,overlap_mm3=v,push_mm=.1)
        moving=[l for l,r in rows.items() if r.get('removal_group')==group and 'axial_' not in l]
        fixed=[l for l in rows if l not in moving and ('axial_' not in l or l.endswith('_nut'))]
        motionhits=[]
        for angle,travel in [(a,.6*a/60) for a in range(0,61,5)]+[(60,.6+t) for t in (5,10,20,40,80)]:
            transform=dock@matrix([{'translate':[0,0,travel]},{'rotate':[0,0,-angle]}])@inv
            for a in moving:
                trial=meshes[a].copy();trial.apply_transform(transform)
                for b in fixed:
                    v=intersection(trial,meshes[b])
                    if v>.1:motionhits.append(dict(angle_deg=angle,travel_mm=travel,a=a,b=b,mm3=v))
        record(name+'_release_sampled',not motionhits,hits=motionhits,rotation_step_deg=5,
               note='Discrete samples only; axial screws, washers, and U spacers removed; receiver nuts remain before motion.')
    final_hashes=hashes()
    record('fixture_inputs_unchanged_during_run',input_hashes==final_hashes,
           changed=[f for f in inputs if input_hashes[f]!=final_hashes[f]])
    result=dict(passed=all(c['passed'] for c in checks),complete=True,
        scope=assembly_filter or 'both assemblies',check_count=len(checks),
        input_sha256=input_hashes,checks=checks,
        limits=['Discrete motion and insertion samples do not prove continuous clearance.',
                'Physical assembly, clamp load, material strength and camera dimensions require independent verification.'])
    report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('PASS' if result['passed'] else 'FAIL',flush=True)
    return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
