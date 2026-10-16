"""Check above-deck Allen-key shafts against actual component STEP solids."""
import FreeCAD as A,Part,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
d=json.loads((O/'service_placement.json').read_text(encoding='utf-8'))
targets=['plate','p_main','spresense','box_bcas212310g','lift_carrier','p_pwr','tx_improved']
shapes={}
for it in d['items']:
 if it['label'] not in targets:continue
 s=Part.read(str(R/it['part']/(it.get('file',Path(it['part']).name)+'.step')))
 for op in reversed(it['ops']):
  if 'rotate' in op:
   for axis,angle in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],op['rotate']):s.rotate(A.Vector(0,0,0),axis,angle)
  if 'translate' in op:s.translate(A.Vector(*op['translate']))
 shapes[it['label']]=s
results=[]
for i,(x,y) in enumerate(d['service_prop_centres_mm']):
 for j,dy in enumerate([-9,9]):
  shaft=Part.makeCylinder(1.6,100,A.Vector(x,y+dy,123.3))
  collisions=[]
  for k,s in shapes.items():
   if s.BoundBox.intersect(shaft.BoundBox):
    volume=s.common(shaft).Volume
    if volume>.1:collisions.append(dict(part=k,volume_mm3=volume))
  results.append(dict(screw=f'{i}_{j}',axis_mm=[x,y+dy,123.3],tool_shaft_diameter_mm=3.2,above_head_length_mm=100,collisions=collisions))
floor_case_overlap=shapes['plate'].common(shapes['box_bcas212310g']).Volume
report=dict(floor_case_intersection_mm3=floor_case_overlap,status='PASS' if all(not x['collisions'] for x in results) and floor_case_overlap<.1 else 'FAIL',scope='Straight tool-shaft clearance only; actual tightening/preload, grip and captive-nut retention not verified.',checks=results,service_step_sha256=hashlib.sha256((O/'service.step').read_bytes()).hexdigest())
(O/'service_tool_access.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['status'],len(results),'tool shafts')
assert report['status']=='PASS'

