"""FreeCAD CLI: read saved fixture STEPs and compare them with print STLs."""
import json,os,hashlib
from pathlib import Path
import Part,Mesh

root=Path(os.environ['ASM_ROOT'])
job=json.loads(Path(os.environ['CAMERA_STEP_JOB']).read_text(encoding='utf-8'))
checks=[]
for item in job['parts']:
    stem=root/item
    shape=Part.Shape();shape.read(str(stem.with_suffix('.step')))
    mesh=Mesh.Mesh(str(stem.with_suffix('.stl')))
    names=['XMin','YMin','ZMin','XMax','YMax','ZMax']
    delta=max(abs(getattr(shape.BoundBox,k)-getattr(mesh.BoundBox,k)) for k in names)
    vol=abs(abs(shape.Volume)-abs(mesh.Volume))/max(abs(mesh.Volume),1e-9)
    checks.append(dict(part=item,stl_sha256=hashlib.sha256(stem.with_suffix('.stl').read_bytes()).hexdigest(),step_sha256=hashlib.sha256(stem.with_suffix('.step').read_bytes()).hexdigest(),valid=shape.isValid(),solids=len(shape.Solids),
        bounds_delta_mm=delta,relative_volume_error=vol,
        passed=shape.isValid() and len(shape.Solids)==1 and delta<.01 and vol<.0025))
out=dict(passed=all(r['passed'] for r in checks),checks=checks)
Path(os.environ['CAMERA_STEP_REPORT']).write_text(json.dumps(out,indent=2),encoding='utf-8')
if not out['passed']:raise RuntimeError('Fixture STEP/STL mismatch')
print('Saved STEP/STL checks PASS',len(checks))
