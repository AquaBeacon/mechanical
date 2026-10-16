"""Verify independent lower-clamp brackets against actual assembly meshes."""
import hashlib,json
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Point,Polygon
from prepare_child_horizontal_plate_frame import ROOT,OUT,load_world,matrix,overlap,save


def main():
    placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    validation=json.loads((OUT/'_work/analysis/layout/validation.json').read_text(encoding='utf-8'))
    world=load_world(placement); by_name={r['label']:m for r,m in world}
    interface=placement['clamp_support']; dims=placement['dimensions_mm']
    supports=[(r,m) for r,m in world if r.get('role')=='detachable_clamp_support']
    failures=list(validation['failures']); brackets=[]; joints=[]; sides=[]
    side_sections={}
    inputs={OUT/'placement.json',OUT/'_work/analysis/layout/validation.json',Path(__file__).resolve()}
    for side,s in [('left',-1),('right',1)]:
        frame=by_name[side+'_side_frame']; inside=s*(dims['width']/2-dims['side_thickness'])
        row=dict(side=side,dimensions_mm=frame.extents.tolist(),
                 removed_integral_arms=bool(abs(frame.extents[0]-dims['side_thickness'])<.001))
        sides.append(row)
        section=frame.section(plane_origin=[inside+s*1.4,0,0],plane_normal=[1,0,0])
        loops=[Polygon(loop[:,1:3]) for loop in section.discrete]
        exterior=max(loops,key=lambda p:p.area)
        side_sections[side]=(exterior,[p for p in loops if p is not exterior])
        if not row['removed_integral_arms']: failures.append(row)
        for item,mesh in supports:
            if not item['label'].startswith(side+'_'): continue
            source=ROOT/item['part']/(item['file']+'.stl'); inputs.add(source)
            station=float(item['label'].rsplit('_',1)[-1])
            mount=mesh.bounds[1,0] if s==1 else mesh.bounds[0,0]
            bores=[]
            x=s*abs(interface['lower_clamp_hole_x_mm'][0])
            for dy in interface['lower_clamp_hole_axial_offsets_mm']:
                screw=by_name[f'mount_lower_{int(station)}_{int(x)}_{int(dy)}_screw']
                bores.append(dict(centre_xy_mm=[x,station+dy],screw_interference_mm3=overlap(screw,mesh)))
            row=dict(label=item['label'],connected_components=len(mesh.split()),watertight=bool(mesh.is_volume),
                support_to_side_gap_mm=abs(mount-inside),support_top_z_mm=float(mesh.bounds[1,2]),
                preserved_lower_clamp_plane_z_mm=interface['lower_clamp_plane_z_mm'],clamp_mount_holes=bores)
            brackets.append(row)
            if (row['connected_components']!=1 or not row['watertight'] or row['support_to_side_gap_mm']>.001
                    or abs(row['support_top_z_mm']-interface['lower_clamp_plane_z_mm'])>.001
                    or any(b['screw_interference_mm3']>.1 for b in bores)):
                failures.append(row)
        source=next(r for r,m in world if r['label']==side+'_side_frame')
        inputs.add(ROOT/source['part']/(source['file']+'.stl'))
    for joint in placement['fastener_joints']:
        if not joint['label'].startswith('support_join_'): continue
        _,_,s,station,dy,z=joint['label'].split('_'); s=int(s); station=float(station); dy=float(dy)
        side='left' if s==-1 else 'right'
        mesh=by_name[f'{side}_clamp_support_{int(station)}']
        inside=s*(dims['width']/2-dims['side_thickness'])
        foot_inner=inside-s*interface['mounting_foot_thickness_mm']
        axis=matrix([{'rotate':joint['axis_rotation_deg']}])[:3,2]
        tip=np.array(joint['seat_mm'])-axis*joint['length_mm']
        recess=s*(tip[0]-foot_inner)
        path=next(r for r in validation['nut_insertion_paths'] if r['nut']==joint['label']+'_nut')
        driver=next(r for r in validation['driver_paths'] if r['screw']==joint['label']+'_screw')
        # The shaft corridor through the full side and foot is also probed.
        depth=dims['side_thickness']+interface['mounting_foot_thickness_mm']
        probe=trimesh.creation.cylinder(radius=1.5,height=depth,sections=48)
        probe.apply_transform(matrix([{'translate':[s*(dims['width']/2-depth/2),station+dy,float(z)]},
                                      {'rotate':[0,90,0]}]))
        interference=overlap(probe,mesh)+overlap(probe,by_name[side+'_side_frame'])
        # Full foot, no recessed hex nut. Material remains beside the shaft
        # throughout its inner face; external nut space is on the other side.
        roof_points=[[foot_inner+s*d,station+dy,float(z)+2.5] for d in [.4,3.0]]
        roof_material=[bool(v) for v in mesh.contains(roof_points)]
        exterior,openings=side_sections[side]
        bore=next(p for p in openings if p.covers(Point(station+dy,float(z))))
        ligament=min([bore.distance(exterior.exterior)]+[bore.distance(p) for p in openings if p is not bore])
        row=dict(label=joint['label'],shaft_interference_mm3=interference,screw_tip_mm=tip.tolist(),
            tip_recess_mm=recess,nut_insertion_path=path,driver_path=driver,
            roof_probe_points_mm=roof_points,roof_probe_material=roof_material,
            side_bore_ligament_at_inner_section_mm=ligament)
        joints.append(row)
        if (not joint.get('exposed_nut') or recess>-.5-2.4 or interference>.1 or path['blocked']
                or driver['blocked'] or roof_material!=[True,True] or ligament<2):
            failures.append(row)
    previous_file=OUT/'_work/intermediate/history/before_detachable_clamp_supports/assemblies/child_horizontal_plate_frame/placement.json'
    inputs.add(previous_file)
    previous=json.loads(previous_file.read_text(encoding='utf-8'))
    old={r['label']:r for r in previous['items'] if r['group']=='clamp'}
    for item in placement['items']:
        if item['group']!='clamp': continue
        if (item['part'],item['file'],item['ops'])!=(old[item['label']]['part'],old[item['label']]['file'],old[item['label']]['ops']):
            failures.append(dict(error='Clamp placement changed',label=item['label']))
    if len(brackets)!=4 or len(joints)!=16:
        failures.append(dict(error='Expected four brackets and sixteen side fastening sets'))
    report=dict(result='FAIL' if failures else 'PASS',plain_side_frames=sides,brackets=brackets,
        side_fasteners=joints,failures=failures,
        inputs_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
        note='Geometric fit and access only; printed PETG bracket and screw joints still require physical load/creep testing.')
    save(OUT/'_work/analysis/detachable_supports/validation.json',report)
    print(json.dumps(dict(result=report['result'],brackets=len(brackets),side_fasteners=len(joints),
        clamp_mount_holes=sum(len(r['clamp_mount_holes']) for r in brackets),failures=failures),ensure_ascii=False))
    if failures: raise RuntimeError('Detachable clamp support validation failed')


if __name__=='__main__': main()
