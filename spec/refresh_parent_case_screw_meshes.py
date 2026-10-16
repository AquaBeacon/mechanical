"""Remesh canonical current STEP files, preserving floor bytes exactly."""
from pathlib import Path
import sys,json,hashlib
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'spec'))
from parent_access_common import mesh_volume
O=R/'assemblies/parent_hand_service';D=O/'_work/analysis/case_screw_access_20261012'
if '--battery-slide-lid' in sys.argv:D=O/'_work/analysis/battery_slide_lid_20261012'
if '--battery-child-reference' in sys.argv:D=O/'_work/analysis/battery_child_reference_20261012'
if '--battery-tool-nut' in sys.argv:D=O/'_work/analysis/battery_tool_nut_access_20261013'
if '--battery-side-grooves' in sys.argv:D=O/'_work/analysis/battery_side_grooves_20261013'
W=O/'_work/intermediate/case_screw_remesh';W.mkdir(parents=True,exist_ok=True)
baseline=json.loads((D/'baseline.json').read_text(encoding='utf-8'))
placement=json.loads((O/'placement.json').read_text(encoding='utf-8'))
config=json.loads((O/'print_config.json').read_text(encoding='utf-8'))
files=set()
for it in placement['items']+config.get('extra_parts',[]):
    if '/printed/' not in it['part']:continue
    p=R/it['part'];stem=it.get('file',p.name)
    if stem in json.loads((p/'manufacturing.json').read_text(encoding='utf-8')).get('non_print_files',[]):continue
    files.add(p/(stem+'.step'))
rows=[]
for p in sorted(files):
    s=Part.read(str(p));assert s.isValid() and len(s.Solids)==1,p
    mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.025,AngularDeflection=.10,Relative=False)
    assert mesh.isSolid(),p
    b=s.optimalBoundingBox(False,False)
    delta=max(abs(getattr(b,k)-getattr(mesh.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
    vol=abs(s.Volume-mesh_volume(mesh))/s.Volume;assert delta<.05 and vol<.02,(p,delta,vol)
    target=W/p.with_suffix('.stl').name;mesh.write(str(target))
    sha=hashlib.sha256(target.read_bytes()).hexdigest()
    if p.stem=='floor_plate':
        assert sha==baseline[p.with_suffix('.stl').relative_to(R).as_posix()], 'Floor remesh differs: preserve original and investigate'
    p.with_suffix('.stl').write_bytes(target.read_bytes())
    rows.append(dict(part=p.relative_to(R).as_posix(),closed_stl=True,bbox_delta_mm=delta,relative_volume_delta=vol,sha256=sha))
(D/'mesh_checks.json').write_text(json.dumps(dict(status='PASS',checks=rows),indent=2),encoding='utf-8')
print('PASS',len(rows),'current print meshes; floor bytes unchanged',flush=True)
