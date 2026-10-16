"""Check actual B hole axes, saved fasteners and bottom-frame nut pockets."""
import hashlib,json
from pathlib import Path
import numpy as np
import trimesh
from prepare_child_horizontal_plate_frame import ROOT,OUT,load_world,overlap,save

placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
reference=json.loads((OUT/'_work/analysis/ballast_mount/reference.json').read_text(encoding='utf-8'))
layout=json.loads((OUT/'_work/analysis/layout/validation.json').read_text(encoding='utf-8'))
world=load_world(placement);by_name={r['label']:(r,m) for r,m in world}
bottom=by_name['lowest_ballast_frame'][1]
from shapely.geometry import Polygon
section=bottom.section(plane_origin=[0,0,2],plane_normal=[0,0,1])
loops=[Polygon(loop[:,:2]) for loop in section.discrete]
outer=max(loops,key=lambda p:p.area)
def hole_at(x,y):
    near=[p for p in loops if np.linalg.norm(np.array(p.centroid.coords[0])-[x,y])<.01]
    assert len(near)==1,(x,y,len(near))
    return near[0]
service=[hole_at(x,y) for x in [-20,20] for y in [-70,-50,50,70]]
mouth_section=bottom.section(plane_origin=[0,0,.01],plane_normal=[0,0,1])
mouth_loops=[Polygon(loop[:,:2]) for loop in mouth_section.discrete]
def mouth_at(x,y):
    near=[p for p in mouth_loops if np.linalg.norm(np.array(p.centroid.coords[0])-[x,y])<.01]
    assert len(near)==1,(x,y,len(near))
    return near[0]
mouth_service=[mouth_at(x,y) for x in [-20,20] for y in [-70,-50,50,70]]
plates=[(r,m) for r,m in world if r['label'].startswith('ballast_plate_')]
failures=[];checks=[]
assert len(plates)==4 and all(r['file']=='ballast_plate_b' and r['mass_g']==60 for r,m in plates)
assert placement['ballast']['example_A_count']==0 and placement['ballast']['example_B_count']==4
for row,plate in plates:
    y=float(row['ops'][0]['translate'][1])
    for x,_,diameter in reference['holes_xyd_mm']:
        label=f'plate_mount_{x}_{int(y)}'
        screw=by_name[label+'_screw'][1];nut=by_name[label+'_nut'][1];washer=by_name[label+'_washer'][1]
        probe=trimesh.creation.cylinder(radius=2.5,height=11,sections=64)
        probe.apply_translation([x,y,5.5])
        interference=overlap(probe,bottom)+overlap(probe,plate)
        # The generic cut includes a 0.1 mm Boolean allowance above nominal 4.4.
        points=[[x+3.4,y,4.45],[x+3.4,y,4.55]]
        material=bottom.contains(points).tolist()
        pocket=hole_at(x,y)
        ligament=min(pocket.distance(other) for other in service)
        # Both 45-degree entrance chamfers widen by at most 0.01 below this slice.
        mouth_ligament_bound=min(mouth_at(x,y).distance(other) for other in mouth_service)-.02
        edge_ligament=pocket.distance(outer.exterior)
        check=dict(plate=row['label'],hole_x_mm=x,y_mm=y,
            hole_d_mm_provisional=diameter,shaft_interference_mm3=interference,
            nut_roof_probe_z_mm=[4.45,4.55],material_at_roof_probes=material,
            nut_to_service_hole_ligament_mm=ligament,nut_to_outer_edge_ligament_mm=edge_ligament,
            chamfer_mouth_ligament_lower_bound_mm=mouth_ligament_bound,
            screw_tip_z_mm=float(screw.bounds[0,2]),nut_z_mm=nut.bounds[:,2].tolist(),
            washer_z_mm=washer.bounds[:,2].tolist())
        checks.append(check)
        if (interference>.1 or material!=[False,True] or ligament<2 or mouth_ligament_bound<1.5 or edge_ligament<2 or screw.bounds[0,2]<-.001
                or nut.bounds[0,2]<0 or abs(washer.bounds[0,2]-plate.bounds[1,2])>.001):
            failures.append(check)
base_joints={j['label'] for j in placement['fastener_joints'] if j.get('owner')!='side_twist_accessory'}
assert len(checks)==16
assert {r['screw'].removesuffix('_screw') for r in layout['driver_paths']}==base_joints
assert {r['nut'].removesuffix('_nut') for r in layout['nut_insertion_paths']}==base_joints
if layout['failures']:failures.extend(layout['failures'])
inputs=[OUT/'placement.json',OUT/'_work/analysis/ballast_mount/reference.json',Path(__file__).resolve()]
inputs+=[ROOT/r['part']/(r['file']+'.stl') for r,m in world if
    r['label']=='lowest_ballast_frame' or r['label'].startswith(('ballast_plate_','plate_mount_'))]
save(OUT/'_work/analysis/ballast_mount/validation.json',dict(status='fit_prototype',
    result='FAIL' if failures else 'PASS',plates=4,fasteners=16,checks=checks,failures=failures,
    minimum_roof_thickness_mm=3.5,inputs_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
    notes=['Actual B hole diameter remains unmeasured; existing CAD uses provisional 5.5 mm',
           'Nominal nut pocket 4.4 mm plus 0.1 mm cutting allowance; nut has 0.1 mm axial assembly clearance',
           'CAD geometric checks do not qualify printed PETG retention or creep']))
print('BALLAST_MOUNTS_FAIL' if failures else f'BALLAST_MOUNTS_PASS: B4, M5x12 16 sets, {len(base_joints)} base driver/nut paths; accessories checked separately')
if failures:raise RuntimeError(json.dumps(failures,indent=2))
