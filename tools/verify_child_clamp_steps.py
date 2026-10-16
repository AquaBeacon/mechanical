"""FreeCAD CLI: compare only this clamp's exported STEP bounds and volume."""
import json
import hashlib
import os
from pathlib import Path
import Part
import Mesh

root=Path(os.environ["ASM_ROOT"])
folder=root/"parts/child/exterior/printed/child_wte4_suspension_clamp"
folder=Path(os.environ.get('CLAMP_STEP_FOLDER',str(folder)))
results=[]
names=["child_wte4_suspension_clamp_half","child_wte4_suspension_clamp_liner"]
smooth="child_wte4_suspension_clamp_smooth"
if (folder/(smooth+".step")).exists():
    names.append(smooth)
if 'CLAMP_STEP_NAMES' in os.environ:
    names=json.loads(os.environ['CLAMP_STEP_NAMES'])
for name in names:
    s=Part.read(str(folder/(name+".step")))
    m=Mesh.Mesh(str(folder/(name+".stl")))
    sb,mb=s.BoundBox,m.BoundBox
    sd=[sb.XMin,sb.YMin,sb.ZMin,sb.XMax,sb.YMax,sb.ZMax]
    md=[mb.XMin,mb.YMin,mb.ZMin,mb.XMax,mb.YMax,mb.ZMax]
    dv=abs(s.Volume-m.Volume)/abs(m.Volume)
    err=max(abs(a-b) for a,b in zip(sd,md))
    results.append(dict(name=name,step_sha256=hashlib.sha256((folder/(name+'.step')).read_bytes()).hexdigest(),
                        stl_sha256=hashlib.sha256((folder/(name+'.stl')).read_bytes()).hexdigest(),
                        valid=s.isValid(),solid_count=len(s.Solids),shell_count=len(s.Shells),step_volume_mm3=s.Volume,
                        stl_volume_mm3=m.Volume,relative_volume_error=dv,max_bound_error_mm=err,
                        pass_check=bool(s.isValid() and len(s.Solids)==1 and len(s.Shells)==1 and err<0.1 and dv<0.02)))
out=dict(parts=results,pass_check=all(i["pass_check"] for i in results))
Path(os.environ.get("CLAMP_STEP_CHECKS",str(folder/"_work/analysis/step_checks.json"))).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps(out,indent=2))
if not out["pass_check"]:
    raise RuntimeError("STEP/STL mismatch")
