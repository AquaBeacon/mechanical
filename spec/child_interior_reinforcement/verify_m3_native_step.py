import os,json
from pathlib import Path
import Part,Mesh
root=Path(os.environ['BODY_ROOT'])
p=root/'parts/child/interior/printed/child_vtray_batt_box/child_vtray_batt_box'
s=Part.read(str(p.with_suffix('.step')));m=Mesh.Mesh(str(p.with_suffix('.stl')))
r={'valid':s.isValid(),'solids':len(s.Solids),'step_volume_mm3':s.Volume,'mesh_volume_mm3':m.Volume,'relative_difference':abs(s.Volume-m.Volume)/m.Volume}
print(r,flush=True)
assert r['valid'] and r['solids']==1 and r['relative_difference']<0.005
(root/'assemblies/child_interior/_work/logs/m3_box_step_check.json').write_text(json.dumps(r,indent=2))
