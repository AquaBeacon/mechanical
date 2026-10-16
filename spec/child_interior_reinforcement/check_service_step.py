import os,json,Part
from pathlib import Path
root=Path(os.environ['BODY_ROOT']);r=[]
for n in ['child_vtray_batt_box','child_vtray_batt_floor']:
 p=root/'parts/child/interior/printed'/n/(n+'.step');s=Part.Shape();s.read(str(p))
 r.append({'part':n,'valid':s.isValid(),'solids':len(s.Solids),'volume_mm3':s.Volume})
 assert s.isValid() and len(s.Solids)==1,n
print(json.dumps(r))
(root/'spec/child_interior_reinforcement/service_step_check.json').write_text(json.dumps(r,indent=2))
