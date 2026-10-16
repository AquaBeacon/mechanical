"""M3-only fasteners, exposed pan-head reserves, and bed plane checks."""
import json,sys
from pathlib import Path
import numpy as np
import trimesh
sys.path.insert(0,str(Path('scad/lib').resolve()))
from check_asm_contacts import load
from verify_child_interior import matrix
items=json.loads(Path('assemblies/child_interior/placement.json').read_text(encoding='utf-8'))['items']
solids={it['label']:load(Path('.'),it) for it in items if '/cots/screw' not in it['part'] and 'harness' not in it['label']}
for m in solids.values():m.fix_normals()
errors=[];heads=[]
for it in items:
 if '/cots/screw' not in it['part']:continue
 if it['file']=='screw_nut_m3':continue # plain purchased captive nuts have no pan head
 if not it['file'].startswith('screw_m3'):
  errors.append({'non_m3':it['label']});continue
 if it['file'].endswith('_flat'):continue # existing 5.8 mm conical seat and tool checked separately
 head=trimesh.creation.cylinder(radius=3.3,height=2,sections=64)
 head.apply_translation([0,0,1]);head.apply_transform(matrix(it['ops']))
 for name,m in solids.items():
  if np.any(head.bounds[0]>=m.bounds[1]-0.001) or np.any(m.bounds[0]>=head.bounds[1]-0.001):continue
  c=trimesh.boolean.intersection([head,m],engine='manifold',check_volume=False)
  v=abs(c.volume) if len(c.faces) else 0
  heads.append({'head':it['label'],'other':name,'reserved_volume_overlap_mm3':float(v)})
  if v>0.01:errors.append(heads[-1])
bed=[]
for part,angle in [('child_vtray_deck/child_vtray_deck_t200',90),('child_flange_brace/child_flange_brace',0),('child_vtray_batt_box/child_vtray_batt_box',-90),('child_vtray_batt_floor/child_vtray_batt_floor',90),('child_rx_edge_clamp/child_rx_edge_clamp_base_pair',-90),('child_rx_edge_clamp/child_rx_edge_clamp_cap_pair',90)]:
 m=trimesh.load(Path('parts/child/interior/printed')/(part+'.stl'),force='mesh');m.fix_normals()
 assert m.is_volume and len(m.split())==1,part
 m.apply_transform(matrix([{'rotate':[angle,0,0]}]))
 z0=float(m.bounds[0,2]);normals=m.face_normals
 flat=(normals[:,2]<-0.999)&(np.max(m.triangles[:,:,2],axis=1)<z0+0.015)
 area=float(m.area_faces[flat].sum())
 bed.append({'part':part,'bed_area_mm2':area,'rotation_x':angle})
 if area<5:errors.append({'no_flat_bed':part})
report={'errors':errors,'pan_head_reserve_d_mm':6.6,'flat_head_seat_d_mm':5.8,'heads':heads,'bed':bed}
Path('assemblies/child_interior/_work/logs/m3_print_check.json').write_text(json.dumps(report,indent=2))
print('errors',errors,'pan head checks',len(heads),'bed',bed)
sys.exit(bool(errors))
