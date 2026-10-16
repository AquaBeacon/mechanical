"""Verify exposed nut access, screw alternatives, octagonal bores and printed stock."""
import hashlib,json
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Point,Polygon
from prepare_child_horizontal_plate_frame import ROOT,OUT,PART,load_world,matrix,overlap,save,printed_baseline


def main():
    placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    world=load_world(placement);by_name={r['label']:(r,m) for r,m in world}
    failures=[];access=[];alternatives=[];holes=[];pads=[]
    locked=printed_baseline()
    previous=json.loads((OUT/'_work/intermediate/history/before_open_nut_fastening/assemblies/child_horizontal_plate_frame/placement.json').read_text(encoding='utf-8'))
    old={r['label']:r for r in previous['items']}
    for row,mesh in world:
        if (ROOT/row['part']/(row['file']+'.stl')).relative_to(ROOT).as_posix() not in locked: continue
        if (row['part'],row['file'],row['ops'])!=(old[row['label']]['part'],old[row['label']]['file'],old[row['label']]['ops']):
            failures.append(dict(error='Printed stock placement changed',label=row['label']))
    layout=json.loads((OUT/'_work/analysis/layout/validation.json').read_text(encoding='utf-8'))
    failures.extend(layout['failures'])
    for joint in placement['fastener_joints']:
        if not joint.get('exposed_nut') or joint.get('owner')=='side_twist_accessory': continue
        label=joint['label'];s=int(label.split('_')[2]);nut=by_name[label+'_nut'][1]
        axis=matrix([{'rotate':joint['nut_rotation_deg']}])[:3,2]
        if label.startswith('support_join_'):
            dy=float(label.split('_')[4]);entry=np.array([0,np.sign(dy),0])
            target=('left' if s==-1 else 'right')+'_clamp_support_'+label.split('_')[3]
            lengths=[25,30];pad_depth=8
        elif label.startswith('key_join_'):
            entry=np.array([0,1,0]);target=('left' if s==-1 else 'right')+'_rotation_key'
            lengths=[25,30];pad_depth=8
        elif label.startswith('guard_join_'):
            y=float(label.split('_')[3]);entry=np.array([0,np.sign(y),0])
            target=('left' if s==-1 else 'right')+('_front_guard' if y>0 else '_rear_guard')
            lengths=[25,30];pad_depth=8
        else:
            entry=np.array([0,0,1]);target='removable_upper_frame';lengths=[30,40];pad_depth=12
        # Conservative solid envelope of a thin open-ended spanner head/handle.
        # Own nut/shaft are excluded: the actual jaw is open. Width10, thickness
        #2.6 are assumed maximum tool dimensions, to be checked on the real tool.
        centre=np.array(joint['nut_start_mm'])+axis*1.2
        across=np.cross(axis,entry)
        corners=np.array([centre+axis*a+entry*b+across*c
                          for a in [-1.3,1.3] for b in [-5,35] for c in [-5,5]])
        tool=trimesh.convex.convex_hull(corners)
        blocked=[dict(part=r['label'],volume_mm3=overlap(tool,m)) for r,m in world
                 if not r['label'].startswith(label+'_')]
        blocked=[r for r in blocked if r['volume_mm3']>.1]
        record=dict(label=label,entry_direction=entry.tolist(),head_width_mm=10,
                    thickness_mm=2.6,handle_reach_mm=35,blocked=blocked)
        access.append(record)
        if blocked: failures.append(record)
        # Solid pad beside the octagonal shaft: no sunk nut seat within the pad.
        bearing=np.array(joint['nut_start_mm'])-axis*.5
        points=[bearing-axis*d+across*2.5 for d in [.4,pad_depth-.4]]
        material=by_name[target][1].contains(points).tolist()
        pads.append(dict(label=label,pad_depth_mm=pad_depth,material_probe=material))
        if material!=[True,True]: failures.append(pads[-1])
        for length in lengths:
            source=ROOT/f'parts/common/interior/cots/screw/screw_m3x{length}.stl'
            screw=trimesh.load(source,force='mesh')
            screw.apply_transform(matrix([{'translate':joint['seat_mm']},{'rotate':joint['axis_rotation_deg']}]))
            blocked=[dict(part=r['label'],volume_mm3=overlap(screw,m)) for r,m in world
                     if r['label']!=label+'_screw']
            blocked=[r for r in blocked if r['volume_mm3']>.1]
            outward=matrix([{'rotate':joint['axis_rotation_deg']}])[:3,2]
            tip=np.array(joint['seat_mm'])-outward*length
            protrusion=float((tip-(np.array(joint['nut_start_mm'])+axis*2.4))@axis)
            record=dict(label=label,length_mm=length,protrusion_beyond_nut_mm=protrusion,blocked=blocked)
            alternatives.append(record)
            if blocked or protrusion<.5: failures.append(record)
    z=placement['dimensions_mm']['tube_center_z']
    top_z=z+62.8
    checks=[('top','removable_upper_frame',[20,-70,top_z+5],[0,0,1]),
            ('support_mount','left_clamp_support_-60',[-20,-70,73],[0,0,1]),
            ('support_side','left_clamp_support_-60',[-108,-70,42],[1,0,0]),
            ('key','left_rotation_key',[-108,-98,142],[1,0,0]),
            ('front_guard','left_front_guard',[-106,98,100],[1,0,0]),
            ('rear_guard','left_rear_guard',[-106,-98,100],[1,0,0]),
            ('ballast_cap','ballast_cap_-54_-24',[-22,-24,40.55],[0,0,1])]
    for name,label,point,normal in checks:
        mesh=by_name[label][1];section=mesh.section(plane_origin=point,plane_normal=normal)
        indices=[0,1] if normal[2] else [1,2]
        centre=np.array(point)[indices]
        loops=[] if section is None else [Polygon(loop[:,indices]).simplify(1e-4) for loop in section.discrete]
        candidates=[p for p in loops if p.covers(Point(centre))]
        polygon=min(candidates,key=lambda p:p.area) if candidates else None
        if polygon is None:
            failures.append(dict(error='Bore section missing',label=label));continue
        vertices=np.asarray(polygon.exterior.coords)[:-1]
        flat_d=2*polygon.exterior.distance(Point(centre))
        row=dict(feature=name,label=label,sides=len(vertices),inscribed_diameter_mm=float(flat_d))
        holes.append(row)
        if len(vertices)!=8 or abs(flat_d-3.5)>.001: failures.append(row)
    ligaments=[]
    for label,origin,direction in [
            ('left_clamp_support_-60',[-95,-70,20],[0,0,1]),
            ('left_rotation_key',[-95,-98,100],[0,0,1]),
            ('removable_upper_frame',[-91,-110,top_z+5],[0,1,0])]:
        mesh=by_name[label][1]
        hits,_,_=mesh.ray.intersects_location([origin],[direction])
        distances=np.sort((hits-np.array(origin))@np.array(direction))
        distances=distances[np.r_[True,np.diff(distances)>1e-4]]
        thicknesses=np.diff(distances)[::2] if len(distances)%2==0 else np.array([])
        row=dict(label=label,origin_mm=origin,direction=direction,
                 material_intervals_mm=thicknesses.tolist(),minimum_at_probe_mm=float(min(thicknesses)) if len(thicknesses) else 0)
        ligaments.append(row)
        if row['minimum_at_probe_mm']<2: failures.append(row)
    if len(access)!=32: failures.append(dict(error='Expected32 exposed nut fastening sets',actual=len(access)))
    report=dict(result='FAIL' if failures else 'PASS',printed_source_sha256=locked,
        spanner_envelopes=access,alternative_screws=alternatives,solid_bearing_pads=pads,
        octagonal_hole_sections=holes,local_access_ligament_probes=ligaments,failures=failures,
        tool_assumption='5.5 mm open-ended spanner, maximum head width10 mm/thickness2.6 mm/handle reach35 mm; confirm real tool. Geometric access only.',
        limitations=['No material strength or PETG creep certification','Printed parts keep their existing round bores and nut pockets'],
        input_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [OUT/'placement.json',Path(__file__).resolve(),PART/'child_horizontal_plate_frame.scad']+
                sorted({ROOT/r['part']/(r['file']+'.stl') for r,m in world})})
    save(OUT/'_work/analysis/open_nut_fastening/validation.json',report)
    print(json.dumps(dict(result=report['result'],free_nuts=len(access),screw_alternatives=len(alternatives),
        polygon_sections=holes,failures=failures),ensure_ascii=False))
    if failures: raise RuntimeError('Exposed nut/printed stock verification failed')


if __name__=='__main__': main()
