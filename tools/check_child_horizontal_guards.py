"""Check tab capture, lift-in access and end protection using actual meshes."""
from pathlib import Path
import hashlib,json
import numpy as np
import trimesh
from prepare_child_horizontal_plate_frame import OUT,ROOT,load_world,matrix,overlap,save

placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
world=load_world(placement)
vendor=json.loads((OUT/'_work/analysis/guards/vendor_profile.json').read_text(encoding='utf-8'))
cap=next(m for r,m in world if r['label']=='end_cap_bottom')
dome=next(m for r,m in world if r['label']=='dome_top')
rear=[(r,m) for r,m in world if r['label'].endswith(('rear_guard','rotation_key'))]
printed=[(r,m) for r,m in world if r['print']]
vessel=[(r,m) for r,m in world if r['group']=='vessel']
z=placement['dimensions_mm']['tube_center_z'];protection=placement['protection']
failures=[];rotation=[];lift=[];tools=[]
inner_extensions=[]
for row,mesh in world:
    if row.get('role')!='side_frame_extension':continue
    sign=-1 if row['label'].startswith('left') else 1
    expected=np.array([-110,-102] if sign<0 else [102,110])
    record=dict(label=row['label'],source_variant=row['file'],x_bounds_mm=mesh.bounds[:,0].tolist(),
                expected_x_bounds_mm=expected.tolist())
    inner_extensions.append(record)
    if not row['file'].endswith('_inner') or np.max(np.abs(mesh.bounds[:,0]-expected))>1e-4:
        failures.append(record)
if len(inner_extensions)!=4:failures.append(dict(error='Expected four inside extensions'))
for angle in [0,.25,-.25,.5,-.5,1,-1,2,-2,5,-5,10,-10,180]:
    test=cap.copy();test.apply_transform(matrix([{'translate':[0,0,z]},{'rotate':[0,angle,0]},{'translate':[0,0,-z]}]))
    volumes=[overlap(test,m) for r,m in rear];total=sum(volumes)
    rotation.append(dict(angle_deg=angle,interference_mm3=total,receiver_volumes_mm3=volumes))
    if angle in (0,180) and total>.1:failures.append(rotation[-1])
    if abs(angle) in (5,10) and total<=.1:failures.append(dict(error='Tab key does not resist roll',**rotation[-1]))
for height in [0,.5,1,2,5,10,20,40,80,100]:
    volumes=[]
    for row,mesh in vessel:
        test=mesh.copy();test.apply_translation([0,0,height])
        volumes.append(dict(part=row['label'],interference_mm3=sum(overlap(test,m) for r,m in rear)))
    total=sum(row['interference_mm3'] for row in volumes)
    lift.append(dict(vertical_lift_mm=height,interference_mm3=total,vessel_components=volumes))
    if total>.1:failures.append(lift[-1])
for label,positions,radius,length in [('M3_driver',vendor['cap_screws_xz_mm'],4,35),
        ('M10_tool_provisional',vendor['penetrators_xz_mm'],15,35),
        ('penetrator_provisional',vendor['penetrators_xz_mm'],13,26)]:
    for index,(x,dz) in enumerate(positions):
        test=trimesh.creation.cylinder(radius=radius,height=length,sections=48)
        test.apply_transform(matrix([{'translate':[x,protection['cap_outer_y']-.2-length/2,z+dz]},{'rotate':[90,0,0]}]))
        blocked=[dict(part=r['label'],interference_mm3=overlap(test,m)) for r,m in printed]
        blocked=[r for r in blocked if r['interference_mm3']>.1]
        record=dict(label=label,index=index+1,diameter_mm=2*radius,length_mm=length,blocked=blocked)
        tools.append(record)
        if blocked:failures.append(record)
front_clear=protection['front_tip_y']-float(dome.bounds[1,1])
cable_end=protection['cap_outer_y']-protection['cable_reserved_length_mm']
rear_clear=cable_end-protection['rear_tip_y']
if front_clear<12 or rear_clear<12:failures.append(dict(front_clear_mm=front_clear,rear_clear_mm=rear_clear))
result=dict(status='fit_prototype',front_clearance_to_existing_reference_dome_mm=front_clear,
    inside_extensions=inner_extensions,
    rear_clearance_after_cable_reservation_mm=rear_clear,roll_capture=rotation,vertical_cap_entry=lift,
    cap_tools_and_provisional_connectors=tools,failures=failures,
    inputs_sha256={str(path.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [OUT/'placement.json',OUT/'_work/analysis/guards/vendor_profile.json']+
            [ROOT/r['part']/(r['file']+'.stl') for r,m in world if r['print'] or r['group']=='vessel']},
    cap_sha256=hashlib.sha256((ROOT/next(r['part'] for r,m in world if r['label']=='end_cap_bottom')/'WTE4-M-END-CAP-5XM10-R2.stl').read_bytes()).hexdigest(),
    notes=['50 mm cable reservation confirmed by user 2026-10-08',
           '180 degree reversal remains possible because original tabs are symmetric',
           'Dome is the existing reference model; actual dome height and cable bend radii remain to measure',
           'Rigid-mesh geometric capture is not a torque or impact strength rating'])
save(OUT/'_work/analysis/guards/functional_validation.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2) if failures else json.dumps(dict(result='GUARDS_PASS',front_clear_mm=front_clear,rear_clear_mm=rear_clear,roll_checks=len(rotation),lift_checks=len(lift),tool_checks=len(tools))))
if failures:raise RuntimeError('Guard functional checks failed')
