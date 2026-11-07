import os
"""Camera hand-release geometric regression; samples, not physical proof."""
from pathlib import Path
import sys, json, math, hashlib
import numpy as np, trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'spec')]
from prepare_child_horizontal_plate_frame import matrix,load_world
from verify_parent_exterior_qr import intersection

def overlap(a,b):
 if np.any(a.bounds[1]<b.bounds[0]) or np.any(b.bounds[1]<a.bounds[0]):return 0.
 return float(intersection(a,b))
def finger_envelope(x,y,z,side,diverge=0):
 axis=np.array([diverge,side,0.],float);axis/=np.linalg.norm(axis)
 body=trimesh.creation.revolve([[0,0],[4.5,0],[8,8],[8,25],[0,25]])
 body.apply_transform(trimesh.geometry.align_vectors([0,0,1],axis));body.apply_translation([x,y,z])
 tip=trimesh.creation.icosphere(subdivisions=2,radius=4.5);tip.apply_translation([x,y,z])
 return body,tip
def run(name):
 p=json.loads((ROOT/'assemblies'/name/'placement.json').read_text(encoding='utf-8'))
 for r in p['items']:r.setdefault('file',Path(r['part']).name)
 world=load_world(p);rows={r['label']:r for r,m in world};meshes={r['label']:m for r,m in world}
 inputs={ROOT/'assemblies'/name/'placement.json', ROOT/'scad/lib/camera_rotary_joint.scad',Path(__file__).resolve()}
 for r,m in world:
  target=ROOT/r['part']/(r['file']+'.stl')
  if target.is_file():inputs.add(target)
 for folder in ['parts/child/exterior/printed/dji_osmo_action6_mount_m3','parts/parent/exterior/printed/parent_oneplate_camera_qr','parts/child/exterior/printed/child_horizontal_twist_mount']:
  inputs.update((ROOT/folder).glob('*.scad'))
 def hash_inputs():return {str(q.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(inputs)}
 before=hash_inputs()
 pre='camera_qr_axial_' if name=='parent_exterior' else 'side_camera_axial_'
 female='camera_qr_female' if name=='parent_exterior' else 'side_camera_frame_receiver'
 mount='camera_mount' if name=='parent_exterior' else 'side_camera_mount'
 base=rows[female]['ops']+([] if name=='parent_exterior' else [{'translate':[-53,0,0]},{'rotate':[0,0,90]}])
 dock=matrix(base);inv=np.linalg.inv(dock); checks=[]
 def record(label,hits,**kw):
  ok=not hits;checks.append(dict(name=label,passed=ok,hits=hits,**kw))
  print(name,label,'PASS' if ok else 'FAIL',len(hits),flush=True)
 def coll(a,skip,transforms=None):
  hits=[]
  for label,b0 in meshes.items():
   if label in skip:continue
   b=b0.copy() if transforms and label in transforms else b0
   if transforms and label in transforms:b.apply_translation(transforms[label])
   v=overlap(a,b)
   if v>.04:hits.append(dict(part=label,mm3=round(v,6)))
  return hits
 record('receiver_installed_clearance',coll(meshes[female],{female}))
 for i,side in [(0,-1),(1,1)]:
  stem=pre+str(i);members={stem+'_'+s for s in ('screw','knob','knob_cap')};spacer=stem+'_spacer';nut=stem+'_nut'; y=side*52
  for lab in [*members,spacer,nut,female,mount]:
   m=meshes[lab];record(f'{i}_{lab}_closed',[] if m.is_volume and len(m.split())==1 else [lab])
  for aa,bb in [('screw','knob'),('screw','knob_cap'),('knob','knob_cap')]:
   v=overlap(meshes[stem+'_'+aa],meshes[stem+'_'+bb])
   record(f'{i}_internal_{aa}_{bb}',[] if v<.01 else [dict(overlap_mm3=v)],overlap_mm3=v)
  # Fixed pose: test accessories individually against nearby real assembly.
  hits=[]
  for lab in members|{spacer}:
   for hit in coll(meshes[lab],members|{spacer,nut}):hits.append(dict(moving=lab,**hit))
  record(f'{i}_installed_clearance',hits)
  # Whole knob rotates with cap/head in small angle increments while rising;
  # intentional nut thread fit and whole member contacts are excluded.
  hits=[]
  for lift in [0,1.9,3.5,3.8]:
   for a in range(0,360,30):
    turn=dock@matrix([{'translate':[0,y,lift]},{'rotate':[0,0,a]},{'translate':[0,-y,0]}])@inv
    for lab in members:
     trial=meshes[lab].copy();trial.apply_transform(turn)
     for hit in coll(trial,members|{nut}):hits.append(dict(lift=lift,angle=a,moving=lab,**hit))
  record(f'{i}_knob_turning_sampled',hits,lifts=[0,1.9,3.5,3.8],angles_step_deg=30)
  # Fingers pinch the external quadrant; 9 mm ball is a partial finger model.
  hits=[]
  for lift in [0,1.9,3.5,3.8]:
   for x in [-10.3,10.3]:
    for distance in [8,12,16,20,24]:
     finger=trimesh.creation.icosphere(subdivisions=2,radius=4.5);finger.apply_translation([x,side*(52+distance),32.4+lift]);finger.apply_transform(dock)
     for hit in coll(finger,members):hits.append(dict(lift=lift,x=x,radial=distance,**hit))
  record(f'{i}_knob_fingertip_approach',hits,finger_diameter_mm=9,note='Partial soft fingertips intentionally overlap grasped knob; full finger body checked separately.')
  # An intentional small pad overlap models soft fingertip contact, not collision.
  for target,xs,z in [('knob',[-10.3,10.3],32.4),('spacer',[-17,-4],13.25)]:
   contact=[]
   for x in xs:
    tip=trimesh.creation.icosphere(subdivisions=2,radius=4.5)
    tip.apply_translation([x,side*60,z]);tip.apply_transform(dock)
    contact.append(overlap(tip,meshes[stem+'_'+target]))
   record(f'{i}_{target}_two_fingertip_contact',[] if min(contact)>.01 else contact,
    intentional_soft_contact_mm3=contact,note='Positive volume approximates soft-pad contact, not rigid interference.')
  # Simultaneous fingertips plus tapered 16 mm x 25 mm finger bodies.
  hits=[]
  for lift in [0,1.9,3.5,3.8]:
   for offset in [8,12,16,20,24]:
    bodies=[]
    for x in [-10.3,10.3]:
     parts=finger_envelope(x,side*(52+offset),32.4+lift,side)
     for part in parts:
      part.apply_transform(dock)
      for hit in coll(part,members):hits.append(dict(lift=lift,x=x,offset=offset,**hit))
     bodies.append(parts[0])
    v=overlap(*bodies)
    if v>.04:hits.append(dict(finger_pair_overlap=v))
  record(f'{i}_full_fingers_knob_approach',hits,tip_diameter_mm=9,body_diameter_mm=16,body_length_mm=25)
  hits=[]
  for d in np.arange(0,24.01,2):
   bodies=[]
   for x in [-10.3,10.3]:
    parts=finger_envelope(x,side*(60+d),36.2,side)
    for part in parts:
     part.apply_transform(dock)
     for hit in coll(part,members|{spacer}):hits.append(dict(travel=float(d),x=x,**hit))
    bodies.append(parts[0])
   v=overlap(*bodies)
   if v>.04:hits.append(dict(finger_pair_overlap=v))
  record(f'{i}_full_fingers_knob_withdraw',hits,step_mm=2)
  hits=[]
  raised={lab:dock[:3,2]*3.8 for lab in members}
  for d in np.arange(0,20.01,2):
   bodies=[]
   for n,x in enumerate([-17,-4]):
    parts=finger_envelope(x-d,side*60,13.25,side,(-.5 if n==0 else .5))
    for part in parts:
     part.apply_transform(dock)
     for hit in coll(part,{spacer},raised):hits.append(dict(travel=float(d),x=x,**hit))
    bodies.append(parts[0])
   v=overlap(*bodies)
   if v>.04:hits.append(dict(finger_pair_overlap=v))
  record(f'{i}_full_fingers_spacer_withdraw',hits,step_mm=2,note='Divergent finger bodies, +/-0.5 X per unit outward Y')
  # First remove U spacer after loosening, while bolt stays in place.
  hits=[]; move={lab:dock[:3,2]*3.8 for lab in members}
  for d in np.arange(0,20.01,1):
   q=meshes[spacer].copy();q.apply_translation(-dock[:3,0]*d)
   for hit in coll(q,{spacer},move):hits.append(dict(travel_mm=float(d),**hit))
  record(f'{i}_spacer_pull_sampled',hits,direction='dock -X',step_mm=1)
  hits=[]
  for d in np.arange(0,20.01,2):
   for x in [-17,-4]:
    finger=trimesh.creation.icosphere(subdivisions=2,radius=4.5);finger.apply_translation([x-d,side*60,13.25]);finger.apply_transform(dock)
    for hit in coll(finger,{spacer},move):hits.append(dict(travel_mm=float(d),x=x,**hit))
  record(f'{i}_spacer_fingertip_pull',hits,finger_diameter_mm=9,step_mm=2)
  # Only after spacer removal may the screw move sideways along the two slots.
  hits=[]
  for d in np.arange(0,24.01,1):
   for lab in members:
    q=meshes[lab].copy();q.apply_translation(dock[:3,2]*3.8+dock[:3,1]*side*d)
    for hit in coll(q,members|{spacer}):hits.append(dict(travel_mm=float(d),moving=lab,**hit))
  record(f'{i}_screw_radial_removal',hits,step_mm=1,unthreaded_tip_z=5.3)
  hits=[]
  for d in np.arange(0,24.01,2):
   for x in [-10.3,10.3]:
    finger=trimesh.creation.icosphere(subdivisions=2,radius=4.5);finger.apply_translation([x,side*(60+d),36.2]);finger.apply_transform(dock)
    for hit in coll(finger,members|{spacer}):hits.append(dict(travel_mm=float(d),x=x,**hit))
  record(f'{i}_screw_fingertip_pull',hits,finger_diameter_mm=9,step_mm=2)
  # Demonstrate contact/reactions separately from clearance.
  tests=[('head_floor',stem+'_screw',stem+'_knob',-dock[:3,2]*.1),('floor_male',stem+'_knob',mount,-dock[:3,2]*.1),('spacer_receiver',spacer,female,-dock[:3,2]*.1),('spacer_male',spacer,mount,dock[:3,2]*.1),('nut_roof',nut,female,dock[:3,2]*.1)]
  for label,moving,target,delta in tests:
   q=meshes[moving].copy();q.apply_translation(delta);v=overlap(q,meshes[target]);record(f'{i}_{label}',[] if v>.01 else [dict(overlap_mm3=v)],push_mm=.1,overlap_mm3=v)
  n=meshes[nut].copy();turn=dock@matrix([{'translate':[0,y,0]},{'rotate':[0,0,15]},{'translate':[0,-y,0]}])@inv;n.apply_transform(turn);v=overlap(n,meshes[female]);record(f'{i}_nut_rotation_reaction',[] if v>.01 else [dict(overlap_mm3=v)],angle_deg=15,overlap_mm3=v)
  # Barrier under upward pull: filled nut swept far through the roof.
  n=meshes[nut]; hull=trimesh.convex.convex_hull(np.vstack((n.vertices,n.vertices+dock[:3,2]*12)));v=overlap(hull,meshes[female]);record(f'{i}_nut_swept_roof',[] if v>.01 else [dict(overlap_mm3=v)],stroke_mm=12,overlap_mm3=v)
  local_nut=meshes[nut].copy();local_nut.apply_transform(inv);local_nut.apply_translation([0,0,-.4])
  vertices=local_nut.vertices
  sweep=trimesh.convex.convex_hull(np.vstack((vertices,vertices+np.array([0,side*25,0]))));sweep.apply_transform(dock)
  v=overlap(sweep,meshes[female]);record(f'{i}_nut_side_insertion_swept',[] if v<.04 else [dict(overlap_mm3=v)],overlap_mm3=v,distance_mm=25)
  tip=trimesh.creation.cylinder(radius=1.49,height=1.0,sections=32)
  tip.apply_translation([0,y,1]);tip.apply_transform(dock)
  v=overlap(tip,meshes[female]);record(f'{i}_screw_tip_clearance',[] if v<.04 else [dict(overlap_mm3=v)],overlap_mm3=v,tip_z=1.5,clearance_floor_z=.5)
  record(f'{i}_nominal_thread_engagement',[],nut_z=[2.4,4.8],tip_z=1.5,engagement_mm=2.4,protrusion_mm=.9,
   note='Nominal geometry, not confirmation of real fastener pitch or hardware tolerances.')
  # Geometric capture of hex screw, snap cap and printed floor.
  head=meshes[stem+'_screw'].copy();head.apply_transform(dock@matrix([{'translate':[0,y,0]},{'rotate':[0,0,15]},{'translate':[0,-y,0]}])@inv);v=overlap(head,meshes[stem+'_knob']);record(f'{i}_head_hex_torque_reaction',[] if v>.01 else [dict(overlap_mm3=v)],angle_deg=15,overlap_mm3=v)
  cap=meshes[stem+'_knob_cap'].copy();cap.apply_translation(dock[:3,2]*.2);v=overlap(cap,meshes[stem+'_knob']);record(f'{i}_cap_pull_reaction',[] if v>.005 else [dict(overlap_mm3=v)],pull_mm=.2,overlap_mm3=v)
 # Design-space check only: the nominal 0.6 mm radial separation of
 # the arc inner edge from the core exceeds the 0.15 mm radial snap interference.
 # This is not a deformable-solid simulation or physical insertion proof.
 record('cap_nominal_flex_space',[] if 4.1-3.5>.15 else ['insufficient gap'],
  gap_mm=4.1-3.5,required_radial_deflection_mm=.15,remaining_mm=(4.1-3.5)-.15,
  note='Nominal radial arithmetic; actual arm bending/strain and printed contact not simulated.')
 # The seated cap is clear; insertion and pull require its retaining nubs
 # to flex past the lip. Positive interference is expected over this range.
 cap_samples=[]
 for d in np.arange(0,.801,.05):
  q=meshes[pre+'0_knob_cap'].copy();q.apply_translation(dock[:3,2]*float(d))
  cap_samples.append([round(float(d),3),round(overlap(q,meshes[pre+'0_knob']),6)])
 record('cap_install_and_pull_barrier',[] if cap_samples[0][1]<.01 and max(v for d,v in cap_samples)>.01 else cap_samples,
  samples=cap_samples,note='Same reverse path for snap insertion; elastic accommodation and durability require physical testing.')
 # Camera removal after both hand assemblies and spacers removed, nuts stay.
 group='camera' if name=='parent_exterior' else 'child_camera'
 moving=[l for l,r in rows.items() if r.get('removal_group')==group and 'axial_' not in l]
 fixed=[l for l in rows if l not in moving and ('axial_' not in l or l.endswith('_nut'))]
 hits=[]
 for a,d in [(a,.6*a/60) for a in range(0,61,5)]+[(60,.6+t) for t in (5,10,20,40,80)]:
  T=dock@matrix([{'translate':[0,0,d]},{'rotate':[0,0,-a]}])@inv
  for label in moving:
   q=meshes[label].copy();q.apply_transform(T)
   for target in fixed:
    v=overlap(q,meshes[target])
    if v>.1:hits.append(dict(angle_deg=a,travel_mm=d,moving=label,part=target,mm3=v))
 record('camera_release_sampled',hits,rotation_step_deg=5)
 out=ROOT/'assemblies'/name/'_work/analysis'/os.environ.get('CAMERA_HAND_REPORT_DIR','camera_hand_release_20261029');out.mkdir(parents=True,exist_ok=True)
 after=hash_inputs()
 record('inputs_unchanged_during_run',[] if before==after else [x for x in before if before[x]!=after.get(x)])
 result=dict(passed=all(x['passed'] for x in checks),checks=checks,scope=name,input_sha256=before,
  limitations=['Discrete geometry samples only; not a continuous motion proof.','Finger proxy models tapered 9 mm fingertips expanding to 16 mm bodies, not complete hands or wet grip.','Physical print, snap fatigue, grip, material strength and creep are unverified.'])
 (out/'geometry_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 return result['passed']
if __name__=='__main__':
 names=sys.argv[1:] or ['parent_exterior','child_horizontal_plate_frame']
 raise SystemExit(0 if all(run(n) for n in names) else 1)
