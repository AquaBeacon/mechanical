"""Orient only the changed rear; preserve the already printed front artifacts."""
from pathlib import Path
import hashlib,json,math
import trimesh
R=Path(__file__).resolve().parents[1]
A=R/'assemblies/child_simple_assembly'
for entry in json.loads((A/'revisions/r2_before_light/front_hashes.json').read_text(encoding='utf-8-sig')):
    assert hashlib.sha256(Path(entry['Path']).read_bytes()).hexdigest().upper()==entry['Hash']
p=R/'parts/child/exterior/printed/child_simple_rear/child_simple_rear.stl'
m=trimesh.load(p,force='mesh')
assert m.is_watertight and m.is_winding_consistent and len(m.split())==1
record=dict(watertight=True,winding_consistent=True,components=1,bbox_mm=m.extents.tolist(),bounds_mm=m.bounds.tolist(),volume_cm3=m.volume/1000,revision='r3_rear_light',fea_status='not_run_for_r3')
data=json.loads((A/'mesh_checks.json').read_text())
data['parts']['child_simple_rear']=record
(A/'mesh_checks.json').write_text(json.dumps(data,indent=2))
m.apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2,[1,0,0]))
m.apply_translation(-m.bounds[0])
assert max(m.extents)<250
m.export(R/'print_jobs/child_simple/child_simple_rear_print.stl')
print(record)
