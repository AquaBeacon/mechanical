"""Probe the actual side accessory holes and independent key fasteners."""
import hashlib,json
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Point,Polygon
from prepare_child_horizontal_plate_frame import ROOT,OUT,load_world,matrix,overlap,save


def main():
    placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    world=load_world(placement); by_name={r['label']:m for r,m in world}
    interface=placement['attachment_interface']; dims=placement['dimensions_mm']
    failures=[]; holes=[]; keys=[]; inputs={OUT/'placement.json',Path(__file__).resolve()}
    nut_source=ROOT/'parts/common/interior/cots/screw/screw_nut_m3.stl'
    nut=trimesh.load(nut_source,force='mesh'); inputs.add(nut_source)
    for side,s in [('left',-1),('right',1)]:
        frame=by_name[side+'_side_frame']
        inside=s*(dims['width']/2-dims['side_thickness'])
        # Measure actual middle-thickness sections: distance from each hole to
        # every other opening / outer edge. This includes the six-sided pocket.
        section=frame.section(plane_origin=[inside+s*1.4,0,0],plane_normal=[1,0,0])
        loops=[Polygon(loop[:,1:3]) for loop in section.discrete]
        exterior=max(loops,key=lambda p:p.area)
        openings=[p for p in loops if p is not exterior]
        for y,z in interface['hole_centres_yz_mm']:
            shaft=trimesh.creation.cylinder(radius=1.5,height=dims['side_thickness']+.2,sections=48)
            shaft.apply_transform(matrix([{'translate':[s*(dims['width']/2-dims['side_thickness']/2),y,z]},
                                          {'rotate':[0,90,0]}]))
            fitted=nut.copy()
            fitted.apply_transform(matrix([{'translate':[inside+s*.4,y,z]},
                {'rotate':[0,s*90,0]},{'rotate':[0,0,30]}]))
            # 10 mm travel clears the 2.8 mm pocket completely and leaves the
            # nut in the existing gap between the side and ballast supports.
            nut_travel=10
            swept=trimesh.convex.convex_hull(np.vstack([fitted.vertices,fitted.vertices+[-s*nut_travel,0,0]]))
            centre=Point(y,z); pocket=next(p for p in openings if p.covers(centre))
            ligament=min([pocket.distance(exterior.exterior)]+
                          [pocket.distance(p) for p in openings if p is not pocket])
            blocked=[dict(part=r['label'],volume_mm3=overlap(swept,m)) for r,m in world
                     if r['print'] or r['group'] in ('vessel','ballast')]
            blocked=[r for r in blocked if r['volume_mm3']>.1]
            record=dict(side=side,centre_yz_mm=[y,z],shaft_interference_mm3=overlap(shaft,frame),
                nut_interference_mm3=overlap(fitted,frame),nut_insertion_travel_mm=nut_travel,nut_insertion_blocked=blocked,
                minimum_pocket_ligament_at_inner_section_mm=ligament)
            holes.append(record)
            if record['shaft_interference_mm3']>.1 or record['nut_interference_mm3']>.1 or blocked or ligament<2:
                failures.append(record)
        key=by_name[side+'_rotation_key']
        for joint in placement['fastener_joints']:
            if not joint['label'].startswith(f'key_join_{s}_'): continue
            screw=by_name[joint['label']+'_screw']
            direction=matrix([{'rotate':joint['axis_rotation_deg']}])[:3,2]
            seat=np.array(joint['seat_mm']); tip=seat-direction*joint['length_mm']
            innermost_plane=inside-s*placement['protection']['key_mount_thickness_mm']
            # Free nut/washer on the full foot; tip extends beyond the nut.
            tip_recess=s*(tip[0]-innermost_plane)
            record=dict(label=joint['label'],screw_tip_mm=tip.tolist(),tip_recess_mm=tip_recess,
                        key_interference_mm3=overlap(screw,key),frame_interference_mm3=overlap(screw,frame))
            keys.append(record)
            if (not joint.get('exposed_nut') or tip_recess>-.5-2.4
                    or record['key_interference_mm3']>.1 or record['frame_interference_mm3']>.1):
                failures.append(record)
        source=next(r for r,m in world if r['label']==side+'_rotation_key')
        inputs.add(ROOT/source['part']/(source['file']+'.stl'))
        source=next(r for r,m in world if r['label']==side+'_side_frame')
        inputs.add(ROOT/source['part']/(source['file']+'.stl'))
    if len(holes)!=2*interface['holes_per_side'] or len(keys)!=4:
        failures.append(dict(error='Incorrect accessory or key mounting count'))
    result=dict(result='FAIL' if failures else 'PASS',accessory_holes=holes,key_fasteners=keys,
        failures=failures,inputs_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in sorted(inputs)},
        note='Nut and geometric clearance only; future attachments require their own interference/load check.')
    save(OUT/'_work/analysis/side_attachments/validation.json',result)
    print(json.dumps(dict(result=result['result'],accessory_holes=len(holes),key_fasteners=len(keys),
        minimum_ligament_mm=min(h['minimum_pocket_ligament_at_inner_section_mm'] for h in holes),failures=failures),ensure_ascii=False))
    if failures: raise RuntimeError('Side attachment checks failed')


if __name__=='__main__': main()
