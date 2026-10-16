import FreeCAD as App, Part,Mesh,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assemblies/parent_service_review'
checks=[]
for folder,name in [('parts/parent/interior/printed/parent_plate_service','parent_plate_service'),('parts/parent/interior/cots/spresense_service_stack','spresense_service_stack')]:
 s=Part.read(str(ROOT/folder/(name+'.step')));m=Mesh.Mesh(str(ROOT/folder/(name+'.stl')))
 a,b=s.BoundBox,m.BoundBox
 diff=max(abs(getattr(a,k)-getattr(b,k)) for k in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])
 rel=abs(s.Volume-m.Volume)/s.Volume
 checks.append(dict(part=name,bbox_difference_mm=diff,relative_volume_difference=rel,valid_step=s.isValid(),closed_stl=m.isSolid()))
 print(checks[-1],flush=True)
 assert diff<.05 and rel<.02
os.environ['ASM_JSON']=str(OUT/'placement.json');os.environ['ASM_ROOT']=str(ROOT);os.environ['STEP_IN']=str(OUT/'parent_service_review.step')
exec((ROOT/'scad/lib/verify_asm_step.py').read_text(encoding='utf-8'))
(OUT/'step_stl_checks.json').write_text(json.dumps(checks,indent=2))
